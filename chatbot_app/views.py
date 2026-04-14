import json
import re
from datetime import datetime

from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from django.utils import timezone

from .matcher import get_best_match
from .booking_flow import (
    process_booking_turn,
    is_booking_intent,
    has_active_booking_session,
    format_booking_json,
)
from consultation_app.models import Availability, Appointment
from auth_app.models import User


_CHATBOT_REPEAT_COUNTS_SESSION_KEY = "chatbot_repeat_query_counts"
_CHATBOT_REPEAT_COUNTS_LIMIT = 40
_CHATBOT_TEMPLATE_PREFS_SESSION_KEY = "chatbot_response_template_prefs"
_CHATBOT_RESPONSE_MODES = {"short", "medium", "detailed"}
_CHATBOT_LANGUAGE_STYLES = {"english", "hinglish"}


def chatbot_page(request):
    """Redirect to homepage — chatbot is now a modal overlay in base.html."""
    return redirect('/?chatbot=open')


def _normalize_chatbot_query_key(message: str) -> str:
    text = (message or "").lower().strip()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:120]


def _get_chatbot_repeat_count(request, message: str) -> int:
    """
    Returns how many times the same normalized query was already asked in this session.
    First time => 0, second time => 1, etc.
    """
    key = _normalize_chatbot_query_key(message)
    if not key:
        return 0

    counts = request.session.get(_CHATBOT_REPEAT_COUNTS_SESSION_KEY, {})
    if not isinstance(counts, dict):
        counts = {}

    previous_count = int(counts.get(key, 0) or 0)
    counts[key] = min(previous_count + 1, 99)

    while len(counts) > _CHATBOT_REPEAT_COUNTS_LIMIT:
        oldest_key = next(iter(counts))
        counts.pop(oldest_key, None)

    request.session[_CHATBOT_REPEAT_COUNTS_SESSION_KEY] = counts
    return previous_count


def _normalize_response_mode(value: str | None) -> str:
    mode = str(value or "").strip().lower()
    return mode if mode in _CHATBOT_RESPONSE_MODES else "medium"


def _normalize_language_style(value: str | None) -> str:
    style = str(value or "").strip().lower().replace("_", "-")
    if style in {"hinglish", "hindi-english", "mix", "mixed"}:
        return "hinglish"
    return "english"


def _get_chatbot_template_prefs(request):
    prefs = request.session.get(_CHATBOT_TEMPLATE_PREFS_SESSION_KEY, {})
    if not isinstance(prefs, dict):
        prefs = {}
    return {
        "response_mode": _normalize_response_mode(prefs.get("response_mode")),
        "language_style": _normalize_language_style(prefs.get("language_style")),
    }


def _set_chatbot_template_prefs(request, *, response_mode=None, language_style=None):
    prefs = _get_chatbot_template_prefs(request)
    if response_mode is not None:
        prefs["response_mode"] = _normalize_response_mode(response_mode)
    if language_style is not None:
        prefs["language_style"] = _normalize_language_style(language_style)
    request.session[_CHATBOT_TEMPLATE_PREFS_SESSION_KEY] = prefs
    return prefs


def _handle_template_pref_command(request, message: str):
    """
    Supports lightweight chat commands without UI controls:
      - mode short|medium|detailed
      - style english|hinglish
      - format short hinglish
      - response mode detailed
    """
    text = (message or "").strip().lower()
    if not text:
        return None
    normalized = re.sub(r"\s+", " ", text)

    mode_match = re.match(
        r"^(?:/bot\s+)?(?:set\s+)?(?:response\s+)?mode\s+(short|medium|detailed)$",
        normalized,
    )
    if mode_match:
        prefs = _set_chatbot_template_prefs(request, response_mode=mode_match.group(1))
        return (
            "<b>Response format updated.</b><br>"
            f"Mode: <b>{prefs['response_mode']}</b><br>"
            f"Style: <b>{prefs['language_style']}</b><br>"
            "<small>Tip: use <code>style hinglish</code> or <code>style english</code>.</small>"
        )

    style_match = re.match(
        r"^(?:/bot\s+)?(?:set\s+)?style\s+(english|hinglish|hindi-english|mix|mixed)$",
        normalized,
    )
    if style_match:
        prefs = _set_chatbot_template_prefs(request, language_style=style_match.group(1))
        return (
            "<b>Language style updated.</b><br>"
            f"Mode: <b>{prefs['response_mode']}</b><br>"
            f"Style: <b>{prefs['language_style']}</b><br>"
            "<small>Tip: use <code>mode short</code>, <code>mode medium</code>, or <code>mode detailed</code>.</small>"
        )

    format_match = re.match(
        r"^(?:/bot\s+)?(?:set\s+)?format\s+(short|medium|detailed)(?:\s+(english|hinglish|hindi-english|mix|mixed))?$",
        normalized,
    )
    if format_match:
        prefs = _set_chatbot_template_prefs(
            request,
            response_mode=format_match.group(1),
            language_style=format_match.group(2) if format_match.group(2) else None,
        )
        return (
            "<b>Chatbot response template updated.</b><br>"
            f"Mode: <b>{prefs['response_mode']}</b><br>"
            f"Style: <b>{prefs['language_style']}</b><br>"
            "<small>Examples: <code>format detailed hinglish</code>, <code>mode short</code>, <code>style english</code>.</small>"
        )

    if normalized in {"show format", "format status", "response format", "/bot format"}:
        prefs = _get_chatbot_template_prefs(request)
        return (
            "<b>Current chatbot response template</b><br>"
            f"Mode: <b>{prefs['response_mode']}</b><br>"
            f"Style: <b>{prefs['language_style']}</b><br>"
            "<small>Commands: <code>mode short|medium|detailed</code>, "
            "<code>style english|hinglish</code>, <code>format detailed hinglish</code></small>"
        )

    return None


@require_POST
def chatbot_reply(request):
    message = request.POST.get("msg", "").strip()
    if not message:
        return JsonResponse({"error": "Message is required."}, status=400)

    # Optional direct overrides from frontend (future UI buttons can use these).
    posted_mode = request.POST.get("response_mode")
    posted_style = request.POST.get("language_style")
    if posted_mode or posted_style:
        _set_chatbot_template_prefs(
            request,
            response_mode=posted_mode if posted_mode else None,
            language_style=posted_style if posted_style else None,
        )

    pref_command_reply = _handle_template_pref_command(request, message)
    if pref_command_reply is not None:
        return HttpResponse(pref_command_reply)

    booking_session_id = request.session.get("chatbot_booking_session_id")
    if is_booking_intent(message) or has_active_booking_session(booking_session_id):
        booking_turn = process_booking_turn(
            message,
            session_id=booking_session_id,
            user=request.user if request.user.is_authenticated else None,
        )
        request.session["chatbot_booking_session_id"] = booking_turn["sessionId"]

        # If booking details are complete and patient is logged in, auto-create appointment.
        if booking_turn.get("status") == "ready" and booking_turn.get("bookingData"):
            if not request.user.is_authenticated:
                return HttpResponse(
                    booking_turn["reply"]
                    + "<br><br>Please log in to complete booking."
                )
            if not _is_patient(request.user):
                return HttpResponse(
                    booking_turn["reply"]
                    + "<br><br>Only patient accounts can create appointments."
                )
            booking_result, status_code = _create_ai_appointment_from_payload(
                request.user,
                booking_turn["bookingData"],
            )
            if status_code == 201:
                return HttpResponse(booking_result["confirmationMessage"])
            return HttpResponse(
                "I collected your details, but I could not complete booking right now: "
                + booking_result.get("error", "Unknown error")
            )

        return HttpResponse(booking_turn["reply"])

    repeat_count = _get_chatbot_repeat_count(request, message)
    prefs = _get_chatbot_template_prefs(request)
    answer = get_best_match(
        message,
        repeat_count=repeat_count,
        response_mode=prefs["response_mode"],
        language_style=prefs["language_style"],
    )
    return HttpResponse(answer)


def _is_patient(user):
    if getattr(user, "role", None) == "PATIENT":
        return True
    is_patient_attr = getattr(user, "is_patient", None)
    return is_patient_attr() if callable(is_patient_attr) else bool(is_patient_attr)


def _parse_iso_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except (TypeError, ValueError):
        return None


def _parse_hhmm_time(time_str):
    try:
        return datetime.strptime(time_str, "%H:%M").time()
    except (TypeError, ValueError):
        return None


def _required_booking_fields_missing(payload):
    required = [
        "name",
        "age",
        "gender",
        "contactNumber",
        "symptoms",
        "doctorSpecialization",
        "preferredDate",
        "preferredTime",
        "location",
        "visitType",
    ]
    return [field for field in required if payload.get(field) in (None, "")]


def _create_ai_appointment_from_payload(patient_user, payload):
    """
    Creates appointment from validated AI booking payload.
    Returns (response_dict, http_status_code).
    """
    missing = _required_booking_fields_missing(payload)
    if missing:
        return {"error": f"Missing required fields: {', '.join(missing)}"}, 400

    preferred_date = _parse_iso_date(payload.get("preferredDate"))
    preferred_time = _parse_hhmm_time(payload.get("preferredTime"))
    if not preferred_date:
        return {"error": "Invalid preferredDate. Use YYYY-MM-DD."}, 400
    if not preferred_time:
        return {"error": "Invalid preferredTime. Use HH:MM."}, 400
    if preferred_date < timezone.localdate():
        return {"error": "Preferred date cannot be in the past."}, 400

    try:
        age = int(str(payload.get("age")).strip())
    except (TypeError, ValueError):
        return {"error": "Age must be numeric."}, 400
    if age < 1 or age > 120:
        return {"error": "Age must be between 1 and 120."}, 400

    # Sync patient profile basics from collected conversational data.
    patient_name = str(payload.get("name", "")).strip()
    contact_number = str(payload.get("contactNumber", "")).strip()
    location = str(payload.get("location", "")).strip()
    first_name, _, last_name = patient_name.partition(" ")
    if first_name:
        patient_user.first_name = first_name
        patient_user.last_name = last_name.strip()
        patient_user.save(update_fields=["first_name", "last_name"])
    profile = getattr(patient_user, "profile", None)
    if profile:
        profile.phone_number = contact_number
        profile.address = location
        profile.save(update_fields=["phone_number", "address"])

    specialization = str(payload.get("doctorSpecialization", "")).strip()
    specialization_filter = "general" if specialization.lower() == "general physician" else specialization
    symptom_text = str(payload.get("symptoms", "")).strip()
    visit_type = str(payload.get("visitType", "")).strip()

    # Prefer exact/near-time slots for doctors matching specialization and optional location.
    slot_qs = (
        Availability.objects.select_related("doctor", "doctor__doctor_profile", "doctor__profile")
        .filter(
            date=preferred_date,
            is_booked=False,
            doctor__role=User.Role.DOCTOR,
            doctor__is_active=True,
            doctor__doctor_profile__specialty__icontains=specialization_filter,
        )
        .order_by("start_time", "id")
    )
    if location:
        slot_qs = slot_qs.filter(doctor__profile__address__icontains=location)

    slots = list(slot_qs)
    if not slots:
        # Relax location filter first, then specialization fallback to General Physician.
        slots = list(
            Availability.objects.select_related("doctor", "doctor__doctor_profile", "doctor__profile")
            .filter(
                date=preferred_date,
                is_booked=False,
                doctor__role=User.Role.DOCTOR,
                doctor__is_active=True,
            )
            .filter(
                doctor__doctor_profile__specialty__icontains=specialization_filter
            )
            .order_by("start_time", "id")
        )
    if not slots and specialization.lower() != "general physician":
        slots = list(
            Availability.objects.select_related("doctor", "doctor__doctor_profile", "doctor__profile")
            .filter(
                date=preferred_date,
                is_booked=False,
                doctor__role=User.Role.DOCTOR,
                doctor__is_active=True,
                doctor__doctor_profile__specialty__icontains="general",
            )
            .order_by("start_time", "id")
        )
    if not slots:
        return {"error": "No available doctors found for the selected date/time and specialization."}, 409

    preferred_minutes = preferred_time.hour * 60 + preferred_time.minute

    def slot_rank(slot):
        slot_minutes = slot.start_time.hour * 60 + slot.start_time.minute
        return (abs(slot_minutes - preferred_minutes), slot_minutes)

    best_slot = sorted(slots, key=slot_rank)[0]

    with transaction.atomic():
        try:
            locked_slot = Availability.objects.select_for_update().select_related("doctor").get(
                id=best_slot.id, is_booked=False
            )
        except Availability.DoesNotExist:
            return {"error": "Selected slot became unavailable. Please try another time."}, 409

        appointment = Appointment.objects.create(
            patient=patient_user,
            doctor=locked_slot.doctor,
            availability=locked_slot,
            appointment_date=locked_slot.date,
            appointment_time=locked_slot.start_time,
            status=Appointment.Status.REQUESTED,
            reason=f"{visit_type} visit. Symptoms: {symptom_text}",
            notes=json.dumps(
                {
                    "aiBooking": True,
                    "age": age,
                    "gender": payload.get("gender"),
                    "contactNumber": contact_number,
                    "visitType": visit_type,
                    "emergency": bool(payload.get("emergency", False)),
                }
            ),
        )
        locked_slot.is_booked = True
        locked_slot.save(update_fields=["is_booked"])

    doctor_name = locked_slot.doctor.get_full_name() or locked_slot.doctor.email
    doctor_specialization = (
        getattr(getattr(locked_slot.doctor, "doctor_profile", None), "specialty", None)
        or specialization
    )

    response = {
        "appointmentId": str(appointment.id),
        "doctorName": doctor_name,
        "doctorSpecialization": doctor_specialization,
        "date": appointment.appointment_date.isoformat(),
        "time": appointment.appointment_time.strftime("%H:%M"),
        "status": appointment.status,
        "detailUrl": appointment.get_absolute_url(),
        "confirmationMessage": (
            f"Your appointment with Dr. {doctor_name}, {doctor_specialization}, "
            f"is confirmed on {appointment.appointment_date.isoformat()} at "
            f"{appointment.appointment_time.strftime('%H:%M')}. "
            f"Your Appointment ID is {appointment.id}."
        ),
    }
    return response, 201


@require_POST
@login_required
@user_passes_test(_is_patient)
def chatbot_quick_book(request):
    """
    Create an appointment directly from the chatbot given an availability slot.
    Expected POST fields:
      - availability_id (required): ID of Availability to book
      - reason (optional): text reason
    """
    availability_id = request.POST.get("availability_id")
    reason = request.POST.get("reason", "").strip()

    if not availability_id:
        return JsonResponse({"success": False, "error": "availability_id is required."}, status=400)

    try:
        availability_id_int = int(availability_id)
    except ValueError:
        return JsonResponse({"success": False, "error": "availability_id must be an integer."}, status=400)

    with transaction.atomic():
        try:
            slot = (
                Availability.objects.select_for_update()
                .select_related("doctor")
                .get(id=availability_id_int, is_booked=False)
            )
        except Availability.DoesNotExist:
            return JsonResponse({"success": False, "error": "Slot not available."}, status=404)

        appointment = Appointment.objects.create(
            patient=request.user,
            doctor=slot.doctor,
            availability=slot,
            appointment_date=slot.date,
            appointment_time=slot.start_time,
            status=Appointment.Status.REQUESTED,
            reason=reason or "Booked via chatbot quick-book",
        )
        slot.is_booked = True
        slot.save(update_fields=["is_booked"])

    return JsonResponse(
        {
            "success": True,
            "appointment_id": str(appointment.id),
            "doctor": slot.doctor.get_full_name(),
            "date": slot.date.isoformat(),
            "time": slot.start_time.strftime("%H:%M"),
            "detail_url": appointment.get_absolute_url(),
        }
    )


@require_POST
@login_required
@user_passes_test(_is_patient)
def ai_booking_converse(request):
    """
    Conversational AI booking endpoint.
    Accepts JSON or form data:
      - message (required)
      - sessionId (optional; returned on first turn)
    Returns booking conversation state and final booking confirmation when completed.
    """
    if request.content_type and "application/json" in request.content_type:
        try:
            body = json.loads(request.body.decode("utf-8") or "{}")
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON body."}, status=400)
        message = str(body.get("message", "")).strip()
        session_id = body.get("sessionId")
    else:
        message = request.POST.get("message", "").strip()
        session_id = request.POST.get("sessionId")

    if not message:
        return JsonResponse({"error": "message is required."}, status=400)

    turn = process_booking_turn(message, session_id=session_id, user=request.user)

    # Auto-create appointment once all required fields are collected.
    if turn.get("status") == "ready" and turn.get("bookingData"):
        booking_result, status_code = _create_ai_appointment_from_payload(
            request.user,
            turn["bookingData"],
        )
        if status_code == 201:
            turn["status"] = "booked"
            turn["appointment"] = booking_result
            turn["reply"] = booking_result["confirmationMessage"]
        else:
            turn["status"] = "error"
            turn["bookingError"] = booking_result
            turn["reply"] = (
                "I collected all required details, but booking could not be completed: "
                + booking_result.get("error", "Unknown error")
            )
        return JsonResponse(turn, status=status_code if status_code != 201 else 200)

    return JsonResponse(turn)


@require_POST
@login_required
@user_passes_test(_is_patient)
def api_create_appointment(request):
    """
    POST /api/appointments
    Creates appointment from structured AI booking JSON payload.
    """
    try:
        payload = json.loads(request.body.decode("utf-8") or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON body."}, status=400)

    # Accept wrapper payloads like {"bookingData": {...}}
    if "bookingData" in payload and isinstance(payload["bookingData"], dict):
        payload = payload["bookingData"]

    # Normalize to required exact shape if possible.
    payload = format_booking_json(payload)
    result, status_code = _create_ai_appointment_from_payload(request.user, payload)
    return JsonResponse(result, status=status_code)

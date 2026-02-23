import re
import uuid
from datetime import datetime

from django.core.cache import cache
from django.utils import timezone


SESSION_TTL_SECONDS = 60 * 60
CACHE_KEY_PREFIX = "chatbot_booking_session:"

FIELD_ORDER = [
    "name",
    "age",
    "gender",
    "contactNumber",
    "symptoms",
    "preferredDate",
    "preferredTime",
    "location",
    "visitType",
]

FIELD_PROMPTS = {
    "name": "Please share the patient's full name.",
    "age": "What is the patient's age?",
    "gender": "What is the patient's gender? (Male / Female / Other)",
    "contactNumber": "Please share a contact number.",
    "symptoms": "What symptoms or reason for visit would you like the doctor to check?",
    "preferredDate": "What is your preferred appointment date? (YYYY-MM-DD)",
    "preferredTime": "What is your preferred time? (e.g., 10:30 AM)",
    "location": "Which city or location do you prefer?",
    "visitType": "Is this a First-time visit or a Follow-up?",
}

EMERGENCY_KEYWORDS = [
    "chest pain",
    "breathing issue",
    "shortness of breath",
    "breathlessness",
    "difficulty breathing",
    "severe bleeding",
    "unconscious",
    "fainted",
    "stroke",
    "seizure",
    "heart attack",
]

SPECIALIZATION_RULES = [
    ("Cardiologist", ["chest pain", "heart", "palpitation", "bp", "blood pressure"]),
    ("Pulmonologist", ["breathing", "asthma", "cough", "wheezing", "lungs"]),
    ("Dermatologist", ["skin", "rash", "acne", "itching", "eczema", "psoriasis"]),
    ("Neurologist", ["headache", "migraine", "seizure", "numbness", "brain", "stroke"]),
    ("Orthopedic", ["bone", "joint", "knee", "back pain", "fracture", "shoulder pain"]),
    ("ENT Specialist", ["ear", "nose", "throat", "sinus", "tonsil", "hearing"]),
    ("Gynecologist", ["period", "pregnancy", "pcos", "uterus", "vaginal"]),
    ("Urologist", ["urine", "kidney", "uti", "bladder", "prostate"]),
    ("Gastroenterologist", ["stomach", "abdomen", "acidity", "gas", "constipation", "diarrhea"]),
    ("Psychiatrist", ["anxiety", "depression", "panic", "mental health", "insomnia"]),
    ("Pediatrician", ["child", "baby", "infant", "kid", "vaccination"]),
    ("General Physician", []),
]

GENDER_VALUES = {
    "male": "Male",
    "m": "Male",
    "female": "Female",
    "f": "Female",
    "other": "Other",
}

VISIT_TYPE_VALUES = {
    "first": "First-time",
    "first-time": "First-time",
    "first time": "First-time",
    "new": "First-time",
    "follow": "Follow-up",
    "follow-up": "Follow-up",
    "follow up": "Follow-up",
}


def _cache_key(session_id):
    return f"{CACHE_KEY_PREFIX}{session_id}"


def _default_state(user=None):
    state = {
        "data": {
            "name": "",
            "age": "",
            "gender": "",
            "contactNumber": "",
            "symptoms": "",
            "doctorSpecialization": "",
            "preferredDate": "",
            "preferredTime": "",
            "location": "",
            "visitType": "",
            "emergency": False,
        },
        "started": True,
        "completed": False,
        "emergencyWarningShown": False,
        "lastUpdated": timezone.now().isoformat(),
    }

    if user and getattr(user, "is_authenticated", False):
        full_name = (user.get_full_name() or "").strip()
        if full_name:
            state["data"]["name"] = full_name
        profile = getattr(user, "profile", None)
        if profile:
            phone = (getattr(profile, "phone_number", None) or "").strip()
            if phone:
                state["data"]["contactNumber"] = phone
            address = (getattr(profile, "address", None) or "").strip()
            if address:
                state["data"]["location"] = address
    return state


def load_state(session_id):
    if not session_id:
        return None
    return cache.get(_cache_key(session_id))


def save_state(session_id, state):
    state["lastUpdated"] = timezone.now().isoformat()
    cache.set(_cache_key(session_id), state, SESSION_TTL_SECONDS)


def clear_state(session_id):
    if session_id:
        cache.delete(_cache_key(session_id))


def ensure_session(session_id=None, user=None):
    if session_id:
        existing = load_state(session_id)
        if existing:
            return session_id, existing
    new_session_id = session_id or str(uuid.uuid4())
    state = _default_state(user=user)
    save_state(new_session_id, state)
    return new_session_id, state


def has_active_booking_session(session_id):
    state = load_state(session_id)
    return bool(state and state.get("started") and not state.get("completed"))


def is_booking_intent(message):
    text = (message or "").lower()
    phrases = [
        "book appointment",
        "book an appointment",
        "schedule appointment",
        "schedule me appointment",
        "doctor appointment",
        "consultation booking",
    ]
    return any(p in text for p in phrases)


def _normalize_whitespace(text):
    return re.sub(r"\s+", " ", (text or "").strip())


def _parse_age(raw):
    text = _normalize_whitespace(raw)
    if not text:
        return None, "Age is required."
    m = re.search(r"\b(\d{1,3})\b", text)
    if not m:
        return None, "Please enter age as a number."
    age = int(m.group(1))
    if age <= 0 or age > 120:
        return None, "Please enter a valid age between 1 and 120."
    return str(age), None


def _parse_gender(raw):
    text = _normalize_whitespace(raw).lower()
    if text in GENDER_VALUES:
        return GENDER_VALUES[text], None
    for key, value in GENDER_VALUES.items():
        if re.search(rf"\b{re.escape(key)}\b", text):
            return value, None
    return None, "Please enter gender as Male, Female, or Other."


def _parse_contact(raw):
    text = _normalize_whitespace(raw)
    digits = re.sub(r"\D", "", text)
    if len(digits) < 10 or len(digits) > 15:
        return None, "Please enter a valid contact number (10-15 digits)."
    return digits, None


def _parse_date(raw):
    text = _normalize_whitespace(raw)
    formats = ("%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y", "%d %b %Y", "%d %B %Y")
    parsed = None
    for fmt in formats:
        try:
            parsed = datetime.strptime(text, fmt).date()
            break
        except ValueError:
            continue
    if not parsed:
        return None, "Please enter a valid date (example: 2026-02-25)."
    if parsed < timezone.localdate():
        return None, "Preferred date cannot be in the past."
    return parsed.isoformat(), None


def _parse_time(raw):
    text = _normalize_whitespace(raw)
    formats = ("%H:%M", "%I:%M %p", "%I %p", "%I%p")
    parsed = None
    normalized = text.upper().replace(".", "")
    for fmt in formats:
        try:
            parsed = datetime.strptime(normalized, fmt).time()
            break
        except ValueError:
            continue
    if not parsed:
        return None, "Please enter a valid time (example: 10:30 AM)."
    return parsed.strftime("%H:%M"), None


def _parse_visit_type(raw):
    text = _normalize_whitespace(raw).lower()
    for key, value in VISIT_TYPE_VALUES.items():
        if key in text:
            return value, None
    return None, "Please specify visit type as First-time or Follow-up."


def _parse_name(raw):
    text = _normalize_whitespace(raw)
    if not text:
        return None, "Full name is required."
    text = re.sub(r"^(my name is|name is|i am|i'm)\s+", "", text, flags=re.I).strip()
    if len(text.split()) < 2:
        return None, "Please enter full name (first and last name)."
    if len(text) > 120:
        return None, "Full name is too long."
    return text, None


def _parse_location(raw):
    text = _normalize_whitespace(raw)
    text = re.sub(r"^(city|location)\s*[:\-]?\s*", "", text, flags=re.I).strip()
    if len(text) < 2:
        return None, "Please enter a valid city or location."
    return text, None


def _parse_symptoms(raw):
    text = _normalize_whitespace(raw)
    text = re.sub(r"^(symptoms?|reason|reason for visit)\s*[:\-]?\s*", "", text, flags=re.I).strip()
    if len(text) < 3:
        return None, "Please describe the symptoms or reason for visit."
    return text, None


def _parse_field(field_name, raw):
    parsers = {
        "name": _parse_name,
        "age": _parse_age,
        "gender": _parse_gender,
        "contactNumber": _parse_contact,
        "symptoms": _parse_symptoms,
        "preferredDate": _parse_date,
        "preferredTime": _parse_time,
        "location": _parse_location,
        "visitType": _parse_visit_type,
    }
    return parsers[field_name](raw)


def _extract_explicit_values(message):
    text = _normalize_whitespace(message)
    lower = text.lower()
    extracted = {}

    # Name
    name_match = re.search(r"\b(?:my name is|name is)\s+([a-z][a-z\s.'-]{2,})$", text, re.I)
    if name_match:
        parsed, err = _parse_name(name_match.group(1))
        if not err:
            extracted["name"] = parsed

    # Age
    age_match = re.search(r"\bage\s*(?:is|:)?\s*(\d{1,3})\b", lower)
    if age_match:
        parsed, err = _parse_age(age_match.group(1))
        if not err:
            extracted["age"] = parsed

    # Gender
    gender_match = re.search(r"\bgender\s*(?:is|:)?\s*(male|female|other|m|f)\b", lower)
    if gender_match:
        parsed, err = _parse_gender(gender_match.group(1))
        if not err:
            extracted["gender"] = parsed

    # Contact
    contact_match = re.search(r"\b(?:phone|contact|mobile|number)\s*(?:is|:)?\s*([+\d][\d\s\-()]{8,})", text, re.I)
    if contact_match:
        parsed, err = _parse_contact(contact_match.group(1))
        if not err:
            extracted["contactNumber"] = parsed

    # Date
    date_match = re.search(r"\b(?:date|preferred date)\s*(?:is|:)?\s*([0-9/\-]{6,10}|[0-9]{1,2}\s+[A-Za-z]{3,9}\s+[0-9]{4})", text, re.I)
    if date_match:
        parsed, err = _parse_date(date_match.group(1))
        if not err:
            extracted["preferredDate"] = parsed

    # Time
    time_match = re.search(r"\b(?:time|preferred time)\s*(?:is|:)?\s*([0-9]{1,2}(?::[0-9]{2})?\s*(?:am|pm)?)", text, re.I)
    if time_match:
        parsed, err = _parse_time(time_match.group(1))
        if not err:
            extracted["preferredTime"] = parsed

    # Visit type
    if "follow-up" in lower or "follow up" in lower:
        extracted["visitType"] = "Follow-up"
    elif "first-time" in lower or "first time" in lower:
        extracted["visitType"] = "First-time"

    # Location
    location_match = re.search(r"\b(?:city|location)\s*(?:is|:)?\s*([a-z][a-z\s.-]{1,})$", text, re.I)
    if location_match:
        parsed, err = _parse_location(location_match.group(1))
        if not err:
            extracted["location"] = parsed

    # Symptoms / reason
    symptom_match = re.search(r"\b(?:symptoms?|reason(?: for visit)?)\s*(?:is|:)?\s*(.+)$", text, re.I)
    if symptom_match:
        parsed, err = _parse_symptoms(symptom_match.group(1))
        if not err:
            extracted["symptoms"] = parsed

    return extracted


def _detect_emergency(text):
    lower = (text or "").lower()
    return any(keyword in lower for keyword in EMERGENCY_KEYWORDS)


def classify_specialization(symptoms_text):
    text = (symptoms_text or "").lower()
    for specialization, keywords in SPECIALIZATION_RULES:
        if any(keyword in text for keyword in keywords):
            return specialization
    return "General Physician"


def get_missing_fields(data):
    missing = []
    for field in FIELD_ORDER:
        value = data.get(field)
        if value in (None, ""):
            missing.append(field)
    return missing


def _field_label(field_name):
    labels = {
        "name": "Full Name",
        "age": "Age",
        "gender": "Gender",
        "contactNumber": "Contact Number",
        "symptoms": "Symptoms / Reason for visit",
        "doctorSpecialization": "Doctor Specialization",
        "preferredDate": "Preferred Date",
        "preferredTime": "Preferred Time",
        "location": "City / Location",
        "visitType": "Type of Visit",
        "emergency": "Emergency",
    }
    return labels.get(field_name, field_name)


def format_booking_json(data):
    def _s(key):
        value = data.get(key, "")
        return "" if value is None else str(value)

    ordered = {
        "name": _s("name"),
        "age": _s("age"),
        "gender": _s("gender"),
        "contactNumber": _s("contactNumber"),
        "symptoms": _s("symptoms"),
        "doctorSpecialization": _s("doctorSpecialization"),
        "preferredDate": _s("preferredDate"),
        "preferredTime": _s("preferredTime"),
        "location": _s("location"),
        "visitType": _s("visitType"),
        "emergency": bool(data.get("emergency", False)),
    }
    return ordered


def process_booking_turn(message, session_id=None, user=None):
    message = _normalize_whitespace(message)
    session_id, state = ensure_session(session_id=session_id, user=user)
    data = state["data"]

    if not message:
        missing = get_missing_fields(data)
        next_field = missing[0] if missing else None
        reply = "I can help book an appointment. " + (FIELD_PROMPTS[next_field] if next_field else "Please confirm if you want me to proceed.")
        save_state(session_id, state)
        return _build_response(session_id, state, reply)

    explicit_values = _extract_explicit_values(message)
    for key, value in explicit_values.items():
        data[key] = value

    missing_before_direct = get_missing_fields(data)
    current_target = missing_before_direct[0] if missing_before_direct else None

    # If user replied with a short direct answer, treat it as the next missing field.
    direct_assigned = False
    validation_error = None
    if current_target and current_target not in explicit_values:
        parsed_value, err = _parse_field(current_target, message)
        if err is None:
            data[current_target] = parsed_value
            direct_assigned = True
        else:
            # Only treat as validation error if the user likely answered the field rather than a fresh intent.
            likely_direct_answer = len(message.split()) <= 8 or current_target in {"age", "gender", "preferredDate", "preferredTime", "visitType"}
            if likely_direct_answer:
                validation_error = err

    if data.get("symptoms"):
        data["doctorSpecialization"] = classify_specialization(data["symptoms"])
        if _detect_emergency(data["symptoms"]):
            data["emergency"] = True
    elif _detect_emergency(message):
        data["emergency"] = True

    if validation_error and not explicit_values and not direct_assigned:
        reply = f"{validation_error} {FIELD_PROMPTS[current_target]}"
        if data.get("emergency") and not state.get("emergencyWarningShown"):
            state["emergencyWarningShown"] = True
            reply = (
                "If you have severe chest pain, breathing difficulty, or other emergency symptoms, "
                "please seek emergency care immediately or call local emergency services. "
            ) + reply
        save_state(session_id, state)
        return _build_response(session_id, state, reply)

    missing = get_missing_fields(data)

    if data.get("emergency") and not state.get("emergencyWarningShown"):
        state["emergencyWarningShown"] = True
        emergency_msg = (
            "Your symptoms may need urgent attention. Please seek emergency care immediately or call local emergency services if symptoms are severe."
        )
        if missing:
            emergency_msg += " If you still want me to help schedule, " + FIELD_PROMPTS[missing[0]].lower()
        save_state(session_id, state)
        return _build_response(session_id, state, emergency_msg, status="emergency")

    if missing:
        reply = FIELD_PROMPTS[missing[0]]
        if not explicit_values and not direct_assigned and is_booking_intent(message):
            reply = "I can help with that. " + reply
        save_state(session_id, state)
        return _build_response(session_id, state, reply)

    state["completed"] = True
    save_state(session_id, state)
    return _build_response(
        session_id,
        state,
        "Thank you. I have collected all required details.",
        status="ready",
        include_booking_json=True,
    )


def _build_response(session_id, state, reply, status="collecting", include_booking_json=False):
    booking_json = format_booking_json(state["data"])
    missing = get_missing_fields(state["data"])
    payload = {
        "sessionId": session_id,
        "status": status,
        "reply": reply,
        "missingFields": missing,
        "collectedFields": [f for f in FIELD_ORDER if booking_json.get(f)],
        "emergency": bool(booking_json["emergency"]),
    }
    if include_booking_json:
        payload["bookingData"] = booking_json
    return payload

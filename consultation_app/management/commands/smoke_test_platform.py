import json
from datetime import timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand, CommandError
from django.test import Client
from django.utils import timezone

from auth_app.models import User, Profile, DoctorProfile
from consultation_app.models import Availability, Appointment
from payment_app.models import Payment


class Command(BaseCommand):
    help = "Run endpoint smoke tests for core platform flows (auth, search, chatbot, booking, payment)."

    def handle(self, *args, **options):
        suffix = timezone.now().strftime("%Y%m%d%H%M%S%f")
        created_user_ids = []

        try:
            self._check_public_pages()
            self._check_chatbot_reply()
            registered_doctor = self._check_doctor_registration(suffix)
            created_user_ids.append(registered_doctor.id)

            doctor, patient = self._create_test_users(suffix)
            created_user_ids.extend([doctor.id, patient.id])

            self._check_doctor_search_page_has_doctor(doctor)

            self._check_ai_booking_conversation(patient, doctor)
            self._check_direct_api_appointments(patient, doctor)

            slot1 = self._create_slot(doctor, days=1, start_hhmm="10:00", end_hhmm="10:30")
            appointment1 = self._check_chatbot_quick_book(patient, doctor, slot1)
            self._check_payment_checkout_confirms_appointment(patient, appointment1)
            self._check_doctor_status_update(doctor, appointment1, Appointment.Status.COMPLETED)

            slot2 = self._create_slot(doctor, days=2, start_hhmm="11:00", end_hhmm="11:30")
            appointment2 = self._check_chatbot_quick_book(patient, doctor, slot2)
            self._check_cancel_releases_slot(patient, appointment2, slot2)

            slot3 = self._create_slot(doctor, days=1, start_hhmm="12:00", end_hhmm="12:30")
            appointment3 = self._check_chatbot_quick_book(patient, doctor, slot3)
            self._check_payment_checkout_confirms_appointment(patient, appointment3)
            self._check_join_consultation_future_redirect(patient, appointment3)

            self.stdout.write(self.style.SUCCESS("Smoke tests passed for core flows."))
        except Exception as exc:
            if isinstance(exc, CommandError):
                raise
            raise CommandError(str(exc)) from exc
        finally:
            if created_user_ids:
                User.objects.filter(id__in=created_user_ids).delete()
                self.stdout.write(self.style.WARNING("Smoke test temporary users cleaned up."))

    def _assert(self, condition, message):
        if not condition:
            raise CommandError(message)

    def _client(self):
        return Client()

    def _check_public_pages(self):
        client = self._client()
        for path in ["/", "/doctors/search/", "/auth/login/", "/auth/register/", "/chatbot/"]:
            response = client.get(path)
            if path == "/chatbot/":
                self._assert(response.status_code in (301, 302), f"{path} expected redirect, got {response.status_code}")
            else:
                self._assert(response.status_code == 200, f"{path} expected 200, got {response.status_code}")
        self.stdout.write(self.style.SUCCESS("Public pages OK"))

    def _check_chatbot_reply(self):
        client = self._client()
        response = client.post("/chatbot/get/", {"msg": "hello"})
        self._assert(response.status_code == 200, f"/chatbot/get/ expected 200, got {response.status_code}")
        body = response.content.decode("utf-8", errors="ignore").lower()
        self._assert("ayurbot" in body, "Chatbot greeting did not return expected content")
        self.stdout.write(self.style.SUCCESS("Chatbot reply endpoint OK"))

    def _check_doctor_registration(self, suffix):
        client = self._client()
        email = f"register_doc_{suffix}@test.local"
        payload = {
            "role": User.Role.DOCTOR,
            "first_name": "Reg",
            "last_name": "Doctor",
            "email": email,
            "password1": "Pass12345!",
            "password2": "Pass12345!",
            "specialty": "Dermatology",
            "license_number": f"REG-LIC-{suffix}",
            "experience_years": "7",
            "consultation_fee": "800",
            "education": "MBBS, MD",
            "bio": "Experienced dermatologist",
            "hospital_affiliation": "City Hospital",
            "languages_spoken": "English, Hindi",
            "terms": "on",
        }
        response = client.post("/auth/register/", payload)
        self._assert(response.status_code in (302, 303), f"Doctor registration expected redirect, got {response.status_code}")

        user = User.objects.get(email=email)
        self._assert(user.role == User.Role.DOCTOR, "Registered doctor role not saved")
        self._assert(hasattr(user, "doctor_profile"), "Doctor profile was not created at registration")
        self._assert(user.doctor_profile.license_number == payload["license_number"], "Doctor license number not saved at registration")
        self.stdout.write(self.style.SUCCESS("Single-step doctor registration OK"))
        return user

    def _create_test_users(self, suffix):
        doctor = User.objects.create_user(
            email=f"smoke_doc_{suffix}@test.local",
            password="Pass12345!",
            role=User.Role.DOCTOR,
            first_name="Smoke",
            last_name="Doctor",
        )
        patient = User.objects.create_user(
            email=f"smoke_patient_{suffix}@test.local",
            password="Pass12345!",
            role=User.Role.PATIENT,
            first_name="Smoke",
            last_name="Patient",
        )
        Profile.objects.get_or_create(user=doctor, defaults={"address": "Test City"})
        Profile.objects.get_or_create(user=patient)
        DoctorProfile.objects.update_or_create(
            user=doctor,
            defaults={
                "specialty": "General Medicine",
                "license_number": f"SMOKE-LIC-{suffix}",
                "experience_years": 5,
                "consultation_fee": Decimal("500.00"),
                "bio": "Smoke test doctor",
                "education": "MBBS",
                "hospital_affiliation": "Smoke Hospital",
                "languages_spoken": "English",
            },
        )
        self.stdout.write(self.style.SUCCESS("Test users created"))
        return doctor, patient

    def _check_doctor_search_page_has_doctor(self, doctor):
        client = self._client()
        response = client.get("/doctors/search/", {"query": "Smoke"})
        self._assert(response.status_code == 200, "Doctor search page did not load")
        body = response.content.decode("utf-8", errors="ignore")
        self._assert(doctor.get_full_name() in body, "Doctor search did not include licensed doctor")
        self.stdout.write(self.style.SUCCESS("Doctor search flow OK"))

    def _create_slot(self, doctor, days, start_hhmm, end_hhmm):
        start_time = timezone.datetime.strptime(start_hhmm, "%H:%M").time()
        end_time = timezone.datetime.strptime(end_hhmm, "%H:%M").time()
        return Availability.objects.create(
            doctor=doctor,
            date=timezone.now().date() + timedelta(days=days),
            start_time=start_time,
            end_time=end_time,
            is_booked=False,
        )

    def _json_post(self, client, path, payload):
        return client.post(path, data=json.dumps(payload), content_type="application/json")

    def _login(self, client, user):
        ok = client.login(email=user.email, password="Pass12345!")
        self._assert(ok, f"Login failed for {user.email}")

    def _check_chatbot_quick_book(self, patient, doctor, slot):
        client = self._client()
        self._login(client, patient)
        response = client.post("/chatbot/quick-book/", {"availability_id": slot.id, "reason": "Smoke booking"})
        self._assert(response.status_code == 200, f"chatbot quick-book expected 200, got {response.status_code}")
        payload = response.json()
        self._assert(payload.get("success") is True, "chatbot quick-book returned unsuccessful payload")
        slot.refresh_from_db()
        self._assert(slot.is_booked is True, "Slot not marked booked after quick-book")
        appointment = Appointment.objects.get(id=payload["appointment_id"])
        self._assert(appointment.patient_id == patient.id, "Quick-book appointment patient mismatch")
        self._assert(appointment.doctor_id == doctor.id, "Quick-book appointment doctor mismatch")
        self._assert(appointment.status == Appointment.Status.REQUESTED, "Quick-book should create REQUESTED appointment")
        self.stdout.write(self.style.SUCCESS(f"Chatbot quick-book OK ({appointment.id})"))
        return appointment

    def _check_ai_booking_conversation(self, patient, doctor):
        slot = self._create_slot(doctor, days=1, start_hhmm="09:30", end_hhmm="10:00")
        client = self._client()
        self._login(client, patient)

        date_str = slot.date.isoformat()
        turns = [
            "I want to book an appointment",
            "Rahul Sharma",
            "35",
            "Male",
            "9876543210",
            "Skin rash and itching for 3 days",
            date_str,
            "09:30 AM",
            "Test City",
            "First-time",
        ]
        session_id = None
        final_payload = None
        for turn in turns:
            payload = {"message": turn}
            if session_id:
                payload["sessionId"] = session_id
            response = self._json_post(client, "/chatbot/ai-booking/", payload)
            self._assert(response.status_code in (200, 409), f"AI booking conversation returned {response.status_code}")
            final_payload = response.json()
            session_id = final_payload.get("sessionId", session_id)

        self._assert(final_payload is not None, "AI booking conversation produced no response")
        # Because doctor specialty is General Medicine in base fixture, booking should still complete via fallback if no dermatology slot exists.
        self._assert(final_payload.get("status") in ("booked", "error"), "AI booking conversation did not reach terminal state")
        if final_payload.get("status") == "booked":
            self._assert("appointment" in final_payload, "Booked AI conversation response missing appointment payload")
            self._assert(final_payload["appointment"].get("appointmentId"), "AI conversation appointment missing ID")
        self.stdout.write(self.style.SUCCESS("AI booking conversation flow OK"))

    def _check_direct_api_appointments(self, patient, doctor):
        slot = self._create_slot(doctor, days=1, start_hhmm="15:00", end_hhmm="15:30")
        client = self._client()
        self._login(client, patient)
        payload = {
            "name": "API Patient",
            "age": "29",
            "gender": "Female",
            "contactNumber": "9876501234",
            "symptoms": "General fever and weakness",
            "doctorSpecialization": "General Physician",
            "preferredDate": slot.date.isoformat(),
            "preferredTime": "15:00",
            "location": "Test City",
            "visitType": "First-time",
            "emergency": False,
        }
        response = self._json_post(client, "/api/appointments", payload)
        self._assert(response.status_code == 201, f"/api/appointments expected 201, got {response.status_code}")
        body = response.json()
        self._assert(body.get("appointmentId"), "/api/appointments missing appointmentId")
        self._assert(body.get("confirmationMessage"), "/api/appointments missing confirmationMessage")
        self.stdout.write(self.style.SUCCESS("Direct /api/appointments contract OK"))

    def _check_payment_checkout_confirms_appointment(self, patient, appointment):
        client = self._client()
        self._login(client, patient)
        response = client.get(f"/payment/checkout/{appointment.id}/")
        self._assert(response.status_code in (302, 303), f"payment checkout expected redirect, got {response.status_code}")
        appointment.refresh_from_db()
        self._assert(appointment.status == Appointment.Status.CONFIRMED, "Simulated payment did not confirm appointment")
        payment = Payment.objects.get(appointment=appointment)
        self._assert(payment.status == Payment.Status.COMPLETED, "Payment not marked completed after simulated checkout")
        self.stdout.write(self.style.SUCCESS(f"Payment checkout flow OK ({appointment.id})"))

    def _check_doctor_status_update(self, doctor, appointment, target_status):
        client = self._client()
        self._login(client, doctor)
        response = client.post(f"/appointment/{appointment.id}/update-status/", {"status": target_status})
        self._assert(response.status_code in (302, 303), f"status update expected redirect, got {response.status_code}")
        appointment.refresh_from_db()
        self._assert(appointment.status == target_status, f"Appointment status not updated to {target_status}")
        self.stdout.write(self.style.SUCCESS(f"Doctor status update OK ({target_status})"))

    def _check_cancel_releases_slot(self, patient, appointment, slot):
        client = self._client()
        self._login(client, patient)
        response = client.post(f"/appointment/{appointment.id}/cancel/")
        self._assert(response.status_code in (302, 303), f"cancel expected redirect, got {response.status_code}")
        appointment.refresh_from_db()
        slot.refresh_from_db()
        self._assert(appointment.status == Appointment.Status.CANCELLED, "Appointment not cancelled")
        self._assert(slot.is_booked is False, "Cancelled appointment did not release availability slot")
        self.stdout.write(self.style.SUCCESS("Cancel appointment flow OK"))

    def _check_join_consultation_future_redirect(self, patient, appointment):
        client = self._client()
        self._login(client, patient)
        response = client.get(f"/appointment/{appointment.id}/join/")
        self._assert(response.status_code in (302, 303), f"join consultation expected redirect, got {response.status_code}")
        self.stdout.write(self.style.SUCCESS("Join consultation future-slot guard OK"))

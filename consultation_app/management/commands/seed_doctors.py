import random
from datetime import date, time, timedelta
from django.core.management.base import BaseCommand
from auth_app.models import User, DoctorProfile, Profile
from consultation_app.models import Availability


DOCTORS = [
    {
        "first_name": "Rajesh", "last_name": "Mehta",
        "specialty": "Cardiologist",
        "experience": 18, "fee": 1200,
        "education": "MBBS, MD (Cardiology) – AIIMS Delhi",
        "hospital": "Apollo Heart Centre, Greams Road, Chennai, Tamil Nadu – 600006 India",
        "languages": "English, Hindi, Tamil",
        "bio": "Professional Summary\nDr. Rajesh Mehta is a senior interventional cardiologist with over 18 years of experience in diagnosing and treating complex cardiovascular conditions. He has performed 5,000+ angioplasties and is a pioneer in minimally invasive cardiac procedures in South India.",
    },
    {
        "first_name": "Priya", "last_name": "Sharma",
        "specialty": "Dermatologist",
        "experience": 12, "fee": 800,
        "education": "MBBS, MD (Dermatology) – KEM Hospital, Mumbai",
        "hospital": "SkinCare Clinic, Bandra West, Mumbai, Maharashtra – 400050 India",
        "languages": "English, Hindi, Marathi",
        "bio": "Professional Summary\nDr. Priya Sharma is a board-certified dermatologist specializing in acne management, pigmentation disorders, and cosmetic dermatology. She has published 25+ research papers and is known for her holistic approach combining modern dermatology with Ayurvedic skincare principles.",
    },
    {
        "first_name": "Arjun", "last_name": "Reddy",
        "specialty": "Orthopedic Surgeon",
        "experience": 15, "fee": 1500,
        "education": "MBBS, MS (Ortho) – Osmania Medical College, Hyderabad",
        "hospital": "CARE Hospitals, Banjara Hills, Hyderabad, Telangana – 500034 India",
        "languages": "English, Hindi, Telugu",
        "bio": "Professional Summary\nDr. Arjun Reddy is a leading orthopedic surgeon specializing in joint replacement surgery and sports medicine. He has successfully performed over 3,000 knee and hip replacement surgeries using robotic-assisted techniques.",
    },
    {
        "first_name": "Sneha", "last_name": "Iyer",
        "specialty": "Pediatrician",
        "experience": 10, "fee": 700,
        "education": "MBBS, DCH, MD (Pediatrics) – CMC Vellore",
        "hospital": "Rainbow Children's Hospital, Koramangala, Bengaluru, Karnataka – 560034 India",
        "languages": "English, Hindi, Kannada, Tamil",
        "bio": "Professional Summary\nDr. Sneha Iyer is a compassionate pediatrician with a decade of experience in neonatal care and childhood developmental disorders. She runs a popular parenting blog and conducts free vaccination drives in underserved communities.",
    },
    {
        "first_name": "Vikram", "last_name": "Singh",
        "specialty": "Neurologist",
        "experience": 20, "fee": 1800,
        "education": "MBBS, DM (Neurology) – PGIMER Chandigarh",
        "hospital": "Fortis Memorial Research Institute, Sector 44, Gurugram, Haryana – 122002 India",
        "languages": "English, Hindi, Punjabi",
        "bio": "Professional Summary\nDr. Vikram Singh is a renowned neurologist with two decades of expertise in stroke management, epilepsy, and neurodegenerative diseases. He leads the Stroke Unit at Fortis and has trained over 100 neurology residents.",
    },
    {
        "first_name": "Kavitha", "last_name": "Nair",
        "specialty": "Gynecologist",
        "experience": 14, "fee": 1000,
        "education": "MBBS, MS (OBG), DNB – Amrita Institute, Kochi",
        "hospital": "Aster Medcity, Cheranalloor, Kochi, Kerala – 682027 India",
        "languages": "English, Hindi, Malayalam",
        "bio": "Professional Summary\nDr. Kavitha Nair is an experienced obstetrician and gynecologist specializing in high-risk pregnancies and laparoscopic gynecological surgeries. She is a strong advocate for women's reproductive health awareness in rural Kerala.",
    },
    {
        "first_name": "Aditya", "last_name": "Joshi",
        "specialty": "Ophthalmologist",
        "experience": 11, "fee": 900,
        "education": "MBBS, MS (Ophthalmology) – BJ Medical College, Pune",
        "hospital": "Sankara Eye Hospital, Sadashiv Peth, Pune, Maharashtra – 411030 India",
        "languages": "English, Hindi, Marathi",
        "bio": "Professional Summary\nDr. Aditya Joshi is a skilled ophthalmologist specializing in LASIK surgery, cataract removal, and retinal disorders. He has restored vision to over 10,000 patients and actively participates in remote eye-care camps across Maharashtra.",
    },
    {
        "first_name": "Meera", "last_name": "Patel",
        "specialty": "Endocrinologist",
        "experience": 9, "fee": 1100,
        "education": "MBBS, MD (Medicine), DM (Endocrinology) – SMS Medical College, Jaipur",
        "hospital": "Sterling Hospital, Drive-In Road, Ahmedabad, Gujarat – 380054 India",
        "languages": "English, Hindi, Gujarati",
        "bio": "Professional Summary\nDr. Meera Patel is a dynamic endocrinologist focused on diabetes management, thyroid disorders, and PCOS treatment. She runs a comprehensive Diabetes Reversal Program that has helped 2,000+ patients reduce their A1C levels without surgery.",
    },
    {
        "first_name": "Saurabh", "last_name": "Khanna",
        "specialty": "Psychiatrist",
        "experience": 13, "fee": 1300,
        "education": "MBBS, MD (Psychiatry) – NIMHANS, Bengaluru",
        "hospital": "Manipal Hospital, Old Airport Road, Bengaluru, Karnataka – 560017 India",
        "languages": "English, Hindi, Kannada",
        "bio": "Professional Summary\nDr. Saurabh Khanna is a leading psychiatrist specializing in anxiety disorders, depression, and de-addiction therapy. He integrates cognitive behavioral therapy with mindfulness-based treatments and has counseled over 8,000 patients.",
    },
    {
        "first_name": "Divya", "last_name": "Rao",
        "specialty": "Pulmonologist",
        "experience": 8, "fee": 950,
        "education": "MBBS, MD (Pulmonary Medicine) – Kasturba Medical College, Manipal",
        "hospital": "Yashoda Hospitals, Somajiguda, Hyderabad, Telangana – 500082 India",
        "languages": "English, Hindi, Telugu, Kannada",
        "bio": "Professional Summary\nDr. Divya Rao is a pulmonologist with deep expertise in asthma management, COPD, and post-COVID respiratory rehabilitation. She set up Yashoda's dedicated Long-COVID clinic that has treated 1,500+ patients.",
    },
    {
        "first_name": "Manish", "last_name": "Gupta",
        "specialty": "Gastroenterologist",
        "experience": 16, "fee": 1400,
        "education": "MBBS, MD (Medicine), DM (Gastro) – GB Pant Hospital, Delhi",
        "hospital": "Max Super Speciality Hospital, Saket, New Delhi – 110017 India",
        "languages": "English, Hindi",
        "bio": "Professional Summary\nDr. Manish Gupta is a senior gastroenterologist and hepatologist with 16 years of experience in advanced endoscopic procedures, liver disease management, and IBD treatment. He has performed 12,000+ endoscopies.",
    },
    {
        "first_name": "Ananya", "last_name": "Das",
        "specialty": "Oncologist",
        "experience": 17, "fee": 2000,
        "education": "MBBS, MD (Radiation Oncology) – Tata Memorial Hospital, Mumbai",
        "hospital": "HCG Cancer Centre, Park Street, Kolkata, West Bengal – 700016 India",
        "languages": "English, Hindi, Bengali",
        "bio": "Professional Summary\nDr. Ananya Das is an award-winning oncologist specializing in breast cancer, head-and-neck cancers, and precision radiation therapy. She has treated 4,000+ cancer patients and published extensively on targeted therapy outcomes in Indian populations.",
    },
    {
        "first_name": "Rohan", "last_name": "Verma",
        "specialty": "ENT Specialist",
        "experience": 7, "fee": 750,
        "education": "MBBS, MS (ENT) – Maulana Azad Medical College, Delhi",
        "hospital": "Sir Ganga Ram Hospital, Rajinder Nagar, New Delhi – 110060 India",
        "languages": "English, Hindi",
        "bio": "Professional Summary\nDr. Rohan Verma is an ENT specialist with expertise in sinus surgery, cochlear implants, and pediatric ENT disorders. He has performed over 2,000 functional endoscopic sinus surgeries with a 98% success rate.",
    },
    {
        "first_name": "Lakshmi", "last_name": "Subramaniam",
        "specialty": "Rheumatologist",
        "experience": 12, "fee": 1100,
        "education": "MBBS, MD (Medicine), DM (Rheumatology) – CMC Vellore",
        "hospital": "MIOT International, Manapakkam, Chennai, Tamil Nadu – 600089 India",
        "languages": "English, Hindi, Tamil",
        "bio": "Professional Summary\nDr. Lakshmi Subramaniam is a rheumatologist specializing in rheumatoid arthritis, lupus, and autoimmune disorders. She runs an internationally recognized Biologics Centre and has helped 3,500+ patients achieve disease remission.",
    },
    {
        "first_name": "Nikhil", "last_name": "Deshmukh",
        "specialty": "Urologist",
        "experience": 14, "fee": 1300,
        "education": "MBBS, MS (Surgery), MCh (Urology) – Seth GS Medical College, Mumbai",
        "hospital": "Kokilaben Dhirubhai Ambani Hospital, Andheri West, Mumbai, Maharashtra – 400053 India",
        "languages": "English, Hindi, Marathi",
        "bio": "Professional Summary\nDr. Nikhil Deshmukh is a senior urologist specializing in robotic prostatectomy, kidney stone management, and male infertility. He is one of the few surgeons in India certified in da Vinci robotic surgery.",
    },
    {
        "first_name": "Sunita", "last_name": "Agarwal",
        "specialty": "General Physician",
        "experience": 22, "fee": 600,
        "education": "MBBS, MD (General Medicine) – King George's Medical University, Lucknow",
        "hospital": "Medanta – The Medicity, Sector 38, Gurugram, Haryana – 122001 India",
        "languages": "English, Hindi, Urdu",
        "bio": "Professional Summary\nDr. Sunita Agarwal is a highly experienced general physician with 22 years of practice in internal medicine, preventive healthcare, and lifestyle disease management. She is Medanta's faculty lead for the Annual Preventive Health Checkup Program.",
    },
    {
        "first_name": "Karthik", "last_name": "Menon",
        "specialty": "Nephrologist",
        "experience": 10, "fee": 1200,
        "education": "MBBS, MD (Medicine), DM (Nephrology) – JIPMER, Puducherry",
        "hospital": "Amrita Hospital, Faridabad, Haryana – 121002 India",
        "languages": "English, Hindi, Malayalam, Tamil",
        "bio": "Professional Summary\nDr. Karthik Menon is a nephrologist specializing in chronic kidney disease, dialysis management, and kidney transplant evaluation. He has managed 1,800+ dialysis patients and facilitated 200+ successful transplants.",
    },
    {
        "first_name": "Pooja", "last_name": "Banerjee",
        "specialty": "Dentist",
        "experience": 6, "fee": 500,
        "education": "BDS, MDS (Orthodontics) – Manipal College of Dental Sciences",
        "hospital": "Clove Dental, Salt Lake City, Kolkata, West Bengal – 700091 India",
        "languages": "English, Hindi, Bengali",
        "bio": "Professional Summary\nDr. Pooja Banerjee is a skilled orthodontist and cosmetic dentist specializing in Invisalign aligners, dental implants, and smile makeovers. She has transformed 5,000+ smiles and is a certified Invisalign Platinum Provider.",
    },
    {
        "first_name": "Harsh", "last_name": "Trivedi",
        "specialty": "Ayurveda Specialist",
        "experience": 19, "fee": 650,
        "education": "BAMS, MD (Ayurveda Kayachikitsa) – Gujarat Ayurved University, Jamnagar",
        "hospital": "Jiva Ayurveda Clinic, Sector 63, Noida, Uttar Pradesh – 201301 India",
        "languages": "English, Hindi, Gujarati, Sanskrit",
        "bio": "Professional Summary\nDr. Harsh Trivedi is a renowned Ayurveda specialist with 19 years of clinical practice in Panchakarma therapy, chronic disease management through Ayurveda, and herbal pharmacology. He has treated 15,000+ patients and authored two books on Ayurvedic lifestyle medicine.",
    },
    {
        "first_name": "Ishita", "last_name": "Chatterjee",
        "specialty": "Physiotherapist",
        "experience": 8, "fee": 550,
        "education": "BPT, MPT (Sports Physiotherapy) – MAMC, Delhi",
        "hospital": "PhysioActive Rehab Centre, Park Circus, Kolkata, West Bengal – 700017 India",
        "languages": "English, Hindi, Bengali",
        "bio": "Professional Summary\nDr. Ishita Chatterjee is a sports physiotherapist specializing in post-surgical rehabilitation, spinal cord injury recovery, and athletic performance optimization. She has worked with IPL cricket teams and rehabilitated 3,000+ patients back to full mobility.",
    },
]


class Command(BaseCommand):
    help = "Seed the database with 20 realistic doctor profiles and availability slots"

    def handle(self, *args, **options):
        created_count = 0
        today = date.today()

        for doc in DOCTORS:
            email = f"dr.{doc['first_name'].lower()}.{doc['last_name'].lower()}@chikitsa360.com"

            if User.objects.filter(email=email).exists():
                self.stdout.write(self.style.WARNING(f"  Skipped (exists): {email}"))
                continue

            # 1. Create User
            user = User.objects.create_user(
                email=email,
                password="Doctor@123",
                first_name=doc["first_name"],
                last_name=doc["last_name"],
                role=User.Role.DOCTOR,
                is_verified=True,
            )

            # 2. Create DoctorProfile
            DoctorProfile.objects.create(
                user=user,
                specialty=doc["specialty"],
                license_number=f"MCI-{random.randint(100000, 999999)}",
                experience_years=doc["experience"],
                bio=doc["bio"],
                consultation_fee=doc["fee"],
                education=doc["education"],
                hospital_affiliation=doc["hospital"],
                languages_spoken=doc["languages"],
                is_available=True,
            )

            # 3. Create Profile (optional extras)
            Profile.objects.get_or_create(
                user=user,
                defaults={
                    "phone_number": f"+91 {random.randint(70000, 99999)} {random.randint(10000, 99999)}",
                    "address": doc["hospital"],
                },
            )

            # 4. Create Availability slots (next 7 days, 3 slots/day)
            slot_times = [
                (time(9, 0), time(9, 30)),
                (time(11, 0), time(11, 30)),
                (time(14, 0), time(14, 30)),
                (time(16, 0), time(16, 30)),
                (time(18, 0), time(18, 30)),
            ]
            for day_offset in range(1, 8):
                slot_date = today + timedelta(days=day_offset)
                chosen = random.sample(slot_times, k=3)
                for start, end in chosen:
                    Availability.objects.create(
                        doctor=user,
                        date=slot_date,
                        start_time=start,
                        end_time=end,
                    )

            created_count += 1
            self.stdout.write(self.style.SUCCESS(
                f"  Created: Dr. {doc['first_name']} {doc['last_name']} ({doc['specialty']})"
            ))

        self.stdout.write(self.style.SUCCESS(f"\nDone! {created_count} doctors seeded."))

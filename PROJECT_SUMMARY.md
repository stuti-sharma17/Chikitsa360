# Chikitsa360 - Comprehensive Project Summary

## Table of Contents
1. [Project Overview](#project-overview)
2. [Technology Stack](#technology-stack)
3. [Architecture & Design Patterns](#architecture--design-patterns)
4. [Database Schema & Models](#database-schema--models)
5. [Application Structure](#application-structure)
6. [Features & Implementations](#features--implementations)
7. [Security Implementation](#security-implementation)
8. [API Integrations](#api-integrations)
9. [Frontend Implementation](#frontend-implementation)
10. [Deployment Configuration](#deployment-configuration)
11. [UML Diagrams](#uml-diagrams)
12. [Workflows & User Journeys](#workflows--user-journeys)

---

## Project Overview

**Chikitsa360** is a comprehensive telemedicine platform built with Django that enables patients and healthcare providers to conduct secure video consultations. The platform facilitates appointment booking, real-time video consultations, automated transcription services, payment processing, and secure messaging between patients and doctors.

### Key Objectives
- Provide accessible healthcare through telemedicine
- Enable secure doctor-patient interactions
- Automate consultation documentation via transcription
- Streamline appointment management and payment processing
- Support real-time communication via WebSockets

---

## Technology Stack

### Backend Framework
- **Django 4.x**: Python web framework
- **Django Channels**: WebSocket support for real-time features
- **ASGI (Daphne)**: ASGI server for async support
- **PostgreSQL**: Primary database
- **psycopg2-binary**: PostgreSQL adapter

### Frontend Technologies
- **HTML5/CSS3**: Structure and styling
- **JavaScript (ES6+)**: Client-side interactivity
- **Tailwind CSS**: Utility-first CSS framework
- **WebRTC**: Real-time video communication
- **Daily.co SDK**: Video conferencing infrastructure

### Real-time Communication
- **Django Channels**: WebSocket framework
- **InMemoryChannelLayer**: Channel layer for WebSocket routing
- **WebSocket Protocol**: Real-time bidirectional communication

### Third-Party Integrations
- **Daily.co API**: Video conferencing platform
  - Room creation and management
  - Token-based authentication
  - WebRTC infrastructure
- **Deepgram API**: Speech-to-text transcription
  - Real-time audio processing
  - Multi-language support
- **Razorpay**: Payment gateway (currently in simulation mode)
  - Order creation
  - Payment verification
  - Receipt generation
- **SMTP (Gmail)**: Email notifications
  - Appointment confirmations
  - Transcription delivery
  - System notifications

### Development & Deployment Tools
- **python-dotenv**: Environment variable management
- **django-environ**: Environment configuration
- **django-cors-headers**: Cross-origin resource sharing
- **django-widget-tweaks**: Form widget customization
- **WhiteNoise**: Static file serving
- **django-csp**: Content Security Policy
- **Gunicorn**: WSGI HTTP server
- **dj-database-url**: Database URL parsing

### Additional Libraries
- **Pillow**: Image processing
- **requests**: HTTP library for API calls
- **openai**: (Configured but not actively used)

---

## Architecture & Design Patterns

### Architecture Pattern
**MVC (Model-View-Template)** - Django's implementation of MVC pattern:
- **Models**: Data layer (`models.py`)
- **Views**: Business logic layer (`views.py`)
- **Templates**: Presentation layer (`templates/`)

### Design Patterns Implemented

#### 1. **Repository Pattern**
- Models abstract database operations
- Custom managers for User model (`UserManager`)

#### 2. **Mixin Pattern**
- `LoginRequiredMixin`: Authentication checks
- `PatientRequiredMixin`: Patient role verification
- `DoctorRequiredMixin`: Doctor role verification
- `AdminRequiredMixin`: Admin role verification
- `RoleRequiredMixin`: Base role-based access control

#### 3. **Service Pattern**
- `TranscriptionService`: Handles transcription logic
- Separates business logic from views

#### 4. **Consumer Pattern (Channels)**
- `ChatConsumer`: WebSocket message handling
- Async/await pattern for real-time communication

#### 5. **Form Pattern**
- Django forms for data validation
- Custom forms with Tailwind CSS styling

### Application Structure
```
chikitsa360/
├── auth_app/          # Authentication & User Management
├── consultation_app/   # Appointments & Consultations
├── payment_app/        # Payment Processing
├── chat_app/           # Real-time Messaging
├── transcription_app/  # Audio Transcription
└── chikitsa360/        # Project Configuration
```

---

## Database Schema & Models

### Entity Relationship Overview

```
User (AbstractUser)
├── Profile (OneToOne)
├── DoctorProfile (OneToOne, conditional)
├── PatientAppointments (OneToMany)
├── DoctorAppointments (OneToMany)
├── Payments (OneToMany)
├── ChatMessages (OneToMany)
└── HealthTips (OneToMany, as author)

Availability
└── Appointment (OneToOne)

Appointment
├── Payment (OneToOne)
├── Transcription (OneToOne)
└── ChatMessages (OneToMany)

Service (Independent)
Testimonial (Independent)
HealthTip (Independent)
Receipt (OneToOne with Payment)
```

### Detailed Model Specifications

#### 1. **User Model** (`auth_app/models.py`)
**Inherits**: `AbstractUser`
**Primary Key**: Auto-incrementing ID
**Authentication**: Email-based (custom backend)

**Fields**:
- `email`: EmailField (unique, primary identifier)
- `username`: CharField (optional, nullable)
- `role`: CharField (choices: ADMIN, DOCTOR, PATIENT)
- `is_verified`: BooleanField
- Standard Django user fields (first_name, last_name, etc.)

**Methods**:
- `is_admin()`: Check if user is admin
- `is_doctor()`: Check if user is doctor
- `is_patient()`: Check if user is patient

**Relationships**:
- OneToOne → Profile
- OneToOne → DoctorProfile (if role is DOCTOR)
- OneToMany → Appointments (as patient or doctor)
- OneToMany → Payments
- OneToMany → ChatMessages

#### 2. **Profile Model** (`auth_app/models.py`)
**Relationship**: OneToOne with User

**Fields**:
- `profile_picture`: URLField
- `phone_number`: CharField
- `address`: TextField
- `date_of_birth`: DateField
- `created_at`: DateTimeField (auto)
- `updated_at`: DateTimeField (auto)

#### 3. **DoctorProfile Model** (`auth_app/models.py`)
**Relationship**: OneToOne with User (conditional)

**Fields**:
- `specialty`: CharField
- `license_number`: CharField
- `experience_years`: PositiveIntegerField
- `bio`: TextField
- `consultation_fee`: DecimalField
- `education`: TextField
- `hospital_affiliation`: CharField
- `languages_spoken`: CharField
- `is_available`: BooleanField

#### 4. **Availability Model** (`consultation_app/models.py`)
**Purpose**: Doctor's available time slots

**Fields**:
- `doctor`: ForeignKey → User
- `date`: DateField
- `start_time`: TimeField
- `end_time`: TimeField
- `is_booked`: BooleanField
- `created_at`: DateTimeField (auto)
- `updated_at`: DateTimeField (auto)

**Constraints**:
- Unique together: (doctor, date, start_time)
- Validation: start_time < end_time

**Properties**:
- `is_past`: Check if slot is in the past

#### 5. **Appointment Model** (`consultation_app/models.py`)
**Primary Key**: UUID (for security)

**Status Choices**:
- REQUESTED
- CONFIRMED
- COMPLETED
- CANCELLED
- NO_SHOW

**Fields**:
- `id`: UUIDField (primary key)
- `patient`: ForeignKey → User
- `doctor`: ForeignKey → User
- `availability`: OneToOneField → Availability
- `appointment_date`: DateField
- `appointment_time`: TimeField
- `status`: CharField (choices)
- `reason`: TextField
- `notes`: TextField
- `video_room_id`: CharField (Daily.co room identifier)
- `video_room_token`: TextField (Daily.co access token)
- `created_at`: DateTimeField (auto)
- `updated_at`: DateTimeField (auto)

**Properties**:
- `is_past`: Check if appointment is in the past
- `is_today`: Check if appointment is today
- `can_join`: Check if user can join (15 min before to 1 hour after)

#### 6. **Service Model** (`consultation_app/models.py`)
**Purpose**: Healthcare services offered

**Fields**:
- `name`: CharField
- `description`: TextField
- `icon_class`: CharField (FontAwesome classes)
- `display_order`: PositiveIntegerField
- `is_active`: BooleanField

#### 7. **Testimonial Model** (`consultation_app/models.py`)
**Fields**:
- `patient`: ForeignKey → User (nullable)
- `name`: CharField
- `image`: URLField
- `content`: TextField
- `rating`: PositiveSmallIntegerField (1-5)
- `is_featured`: BooleanField
- `is_approved`: BooleanField

#### 8. **HealthTip Model** (`consultation_app/models.py`)
**Fields**:
- `title`: CharField
- `content`: TextField
- `image_url`: URLField
- `author`: ForeignKey → User
- `is_featured`: BooleanField

#### 9. **Payment Model** (`payment_app/models.py`)
**Primary Key**: UUID

**Status Choices**:
- PENDING
- COMPLETED
- FAILED
- REFUNDED

**Fields**:
- `id`: UUIDField
- `appointment`: OneToOneField → Appointment
- `patient`: ForeignKey → User
- `amount`: DecimalField
- `currency`: CharField (default: INR)
- `razorpay_order_id`: CharField
- `razorpay_payment_id`: CharField
- `razorpay_signature`: CharField
- `status`: CharField (choices)
- `receipt_url`: CharField

#### 10. **Receipt Model** (`payment_app/models.py`)
**Relationship**: OneToOne with Payment

**Fields**:
- `id`: UUIDField
- `payment`: OneToOneField → Payment
- `receipt_number`: CharField
- `patient_name`: CharField
- `doctor_name`: CharField
- `appointment_date`: DateField
- `appointment_time`: TimeField
- `amount`: DecimalField
- `tax_amount`: DecimalField (18% GST)
- `total_amount`: DecimalField
- `payment_date`: DateTimeField

#### 11. **ChatMessage Model** (`chat_app/models.py`)
**Fields**:
- `appointment`: ForeignKey → Appointment
- `sender`: ForeignKey → User
- `message`: TextField
- `is_read`: BooleanField
- `created_at`: DateTimeField (auto)

#### 12. **Transcription Model** (`transcription_app/models.py`)
**Primary Key**: UUID

**Status Choices**:
- PENDING
- PROCESSING
- COMPLETED
- FAILED

**Fields**:
- `id`: UUIDField
- `appointment`: OneToOneField → Appointment
- `content`: TextField
- `status`: CharField (choices)
- `error_message`: TextField
- `audio_duration`: FloatField (seconds)
- `created_at`: DateTimeField (auto)
- `updated_at`: DateTimeField (auto)

---

## Application Structure

### 1. **auth_app** - Authentication & User Management

**Purpose**: User registration, authentication, profile management

**Files**:
- `models.py`: User, Profile, DoctorProfile models
- `views.py`: Authentication views, profile views, dashboard views
- `forms.py`: Registration, login, profile forms
- `urls.py`: URL routing
- `backends.py`: Custom email authentication backend
- `mixins.py`: Role-based access control mixins
- `admin.py`: Django admin configuration

**Key Views**:
- `CustomLoginView`: Email-based login
- `RegisterView`: User registration with role selection
- `ProfileUpdateView`: Update user profile
- `DoctorProfileUpdateView`: Update doctor-specific information
- `PatientDashboardView`: Patient dashboard
- `DoctorDashboardView`: Doctor dashboard
- `AdminDashboardView`: Admin dashboard with statistics

**URL Patterns**:
- `/auth/login/` - Login
- `/auth/logout/` - Logout
- `/auth/register/` - Registration
- `/auth/profile/` - View profile
- `/auth/profile/edit/` - Edit profile
- `/auth/profile/doctor/update/` - Update doctor profile
- `/auth/dashboard/patient/` - Patient dashboard
- `/auth/dashboard/doctor/` - Doctor dashboard
- `/auth/dashboard/admin/` - Admin dashboard

### 2. **consultation_app** - Appointments & Consultations

**Purpose**: Doctor search, appointment booking, video consultations

**Files**:
- `models.py`: Availability, Appointment, Service, Testimonial, HealthTip
- `views.py`: All consultation-related views
- `forms.py`: Availability, Appointment, DoctorSearch forms
- `urls.py`: URL routing
- `admin.py`: Admin configuration

**Key Views**:
- `HomeView`: Landing page with featured content
- `DoctorSearchView`: Search doctors by name, specialty, date
- `DoctorDetailView`: Doctor profile and available slots
- `DoctorAvailabilityView`: Manage availability slots
- `BookAppointmentView`: Book an appointment
- `AppointmentDetailView`: View appointment details
- `JoinConsultationView`: Join video consultation
- `PatientAppointmentsView`: Patient's appointment list
- `DoctorAppointmentsView`: Doctor's appointment list
- `UpdateAppointmentStatusView`: Update appointment status
- `CancelAppointmentView`: Cancel appointment

**URL Patterns**:
- `/` - Home page
- `/doctors/search/` - Search doctors
- `/doctors/<id>/` - Doctor detail
- `/doctor/availability/` - Manage availability
- `/appointment/book/<availability_id>/` - Book appointment
- `/appointment/<uuid>/` - Appointment detail
- `/appointment/<uuid>/join/` - Join consultation
- `/patient/appointments/` - Patient appointments
- `/doctor/appointments/` - Doctor appointments
- `/appointment/<uuid>/update-status/` - Update status
- `/appointment/<uuid>/cancel/` - Cancel appointment

### 3. **payment_app** - Payment Processing

**Purpose**: Payment integration with Razorpay

**Files**:
- `models.py`: Payment, Receipt models
- `views.py`: Payment checkout, callback, receipt views
- `urls.py`: URL routing
- `admin.py`: Admin configuration

**Key Views**:
- `PaymentCheckoutView`: Create payment order
- `PaymentCallbackView`: Handle payment callback (CSRF exempt)
- `ReceiptDetailView`: View payment receipt

**Payment Flow**:
1. Patient books appointment → Redirected to payment
2. Payment order created via Razorpay API
3. Patient completes payment
4. Razorpay sends callback
5. Payment verified and receipt generated
6. Appointment status updated to CONFIRMED

**URL Patterns**:
- `/payment/checkout/<appointment_id>/` - Payment checkout
- `/payment/callback/` - Payment callback
- `/payment/receipt/<uuid>/` - View receipt

### 4. **chat_app** - Real-time Messaging

**Purpose**: WebSocket-based real-time chat during consultations

**Files**:
- `models.py`: ChatMessage model
- `consumers.py`: WebSocket consumer (ChatConsumer)
- `views.py`: Chat history views
- `routing.py`: WebSocket URL routing
- `urls.py`: HTTP URL routing
- `admin.py`: Admin configuration

**WebSocket Consumer** (`ChatConsumer`):
- Connects to appointment-specific chat room
- Handles message sending/receiving
- Saves messages to database
- Broadcasts to room group
- Permission checking

**Key Views**:
- `ChatHistoryView`: Display chat history
- `LoadMessagesView`: AJAX endpoint for loading messages

**URL Patterns**:
- `/chat/appointment/<uuid>/` - Chat history
- `/chat/appointment/<uuid>/messages/` - Load messages (AJAX)
- `/ws/chat/<uuid>/` - WebSocket endpoint

### 5. **transcription_app** - Audio Transcription

**Purpose**: Convert consultation audio to text using Deepgram

**Files**:
- `models.py`: Transcription model
- `services.py`: TranscriptionService class
- `views.py`: Transcription creation and status views
- `urls.py`: URL routing
- `admin.py`: Admin configuration

**TranscriptionService**:
- `process_audio()`: Process audio file with Deepgram API
- `send_transcription_emails()`: Email transcription to patient and doctor

**Key Views**:
- `TranscriptionCreateView`: Create transcription from audio
- `TranscriptionStatusView`: Check transcription status
- `TranscriptionDetailView`: View transcription

**URL Patterns**:
- `/transcription/create/<appointment_id>/` - Create transcription
- `/transcription/status/<uuid>/` - Check status
- `/transcription/detail/<uuid>/` - View transcription

### 6. **chikitsa360** - Project Configuration

**Files**:
- `settings.py`: Django settings
- `urls.py`: Root URL configuration
- `asgi.py`: ASGI application for WebSockets
- `wsgi.py`: WSGI application

**Key Settings**:
- Custom User model: `auth_app.User`
- Authentication backends: EmailBackend, ModelBackend
- Channel layers: InMemoryChannelLayer
- Database: PostgreSQL (configurable via environment)
- Static files: WhiteNoise
- Security: CSP, CSRF protection, CORS

---

## Features & Implementations

### 1. **User Authentication & Authorization**

#### Email-Based Authentication
- Custom `EmailBackend` for email/password login
- Username field optional (email is primary identifier)
- Role-based access control (ADMIN, DOCTOR, PATIENT)

#### Registration Flow
1. User selects role (Patient or Doctor)
2. Provides email, password, name
3. Profile automatically created
4. DoctorProfile created if role is DOCTOR
5. Auto-login after registration
6. Doctors redirected to complete profile

#### Role-Based Access Control
- Mixins for role verification
- Permission checks in views
- Template-level role checks
- Admin panel access control

### 2. **Doctor Search & Discovery**

#### Search Functionality
- Search by doctor name
- Search by specialty
- Filter by available date
- Display featured doctors on homepage
- Pagination support

#### Doctor Profile Display
- Professional information
- Specialty and experience
- Consultation fee
- Education and affiliations
- Available time slots (next 7 days)
- Hospital affiliations

### 3. **Appointment Management**

#### Availability Management (Doctors)
- Create availability slots (date + time range)
- View all availability slots grouped by date
- Delete unbooked slots
- Validation: No past dates, start < end time
- Unique constraint: (doctor, date, start_time)

#### Appointment Booking (Patients)
1. Patient selects available slot
2. Provides consultation reason
3. Availability marked as booked
4. Appointment created with REQUESTED status
5. Redirected to payment page

#### Appointment Status Management
- **REQUESTED**: Initial booking state
- **CONFIRMED**: After successful payment
- **COMPLETED**: After consultation ends
- **CANCELLED**: Cancelled by patient/doctor
- **NO_SHOW**: Patient didn't attend

#### Appointment Views
- Patient: Upcoming and past appointments
- Doctor: Today's, upcoming, and past appointments
- Appointment detail page with all information
- Status update capability (doctors)
- Cancellation (patients and doctors)

### 4. **Video Consultations**

#### Daily.co Integration
- Room creation via Daily.co API
- Token-based authentication
- Room expiration (2 hours)
- WebRTC infrastructure

#### Video Call Flow
1. Appointment must be CONFIRMED
2. Check if within join window (15 min before to 1 hour after)
3. Create Daily.co room if not exists
4. Generate access token
5. Load video room interface
6. Auto-join on page load

#### Video Room Features
- Local and remote video streams
- Audio mute/unmute
- Video enable/disable
- Call timer
- End call button
- Chat integration
- Audio recording for transcription

#### Video Room Implementation (`static/js/video.js`)
- Daily.co SDK integration
- MediaRecorder API for audio capture
- Event handlers for call events
- Automatic recording start/stop
- Transcription submission on call end

### 5. **Real-time Chat**

#### WebSocket Implementation
- Django Channels for WebSocket support
- Appointment-specific chat rooms
- Real-time message broadcasting
- Message persistence in database

#### Chat Features
- Send/receive messages instantly
- Message history loading
- Read/unread status
- Sender identification
- Timestamp display
- Auto-scroll to latest message

#### Chat Consumer (`chat_app/consumers.py`)
- Async WebSocket consumer
- Permission checking
- Message saving
- Group broadcasting
- Connection management

### 6. **Audio Transcription**

#### Transcription Flow
1. Audio recorded during video call
2. Audio blob created on call end
3. Submitted to `/transcription/create/<appointment_id>/`
4. TranscriptionService processes audio
5. Deepgram API called with audio file
6. Transcript extracted and saved
7. Emails sent to patient and doctor

#### Deepgram Integration
- API key authentication
- Audio file upload (WebM format)
- Language detection enabled
- Punctuation enabled
- Utterances enabled
- Error handling and retry logic

#### Transcription Status
- PENDING: Created but not processed
- PROCESSING: Currently being transcribed
- COMPLETED: Successfully transcribed
- FAILED: Error occurred

#### Email Notifications
- HTML email templates
- Patient email: Consultation transcript
- Doctor email: Consultation transcript
- Includes appointment details and duration

### 7. **Payment Processing**

#### Razorpay Integration
- Order creation
- Payment verification
- Signature validation
- Receipt generation

#### Payment Flow
1. Patient books appointment
2. Redirected to payment checkout
3. Razorpay order created
4. Payment details stored in Payment model
5. Patient completes payment on Razorpay
6. Callback received and verified
7. Payment status updated to COMPLETED
8. Appointment status updated to CONFIRMED
9. Receipt generated with tax calculation (18% GST)

#### Payment Simulation Mode
- `RAZORPAY_ENABLED` setting
- When disabled, simulates successful payment
- Useful for development/testing

#### Receipt Generation
- Unique receipt number format: `R{YYYYMMDD}-{hex}`
- Tax calculation (18% GST)
- Total amount calculation
- PDF-ready format (can be extended)

### 8. **Email Notifications**

#### SMTP Configuration
- Gmail SMTP server
- TLS encryption
- HTML email support
- Template-based emails

#### Email Types
- Appointment confirmations
- Transcription delivery
- System notifications

### 9. **Content Management**

#### Services Management
- Dynamic service listing
- Icon support (FontAwesome)
- Display order control
- Active/inactive status

#### Testimonials
- Patient testimonials
- Rating system (1-5 stars)
- Featured testimonials
- Approval workflow
- Anonymous or named

#### Health Tips
- Health articles/tips
- Author attribution
- Featured tips
- Image support
- Creation date tracking

### 10. **Admin Panel**

#### Django Admin Features
- User management
- Doctor profile management
- Appointment management
- Payment tracking
- Service management
- Testimonial approval
- Health tip management

#### Admin Dashboard
- Total users count
- Total doctors count
- Total patients count
- Additional statistics (extensible)

---

## Security Implementation

### 1. **Authentication Security**
- Password hashing (Django's PBKDF2)
- CSRF protection on all forms
- Session-based authentication
- Secure cookie settings (production)
- Email-based login (reduces username enumeration)

### 2. **Authorization Security**
- Role-based access control
- Permission checks in views
- Mixins for access control
- Template-level permission checks

### 3. **Data Security**
- UUID primary keys (non-sequential)
- SQL injection prevention (Django ORM)
- XSS protection (template escaping)
- CSRF tokens on all forms

### 4. **Content Security Policy (CSP)**
- Configured in settings.py
- Script sources whitelisted
- Style sources whitelisted
- Frame sources for Daily.co
- Media sources for video

### 5. **HTTPS Configuration**
- SSL redirect (production)
- Secure cookies (production)
- CSRF secure cookies (production)
- HSTS headers (production)

### 6. **API Security**
- Razorpay signature verification
- Deepgram API key protection
- Daily.co token expiration
- Environment variable protection

### 7. **File Upload Security**
- File type validation (implicit)
- Size limits (implicit)
- Secure file storage

### 8. **Session Security**
- Session cookie secure flag
- SameSite cookie policy
- Session timeout (default Django)

---

## API Integrations

### 1. **Daily.co API**

#### Endpoints Used
- `POST https://api.daily.co/v1/rooms` - Create room
- `POST https://api.daily.co/v1/meeting-tokens` - Generate token

#### Implementation
```python
# Room creation
headers = {
    'Authorization': f'Bearer {DAILY_API_KEY}',
    'Content-Type': 'application/json'
}
data = {
    'name': room_name,
    'properties': {
        'enable_chat': True,
        'start_audio_off': False,
        'start_video_off': False,
        'exp': expiration_timestamp
    }
}
response = requests.post('https://api.daily.co/v1/rooms', headers=headers, json=data)
```

#### Features
- Room name generation (UUID-based)
- Token expiration (2 hours)
- Chat enabled
- Audio/video settings

### 2. **Deepgram API**

#### Endpoint Used
- `POST https://api.deepgram.com/v1/listen` - Transcribe audio

#### Implementation
```python
headers = {
    "Authorization": f"Token {DEEPGRAM_API_KEY}",
    "Content-Type": "audio/webm"
}
params = {
    "model": "general",
    "language": "en-US",
    "detect_language": "true",
    "punctuate": "true",
    "utterances": "true"
}
response = requests.post(
    "https://api.deepgram.com/v1/listen",
    headers=headers,
    params=params,
    data=audio_file
)
```

#### Features
- Multi-language support
- Automatic language detection
- Punctuation enabled
- Utterance segmentation
- Error handling

### 3. **Razorpay API**

#### Endpoints Used
- `POST /orders` - Create order
- Payment verification (utility method)

#### Implementation
```python
client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))
order = client.order.create({
    'amount': amount_in_paisa,
    'currency': 'INR',
    'receipt': receipt_id,
    'notes': {...}
})
```

#### Features
- Order creation
- Payment verification
- Signature validation
- Receipt generation

### 4. **SMTP (Gmail)**

#### Configuration
- Host: smtp.gmail.com
- Port: 587
- TLS: Enabled
- Authentication: App password

#### Implementation
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
```

---

## Frontend Implementation

### 1. **Template Structure**

#### Base Template (`templates/base.html`)
- Header with navigation
- User menu dropdown
- Mobile menu
- Footer with links
- Message display system
- CSRF token inclusion

#### Key Templates
- `index.html`: Landing page
- `auth/login.html`: Login page
- `auth/register.html`: Registration
- `auth/profile.html`: User profile
- `consultation/video_room.html`: Video consultation
- `doctor/doctor_detail.html`: Doctor profile
- `patient/book_appointment.html`: Booking form
- `payment/checkout.html`: Payment page
- `payment/receipt.html`: Receipt display

### 2. **JavaScript Modules**

#### `static/js/main.js`
- CSRF token handling
- AJAX setup
- Form validation
- Date/time formatting
- Notification system
- Menu toggles

#### `static/js/video.js`
- Daily.co SDK integration
- Video call management
- Audio recording
- Transcription submission
- Chat integration
- Call controls (mute, video toggle)

#### `static/js/chat.js`
- WebSocket connection
- Message sending/receiving
- Chat history loading
- Auto-scroll
- Connection status

#### `static/js/payment.js`
- Razorpay integration
- Payment form handling
- Callback processing

#### `static/js/animations.js`
- Scroll animations
- Fade-in effects
- Slide-up animations

### 3. **CSS Styling**

#### `static/css/custom.css`
- Custom color variables
- Button styles
- Card styles
- Hero section
- Service icons
- Testimonial styles
- Responsive design

#### Tailwind CSS
- Utility-first approach
- Responsive breakpoints
- Custom configuration
- Component classes

### 4. **UI Components**

#### Buttons
- Primary button (teal)
- Secondary button (outline)
- Icon buttons

#### Cards
- Service cards
- Doctor cards
- Testimonial cards
- Health tip cards

#### Forms
- Styled form inputs
- Validation feedback
- Error display

#### Navigation
- Desktop menu
- Mobile menu
- User dropdown
- Breadcrumbs

---

## Deployment Configuration

### 1. **Environment Variables**

#### Required Variables
```env
SECRET_KEY=django-secret-key
DEBUG=False
PGDATABASE=chikitsa360
PGUSER=postgres
PGPASSWORD=password
PGHOST=localhost
PGPORT=5432
RAZORPAY_KEY_ID=key_id
RAZORPAY_KEY_SECRET=key_secret
DAILY_API_KEY=daily_api_key
DEEPGRAM_API_KEY=deepgram_api_key
OPENAI_API_KEY=openai_api_key (optional)
```

### 2. **Database Configuration**

#### Development
- PostgreSQL local instance
- Environment-based configuration

#### Production
- `dj-database-url` for URL parsing
- Database URL from environment

### 3. **Static Files**

#### Configuration
- `STATIC_URL = 'static/'`
- `STATICFILES_DIRS = [BASE_DIR / 'static']`
- `STATIC_ROOT = BASE_DIR / 'staticfiles'`
- WhiteNoise for serving

#### Collection
```bash
python manage.py collectstatic
```

### 4. **ASGI Configuration**

#### Channel Layers
- InMemoryChannelLayer (development)
- Redis recommended for production

#### ASGI Application
- HTTP protocol routing
- WebSocket protocol routing
- Authentication middleware

### 5. **Server Configuration**

#### Development
- `python manage.py runserver`
- Daphne for ASGI

#### Production
- Gunicorn (WSGI)
- Daphne (ASGI)
- Nginx reverse proxy (recommended)
- Koyeb deployment ready

### 6. **Security Settings (Production)**

```python
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SAMESITE = 'Lax'
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'
X_FRAME_OPTIONS = 'DENY'
```

### 7. **CORS Configuration**

```python
CORS_ALLOW_ALL_ORIGINS = True  # Development
# CORS_ALLOWED_ORIGINS = [...]  # Production
CORS_ALLOW_METHODS = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS']
```

---

## UML Diagrams

### 1. **Class Diagram (Simplified)**

```
┌─────────────────┐
│      User       │
├─────────────────┤
│ +email          │
│ +role           │
│ +is_verified    │
│ +is_admin()     │
│ +is_doctor()    │
│ +is_patient()   │
└────────┬────────┘
         │
         ├─────────────────┐
         │                 │
    ┌────▼────┐      ┌─────▼─────┐
    │ Profile │      │DoctorProfile│
    ├─────────┤      ├────────────┤
    │+phone   │      │+specialty  │
    │+address │      │+fee        │
    └─────────┘      └────────────┘

┌─────────────────┐
│  Availability   │
├─────────────────┤
│ +doctor         │
│ +date           │
│ +start_time     │
│ +end_time       │
│ +is_booked      │
└────────┬────────┘
         │
         │ 1:1
         │
┌────────▼────────┐
│   Appointment   │
├─────────────────┤
│ +patient        │
│ +doctor         │
│ +status         │
│ +video_room_id  │
└────────┬────────┘
         │
    ┌────┴────┬──────────┬─────────────┐
    │         │          │             │
┌───▼───┐ ┌──▼───┐ ┌─────▼────┐ ┌──────▼─────┐
│Payment│ │Trans │ │ChatMessage│ │Availability│
└───────┘ └──────┘ └───────────┘ └────────────┘
```

### 2. **Sequence Diagram - Appointment Booking**

```
Patient    Doctor    System    Payment    Video
  │          │         │         │         │
  │──Search──>│         │         │         │
  │<──List───│         │         │         │
  │          │         │         │         │
  │──Select──>│         │         │         │
  │          │         │         │         │
  │──Book────>│         │         │         │
  │          │         │         │         │
  │          │<─Create─│         │         │
  │          │         │         │         │
  │<─Redirect─│         │         │         │
  │          │         │         │         │
  │──Pay─────>│         │         │         │
  │          │         │<─Verify─>│         │
  │          │         │         │         │
  │<─Confirm──│         │         │         │
  │          │         │         │         │
  │──Join────>│         │         │<─Room───│
  │          │         │         │         │
  │<─Video────│         │         │         │
```

### 3. **Sequence Diagram - Video Consultation**

```
Patient    Doctor    Video    Transcription
  │          │         │            │
  │──Join───>│         │            │
  │          │<─Room───│            │
  │          │         │            │
  │<─Stream──│         │            │
  │          │         │            │
  │──Chat───>│         │            │
  │          │         │            │
  │──End────>│         │            │
  │          │         │            │
  │          │<─Audio──│            │
  │          │         │            │
  │          │──Submit─────────────>│
  │          │         │            │
  │          │<─Transcript──────────│
  │          │         │            │
  │<─Email───│         │            │
```

### 4. **State Diagram - Appointment Status**

```
[REQUESTED] ──payment──> [CONFIRMED] ──join──> [IN_PROGRESS]
     │                         │                      │
     │                         │                      │
     └──cancel──> [CANCELLED]  │                      │
                                │                      │
                                │                      │
                                └──end──> [COMPLETED] │
                                                      │
                                                      │
                                                      └──no_show──> [NO_SHOW]
```

### 5. **Component Diagram**

```
┌─────────────────────────────────────────┐
│         Django Application               │
│                                         │
│  ┌──────────┐  ┌──────────┐  ┌──────┐ │
│  │auth_app  │  │consult   │  │payment│ │
│  └──────────┘  └──────────┘  └──────┘ │
│                                         │
│  ┌──────────┐  ┌──────────┐            │
│  │chat_app  │  │transcript│            │
│  └──────────┘  └──────────┘            │
└─────────────────────────────────────────┘
         │              │              │
         │              │              │
    ┌────▼────┐   ┌────▼────┐   ┌─────▼────┐
    │PostgreSQL│   │Daily.co │   │Deepgram  │
    └──────────┘   └─────────┘   └──────────┘
         │
    ┌────▼────┐
    │Razorpay │
    └─────────┘
```

---

## Workflows & User Journeys

### 1. **Patient Registration & Booking Flow**

1. **Registration**
   - Visit homepage
   - Click "Sign Up"
   - Select "Patient" role
   - Fill registration form
   - Submit → Profile created
   - Redirected to patient dashboard

2. **Finding a Doctor**
   - Use search on homepage
   - Filter by specialty/date
   - View doctor profiles
   - See available slots

3. **Booking Appointment**
   - Select available slot
   - Provide consultation reason
   - Submit booking
   - Redirected to payment

4. **Payment**
   - View appointment details
   - Complete payment (Razorpay)
   - Payment verified
   - Appointment confirmed
   - Receipt generated

5. **Attending Consultation**
   - View appointment in dashboard
   - Click "Join Consultation" (15 min before)
   - Video room loads
   - Auto-join call
   - Consult with doctor
   - Use chat if needed
   - End call

6. **Post-Consultation**
   - Audio automatically submitted
   - Transcription processed
   - Email received with transcript
   - View appointment details

### 2. **Doctor Registration & Management Flow**

1. **Registration**
   - Visit homepage
   - Click "Sign Up"
   - Select "Doctor" role
   - Fill registration form
   - Submit → Profile + DoctorProfile created
   - Redirected to complete doctor profile

2. **Profile Completion**
   - Enter specialty
   - Add license number
   - Set consultation fee
   - Add education details
   - Add hospital affiliation
   - Save profile

3. **Setting Availability**
   - Go to "My Availability"
   - Select date
   - Set time range
   - Add multiple slots
   - View grouped by date

4. **Managing Appointments**
   - View appointments dashboard
   - See today's, upcoming, past
   - View appointment details
   - Update status (CONFIRMED → COMPLETED)
   - Add notes

5. **Conducting Consultation**
   - Join video call
   - Consult with patient
   - Use chat for clarifications
   - End call

6. **Post-Consultation**
   - Transcription automatically generated
   - Email received with transcript
   - Review appointment notes

### 3. **Video Consultation Flow**

1. **Pre-Call**
   - Appointment must be CONFIRMED
   - Check join window (15 min before to 1 hour after)
   - Create Daily.co room (if not exists)
   - Generate access token

2. **Call Initialization**
   - Load video room page
   - Initialize Daily.co SDK
   - Request media permissions
   - Join room with token

3. **During Call**
   - Video streams active
   - Audio recording starts automatically
   - Chat available
   - Mute/unmute controls
   - Video toggle controls
   - Call timer display

4. **Call End**
   - Stop audio recording
   - Create audio blob
   - Submit for transcription
   - Leave Daily.co room
   - Update UI

5. **Post-Call**
   - Transcription processing
   - Status updates (PENDING → PROCESSING → COMPLETED)
   - Email notifications sent
   - Appointment can be marked COMPLETED

### 4. **Chat Flow**

1. **Connection**
   - WebSocket connects to `/ws/chat/<appointment_id>/`
   - Permission check (patient or doctor)
   - Join appointment-specific room

2. **Message Sending**
   - User types message
   - Submit via form or Enter key
   - Message sent via WebSocket
   - Saved to database
   - Broadcast to room group

3. **Message Receiving**
   - WebSocket receives message
   - Display in chat UI
   - Mark as read (if not sender)
   - Auto-scroll to bottom

4. **History Loading**
   - Load previous messages on page load
   - AJAX endpoint for incremental loading
   - Display with sender info and timestamps

### 5. **Transcription Flow**

1. **Audio Capture**
   - MediaRecorder API captures audio during call
   - Audio chunks collected
   - Blob created on call end

2. **Submission**
   - FormData created with audio blob
   - POST to `/transcription/create/<appointment_id>/`
   - Transcription record created (PENDING)

3. **Processing**
   - TranscriptionService.process_audio() called
   - Status updated to PROCESSING
   - Audio file sent to Deepgram API
   - Transcript extracted from response

4. **Completion**
   - Transcript saved to database
   - Status updated to COMPLETED
   - Audio duration recorded
   - Emails sent to patient and doctor

5. **Error Handling**
   - If processing fails, status set to FAILED
   - Error message stored
   - User notified

---

## Additional Technical Details

### 1. **Custom Authentication Backend**

**File**: `auth_app/backends.py`

```python
class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
```

**Features**:
- Email as username
- Password verification
- User retrieval

### 2. **Custom User Manager**

**File**: `auth_app/models.py`

```python
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        # Email normalization
        # Password hashing
        # User creation
    
    def create_superuser(self, email, password=None, **extra_fields):
        # Superuser creation with admin role
```

### 3. **Form Validation**

**Custom Validation**:
- Email uniqueness check
- Date validation (no past dates)
- Time validation (start < end)
- Availability slot uniqueness

### 4. **Property Methods**

**Appointment Model**:
- `is_past`: Check if appointment date/time is past
- `is_today`: Check if appointment is today
- `can_join`: Check if within join window

**Availability Model**:
- `is_past`: Check if slot is in the past

### 5. **Template Tags**

**File**: `consultation_app/templatetags/form_filters.py`
- Custom template filters for form rendering

### 6. **Middleware Stack**

1. CORS Middleware
2. Security Middleware
3. Session Middleware
4. Common Middleware
5. CSRF Middleware
6. Authentication Middleware
7. Message Middleware
8. Clickjacking Protection
9. WhiteNoise Middleware
10. CSP Middleware

### 7. **URL Routing**

**Pattern**: App-based URL includes
- Root URLs include app URLs
- Namespace support ready
- Reverse URL lookups

### 8. **Static Files Organization**

```
static/
├── css/
│   ├── custom.css
│   └── tailwind.css
├── js/
│   ├── main.js
│   ├── video.js
│   ├── chat.js
│   ├── payment.js
│   └── animations.js
└── images/
    ├── chikitsa360-logo.png
    └── chikitsa360-logo.svg
```

### 9. **Template Organization**

```
templates/
├── base.html
├── index.html
├── auth/
│   ├── login.html
│   ├── register.html
│   ├── profile.html
│   └── edit_profile.html
├── consultation/
│   ├── video_room.html
│   ├── appointment_detail.html
│   └── doctor_availability.html
├── doctor/
│   ├── dashboard.html
│   ├── doctor_detail.html
│   └── doctor_appointments.html
├── patient/
│   ├── dashboard.html
│   ├── book_appointment.html
│   └── patient_appointments.html
├── payment/
│   ├── checkout.html
│   └── receipt.html
└── transcription/
    ├── email_patient.html
    └── email_doctor.html
```

---

## Performance Considerations

### 1. **Database Optimization**
- Indexed foreign keys
- Unique constraints
- Query optimization (select_related, prefetch_related ready)
- Pagination for lists

### 2. **Caching** (Ready for Implementation)
- Template caching ready
- Query caching ready
- Redis support ready (for production)

### 3. **Static Files**
- WhiteNoise for serving
- CDN ready (can be configured)
- Compression ready

### 4. **Async Operations**
- WebSocket consumers (async)
- Transcription processing (can be async)
- Email sending (can be async)

---

## Testing Considerations

### 1. **Unit Tests** (To be implemented)
- Model tests
- View tests
- Form tests
- Service tests

### 2. **Integration Tests** (To be implemented)
- Authentication flow
- Appointment booking flow
- Payment flow
- Video call flow

### 3. **WebSocket Tests** (To be implemented)
- Chat consumer tests
- Message broadcasting tests

---

## Future Enhancements

### 1. **Potential Features**
- Prescription management
- Medical records storage
- Appointment reminders (SMS/Email)
- Doctor ratings and reviews
- Multi-language support
- Mobile app (React Native)
- Push notifications
- File sharing during consultations
- Screen sharing
- Recording of video calls
- Analytics dashboard
- Reporting system

### 2. **Technical Improvements**
- Redis for channel layers (production)
- Celery for async tasks
- Elasticsearch for doctor search
- CDN for static files
- Docker containerization
- CI/CD pipeline
- Comprehensive test suite
- API documentation (DRF)
- Monitoring and logging (Sentry)

---

## Conclusion

Chikitsa360 is a comprehensive telemedicine platform built with modern web technologies. It provides a complete solution for remote healthcare consultations with features including:

- Secure user authentication and authorization
- Doctor discovery and appointment booking
- Real-time video consultations
- Automated transcription services
- Payment processing
- Real-time chat
- Content management

The platform is built with scalability, security, and user experience in mind, using industry-standard practices and modern web technologies. The modular architecture allows for easy extension and maintenance.

---

**Document Version**: 1.0  
**Last Updated**: 2025  
**Author**: Project Analysis  
**Project**: Chikitsa360 - Telemedicine Platform


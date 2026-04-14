from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .models import User, Profile, DoctorProfile
from django.contrib.auth import get_user_model
class CustomAuthenticationForm(AuthenticationForm):
    """Custom authentication form with styling."""
    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'class': 'w-full px-4 py-2 border rounded-md', 'placeholder': 'Email'})
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'w-full px-4 py-2 border rounded-md', 'placeholder': 'Password'})
    )

class UserRegistrationForm(UserCreationForm):
    """Form for user registration."""
    role = forms.ChoiceField(
        choices=[(User.Role.PATIENT, 'Patient'), (User.Role.DOCTOR, 'Doctor')],
        widget=forms.RadioSelect(attrs={'class': 'mr-2'}),
        initial=User.Role.PATIENT
    )
    
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-md', 'placeholder': 'First Name'})
    )
    
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-md', 'placeholder': 'Last Name'})
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'w-full px-4 py-2 border rounded-md', 'placeholder': 'Email'})
    )
    
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'w-full px-4 py-2 border rounded-md', 'placeholder': 'Password'})
    )
    
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'w-full px-4 py-2 border rounded-md', 'placeholder': 'Confirm Password'})
    )

    # Doctor-only fields (validated when role == DOCTOR)
    specialty = forms.CharField(
        required=False,
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-md', 'placeholder': 'Specialty'})
    )
    license_number = forms.CharField(
        required=False,
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-md', 'placeholder': 'License Number'})
    )
    experience_years = forms.IntegerField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'w-full px-4 py-2 border rounded-md', 'placeholder': 'Years of Experience'})
    )
    consultation_fee = forms.DecimalField(
        required=False,
        max_digits=10,
        decimal_places=2,
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'w-full px-4 py-2 border rounded-md', 'placeholder': 'Consultation Fee (INR)'})
    )
    bio = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'w-full px-4 py-2 border rounded-md', 'rows': 4, 'placeholder': 'Professional Bio'})
    )
    education = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'w-full px-4 py-2 border rounded-md', 'rows': 3, 'placeholder': 'Education & Qualifications'})
    )
    hospital_affiliation = forms.CharField(
        required=False,
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-md', 'placeholder': 'Hospital Affiliation (optional)'})
    )
    languages_spoken = forms.CharField(
        required=False,
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-md', 'placeholder': 'Languages Spoken (optional)'})
    )
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2', 'role')
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists")
        return email

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get("role")
        if role != User.Role.DOCTOR:
            return cleaned_data

        required_doctor_fields = [
            ("specialty", "Specialty is required for doctor registration."),
            ("license_number", "License number is required for doctor registration."),
            ("experience_years", "Years of experience is required for doctor registration."),
            ("consultation_fee", "Consultation fee is required for doctor registration."),
            ("bio", "Professional bio is required for doctor registration."),
            ("education", "Education details are required for doctor registration."),
        ]

        for field_name, message in required_doctor_fields:
            value = cleaned_data.get(field_name)
            if value in (None, ""):
                self.add_error(field_name, message)

        license_number = cleaned_data.get("license_number")
        if license_number and DoctorProfile.objects.filter(license_number__iexact=license_number.strip()).exists():
            self.add_error("license_number", "This license number is already registered.")

        return cleaned_data

    def get_doctor_profile_data(self):
        """Return normalized doctor profile values from cleaned_data."""
        return {
            "specialty": (self.cleaned_data.get("specialty") or "").strip(),
            "license_number": (self.cleaned_data.get("license_number") or "").strip(),
            "experience_years": self.cleaned_data.get("experience_years"),
            "consultation_fee": self.cleaned_data.get("consultation_fee"),
            "bio": (self.cleaned_data.get("bio") or "").strip(),
            "education": (self.cleaned_data.get("education") or "").strip(),
            "hospital_affiliation": (self.cleaned_data.get("hospital_affiliation") or "").strip() or None,
            "languages_spoken": (self.cleaned_data.get("languages_spoken") or "").strip() or None,
        }

class ProfileForm(forms.ModelForm):
    """Form for user profile information."""
    phone_number = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-md', 'placeholder': 'Phone Number'})
    )
    
    address = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'w-full px-4 py-2 border rounded-md', 'rows': 3, 'placeholder': 'Address'})
    )
    
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'w-full px-4 py-2 border rounded-md', 'type': 'date'})
    )
    
    class Meta:
        model = Profile
        fields = ('phone_number', 'address', 'date_of_birth')

class DoctorProfileForm(forms.ModelForm):
    """Form for doctor-specific profile information (all key fields required)."""

    class Meta:
        model = DoctorProfile
        fields = [
            'specialty', 'license_number', 'experience_years',
            'consultation_fee', 'bio', 'education',
            'hospital_affiliation', 'languages_spoken'
        ]
        labels = {
            'specialty': 'Specialty',
            'license_number': 'License Number',
            'experience_years': 'Years of Experience',
            'consultation_fee': 'Consultation Fee (INR)',
            'bio': 'Professional Bio',
            'education': 'Education & Qualifications',
            'hospital_affiliation': 'Hospital Affiliation (optional)',
            'languages_spoken': 'Languages Spoken (optional)',
        }
        widgets = {
            'specialty': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-md', 'placeholder': 'Specialty *', 'data-required': 'true'}),
            'license_number': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-md', 'placeholder': 'License Number *', 'data-required': 'true'}),
            'experience_years': forms.NumberInput(attrs={'class': 'w-full px-4 py-2 border rounded-md', 'placeholder': 'Years of Experience *', 'min': 0, 'data-required': 'true'}),
            'consultation_fee': forms.NumberInput(attrs={'class': 'w-full px-4 py-2 border rounded-md', 'placeholder': 'Consultation Fee (INR) *', 'min': 0, 'data-required': 'true'}),
            'bio': forms.Textarea(attrs={'class': 'w-full px-4 py-2 border rounded-md', 'rows': 5, 'placeholder': 'Professional Bio *', 'data-required': 'true'}),
            'education': forms.Textarea(attrs={'class': 'w-full px-4 py-2 border rounded-md', 'rows': 3, 'placeholder': 'Education & Qualifications *', 'data-required': 'true'}),
            'hospital_affiliation': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-md', 'placeholder': 'Hospital Affiliation (optional)'}),
            'languages_spoken': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-md', 'placeholder': 'Languages Spoken (optional)'}),
        }

User = get_user_model()

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone_number', 'address', 'date_of_birth']

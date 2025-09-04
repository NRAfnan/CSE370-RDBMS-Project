from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import (
    ElderProfile, Medication, MedicationSchedule, MedicationLog, 
    Appointment, CareTask, EmergencyContact, VitalsLog, 
    IncidentReport, Notification, UserProfile
)

class ElderForm(forms.ModelForm):
    class Meta:
        model = ElderProfile
        fields = [
            'guardian', 'full_name', 'date_of_birth', 'gender', 'address', 
            'phone', 'email', 'medical_conditions', 'allergies', 
            'blood_type', 'emergency_notes'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
            'medical_conditions': forms.Textarea(attrs={'rows': 4}),
            'allergies': forms.Textarea(attrs={'rows': 3}),
            'emergency_notes': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Get the current user
        super().__init__(*args, **kwargs)
        
        # Restrict guardian selection based on user permissions
        if self.user:
            try:
                user_profile = self.user.profile
                if user_profile and user_profile.user_type == 'ADMIN':
                    # Admin can assign to any user
                    self.fields['guardian'].queryset = User.objects.all().order_by('username')
                else:
                    # Non-admin users can only assign to themselves
                    self.fields['guardian'].queryset = User.objects.filter(id=self.user.id)
                    self.fields['guardian'].initial = self.user
                    self.fields['guardian'].widget.attrs['readonly'] = 'readonly'
                    self.fields['guardian'].widget.attrs['class'] = 'form-control bg-light'
                    self.fields['guardian'].help_text = 'You can only add elders for yourself.'
            except UserProfile.DoesNotExist:
                # No profile means not admin - restrict to self only
                self.fields['guardian'].queryset = User.objects.filter(id=self.user.id)
                self.fields['guardian'].initial = self.user
                self.fields['guardian'].widget.attrs['readonly'] = 'readonly'
                self.fields['guardian'].widget.attrs['class'] = 'form-control bg-light'
                self.fields['guardian'].help_text = 'You can only add elders for yourself.'
    
    def clean_guardian(self):
        """Validate guardian selection based on user permissions"""
        guardian = self.cleaned_data.get('guardian')
        
        if self.user:
            try:
                user_profile = self.user.profile
                if not user_profile or user_profile.user_type != 'ADMIN':
                    # Non-admin users can only assign to themselves
                    if guardian != self.user:
                        raise forms.ValidationError("You can only add elders for yourself.")
            except UserProfile.DoesNotExist:
                # No profile means not admin
                if guardian != self.user:
                    raise forms.ValidationError("You can only add elders for yourself.")
        
        return guardian

class MedicationForm(forms.ModelForm):
    class Meta:
        model = Medication
        fields = ['name', 'description', 'medication_type', 'strength', 'manufacturer']

class MedicationScheduleForm(forms.ModelForm):
    class Meta:
        model = MedicationSchedule
        fields = [
            'elder', 'medication', 'dosage', 'frequency', 'start_date',
            'end_date', 'time_1', 'time_2', 'time_3', 'instructions'
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'time_1': forms.TimeInput(attrs={'type': 'time'}),
            'time_2': forms.TimeInput(attrs={'type': 'time'}),
            'time_3': forms.TimeInput(attrs={'type': 'time'}),
            'instructions': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            try:
                up = self.user.profile
                if up and up.user_type in ['ADMIN', 'DOCTOR', 'NURSE', 'CAREGIVER']:
                    self.fields['elder'].queryset = ElderProfile.objects.all()
                else:
                    self.fields['elder'].queryset = ElderProfile.objects.filter(guardian=self.user)
            except UserProfile.DoesNotExist:
                self.fields['elder'].queryset = ElderProfile.objects.filter(guardian=self.user)

    def clean_elder(self):
        elder = self.cleaned_data.get('elder')
        if not self.user or not elder:
            return elder
        try:
            up = self.user.profile
            if not up or up.user_type not in ['ADMIN', 'DOCTOR', 'NURSE', 'CAREGIVER']:
                if elder.guardian_id != self.user.id:
                    raise ValidationError("Guardians can only select their own elders.")
        except UserProfile.DoesNotExist:
            if elder.guardian_id != self.user.id:
                raise ValidationError("Guardians can only select their own elders.")
        return elder

class MedicationLogForm(forms.ModelForm):
    class Meta:
        model = MedicationLog
        fields = ['notes', 'was_skipped', 'skip_reason']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
            'skip_reason': forms.Textarea(attrs={'rows': 3}),
        }

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = [
            'elder', 'title', 'appointment_type', 'appointment_date',
            'duration', 'location', 'doctor_name', 'phone', 'notes'
        ]
        widgets = {
            'appointment_date': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            try:
                up = self.user.profile
                if up and up.user_type in ['ADMIN', 'DOCTOR', 'NURSE', 'CAREGIVER']:
                    self.fields['elder'].queryset = ElderProfile.objects.all()
                else:
                    self.fields['elder'].queryset = ElderProfile.objects.filter(guardian=self.user)
            except UserProfile.DoesNotExist:
                self.fields['elder'].queryset = ElderProfile.objects.filter(guardian=self.user)

    def clean_elder(self):
        elder = self.cleaned_data.get('elder')
        if not self.user or not elder:
            return elder
        try:
            up = self.user.profile
            if not up or up.user_type not in ['ADMIN', 'DOCTOR', 'NURSE', 'CAREGIVER']:
                if elder.guardian_id != self.user.id:
                    raise ValidationError("Guardians can only select their own elders.")
        except UserProfile.DoesNotExist:
            if elder.guardian_id != self.user.id:
                raise ValidationError("Guardians can only select their own elders.")
        return elder

class CareTaskForm(forms.ModelForm):
    class Meta:
        model = CareTask
        fields = [
            'elder', 'title', 'description', 'task_type', 'frequency',
            'assigned_to', 'priority', 'due_date', 'notes'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'due_date': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            try:
                up = self.user.profile
                if up and up.user_type in ['ADMIN', 'DOCTOR', 'NURSE', 'CAREGIVER']:
                    self.fields['elder'].queryset = ElderProfile.objects.all()
                else:
                    self.fields['elder'].queryset = ElderProfile.objects.filter(guardian=self.user)
            except UserProfile.DoesNotExist:
                self.fields['elder'].queryset = ElderProfile.objects.filter(guardian=self.user)

    def clean_elder(self):
        elder = self.cleaned_data.get('elder')
        if not self.user or not elder:
            return elder
        try:
            up = self.user.profile
            if not up or up.user_type not in ['ADMIN', 'DOCTOR', 'NURSE', 'CAREGIVER']:
                if elder.guardian_id != self.user.id:
                    raise ValidationError("Guardians can only select their own elders.")
        except UserProfile.DoesNotExist:
            if elder.guardian_id != self.user.id:
                raise ValidationError("Guardians can only select their own elders.")
        return elder

class EmergencyContactForm(forms.ModelForm):
    class Meta:
        model = EmergencyContact
        fields = ['name', 'relation', 'phone', 'phone_2', 'email', 'address', 'is_primary', 'notes']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

class VitalsLogForm(forms.ModelForm):
    class Meta:
        model = VitalsLog
        fields = [
            'elder', 'blood_pressure_systolic', 'blood_pressure_diastolic',
            'heart_rate', 'temperature', 'weight', 'oxygen_saturation', 
            'blood_sugar', 'notes'
        ]
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

class IncidentReportForm(forms.ModelForm):
    class Meta:
        model = IncidentReport
        fields = [
            'elder', 'incident_type', 'incident_date', 'description',
            'severity', 'location', 'witnesses', 'actions_taken',
            'follow_up_required', 'follow_up_notes'
        ]
        widgets = {
            'incident_date': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
            'description': forms.Textarea(attrs={'rows': 4}),
            'location': forms.TextInput(attrs={'placeholder': 'Where did this happen?'}),
            'witnesses': forms.Textarea(attrs={'rows': 3}),
            'actions_taken': forms.Textarea(attrs={'rows': 4}),
            'follow_up_notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            try:
                up = self.user.profile
                if up and up.user_type in ['ADMIN', 'DOCTOR', 'NURSE', 'CAREGIVER']:
                    self.fields['elder'].queryset = ElderProfile.objects.all()
                else:
                    self.fields['elder'].queryset = ElderProfile.objects.filter(guardian=self.user)
            except UserProfile.DoesNotExist:
                self.fields['elder'].queryset = ElderProfile.objects.filter(guardian=self.user)

    def clean_elder(self):
        elder = self.cleaned_data.get('elder')
        if not self.user or not elder:
            return elder
        try:
            up = self.user.profile
            if not up or up.user_type not in ['ADMIN', 'DOCTOR', 'NURSE', 'CAREGIVER']:
                if elder.guardian_id != self.user.id:
                    raise ValidationError("Guardians can only select their own elders.")
        except UserProfile.DoesNotExist:
            if elder.guardian_id != self.user.id:
                raise ValidationError("Guardians can only select their own elders.")
        return elder

class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['elder', 'notification_type', 'message', 'priority', 'expires_at']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4}),
            'expires_at': forms.DateTimeInput(
                attrs={'type': 'datetime-local'}, 
                format='%Y-%m-%dT%H:%M'
            ),
        }

class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    
    class Meta:
        model = UserProfile
        fields = ['user_type', 'phone', 'address', 'emergency_contact', 'emergency_phone']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Get the current user
        super().__init__(*args, **kwargs)
        
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
        
        # Make user_type read-only for non-admin users
        if self.user:
            try:
                user_profile = self.user.profile
                if not user_profile or user_profile.user_type != 'ADMIN':
                    # Non-admin users cannot change their role
                    self.fields['user_type'].widget.attrs['readonly'] = 'readonly'
                    self.fields['user_type'].widget.attrs['class'] = 'form-control bg-light'
                    self.fields['user_type'].help_text = 'Only administrators can change user roles.'
            except UserProfile.DoesNotExist:
                # No profile means not admin
                self.fields['user_type'].widget.attrs['readonly'] = 'readonly'
                self.fields['user_type'].widget.attrs['class'] = 'form-control bg-light'
                self.fields['user_type'].help_text = 'Only administrators can change user roles.'
    
    def clean_user_type(self):
        """Prevent non-admin users from changing user_type"""
        user_type = self.cleaned_data.get('user_type')
        
        if self.user:
            try:
                user_profile = self.user.profile
                if not user_profile or user_profile.user_type != 'ADMIN':
                    # Non-admin users cannot change their role
                    if self.instance and self.instance.user_type != user_type:
                        raise forms.ValidationError("Only administrators can change user roles.")
            except UserProfile.DoesNotExist:
                # No profile means not admin
                if self.instance and self.instance.user_type != user_type:
                    raise forms.ValidationError("Only administrators can change user roles.")
        
        return user_type
    
    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            # Update User fields
            if profile.user:
                profile.user.first_name = self.cleaned_data['first_name']
                profile.user.last_name = self.cleaned_data['last_name']
                profile.user.email = self.cleaned_data['email']
                profile.user.save()
            profile.save()
        return profile

class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    user_type = forms.ChoiceField(choices=UserProfile.USER_TYPE_CHOICES, initial='CAREGIVER')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            UserProfile.objects.create(
                user=user,
                user_type=self.cleaned_data['user_type']
            )
        return user

class QuickVitalsForm(forms.Form):
    blood_pressure_systolic = forms.IntegerField(
        required=False, 
        min_value=50, 
        max_value=300,
        widget=forms.NumberInput(attrs={'placeholder': 'Systolic'})
    )
    blood_pressure_diastolic = forms.IntegerField(
        required=False, 
        min_value=30, 
        max_value=200,
        widget=forms.NumberInput(attrs={'placeholder': 'Diastolic'})
    )
    heart_rate = forms.IntegerField(
        required=False, 
        min_value=30, 
        max_value=200,
        widget=forms.NumberInput(attrs={'placeholder': 'BPM'})
    )
    temperature = forms.DecimalField(
        required=False, 
        min_value=90.0, 
        max_value=110.0,
        decimal_places=1,
        widget=forms.NumberInput(attrs={'placeholder': '°F', 'step': '0.1'})
    )
    weight = forms.DecimalField(
        required=False, 
        min_value=0, 
        max_value=999.99,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'placeholder': 'lbs', 'step': '0.01'})
    )
    oxygen_saturation = forms.IntegerField(
        required=False, 
        min_value=70, 
        max_value=100,
        widget=forms.NumberInput(attrs={'placeholder': '%'})
    )
    blood_sugar = forms.IntegerField(
        required=False, 
        min_value=20, 
        max_value=600,
        widget=forms.NumberInput(attrs={'placeholder': 'mg/dL'})
    )
    notes = forms.CharField(
        required=False, 
        widget=forms.Textarea(attrs={'rows': 2, 'placeholder': 'Additional notes...'})
    )

class SearchForm(forms.Form):
    query = forms.CharField(
        required=False, 
        widget=forms.TextInput(attrs={'placeholder': 'Search elders, medications, tasks...'})
    )
    category = forms.ChoiceField(
        choices=[
            ('all', 'All'),
            ('elders', 'Elders'),
            ('medications', 'Medications'),
            ('tasks', 'Tasks'),
            ('appointments', 'Appointments'),
        ],
        required=False,
        initial='all'
    )

#!/usr/bin/env python
"""
Script to load demo data for the eldercare platform
"""
import os
import sys
import django
from datetime import datetime, timedelta

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'special_care_platform.settings')
django.setup()

from django.contrib.auth.models import User
from care_app.models import (
    ElderProfile, Medication, MedicationSchedule, Appointment, 
    CareTask, EmergencyContact, VitalsLog, IncidentReport, Notification
)

def create_demo_data():
    print("Creating demo data...")
    
    # Create a demo user
    user, created = User.objects.get_or_create(
        username='demo_user',
        defaults={
            'first_name': 'Demo',
            'last_name': 'User',
            'email': 'demo@example.com',
            'is_staff': True,
            'is_superuser': True
        }
    )
    if created:
        user.set_password('demo123')
        user.save()
        print(f"Created demo user: {user.username}")
    
    # Create a demo elder
    elder, created = ElderProfile.objects.get_or_create(
        full_name='John Doe',
        defaults={
            'guardian': user,
            'date_of_birth': datetime(1945, 7, 20).date(),
            'gender': 'M',
            'address': '123 Main St, Springfield',
            'phone': '+1234567890',
            'email': 'john.doe@example.com',
            'medical_conditions': 'Hypertension, Diabetes',
            'allergies': 'Penicillin',
            'blood_type': 'O+',
            'emergency_notes': 'Contact daughter Jane first'
        }
    )
    if created:
        print(f"Created demo elder: {elder.full_name}")
    
    # Create demo medication
    medication, created = Medication.objects.get_or_create(
        name='Aspirin',
        defaults={
            'description': 'Used to reduce fever and pain',
            'medication_type': 'PILL',
            'strength': '81 mg',
            'manufacturer': 'Generic'
        }
    )
    if created:
        print(f"Created demo medication: {medication.name}")
    
    # Create demo vitals
    vitals, created = VitalsLog.objects.get_or_create(
        elder=elder,
        recorded_at=datetime.now() - timedelta(days=1),
        defaults={
            'blood_pressure_systolic': 120,
            'blood_pressure_diastolic': 80,
            'heart_rate': 72,
            'temperature': 98.6,
            'weight': 165.5,
            'oxygen_saturation': 98,
            'blood_sugar': 110,
            'notes': 'All vitals within normal range',
            'logged_by': user
        }
    )
    if created:
        print(f"Created demo vitals for {elder.full_name}")
    
    # Create demo emergency contact
    contact, created = EmergencyContact.objects.get_or_create(
        elder=elder,
        name='Jane Doe',
        defaults={
            'relation': 'CHILD',
            'phone': '+1234567891',
            'email': 'jane.doe@example.com',
            'is_primary': True,
            'notes': 'Daughter - primary contact'
        }
    )
    if created:
        print(f"Created demo emergency contact: {contact.name}")
    
    print("Demo data creation completed!")
    print(f"Login with username: {user.username}, password: demo123")

if __name__ == '__main__':
    create_demo_data()

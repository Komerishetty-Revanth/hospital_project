from django.db import models
from django.contrib.auth.models import User

# Hospital model
class Hospital(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    specialization = models.CharField(max_length=200)
    contact_number = models.CharField(max_length=15)

    def __str__(self):
        return self.name

# Receiver model
class Receiver(models.Model):
    BLOOD_GROUPS = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUPS)
    contact_number = models.CharField(max_length=15)

    def __str__(self):
        return self.name

# Blood sample model
class BloodSample(models.Model):
    BLOOD_TYPES = Receiver.BLOOD_GROUPS
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPES)
    units_available = models.PositiveIntegerField()
    date_added = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.blood_type} - {self.hospital.name}- {self.units_available}- {self.location}"
# hospitalapp/models.py
from django.db import models
from django.contrib.auth.models import User

class RequestSample(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    requester_name = models.CharField(max_length=100)
    contact_info = models.CharField(max_length=255)  # Keep only one contact_info

    blood_sample = models.ForeignKey('BloodSample', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    requested_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.receiver.username} - {self.blood_sample.blood_type} - {self.status}"

class Campaign(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    location = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.name} ({self.location} - {self.start_date})"



class DonorRegistration(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    blood_group = models.CharField(max_length=5)

    def __str__(self):
        return f"{self.name} - {self.campaign.location}"
    
class BloodRequest(models.Model):
    receiver = models.ForeignKey(User, on_delete=models.CASCADE)
    blood_sample = models.ForeignKey('BloodSample', on_delete=models.CASCADE)
    request_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')],
        default='Pending'
    )

    def __str__(self):
        return f"{self.receiver.username} requested {self.blood_sample.blood_type}"
    
    
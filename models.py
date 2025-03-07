from django.db import models
from django.contrib.auth.models import User
import os
import uuid


def patient_image_path(instance, filename):
    # Génère un chemin sécurisé pour les images
    return os.path.join(f"patients/{instance.patient.id}/images", f"{uuid.uuid4()}_{filename}")


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Associer un utilisateur à un patient
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(
        max_length=10,
        choices=[('M', 'Male'), ('F', 'Female')],
        verbose_name="Gender"
    )
    contact_info = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.age} ans)"


class TumorAnalysis(models.Model):
    RESULT_CHOICES = [
        ('tumor_detected', 'Tumor Detected'),
        ('no_tumor', 'No Tumor'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='analyses')
    image = models.ImageField(upload_to=patient_image_path, verbose_name="Image")
    result = models.CharField(max_length=20, choices=RESULT_CHOICES, verbose_name="Result")
    confidence_score = models.FloatField(null=True, blank=True)
    comments = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_tumor_detected(self):
        """Retourne True si une tumeur est détectée."""
        return self.result == 'tumor_detected'

    def __str__(self):
        return f"Analysis for {self.patient.name} - {self.get_result_display()}"

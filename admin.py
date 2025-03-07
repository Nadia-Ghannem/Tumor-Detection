from django.contrib import admin
from .models import Patient, TumorAnalysis
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Patient


@receiver(post_save, sender=User)
def create_patient(sender, instance, created, **kwargs):
    if created:
        Patient.objects.create(user=instance, name=instance.username)


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("name", "age", "created_at")  # Colonnes affichées dans la liste
    search_fields = ("name",)  # Barre de recherche sur le champ 'name'
    list_filter = ("age",)  # Ajoute des filtres sur la colonne 'age'


@admin.register(TumorAnalysis)
class TumorAnalysisAdmin(admin.ModelAdmin):
    list_display = (
        "patient",
        "result",
        "created_at",
    )  # Colonnes affichées dans la liste
    list_filter = ("result",)  # Ajoute des filtres sur la colonne 'result'

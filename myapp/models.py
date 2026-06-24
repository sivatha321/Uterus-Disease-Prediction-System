from django.db import models


class Symptom(models.Model):

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Patient(models.Model):

    BMI_CHOICES = [
        ('Underweight', 'Underweight'),
        ('Normal', 'Normal'),
        ('Overweight', 'Overweight'),
        ('Obese', 'Obese'),
    ]

    patient_name = models.CharField(max_length=100)

    age = models.IntegerField()

    bmi_category = models.CharField(
        max_length=20,
        choices=BMI_CHOICES
    )

    symptoms = models.ManyToManyField(
        Symptom,
        blank=True
    )

    image = models.ImageField(
        upload_to='patients/',
        null=True,
        blank=True
    )

    gradcam_image = models.ImageField(
        upload_to='gradcam/',
        blank=True,
        null=True
    )

    disease = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    rf_disease = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    ai_report = models.TextField(
        blank=True,
        null=True
    )
    confidence_score = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.patient_name
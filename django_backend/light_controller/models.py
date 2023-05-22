from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

def rgb_field():
    return models.PositiveIntegerField(
        validators=[MinValueValidator(0),MaxValueValidator(255)]
    )

class ColorChange(models.Model):
    time = models.TimeField() 
    red = rgb_field()
    green = rgb_field()
    blue = rgb_field()
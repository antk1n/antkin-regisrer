from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator

# Create your models here.

# osauhing table - osauhingu pohiandmed asuvad 'Isikud' tabelis, teised andmed siin.
# 'isik' -> isikud.id, isikud.isosauhing = true
class Osauhing(models.Model):
    id = models.BigAutoField(primary_key=True)
    isik = models.ForeignKey('Isikud', on_delete=models.CASCADE)
    asutamisekp = models.DateField()
    kogukapital = models.IntegerField()

    # sattistame nimed et kuvada adminpaneelis 
    class Meta:
        verbose_name = 'Osauhing'
        verbose_name_plural = 'Osauhing'

# isikud - põhitabel, kuhu salvestame kõik isikute pohiandmed andmed
class Isikud(models.Model):
    
    CHOICES = [
    ("F", "Füüsiline isik"),
    ("J", "Juriidiline isik"),
    ]

    id = models.BigAutoField(primary_key=True)
    isikutyyp = models.CharField(max_length=1, choices=CHOICES)
    isosauhing = models.BooleanField()
    nimi = models.CharField(validators=[MinLengthValidator(3)], max_length=100)
    perenimi = models.CharField(validators=[MinLengthValidator(3)],max_length=100, default=None, blank=True, null=True)
    kood = models.CharField(unique=True, max_length=20)

    
    def clean(self):
        if self.isikutyyp != 'F' and self.isikutyyp != 'J':
            raise ValidationError('Value peab olema kas F voi J')
        
    def __str__(self):
        return '%s %s (%s)' % (self.nimi,self.perenimi, self.kood)
    
    # sattistame nimed et kuvada adminpaneelis 
    class Meta:
        verbose_name = 'Isikud'
        verbose_name_plural = 'Isikud'


# osauhing_isikud - asutaja pohiandmed andmed asuvad 'Isikud' tabelis, teised andmed siin. 'osauhing' - seos osauhingu andmetega
# 'osauhing' -> Osauhing.id
# 'isik' -> isikud.id
class Osauhing_Isikud(models.Model):
    id = models.BigAutoField(primary_key=True)
    osauhing = models.ForeignKey('Osauhing', on_delete=models.CASCADE)
    isik = models.ForeignKey('Isikud', on_delete=models.CASCADE)
    osauhinguOsa = models.IntegerField()
    isasutaja = models.BooleanField()

    # sattistame nimed et kuvada adminpaneelis 
    class Meta:
        verbose_name = 'Osauhing_Isikud'
        verbose_name_plural = 'Osauhing_Isikud'
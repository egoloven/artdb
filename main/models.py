from django.db import models

class Sex(models.Model):
    name = models.CharField(
        'sex',
        max_length=20,
        unique=True
    )

    def __str__(self):
        return self.name

class Type(models.Model):
    name = models.CharField(
        'type',
        max_length=20,
        unique=True
    )
    description = models.CharField(
        'description',
        max_length=50,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name

class PeriodsAndMovements(models.Model):
    name = models.CharField(
        'period or movement',
        max_length=20,
        unique=True
    )
    start = models.DateField(blank=True, null=True)
    end   = models.DateField(blank=True, null=True)
    description = models.CharField(
        'description',
        max_length=50,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name

class Artist(models.Model):
    full_name = models.CharField(
        'full name',
        max_length=40,
    )
    birth_date = models.DateField(blank=True, null=True)
    death_date = models.DateField(blank=True, null=True)
    sex = models.ForeignKey(
        Sex,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.full_name

class Artwork(models.Model):
    name = models.CharField(
        'name',
        max_length=30
    )
    creation_date = models.DateField(blank=True, null=True)
    description = models.CharField(
        'description',
        max_length=60,
        blank=True,
        null=True
    )
    author = models.ManyToManyField(
        Artist
    )
    arttype = models.ForeignKey(
        Type,
        on_delete=models.CASCADE
    )
    pm = models.ManyToManyField(
        PeriodsAndMovements
    )
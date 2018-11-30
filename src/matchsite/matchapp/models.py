from django.contrib.auth.models import User
from django.db import models

# The Hobby models provides an intermediate model for
# the 'hobbies' ManyToMany relationship between Members
# Pre-defined hobbies to be entered into the database


class Hobby(models.Model):
    # Given hobby [LIST]
    # Tennis, basketball, running, gym etc
    hobby = models.CharField(max_length=4096)

    def __str__(self):
        return self.hobby

# Django's User model allows for Members to inherit
# username and password


class Member(User):
    hobbies = models.ManyToManyField(
        blank=True,
        to=Hobby,
        symmetrical=False,
        related_name='related_to'
    )

    # one property that counts hobbies for member
    @property
    def hobbies_count(self):
        return self.hobbies.count()

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(
        to=Member,
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to='profile_images',
                              default='default.jpg')
    email = models.EmailField()
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    dob = models.DateField(max_length=8, null=True)

    def __str__(self):
        return self.user.username

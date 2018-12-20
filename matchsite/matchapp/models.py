from django.contrib.auth.models import User
from django.db import models
from datetime import datetime
from django.core.validators import RegexValidator

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
    # ManytoMany relationship, members can select many
    # hobbies
    hobbies = models.ManyToManyField(
        blank=True,
        to=Hobby,
        symmetrical=False,
        related_name='related_to'
    )

    # Users are able to request numbers from other users
    # which they will then become friends
    friends = models.ManyToManyField(
        to='self',
        blank=True,
        related_name="related_nums"
    )

    # Users are able to like each other
    like = models.ManyToManyField(
        to='self',
        blank=True,
        symmetrical=False,
        through='Like',
        related_name='likes'
    )

    # one property that counts hobbies for member
    @property
    def hobbies_count(self):
        return self.hobbies.count()

    def __str__(self):
        return self.username


class Profile(models.Model):
    # One profile for one user
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
    phone_regex = RegexValidator(
        regex=r'^(?:0|\+?44)(?:\d\s?){9,11}$', message="Phone number must be entered in the format: '+999999999'. only 11 digits allowed.")
    number = models.CharField(
        validators=[phone_regex], max_length=11, blank=True)  # validators should be a list

    # Convert the DOB into an age number
    @property
    def age(self):
        if self.dob is not None:
            return int((datetime.now().year - self.dob.year))
        else:
            return "DOB not specified"

    def __str__(self):
        return self.user.username

# Users are able to like each other


class Like(models.Model):
    to_user = models.ForeignKey(
        to=Member,
        related_name='like_sent',
        on_delete=models.CASCADE
    )

    from_user = models.ForeignKey(
        to=Member,
        related_name='like_received',
        on_delete=models.CASCADE
    )
    liked = models.BooleanField(default=False)

    def __str__(self):
        return 'From ' + self.from_user.username + ' likes ' + self.to_user.username

# Users can request numbers from each other


class Number(models.Model):
    to_user = models.ForeignKey(
        to=Member,
        related_name='sent',
        on_delete=models.CASCADE
    )

    from_user = models.ForeignKey(
        to=Member,
        related_name='received',
        on_delete=models.CASCADE
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'From ' + self.from_user.username + ' to ' + self.to_user.username
from echoApp.validators import message_url_validator
from django.db import models


GENDERS = (
    ("M", "Man"),
    ("W", "Women")
)


CURRENCY = (
    ("USD", "USD"),
    ("BYN", "BYN"),
    ("RUB", "RUB"),
)
EMPLOYMENT = (
    ("-", "-"),
    ("Full employment", "Full employment"),
    ("Part-time employment", "Part-time employment"),
    ("One-time job", "One-time job"),
    ("Internship", "Internship"),
)
EDUCATION = (
    ("-", "-"),
    ("Higher", "Higher"),
    ("Vocational", "Vocational"),
    ("Specialized secondary", "Specialized secondary"),
)

EXPERIENCE = (
    ("-", "-"),
    ("Without experience", "Without experience"),
    ("Less than 1 years", "Less than 1 years"),
    ("From 1 yo 3 years", "From 1 yo 3 years"),
    ("More that 3 years", "More that 3 years"),
)

"""#################################### general constants ####################################"""


class Country(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Region(models.Model):
    title = models.CharField(max_length=255)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class District(models.Model):
    title = models.CharField(max_length=255)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Messenger(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField(max_length=255, validators=[message_url_validator])
    is_publish = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Education(models.Model):
    title = models.CharField(max_length=255)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


"""#################################### echo ####################################"""


class User(models.Model):
    resume = models.FileField(upload_to='resume')
    nams = models.CharField(max_length=150, blank=True)
    surname = models.CharField(max_length=150, blank=True)
    email = models.CharField(unique=True, max_length=255)
    username = models.CharField(max_length=230, blank=True, unique=True, null=True)
    password = models.CharField(max_length=100)
    phone = models.CharField(max_length=30, blank=True, default='')
    gender = models.CharField(max_length=255, null=True, default=None)
    profession = models.CharField(max_length=255, null=True, default=None)
    experience = models.CharField(max_length=255, null=True, default=None)
    img = models.ImageField(upload_to="user_photo", blank=True, default='../static/img/none-logo.png')
    birthday = models.CharField(max_length=10, blank=True, default='')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True)
    city = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True)
    cover_letter = models.TextField()
    institution_name = models.TextField()
    graduation_year = models.IntegerField(null=True, blank=True)
    specialization = models.CharField(max_length=255, null=True, blank=True)
    skills = models.CharField(max_length=255, null=True, blank=True)
    contacts = models.CharField(max_length=255, null=True, blank=True)

    publish_phone = models.BooleanField(default=False)
    public_status = models.BooleanField(default=False)

    def __str__(self):
        return self.email


class Company(models.Model):
    title = models.CharField(max_length=255)
    logo = models.ImageField(upload_to="company", blank=True)
    description = models.TextField()

    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    country = models.ForeignKey(Country, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.title


class Vacancy(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    salary = models.PositiveIntegerField()
    currency = models.CharField(max_length=255, choices=CURRENCY,  null=True, default=None)
    date_of_create = models.DateField(auto_now_add=True)
    responses = models.PositiveIntegerField(default=0)

    country = models.ForeignKey(Country, on_delete=models.CASCADE, blank=True, null=True) #
    region = models.ForeignKey(Region, on_delete=models.CASCADE, blank=True, null=True) #
    district = models.ForeignKey(District, on_delete=models.CASCADE, blank=True, null=True) #
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True)

    experience = models.CharField(max_length=255, choices=EXPERIENCE,  null=True, default=None)
    education = models.CharField(max_length=255, choices=EDUCATION,  null=True, default=None)
    employment = models.CharField(max_length=255, choices=EMPLOYMENT,  null=True, default=None)

    is_publish = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    photo = models.ImageField(upload_to='user_photos/', default='user_photos/none-logo.png')
    user = models.CharField(default="User deleted", max_length=20)
    text = models.TextField(max_length=500)

    def __str__(self):
        return self.user


class Summary(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date_of_create = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    experience = models.CharField(max_length=255,  null=True, default=None)
    employment = models.CharField(max_length=255,  null=True, default=None)
    skills = models.TextField(null=True, default=None)

    is_publish = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Response(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)
    message = models.TextField()

"""#################################### echo.job ####################################"""



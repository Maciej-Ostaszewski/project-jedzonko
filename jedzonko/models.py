import re
from django.db import models
from enum import IntEnum
from django.template.defaultfilters import slugify


# from django.fields import EnumChoiceField


days = (
    ('pon',"Poniedziałek"),
    ('wt', "Wtorek"),
    ('śr', "Środa"),
    ('czw', "Czwartek"),
    ('pt', "Piątek"),
    ('sob', "Sobota"),
    ('nd', "Niedziela")
)
# class Days(IntEnum):
#     Poniedziałek = 1
#     Wtorek = 2
#     Środa = 3
#     Czwartek = 4
#     Piątek = 5
#     Sobota = 6
#     Niedziela = 7
#
#     @classmethod
#     def choices(cls):
#         return [(key.value, key.name) for key in cls]


# Create your models here.
class Recipe(models.Model):
    name = models.CharField(max_length=255)
    ingredients = models.TextField()
    description = models.TextField()
    preparation = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    preparation_time = models.IntegerField()
    votes = models.IntegerField(default=0)


class DayName(models.Model):
    day_name = models.CharField(max_length=16, choices=days)
    order = models.IntegerField(unique=True)


class Plan(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created = models.DateField(auto_now_add=True)
    recipes = models.ManyToManyField(Recipe, through='RecipePlan')
    day_names = models.ManyToManyField(DayName, through='RecipePlan')


class RecipePlan(models.Model):
    meal_name = models.CharField(max_length=255)
    order = models.IntegerField()
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    day_name = models.ForeignKey(DayName, on_delete=models.CASCADE)


class Page(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Page, self).save(*args, **kwargs)

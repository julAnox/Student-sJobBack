from django.contrib import admin

from echoApp.models import *


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("title",)


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ("title", "country")


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ("title", "region")


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ("title", "country")


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "username",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "photo")


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("title", "creator")


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ("title", "salary")


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ("user", "vacancy")\

@admin.register(Summary)
class SummaryAdmin(admin.ModelAdmin):
    list_display = ("title", "user")


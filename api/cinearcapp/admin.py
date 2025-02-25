from django.contrib import admin
from .models import Movie, Session, Room, Basket
from django_celery_beat.models import PeriodicTask, CrontabSchedule, IntervalSchedule

# Register your models here.
admin.site.register(Movie)
admin.site.register(Session)
admin.site.register(Room)
admin.site.register(Basket)
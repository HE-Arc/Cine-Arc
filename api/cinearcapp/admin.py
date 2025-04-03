from django.contrib import admin
from .models import Movie, Session, Room, Basket

#Register your models here.
admin.site.register(Movie)
admin.site.register(Session)
admin.site.register(Room)
admin.site.register(Basket)



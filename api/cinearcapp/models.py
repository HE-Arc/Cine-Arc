from django.db import models
from django.contrib.auth.models import User

# Model for a movie
class Movie(models.Model):
    title = models.CharField(max_length=100, null=False)
    synopsis = models.TextField(max_length=500, null=True, blank=True)
    duration = models.IntegerField(null=False)
    type = models.CharField(max_length=50, null=False)
    release_date = models.DateField(null=False)
    picture_url = models.URLField(max_length=255, null=True, blank=True)
    rating = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.title

# Model for a session
class Session(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="sessions")
    room = models.CharField(max_length=50, null=False)
    date_hour = models.DateTimeField(null=False)

    def __str__(self):
        return f"{self.movie.title} - {self.room} ({self.date_hour})"

# Model for a reservation
class Reservation(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('paid', 'Payé'),
        ('not paid', 'Non payé'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reservations")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    date = models.DateField(null=False)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='not paid')

    def __str__(self):
        return f"Réservation {self.id} - {self.user.email} - {self.payment_status}"

# Model for a basket
class Basket(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name="baskets")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="baskets")
    quantity = models.IntegerField(null=False)

    class Meta:
        unique_together = ('session', 'user')  # Un utilisateur ne peut avoir qu'une seule entrée par session

    def __str__(self):
        return f"{self.user.email} - {self.session.movie.title} ({self.quantity} places)"
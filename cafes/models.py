from django.db import models
from django.db.models import Avg
from users.models import CafeOwner

class CafeShop(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(CafeOwner, on_delete=models.CASCADE)
    introduction = models.TextField(null=True, blank=True)
    address = models.CharField(max_length=255)
    contact = models.CharField(max_length=20, null=True, blank=True)
    price_range = models.CharField(
        max_length=10,
        choices=[('£0-10', '£0-10'), ('£10-20', '£10-20'), ('£20-30', '£20-30'),
                 ('£30-40', '£30-40'), ('£40-50', '£40-50'), ('over £50', 'over £50')],
        default='£0-10'
    )
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)

    def update_average_rating(self):
        from reviews.models import Review
        reviews = Review.objects.filter(cafe=self)

        if reviews.exists():
            self.average_rating = reviews.aggregate(Avg("rating"))["rating__avg"]
        else:
            self.average_rating = 0

        self.save()
    # Here the URLField is used to store the Cloudinary image URLs
    img_url = models.URLField(max_length=500, null=True, blank=True)

    class Meta:
        db_table = 'Cafe_Shop'

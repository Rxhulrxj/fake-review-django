from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Products(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=50)
    product_description = models.TextField()
    product_price = models.IntegerField()
    product_image = models.FileField(upload_to="product_images")
    class Meta:
        verbose_name_plural = "Products"
    def __str__(self):
        return self.product_name

status = [('published','published'),('under_review','under_review'),('rejected','rejected')]
class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    review = models.TextField()
    review_by = product_id = models.ForeignKey(User, on_delete=models.CASCADE)
    review_date = models.DateField()
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE)
    text_percentage = models.IntegerField()
    review_status = models.CharField(max_length=50,choices=status)
    review_pred= models.IntegerField()
    class Meta:
        verbose_name_plural = "Reviews"

    def __str__(self):
        return str(self.review_id)
class Product_Purchase(models.Model):
    purchase_id = models.AutoField(primary_key = True)
    purchased_by = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = "Product Purchase"

    def __str__(self):
        return str(self.purchase_id)
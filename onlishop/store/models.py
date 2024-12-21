from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CASCADE



class UserProfile(AbstractUser):
    age=models.PositiveSmallIntegerField(default=0, null=True,blank=True)
    date_registered=models.DateField(auto_now_add=True, null=True, blank=True)
    phone_number=models.PositiveSmallIntegerField(null=True, blank=True)
    STATUS_CHOICES=(
        ('gold', 'gold'),
        ('silver', 'silver'),
        ('bronze', 'bronze'),
        ('simple', 'simple'),
    )
    status=models.CharField(max_length=10, choices=STATUS_CHOICES, default='simple')

    def __str__(self):
        return f'{self.first_name}-{self.first_name}-{self.status}'

class Category(models.Model):
    category_name=models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.category_name


class Product(models.Model):
    product_name=models.CharField(max_length=32)
    category=models.ForeignKey(Category, related_name='products', on_delete=CASCADE)
    price=models.PositiveIntegerField()
    description=models.TextField()
    data=models.DateField(auto_now_add=True)
    active=models.BooleanField(verbose_name='в наличии', default=True)
    product_video=models.FileField(upload_to='vid/', verbose_name='video', null=True,blank=True)
    owner=models.ForeignKey(UserProfile, on_delete=CASCADE, null=True, blank=True)


    def __str__(self):
        return self.product_name


class ProductPhotos(models.Model):
    product=models.ForeignKey(Product, related_name='product', on_delete=models.CASCADE)
    image=models.ImageField(upload_to='product_img/')


class Rating(models.Model):
    product=models.ForeignKey(Product, related_name='ratings', on_delete=CASCADE)
    user=models.ForeignKey(UserProfile, on_delete=CASCADE)
    starts=models.IntegerField(choices=[(i, str(i)) for i in range(0, 6)], verbose_name="Рейтинг")

    def __str__(self):
        return f'{self.product}-{self.user}-{self.starts}'


class Review(models.Model):
    author=models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    text=models.TextField()
    product=models.ForeignKey(Product,related_name='review', on_delete=models.CASCADE)
    parent_review=models.ForeignKey('self', related_name='replies', null=True, blank=True , on_delete=models.CASCADE)
    created_date=models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.author}-{self.product}'


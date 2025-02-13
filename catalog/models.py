from django.db import models
from django_countries.fields import CountryField
from django.shortcuts import reverse
from django.contrib.auth.models import User
import phonenumbers
import os
import uuid
from django.core.exceptions import ValidationError

PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'Paypal'),
    ('C','creditcard')
)


class Item(models.Model):
    title = models.CharField(max_length=150)
    price = models.IntegerField()
    color = models.CharField(max_length=100,blank=True, null=True)    
    discount_price = models.IntegerField(blank=True, null=True)
    storage = models.IntegerField(blank=True, null=True)
    slug = models.SlugField()
    description = models.TextField()
    inform = models.TextField(blank=True, null=True)
    rating = models.ForeignKey("Rating", on_delete=models.CASCADE, blank=True, null=True)   
    category = models.ForeignKey(
        "Category", on_delete=models.SET_NULL, blank=True, null=True)
    image = models.ImageField( upload_to='product_images')

    image2 = models.ImageField(upload_to='product_images',blank=True, null=True)

    image3 = models.ImageField(upload_to='product_images',blank=True, null=True)

    image4 = models.ImageField(upload_to='product_images',blank=True, null=True)

    image5 = models.ImageField(upload_to='product_images',blank=True, null=True)

    image6 = models.ImageField(upload_to='product_images',blank=True, null=True)

    is_active = models.BooleanField(default=False)  # To indicate the active image

    on_sale = models.BooleanField(default=False)  # New field to indicate if the item is on sale

    def __str__(self):
        return self.title

    def get_add_to_cart_url(self):
        return reverse('add_to_cart', kwargs={'pk': self.pk})

    def get_remove_from_cart_url(self):
        return reverse('remove_from_cart', kwargs={'pk': self.pk})

    def get_remove_single_from_cart_url(self):
        return reverse('remove_single_from_cart', kwargs={'pk': self.pk})

def get_country_code_choices():
    country_codes = []
    for region in phonenumbers.SUPPORTED_REGIONS:  # Get all supported country codes
        country_code = phonenumbers.country_code_for_region(region)
        country_codes.append((f'+{country_code}', f'{region} (+{country_code})'))
    return sorted(set(country_codes))  # Remove duplicates and sort

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer')
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    profileimg = models.ImageField(upload_to='profile_image', blank=True, null=True)
    country_code = models.CharField(max_length=5, choices=get_country_code_choices(), default='+44  ')  # Auto-generate choices
    mobile = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username

    def formatted_mobile(self):
        if not self.mobile.startswith("+"):
            return f"{self.country_code}{self.mobile}"
        return self.mobile


class customerrates(models.Model):
    item = models.ForeignKey(Item, related_name="customerrate", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customerrate = models.TextField(blank=True,null=True)
    customerratevideo = models.FileField(upload_to='customerrate/videos/', blank=True, null=True)
    rating = models.ForeignKey("Rating", on_delete=models.CASCADE, blank=True, null=True)
    customerrateimage1= models.ImageField(upload_to='customerrate',blank=True, null=True)
    customerrateimage2= models.ImageField(upload_to='customerrate',blank=True, null=True)
    customerrateimage3= models.ImageField(upload_to='customerrate',blank=True, null=True)

    # def save(self, *args, **kwargs):
    #     # Check if a video is uploaded
    #     if self.customerratevideo:
    #         original_name = self.customerratevideo.name
    #         extension = os.path.splitext(original_name)[1]  # Get file extension (e.g., .mp4, .avi)
            
    #         # Generate a shorter filename with UUID
    #         new_filename = f"{uuid.uuid4().hex[:10]}{extension}"
            
    #         # Rename the file
    #         self.customerratevideo.name = new_filename
        
    #     super().save(*args, **kwargs)
    
    # def __str__(self):
    #     def __str__(self):
    # return f"Review by {self.user.username} for {self.item.id}"

    
class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_amount_saved(self):
        return self.get_item_price() - self.get_item_final_price()

    def get_item_discount_price(self):
        return self.item.discount_price * self.quantity

    def get_item_price(self):
        return self.item.price * self.quantity

    def get_item_final_price(self):
        if self.item.discount_price:
            return self.get_item_discount_price()
        else:
            return self.get_item_price()


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    ordered = models.BooleanField(default=False)
    ref_code = models.CharField(max_length=20)
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    address = models.ForeignKey(
        "Address", on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(auto_now=True)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    def __str__(self):
        return f"Order by {self.user.username if self.user else 'Unknown User'}"
    
    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_item_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=255)
    apartment_address = models.CharField(max_length=255, blank=True, null=True)
    country = CountryField(blank_label='(Select country)')
    city = models.CharField(max_length=100,blank=True, null=True)
    zip = models.CharField(max_length=20, blank=True, null=True)  # Allow blank and NULL value
    default = models.BooleanField(default=False)      
    # class Address(models.Model):
    #     user = models.ForeignKey(User, on_delete=models.CASCADE)
    #     street_address = models.CharField(max_length=250)
    #     apartment_address = models.CharField(max_length=300, blank=True, null=True)
    #     country = CountryField(blank_label='(Select country)')
    #     city = models.CharField(max_length=50,blank=True, null=True)
    #     zip = models.CharField(max_length=5)
    #     default = models.BooleanField(default=False)
    #     save_info = models.BooleanField(default=False)
    #     use_default = models.BooleanField()
    #     payment_option = models.CharField(choices=PAYMENT_CHOICES, max_length=1)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Addresses'


class Payment(models.Model):
    charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.IntegerField()
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment of {self.amount} by {self.user.username if self.user else 'Unknown User'}"



class Coupon(models.Model):
    code = models.CharField(max_length=20)
    amount = models.IntegerField()

    def __str__(self):
        return self.code


class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.order.user.username


class Category(models.Model):
    name = models.CharField(max_length=200)
    thumbnail = models.ImageField(
        default='default.jpg', upload_to='static/cat_imgs')

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Rating(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True)
    value = models.IntegerField(blank=True, null=True)
    message = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return self.message


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}'s wishlist"

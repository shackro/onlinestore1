from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from .models import Customer
import phonenumbers


PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'Paypal'),
    ('M', 'M-pesa'),
    ('C','creditcard')
)

class CreditCardForm(forms.Form):
    card_number = forms.CharField(max_length=16, label="Card Number")
    expiry_date = forms.CharField(max_length=5, label="Expiry Date (MM/YY)")
    cvv = forms.CharField(max_length=3, label="CVV")
    cardholder_name = forms.CharField(max_length=100, label="Cardholder Name")

class AddressForm(forms.Form):
    street_address = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Street Address'}),
        label='Street Address'
    )
    apartment_address = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apartment, suite, etc. (optional)'}),
        label='Apartment Address'
    )
    country = CountryField(blank_label='Select country').formfield(
        widget=CountrySelectWidget(attrs={
            'class': "custom-select d-block w-100",
        }),
        label='Country'
    )
    city = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
        label='City'
    )
    zip_code = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ZIP/Postal Code'}),
        label='ZIP/Postal Code'
    )




def get_country_code_choices():
    country_codes = []
    for region in phonenumbers.SUPPORTED_REGIONS:
        country_code = phonenumbers.country_code_for_region(region)
        country_codes.append((f'+{country_code}', f'{region} (+{country_code})'))
    return sorted(set(country_codes))  # Remove duplicates and sort

class CustomerProfileForm(forms.ModelForm):
    profileimg = forms.ImageField(required=False)
    first_name = forms.CharField(max_length=50, required=False)
    last_name = forms.CharField(max_length=50, required=False)
    mobile = forms.CharField(max_length=15, required=False)
    country_code = forms.ChoiceField(choices=get_country_code_choices(), required=False)  # Dropdown for country codes

    class Meta:
        model = Customer  
        fields = ['profileimg', 'first_name', 'last_name', 'mobile', 'country_code']


    
    

class CouponForm(forms.Form):
    code = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'class': "form-control",
        'placeholder': "Promo code",
        'aria-label': "Recipient's username",
        'aria-describedby': "basic-addon2"
    }))


class RefundForm(forms.Form):
    code = forms.CharField(max_length=20)
    email = forms.EmailField()
    reason = forms.CharField(widget=forms.Textarea())

from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.db import IntegrityError 
from django.utils import timezone
from paypal.standard.forms import PayPalPaymentsForm
import uuid 
from django.views.generic import ListView, DetailView, View
from .models import (
    Item, OrderItem, Order, Address, Payment, Coupon,
    Refund, Category, Wishlist, Rating,Customer,customerrates
)
from .forms import AddressForm, CouponForm, RefundForm,CustomerProfileForm,CreditCardForm
import json
import stripe
import string
import random
import smtplib
import imghdr
from email.message import EmailMessage
import uuid
import logging
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from square.client import Client




def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))


# stripe.api_key = settings.STRIPE_SECRET_KEY


def SignupPage(request):
    error_message = None  # Initialize the error message variable

    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        # Check if passwords match
        if pass1 != pass2:
            error_message = "Your password and confirm password are not the same!"
        else:
            try:
                # Attempt to create a new user
                my_user = User.objects.create_user(username=uname, email=email, password=pass1)
                my_user.save()
                return redirect('login')  # Redirect to login page after successful signup
            except IntegrityError:
                # Handle the case where the username already exists
                error_message = "Username already exists. Please choose a different one."

    # Render the signup page with any error messages
    return render(request, 'signup.html', {'error_message': error_message})

def LoginPage(request):
    error_message = None
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            error_message="Username or Password is incorrect!!!"

    return render (request,'login.html',{'error_message': error_message})

class Refubrished(View):
    def get(self, *args, **kwargs):
        Refubrished = Item.objects.filter(category__name="Refurbished").order_by('?')
        context = {
            'Refubrished': Refubrished,
        }
        return render(self.request, 'Refubrished.html', context)

class Smartwatch(View):
    def get(self, *args, **kwargs):
        Smartwatch = Item.objects.filter(category__name="Smartwatch").order_by('?')
        context = {
            'Smartwatch': Smartwatch,
        }
        return render(self.request, 'smartwatch.html', context)

class onsale(View):
    def get(self, *args, **kwargs):
        context = {
            'items':  Item.objects.all().order_by('?'),
        }
        return render(self.request, 'onsale.html', context)

class Case(View):
    def get(self, *args, **kwargs):
        Case = Item.objects.filter(category__name="Case").order_by('?')
        context = {
            'Case': Case,
        }
        return render(self.request, 'Cases.html', context)
    
#fix search ..............    
def search(request):
    query = request.GET.get('search', '')  # Use get() with a default value
    item = Item.objects.filter(title__icontains=query)
    return render(request, 'search.html', {'item': item})
  

class ProductDetailView(DetailView):
    model = Item
    template_name = 'product.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item = self.get_object()  # Get the current product being viewed
        context.update({
            'items': Item.objects.all().order_by('id'),
            'reviews': customerrates.objects.filter(item=item).order_by('-id'),  # Use item instead of product
        })
        return context

    def post(self, *args, **kwargs):
        print(self.request.POST)
        return redirect('cart')



class  IndexView(View):
    def get(self, *args, **kwargs):

        Refubrished = Item.objects.filter(category__name="Refurbished")
        Smartwatch = Item.objects.filter(category__name="Smartwatch")
        Case = Item.objects.filter(category__name="Case")
        context = {
            'Case': Case.order_by('?')[:6],
            'Smartwatch': Smartwatch.order_by('?')[:6],
            'Refubrished': Refubrished.order_by('?')[:6],
            'items':  Item.objects.order_by('?')[:6],

        }
        return render(self.request, 'index.html', context)


class HomeView(View):
    def get(self, *args, **kwargs):
        context = {
            'items':  Item.objects.all().order_by('?'),

        }
        return render(self.request, 'home.html', context)        


class Cart(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'cart.html')


class ShopBlockView(View):
    def get(self, *args, **kwargs):
        context = {
            'items': Item.objects.all()
        }
        return render(self.request, 'shop.html', context)


class ShopListView(View):
    def get(self, *args, **kwargs):
        context = {
            'items': Item.objects.all()
        }
        return render(self.request, 'shop_list.html', context)


class CheckOutView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = AddressForm()

            context = {
                'form': form,
                'order': order,
                'DISPLAY_COUPON_FORM': False
            }
            return render(self.request, 'checkout.html', context)
        except Order.DoesNotExist:
            messages.info(self.request, "You don't have an active order")
            return redirect('order_summary')

    def post(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = AddressForm(self.request.POST or None)

            if form.is_valid():
                # Create and save the new address
                address = Address(
                    user=self.request.user,
                    street_address=form.cleaned_data.get('street_address'),
                    apartment_address=form.cleaned_data.get('apartment_address'),
                    country=form.cleaned_data.get('country'),
                    city=form.cleaned_data.get('city'),
                    zip=form.cleaned_data.get('zip_code'),
                )
                address.save()

                # Assign the address to the order
                order.address = address
                order.save()

                return redirect('payment')  # Redirect to payment page

            else:
                messages.error(self.request, "Please correct the errors below.")
                context = {
                    'form': form,
                    'order': order,
                    'DISPLAY_COUPON_FORM': False
                }
                return render(self.request, 'checkout.html', context)

        except Order.DoesNotExist:
            messages.info(self.request, "You don't have an active order!")
            return redirect('order_summary')
        except Exception as e:
            messages.error(self.request, f"An error occurred: {str(e)}")
            return redirect('checkout')

#paypal 2
# @csrf_exempt
# def paypal_ipn(sender, **kwargs):
#     ipn_obj = sender
#     if ipn_obj.payment_status == ST_PP_COMPLETED:
#         # Validate payment amount
#         try:
#             order = Order.objects.get(ref_code=ipn_obj.invoice, ordered=False)
#             if ipn_obj.mc_gross == order.get_total() and ipn_obj.mc_currency == 'USD':
#                 order.ordered = True
#                 order.ordered_date = timezone.now()
#                 order.save()
#                 logger.info(f"Payment completed for order {order.ref_code}")
#         except Order.DoesNotExist:
#             logger.error(f"Order not found for IPN: {ipn_obj.invoice}")
#     else:
#         logger.warning(f"Unhandled PayPal IPN status: {ipn_obj.payment_status}")

# valid_ipn_received.connect(paypal_ipn)





logger = logging.getLogger(__name__)

class paypal(View):
    def get(self, request, *args, **kwargs):
        try:
            if not request.user.is_authenticated:
                return redirect('login')

            order = Order.objects.get(user=request.user, ordered=False)
            logger.info(f"Order found: {order}")

            # Generate reference code if not exists
            if not order.ref_code:
                order.ref_code = uuid.uuid4()
                order.save()

            # PayPal Dictionary for Classic Payments
            paypal_dict = {
                "business": settings.PAYPAL_RECEIVER_EMAIL,
                "amount": str(order.get_total()),
                "item_name": "Purchased Products",
                "invoice": str(order.ref_code),
                "currency_code": "USD",
                "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
                "return_url": request.build_absolute_uri(reverse('payment-complete')),
                "cancel_return": request.build_absolute_uri(reverse('payment-cancelled')),
            }

            form = PayPalPaymentsForm(initial=paypal_dict)

            context = {
                'order': order,
                'form': form,
                'paypal_client_id': settings.PAYPAL_CLIENT_ID,  # For Smart Buttons
                'paypal_currency': "USD",
                'paypal_test': settings.PAYPAL_TEST,
            }
            return render(request, 'paypal.html', context)

        except Order.DoesNotExist:
            logger.error("No active order found for the user.")
            return redirect('order-summary')
        except Exception as e:
            logger.error(f"Error in paypal: {str(e)}")
            return redirect('home')

class SquarePaymentView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        
        order = Order.objects.get(user=request.user, ordered=False)
        amount = int(order.get_total() * 100)  # Convert to cents

        # Initialize Square client
        client = Client(
            access_token=settings.SQUARE_ACCESS_TOKEN,
            environment=settings.SQUARE_ENVIRONMENT,
        )

        try:
            # Create a payment link
            payment_link_result = client.checkout.create_payment_link(
                body={
                    "idempotency_key": str(order.id),  # Unique key for idempotency
                    "order": {
                        "location_id": settings.SQUARE_LOCATION_ID,
                        "line_items": [
                            {
                                "name": "Order #{}".format(order.ref_code),
                                "quantity": "1",
                                "base_price_money": {
                                    "amount": amount,
                                    "currency": "USD",  # Change to your currency
                                },
                            },
                        ],
                    },
                    "checkout_options": {
                        "redirect_url": request.build_absolute_uri(reverse('payment-complete')),
                    },
                }
            )

            if payment_link_result.is_success():
                # Redirect the user to the Square payment link
                payment_link_url = payment_link_result.body['payment_link']['url']
                return redirect(payment_link_url)
            else:
                logger.error(f"Square payment link creation failed: {payment_link_result.errors}")
                return redirect('payment-failed')

        except Exception as e:
            logger.error(f"Error creating Square payment link: {str(e)}")
            return redirect('payment-failed')

class creditcard(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        if self.request.method == 'POST':
            form = CreditCardForm(self.request.POST)
            if form.is_valid():
                # Handle the submitted data here (e.g., send it to a payment gateway)
                card_number = form.cleaned_data['card_number']
                expiry_date = form.cleaned_data['expiry_date']
                cvv = form.cleaned_data['cvv']
                cardholder_name = form.cleaned_data['cardholder_name']

                # For now, just return a success message
                return HttpResponse("Credit Card Information Submitted Successfully!")
        else:
            form = CreditCardForm()      
            
            context = {
                    'order': order,
                    'DISPLAY_COUPON_FORM': False,
                    'form': form,
                }
        return render(self.request, 'creditcard.html',context)


class PaymentView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if order.address is not None:
                context = {
                    'order': order,
                    'DISPLAY_COUPON_FORM': False
                }
                return render(self.request, 'pay.html', context)
            else:
                messages.info(
                    self.request, "Please provide a shipping address")
                return redirect('checkout')
        except ObjectDoesNotExist:
            messages.info(self.request, "You don't have an active order")
            return redirect('order_summary')

    def post(self, *args, **kwargs):
        to_email = self.request.user.email
        print('customer email -->', to_email)
        order = Order.objects.get(user=self.request.user, ordered=False)
        try:
            customer = stripe.Customer.create(
                name=self.request.user,
                email=self.request.user.email,
                source=self.request.POST['stripeToken']

            )
            amount = int(order.get_total() * 100)
            charge = stripe.Charge.create(
                amount=amount,
                currency="usd",
                customer=customer,
                description="My first own test"
            )
            payment = Payment()
            payment.charge_id = charge['id']
            payment.user = self.request.user
            payment.amount = order.get_total()
            payment.save()

            order_items = order.items.all()
            order_items.update(ordered=True)
            for item in order_items:
                print(item.item.title)
                print(item.item.discount_price)
                item.save()

            order.ordered = True
            order.payment = payment
            order.ref_code = create_ref_code()
            order.save()

            msg = EmailMessage()
            msg['Subject'] = f'Your order{item.item.title}'
            msg['From'] = "ONlineTech Online <shifttry42@gmail@gmail.com>"
            msg['To'] = to_email
            msg.set_content(
                f"Testing{item.item.title} for {item.item.discount_price} to be shipped to {order.address.street_address} the new feature of buteks online {item.item.image.url}")

            msg.add_alternative(
                """
                <!DOCTYPE html>
                <html lang="en">
                    <body>
                        <h1 style="color:gray;">Helloh</h1>
                        <img src='catalog/img.jpg' alt="itemimg">
                    </body>
                </html>
                """
            , subtype='html')

            with open(f'media/{item.item.image}', 'rb') as f:
                file_data = f.read()
                file_type = imghdr.what(f.name)
                file_name = f.name

            msg.add_attachment(file_data, maintype='image',
                               subtype=file_type, filename=file_name)

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                username = ""
                password = ""
                smtp.login(username, password)

                smtp.send_message(msg)

            messages.success(
                self.request, 'Your payment was successful. Go to you profile to view the deilvery status')
            return redirect('home')

        except stripe.error.CardError as e:
            body = e.json_body
            err = body.get('error', {})
            messages.info(self.request, f"{err.get('message')}")
            return redirect('/')
        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            messages.info(self.request, "Rate limit error")
            return redirect('/')
        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            messages.info(self.request, "Invalid parameters")
            return redirect('/')
        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            messages.info(self.request, "Not authenticated")
            return redirect('/')
        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            messages.info(
                self.request, "Connection error...Please check your connection")
            return redirect('/')
        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            messages.info(
                self.request, "Something went wrong, You were not charged. Please try again")
            return redirect('/')
        except Exception as e:
            # Send an e-mail to ourselves
            print(e)
            messages.info(
                self.request, "A serious error occurred, We were notified and are handling it.")
            return redirect('/')


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'objects': order
            }
            return render(self.request, 'cart.html', context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You don't have an active order!")
            return redirect('home')


class CouponView(View):
    def post(self, *args, **kwargs):
        coupon_form = CouponForm(self.request.POST or None)
        if coupon_form.is_valid():
            try:
                code = coupon_form.cleaned_data.get('code')
                order = Order.objects.get(
                    user=self.request.user, ordered=False)
                order.coupon = Coupon.objects.get(code=code)
                order.save()
                messages.success(self.request, 'Successfully added coupon!')
                return redirect('checkout')
            except ObjectDoesNotExist:
                messages.info(self.request, "You don't have an active order!")
                return redirect('checkout')


class RefundView(View):
    def get(self, *args, **kwargs):
        form = RefundForm()
        context = {
            'form': form
        }
        return render(self.request, 'refund.html', context)

    def post(self, *args, **kwargs):
        form = RefundForm(self.request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email'),
            code = form.cleaned_data.get('code'),
            reason = form.cleaned_data.get('reason')
            try:
                code = form.cleaned_data.get('code')
                order = Order.objects.get(ref_code=code, ordered=True)
                order.refund_requested = True
                order.save()

                refund = Refund()
                refund.order = order
                refund.email = email
                refund.message = reason
                refund.save()
                messages.success(
                    self.request, "You refund request has been received and is being processed!")
                return redirect('home')
            except ObjectDoesNotExist:
                messages.info(
                    self.request, "This order does not exist! Enter the correct reference code")
                return redirect('request_refund')
        messages.warning(
            self.request, "Please enter the correct order reference code")
        return redirect('request_refund')


def payment_complete(request):
    body = json.loads(request.body)
    order = Order.objects.get(
        user=request.user, ordered=False, id=body['order_id'])

    # create the payment
    payment = Payment()
    payment.charge_id = create_ref_code()
    payment.user = request.user
    payment.amount = order.get_total()
    payment.save()

    order_items = order.items.all()
    order_items.update(ordered=True)
    for item in order_items:
        item.save()

    # assign the payment to the order
    order.ordered = True
    order.payment = payment
    order.ref_code = create_ref_code()
    order.save()
    messages.success(
        request, 'Your payment was successful. Go to you profile to view the deilvery status')
    return redirect('home')



def payment_canceled(request):
    messages.success(
        request, 'Your payment was canceled. Pleae try again ')
    return redirect('home')

class PaymentFailedView(View):
    def get(self, request, *args, **kwargs):
        # Handle failed payment
        return redirect('home')


@login_required
def profile(request):
    try:
        context = {
        'customer': request.user.customer,    
        'orders': Order.objects.filter(user=request.user).order_by('ordered_date')}
        return render(request, 'profile.html', context)
    except Customer.DoesNotExist:
        context = {
        'customer': Customer.objects.create(user=request.user),    
        'orders': Order.objects.filter(user=request.user).order_by('ordered_date')}
        return render(request, 'profile.html', context)
    
    # form = CustomerProfileForm()
    # order = Order.objects.get(user=request.user, ordered=False)
    # context = {
    #         'form' : form,
    #         'order': order
    #     }    
    # return render(request, 'profile.html',context)
    # def post(request):
    #     form = CustomerProfileForm(request.POST)
    #     if form.is_valid():
    #         user = request.Customer
    #         first_name = form.cleaned_data['first_name']
    #         last_name = form.cleaned_data['last_name']
    #         city = form.cleaned_data['city']
    #         mobile = form.cleaned_data['mobile']
    #         country = form.cleaned_data['country']
    #         zipcode = form.cleaned_data['zipcode']

    #         reg = Customer(user=user,last_name=last_name,first_name=first_name,city=city,mobile=mobile,country=country,zipcode=zipcode)
    #         reg.save()
    #         messages.success(request, "Congratulations! Profile Saved  Successfully")
    #     return render(request,'profile.html',locals())


@login_required
def editprofile(request):
    # Try to get the customer's profile
    try:
        customer = request.user.customer
    except Customer.DoesNotExist:
        # Create a new customer if it does not exist
        customer = Customer.objects.create(user=request.user)

    # Initialize the form with current customer data
    if request.method == 'POST':
        # Include request.FILES to handle file uploads
        form = CustomerProfileForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            # Save the form directly, which will update the customer instance
            form.save()  # This will save all fields including profileimg
            return redirect('profile')
    else:
        # Prepopulate the form with existing data for GET requests
        form = CustomerProfileForm(instance=customer)

    return render(request, "editprofile.html", {"form": form})
    # customer = Customer.objects.get(user =request.user )
    
    # if request.method == "POST":
    #     form = CustomerProfileForm(request.POST,instance=customer)
    #     if form.is_valid():
    #         form.save()
    #         return redirect("profile")
    # else:
    #     form =CustomerProfileForm(instance = customer)
        
    # return render(request,"editprofile.html",{"form": form})



def login_redict(request):
    if not request.user.profile.first_name:
        return redirect('updateprofile')
    return redirect('profile')

def shippingrates(request):
    return render(request,'shippingrate.html')

def Help(request):
    return render(request,'help.html')

def FQAs(request):
    return render(request,'help_content/FAQs.html')

def FQAs2(request):
    return render(request,'help_content/FAQs2.html')        

def howtopay(request):
    return render(request,'help_content/howtopay.html') 

def cancelorder(request):
    return render(request,'help_content/cancel_order.html') 

def returnandrefund(request):
    return render(request,'help_content/returnandrefund.html') 

def subhelp1(request):
    return render(request,'help_content/howtoplaceorder.html') 

def trackorder(request):
    return render(request,'help_content/track_order.html') 

def terms(request):
    return render(request,'help_content/termsandconditions.html')     

@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False,
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.success(request, f"{item}'s quantity was updated")
            return redirect('order_summary')
        else:
            order.items.add(order_item)
            messages.success(request, f"{item} was added to your cart")
            return redirect('order_summary')
    else:
        # ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered=False)  # ordered_date=ordered_date)
        order.items.add(order_item)
        messages.success(request, f"{item} was added to your cart")
        return redirect('order_summary')


@login_required
def remove_single_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False)[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
                order.save()
            messages.success(request, f"{item}'s quantity was updated!")
            return redirect('order_summary')

        else:
            messages.success(request, f"{item} was not in your cart")
            return redirect('detail', slug=slug)
    else:
        messages.success(request, "You do not have an active order")
        return redirect('detail', slug=slug)


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False)[0]

            order.items.remove(order_item)
            messages.success(request, f"{item} was removed from your cart!")
            return redirect('order_summary')

        else:
            messages.success(request, f"{item} was not in your cart")
            return redirect('detail', slug=slug)
    else:
        messages.success(request, "You do not have an active order")
        return redirect('detail', slug=slug)




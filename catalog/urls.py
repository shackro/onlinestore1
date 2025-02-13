from django.urls import path,include
from django.contrib.auth import views as auth_views
from paypal.standard.ipn.views import ipn
from .views import (
    HomeView,
    IndexView,
    Case,
    Refubrished,
    Smartwatch,
    ProductDetailView,
    OrderSummaryView,
    PaymentView,
    CheckOutView,
    CouponView,
    RefundView,
    ShopBlockView,
    ShopListView,
    add_to_cart,
    payment_complete,
    profile,
    editprofile,
    remove_from_cart,
    remove_single_from_cart,
    SignupPage,
    LoginPage,
    paypal,
    creditcard,
    search,
    onsale,
    payment_canceled,
    SquarePaymentView,
    PaymentFailedView,
    Help,
    FQAs,
    FQAs2,
    howtopay,
    cancelorder,
    returnandrefund,
    subhelp1,
    trackorder,
    shippingrates,
    terms,
    # Cart
)

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('all_products', HomeView.as_view(), name='all_products'),
    path('signup/',SignupPage,name='signup'),
    path('login/',LoginPage,name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'),name='logout'),
    

    

    # path('cart/<slug>/', Cart.as_view(), name='cart'),

    path('search/',search,name="search"),
    path('Smartwatch/',Smartwatch.as_view(),name ='Smartwatch'),
    path('Case/',Case.as_view(),name ='Case'),
    path('onsale/',onsale.as_view(),name ='onsale'),
    
        
    path('refubrished/',Refubrished.as_view(),name ='refubrished'),
    path('add-coupon', CouponView.as_view(), name='add_coupon'),
    

    path('profile/', profile, name='profile'),
    path('editprofile/', editprofile, name='editprofile'),
    path('Help/',Help,name='help'),
    path('terms_and_conditions/',terms,name='terms'),
    path('how_to_pay/', howtopay, name='how_to_pay'),
    path('cancel_order/', cancelorder, name='cancel_order'),
    path('track_order/', trackorder, name='track_order'),
    path('return_and_refund/', returnandrefund, name='return_and_refund'),
    path('shippingrates/', shippingrates, name='shippingrates'),
    path('FQAs/', FQAs, name='FQAs'),
    path('subFQAs/', FQAs2, name='subFQAs'),
    path('subhelp1/', subhelp1, name='subhelp1'),
    

    path('shop/', ShopBlockView.as_view(), name='shop'),
    path('shop-list/', ShopListView.as_view(), name='shop_list'),
    path('request-refund', RefundView.as_view(), name='request_refund'),
    # urls.py
    path('detail/<int:pk>/', ProductDetailView.as_view(), name='detail'),
    path('add-to-cart/<int:pk>/', add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:pk>/', remove_from_cart, name='remove_from_cart'),
    path('payment/', PaymentView.as_view(), name='payment'),    
    path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),
    path('remove-single-from-cart/<int:pk>/',remove_single_from_cart, name='remove_single_from_cart'),
    path('order-summary/', OrderSummaryView.as_view(), name='order_summary'),
    
    path('square-payment/', SquarePaymentView.as_view(), name='square-payment'),
    path('paypal-ipn/', include('paypal.standard.ipn.urls')),
    path('credit-card/', creditcard.as_view(), name='credit_card_entry'),
    path('payment-cancelled/',payment_canceled, name='payment-cancelled'),
    path('payment-failed/', PaymentFailedView.as_view(), name='payment-failed'),
    

    path('checkout/', CheckOutView.as_view(), name='checkout'),
    path('paypal/<payment_option>/', paypal.as_view(), name='paypal'),
    path('paypal/', paypal.as_view(), name='paypal_payment'),
    path('creditcard/', creditcard.as_view(), name='creditcard'),
    path('creditcard/<payment_option>/', creditcard.as_view(), name='creditcard'),
    path('payment-complete', payment_complete, name='payment-complete'),


    path('password_reset/', 
         auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), 
         name='password_reset'),

    # Inform the user that the reset email has been sent
    path('password_reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), 
         name='password_reset_done'),

    # The link sent to the user's email will direct here for resetting the password
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), 
         name='password_reset_confirm'),

    # Final page after the password has been successfully reset
    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), 
         name='password_reset_complete'),

]

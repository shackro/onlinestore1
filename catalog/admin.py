from django.contrib import admin
from .models import (
    Item, OrderItem, Order, Address, Payment, Coupon,
    Refund, Category, Rating, Wishlist,Customer,customerrates
)
from django.utils.html import format_html
from django.shortcuts import redirect
from django.urls import path
from django.contrib import messages




def refund_accepted(modeladmin, request, queryset):
    queryset.update(refund_requested=False, refund_granted=True)


refund_accepted.short_description = 'Update to Refund granted'


def received(modeladmin, request, queryset):
    queryset.update(received=True)


received.short_descritpion = 'Update to Received'


class ItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ['title', 'price', 'color', 'discount_price', 'category', 'on_sale', 'duplicate_link','storage']
    search_fields = ['title', ]
    list_filter = ['category']
    list_display_links = ('title',)
    actions = ['duplicate_items']

    def duplicate_items(self, request, queryset):
        for obj in queryset:
            obj.pk = None
            obj.slug = f"{obj.slug}-copy"
            obj.title = f"Copy of {obj.title}"
            obj.save()
        self.message_user(request, "Selected items duplicated successfully!", messages.SUCCESS)

    duplicate_items.short_description = "Duplicate selected items"

    def duplicate_link(self, obj):
        return format_html('<a href="{}">Duplicate</a>', f"duplicate/{obj.pk}")

    duplicate_link.short_description = "Duplicate"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('duplicate/<int:pk>/', self.admin_site.admin_view(self.duplicate_single_item), name="duplicate_item"),
        ]
        return custom_urls + urls

    def duplicate_single_item(self, request, pk):
        obj = self.model.objects.get(pk=pk)
        obj.pk = None
        obj.slug = f"{obj.slug}-copy"
        obj.title = f"Copy of {obj.title}"
        obj.save()
        self.message_user(request, "Item duplicated successfully!", messages.SUCCESS)
        return redirect(f"../{obj.pk}/change/")


class AddressAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'street_address',
                    'apartment_address',
                    'country',
                    'city']

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user','firstname','lastname','city','mobile','country','country_code']


class customerrateAdmin(admin.ModelAdmin):
    list_display=['user','item','rating','customerratevideo','customerrate','customerrateimage1','customerrateimage2','customerrateimage3']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'ordered',
                    'ref_code',
                    'ordered_date',
                    'address',
                    'refund_requested',
                    'refund_granted',
                    'received']
    search_fields = ['user__username', 'ref_code']
    list_filter = [
        'user',
        'ordered',
        'received',
        'refund_requested',
        'refund_granted'
    ]
    actions = [
        refund_accepted,
        received
    ]


class RefundAdmin(admin.ModelAdmin):
    list_display = [
        'order',
        'email',
        'message'
    ]


class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'charge_id',
                    'amount',
                    'timestamp']


class RatingAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'value',
        'message'
    ]
    list_filter = [
        'user',
        'value'
    ]
    search_fields = [
        'value'
    ]


class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'amount']



admin.site.register(customerrates,customerrateAdmin)
admin.site.register(Customer)
admin.site.register(Item, ItemAdmin)
admin.site.register(OrderItem)
admin.site.register(Address, AddressAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Coupon, CouponAdmin)
admin.site.register(Category)
admin.site.register(Wishlist)
admin.site.register(Rating, RatingAdmin)
admin.site.register(Refund, RefundAdmin)

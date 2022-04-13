from django.contrib import admin
from . models import Product,Contact,Orders,OrderUpdate

# Register your models here.

admin.site.register(Product)
admin.site.register(Orders)
admin.site.register(Contact)
admin.site.register(OrderUpdate)


from django.contrib import admin

from .models import employee,storage,product,addMovements,removeMovements

admin.site.register(employee)
admin.site.register(storage)
admin.site.register(product)
admin.site.register(addMovements)
admin.site.register(removeMovements)

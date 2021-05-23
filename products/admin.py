from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Manufacturer)
admin.site.register(Smartphone)
admin.site.register(NoteBook)
admin.site.register(VideoCard)
admin.site.register(HddDisk)

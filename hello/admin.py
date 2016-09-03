from django.contrib import admin

# Register your models here.
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    pass

@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    pass
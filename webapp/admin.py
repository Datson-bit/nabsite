from django.contrib import admin
from .models import Event,Blog, Gallery,Video, Sponsor,Comment,Subscriber, GalleryImage, Executives, Parliamentary, Registration, EventPass, LiveStream
from import_export.admin import ExportMixin
from import_export import resources
from import_export.fields import Field


admin.site.site_header = "Nabwes Admin Dashboard"
admin.site.site_title = "Nabwes Admin Portal"

admin.site.register(Blog)
admin.site.register(Comment)
class EventPassResource(resources.ModelResource):
    # Add fields from related models
    full_name = resources.Field(attribute='registration__full_name', column_name='Full Name')
    email = resources.Field(attribute='registration__email', column_name='Email')
    phone = resources.Field(attribute='registration__phone', column_name='Phone Number')
    event_title = resources.Field(attribute='registration__event__title', column_name='Event Title')
    event_date = resources.Field(attribute='registration__event__date', column_name='Event Date')
    pass_code = resources.Field(attribute='pass_code', column_name='Event Pass Code')

    class Meta:
        model = EventPass
        fields = ('full_name', 'email', 'phone', 'event_title', 'event_date', 'pass_code')  # Specify export fields
        export_order = ('full_name', 'email', 'phone', 'event_title', 'event_date', 'pass_code')  # Order of fields

@admin.register(Executives)
class ExecutivesAdmin(admin.ModelAdmin):
    model = Executives
    list_display= ('name', 'position')
    
@admin.register(Parliamentary)
class ExecutivesAdmin(admin.ModelAdmin):
    model = Parliamentary
    list_display= ('name', 'position')

class GalleryImageInline(admin.TabularInline):  # Use StackedInline for vertical forms
    model = GalleryImage
    extra = 3  # Number of empty forms to display for new images
    fields = ('image', 'caption')

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    inlines = [GalleryImageInline]

@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('gallery', 'caption')

class SponsorInine(admin.TabularInline):
    model = Sponsor
    extra = 1

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    inlines = [SponsorInine]
    list_display = ['title', 'date', 'venue', ]

@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    list_display = ('name', 'event')

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email',)

@admin.register(Registration)
class RegistrationAdmin(ExportMixin,admin.ModelAdmin):
    resource_class = EventPassResource
    list_display = ['full_name', 'email', 'event', 'registered_at']

@admin.register(EventPass)
class EventPassAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = EventPassResource
   # Display related fields in the admin list view
    list_display = ('get_full_name', 'get_event_title', 'pass_code')
    search_fields = ('registration__full_name', 'registration__email', 'registration__event__title', 'pass_code')
    list_filter = ('registration__event__title', 'registration__event__date')  # Filter by event details

    # Custom method to display the registrant's full name
    def get_full_name(self, obj):
        return obj.registration.full_name
    get_full_name.short_description = 'Full Name'

    # Custom method to display the event title
    def get_event_title(self, obj):
        return obj.registration.event.title
    get_event_title.short_description = 'Event Title'


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'uploaded_at']


@admin.register(LiveStream)
class LiveStreamAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active')
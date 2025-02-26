from django.db import models
from ckeditor.fields import RichTextField
from taggit.managers import TaggableManager
from PIL import Image
from django.conf import settings
import secrets
from .paystack import PayStack
from django.utils.text import slugify


class Blog(models.Model):
    img_url =  models.ImageField(upload_to="images/")
    title = models.CharField(max_length=1000)
    authour = models.CharField(max_length=500)
    desc = models.CharField(max_length=500, default="")
    authour_img = models.ImageField(default="", )
    slug = models.SlugField( blank=True, null=True)
    # tags = TaggableManager()
    body = RichTextField(blank=True, null=True)
    date = models.DateField()
    view_count = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title) # Automatically generate slug from title
        super().save(*args, **kwargs)


    def __str__(self):
        return self.title

    
    def comment_count(self):
        return self.comments.filter(active=True).count()


class Event(models.Model):
    title= models.CharField(default="", max_length=1024)
    venue = models.CharField(max_length=1024, default="")
    desc = models.CharField(max_length=500, default="")
    body = RichTextField(blank=True, null=True)
    capacity = models.PositiveIntegerField(default=200, null=True)
    event_img_url= models.ImageField()
    date = models.DateField(null=True)

    def __str__(self):
        return self.title

class Registration(models.Model):
    event = models.ForeignKey(Event, related_name='registrations', on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    registered_at= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.event.title}"

class EventPass(models.Model):
    registration = models.OneToOneField(Registration, on_delete=models.CASCADE, related_name='event_pass')
    pass_code = models.CharField(max_length=12, unique= True)
    

    def __str__(self):
        return f"Pass for {self.registration.full_name}"
    
class Sponsor(models.Model):
    event = models.ForeignKey(Event, related_name='sponsors', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='sponsors/')
    website_or_social_url= models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name
    
class Gallery(models.Model):
    title = models.CharField(default="", max_length=1024)
    desc= models.CharField(default="", max_length=500)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return self.title
    

class GalleryImage(models.Model):
    gallery = models.ForeignKey(Gallery, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='gallery_images/')
    caption = models.CharField(max_length=100, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)

        # Set maximum dimensions
        max_width, max_height = 800, 800

        if img.width > max_width or img.height > max_height:
            # Resize the image
            img.thumbnail((max_width, max_height))
            img.save(self.image.path)


class HomeGallery(models.Model):
   title=  models.CharField( max_length=50)
   image = models.ImageField()

   def __str__(self):
       return self.title

class Comment(models.Model):
    blog = models.ForeignKey(Blog, related_name='comments', on_delete=models.CASCADE)
    author = models.CharField(max_length=70)
    email = models.EmailField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

class Executives(models.Model):
    name = models.CharField(max_length=500)
    position = models.CharField(max_length=500)
    image= models.ImageField(upload_to="gallery_images/")
    facebook_link = models.CharField(max_length=2000)
    linkedIn_link = models.CharField(max_length=2000)
    twitter_link = models.CharField(max_length=2000)

class Parliamentary(models.Model):
    name = models.CharField(max_length=500)
    position = models.CharField(max_length=500)
    image= models.ImageField(upload_to="gallery_images/")
    facebook_link = models.CharField(max_length=2000)
    linkedIn_link = models.CharField(max_length=2000)
    twitter_link = models.CharField(max_length=2000)

class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    subscried_at= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
    
class Video(models.Model):
    title = models.CharField(max_length=225)
    description = models.CharField(max_length=255)
    video_file = models.FileField(upload_to="video/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

# Live Stream start
class LiveStream(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    stream_url = models.URLField(help_text="URL of the live stream")
    is_active = models.BooleanField(default=True)
# Live Stream start
    
    def __str__(self):
        return self.title
    
class Due(models.Model):
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    

class Payment(models.Model):
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    email = models.EmailField(max_length= 50)
    due = models.ForeignKey(Due, on_delete=models.CASCADE, default="")
    # amount = models.DecimalField(max_digits=10, decimal_places=2)
    ref= models.CharField(max_length=100, unique=True, blank= True)
    verified = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment by {self.name} - Ref {self.ref}"
    
    def save(self, *args, **kwargs):
        if not self.ref:
            self.ref = secrets.token_urlsafe(20)
        super().save(*args, **kwargs)

    def verify_payment(self):
        paystack = PayStack()
        status, result = paystack.verify_payment(self.ref, self.due.amount)

        if status:
            self.verified = True
            self.save()
        return self.verified
    




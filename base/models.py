import uuid, shutil, os
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from PIL import Image
from io import BytesIO
from django.core.files import File
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import default_storage
from ckeditor.fields import RichTextField
from colorfield.fields import ColorField

# Create your models here.

def compressImage(image):
    im = Image.open(image)
    im = im.convert('RGB')
    im_io = BytesIO()
    im.save(im_io, 'JPEG', quality=50)
    new_image = File(im_io, name=image.name)
    return new_image

def nameAndOverwriteMemberImage(instance, filename):
    return ('images/profile_pics/' + instance.user.username + str(instance.id) + ".jpg").replace(" ", "_")

class Member(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE, default="", related_name="member")
    name = models.CharField(max_length= 100)
    email = models.EmailField(max_length= 254, default="")
    admission = models.CharField(max_length=50, default="",blank=True)
    year = models.CharField(max_length=20, choices=[('1st Year', 'First year'), ('2nd Year', 'Second year'), ('3rd Year', 'Third year'), ('4th Year', 'Fourth year'), ('Faculty', 'Faculty'), ('Alumni', 'Alumni')], default="1st")
    mobile_no = models.CharField(max_length=10, default="", blank=True)
    faculty = models.BooleanField(default=False)
    profile_pic = models.ImageField(upload_to=nameAndOverwriteMemberImage, default="images/profile_pics/default.png", blank=True)
    linked_in = models.CharField(max_length=150, default="", null=True, blank=True)
    github = models.CharField(max_length=150, default="", null=True, blank=True)
    w_chapter = models.BooleanField(default=False)
    core = models.CharField(max_length= 50, null=True, blank=True)
    role = models.CharField(max_length= 100, null=True, blank=True)
    short_desc = models.CharField(max_length=120, default="Hello, I love being in ACM's core team", blank=True)
    desc = models.TextField(max_length=500, default="Hello, I love being in ACM's core team", blank=True)
    unique_url = models.CharField(max_length=255, blank=True)
    url_timeout = models.TimeField(auto_now= False, auto_now_add=False, null=True, blank=True)

    def save(self, *args, **kwargs):
        # try:
        #     this = Member.objects.get(id=self.id)
        #     if not self.profile_pic:
        #         if self.profile_pic.field.default != this.profile_pic:
        #             default_storage.delete(this.profile_pic.path)
        #         self.profile_pic = self.profile_pic.field.default
            
        #     if this.profile_pic and this.profile_pic != self.profile_pic and this.profile_pic != self.profile_pic.field.default and os.path.isfile(this.profile_pic.path):
        #         default_storage.delete(this.profile_pic.path)
        #         new_image = compressImage(self.profile_pic)
        #         self.profile_pic = new_image
        # except ObjectDoesNotExist:
        #     pass
        new_image = compressImage(self.profile_pic)
        self.profile_pic = new_image
        super(Member, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name

def nameNewsImage(instance, filename):
    try:
        this = News.objects.get(id=instance.id)
        if this.image.path and os.path.isfile(this.image.path):
            os.remove(this.image.path)
    except (ObjectDoesNotExist, PermissionError):
        pass
    return ('images/news/' + filename + ".jpg").replace(" ", "_")

class News(models.Model):
    headline = models.CharField(max_length=80)
    image = models.ImageField(upload_to=nameNewsImage, blank=True)
    desc = models.TextField(max_length=500)
    created = models.DateTimeField()
    
    def save(self, *args, **kwargs):
        new_image = compressImage(self.image)
        self.image = new_image
        super(News, self).save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.headline

class Byte(models.Model):
    owner = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="mybytes")
    byte = models.CharField(max_length=120)
    created = models.DateTimeField(editable=False)
    edited = models.DateTimeField()
    
    def __str__(self) -> str:
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.edited = timezone.now()
        return super(User, self).save(*args, **kwargs)

def nameEventPhotos(instance, filename):
    try:
        this = Photo.objects.get(id=instance.id)
        if this.image.path and os.path.isfile(this.image.path):
            os.remove(this.image.path)
    except ObjectDoesNotExist:
        pass
    return ('images/events/' + instance.event.name + "/" + filename).replace(" ", "_")

class Photo(models.Model):
    image = models.ImageField(upload_to=nameEventPhotos)
    event = models.ForeignKey('Event', on_delete= models.CASCADE, related_name="photos")

    def save(self, *args, **kwargs):
        new_image = compressImage(self.image)
        self.image = new_image
        super(Photo, self).save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.event.name

class Tag(models.Model):
    name = models.CharField(max_length=100)
    tag_bg_color = ColorField(null=True)
    tag_text_color = ColorField(null=True)
    
    def related_events(self) -> int:
        return self.events.count()
    
    def __str__(self) -> str:
        return self.name

def nameAndOverwriteStudentImage(instance, filename):
    return ('images/profile_pics/' + instance.user.username + str(instance.id) + ".jpg").replace(" ", "_")

class Student(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE, default="", related_name="student")
    name = models.CharField(max_length= 100)
    college = models.CharField(max_length=150, null=True, blank=True)
    year = models.CharField(max_length=20, choices=[('1st Year', 'First year'), ('2nd Year', 'Second year'), ('3rd Year', 'Third year'), ('4th Year', 'Fourth year'), ('Alumni', 'Alumni')], default="1st")
    admission = models.CharField(max_length=50, default="")
    email = models.EmailField(max_length= 254, default="", unique=True)
    mobile_no = models.CharField(max_length=10, default="", blank=True)
    profile_pic = models.ImageField(upload_to=nameAndOverwriteStudentImage, default="images/profile_pics/default.png", blank=True)
    linked_in = models.CharField(max_length=150, default="", null=True, blank=True)
    github = models.CharField(max_length=150, default="", null=True, blank=True)
    core = models.CharField(max_length= 50, null=True, blank=True)
    desc = models.TextField(max_length=500, default="Hello, I promise to be awesome!!", blank=True)
    teams = models.ManyToManyField('Team', blank=True, related_name="member")
    unique_url = models.CharField(max_length=255, blank=True)
    url_timeout = models.TimeField(auto_now= False, auto_now_add=False, null=True, blank=True)

    def save(self, *args, **kwargs):
        # try:
        #     this = Student.objects.get(id=self.id)
        #     if not self.profile_pic:
        #         if self.profile_pic.field.default != this.profile_pic:
        #             default_storage.delete(this.profile_pic.path)
        #         self.profile_pic = self.profile_pic.field.default
            
        #     if this.profile_pic and this.profile_pic != self.profile_pic and this.profile_pic != self.profile_pic.field.default and os.path.isfile(this.profile_pic.path):
        #         default_storage.delete(this.profile_pic.path)
        #         new_image = compressImage(self.profile_pic)
        #         self.profile_pic = new_image
        # except ObjectDoesNotExist:
        #     pass
        
        new_image = compressImage(self.profile_pic)
        self.profile_pic = new_image
        super(Student, self).save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.user.username

def nameEventImage(instance, filename):
    # try:
    #     this = Event.objects.get(id=instance.id)
    #     if this.image.path and os.path.isfile(this.image.path):
    #         os.remove(this.image.path)
    # except (ObjectDoesNotExist, PermissionError):
    #     pass
    return ('images/events/' + instance.name[:30] + "/" + instance.name[:30] + "_poster.jpg").replace(" ", "_")

class Event(models.Model):
    name = models.CharField(max_length= 150)
    description = models.TextField(null= True, blank= True)
    details = RichTextField(null=True, blank=True)
    location = models.CharField(max_length= 150, null=True, blank=True)
    image = models.ImageField(upload_to=nameEventImage)
    tag = models.ManyToManyField(Tag, blank=True, related_name="events")
    fee = models.CharField(max_length= 5, default= 0)
    ongoing = models.BooleanField(default=False)
    team_members = models.IntegerField(default=1)
    coordinator = models.ManyToManyField(Member, blank=True, related_name="coordinated")
    updated = models.DateTimeField(auto_now= True)
    created = models.DateTimeField(auto_now_add= True)
    event_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    participants = models.ManyToManyField(Student, blank=True, related_name="participated")
    first = models.ManyToManyField(Student, blank=True, related_name="first")
    second = models.ManyToManyField(Student, blank=True, related_name="second")
    third = models.ManyToManyField(Student, blank=True, related_name="third")

    def __str__(self) -> str:
        return self.name
    
    def incharge(self):
        return ",".join([str(c) for c in self.coordinator.all()])
    
    def save(self, *args, **kwargs):
        new_image = compressImage(self.image)
        self.image = new_image
        super(Event, self).save(*args, **kwargs)


class Team(models.Model):
    team_name = models.CharField(max_length=100)
    team_id = models.CharField(max_length=255, unique=True, default=uuid.uuid4, editable=False)
    event = models.ManyToManyField(Event, related_name="teams")
    leaders = models.ManyToManyField(Student, related_name="team_leader")
    members = models.ManyToManyField(Student, blank=True, related_name="myteams")
    verified_by = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="verifications", null=True, blank=True)

    def __str__(self) -> str:
        return self.team_name
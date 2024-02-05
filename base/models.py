from typing import Any
import json
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
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

def existsThenDelete(name):
    supabase = create_client(os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_KEY"))
    res = supabase.storage.from_('images').list(path=os.path.dirname(name))
    
    if any(file['name'] == os.path.basename(name) for file in res):
        supabase.storage.from_('images').remove(name)

def nameAndOverwriteMemberImage(instance, filename):
    name = ('images/profile_pics/' + instance.user.username + str(instance.id) + ".jpg").replace(" ", "_")
    existsThenDelete(name)
    return name

class Member(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE, default="", related_name="member")
    name = models.CharField(max_length= 100)
    email = models.EmailField(max_length= 254, default="")
    admission = models.CharField(max_length=50, default="",blank=True)
    year = models.CharField(max_length=20, choices=[('1st Year', 'First year'), ('2nd Year', 'Second year'), ('3rd Year', 'Third year'), ('4th Year', 'Fourth year'), ('Faculty', 'Faculty'), ('Alumni', 'Alumni')], default="1st")
    mobile_no = models.CharField(max_length=10, default="", blank=True)
    faculty = models.BooleanField(default=False)
    profile_pic = models.ImageField(upload_to=nameAndOverwriteMemberImage, default="images/profile_pics/default.jpg", blank=True)
    linked_in = models.CharField(max_length=150, default="", null=True, blank=True)
    github = models.CharField(max_length=150, default="", null=True, blank=True)
    w_chapter = models.BooleanField(default=False)
    core = models.CharField(max_length= 50, null=True, blank=True)
    role = models.CharField(max_length= 100, default="Member", null=True, blank=True)
    short_desc = models.CharField(max_length=120, default="Hello, I love being in ACM's core team", blank=True)
    desc = models.TextField(max_length=500, default="Hello, I love being in ACM's core team", blank=True)
    unique_url = models.CharField(max_length=255, blank=True)
    url_timeout = models.TimeField(auto_now= False, auto_now_add=False, null=True, blank=True)

    def save(self, *args, **kwargs):
        try:
            this = Member.objects.get(id=self.id)
            if not self.profile_pic:
                if self.profile_pic.field.default != this.profile_pic:
                    create_client(os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_KEY")).storage.from_("images").remove(this.profile_pic.name)
                self.profile_pic = self.profile_pic.field.default
        except ObjectDoesNotExist:
            pass
        super(Member, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name

def nameNewsImage(instance, filename):
    name = ('images/news/' + filename + ".jpg").replace(" ", "_")
    existsThenDelete(name)
    return name

class News(models.Model):
    headline = models.CharField(max_length=80)
    image = models.ImageField(upload_to=nameNewsImage, blank=True)
    desc = models.TextField(max_length=500)
    created = models.DateTimeField()
    
    def __str__(self) -> str:
        return self.headline


def nameEventPhotos(instance, filename):
    name = ('images/events/' + instance.event.name + "/" + filename).replace(" ", "_")
    existsThenDelete(name)
    return name

class Photo(models.Model):
    image = models.ImageField(upload_to=nameEventPhotos)
    event = models.ForeignKey('Event', on_delete= models.CASCADE, related_name="photos")
    
    def __str__(self) -> str:
        return self.event.name

class Tag(models.Model):
    name = models.CharField(max_length=100)
    theme = ColorField(null=True)
    
    def related_events(self) -> int:
        return self.events.count()
    
    def __str__(self) -> str:
        return self.name

def nameAndOverwriteStudentImage(instance, filename):
    name = ('images/profile_pics/' + instance.user.username + str(instance.id) + ".jpg").replace(" ", "_")
    existsThenDelete(name)
    return name

class Student(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE, default="", related_name="student")
    name = models.CharField(max_length= 100)
    college = models.CharField(max_length=150, null=True, blank=True)
    year = models.CharField(max_length=20, choices=[('1st Year', 'First year'), ('2nd Year', 'Second year'), ('3rd Year', 'Third year'), ('4th Year', 'Fourth year'), ('Alumni', 'Alumni')], default="1st")
    admission = models.CharField(max_length=50, default="")
    email = models.EmailField(max_length= 254, default="", unique=True)
    mobile_no = models.CharField(max_length=10, default="", blank=True)
    profile_pic = models.ImageField(upload_to=nameAndOverwriteStudentImage, default="images/profile_pics/default.jpg", blank=True)
    linked_in = models.CharField(max_length=150, default="", null=True, blank=True)
    github = models.CharField(max_length=150, default="", null=True, blank=True)
    core = models.CharField(max_length= 50, null=True, blank=True)
    desc = models.TextField(max_length=500, default="Hello, I promise to be awesome!!", blank=True)
    teams = models.ManyToManyField('Team', blank=True, related_name="member")
    unique_url = models.CharField(max_length=255, blank=True)
    url_timeout = models.TimeField(auto_now= False, auto_now_add=False, null=True, blank=True)

    def save(self, *args, **kwargs):
        try:
            this = Student.objects.get(id=self.id)
            if not self.profile_pic:
                if self.profile_pic.field.default != this.profile_pic:
                    create_client(os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_KEY")).storage.from_("images").remove(this.profile_pic.name)
                self.profile_pic = self.profile_pic.field.default
        except ObjectDoesNotExist:
            pass
        super(Student, self).save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.user.username

def nameEventImage(instance, filename):
    name = ('images/events/' + instance.name[:30] + "/" + instance.name[:30] + "_poster.jpg").replace(" ", "_")
    existsThenDelete(name)
    return name

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


class Question(models.Model):
    question = models.TextField()
    option = models.TextField()
    belongsTo = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='questions')

    def __str__(self) -> str:
        return f"{self.question} {self.belongsTo}"

    def toDict(self):
        return {
            'question':self.question,
            'options':json.loads(self.option),
            'belongsTo':self.belongsTo.id,
            'id':self.id,
        }

class QuestionResponse(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='responses')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='responses')
    answer = models.TextField()

    def __str__(self) -> str:
        return f"{self.question} {self.student}"

class Team(models.Model):
    team_name = models.CharField(max_length=100)
    team_id = models.CharField(max_length=255, unique=True, default=uuid.uuid4, editable=False)
    event = models.ManyToManyField(Event, related_name="teams")
    leaders = models.ManyToManyField(Student, related_name="team_leader")
    members = models.ManyToManyField(Student, blank=True, related_name="myteams")
    verified_by = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="verifications", null=True, blank=True)

    def __str__(self) -> str:
        return self.team_name
    


def nameBytePoster(instance, filename):
    name = ('images/blogsPosters/' + instance.owner.username +'/' + filename).replace(" ", "_")
    return name

class Byte(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="mybytes", default='', null=True, blank=True)
    byte = models.TextField()
    poster = models.ImageField(upload_to=nameBytePoster, blank=True, null=True)
    likeOwner = models.ManyToManyField(User, blank=True, related_name='liked', default='')
    likes = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.owner.username
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.edited = timezone.now()
        return super(Byte, self).save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        if self.poster:
            create_client(os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_KEY")).storage.from_("images").remove(self.poster.name)
        return super().delete(*args, **kwargs)
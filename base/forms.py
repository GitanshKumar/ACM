from django import forms
from captcha.fields import CaptchaField
from .models import Member, Student

class CaptchaForm(forms.Form):
    captcha = CaptchaField(label="Please enter the characters in the image")

class EditMemberForm(forms.ModelForm):
    core = forms.CharField(required=True)
    admission = forms.CharField(required=True)
    desc = forms.CharField(widget=forms.Textarea(attrs={"maxlength": "500", "rows":"8"}))
    short_desc = forms.CharField(widget=forms.Textarea(attrs={"maxlength": "120", "rows":"3"}))
    class Meta:
        model = Member
        fields = ('year', 'mobile_no', 'profile_pic', 'linked_in', 'github', 'desc', 'short_desc', 'core', 'admission')

class EditStudentForm(forms.ModelForm):
    core = forms.CharField(required=True)
    admission = forms.CharField(required=True)
    desc = forms.CharField(widget=forms.Textarea(attrs={"maxlength": "500", "rows":"8"}))
    class Meta:
        model = Student
        fields = ('year', 'mobile_no', 'profile_pic', 'linked_in', 'github', 'desc', 'core', 'admission')
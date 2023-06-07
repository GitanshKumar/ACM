import csv, uuid, re
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.core import serializers
from itertools import chain
from django.db.models import Q
from datetime import datetime, timedelta, time
from .models import Event, Member, Student, Team, Tag, News
from .forms import EditMemberForm, EditStudentForm, CaptchaForm
from .custom import send_mail

def home(request):
    ongoing = Event.objects.filter(ongoing= True).order_by("event_date")
    other = Event.objects.filter(ongoing= False).order_by("-event_date")[:9 - ongoing.count()]
    news = News.objects.all()[:5]
    context = {"other": other, "ongoing": ongoing, "news":news}
    return render(request, 'base/home.html', context)

def search(request):
    q = request.GET.get("search", "")
    shown = 8
    if request.headers.get('x-requested-with'):
        if "loadmore" in request.GET:
            prev = int(request.GET["count"])
            q = request.GET["q"]
            shown = prev + 5
            event_results = Event.objects.filter(name__icontains=q)
            member = Member.objects.filter(name__startswith= q)
            stu = Student.objects.filter(name__startswith= q)
            res = []
            for i in event_results:
                res.append(["event", i.name, i.image.url, i.event_date.date(), i.description, list(i.tag.all().values_list("name", flat=True))])
            for i in stu:
                res.append(["student", i.name, i.user.username, i.profile_pic.url, i.core if i.core else "", i.year, "", i.desc])
            for i in member:
                res.append(["member", i.name, i.user.username, i.profile_pic.url, i.core, i.year, i.role, i.desc])
            
            count = event_results.count() + member.count() + stu.count()
            left = True
            if shown > count:
                left = False
                shown = count
            return JsonResponse([left, shown, count] + sorted(res, key= lambda a: a[1])[prev:shown], safe=False)
        
        elif q != "":
            event_results = Event.objects.filter(name__icontains=q).values_list("name")[:5]
            member = Member.objects.filter(name__startswith= q)[:5]
            stu = Student.objects.filter(name__startswith= q)[:5]
            res = list(event_results)
            for i in stu:
                res.append([i.name, i.user.username, i.profile_pic.url, "", i.core if i.core else "", ""])
            for i in member:
                res.append([i.name, i.user.username, i.profile_pic.url, "MEMBER", i.core, i.role])
            return JsonResponse(sorted(res, key= lambda a: a[0])[:8], safe=False)
        else:
            return JsonResponse("", safe=False)
    
    event_results = Event.objects.filter(name__icontains=q)
    member = Member.objects.filter(name__startswith= q)
    stu = Student.objects.filter(name__startswith= q)
    combined_results = sorted(chain(event_results, member, stu),key=lambda x: x.name.lower())
    
    left = shown < len(combined_results)
    return render(request, "base/search.html", {"results":combined_results[:shown], "left":left, "shown": shown, "total":len(combined_results)})

def event(request, pk):
    sel_event = Event.objects.get(name=pk)
    mem = False
    registered = False
    if request.user.is_authenticated:
        try:
            Member.objects.get(user=request.user)
            mem = True
        except:
            if sel_event in request.user.student.participated.all():
                registered = True

    if request.method == "POST":
        if request.user.is_authenticated:
            sel_event.participants.add(request.user.student)
            sel_event.save()
            return redirect(reverse("event", args=(sel_event.name,)))
        else:
            messages.error(request, "Signup or Login to register for events")
            return redirect("login")

    context = {'event': sel_event, "member":mem, "registered":registered, "photos": sel_event.photos.all()}
    return render(request, 'base/event.html', context)

def events(request):
    q = request.GET.get("q", "")
    start = request.GET.get("start") if request.GET.get("start") and request.GET.get("start") != "mm-dd-yyyy" else "1900-01-01"
    end = request.GET.get("end") if request.GET.get("end") and request.GET.get("end") != "mm-dd-yyyy" else "9999-01-01"
    events = Event.objects.all().order_by("-event_date")
    count = total = events.count()
    context = {"events": events}
    shown = 10

    if "clear" in request.GET:
        q, start, end = "", "1900-01-01", "9999-01-01"

    if "q" in request.GET:
        events = events.filter(Q(name__icontains=q) | Q(tag__name__icontains=q), event_date__date__range=(start, end)).order_by("-event_date").distinct()
        count = events.count()
    
    if "loadmore" in request.GET:
        prev = int(request.GET["count"])
        shown = prev + 5
        res = []
        print(shown, q, prev)
        for i in events[prev:shown]:
             res.append([i.name, i.image.url, i.event_date.date(), i.description, list(i.tag.all().values_list("name", flat=True))])
        return JsonResponse([shown < count] + res, safe=False)
    
    context = {"tags": sorted(Tag.objects.all().order_by("name"), key= lambda a: a.related_events(), reverse=True),
               "events": events[:shown],
               "total": total,
               "left":shown < count,
               "search":q,
               "start":"mm-dd-yyyy" if start == "1900-01-01" else start,
               "end": "mm-dd-yyyy" if end == "9999-01-01" else end}
    
    return render(request, 'base/events.html', context)

def aboutus(request):
    fac_team = Member.objects.filter(faculty= True)
    stu_team = Member.objects.filter(faculty= False).order_by("-role")
    return render(request, 'base/aboutus.html', {"faculty":fac_team,
                                                 "student":stu_team.filter(w_chapter= False),
                                                 "wchapter":stu_team.filter(w_chapter=True)})

def team(request):
    fac_team = Member.objects.filter(faculty= True)
    stu_team = Member.objects.filter(faculty= False).order_by("-role")
    return render(request, 'base/team.html', {"faculty":fac_team,
                                                 "student":stu_team.filter(w_chapter= False),
                                                 "wchapter":stu_team.filter(w_chapter=True)})

def valid_password(p1: str, p2: str):
    res = []
    if p1 != p2: res.append("Password do not match")
    if len(p1) < 8: res.append("Password must be 8 characters long")
    if not re.search(r'[A-Z]', p1): res.append("At least one uppercase")
    if not re.search(r'[a-z]', p1): res.append("At least one lowercase")
    if not re.search(r'[!@#$%^&*]', p1): res.append("At least one special character")
    if not re.search(r'\d', p1): res.append("At least one digit")
    return res, res == []

def signup(request):
    context = {}
    if request.method == "POST":
        name = request.POST.get("name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        re_password = request.POST.get("re-password")
        form = CaptchaForm(request.POST)
        if not form.is_valid():
            context["captcha"] = True
        
        if User.objects.filter(username=username).first():
            context["username"] = username
        
        errors, valid = valid_password(password, re_password)
        if not valid:
            context["password"] = errors
        
        if Student.objects.filter(email=email).first():
            context["email"] = email
        
        if not context:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            mem = Student(user=user, name=name, email=email)
            mem.save()
            user = authenticate(request, username= username, password=password)
            login(request, user)
            return redirect("edit_profile")
        
        context["name"] = name
    
    form = CaptchaForm()
    context["form"] = form
    return render(request, "base/signup.html", context)

def loginuser(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            user = User.objects.get(username= username)
        except: 
            messages.error(request, "User Does not exist")
        
        user = authenticate(request, username= username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Username or password Does not exist")
        
    return render(request, 'base/login.html')

def profile(request, pk):
    try:
        user = Member.objects.get(user=User.objects.get(username=pk))
        is_mem = True
        events_info = user.coordinated.all()
    except:
        is_mem = False
        user = Student.objects.get(user=User.objects.get(username=pk))
        events_info = user.participated.all()
    context = {"user":user, "is_owner": request.user == user.user, "member": is_mem, "event_info":events_info}
    return render(request, 'base/myprofile.html', context)

def logoutuser(request):
    logout(request)
    return redirect("home")

@login_required
def edit_profile(request):
    if request.method == 'POST':
        try:
            user = request.user.member
            form = EditMemberForm(request.POST, request.FILES, instance=user)
        except:
            user = request.user.student
            form = EditStudentForm(request.POST, request.FILES, instance=user)
        
        if form.is_valid():
            form.save()
            return redirect(reverse("profile", args=(user.user,)))
    else:
        try:
            form = EditMemberForm(instance=request.user.member)
            mem = True
        except:
            form = EditStudentForm(instance=request.user.student)
            mem = False
    return render(request, 'base/edit_profile.html', {'form': form, "member": mem})

def register(request, pk, cat):
    if not request.user.is_authenticated:
        messages.error(request, "Signup or login to register for the event")
        return redirect("login")
    
    event = Event.objects.get(name=pk)
    student = request.user.student
    context = {"event": event, "user":student, "join": cat == "join", "error": ""}

    if request.method == "POST":
        if cat == "join":
            team_id = request.POST.get("team_id")
            if student not in event.participants.all():
                try:
                    team = Team.objects.get(team_id=team_id)
                except:
                    context["error"] = "Team does not exist"
                    return render(request, "base/register.html", context)
                if team.members.count() == event.team_members:
                    context["error"] = "Team full"
                    return render(request, "base/register.html", context)
                team.members.add(student)
                event.participants.add(student)
                event.save()
                team.save()
                return redirect(reverse("viewteam", args=(event.name,)))
            else:
                context["error"] = "Already Registered"
                return render(request, "base/register.html", context)
        else:
            team_name = request.POST.get("team_name")

            if student not in event.participants.all():
                team = Team.objects.create(team_name=team_name)
                team.leaders.add(student)
                team.members.add(student)
                team.event.add(event)
                team.save()
                event.participants.add(student)
                event.save()
                return redirect(reverse("viewteam", args=(event.name,)))
            else:
                context["error"] = "ALready registered"
                return render(request, "base/register.html", context)
    
    return render(request, "base/register.html", context)

def viewteam(request, pk):
    if not request.user.is_authenticated:
        messages.error(request, "Signup to create a team")
        return redirect("home")
    
    event = Event.objects.get(name=pk)
    team = request.user.student.myteams.filter(event=event).first()
    if team is None: return redirect("home")
    leader = team.leaders.all().first()
    members = []
    for member in team.members.all():
        if leader != member:
            members.append(member)
    return render(request, "base/viewteam.html", {"leader":leader, "members":members, "team":team, "event":event})

def event_details(request, pk):
    request.user.member
    event = Event.objects.get(name=pk)
    teams, participants = "", ""
    q = request.GET.get("q", "")
    if "clear" in request.GET: q = ""

    if event.team_members > 1: teams = Team.objects.filter(Q(team_name__startswith= q) | Q(leaders__name__startswith= q), event=event)
    else: participants = event.participants.all()
    
    context = {"values":participants or teams, "team": teams != "", "event": event, "search":q}
    return render(request, "base/event_details.html", context)

def reset_password(request, reset_id):
    if request.method == "POST":
        if "email" in request.POST:
            email = request.POST.get("email")
            user = Member.objects.filter(email=email).first()
            if not user: user = Student.objects.filter(email=email).first()
            if not user:
                messages.error(request, "Email does not exist")
                return redirect(reverse("reset_pass", args=("request",)))
            user.unique_url = uuid.uuid4()
            user.url_timeout = datetime.now()
            user.save()
            send_mail(email, "Reset Password request", "<div>You can reset password through this link " + request.build_absolute_uri(reverse("reset_pass", args=(user.unique_url,))) + "<br>Link will expire in 1 hour.</div>")
            return render(request, 'base/reset_password.html', {"email_sent":True})
        else:

            password = request.POST.get("pass")
            re_password = request.POST.get("cpass")
            errors, valid = valid_password(password, re_password)
            if not valid:
                return render(request, 'base/reset_password.html', {"reset":True, "errors":errors})
            else:
                user = Member.objects.filter(unique_url= reset_id).first()
                if not user: user = Student.objects.filter(unique_url= reset_id).first()
                user.user.set_password(password)
                user.unique_url = ""
                user.url_timeout = None
                user.user.save()
                messages.error(request, "Successfully updated password")
                return redirect("login")
    
    if reset_id != "request":
        user = Member.objects.filter(unique_url= reset_id).first()
        if not user: user = Student.objects.filter(unique_url= reset_id).first()
        if not user: return redirect("home")
        time_diff = (datetime.now() - datetime.combine(datetime.today(), user.url_timeout)).total_seconds() / 3600
        if time_diff > 1:
            user.unique_url = ""
            user.url_timeout = None
            user.save()
            messages.error(request, "Link expired, request another now")
            return redirect(reverse("reset_pass", args=("request",)))
        return render(request, 'base/reset_password.html', {"reset":True})
    
    return render(request, 'base/reset_password.html', {"req":True})


# import random
# import string

# def generate_random_password():
#     length = 8
#     while True:
#         password = []
#         password.append(random.choice(string.ascii_uppercase))  # At least 1 uppercase
#         password.append(random.choice(string.ascii_lowercase))  # At least 1 lowercase
#         password.append(random.choice(string.digits))  # At least 1 digit
#         password.append(random.choice("!@#$&*"))  # At least 1 special character

#         remaining_length = length - len(password)
#         password += random.choices(
#             string.ascii_letters + string.digits + string.punctuation,
#             k=remaining_length
#         )

#         random.shuffle(password)
#         password = ''.join(password)

#         if (
#             any(c.isupper() for c in password) and
#             any(c.islower() for c in password) and
#             any(c.isdigit() for c in password) and
#             any(c in string.punctuation for c in password)
#         ):
#             return password

# def temp():
#     with open("temo\ACM Members - 1st year.csv", "r") as f:
#         a = csv.DictReader(f)
#         with open("temo/1st.csv", "a") as f1:
#             for i in a:
#                 pwd = generate_random_password()
#                 name = "".join(i["Name"].split()).lower()
                
#                 user = User.objects.create(username=name, email=i["email id"], password= pwd)
#                 user.save()
#                 mem = Member(user=user, name=i["Name"], email=i["email id"], admission=i["Admission no."], year="1st", mobile_no=i["mobile number"], core="CS")
#                 mem.save()

#                 f1.write()
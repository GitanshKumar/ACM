from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.db.models import Q
from .models import Event, Member, Student, Team, Tag
from .forms import EditMemberForm, EditStudentForm, CaptchaForm
import re

def home(request):
    ongoing = Event.objects.filter(ongoing= True).order_by("event_date")
    other = Event.objects.filter(ongoing= False).order_by("-event_date")[:9 - ongoing.count()]
    context = {"other": other, "ongoing": ongoing}
    return render(request, 'base/home.html', context)

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
    events = Event.objects.all().order_by("-event_date")
    q = request.GET.get("q", "")
    start = request.GET.get("start") if request.GET.get("start") and request.GET.get("start") != "mm-dd-yyyy" else "1900-01-01"
    end = request.GET.get("end") if request.GET.get("end") and request.GET.get("end") != "mm-dd-yyyy" else "9999-01-01"
    shown = int(request.GET.get("events")) if request.GET.get("events") else 5
    if "clear" in request.GET:
        q, start, end, shown = "", "1900-01-01", "9999-01-01", 5
    
    context = {"tags": sorted(Tag.objects.all().order_by("name"), key= lambda a: a.related_events(), reverse=True),
               "events": events[:shown],
               "shown":shown,
               "total":events.count(),
               "left":shown < events.count(),
               "search":q,
               "start":"mm-dd-yyyy" if start == "1900-01-01" else start,
               "end": "mm-dd-yyyy" if end == "9999-01-01" else end}

    if "q" in request.GET:
        context["events"] = events.filter(Q(name__icontains=q) | Q(tag__name__icontains=q), event_date__date__range=(start, end)).order_by("-event_date").distinct()
    
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
        except:
            form = EditStudentForm(instance=request.user.student)
    return render(request, 'base/edit_profile.html', {'form': form})

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

    if event.team_members > 1: teams = Team.objects.filter(Q(team_name__icontains= q) | Q(leaders__name__icontains= q), event=event)
    else: participants = event.participants.all()
    
    context = {"values":participants or teams, "team": teams != "", "event": event, "search":q}
    return render(request, "base/event_details.html", context)
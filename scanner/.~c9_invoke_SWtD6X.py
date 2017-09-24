from django.shortcuts import render, HttpResponseRedirect
from django.core.urlresolvers import reverse
from forms import ScanForm, NewUserForm, NewItemForm, AdminLoginForm, NewLeadershipMemberForm, ChangePermissionsForm
from models import Person, CheckoutItem, Checkout, Checkin, LeadershipMember
from datetime import datetime, timedelta
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from decorators import not_login_required

# Create your views here.

master_schedule = ["BCDEFG", "CAEDGF", "ABDEFG", "BACEGF", "CABDFG", "ABCDEG", "BACDEF"]

@not_login_required
def main (request):
    logout(request)
    if request.method == 'POST':
        form = ScanForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
        return HttpResponseRedirect(reverse("scan", args=(data["scan"],)))
        
    form = ScanForm()
    return render(request, "scanner/main.html", {"form": form})

@not_login_required
def schedule(request):
    schedule=[]
    for i in range(7):
        schedule.append([])
    for i in range(7):
        schedule[0].append(["Day " + str(i + 1)])
    for i in range(7):
        for j in range(6):
            schedule[j + 1].append([master_schedule[i][j:j+1]])
            
    for lm in LeadershipMember.objects.all():
        for i in range(len(lm.periods) / 2):
            day = int(lm.periods[i * 2 + 1:i * 2 + 2])
            period = master_schedule[day - 1].index(lm.periods[i * 2:i * 2 + 1])
            schedule[period + 1][day - 1].append(lm.first_name + " " + lm.last_name)
    return render(request, "scanner/schedule.html", {'schedule_table': schedule})

@not_login_required
def checkin (request):
    
    messages = []
    
    if request.method == 'POST':
        form = ScanForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            idnum = data["scan"]
            if len(Person.objects.filter(id=idnum)) != 0:
                person = Person.objects.get(id=idnum)
                checkins = Checkin.objects.filter(person=person, completed=False)
                if len(checkins) == 0:
                    messages.append("Successfully checked in " + person.first_name + " " + person.last_name)
                    new_checkin = Checkin(person=person, checkin=datetime.now(), checkout=datetime.now())
                    new_checkin.save()
                else:
                    for obj in checkins:
                        obj.checkout = datetime.now()
                        obj.completed = True
                        obj.save()
                        person.hours += float((obj.checkout - obj.checkin).total_seconds()) / 3600
                        person.save()
                    messages.append("Successfully checked out " + person.first_name + " " + person.last_name)
        
    form = ScanForm()
    return render(request, "scanner/checkin.html", {"form": form, "messages": messages})

@not_login_required
def scan (request, idnum):
    idnum = int(idnum)
    if idnum < 10000:
        return user(request, idnum)
    if idnum > 10000 and idnum < 20000:
        return checkout_item(request, idnum)
    return render(request, "scanner/item.html", {"idnum": idnum})

@not_login_required
def user (request, idnum):
    if len(Person.objects.filter(id=idnum)) == 0:
        if request.method == 'POST':
            form = NewUserForm(request.POST)
            if form.is_valid():
                person = form.save(commit=False)
                person.id = idnum
                person.save()
        else:
            form = NewUserForm()
            return render(request, "scanner/newuser.html", {"idnum": idnum, "form": form})
    
    person = Person.objects.get(id=idnum)
    messages = []
    
    if request.method == 'POST':
        form = ScanForm(request.POST)
        if form.is_valid():
            if len(CheckoutItem.objects.filter(id=form.cleaned_data["scan"])) > 0:
                item = CheckoutItem.objects.get(id=form.cleaned_data["scan"])
                if len(Checkout.objects.filter(person=person, item=item, checked_in=False)) > 0:
                    for checkout in Checkout.objects.filter(person=person, item=item, checked_in=False):
                        checkout.checked_in = True
                        checkout.date_returned = datetime.now()
                        checkout.save()
                        messages.append(item.name + " successfully checked in.")
                else:
                    new_checkout = Checkout(person=person, item=CheckoutItem.objects.get(id=form.cleaned_data["scan"]), date_checked_out=datetime.now() , date_due=datetime.now() + timedelta(CheckoutItem.objects.get(id=form.cleaned_data["scan"]).default_checkout_time))
                    new_checkout.save()
                    messages.append(item.name + " successfully checked out.")
            else:
                messages.append("That item is not in the database.")
    form = ScanForm()
    return render(request, "scanner/user.html", {"person": person, "form": form, "checkouts": Checkout.objects.filter(person=person, checked_in=False), "messages": messages})

@not_login_required
def checkout_item (request, idnum):
    if len(CheckoutItem.objects.filter(id=idnum)) == 0:
        if request.method == 'POST':
            form = NewItemForm(request.POST)
            if form.is_valid():
                item = form.save(commit=False)
                item.id = idnum
                item.save()
            else:
                form = NewItemForm()
                return render(request, "scanner/newitem.html", {"idnum": idnum, "form": form})
        else:
            form = NewItemForm()
            return render(request, "scanner/newitem.html", {"idnum": idnum, "form": form})
            
    return render(request, "scanner/item.html", {"item": CheckoutItem.objects.get(id=idnum)})

@not_login_required
def checkout(request, personid, itemid):
    return render(request, "scanner/item.html", {"item": CheckoutItem.objects.get(id=itemid)})
    
@login_required
def admin(request):
    person = request.user.leadershipmember
    return render(request, "scanner/admin.html", {"person": person})

@not_login_required
def admin_login(request):
    
    if request.method == 'POST':
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            username = data["id"]
            password = data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("admin"))
    
    form = AdminLoginForm()
        
    return render(request, "scanner/admin_login.html", {"form": form})
    
@login_required
def admin_add_leadership(request):
    if not request.user.leadershipmember.can_add_leadership_members:
        return HttpResponseRedirect(reverse("admin"))
    if request.method == 'POST':
        form = NewLeadershipMemberForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            person = Person.objects.get(id=data["id"])
            
            if len(User.objects.filter(username=data["id"])) == 0:
                print(data["password"])
                user = User.objects.create_user(data["id"], data["email"], data["password"])
                user.save()
            user = User.objects.get(username=data["id"])
            leadershipmember = LeadershipMember(first_name=person.first_name, last_name=person.last_name, id=person.id, hours=person.hours, periods=data["periods"], user=user)
            person.delete()
            leadershipmember.save()
            return HttpResponseRedirect(reverse("admin"))
    
    form = NewLeadershipMemberForm()
    return render(request, "scanner/admin_add_leadership.html", {"form": form})

@login_required
def admin_change_permissions(request):
    if not request.user.leadershipmember.can_change_leadership_permissions:
        return HttpResponseRedirect(reverse("admin"))
    leadershipmembers = LeadershipMember.objects.exclude(id=request.user.leadershipmember.id)
    return render(request, "scanner/admin_change_permissions.html", {'leadershipmembers': leadershipmembers})
  
@login_required  
def admin_change_user_permissions(request, id):
    if not request.user.leadershipmember.can_change_leadership_permissions:
        return HttpResponseRedirect(reverse("admin"))
    if request.method == 'POST':
        form = ChangePermissionsForm(request.POST)
        if form.is_valid():
            print("1")
            if 
            lm = LeadershipMember.objects.get(id=id)
            lm.can_add_leadership_members = data["can_add_leadership_members"]
            lm.can_change_leadership_permissions = data["can_change_leadership_permissions"]
            lm.save()
            return HttpResponseRedirect(reverse("admin change permissions"))
    form = ChangePermissionsForm(i)
    person = request.user.leadershipmember
    return render(request, "scanner/admin_change_user_permissions.html", {"form": form, "person": person, "id": id})
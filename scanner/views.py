from django.shortcuts import render, HttpResponseRedirect
from django.core.urlresolvers import reverse
from .forms import ScanForm, NewUserForm, NewItemForm, AdminLoginForm, NewLeadershipMemberForm, ChangePermissionsForm, LeadershipEditInfoForm, PeriodClassSignupForm
from .models import Person, CheckoutItem, Checkout, Checkin, LeadershipMember, ScheduleDay, Period, PeriodPerson, PeriodClass
from datetime import datetime, timedelta, date, time
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .decorators import not_login_required

# Create your views here.

master_schedule = ["BCDEFG", "CAEDGF", "ABDEFG", "BACEGF", "CABDFG", "ABCDEG", "BACDEF"]
period_times = [time(7, 40), time(8, 46), time(8, 51), time(9, 46)]

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
    schedule = "<table id='schedule'>"
    today = date.today()
    next_five = []
    for i in range(5):
        while today.weekday() >= 5 or ScheduleDay.objects.filter(date=today).count() > 0 and ScheduleDay.objects.get(date=today).day_off:
            today += timedelta(1)
        next_five.append(today)
        today += timedelta(1)
    
    print(next_five)
    
    schedule_days = []
    
    for curr_date in next_five:
        schedule_day = None
        if ScheduleDay.objects.filter(date=curr_date).count() > 0:
            schedule_day = ScheduleDay.objects.get(date=curr_date)
        else:
            done = False
            one_day = timedelta(1)
            today_dt = datetime.combine(curr_date, time())
            today_dt -= one_day
            new_date = today_dt.date()
            days_ellapsed = 0
            day = 0
            while not done:
                if new_date.weekday() < 5 and ScheduleDay.objects.filter(date=new_date).count() == 0:
                    days_ellapsed += 1
                elif new_date.weekday() < 5 and not ScheduleDay.objects.get(date=new_date).day_off:
                    done = True
                    day = (ScheduleDay.objects.get(date=new_date).day + days_ellapsed + 1) % 7
                new_dt = datetime.combine(new_date, time())
                new_dt -= one_day
                new_date = new_dt.date()
            schedule_day = ScheduleDay(date=curr_date, day_off=False, day=day, schedule="")
            schedule_day.save()
        if schedule_day.schedule == "":
            schedule_day.schedule = master_schedule[schedule_day.day]
            schedule_day.save()
            
        if len(schedule_day.period_set.all()) == 0:
            for i in range(len(schedule_day.schedule)):
                period = Period(day=schedule_day, period_number=i, period_letter=schedule_day.schedule[i:i + 1])
                period.save()
                for lm in LeadershipMember.objects.all():
                    if lm.periods.find(schedule_day.schedule[i:i + 1] + str(schedule_day.day)) != -1:
                        period_person = PeriodPerson(period=period, person=lm)
                        period_person.save()
        
        schedule_days.append(schedule_day)
    for day in schedule_days:
        print (str(day.period_set.all()) + " " + str(day.date))
    
    top_row = "<tr id='schedule-title'>"
    other_rows = ["<tr>"]*6
    for day in schedule_days:
        top_row += "<td><p>" + str(day.date.strftime("%A %m/%d")) + "<br>Day " + str(day.day + 1) + "</p></td>"
        for i in range(6):
            period = day.period_set.get(period_number=i)
            other_rows[i] += "<td class='" + period.period_letter + "-period'><a href='" + reverse("schedule period", args=[day.date.month, day.date.day, day.date.year, period.period_letter]) + "'><p class='period-letter'>" + period.period_letter + "</p></a></td>"
    top_row += "</tr>"
    other_rows = [x + "</tr>" for x in other_rows]
    schedule += top_row
    for row in other_rows:
        schedule += row
    schedule += "</table>"
    
    
    return render(request, "scanner/schedule.html", {'schedule_table': schedule})

def schedule_period(request, month, day, year, p):
    sd = ScheduleDay.objects.get(date=date(int(year), int(month), int(day)))
    period = Period.objects.get(day=sd, period_letter=p)
    
    if request.method == 'POST':
        form = ScanForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            idnum = data["scan"]
            if period.individual_spots - period.periodperson_set.all().count() - 10 * period.periodclass_set.all().count() > 0:
                if not Person.objects.filter(id=idnum).exists():
                    return HttpResponseRedirect(reverse("scan", args=[idnum]))
                person = Person.objects.get(id=idnum)
                if not period.periodperson_set.filter(person=person).exists():
                    period_person = PeriodPerson(person=person, period=period)
                    period_person.save()
                else:
                    PeriodPerson.objects.get(person=person, period=period).delete()
    
    
    leadership_members = []
    other_people = []
    for pp in period.periodperson_set.all():
        if LeadershipMember.objects.filter(pk=pp.person.pk).exists():
            leadership_members.append(LeadershipMember.objects.get(pk=pp.person.pk))
        else:
            other_people.append(pp.person)
    
    available_slots = period.individual_spots - period.periodperson_set.all().count() - 10 * period.periodclass_set.all().count()
    form = ScanForm()
    return render(request, "scanner/schedule_period.html", {"period": period, "leadership_members": leadership_members, "other_people": other_people, "available_slots": available_slots, "form": form})

def schedule_period_class(request, month, day, year, p):
    sd = ScheduleDay.objects.get(date=date(int(year), int(month), int(day)))
    period = Period.objects.get(day=sd, period_letter=p)
    
    if request.method == 'POST':
        form = PeriodClassSignupForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if period.individual_spots - period.periodperson_set.all().count() - 10 * period.periodclass_set.all().count() > 10 and not period.periodclass_set.all().exists():
                if not Person.objects.filter(id=data["teacher_id"]).exists():
                    return HttpResponseRedirect(reverse("scan", args=[data["teacher_id"]]))
                teacher = Person.objects.get(id=data["teacher_id"])
                period_class = PeriodClass(period=period, teacher=teacher, students=data["number_of_students"])
                period_class.save()
                return HttpResponseRedirect(reverse("schedule period", args=[month, day, year, p]))
    
    form = PeriodClassSignupForm()
    return render(request, "scanner/schedule_period_class.html", {"period": period, "form": form})

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
    if idnum < 10000 or idnum > 20000:
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
def admin_edit_info(request):
    if request.method == 'POST':
        form = LeadershipEditInfoForm(request.POST, instance=request.user.leadershipmember)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("admin"))
    form = LeadershipEditInfoForm(instance=request.user.leadershipmember)        
    return render(request, "scanner/admin_edit_info.html", {"form": form})
  
@login_required  
def admin_change_user_permissions(request, id):
    if not request.user.leadershipmember.can_change_leadership_permissions:
        return HttpResponseRedirect(reverse("admin"))
    if request.method == 'POST':
        form = ChangePermissionsForm(request.POST)
        if form.is_valid():
            print("1")
            data = form.cleaned_data
            lm = LeadershipMember.objects.get(id=id)
            lm.can_add_leadership_members = data["can_add_leadership_members"]
            lm.can_change_leadership_permissions = data["can_change_leadership_permissions"]
            lm.save()
            return HttpResponseRedirect(reverse("admin change permissions"))
    person = request.user.leadershipmember
    form = ChangePermissionsForm(instance=LeadershipMember.objects.get(id=id))
    return render(request, "scanner/admin_change_user_permissions.html", {"form": form, "person": person, "id": id})
from django.contrib import admin
from .models import Person, CheckoutItem, Checkout, Checkin, LeadershipMember, ScheduleDay, Period, PeriodPerson, PeriodClass
# Register your models here.

admin.site.register(Person)
admin.site.register(CheckoutItem)
admin.site.register(Checkout)
admin.site.register(Checkin)
admin.site.register(LeadershipMember)
admin.site.register(ScheduleDay)
admin.site.register(Period)

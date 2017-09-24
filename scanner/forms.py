from django import forms
from .models import Person, CheckoutItem, LeadershipMember
from django.contrib.auth.models import User

class ScanForm(forms.Form):
    scan = forms.IntegerField(label="Scan a code")
    
class NewUserForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['first_name', 'last_name']
        
class NewItemForm(forms.ModelForm):
    class Meta:
        model = CheckoutItem
        fields = ['name', 'description', 'default_checkout_time']
        
class AdminLoginForm(forms.Form):
    id = forms.IntegerField()
    password = forms.CharField(widget=forms.PasswordInput)
    
class NewLeadershipMemberForm(forms.Form):
    id = forms.IntegerField()
    email = forms.EmailField(widget=forms.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput)
    periods = forms.CharField()
    
class ChangePermissionsForm(forms.ModelForm):
    class Meta:
        model = LeadershipMember
        fields = ['can_add_leadership_members', 'can_change_leadership_permissions']
        
class LeadershipEditInfoForm(forms.ModelForm):
    class Meta:
        model = LeadershipMember
        fields = ["first_name", "last_name", "periods"]
        
class PeriodClassSignupForm(forms.Form):
    teacher_id = forms.IntegerField()
    number_of_students = forms.IntegerField()
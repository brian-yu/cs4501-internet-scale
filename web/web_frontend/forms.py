from django import forms

class RegisterForm(forms.Form):
    first_name = forms.CharField(label='First name', max_length=100, widget=forms.TextInput)
    last_name = forms.CharField(label='Last name', max_length=100, widget=forms.TextInput)
    email = forms.EmailField(label='Email', max_length=100)
    phone_number = forms.CharField(label='Phone (optional)', max_length=17, required=False)
    overview = forms.CharField(label='Overview', widget=forms.Textarea)  
    zip_code = forms.CharField(label='Zipcode', max_length=10, widget=forms.TextInput)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
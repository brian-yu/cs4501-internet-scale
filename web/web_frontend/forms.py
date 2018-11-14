from django import forms


class RegisterForm(forms.Form):
    first_name = forms.CharField(
        label='First name', max_length=100, widget=forms.TextInput)
    last_name = forms.CharField(
        label='Last name', max_length=100, widget=forms.TextInput)
    email = forms.EmailField(label='Email', max_length=100)
    phone_number = forms.CharField(
        label='Phone (optional)', max_length=17, required=False)
    overview = forms.CharField(label='Overview', widget=forms.Textarea, required=False)
    zip_code = forms.CharField(
        label='Zipcode', max_length=10, widget=forms.TextInput)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)


class CreateItemForm(forms.Form):
    CONDITION_CHOICES = (
        ('E', 'Excellent'),
        ('G', 'Good'),
        ('O', 'Okay'),
        ('B', 'Bad')
    )
    title = forms.CharField(label='Title', widget=forms.TextInput)
    price_per_day = forms.DecimalField(
        label='Price per day', widget=forms.TextInput, min_value=0, decimal_places=2)
    condition = forms.ChoiceField(label='Condition', choices=CONDITION_CHOICES)
    max_borrow_days = forms.IntegerField(
        label="Max borrow days", widget=forms.NumberInput)
    description = forms.CharField(label='Description', widget=forms.Textarea)
    # currently_borrowed = forms.BooleanField(
    #     label="Currently Borrowed", widget=forms.NullBooleanSelect)

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Order, Model
from datetime import date


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class DateInput(forms.DateInput):
    input_type = 'date'


class OrderUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields: list = [
            'brand',
            'model',
            'model_year',
            'mileage',
            'choose_date',
            'chain_change_price',
            'oil_and_oil_filter_change_price',
            'air_filter_change_price',
            'brake_fluid_change_price',
            # 'order_status'
        ]
        widgets = {
            'choose_date': DateInput(),
            'chain_change_price': forms.CheckboxInput,
            'oil_and_oil_filter_change_price': forms.CheckboxInput,
            'air_filter_change_price': forms.CheckboxInput,
            'brake_fluid_change_price': forms.CheckboxInput,
        }

    def __init__(self, *args, **kwargs):
        super(OrderUpdateForm, self).__init__(*args, **kwargs)
        self.fields['brand'].disabled = True
        self.fields['model'].disabled = True
        self.fields['model_year'].disabled = True

    # this function will be used for the validation
    def clean(self):

        # data from the form is fetched using super function
        super(OrderUpdateForm, self).clean()
        # extract the username and text field from the data
        input_last_supported_year = self.cleaned_data.get('model_year')

        # conditions to be met for the username length
        if input_last_supported_year < 1991:
            self._errors['model_year'] = self.error_class([
                'That year is not available'])

        return self.cleaned_data


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields: list = [
            'brand',
            'model',
            'model_year',
            'mileage',
            'choose_date',
            'chain_change_price',
            'oil_and_oil_filter_change_price',
            'air_filter_change_price',
            'brake_fluid_change_price',
        ]
        widgets = {
            'choose_date': DateInput(),
            'chain_change_price': forms.CheckboxInput,
            'oil_and_oil_filter_change_price': forms.CheckboxInput,
            'air_filter_change_price': forms.CheckboxInput,
            'brake_fluid_change_price': forms.CheckboxInput,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['model'].queryset = Model.objects.none()

        if 'brand' in self.data:
            try:
                brand_id = int(self.data.get('brand'))
                self.fields['model'].queryset = Model.objects.filter(brand_id=brand_id)
            except(ValueError, TypeError):
                pass
        elif self.instance.pk:
            pass
            self.fields['model'].queryset = self.instance.brand.brand_set.order_by('name')

    # this function will be used for the validation
    def clean(self):

        # data from the form is fetched using super function
        super(OrderForm, self).clean()

        # extract the username and text field from the data
        input_last_supported_year = self.cleaned_data.get('model_year')

        # conditions to be met for the username length
        if input_last_supported_year < 1991:
            self._errors['model_year'] = self.error_class([
                'That year is not available'])
        # if len(text) <10:
        #     self._errors['text'] = self.error_class([
        #         'Post Should Contain a minimum of 10 characters'])

        # return any errors if found
        return self.cleaned_data


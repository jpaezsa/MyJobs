from django.forms import *
from myjobs.forms import BaseUserForm
from myprofile.models import *


def generate_custom_widgets(model):
    """
    Generates custom widgets and sets placeholder values and class names based
    on field type

    Inputs:
    :model:       model class from form Meta
    
    Outputs:
    :widgets:     dictionary of widgets with custom attributes defined
    """
    fields = model._meta.fields
    widgets = {}
    
    for field in fields:
        internal_type = field.get_internal_type()
        # exclude profile unit base fields
        if field.model == model:
            attrs = {}
            attrs['id'] = 'id_' + model.__name__.lower() + '-' + field.attname
            attrs['placeholder'] = field.verbose_name.title()
            if field.choices:
                widgets[field.attname] = Select(attrs=attrs)
            elif internal_type == 'BooleanField':
                attrs['label_class'] = 'checkbox'
                widgets[field.attname] = CheckboxInput(attrs=attrs)
            else:
                widgets[field.attname] = TextInput(attrs=attrs)

    return widgets


class NameForm(BaseUserForm):
    class Meta:
        # form_name is used in the templates to render the form header
        form_name = "Personal Information"
        model = Name
        widgets = generate_custom_widgets(model)
        

class InitialNameForm(NameForm):
    primary = BooleanField(widget=HiddenInput(), required=False, initial="off")


class SecondaryEmailForm(BaseUserForm):
    class Meta:
        form_name = "Secondary Email"
        model = SecondaryEmail
        widgets = generate_custom_widgets(model)


class EducationForm(BaseUserForm):
    class Meta:
        form_name = "Education"
        model = Education
        widgets = generate_custom_widgets(model)        
        

class EmploymentForm(BaseUserForm):
    class Meta:
        form_name = "Most Recent Work History"
        model = EmploymentHistory
        widgets = generate_custom_widgets(model)

       
class PhoneForm(BaseUserForm):
    class Meta:
        form_name = "Phone Number"
        model = Telephone
        widgets = generate_custom_widgets(model)
        widgets['country_dialing'].attrs['class'] = "phoneCountryCode"
        widgets['area_dialing'].attrs['class'] = "phoneAreaCode"
        widgets['number'].attrs['class'] = "phoneNumber"
        widgets['extension'].attrs['class'] = "phoneExtension"
        widgets['country_dialing'].attrs['placeholder'] = "+1"
        widgets['area_dialing'].attrs['placeholder'] = "555"
        widgets['number'].attrs['placeholder'] = "555-5555"
        widgets['extension'].attrs['placeholder'] = "x1234"


class AddressForm(BaseUserForm):
    class Meta:
        form_name = "Address"
        model = Address
        widgets = generate_custom_widgets(model)

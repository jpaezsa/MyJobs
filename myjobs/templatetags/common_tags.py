from django import template

from myjobs import version
from myprofile.models import ProfileUnits
from myjobs.models import User
from mydashboard.models import CompanyUser
from django.db.models.loading import get_model

register=template.Library()

@register.simple_tag
def cache_buster():
    cache_buster = "?v=%s" % version.cache_buster
    return cache_buster

@register.simple_tag
def get_description(module):
    """
    Gets the description for a module.

    inputs:
    :module: The module to get the description for.
    
    outputs:
    The description for the module, or an empty string if the module or the
    description doesn't exist.
    """
    
    try:
        model = get_model("myprofile", module)
        return model.description if model.description else ""
    except Exception:
        return ""


@register.filter
def get_name_obj(user, default=""):
    """
    Retrieve the given user's primary name (if one exists) or a default value

    Inputs:
    :user: User instance
    :default: Return this if no name exists

    Outputs:
    :name: Name instance or :default:
    """
    try:
        name = user.profileunits_set.get(content_type__name="name",
                                         name__primary=True).name
        if not name.get_full_name():
            name = default
    except ProfileUnits.DoesNotExist:
        name = default
    return name

@register.assignment_tag
def is_a_group_member(user, group):
    """ 
    Determines whether or not the user is a member of a group

    Inputs:
    :user: User instance
    :group: String of group being checked for

    Outputs:
    Boolean value indicating whether or not the user is a member of the requested group
    """

    try:
        return User.objects.is_group_member(user, group)
    except ValueError:
        return False

@register.assignment_tag
def get_company_name(user):
    """
    Gets the name of companies associated with a user

    Inputs:
    :user: User instance

    Outputs:
    :company_list: A list of company names, or an empty string if there are no companies associated with the user
    """

    try:
        company_list = {}
        companies = CompanyUser.objects.filter(user=user)
        for i, company in enumerate(companies):
            company_list[i] = company.company
        return company_list
    except CompanyUser.DoesNotExist:
        return {}

import json
import logging
import re

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse
from django.forms.models import model_to_dict
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.views.generic import TemplateView

from myjobs.decorators import user_is_allowed
from myjobs.models import User
from myjobs.forms import *
from myjobs.helpers import *
from myprofile.forms import *
from myprofile.models import ProfileUnits
from registration.forms import *


@user_is_allowed(ProfileUnits)
@user_passes_test(User.objects.not_disabled)
def edit_profile(request):
    """
    Main profile view that the user first sees. Ultimately generates the
    following in data_dict:

    :profile_config: A list of dictionaries. Each dictionary represents a
                     different module (based on module_list) with the keys:
                     verbose - the displayable title of the module
                     name - the module name as it's named in the models.
                     items - all the instances in that module for the user
    """

    settings = {'user': request.user}
    module_list = ['Name', 'Education', 'EmploymentHistory', 'SecondaryEmail',
                   'Telephone', 'Address', 'MilitaryService']
    units = request.user.profileunits_set
    profile_config = []

    for module in module_list:
        model = globals()[module]
        verbose = model._meta.verbose_name

        x = []
        module_config = {}
        module_units = units.filter(content_type__name=verbose)

        module_config['verbose'] = verbose.title()
        module_config['name'] = module
        for unit in module_units:
            if hasattr(unit, module.lower()):
                x.append(getattr(unit, module.lower()))
        module_config['items'] = x

        profile_config.append(module_config)

    data_dict = {'profile_config': profile_config,
                 'view_name': 'My Profile'}

    return render_to_response('myprofile/edit_profile.html', data_dict,
                              RequestContext(request))


@user_is_allowed(ProfileUnits)
@user_passes_test(User.objects.not_disabled)
def handle_form(request):
    item_id = request.REQUEST.get('id', 'new')
    module = request.REQUEST.get('module')

    item = None
    if item_id != 'new':
        try:
            item = request.user.profileunits_set.get(pk=item_id)
            item = getattr(item, module.lower())
        except ProfileUnits.DoesNotExist:
            # User is trying to access a nonexistent PU
            # or a PU that belongs to someone else
            raise Http404

    item_class = item.__class__

    try:
        form = globals()[module + 'Form']
    except KeyError:
        # Someone must have manipulated request data?
        raise Http404

    data_dict = {'view_name': 'My Profile',
                 'item_id': item_id,
                 'module': module}

    if request.method == 'POST':
        if request.POST.get('action') == 'updateEmail':
            activation = ActivationProfile.objects.get_or_create(user=request.user,
                                                                 email=item.email)[0]
            activation.send_activation_email(primary=False)
            return HttpResponse('success')

        if item_id == 'new':
            form_instance = form(user=request.user, data=request.POST,
                                 auto_id=False)
        else:
            form_instance = form(user=request.user, instance=item,
                                 auto_id=False, data=request.POST)
        model = form_instance._meta.model
        data_dict['form'] = form_instance
        data_dict['verbose'] = model._meta.verbose_name.title()
        if form_instance.is_valid():
            form_instance.save()
            if request.is_ajax():
                return HttpResponse(status=200)
            else:
                return HttpResponseRedirect(reverse('view_profile',
                                                    args=[request.user.email]))
        else:
            if request.is_ajax():
                return HttpResponse(json.dumps(form_instance.errors))
            else:
                return render_to_response('myprofile/profile_form.html',
                                          data_dict,
                                          RequestContext(request))
    else:
        if item_id == 'new':
            form_instance = form(user=request.user, auto_id=False)
        else:
            form_instance = form(instance=item, auto_id=False)
            if data_dict['module'] == 'SecondaryEmail':
                data_dict['verified'] = item.verified
        model = form_instance._meta.model
        data_dict['form'] = form_instance
        data_dict['verbose'] = model._meta.verbose_name.title()
        return render_to_response('myprofile/profile_form.html',
                                  data_dict,
                                  RequestContext(request))


@user_is_allowed(ProfileUnits, 'item_id')
@user_passes_test(User.objects.not_disabled)
def delete_item(request, item_id):
    try:
        request.user.profileunits_set.get(id=item_id).delete()
    except ProfileUnits.DoesNotExist:
        pass
    return HttpResponseRedirect(reverse('view_profile',
                                        args=[request.user.email]))


@user_is_allowed(ProfileUnits)
@user_passes_test(User.objects.not_disabled)
def get_details(request):
    module_config = {}
    item_id = request.GET.get('id')
    module = request.GET.get('module')
    item = get_object_or_404(request.user.profileunits_set,
                             pk=item_id)
    item = getattr(item, module.lower())
    model = item.__class__
    module_config['verbose'] = model._meta.verbose_name.title()
    module_config['name'] = module
    module_config['item'] = item
    data_dict = {'module': module_config}
    data_dict['view_name'] = 'My Profile'
    return render_to_response('myprofile/profile_details.html',
                              data_dict, RequestContext(request))

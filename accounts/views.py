from django.shortcuts import render
from django.http import HttpResponse
from .forms import UserRegister
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .utils import role_required


class UserResgisterView(generic.CreateView):
    form_class = UserRegister
    template_name = "registration/register.html"
    success_url =  reverse_lazy('login')



# @login_required
# @role_required('ICT')
# def ict_dashboard(request):
#     return render(request, "ict_dashboard.html")

# @login_required
# @role_required('HOD')
# def hod_dashboard(request):
#     return render(request, "hod_dashboard.html")

# @login_required
# @role_required('COUNCILOR')
# def councilor_dashboard(request):
#     return render(request, "councilor_dashboard.html")


# @login_required
# @role_required('CHAIRMAN')
# def councilor_dashboard(request):
#     return render(request, "chairman_dashboard.html")

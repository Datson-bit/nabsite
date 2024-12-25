from django.shortcuts import render
from django.http import HttpResponse
from .forms import UserRegister
from django.views import generic
from django.urls import reverse_lazy


class UserResgisterView(generic.CreateView):
    form_class = UserRegister
    template_name = "registration/register.html"
    success_url =  reverse_lazy('login')
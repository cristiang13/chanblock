from django.shortcuts import render,redirect
from utils import assetsUtil,userUtil
from django.http import JsonResponse



def home(request):
    return render(request, 'home_es.html')

def home_es(request):
    return render(request, 'home_es.html')
def analysis(request):
    return render(request, 'about/analysis.html')

def regulation(request):
    return render(request, 'about/regulation.html')

def education(request):
    return render(request, 'about/education.html')

def monitoring(request):
    return render(request, 'about/monitoring.html')


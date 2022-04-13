from django.shortcuts import render
from django.http import HttpResponse
from math import ceil
# Create your views here.

def index(Request):
	return render(Request,'index.html')
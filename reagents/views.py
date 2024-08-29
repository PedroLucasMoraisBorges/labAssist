from django.shortcuts import render
from django.views import View

# Create your views here.

class LandingPage(View):
    def get(self, request):
        return render(request, 'landingPage.html')
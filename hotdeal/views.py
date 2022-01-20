from django.shortcuts import render
from .models import Deal
from rest_framework import viewsets
from .serializers import DealSerializers

# Create your views here.
def index(request):
    deals = Deal.objects.all()
    return render(request, 'index.html', {'deals': deals})

class DetailViewSet(viewsets.ModelViewSet):
    queryset = Deal.objects.all()
    serializer_class = DealSerializers
from django.shortcuts import render

def adminsite(request):
    return render(request, 'admin/admin.html')
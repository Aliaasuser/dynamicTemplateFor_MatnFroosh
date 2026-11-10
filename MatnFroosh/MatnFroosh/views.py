from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

def test(request: HttpRequest):
    return render(request, 'test/test.html')
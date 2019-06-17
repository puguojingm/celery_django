from django.shortcuts import render
from django.http import JsonResponse
from .tasks import add,mul,xsum


def app1_view(request):
    print("start app1_view")

    add.delay(2,3)

    print("end app1_view")


    return JsonResponse({'reuslt':'ok'})
from django.shortcuts import render
from django.http import JsonResponse
from .tasks import add,mul,xsum


def app1_add_view(request):
    print("start app1_view")

    add.delay(2,3)
    # add.apply_async(2,3,queue='add')

    print("end app1_view")


    return JsonResponse({'reuslt':'add ok'})



def app1_mul_view(request):
    print("start app1_view")

    mul.delay(2,3)
    # add.apply_async(2,3,queue='add')

    print("end app1_view")


    return JsonResponse({'reuslt':'mul ok'})

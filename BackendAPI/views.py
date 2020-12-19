from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from FgsmAttack import newFgsm
from OnePixelAttack import onePixelAttack
from CWAttack import newCWAttack
from BIAttack import basicIterative
# Create your views here.


def index(request):
    return render(request, "index.html")


def fetchFGSMAttack(request):
    try:
        image_name = request.GET.get("image_name")
        epsilon_value = request.GET.get("epsilon_value")
        epsilon_value = int(epsilon_value)*255//100
        classes = newFgsm.fgsmAttack(image_name, epsilon_value)
        if classes:
            return JsonResponse({"status": "found",  "message": "Results obtained", "classes": classes})
        return JsonResponse({"status": "not found",  "message": "Can't classify", "classes": []})
    except:
        return JsonResponse({"status": "error", "message": "Some error occured", "classes": []})


def fetchCWAttack(request):
    try:
        image_name = request.GET.get("image_name")
        epsilon_value = request.GET.get("epsilon_value")
        classes = newCWAttack.cwAttack(image_name, int(epsilon_value))
        if classes:
            return JsonResponse({"status": "found",  "message": "Results obtained", "classes": classes})
        return JsonResponse({"status": "not found",  "message": "Can't classify", "classes": ""})
    except:
        return JsonResponse({"status": "error", "message": "Some error occured", "classes": ""})


def fetchOnePixelAttackPredict(request):
    try:
        image_name = request.GET.get("image_name")
        classes = onePixelAttack.onePixelAttackUtil1(image_name)
        print(classes)
        if classes:
            return JsonResponse({"status": "found",  "message": "Results obtained", "classes": classes[0], "percent": classes[1]*100})
        return JsonResponse({"status": "not found",  "message": "Can't classify", "classes": "", "percent": 0})
    except:
        return JsonResponse({"status": "error", "message": "Some error occured", "classes": "", "percent": 0})


def fetchOnePixelAttack(request):
    try:
        image_name = request.GET.get("image_name")
        epsilon_value = request.GET.get("epsilon_value")
        epsilon_value = 100-int(epsilon_value)
        classes = onePixelAttack.onePixelAttackUtil2(image_name, epsilon_value)
        print(classes)
        if classes:
            return JsonResponse({"status": "found",  "message": "Results obtained", "classes": classes[0], "percent": classes[1]*100})
        return JsonResponse({"status": "not found",  "message": "Can't classify", "classes": "", "percent": 0})
    except:
        return JsonResponse({"status": "error", "message": "Some error occured", "classes": "", "percent": 0})


def fetchBIAttack(request):
    try:
        image_name = request.GET.get("image_name")
        epsilon_value = request.GET.get("epsilon_value")
        iteration_count = request.GET.get("iteration_count")
        classes = basicIterative.iterativeAttack(
            image_name, int(epsilon_value), int(iteration_count))
        if classes:
            if(epsilon_value == "0" and iteration_count == "0"):
                return JsonResponse({"status": "found",  "message": "Results obtained", "classes": classes[0]})
            else:
                return JsonResponse({"status": "found",  "message": "Results obtained", "classes": classes[1]})
        return JsonResponse({"status": "not found",  "message": "Can't classify", "classes": ""})
    except:
        return JsonResponse({"status": "error", "message": "Some error occured", "classes": ""})


def test(request):

    # names = ["bear.jpg", "bird1.jpg", "blackrhino.jpg", "bmwcar.jpg", "chevroletcar.jpg", "cobra.jpg", "elephant.jpg", "elephant2.jpg", "goldfish.jpg", "house.jpg",
    #          "house2.jpg", "lebanonsnake.jpg", "lion1.jpg", "lion2.jpg", "panda.jpg", "panda2.jpg", "panda3.jpg", "parrot.jpg", "stopsign.jpg", "stopsign2.jpg", "whitebear.jpg"]

    return JsonResponse({"Status": "Active"})

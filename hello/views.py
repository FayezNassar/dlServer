from django.shortcuts import render
from django.http import HttpResponse
import numpy as np
import json
import sys

from .models import Greeting
from . import MLP


def index(request):
    return HttpResponse("<h2>Hello Deep learning server!</h2>")


def request_work(request):
    mode = "validation" if (MLP.image_file_index == 45) else "train"
    print(type(MLP.l1_W,))
    data = {
        "image_file_index": MLP.image_file_index,
        'mode': mode,
        'l1_w': MLP.l1_W.tolist(),
        'l2_w': MLP.l2_W.tolist(),
    }
    MLP.image_file_index = (MLP.image_file_index % 45) + 1
    return HttpResponse(json.dumps(data))


def response_result(request):
    request_message = request.read().decode('utf-8')
    work_time = json.loads(request_message)['work_time']
    print(str(work_time))
    return HttpResponse('responseResult')


def db(request):
    greeting = Greeting()
    greeting.save()
    greetings = Greeting.objects.all()
    return render(request, 'db.html', {'greetings': greetings})

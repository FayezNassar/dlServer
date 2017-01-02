from django.shortcuts import render
from django.http import HttpResponse
import json

from .models import Greeting
from .models import TimeStatistic
from .models import AccuracyStatistic
from . import MLP


def index(request):
    return HttpResponse("<h2>Hello Deep learning server!</h2>")


def join_system(request):
    if request.method == 'POST':
        client_id = MLP.max_client_id
        MLP.max_client_id += 1
        time_statistic = TimeStatistic(device_id=client_id, mini_patch_times=0, total_time=0.0)
        try:
            time_statistic.save()
        except Exception as inst:
            print(type(inst))
            print(inst.args)
            print(inst)
        return HttpResponse(client_id)


def deep_learning(request):
    if request.method == 'GET':
        mode = "validation" if (MLP.image_file_index == 2) else "train"
        data = {
            'image_file_index': MLP.image_file_index,
            'mode': mode,
            'l1_w': MLP.linNeuralNetwork_l1.W.data.tolist(),
            'l2_w': MLP.linNeuralNetwork_l2.W.data.tolist(),
            'epoch_number': MLP.epoch_number,
        }
        MLP.image_file_index = (MLP.image_file_index % 50) + 1
        if MLP.image_file_index == 50:
            MLP.epoch_number += 1
            accuracy_statistic = AccuracyStatistic(epoch_number=MLP.epoch_number, accuracy=0.0,
                                                   number_of_validate_post=0)
            accuracy_statistic.save()
        return HttpResponse(json.dumps(data))

    elif request.method == 'POST':
        request_message = request.read().decode('utf-8')
        mode = str(json.loads(request_message)['mode'])
        if mode == 'train':
            # collect the date that client sent, and update the relevant
            # update the time statistic
            client_id = json.loads(request_message)['id']
            work_time = json.loads(request_message)['work_time']
            time_statistic = TimeStatistic.objects.get(device_id=client_id)
            time_statistic = TimeStatistic(device_id=time_statistic.device_id,
                                           mini_patch_times=time_statistic.mini_patch_times + 1,
                                           total_time=time_statistic.total_time + work_time)
            time_statistic.save()

            # update the network
            l1_delta_list = json.loads(request_message)['l1_delta']
            l2_delta_list = json.loads(request_message)['l2_delta']
            for i in range(300):
                for j in range(784):
                    MLP.linNeuralNetwork_l1.W.data[i][j] += (l1_delta_list[i][j] * 0.1)  # 0.1 is the learning rate.
            for i in range(10):
                for j in range(300):
                    MLP.linNeuralNetwork_l2.W.data[i][j] += (l2_delta_list[i][j] * 0.1)  # 0.1 is the learning rate.

        elif mode == 'validation':
            accuracy = json.loads(request_message)['accuracy']
            epoch_number = json.loads(request_message)['epoch_number']
            accuracy_statistic = AccuracyStatistic.objects.get(epoch_number=epoch_number)
            accuracy_statistic = AccuracyStatistic(epoch_number=epoch_number,
                                                   accuracy=accuracy_statistic.accuracy+(accuracy/5),
                                                   number_of_validate_post=accuracy_statistic.number_of_validate_post+1)
            accuracy_statistic.save()


def db(request):
    greeting = Greeting()
    greeting.save()
    greetings = Greeting.objects.all()
    return render(request, 'db.html', {'greetings': greetings})

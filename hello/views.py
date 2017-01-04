from django.shortcuts import render
from django.http import HttpResponse
import json

from .models import Greeting
from .models import TimeStatistic
from .models import AccuracyStatistic
from .models import MaxClientID
from . import MLP


def index(request):
    return HttpResponse("<h2>Hello Deep learning server!</h2>")


def join_system(request):
    if request.method == 'POST':
        print("got post request")
        try:
            flag = MaxClientID.objects.filter(max_id_str='MAX').exists()
        except Exception as inst:
            print(type(inst))
            print(inst.args)
            print(inst)
        if MaxClientID.objects.filter(max_id_str='MAX').exists():
            print('MaxClientId is empty')
            max_client_id = MaxClientID.objects.get(max_id_str='MAX')
            print('create new MaxClient')
        else:
            print('MaxClientId is not empty')
            max_client_id = MaxClientID(max_id_str='MAX', max_id=1)
            print('got the MaxClient')
        client_id = max_client_id.max_id
        max_client_id = MaxClientID(max_id_str='MAX', max_id = client_id + 1)
        print('before save')
        max_client_id.save()
        print('after save')
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
        print('deep_learning/GET')
        if MLP.image_file_index <= 45:
            mode = 'train'
        else:
            if MLP.number_of_response_per_epoch > 45:
                mode = 'validation'
            else:
                mode = 'wait'
        print('the mode is: ' + mode)
        if mode != 'wait':
            if MLP.image_file_index == 1:
                MLP.epoch_number += 1
        data = {
            'image_file_index': MLP.image_file_index,
            'mode': mode,
            'l1_w': MLP.linNeuralNetwork_l1.W.data.tolist(),
            'l2_w': MLP.linNeuralNetwork_l2.W.data.tolist(),
            'epoch_number': MLP.epoch_number,
        }
        if mode != 'wait':
            MLP.image_file_index = (MLP.image_file_index % 50) + 1
            # in the case the epoch done, reset the number_of_response_per_epoch to start a new repoch
            if MLP.image_file_index == 50:
                MLP.number_of_response_per_epoch = 0
        return HttpResponse(json.dumps(data))

    elif request.method == 'POST':
        request_message = request.read().decode('utf-8')
        mode = str(json.loads(request_message)['mode'])
        if mode == 'train':
            MLP.number_of_response_per_epoch += 1
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
            if AccuracyStatistic.objects.filter(epoch_number=epoch_number).exists():
                accuracy_statistic = AccuracyStatistic.objects.get(epoch_number=epoch_number)
                accuracy_statistic = AccuracyStatistic(epoch_number=epoch_number,
                                                       accuracy=accuracy_statistic.accuracy + (accuracy / 5),
                                                       number_of_validate_post=accuracy_statistic.number_of_validate_post + 1)
            else:
                accuracy_statistic = AccuracyStatistic(epoch_number=epoch_number,
                                                       accuracy=(accuracy / 5),
                                                       number_of_validate_post=1)
            accuracy_statistic.save()
            print("epoch_number: " + str(accuracy_statistic.epoch_number))
            print("accuracy: " + str(accuracy_statistic.accuracy))
            print("number_of_validate_post: " + str(accuracy_statistic.number_of_validate_post))
            accuracy_statistic = AccuracyStatistic(epoch_number=epoch_number,
                                                   accuracy=accuracy_statistic.accuracy+(accuracy/5),
                                                   number_of_validate_post=accuracy_statistic.number_of_validate_post+1)
            accuracy_statistic.save()
        return HttpResponse("<h2>Hello Deep learning server!</h2>")


def db(request):
    greeting = Greeting()
    greeting.save()
    greetings = Greeting.objects.all()
    return render(request, 'db.html', {'greetings': greetings})

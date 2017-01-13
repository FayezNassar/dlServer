from django.shortcuts import render
from django.http import HttpResponse
import json
from .models import Greeting
import chainer.links as L
from pymongo import MongoClient
import time


def index(request):
    return HttpResponse("<h2>Hello Deep learning server!</h2>")


def join_system(request):
    # make connection and get he relevant database
    client = MongoClient('mongodb://Fayez:Fayez93@ds157158.mlab.com:57158/primre')
    _db = client.primre
    if request.method == 'POST':
        if _db.IDs.find().count() == 0:
            new_id = 1
            _db.IDs.insert_one({'max_id': 2})
        else:
            new_id = _db.IDs.find_one_and_update({}, {'$inc': {'max_id': 1}})['max_id']
        _db.TimeStatistic.insert_one({'device_id': new_id, 'mini_patch_times': 1, 'total_time': 0.0})
        if new_id == 1:
            # init the system
            lin_neural_network_l1 = L.Linear(784, 300)
            lin_neural_network_l2 = L.Linear(300, 10)
            l1_list = lin_neural_network_l1.W.data.tolist()
            l2_list = lin_neural_network_l2.W.data.tolist()
            _db.GlobalParameters.insert_one({'id': 1, 'image_file_index': 1, 'number_of_response_per_epoch': 0,
                                             'epoch_number': 0, 'l1_list': l1_list, 'l2_list': l2_list, 'list_busy': 0})
        return HttpResponse(new_id)
    if request.method == 'GET':
        return HttpResponse('Hello From joinSystem Request')


def deep_learning(request):
    # make connection and get he relevant database
    client = MongoClient('mongodb://Fayez:Fayez93@ds157158.mlab.com:57158/primre')
    _db = client.primre
    print('deep_learning')
    image_file_index = 1
    if request.method == 'GET':
        if _db.GlobalParameters.find_one({'id': 1})['epoch_number'] == 12:
            mode = 'stop'
        elif _db.GlobalParameters.find_one({'id': 1})['epoch_number'] == 11:
            print('mode is test')
            mode = 'test'
        else:
            if _db.GlobalParameters.find_one({'id': 1})['image_file_index'] <= 1:
                print('mode is train')
                mode = 'train'
            else:
                if _db.GlobalParameters.find_one({'id': 1})['number_of_response_per_epoch'] >= 1:
                    mode = 'validation'
                    print('mode is validation')
                else:
                    print('mode is wait')
                    mode = 'wait'
        if mode != 'wait':
            new_image_file_index = (_db.GlobalParameters.find_one({'id': 1})['image_file_index'] % 50) + 1
            image_file_index = _db.GlobalParameters.find_one({'id': 1})['image_file_index']
            _db.GlobalParameters.update({'id': 1}, {'$set': {'image_file_index': new_image_file_index}})
            if image_file_index == 1:
                _db.GlobalParameters.update({'id': 1},
                                            {'$inc': {'epoch_number': 1}, '$set': {'number_of_response_per_epoch': 0}})
                _db.AccuracyStatistic.insert_one(
                    {'epoch_number': _db.GlobalParameters.find_one({'id': 1})['epoch_number'], 'accuracy': 0,
                     'number_of_validate_post': 0, 'start_time': time.time(), 'end_time': 0})
            print('image_file_index: ' + str(image_file_index))
            print('new_image_file_index: ' + str(new_image_file_index))
        data = {
            'image_file_index': image_file_index,
            'mode': mode,
            'epoch_number': _db.GlobalParameters.find_one({'id': 1})['epoch_number'],
        }
        return HttpResponse(json.dumps(data))

    elif request.method == 'POST':
        _db.GlobalParameters.update({'id': 1}, {'$inc': {'number_of_response_per_epoch': 1}})
        request_message = request.read().decode('utf-8')
        mode = str(json.loads(request_message)['mode'])
        if mode == 'train':
            # collect the date that client sent, and update the relevant
            # update the time statistic
            client_id = json.loads(request_message)['id']
            work_time = json.loads(request_message)['work_time']
            _db.TimeStatistic.update({'device_id': client_id},
                                     {'$inc': {'mini_patch_times': 1, 'total_time': work_time}})
        elif mode == 'validation':
            print('validation post')
            accuracy = json.loads(request_message)['accuracy']
            epoch_number = json.loads(request_message)['epoch_number']
            if _db.AccuracyStatistic.find({'epoch_number': epoch_number})['number_of_validate_post'] < 5:
                print('number of validate post < 5')
                _db.AccuracyStatistic.update({'epoch_number': epoch_number},
                                             {'$inc': {'accuracy': (accuracy / 5), 'number_of_validate_post': 1}})
            if _db.GlobalParameters.find_one({'id': 1})['number_of_response_per_epoch'] == 50:
                _db.AccuracyStatistic.update(
                    {'epoch_number': epoch_number}, {'$inc': {'end_time': time.time()}})

        elif mode == 'test':
            accuracy = json.loads(request_message)['accuracy']
            if _db.TestAccuracy.find({'id': 1}).count() == 1:
                _db.TestAccuracy.update({'id': 1}, {'$inc': {'accuracy': (accuracy / 50)}})
            else:
                _db.TestAccuracy.insert_one({'id': 1, 'accuracy': (accuracy / 50)})

        return HttpResponse("<h2>Hello Deep learning server!</h2>")


def db(request):
    greeting = Greeting()
    greeting.save()
    greetings = Greeting.objects.all()
    return render(request, 'db.html', {'greetings': greetings})

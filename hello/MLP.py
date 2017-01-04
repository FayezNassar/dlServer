import chainer.links as L
from . import models
# define the initial network
linNeuralNetwork_l1 = L.Linear(784, 300)
linNeuralNetwork_l2 = L.Linear(300, 10)

# witch file is next to train on.
image_file_index = 1
# max_client_id = 1
epoch_number = 0

# to extinguish between different epochs.
number_of_response_per_epoch = 0

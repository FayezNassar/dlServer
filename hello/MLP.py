import chainer.links as L

# define the initial network
linNeuralNetwork_l1 = L.Linear(784, 300)
linNeuralNetwork_l2 = L.Linear(300, 10)

# witch file is next to train on.
image_file_index = 1
max_client_id = 1

import chainer.links as L

# define the initial network
linNeuralNetwork_l1 = L.Linear(784, 300)
linNeuralNetwork_l2 = L.Linear(300, 10)

# define global W's matrix
l1_W = linNeuralNetwork_l1.W.data
l2_W = linNeuralNetwork_l2.W.data

# witch file is next to train on.
image_file_index = 1;

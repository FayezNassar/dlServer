import socket

import chainer
import chainer.functions as F
import chainer.links as L
from chainer import training
from chainer.training import extensions


class MultiLayerPerceptron(chainer.Chain):
    # define  network with three layers, input size is n_units(picture size), output size is 10(digits number)
    def __init__(self, n_in, n_hidden, n_out):
        super(MultiLayerPerceptron, self).__init__(
            l1=L.Linear(n_in, n_in),  # n_in -> n_units
            l2=L.Linear(n_hidden, n_hidden),  # n_units -> n_units' must be 300 neorons.
            l3=L.Linear(n_hidden, n_out)  # n_units -> n_out
        )

    def __call__(self, x):
        h1 = F.relu(self.l1(x))
        h2 = F.relu(self.l2(h1))
        return self.l3(h2)

def first_connection():
    print "Hello world"
    s = socket.socket()
    host = socket.gethostname()
    port = 12345
    s.bind((host, port))
    s.listen(5)
    while True:
        c, addr = s.accept()
        print 'Got connection from', addr
        c.send('Thank you for connecting')
        c.close(s)
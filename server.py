import socket

import os
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


def first_connection(application):
    print "Hello world"
    s = socket.socket()
    host = socket.gethostname()
    port = int(os.environ.get("PORT", 5000))
    print "host is: " + str(host) + ", port number is:" + str(port)
    s.bind((host, port))
    s.listen(5)
    print "After the bind"
    while True:
        print "inside the loop"
        c, addr = s.accept()
        print 'Got connection from', addr
        c.send('Thank you for connecting')
    c.close()
    return application


if __name__ == "__main__":
    print "mr7baaaaaaaaaa"
    first_connection()

import mnist_load_show as mnist

X, y = mnist.read_mnist_training_data()

XTrain = X[0:30000]
XTest  = X[30000:60000]

yTrain = y[0:30000]
yTest  = y[30000:60000]


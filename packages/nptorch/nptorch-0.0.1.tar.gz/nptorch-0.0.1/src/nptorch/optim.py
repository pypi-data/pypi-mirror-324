from . import core


class SGD():
    def step(self, params, lr, wd=None):
        self.params = list(params)
        self.lr = lr

    def __call__(self):
        for param in self.params:
            param.data -=  self.lr * param.grad


class Momentum():
    def step(self, params, lr, wd=None):
        self.params = list(params)
        self.lr = lr
        self.mu = 0.9
        self.v = [core.zeros_like(param) for param in params]

    def __call__(self):
        for i, param in enumerate(self.params):
            self.v[i][:] = self.mu * self.v[i] - self.lr * (param.grad  + 5e-4 * param.data)
            param.data +=  self.v[i]


class Adam():
    def __init__(self, params, lr, wd=None):
        self.params = list(params)
        self.lr = lr
        self.eps = 1.0e-8
        self.beta1 = 0.9
        self.beta2 = 0.999
        self.t = 0
        self.m = [core.zeros_like(param) for param in params]
        self.v = [core.zeros_like(param) for param in params]

    def step(self):
        self.t += 1
        for i, param in enumerate(self.params):
            self.m[i][:] = self.beta1*self.m[i] + (1-self.beta1)*param.grad
            mt = self.m[i] / (1-self.beta1**self.t)
            self.v[i][:] = self.beta2*self.v[i] + (1-self.beta2)*(param.grad**2)
            vt = self.v[i] / (1-self.beta2**self.t)
            param.data -=  self.lr * mt / (core.sqrt(vt) + self.eps)


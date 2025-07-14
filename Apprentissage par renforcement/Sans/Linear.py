import numpy as np

lr = 0.1
dropout = 0.1

class Linear:
    def __init__(self, in_features, out_features, bias=True, lr=lr, dropout_rate=dropout, gradient_clip=3):
        self.in_features = in_features
        self.out_features = out_features
        self.bias = bias
        self.gradient_clip = gradient_clip
        self.lr = lr
        self.dropout = dropout_rate
        self.dropout_mask = None

        # Initialize weights with Kaiming uniform initialization
        limit = np.sqrt(2 / in_features)
        self.w = np.random.uniform(-limit, limit, (in_features, out_features))
        self.b = np.zeros(out_features) if self.bias else None

        self.x = None
        self.grad_w = None
        self.grad_b = None

    def __call__(self, x):
        return self.forward(x)

    def parameters(self):
        return self.get_params()

    def set_lr(self, lr):
        self.lr = lr

    def get_params(self):
        return {'w': self.w, 'b': self.b if self.bias else None}

    def zero_grad(self):
        self.grad_w = np.zeros_like(self.w)
        if self.bias:
            self.grad_b = np.zeros_like(self.b)

    def get_grad(self, name=None):
        grads = {'grad_w': self.grad_w}
        if self.bias:
            grads['grad_b'] = self.grad_b
        return grads[f'grad_{name}'] if name is not None else grads

    def relu(self, out):
        return np.maximum(out, 0)

    def derivative_relu(self, z):
        return z > 0

    def forward(self, x):
        self.x = x
        self.z = np.dot(x, self.w)
        if self.bias:
            self.z += self.b

        if self.dropout > 0.0:
            self.dropout_mask = (np.random.rand(*self.z.shape) > self.dropout).astype(float)
            self.z *= self.dropout_mask

        out = self.relu(self.z)
        self.out = out
        return out

    def backward(self, dL_dout):
        if dL_dout is None:
            raise ValueError('grad output is none')
        
        # Backpropagate through ReLU
        dL_dz = dL_dout * self.derivative_relu(self.z)

        # self.grad_w = np.dot(self.x.T, dL_dz)

        # Gradient w.r.t. input (x)
        # dL_dx = np.dot(dL_dz, self.w.T)
        dL_dx =  self.w.T

        # Gradient w.r.t. bias (b) if bias is enabled
        if self.bias:
            self.grad_b = np.sum(dL_dz, axis=0)

        return dL_dx

    def update(self):
        # self.w -= self.lr * self.grad_w
        # if self.bias:
        #     self.b -= self.lr * self.grad_b
        pass

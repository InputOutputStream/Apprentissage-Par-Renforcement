import alpha as a
lr = 0.1
dropout = 0.1


class Linear:
    def __init__(self,
                 in_features,
                 out_features,
                 bias=True,
                 lr=lr,
                 dropout_rate=dropout,
                 gradient_clip=3):
        self.in_features = in_features
        self.out_features = out_features
        self.bias = bias
        self.gradient_clip = gradient_clip
        self.lr = lr
        self.dropout = dropout_rate
        self.dropout_mask = None

        # Initialize weights with Kaiming uniform initialization
        limit = a.sqrt(2 / in_features)

        self.w = a.uniform(-limit, limit, (in_features, out_features))
        if self.bias:
            self.b = a.zeros(out_features)
        else:
            self.b = None

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
        params = {'w': self.w, 'b': self.b if self.bias else None}
        return params

    def zero_grad(self):
        # Reset all gradients to zero
        self.grad_w = a.zeros_like(self.w)
        if self.bias:
            self.grad_b = a.zeros_like(self.b)

    def get_grad(self, name=None):
        self.grads = {}
        if self.bias:
            self.grads = {'grad_w': self.grad_w, 'grad_b': self.grad_b}
        else:
            self.grads = {'grad_w': self.grad_w}

        return self.grads[f'grad_{name}'] if name is not None else self.grads

    def relu(self, out):
        return a.maximum(out, 0)

    def derivative_relu(self, z):
        return z > 0

    def forward(self, x):
        self.x = x
        self.z = a.matmul(x, self.w)
        if self.bias:
            self.z += self.b

        if self.dropout > 0.0:
            self.dropout_mask = (a.rand(*self.z.shape) >
                                 self.dropout).astype(float)
            self.z = self.z * self.dropout_mask

        out = self.relu(self.z)
        self.out = out
        return out

    def backward(self, dL_dout):
        if dL_dout is None:
            print('grad output is none')
            return None

        dL_dout = dL_dout.reshape(self.z.shape)

        # Backpropagate through ReLU
        dL_dz = dL_dout * self.derivative_relu(self.z)

        # Apply dropout mask during backpropagation
        if self.dropout > 0.0:
            dL_dz = dL_dz * self.dropout_mask

        dL_dz = dL_dz.transpose((1, 0, 2))

        # Gradient w.r.t. weights (w)
        self.grad_w = a.dot(self.x.T, dL_dz)


        # Gradient w.r.t. bias (b) if bias is enabled
        if self.bias:
            self.grad_b = a.sum(dL_dz, axis=0)

        # Gradient Clipping
        if self.gradient_clip is not None:
            self.grad_w = a.clip(self.grad_w, -self.gradient_clip,
                                  self.gradient_clip)
            if self.bias and self.grad_b is not None:
                self.grad_b = a.clip(self.grad_b, -self.gradient_clip,
                                      self.gradient_clip)

    def update(self, ):
        self.w -= self.lr * self.grad_w
        self.b -= self.lr * self.grad_b



y = a.Array.randn((20,900))
x = a.Array.randint(10, 30, (180,900))

md = Linear(180, 20, 0.1, 0.1, 3)

for i in 100:
    out = md(x)
    md.backward(out)
    md.update()
    

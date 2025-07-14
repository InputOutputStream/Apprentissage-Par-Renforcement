import math
import numpy as np
from Linear import Linear

class Linear_Qnet:
    def __init__(self, input_size, hidden_size, output_size):
        self.linear1 = Linear(input_size, hidden_size)
        self.linear2 = Linear(hidden_size, output_size)
    
    def __call__(self, x):
        return self.forward(x)
    
    def forward(self, x):
        z = self.linear1(x)
        a = self.linear2(z)
        return a
    
    def backward(self, loss):    
        grad_l2 = self.linear2.backward(loss)
        grad_l1 = self.linear1.backward(grad_l2)
        
    def update(self):
        self.linear1.update()
        self.linear2.update()
    
    def zero_grad(self):
        self.linear1.zero_grad()
        self.linear2.zero_grad()

    @staticmethod
    def MSE(y, y_hat):
        return ((y - y_hat) ** 2)**5
    
    @staticmethod
    def MSE_derivative(y, y_hat):
        return 2 * (y_hat - y) / y.size





class Qtrainer:
    def __init__(self, model, lr, gamma):
        self.lr = lr
        self.gamma = gamma
        self.model = model
    
    def train_step(self, state, action, reward, next_state, done):
        state = np.array(state, dtype=float)
        next_state = np.array(next_state, dtype=float)
        action = np.array(action, dtype=int)
        reward = np.array(reward, dtype=float)

        if len(state.shape) == 1:
            state = np.expand_dims(state, 0)
            next_state = np.expand_dims(next_state, 0)
            action = np.expand_dims(action, 0)
            reward = np.expand_dims(reward, 0)
            done = (done, )

        pred = self.model(state)
        target = pred.copy()

        for idx in range(len(done)):
            Q_new = reward[idx]
            if not done[idx]:
                Q_new = reward[idx] + self.gamma * np.max(self.model(next_state[idx]))

            target[idx][action[idx]] = Q_new

        self.model.zero_grad()
        loss = self.model.MSE(target, pred)
        self.model.backward(loss)
        self.model.update()

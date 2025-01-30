from .. import core
from . import functional


class Parameter(core.Tensor):
    def __init__(self, t, requires_grad=True):
        super().__init__(t.detach(), requires_grad=requires_grad)

    def __repr__(self):
        return 'Parameter containing:\n' + super().__repr__()

class Module:
    def __init__(self):
        super().__setattr__('training', True)
        super().__setattr__('_parameters', dict())
        super().__setattr__('_buffers', dict())
        super().__setattr__('_modules', dict())
        
    def forward(self):
        raise NotImplementedError("To be implemented")
        
    def __call__(self, *args, **kwargs):
        return self.forward(*args, **kwargs)

    def register_parameter(self, name, parameter):
        self._parameters[name] = parameter

    def register_module(self, name, module):
        self._modules[name] = module
    
    def register_buffer(self, name, buffer):
        self._buffers[name] = buffer
    
    def children(self):
        for value in self._modules.values():
            yield value
        
    def named_children(self):
        for key_value in self._modules.items():
            yield key_value
    
    def modules(self):
        for _, module in self.named_modules():
            yield module
        
    def named_modules(self, memo=None, remove_duplicate=True, prefix=''):
        if memo is None:
            memo = set()
        if self not in memo:
            if remove_duplicate:
                memo.add(self)
            yield prefix, self
            for name, module in self.named_children():
                for m in module.named_modules(memo=memo, remove_duplicate=remove_duplicate, prefix=prefix+'.'+name):
                    yield m   

    def extra_repr(self):
        return ''
    
    def __repr__(self):
        repr_str = ''
        for name, module in self.named_modules():
            name = name.split('.')
            for i in range(len(name)):
                if i==len(name)-1:
                    if name[i] == '':
                        module_name = type(module).__name__
                    else:
                        module_name = name[i]
                    repr_str += f'{module_name}({module.extra_repr()})'
                else:
                    repr_str += '    '
            repr_str += '\n'
        return repr_str
            
    def parameters(self, recurse=True):
        for _, parameter in self.named_parameters(recurse=recurse):
            yield parameter
            
    def named_parameters(self, recurse=True):
        if not recurse:
            for key_value in self._parameters.items():
                yield key_value
        else:
            for module in self.modules():
                for key_value in module._parameters.items():
                    yield key_value
          
    def buffers(self, recurse=True):
        for _, buffer in self.named_buffers(recurse=recurse):
            yield buffer
            
    def named_buffers(self, recurse=True):
        if not recurse:
            for key_value in self._buffers.items():
                yield key_value
        else:
            for module in self.modules():
                for key_value in module._buffers.items():
                    yield key_value
    
    def apply(self, fn):
        for module in self.children():
            module.apply(fn)
        fn(self)
        return self
    
    def train(self, mode):
        if not isinstance(mode, bool):
            raise ValueError("train mode is expected to be boolean")
        for module in self.modules():
            module.training = mode
        return self
        
    def eval(self):
        return self.train(False)
    
    def requires_grad_(self, requires_grad=True):
        for parameter in self.parameters():
            parameter.requires_grad_(requires_grad)
        return self
    
    def zero_grad(self, set_to_none=True):
        for parameter in self.parameters():
            if set_to_none:
                parameter.grad = None
            else:
                parameter.grad = core.zeros_like(parameter.grad)
                
    def to(self, device=None, dtype=None):
        def to_apply(m):
            for key, parameter in m._parameters.items():
                requires_grad = parameter.requires_grad
                m.__setattr__(key, parameter.to(device=device, dtype=dtype).detach().requires_grad_(requires_grad=requires_grad))
                m.register_parameter(key, m.__getattribute__(key))
            for key, buffer in m._buffers.items():
                m.__setattr__(key, buffer.to(device=device, dtype=dtype))
                m.register_buffer(key, m.__getattribute__(key))
        return self.apply(to_apply)

    def __getattr__(self, name):
        parameters = self.__dict__['_parameters']
        if name in parameters:
            return parameters[name]
        buffers = self.__dict__['_buffers']
        if name in buffers:
            return buffers[name]
        modules = self.__dict__['_modules']
        if name in modules:
            return modules[name]
        raise AttributeError(f"{type(self).__name__} object has no attribute {name}")

    def __setattr__(self, name, value):
        if isinstance(value, Parameter):
            self.register_parameter(name, value)
        elif isinstance(value, Module):
            self.register_module(name, value)
        elif name in self._buffers:
            self.register_buffer(name, value)
        else:
            super().__setattr__(name, value)
        


class Linear(Module):

    def __init__(self, in_features, out_features, bias=True, device=None, dtype=None):
        super().__init__()
        self.in_features = in_features
        self.out_features = out_features
        self.weight = Parameter(core.empty(out_features, in_features, dtype=dtype, device=device))
        if bias:
            self.bias = Parameter(core.empty(out_features, dtype=dtype, device=device))
        else:
            self.bias = None
        self.reset_parameters()

    def reset_parameters(self):
        scale = (2.0/self.in_features)**0.5
        self.weight.data = core.randn_like(self.weight)*scale
        if self.bias is not None:
            self.bias.data = core.zeros_like(self.bias)
    
    def forward(self, t):
        if self.bias is not None:
            return core.matmul(t, self.weight.transpose(-1,-2)) + self.bias
        return core.matmul(t, self.weight.transpose(-1,-2))

    def extra_repr(self):
        return f'in_features={self.in_features}, out_features={self.out_features}, bias={self.bias is not None}'


class Conv2d(Module):

    def __init__(self, in_channels, out_channels, kernel_size, stride=1, padding=0, bias=True, padding_mode='zeros', device=None, dtype=None):
        super().__init__()
        self.in_channels = in_channels
        self.out_channels = out_channels
        if isinstance(kernel_size, int):
            kernel_size = (kernel_size, kernel_size)
        self.kernel_size = kernel_size
        self.stride = stride
        self.padding = padding
        self.padding_mode = padding_mode
        self.weight = Parameter(core.empty(out_channels, in_channels, kernel_size[0], kernel_size[1], dtype=dtype, device=device))
        if bias:
            self.bias = Parameter(core.empty(1,out_channels,1,1, dtype=dtype, device=device))
        else:
            self.bias = None
        self.reset_parameters()

    def reset_parameters(self):
        scale = (2.0/(self.in_channels * self.kernel_size[0] * self.kernel_size[1]))**0.5
        self.weight.data = core.randn_like(self.weight)*scale
        if self.bias is not None:
            self.bias.data = core.zeros_like(self.bias)
    
    def forward(self, t):
        if self.bias is not None:
            return functional.conv2d(t, self.weight, stride=self.stride, padding=self.padding) + self.bias
        return functional.conv2d(t, self.weight, stride=self.stride, padding=self.padding)

    def extra_repr(self):
        return f'in_c={self.in_channels}, out_c={self.out_channels}, kernel={self.kernel_size}, stride={self.stride}, pad={self.padding}, bias={self.bias is not None}'

    
class MaxPool2d(Module):

    def __init__(self, kernel_size, stride=None, padding=0, return_indices=False):
        super().__init__()
        self.kernel_size = kernel_size
        self.stride = stride
        self.padding = padding
        self.return_indices = return_indices

    def forward(self, t):
        return functional.max_pool2d(t, self.kernel_size, stride=self.stride, padding=self.padding, return_indices=self.return_indices)

    def extra_repr(self):
        return f'kernel_size={self.kernel_size}, stride={self.stride}, pad={self.padding}'


class Softmax(Module):

    def __init__(self, dim):
        super().__init__()
        self.dim = dim

    def forward(self, t):
        return functional.softmax(t, self.dim)

    def extra_repr(self):
        return f'dim={self.dim}'


class Dropout(Module):

    def __init__(self, p=0.5, inplace=False):
        super().__init__()
        self.p = p
        self.inplace = inplace

    def forward(self, t):
        return functional.dropout(t, p=self.p, training=self.training, inplace=self.inplace)

    def extra_repr(self):
        return f'p={self.p}, inplace={self.inplace}'



class RNN(Module):

    def __init__(self, input_size, hidden_size, num_layers=1, nonlinearity='tanh', bias=True, batch_first=False, dropout=None, device=None, dtype=None):
        super().__init__()
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.nonlinearity = nonlinearity
        self.dropout = dropout
        self.batch_first = batch_first
        for k in range(num_layers):
            if k==0:
                self.__setattr__(f'weight_ih_l{k}', Parameter(core.empty(hidden_size, input_size, dtype=dtype, device=device)))
            else:
                self.__setattr__(f'weight_ih_l{k}', Parameter(core.empty(hidden_size, hidden_size, dtype=dtype, device=device)))
            self.__setattr__(f'weight_hh_l{k}', Parameter(core.empty(hidden_size, hidden_size, dtype=dtype, device=device)))

        if bias:
            for k in range(num_layers):
                self.__setattr__(f'bias_ih_l{k}', Parameter(core.empty(hidden_size, dtype=dtype, device=device)))
                self.__setattr__(f'bias_hh_l{k}', Parameter(core.empty(hidden_size, dtype=dtype, device=device)))
            self.bias=True
        else:
            self.bias=None
            self.bias_ih_l = None
            self.bias_hh_l = None
        self.reset_parameters()

    def reset_parameters(self):
        scale = (1.0/self.hidden_size)**0.5
        for k in range(self.num_layers):
            w_ih = self.__getattr__(f'weight_ih_l{k}')
            w_hh = self.__getattr__(f'weight_hh_l{k}')
            w_ih.data = core.randn_like(w_ih)*scale
            w_hh.data = core.randn_like(w_hh)*scale
        if self.bias is not None:
            for k in range(self.num_layers):
                b_ih = self.__getattr__(f'bias_ih_l{k}')
                b_hh = self.__getattr__(f'bias_hh_l{k}')
                b_ih.data = core.zeros_like(b_ih)*scale
                b_hh.data = core.zeros_like(b_hh)*scale
    
    def forward(self, t, h_0=None):
        if t.numel()==2:
            if self.batch_first:
                t = t.reshape((1, t.shape[0], t.shape[1]))
            else:
                t = t.reshape((t.shape[0], 1, t.shape[1]))
        
        if self.batch_first:
            t = t.transpose(0, 1).contiguous()
        def get_h(t, h, k):
            if self.bias is not None:
                return core.tanh(t.matmul(self.__getattr__(f'weight_ih_l{k}').t()) + self.__getattr__(f'bias_ih_l{k}') \
                    + h.matmul(self.__getattr__(f'weight_hh_l{k}').t()) + self.__getattr__(f'bias_hh_l{k}'))
            return core.tanh(t.matmul(self.__getattr__(f'weight_ih_l{k}').t()) + h.matmul(self.__getattr__(f'weight_hh_l{k}').t()))
        if h_0 is None:
            h = core.zeros(self.num_layers, t.shape[1], self.hidden_size, dtype=t.dtype, device=t.device)
        else:
            h = core.empty(self.num_layers, t.shape[1], self.hidden_size, dtype=t.dtype, device=t.device)
            h[:] = h_0
        out = core.empty(t.shape[0], t.shape[1], self.hidden_size, dtype=t.dtype, device=t.device)
        for i in range(t.shape[0]):
            h[0,:,:] = get_h(t[i,:,:], h[0,:,:], 0)
            for k in range(1, self.num_layers):
                h[k,:,:] = get_h(h[k-1,:,:], h[k,:,:], k)
            out[i,:,:] = h[-1,:,:]
        return out, h

    def extra_repr(self):
        return f'input_size={self.input_size}, hidden_size={self.hidden_size}, num_layers={self.num_layers}, nonlinearity={self.nonlinearity}, dropout={self.dropout}, bias={self.bias is not None}'
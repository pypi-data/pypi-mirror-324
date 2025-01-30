import numpy as np
try:
    import cupy as cp
    import cupyx
    cp.cupyx = cupyx
except:
    cp = None
    print("cupy is not installed. GPU support will be unavailable without cupy")
# Define numeric constants
from math import e, inf, nan, pi
from math import prod as math_prod


# dtypes
float32 = "float32"
float64 = "float64"
double = "float64"
float16 = "float16"
half = "float16"
uint8 = "uint8"
uint16 = "uint16"
uint32 = "uint32"
uint64 = "uint64"
int8 = "int8"
int16 = "int16"
short = "int16"
int32 = "int32"
int64 = "int64"
long = "int64"

def _get_array_module(*args):
    if cp is None:
        return np
    else:
        array_args = [(arg._data if is_tensor(arg) else arg) for arg in args]
        return cp.get_array_module(*array_args)

# cuda class for gpu support using cupy ***************************************
class cuda:
    @staticmethod
    def device_count():
        if cp is not None:
            return cp.cuda.runtime.getDeviceCount()
        print("cupy is not installed. GPU support will be unavailable without cupy")
        return 0
        
    @staticmethod
    def is_available():
        if cp is not None:
            return cp.cuda.is_available()
        print("cupy is not installed. GPU support will be unavailable without cupy")
        return False
    
    @staticmethod    
    def current_device():
        if cp is not None:
            return cp.cuda.runtime.getDevice()
        raise RuntimeError("cupy is not installed. GPU support will be unavailable without cupy")
    
    @staticmethod
    def get_device_properties(device=None):
        if device is None:
            device = cp.current_device()
        if cp is not None: 
            return cp.cuda.runtime.getDeviceProperties(device)
        else:
            raise RuntimeWarning("cupy is not installed. GPU support will be unavailable without cupy")
    
    @staticmethod
    def set_device(device):
        '''Set gpu device. device is int - 0, 1, ...
        '''
        if isinstance(device, int):
            if not cuda.is_available():
                raise RuntimeError("Cuda device not available")
            else:
                cp.cuda.runtime.setDevice(device)
                return f"device set to {cuda.current_device()}'"
        else:
            raise ValueError("device argument should be int - 0, 1, ...")
    
    class device:
        def __init__(self, dev):
            self.dev = dev
            self.current_div = cuda.current_device()
        
        def __enter__(self):
            cuda.set_device(self.dev)
        
        def __exit__(self, exc_type, exc_value, traceback):
            if exc_type:
                print(exc_type)
            if exc_value:
                print(exc_value)
            if traceback:
                print(traceback)
            cuda.set_device(self.current_div)


# Tensor class **************************************************************** 
class Tensor:
    _default_dtype = float32
    
    def __init__(self, in_data, requires_grad=False):
        self._data = in_data
        self.requires_grad = requires_grad
        if self.requires_grad and self._data.dtype.kind != 'f':
            raise RuntimeError("Only Tensors of floating point dtype can require gradients")
        self._grad = None
        self.grad_fn = None

    def requires_grad_(self, requires_grad=True):
        self.requires_grad = requires_grad
        return self

    @property
    def dtype(self):
        return self._data.dtype.name

    @property
    def device(self):
        if isinstance(self._data, np.ndarray):
            return 'cpu'
        else:
            return self._data.device.id

    def __repr__(self):
        data_str = str(self._data).replace("\n", "\n" + " " * 7)
        device_str = f", device={self.device}" if self.device != 'cpu' else "" 
        if self.grad_fn:
            grad_fn_name = self.grad_fn.__repr__()
            grad_fn_name = f"<'{grad_fn_name.split('.')[-1].split()[0]}' at {grad_fn_name.split('.')[-1].split()[-1]}"
            return f"tensor({data_str}, {self.dtype}, grad_fn={grad_fn_name}{device_str})"
        elif self.requires_grad:
            return f"tensor({data_str}, {self.dtype}, requires_grad=True{device_str})"
        else:
            return f"tensor({data_str}, {self.dtype}{device_str})"

    @property
    def shape(self):
        return size(self)
    
    def size(self, dim=None):
        return size(self, dim=dim)
    
    def numel(self):
        return numel(self)
    
    @property
    def ndim(self):
        return self._data.ndim

    def contiguous(self):
        xp = _get_array_module(self._data)
        if self._data.data.contiguous:
            return self
        return as_tensor(xp.ascontiguousarray(self._data))
    
    def __getitem__(self, sl):
        return Get_Item.apply(self, sl=sl)
        
    def __setitem__(self, sl, value):
        Set_Item.apply(self, value, sl=sl)
    
    @property
    def data(self):
        return self.detach()
        
    @data.setter
    def data(self, value):
        self._data = value.detach().to(dtype=self.dtype, device=self.device)._data
            
    @property
    def grad(self):
        if self.requires_grad:
            if self._grad:
                return self._grad
        elif self.grad_fn:
            got_grad = self.grad_fn.get_grad()
            if got_grad:
                return got_grad
            else:
                raise UserWarning("The .grad attribute of non-leaf tensor is being accessed. It won't be populated \
                during .backward() unless .retain_grad() is used. ")
        else:
            raise UserWarning("The .grad attribute of this tensor won't be populated during .backward().")
    
    @grad.setter
    def grad(self, value):
        if (value is not None):
            value = value.detach().to(dtype=self.dtype, device=self.device)
        if self.requires_grad:            
            self._grad = value
        elif self.grad_fn:
            self.grad_fn.set_grad(value)
        else:
            raise UserWarning("This tensor don't need grad.")
                       
        
    def retain_grad(self):
        if self.grad_fn:
            self.grad_fn.retain_grad()
        else:
            raise ValueError("This is not a non-leaf tensor - can't apply retain_grad().")
            
    def backward(self, retain_graph=False):
        if self.numel() > 1:
            raise ValueError("backward() is supported only for tensors of numel (number of elements) = 1")
        stack = []
        visited = set()
        def build_stack(vertex):
            if vertex and (vertex not in visited):
                visited.add(vertex)
                for child in vertex._children:
                    build_stack(child)
                stack.append(vertex)
        build_stack(self.grad_fn)
        if stack:
            stack[-1].accumulate_grad(tensor(1.0, dtype=stack[-1]._saved_dtype, device=stack[-1]._saved_device))
            while stack:
                fn = stack.pop()
                if fn._grad_track:
                    fn._backward()
                if not retain_graph:
                    fn._saved = None
                    fn._children = []
                if not fn._retain_grad:
                    fn._accumulated_grad = None

    def item(self):
        if self.numel() != 1:
            raise ValueError("Tensor.item() only works for tensors with one element.")
        else:
            return self._data.item()
            
    def tolist(self):
        return self._data.tolist()

    def numpy(self):
        if self.device == 'cpu':
            return self._data
        return self._data.get()
        
    def clone(self):
        return Copy_To.apply(self)
    
    def detach(self):
        return as_tensor(self._data)
    
    @property
    def device(self):
        if (type(self._data).__module__ == 'cupy'):
            return self._data.device.id
        else:
            return "cpu"

    def to(self, device=None, dtype=None):
        if device is None:
            device = self.device
        if dtype is None:
            dtype = self.dtype
        if (self.device == device) and (self.dtype == dtype):
            return self
        return Copy_To.apply(self, device=device, dtype=dtype)
    
    def reshape(self, shape):
        return reshape(self, shape)
    
    def view(self, shape):
        return view(self, shape)
    
    def sum(self, dim=None, keepdims=False):
        return sum(self, dim=dim, keepdims=keepdims)
    
    def broadcast_to(self, shape):
        return broadcast_to(self, shape)
    
    def reduce_to(self, shape):
        return reduce_to(self, shape)
    
    def squeeze(self, dims=None):
        return squeeze(self, dims=dims)
    
    def unsqueeze(self, dims):
        return unsqueeze(self, dims=dims)
    
    def transpose(self, dim0, dim1):
        return transpose(self, dim0=dim0, dim1=dim1)
    
    def t(self):
        return t(self)
    
    def stride(self, dim=None):
        if dim == None:
            return tuple([i//8 for i in self._data.strides])
        return tuple([i//8 for i in self._data.strides])[dim]
    
    def __eq__(self, other):
        return as_tensor(self._data==as_tensor(other)._data)
    
    def __ne__(self, other):
        return as_tensor(self._data!=as_tensor(other)._data)
    
    def __gt__(self, other):
        return as_tensor(self._data>as_tensor(other)._data)
    
    def __ge__(self, other):
        return as_tensor(self._data>=as_tensor(other)._data)
    
    def __lt__(self, other):
        return as_tensor(self._data<as_tensor(other)._data)
    
    def __le__(self, other):
        return as_tensor(self._data<=as_tensor(other)._data)
    
    def __neg__(self):
        return Neg.apply(self)
    
    def __add__(self, other):
        return Add.apply(self, other)
    def __radd__(self, other):
        return Add.apply(other, self)
    
    def __sub__(self, other):
        return Sub.apply(self, other)
    def __rsub__(self, other):
        return Sub.apply(other, self)
    
    def __mul__(self, other):
        return Mul.apply(self, other)
    def __rmul__(self, other):
        return Mul.apply(other, self)
    
    def __truediv__(self, other):
        return Div.apply(self, other)
    def __rtruediv__(self, other):
        return Div.apply(other, self)
    
    def __pow__(self, exponent):
        return Pow.apply(self, exponent=exponent)
        
    def pow(self, exponent):
        return self**exponent
        
    def square(self):
        return square(self)
        
    def sqrt(self):
        return sqrt(self)
    
    def abs(self):
        return absolute(self)
        
    def sigmoid(self):
        return sigmoid(self)
    
    def dot(self, t):
        '''Dot product of two 1-D tensors.'''
        return dot(self, t)
    
    def matmul(self, t):
        '''Matrix product of two tensors.'''
        return matmul(self, t)
    
    def tensordot(self, t, dims=2):
        '''Compute tensor dot product along specified dims.'''
        return tensordot(self, t, dims=dims)
        
    def argsort(self, dim=-1):
        '''Returns the indices that would sort an tensor.
        '''
        return argsort(self, dim=dim)

    def argmin(self, dim=None, keepdims=False):
        '''Returns the indices of the minimum values along a dim.
        By default (dim=None), the index is into the flattened tensor.
        '''
        return argmin(self, dim=dim, keepdims=keepdims)

    def argmax(self, dim=None):
        '''Returns the indices of the maximum values along a dim.
        By default (dim=None), the index is into the flattened tensor.
        '''
        return argmax(self, dim=dim)

    def min(self, dim=None, keepdims=False):
        '''Return the minimum along a given axis.
        '''
        return amin(self, dim=dim, keepdims=keepdims)

    def max(self, dim=None, keepdims=False):
        '''Return the maximum along a given axis.
        '''
        return amax(self, dim=dim, keepdims=keepdims)

    def all(self, dim=None, keepdims=False):
        '''Test whether all array elements along a given axis evaluate to True.
        '''
        return all(self, dim=dim, keepdims=keepdims)

    def any(self, dim=None, keepdims=False):
        '''Test whether any array element along a given axis evaluates to True.
        '''
        return any(self, dim=dim, keepdims=keepdims)

    def isinf(self):
        '''Test element-wise for positive or negative infinity.
        '''
        return isinf(self)

    def isnan(self):
        '''Test element-wise for NaN and return result as a boolean tensor.
        '''
        return isnan(self)

    def sort(self, dim=-1):
        '''Sorts the elements of the input tensor along a given dimension 
        in ascending order by value.
        '''
        return sort(self, dim=dim)

    def flip(self, dims=None):
        '''Reverse the order of elements in an array along the given axis.
        The shape of the tensor is preserved, but the elements are reordered.
        
        dims : None or int or tuple of ints, optional - axis or axes along 
        which to flip over. The default, dims=None, will flip over all of 
        the axes of the input tensor.
        '''
        return flip(self, dims=dims)

    def mean(self, dim=None, keepdims=False, dtype=None):
        '''Compute the arithmetic mean along the specified axis.
        '''
        return mean(self, dim=dim, keepdims=keepdims, dtype=dtype)

    def median(self, dim=None, keepdims=False):
        '''Compute the median along the specified axis.
        '''
        return median(self, dim=dim, keepdims=keepdims)
# *****************************************************************************

# tensor creation functions****************************************************
def tensor(in_data, requires_grad=False, dtype=None, device=None):
    '''
    Constructs a tensor with no autograd history (also known as a "leaf tensor"
    Args:
    in_data (array_like): Initial data for the tensor. Can be a list, tuple,
        NumPy ``ndarray``, cupy ndarray, scalar, and other types.

    Keyword args:
        dtype (dtype variable, optional): the desired data type of returned tensor.
        device ('cpu' or gpu device id, optional): the device of the constructed tensor. 
        If None and data is a tensor
            then the device of data is used. If None and data is not a tensor then
            the result tensor is constructed on the current device.
        requires_grad (bool, optional): If autograd should record operations on the
            returned tensor. Default: ``False``.

    Example::

        >>> nptorch.tensor([[0.1, 1.2], [2.2, 3.1], [4.9, 5.2]])
        tensor([[ 0.1000,  1.2000],
                [ 2.2000,  3.1000],
                [ 4.9000,  5.2000]], float32)

        >>> nptorch.tensor([0, 1])  # Type inference on data
        tensor([ 0,  1])

        >>> nptorch.tensor([[0.11111, 0.222222, 0.3333333]],
        ...              dtype=nptorch.float64,
        ...              device=0  # creates a double tensor on a CUDA device
        tensor([[ 0.1111,  0.2222,  0.3333]], float64, device=0)

        >>> torch.tensor([3.14159, 1], requires_grad=True)  # Create a zero-dimensional (scalar) tensor
        tensor([3.1416, 1.0], float32, requires_grad=True)
    '''
    if is_tensor(in_data):
        raise RuntimeError("To copy construct from a tensor, it is recommended to use sourceTensor.clone().detach() \
        or sourceTensor.clone().detach().requires_grad_(True), rather than torch.tensor(sourceTensor).")
    if not (type(in_data).__module__ == 'numpy' or type(in_data).__module__ == 'cupy'):
        if device in [None, 'cpu']:
            in_data = np.array(in_data, dtype=dtype)
            if (dtype is None) and (in_data.dtype.kind == 'f'):
                in_data = in_data.astype(float32)
        else:
            with cuda.device(device):
                in_data = cp.array(in_data, dtype=dtype)
                if (dtype is None) and (in_data.dtype.kind == 'f'):
                    in_data = in_data.astype(float32)
    elif type(in_data).__module__ == 'cupy' and device == 'cpu':
        in_data = cp.asnumpy(in_data)
        if dtype is not None:
            in_data = in_data.astype(dtype)
    else:
        if device in [None, 'cpu']:
            in_data = np.array(in_data, dtype=dtype)
        else:
            with cuda.device(device):
                in_data = cp.array(in_data, dtype=dtype)
    return Tensor(in_data, requires_grad=requires_grad)

def as_tensor(in_data, requires_grad=False, dtype=None, device=None):
    '''
    Converts :attr:`data` into a tensor, sharing data and preserving autograd
    history if possible.

    If :attr:`data` is already a tensor with the requested dtype and device
    then :attr:`data` itself is returned, but if :attr:`data` is a
    tensor with a different dtype or device then it's copied as if using
    `data.to(dtype=dtype, device=device)`.

    Args:
    in_data (array_like): Initial data for the tensor. Can be a list, tuple,
        NumPy ``ndarray``, cupy ndarray, scalar, and other types.
    '''
    if is_tensor(in_data):
        return in_data.to(dtype=dtype, device=device)
    if not (type(in_data).__module__ == 'numpy' or type(in_data).__module__ == 'cupy'):
        return tensor(in_data, dtype=dtype, device=device, requires_grad=requires_grad)

    if type(in_data).__module__ == 'cupy' and device == 'cpu':
        in_data = cp.asnumpy(in_data)
        if dtype is not None:
            in_data = in_data.astype(dtype)
    else:
        xp = _get_array_module(in_data)
        if device in [None, 'cpu']:
            in_data = xp.asarray(in_data, dtype=dtype)
        else:
            with cuda.device(device):
                in_data = xp.asarray(in_data, dtype=dtype)     
    return Tensor(in_data, requires_grad=requires_grad)

def zeros(*shape, requires_grad=False, dtype=None, device=None):
    '''Returns a tensor filled with the scalar value 0, 
    with the shape defined by the variable argument shape.

    >>> zeros(2, 3)
    tensor([[0. 0. 0.]
            [0. 0. 0.]]), float32)

    >>> zeros(4, requires_grad=True)
    tensor([0. 0. 0. 0.], float32, requires_grad=True)
    '''
    if dtype is None:
        dtype = get_default_dtype()
    if device in [None, 'cpu']:
        xp = np 
        return as_tensor(xp.zeros(shape, dtype=dtype), requires_grad=requires_grad)
    with cuda.device(device):
        xp = cp
        return as_tensor(xp.zeros(shape, dtype=dtype), requires_grad=requires_grad)

def zeros_like(t, requires_grad=False, dtype=None, device=None):
    '''Returns a tensor filled with the scalar value 0, with the same shape as t.
    zeros_like(t) is equivalent to zeros(*t.size(), dtype=t.dtype) or zeros(*t.shape, dtype=t.dtype).
    dtype argument can be provided to get the same size as t but different dtype

    >>> t = tensor([[0.1, 0.2, 3, 4.9, 5], [6, 7.5, 8, 9.6, 10]])
    print(t)
    tensor([[ 0.1  0.2  3.   4.9  5. ]
            [ 6.   7.5  8.   9.6 10. ]]), float32)

    >>> zeros_like(t)
    tensor([[0. 0. 0. 0. 0.]
            [0. 0. 0. 0. 0.]]), float32)

    >>> zeros_like(t, dtype='float64', requires_grad=True)
    tensor([[0. 0. 0. 0. 0.]
            [0. 0. 0. 0. 0.]], float64, requires_grad=True)
    '''
    if dtype is None:
        dtype = t.dtype
    if device is None:
        device = t.device
    return zeros(*t.shape, requires_grad=requires_grad, dtype=dtype, device=device)

def ones(*shape, requires_grad=False, dtype=None, device=None):
    '''Returns a tensor filled with the scalar value 1, 
    with the shape defined by the variable argument shape.

    >>> ones(2, 3)
    tensor([[1. 1. 1.]
            [1. 1. 1.]]), float32)

    >>> ones(4, requires_grad=True)
    tensor([1. 1. 1. 1.], float32, requires_grad=True)
    '''
    if dtype is None:
        dtype = get_default_dtype()
    if device in [None, 'cpu']:
        xp = np
        return as_tensor(xp.ones(shape, dtype=dtype), requires_grad=requires_grad)
    with cuda.device(device):
        xp = cp
        return as_tensor(xp.ones(shape, dtype=dtype), requires_grad=requires_grad)

def ones_like(t, requires_grad=False, dtype=None, device=None):
    '''Returns a tensor filled with the scalar value 1, with the same shape as t.
    ones_like(t) is equivalent to ones(*t.size(), dtype=t.dtype) or ones(*t.shape, dtype=t.dtype).
    dtype argument can be provided to get the same size as t but different dtype

    >>> t = tensor([[0.1, 0.2, 3, 4.9, 5], [6, 7.5, 8, 9.6, 10]])
    print(t)
    tensor([[ 0.1  0.2  3.   4.9  5. ]
            [ 6.   7.5  8.   9.6 10. ]]), float32)

    >>> zeros_like(t)
    tensor([[1. 1. 1. 1. 1.]
            [1. 1. 1. 1. 1.]]), float32)

    >>> zeros_like(t, dtype='float64', requires_grad=True)
    tensor([[1. 1. 1. 1. 1.]
            [1. 1. 1. 1. 1.]], float64, requires_grad=True)
    '''
    if dtype is None:
        dtype = t.dtype
    if device is None:
        device = t.device
    return ones(*t.shape, requires_grad=requires_grad, dtype=dtype, device=device)

def empty(*shape, requires_grad=False, dtype=None, device=None):
    '''Returns an uninitialized tensor with the shape defined by the 
    variable argument shape.
    '''
    if dtype is None:
        dtype = get_default_dtype()
    if device in [None, 'cpu']:
        xp = np
        return as_tensor(xp.empty(shape, dtype=dtype), requires_grad=requires_grad)
    with cuda.device(device):
        xp = cp
        return as_tensor(xp.empty(shape, dtype=dtype), requires_grad=requires_grad)

def empty_like(t, requires_grad = False, dtype = None, device=None):
    '''Returns an uninitialized tensor  with the same shape as t. empty_like(t) is 
    equivalent to empty(*t.size(), dtype=t.dtype) or empty(*t.shape, dtype=t.dtype).
    dtype argument can be provided to get the same size as t but different dtype.
    '''
    if dtype is None:
        dtype = t.dtype
    if device is None:
        device = t.device
    return empty(*t.shape, requires_grad=requires_grad, dtype=dtype, device=device)

def arange(*args, requires_grad=False, dtype=None, device=None):
    '''Return evenly spaced values within a given interval.
    start, end, step=1
    
    >>> arange(4)
    tensor([0. 1. 2. 3.]), float32)

    >>> arange(2.3, 7.7)
    tensor([2.3 3.3 4.3 5.3 6.3 7.3]), float32)

    >>> arange(1, 2.5, 0.5)
    tensor([1.  1.5 2. ]), float32)
    '''
    if dtype is None:
        dtype = get_default_dtype()
    if device in [None, 'cpu']:
        xp = np
        return as_tensor(xp.arange(*args, dtype=dtype), requires_grad=requires_grad)
    with cuda.device(device):
        xp = cp
        return as_tensor(xp.arange(*args, dtype=dtype), requires_grad=requires_grad)

def linspace(start, end, steps, requires_grad=False, dtype=None, device=None):
    '''Creates a one-dimensional tensor of size steps whose values are evenly spaced from 
    start to end, inclusive.
    
    >>> linspace(0, 1, 11)
    tensor([0.  0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1. ]), float32)
    '''
    if dtype is None:
        dtype = get_default_dtype()
    if device in [None, 'cpu']:
        xp = np
        return as_tensor(xp.linspace(start=start, stop=end, num=steps, dtype=dtype), requires_grad=requires_grad)
    with cuda.device(device):
        xp = cp
        return as_tensor(xp.linspace(start=start, stop=end, num=steps, dtype=dtype), requires_grad=requires_grad)

def eye(n, requires_grad=False, dtype=None, device=None):
    '''Returns a 2-D identity tensor i.e. a 2-D tensor with ones on the 
    diagonal and zeros elsewhere.
    
    >>> eye(3)
    tensor([[1. 0. 0.]
            [0. 1. 0.]
            [0. 0. 1.]]), float32)
    '''
    if dtype is None:
        dtype = get_default_dtype()
    if device in [None, 'cpu']:
        xp = np
        return as_tensor(xp.identity(n, dtype=dtype), requires_grad=requires_grad)
    with cuda.device(device):
        xp = cp
        return as_tensor(xp.identity(n, dtype=dtype), requires_grad=requires_grad)

def rand(*shape, requires_grad=False, dtype=None, device=None):
    '''Create a tensor with random samples from a uniform distribution over [0, 1). Parameters are integers of shape.
    >>> t = rand(2,3)
    >>> print(t)
    tensor([[0.47786182 0.11399009 0.12682912]
            [0.21122909 0.14755015 0.85070366]]), float32)
    '''
    if dtype is None:
        dtype = get_default_dtype()
    if device in [None, 'cpu']:
        xp = np
        return as_tensor(xp.random.rand(*shape).astype(dtype), requires_grad=requires_grad)
    with cuda.device(device):
        xp = cp
        return as_tensor(xp.random.rand(*shape).astype(dtype), requires_grad=requires_grad)

def rand_like(t, requires_grad = False, dtype = None, device=None):
    '''Create a tensor with random samples from a uniform distribution over [0, 1) with same shape as t.
    >>> t1 = zeros(2,3)
    >>> t2 = rand_like(t1)
    >>> print(t2)
    tensor([[0.7622367  0.6945961  0.9983034 ]
            [0.5883543  0.28077677 0.41802993]]), float32)
    '''
    if dtype is None:
        dtype = t.dtype
    if device is None:
        device = t.device
    return rand(*t.shape, requires_grad=requires_grad, dtype=dtype, device=device)

def randn(*shape, requires_grad=False, dtype=None, device=None):
    '''Create a tensor with random samples from the “standard normal” distribution. Parameters are integers of shape.
    >>> randn(3,3)
    tensor([[ 1.4339195  -0.88396066 -1.1786213 ]
            [-0.23667867  0.8296834  -1.5985084 ]
            [-1.1918153  -0.85116994 -0.7438147 ]]), float32)
    '''
    if dtype is None:
        dtype = get_default_dtype()
    if device in [None, 'cpu']:
        xp = np
        return as_tensor(xp.random.randn(*shape).astype(dtype), requires_grad=requires_grad)
    with cuda.device(device):
        xp = cp
        return as_tensor(xp.random.randn(*shape).astype(dtype), requires_grad=requires_grad)

def randn_like(t, requires_grad = False, dtype = None, device=None):
    '''Create a tensor with random samples from the “standard normal” distribution with same shape as t.
    >>> t1 = zeros(3,3)
    >>> t2 = randn_like(t1)
    >>> print(t2)
    tensor([[ 2.1127505  -1.2561972  -0.5121924 ]
            [ 0.33899143  1.2020179  -2.421359  ]
            [ 0.4532821  -0.9698113  -0.6090799 ]]), float32)
    '''
    if dtype is None:
        dtype = t.dtype
    if device is None:
        device = t.device
    return randn(*t.shape, requires_grad=requires_grad, dtype=dtype, device=device)

def randint(low, high, size, requires_grad=False, dtype=None, device=None):
    '''Create a tensor with random integers generated uniformly between low (inclusive) and high (exclusive).
    The shape of the tensor is defined by the argument size(tuple).
    >>> randint(0,10,(2,3))
    tensor([[2 8 0]
            [2 1 4]]), int32)
    '''
    
    if device in [None, 'cpu']:
        xp = np
        return as_tensor(xp.random.randint(low=low, high=high, size=size, dtype=dtype), requires_grad=requires_grad)
    with cuda.device(device):
        xp = cp
        return as_tensor(xp.random.randint(low=low, high=high, size=size, dtype=dtype), requires_grad=requires_grad)

def randint_like(t, low, high, requires_grad = False, dtype = None, device=None):
    '''Create a tensor with random integers generated uniformly between low (inclusive) and high (exclusive)
    with same shape as t.
    >>> t1 = zeros(3,3)
    >>> t2 = randint_like(t1, 0, 10)
    >>> print(t2)
    tensor([[1 6 0]
            [2 0 7]
            [2 8 6]]), int32)
    '''
    if device is None:
        device = t.device
    return randint(low=low, high=high, size=t.shape, requires_grad=requires_grad, dtype=dtype, device=device)
# *****************************************************************************

# tensor util functions *******************************************************
def is_tensor(x):
    return isinstance(x, Tensor)
    
def get_default_dtype():
    '''Get the current default floating point dtype.'''
    return Tensor._default_dtype
        
def set_default_dtype(d):
    '''Sets the default floating point dtype to d. 
    Supports 'float32' and 'float64' as inputs.'''
    Tensor._default_dtype = d

def size(t, dim=None):
    if dim == None:
        return t._data.shape
    else:
        return t._data.shape[dim]

def numel(t):
    return t._data.size

def argsort(t, dim=-1):
    '''Returns the indices that would sort an tensor.
    '''
    xp = _get_array_module(t)
    return as_tensor(xp.argsort(t._data, axis=dim))

def argmin(t, dim=None, keepdims=False):
    '''Returns the indices of the minimum values along a dim.
    By default (dim=None), the index is into the flattened tensor.
    '''
    xp = _get_array_module(t)
    return as_tensor(xp.argmin(t._data, axis=dim, keepdims=keepdims))

def argmax(t, dim=None):
    '''Returns the indices of the maximum values along a dim.
    By default (dim=None), the index is into the flattened tensor.
    '''
    xp = _get_array_module(t)
    return as_tensor(xp.argmax(t._data, axis=dim))

def all(t, dim=None, keepdims=False):
    '''Test whether all array elements along a given axis evaluate to True.
    '''
    xp = _get_array_module(t)
    return as_tensor(xp.all(t._data, axis=dim, keepdims=keepdims))

def any(t, dim=None, keepdims=False):
    '''Test whether any array element along a given axis evaluates to True.
    '''
    xp = _get_array_module(t)
    return as_tensor(xp.any(t._data, axis=dim, keepdims=keepdims))

def isinf(t):
    '''Test element-wise for positive or negative infinity.
    '''
    xp = _get_array_module(t)
    return as_tensor(xp.isinf(t._data))

def isnan(t):
    '''Test element-wise for NaN and return result as a boolean tensor..
    '''
    xp = _get_array_module(t)
    return as_tensor(xp.isnan(t._data))
# *****************************************************************************

def manual_seed(seed):
    '''Sets the seed for generating random numbers for all devices.'''
    np.random.seed(seed)
    cp.random.seed(seed)

def is_grad_enabled():
    return not(Function._no_grad)

def set_grad_enabled(bl):
    if not isinstance(bl, bool):
        raise ValueError("set_grad_enabled(bl) takes a boolean as its argument")
    Function._no_grad = not(bl)

class no_grad:
    def __init__(self):
        self.grad_enabled_status = is_grad_enabled()

    def __enter__(self):
        set_grad_enabled(False)

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            print(exc_type)
        if exc_value:
            print(exc_value)
        if traceback:
            print(traceback)
        set_grad_enabled(self.grad_enabled_status)

class enable_grad:
    def __init__(self):
        self.grad_enabled_status = is_grad_enabled()

    def __enter__(self):
        set_grad_enabled(True)

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            print(exc_type)
        if exc_value:
            print(exc_value)
        if traceback:
            print(traceback)
        set_grad_enabled(self.grad_enabled_status)
# *****************************************************************************

# math functions **************************************************************
  
def square(t):
    return t**2

def sqrt(t):
    return t**0.5
              
def absolute(t):
    return Abs.apply(t)
     
def exp(t):
    return Exp.apply(t)

def log(t):
    return Log.apply(t)

def sin(t):
    return Sin.apply(t)
            
def cos(t):
    return Cos.apply(t)
            
def tan(t):
    return Tan.apply(t)
            
def asin(t):
    return Asin.apply(t)
    
def arcsin(t):
    return Asin.apply(t)
            
def acos(t):
    return Acos.apply(t)

def arccos(t):
    return Acos.apply(t)
                
def atan(t):
    return Atan.apply(t)
    
def arctan(t):
    return Atan.apply(t)
            
def sinh(t):
    return Sinh.apply(t)
            
def cosh(t):
    return Cosh.apply(t)
            
def tanh(t):
    return Tanh.apply(t)
            
def asinh(t):
    return Asinh.apply(t)

def arcsinh(t):
    return Asinh.apply(t)

def acosh(t):
    return Acosh.apply(t)

def arccosh(t):
    return Acosh.apply(t)

def atanh(t):
    return Atanh.apply(t)

def arctanh(t):
    return Atanh.apply(t)

def maximum(t0, t1):
    return Maximum.apply(t0, t1)

def minimum(t0, t1):
    return Minimum.apply(t0, t1)

def sigmoid(t):
    return Sigmoid.apply(t)
                   
def sum(t, dim=None, keepdims=False):
    '''Returns the sum of all elements in the input tensor if dim = None. if dim is 
    int or tuple of ints, then sum across those dimensions.
    keepdims=True keeps summed axis as 1 in shape - makes easily 
    broadcastable to the original
    '''
    return Sum.apply(t, dim=dim, keepdims=keepdims)

def dot(t0,t1):
    '''Computes the dot product of two 1-D tensors.'''
    if (t0.ndim != 1) and (t1.ndim != 1):
        raise ValueError("dot computes the dot product of two 1D tensors.")
    else:
        return (t0 * t1).sum()
                
def matmul(t0, t1):
    '''Matrix product of two tensors.'''
    return Matmul.apply(t0, t1)
            
def tensordot(t0, t1, dims=2):
    '''Compute tensor dot product along specified axes.
    Given two tensors, t0 and t1, and an array_like object containing two 
    array_like objects, (t0_axes, t1_axes), sum the products of elements of
    t0 and t1 (components) over the axes specified by t0_axes and 
    t1_axes. The third argument can also be a single non-negative 
    integer_like scalar, N; if it is such, then the last N dimensions of
    t0 and the first N dimensions of t1 are summed over.
    '''
    return Tensordot.apply(t0, t1, dims=dims)
# *****************************************************************************

# dimensions manipulation functions *******************************************            
def transpose(t, dim0=None, dim1=None):
    if (dim0 is not None) and (dim0 == dim1):
        return t
    return Transpose.apply(t, dim0=dim0, dim1=dim1)

def t(matrix):
    if matrix.ndim > 2:
        raise ValueError("t() can only transpose tensors of ndim <= 2")
    return transpose(matrix)

def reduce_to(t, shape):
    '''Reduce a tensor to a given shape
    '''
    if t.shape == shape:
        return t
    if not shape:
        return t.sum(keepdims=False)
    if isinstance(shape, int):
        shape = (shape,)
    shape_t = t.shape
    n = max(len(shape), len(shape_t))
    l_t = [0 for _ in range(n)]
    l = [0 for _ in range(n)]
    l_t[-1:] = shape_t[:]
    l[-1:] = shape[:]
    out = t
    for i in zip(reversed(l_t), reversed(l)):
        n -= 1
        if (i[0]==i[1]):
            pass
        elif (i[1]<2):
            out = out.sum(dim=n, keepdims = not(i[1]==0))
        else:
            raise ValueError(f"Unable to reduce_to from {shape_t} to {shape}.")
    return out   

def broadcast_to(t, shape):
    if t.shape == shape:
        return t
    return Broadcast_To.apply(t, shape=shape)
        
def squeeze(t, dims=None):
    return Squeeze.apply(t, dims=dims)
        
def unsqueeze(t, dims):
    return Un_Squeeze.apply(t, dims=dims)
             
def reshape(t, shape):
    '''Returns a tensor with the same data and number of elements as input, but with the specified shape. 
    When possible, the returned tensor will be a view of input. Otherwise, it will be a copy. Contiguous inputs 
    and inputs with compatible strides can be reshaped without copying, but you should not depend on the copying 
    vs. viewing behavior.
    See view() on when it is possible to return a view.

    t - the tensor to be reshaped
    shape - tuple of new shape

    >>> t = arange(4)
    >>> t
    tensor([0. 1. 2. 3.]), float32)

    >>> t.reshape((2,2))
    tensor([[0. 1.]
            [2. 3.]]), float32)
    '''
    if t.shape == shape:
        return t
    return Reshape.apply(t, shape=shape, view=False)

def view(t, shape):
    '''Returns a tensor with the same data and number of elements as input, but with the specified shape. 
    If change of shape isn't possible without coping data then it gives an error.
    See also reshape().

    t - the tensor to be reshaped
    shape - tuple of new shape

    >>> t = arange(4)
    >>> t
    tensor([0. 1. 2. 3.]), float32)

    >>> t.reshape((2,2))
    tensor([[0. 1.]
            [2. 3.]]), float32)
    '''
    if t.shape == shape:
        return t
    return Reshape.apply(t, shape=shape, view=True)

def movedim(t, source, destination):
    '''Moves the dimension(s) of input at the position(s) in source to the position(s) in destination.
    Other dimensions of input that are not explicitly moved remain in their original order and appear 
    at the positions not specified in destination.
    
    input (Tensor) – the input tensor.
    source (int or tuple of ints) – Original positions of the dims to move. These must be unique.
    destination (int or tuple of ints) – Destination positions for each of the original dims. These must also be unique.
    '''
    return Movedim.apply(t, source=source, destination=destination)               
# *****************************************************************************

def amin(t, dim=None, keepdims=False):
    '''Return the minimum along a given axis.
    '''
    return Amin.apply(t, dim=dim, keepdims=keepdims)

def amax(t, dim=None, keepdims=False):
    '''Return the maximum along a given axis.
    '''
    return Amax.apply(t, dim=dim, keepdims=keepdims)



def sort(t, dim=-1):
    '''Sorts the elements of the input tensor along a given dimension 
    in ascending order by value.
    '''
    xp = _get_array_module(t)
    return as_tensor(xp.sort(t._data, axis=dim))

def flip(t, dims=None):
    '''Reverse the order of elements in an array along the given axis.
    The shape of the tensor is preserved, but the elements are reordered.
    t : Input tensor.
    dims : None or int or tuple of ints, optional - axis or axes along 
    which to flip over. The default, dims=None, will flip over all of 
    the axes of the input tensor.
    '''
    xp = _get_array_module(t)
    return as_tensor(xp.flip(t._data, axis=dims))

def mean(t, dim=None, keepdims=False, dtype=None):
    '''Compute the arithmetic mean along the specified axis.
    '''
    xp = _get_array_module(t)
    return as_tensor(xp.mean(t._data, axis=dim, keepdims=keepdims, dtype=dtype))

def median(t, dim=None, keepdims=False):
    '''Compute the median along the specified axis.
    '''
    xp = _get_array_module(t)
    return as_tensor(xp.median(t._data, axis=dim, keepdims=keepdims))

# implement cat() for concetation

# implement stack()

# Function class **************************************************************
class Function:
    _no_grad = False
    
    def __init__(self): 
        self._children = [] # List where the "children" functions of this node function
        # are stored for the purpose of backpropagation.
        self._accumulated_grad = None # This is where the "parent" functions will
        # accumulate their grads
        self._grad_track = False # this tracks whether atleast one of the arguments
        # of Function requires grad.
        self._saved_shape = None
        self._saved_dtype = None
        self._saved_device = None
        self._saved = None
        self._retain_grad = False
        self.xp = None
        
    @classmethod
    def apply(cls, *args, **kwargs): # Here it is assumed that *args only contain
        # things whose gradients will be returned in backward() and all other paramters
        # are passed in **kwargs. See for example the power Function where the exponent
        # pwr is passed as **kwargs
        inst = cls() # create an instance of this Function class.
        inst.xp = _get_array_module(*args)
        tensor_args = []
        _convert_type = None
        for arg in args:
           if is_tensor(arg) and arg._data.dtype.kind == 'f':
               _convert_type = arg._data.dtype
               break
        for arg in args:
            if not is_tensor(arg):
                arg = as_tensor(inst.xp.asarray(arg, dtype=_convert_type))
            tensor_args.append(arg.detach())
            if arg.requires_grad: # arg is a leaf tensor that requires grad populated.
                inst._children.append(Accumulate_Backward(arg))
                inst._grad_track = True
            elif arg.grad_fn: # arg is not a leaf tensor and has a grad_fn then append
                # its grad_fn in _children
                inst._children.append(arg.grad_fn)
                inst._grad_track = True
            else: # arg doesn't require grad and soes not have grad_fn therefore do not
                # keep track of this in the graph.
                inst._children.append(None)
        result = inst.forward(*tensor_args, **kwargs) # forward pass (apply the forward method).
        try:
            if not isinstance(result._data, inst.xp.ndarray):
                result._data = inst.xp.asarray(result._data)
        except:
            pass
        if inst._grad_track and is_grad_enabled() and (type(inst).__name__ == 'Set_Item'):
            args[0].grad_fn = inst
            inst._saved_shape = args[0].shape
            inst._saved_device = args[0].device
            inst._saved_dtype = args[0].dtype
        if inst._grad_track and is_grad_enabled() and is_tensor(result): # If none of the childern 
            # requires grad or Function._no_grad=True then better don't update result.grad_fn
            # so that this function object gets destroyed after returning the result
            # i.e. is untracked for backpropagation.
            result.grad_fn = inst
            inst._saved_shape = result.shape
            inst._saved_device = result.device
            inst._saved_dtype = result.dtype
        return result # return the result of forward pass.
    
    def retain_grad(self):
        self._retain_grad = True
    
    def save_for_backward(self, to_save): # to_save : single item or tuple of items (inside the
        # tuple tensors should be individual and not inside some other structure otherwise the tensors
        # won't be cloned. This might lead to some side effects if the tensor elements are then modified
        # in-place in backward(). 
        if self._grad_track and is_grad_enabled():
            if isinstance(to_save, tuple) or isinstance(to_save, list):
                self._saved = []
                for t in to_save: 
                    if is_tensor(t):
                        self._saved.append(t.detach())
                    else:
                        self._saved.append(t)
                self._saved = tuple(self._saved)
            else:
                if is_tensor(to_save):
                    self._saved = to_save.detach()
                else:
                    self._saved = to_save
                    
    def get_saved(self):
        if self._saved is not None:
            return self._saved
        else:
            raise ValueError("Trying to directly access _saved items after they have already been freed. Use \
             backward(retain_graph=True) if you need to access saved tensors after calling backward")

    def accumulate_grad(self, grad, sl=None):
        if not is_tensor(grad):
            grad = as_tensor(grad, device=self._saved_device, dtype=self._saved_dtype)
        if self._accumulated_grad is None:
            self._accumulated_grad = tensor(0.0, device=self._saved_device, dtype=self._saved_dtype)
        if sl is not None:
            if self._accumulated_grad.shape != self._saved_shape:
                self._accumulated_grad = self._accumulated_grad.broadcast_to(self._saved_shape).clone()
            if grad.numel() <= self._accumulated_grad[sl].numel():
                self._accumulated_grad[sl] += grad
            else:
                self._accumulated_grad[sl] += grad.reduce_to(self._accumulated_grad[sl].shape)
        else:
            if grad.numel() <= math_prod(self._saved_shape):
                self._accumulated_grad += grad
            else:
                self._accumulated_grad += grad.reduce_to(self._saved_shape)
    
    def get_grad(self):
        if self._retain_grad:
            return self._accumulated_grad
        else:
            raise UserWarning("grad won't be retained. Use .retain_grad() to retain")
            
    def set_grad(self, grad):
        if self._retain_grad:
            self._accumulated_grad = grad
        else:
            raise UserWarning("grad won't be retained. Use .retain_grad() to retain")  
    
    def _backward(self):
        if self._grad_track:
            if (len(self._children)==1):
                self._children[0].accumulate_grad(self.backward() * self._accumulated_grad)
            else:
                for child, grad in zip(self._children, self.backward()):
                    if child:
                        child.accumulate_grad(grad * self._accumulated_grad)

# *****************************************************************************

class Neg(Function):    
    
    def forward(self, t):
        result = as_tensor(-(t._data))
        return result   
                                          
    def backward(self):
        return -1.0


class Add(Function):    
    
    def forward(self, x, y):
        result = as_tensor(x._data + y._data)
        return result   
                                          
    def backward(self):
        return 1.0, 1.0
        

class Sub(Function):    
    
    def forward(self, x, y):
        result = as_tensor(x._data - (y._data))
        return result   
                                          
    def backward(self):
        return 1.0, -1.0
        

class Mul(Function):    
    
    def forward(self, x, y):
        result = as_tensor(x._data * y._data)
        self.save_for_backward((x, y))
        return result
    
    def backward(self):
        return self.get_saved()[1], self.get_saved()[0]
        

class Div(Function):    
    
    def forward(self, x, y):
        result = as_tensor(x._data / y._data)
        self.save_for_backward((x, y))
        return result
    
    def backward(self):
        x, y = self.get_saved()
        return 1.0/y, -x/(y**2)
        

class Pow(Function):    
    
    def forward(self, t, exponent):
        result = as_tensor((t._data)**exponent)
        self.save_for_backward((t, exponent))
        return result
    
    def backward(self):
        t, n = self.get_saved()
        return n*t**(n-1)


class Abs(Function):    
    
    def forward(self, t):
        self.save_for_backward(t)
        return as_tensor(self.xp.absolute(t._data))  
                                          
    def backward(self):
        t = self.get_saved().clone()
        t[t>=0] = 1.0
        t[t<0] = -1.0
        return t


class Exp(Function):    
    
    def forward(self, t):
        result = as_tensor(self.xp.exp(t._data))
        self.save_for_backward(result)
        return result
                                          
    def backward(self):
        return self.get_saved()


class Log(Function):    
    
    def forward(self, t):
        self.save_for_backward(t)
        return as_tensor(self.xp.log(t._data))
                                          
    def backward(self):
        return 1.0/self.get_saved()


class Sin(Function):    
    
    def forward(self, t):
        self.save_for_backward(t)
        return as_tensor(self.xp.sin(t._data))
                                          
    def backward(self):
        return cos(self.get_saved())


class Cos(Function):    
    
    def forward(self, t):
        self.save_for_backward(t)
        return as_tensor(self.xp.cos(t._data))
                                          
    def backward(self):
        return -sin(self.get_saved())


class Tan(Function):    
    
    def forward(self, t):
        self.save_for_backward(t)
        return as_tensor(self.xp.tan(t._data))
                                          
    def backward(self):
        return square(1.0/cos(self.get_saved()))


class Asin(Function):    
    
    def forward(self, t):
        self.save_for_backward(t)
        return as_tensor(self.xp.arcsin(t._data))
                                          
    def backward(self):
        return 1.0/sqrt(1.0 - square(self.get_saved()))


class Acos(Function):    
    
    def forward(self, t):
        self.save_for_backward(t)
        return as_tensor(self.xp.arccos(t._data))
                                          
    def backward(self):
        return -1.0/sqrt(1.0 - square(self.get_saved()))


class Atan(Function):    
    
    def forward(self, t):
        self.save_for_backward(t)
        return as_tensor(self.xp.arctan(t._data))
                                          
    def backward(self):
        return 1.0/(1.0 + square(self.get_saved()))


class Sinh(Function):    
    
    def forward(self, t):
        self.save_for_backward(t)
        return as_tensor(self.xp.sinh(t._data))
                                          
    def backward(self):
        return cosh(self.get_saved())


class Cosh(Function):    
    
    def forward(self, t):
        self.save_for_backward(t)
        return as_tensor(self.xp.cosh(t._data))
                                          
    def backward(self):
        return sinh(self.get_saved())


class Tanh(Function):    
    
    def forward(self, t):
        result = as_tensor(self.xp.tanh(t._data))
        self.save_for_backward(result)
        return result
                                          
    def backward(self):
        return 1.0 - square(self.get_saved())


class Asinh(Function):    
    
    def forward(self, t):
        self.save_for_backward(t)
        return as_tensor(self.xp.arcsinh(t._data))
                                          
    def backward(self):
        return 1.0/sqrt(square(self.get_saved()) + 1.0)


class Acosh(Function):    
    
    def forward(self, t):
        self.save_for_backward(t)
        return as_tensor(self.xp.arccosh(t._data))
                                          
    def backward(self):
        return 1.0/sqrt(square(self.get_saved()) - 1.0)


class Atanh(Function):    
    
    def forward(self, t):
        self.save_for_backward(t)
        return as_tensor(self.xp.arctanh(t._data))
                                          
    def backward(self):
        return 1.0/(1.0 - square(self.get_saved()))


class Sum(Function):    
    
    def forward(self, t, dim, keepdims):
        result = t._data.sum(axis=dim, keepdims=keepdims, dtype=t.dtype)
        self.save_for_backward((keepdims, dim))
        return as_tensor(result)
    
    def _backward(self):
        if self.get_saved()[0]:
            self._children[0].accumulate_grad(self._accumulated_grad)
        else:
            dim = self.get_saved()[1]
            if dim is None:
                dim = tuple(range(len(self._saved_shape)))
            self._children[0].accumulate_grad(self._accumulated_grad.unsqueeze(dim))


class Maximum(Function):
    
    def forward(self, t0, t1):
        self.save_for_backward((t0, t1))
        return as_tensor(self.xp.maximum(t0._data, t1._data))

    def _backward(self):
        if self._grad_track:
            t0, t1 = self.get_saved()
            r = t0 == t1
            if self._children[0]:
                r0 = t0 > t1
                self._children[0].accumulate_grad(self._accumulated_grad * (r0.to(dtype=t0.dtype) + r.to(dtype=t0.dtype) / 2.0))
            if self._children[1]:
                r1 = t0 < t1
                self._children[1].accumulate_grad(self._accumulated_grad * (r1.to(dtype=t1.dtype) + r.to(dtype=t1.dtype) / 2.0))


class Minimum(Function):
    
    def forward(self, t0, t1):
        self.save_for_backward((t0, t1))
        return as_tensor(self.xp.minimum(t0._data, t1._data))

    def _backward(self):
        if self._grad_track:
            t0, t1 = self.get_saved()
            r = t0 == t1
            if self._children[0]:
                r0 = t0 < t1
                self._children[0].accumulate_grad(self._accumulated_grad * (r0.to(dtype=t0.dtype) + r.to(dtype=t0.dtype) / 2.0))
            if self._children[1]:
                r1 = t0 > t1
                self._children[1].accumulate_grad(self._accumulated_grad * (r1.to(dtype=t1.dtype) + r.to(dtype=t1.dtype) / 2.0))


class Sigmoid(Function):
    
    def forward(self, t):
        result = as_tensor(1.0 / (1.0 + self.xp.exp(-(t._data))))
        self.save_for_backward(result)
        return result
    
    def backward(self):
        result = self.get_saved()
        return result * (1.0 - result)


class Matmul(Function):

    def forward(self, t0, t1):
        self.save_for_backward((t0, t1))
        return as_tensor(self.xp.matmul(t0._data, t1._data))
    
    def _backward(self):
        if self._grad_track:
            t0, t1 = self.get_saved()
            if self._children[1]:
                if t0.ndim == 1:
                    self._children[1].accumulate_grad(matmul(transpose(t0.unsqueeze(0),-1,-2), 
                                                            self._accumulated_grad.unsqueeze(0)).reshape(t1.shape))
                else:
                    self._children[1].accumulate_grad(matmul(transpose(t0,-1,-2), self._accumulated_grad).reshape(t1.shape))
            if self._children[0]:
                if t1.ndim == 1:
                    self._children[0].accumulate_grad(matmul(self._accumulated_grad.unsqueeze(1),  
                                                            transpose(t1.unsqueeze(1),-1,-2)).reshape(t0.shape))
                else:
                    self._children[0].accumulate_grad(matmul(self._accumulated_grad, transpose(t1,-1,-2)).reshape(t0.shape))


class Tensordot(Function):

    def forward(self, t0, t1, dims):
        self.save_for_backward((t0, t1, dims))
        return as_tensor(self.xp.tensordot(t0._data, t1._data, dims))
    
    def _backward(self):
        if self._grad_track:
            t0, t1, dims = self.get_saved()
            if isinstance(dims, int):
                t0_dims = list(range(t0.ndim-dims))
                t1_dims = list(range(t1.ndim))[dims:]
            else:
                t0_dims = list(range(t0.ndim))
                for i in dims[0]:
                    t0_dims.remove(i)
                t1_dims = list(range(t1.ndim))
                for i in dims[1]:
                    t1_dims.remove(i)
            grad_dims = list(range(len(t0_dims + t1_dims)))
            grad0_dims = (grad_dims[len(t0_dims):], t1_dims)
            grad1_dims = (t0_dims, grad_dims[:len(t0_dims)])
            if self._children[0]:
                grad0 = tensordot(self._accumulated_grad, t1, grad0_dims)
            if self._children[1]:
                grad1 = tensordot(t0, self._accumulated_grad, grad1_dims)
            if not isinstance(dims, int): 
                dict_t0_t1 = {i:j for i,j in zip(dims[0],dims[1])}
                dict_t1_t0 = {i:j for i,j in zip(dims[1],dims[0])}
                original0_dims = list(range(-len(dims[0]), 0))
                original1_dims = list(range(len(dims[0])))
                dims0_sort = list(dims[0])
                dims0_sort.sort()
                dims1_sort = list(dims[1])
                dims1_sort.sort()
                new0_dims = [dict_t1_t0[i] for i in dims1_sort]
                new1_dims = [dict_t0_t1[i] for i in dims0_sort]
                if self._children[0]:
                    grad0 = movedim(grad0, original0_dims, new0_dims)
                if self._children[1]:
                    grad1 = movedim(grad1, original1_dims, new1_dims)
            if self._children[0]:
                self._children[0].accumulate_grad(grad0)
            if self._children[1]: 
                self._children[1].accumulate_grad(grad1)


class Amin(Function):

    def forward(self, t, dim=None, keepdims=False):
        if is_tensor(dim):
            dim = int(dim.item())
        if (dim is not None) and (not isinstance(dim, int)):
            raise ValueError("dim should be an int")
        result = as_tensor(self.xp.amin(t._data, axis=dim, keepdims=keepdims))
        self.save_for_backward((dim, keepdims, t, result))
        return result
    
    def _backward(self):
        if self._grad_track:
            dim, keepdims, t, result = self.get_saved()
            if not keepdims:
                if dim is None:
                    dim = tuple([i for i in range(t.ndim)])
                grad = self._accumulated_grad.unsqueeze(dim)
                result = result.unsqueeze(dim)
            else:
                grad = self._accumulated_grad
            comp = (t==result).to(dtype=t.dtype)
            comp = comp / comp.sum(dim, keepdims=True)
            self._children[0].accumulate_grad(grad * comp)


class Amax(Function):

    def forward(self, t, dim=None, keepdims=False):
        if is_tensor(dim):
            dim = int(dim.item())
        if (dim is not None) and (not isinstance(dim, int)):
            raise ValueError("dim should be an int")
        result = as_tensor(self.xp.amax(t._data, axis=dim, keepdims=keepdims))
        self.save_for_backward((dim, keepdims, t, result))
        return result
    
    def _backward(self):
        if self._grad_track:
            dim, keepdims, t, result = self.get_saved()
            if not keepdims:
                if dim is None:
                    dim = tuple([i for i in range(t.ndim)])
                grad = self._accumulated_grad.unsqueeze(dim)
                result = result.unsqueeze(dim)
            else:
                grad = self._accumulated_grad
            comp = (t==result).to(dtype=t.dtype)
            comp = comp / comp.sum(dim, keepdims=True)
            self._children[0].accumulate_grad(grad * comp)


class Broadcast_To(Function):

    def forward(self, t, shape):
        if self._grad_track and is_grad_enabled():
            self.save_for_backward(t.shape)
        return as_tensor(self.xp.broadcast_to(t._data, shape))
    
    def _backward(self):
        if self._grad_track:
            self._children[0].accumulate_grad(self._accumulated_grad.reduce_to(self.get_saved()))


class Copy_To(Function):

    def forward(self, t, dtype=None, device=None):
        if self._grad_track and is_grad_enabled():
            self.save_for_backward((t.dtype, t.device))
        if dtype is None:
            dtype = t.dtype
        if device is None:
            device = t.device
        return tensor(t._data, dtype=dtype, device=device)
    
    def _backward(self):
        if self._grad_track:
            dtype = self.get_saved()[0]
            device = self.get_saved()[1]
            self._children[0].accumulate_grad(self._accumulated_grad.to(dtype=dtype, device=device))


class Squeeze(Function):

    def forward(self, t, dims):
        if dims==None:
            if self._grad_track and is_grad_enabled():
                calc_dims = tuple([i for i in range(len(t.shape)) if t.shape[i]==1])
                self.save_for_backward(calc_dims)
            return as_tensor(t._data.squeeze())
        else:
            self.save_for_backward(dims)
            return as_tensor(t._data.squeeze(dims))
    
    def _backward(self):
        if self._grad_track:
            dims = self.get_saved()
            self._children[0].accumulate_grad(self._accumulated_grad.unsqueeze(dims))


class Un_Squeeze(Function):

    def forward(self, t, dims):
        self.save_for_backward(dims)
        return as_tensor(self.xp.expand_dims(t._data, dims))
    
    def _backward(self):
        if self._grad_track:
            dims = self.get_saved()
            self._children[0].accumulate_grad(self._accumulated_grad.squeeze(dims))


class Transpose(Function):

    def forward(self, t, dim0=None, dim1=None):
        t_ndim = t.ndim
        if (t_ndim <=2):
            return as_tensor(self.xp.transpose(t._data))
        dim0 = (t_ndim+dim0) if dim0<0 else dim0
        dim1 = (t_ndim+dim1) if dim1<0 else dim1
        l = list(range(t_ndim))
        l[dim0], l[dim1] = dim1, dim0
        self.save_for_backward((dim0, dim1))
        return as_tensor(self.xp.transpose(t._data, axes=l))
    
    def _backward(self):
        if self._grad_track:
            if self._saved is None:
                self._children[0].accumulate_grad(self._accumulated_grad.t())
            else:
                dim0, dim1 = self.get_saved()
                self._children[0].accumulate_grad(self._accumulated_grad.transpose(dim0, dim1))


class Reshape(Function):    
    
    def forward(self, t, shape, view):
        if view:
            result_data = t._data.view()
            result_data.shape = shape
            result = as_tensor(result_data)
        else:
            result = as_tensor(t._data.reshape(shape))
        self.save_for_backward(t.shape)
        return result
    
    def _backward(self):
        if self._grad_track:
            self._children[0].accumulate_grad(self._accumulated_grad.reshape(self.get_saved()))


class Get_Item(Function):    
    
    def forward(self, t, sl):
        if is_tensor(sl):
            sl = sl._data
            if (type(sl).__module__ == 'cupy') and (self.xp.__name__ == 'numpy'):
                sl = sl.get()
        result = as_tensor(t._data[sl])
        self.save_for_backward(sl)
        return result
  
    # Custom _backward for this to update only the slice of 
    # _accumulate_grad instead of passing entire gradient with lots 
    # of zeros. (for efficiency)
    def _backward(self):
        if self._grad_track:
            self._children[0].accumulate_grad(self._accumulated_grad,\
                                          sl = self.get_saved())


class Set_Item(Function):    
    
    def forward(self, t, value, sl):
        if is_tensor(sl):
            sl = sl._data
            if (type(sl).__module__ == 'cupy') and (self.xp.__name__ == 'numpy'):
                sl = sl.get()
        t._data[sl] = value._data
        self.save_for_backward(sl)
    
    def _backward(self):
        if self._grad_track:
            grad = self._accumulated_grad.clone()
            if self._children[1]:
                self._children[1].accumulate_grad(grad[self.get_saved()])
            if self._children[0]:
                grad[self.get_saved()] = tensor(0.0)
                self._children[0].accumulate_grad(grad)
    

class Movedim(Function):
    
    def forward(self, t, source, destination):
        self.save_for_backward((destination, source))
        return as_tensor(self.xp.moveaxis(t._data, source, destination))
    
    def _backward(self):
        if self._grad_track:
            self._children[0].accumulate_grad(movedim(self._accumulated_grad, *self.get_saved()))


class Accumulate_Backward(Function):

    def __init__(self, t):
        self._leaf_tensor = t
        self._saved_shape = t.shape
        self._saved_dtype = t.dtype
        self._saved_device = t.device
        self._children = []
        self._accumulated_grad = None
        self._retain_grad = False
        self._grad_track = False

    @classmethod
    def apply(cls):
        return None

    def accumulate_grad(self, grad, sl=None):
        t = self._leaf_tensor
        if t.requires_grad:
            if not is_tensor(grad):
                grad = as_tensor(grad, device=self._saved_device, dtype=self._saved_dtype)
            if self._saved_device != grad.device:
                grad = tensor(grad._data, device=self._saved_device, dtype=self._saved_dtype)
            if t._grad is None:
                t._grad = zeros(*self._saved_shape, dtype=self._saved_dtype, device=self._saved_device)
            if sl is not None:
                if grad.numel() <= t._grad[sl].numel():
                    t._grad[sl] += grad
                else:
                    t._grad[sl] += grad.reduce_to(t._grad[sl].shape)
            else:
                if grad.numel() <= t._grad.numel():
                    t._grad += grad
                else:
                    t._grad += grad.reduce_to(self._saved_shape)._data

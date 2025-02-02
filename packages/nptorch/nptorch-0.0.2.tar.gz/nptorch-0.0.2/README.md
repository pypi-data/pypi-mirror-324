# nptorch
A lightweight PyTorch clone - deep learning library built using **NumPy** (for CPU) and **CuPy** (for GPU). Ideal for understanding the core concepts of deep learning, backpropagation, automatic differentiation, and tensor operations in a minimalistic, easy-to-follow implementation. May be practically useful in scenarios where the library's small size and low dependency requirements are advantageous.

## Install nptorch using pip:

```bash
pip install nptorch

## Getting Started


```python
import nptorch as nt

# Create tensors
x = nt.tensor([[1.0, 2], [3, 4]], requires_grad=True)
y = nt.tensor([[5.0, 6], [7, 8]], requires_grad=True)

# Perform operations
z = x + y
w = z.mean()
w.backward()

# Print results
print("z:", z)
print("x.grad:", x.grad)
print("y.grad:", y.grad)
```

    z: tensor([[ 6.  8.]
            [10. 12.]], float32, grad_fn=<'Add' at 0x722942528260>)
    x.grad: tensor([[0.25 0.25]
            [0.25 0.25]], float32)
    y.grad: tensor([[0.25 0.25]
            [0.25 0.25]], float32)



```python

```

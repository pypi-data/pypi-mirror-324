from .. import core
from . import functional_classes as fc


def pad(t, pad, mode='constant', value=0):
    # to be corrected for tuple of all zeros
    if pad == 0:
        return t
    return fc.Pad.apply(t, pad=pad, mode=mode, value=value)

def relu(t):
    return fc.Relu.apply(t)

def softmax(t, dim=None):
    return fc.Softmax.apply(t, dim=dim)

def conv2d(x, w, stride=1, padding=0):

    N, C, H, W = x.shape
    num_filters, _, filter_height, filter_width = w.shape

    out_height = (H + 2 * padding - filter_height) // stride + 1
    out_width = (W + 2 * padding - filter_width) // stride + 1

    out = core.zeros(N, num_filters, out_height, out_width, dtype=x.dtype, device=x.device)

    x_cols = fc.im2col_indices(x, w.shape[2], w.shape[3], padding=padding, stride=stride)
    res = w.reshape((w.shape[0], -1)).matmul(x_cols)

    out = res.reshape((w.shape[0], out.shape[2], out.shape[3], x.shape[0]))
    out = core.movedim(out, (3, 0, 1, 2), (0, 1, 2, 3))
    
    return out.contiguous()

def max_pool2d(t, kernel_size, stride=None, padding=None, return_indices=False):
    if padding is not None:
        t = pad(t, padding)
    if isinstance(kernel_size, int):
        fh, fw = kernel_size, kernel_size
    else:
        fh, fw = kernel_size
    if stride is None:
        stride_h, stride_w = fh, fw
    elif isinstance(stride, int):
        stride_h, stride_w = stride, stride
    else:
        stride_h, stride_w = stride
    _, _, h, w = t.shape
    result = t[:,:,:h-fh+1:stride_h,:w-fw+1:stride_w]
    for i in range(fh):
        for j in range(fw):
            if (i != 0) or (j != 0):
                result = core.maximum(result, t[:,:,i:h-fh+1+i:stride_h,j:w-fw+1+j:stride_w])
    return result

def dropout(t, p=0.5, training=True, inplace=False):
    if training:
        if inplace:
            mask = core.rand_like(t) < p
            t[:] *= 1.0/(1.0-p)
            t[mask] = 0.0
        else:
            mask = core.rand_like(t) > p
            return t * (1.0/(1.0-p)) * mask
    else:
        return t


            
from .. import core


class Pad(core.Function):

    def forward(self, t, pad, mode, value):
        if isinstance(pad, int):
            pad = (pad,pad,pad,pad)
        assert len(pad)%2 == 0
        pad_width = [(pad[i], pad[i+1]) for i in range(0, len(pad), 2)]
        pad_width_remaining = [(0, 0) for _ in range(t.ndim - len(pad_width))]
        pad_width = pad_width + pad_width_remaining
        pad_width.reverse()
        pad_width = tuple(pad_width)
        self.save_for_backward(pad_width)
        return core.as_tensor(self.xp.pad(t._data, pad_width, mode=mode, constant_values=value))

    def _backward(self):
        if self._grad_track:
            pad_width = self.get_saved()
            slices = tuple([slice(padding_left, -padding_right if padding_right else None, None) for (padding_left, padding_right) in pad_width])
            self._children[0].accumulate_grad(self._accumulated_grad[slices])

class Relu(core.Function):
    
    def forward(self, t):
        result = t.clone()
        if self._grad_track and core.is_grad_enabled():
            self.save_for_backward((result > 0).to(dtype=result.dtype))
        result[result<0] = 0.0
        return result
    
    def backward(self):
        return self.get_saved()

class Softmax(core.Function):

    def forward(self, t, dim):
        if not isinstance(dim, int):
            raise ValueError("dim should be an int")
        exps = self.xp.exp(t._data - t._data.max(axis=dim, keepdims=True))
        result = core.as_tensor(exps/exps.sum(axis=dim, keepdims=True))
        self.save_for_backward((result, dim))
        return result

    def _backward(self):
        if self._grad_track:
            dim = self.get_saved()[1]
            s = self.get_saved()[0]
            ag = self._accumulated_grad
            result = s * ag
            result -= s * result.sum(dim=dim, keepdims=True)
            self._children[0].accumulate_grad(result)

def im2col_indices(x, field_height, field_width, padding=0, stride=1):
    return Im2col_Indices.apply(x, field_height=field_height, field_width=field_width, padding=padding, stride=stride)

class Im2col_Indices(core.Function):

    def get_im2col_indices(self, x_shape, field_height, field_width, padding, stride):
        N, C, H, W = x_shape
        out_height = (H + 2 * padding - field_height) // stride + 1
        out_width = (W + 2 * padding - field_width) // stride + 1
        i0 = self.xp.repeat(self.xp.arange(field_height), field_width)
        i0 = self.xp.tile(i0, C)
        i1 = stride * self.xp.repeat(self.xp.arange(out_height), out_width)
        j0 = self.xp.tile(self.xp.arange(field_width), field_height * C)
        j1 = stride * self.xp.tile(self.xp.arange(out_width), out_height)
        i = i0.reshape((-1, 1)) + i1.reshape((1, -1))
        j = j0.reshape((-1, 1)) + j1.reshape((1, -1))
        k = self.xp.repeat(self.xp.arange(C), field_height * field_width).reshape((-1, 1))
        return (k, i, j)
    
    def forward(self, x, field_height, field_width, padding, stride):
        x_padded = core.pad(x, padding)
        k, i, j = self.get_im2col_indices(x.shape, field_height, field_width, padding, stride)
        cols = x_padded[:, k, i, j]
        C = x.shape[1]
        cols = core.movedim(cols, (1,2,0), (0,1,2)).reshape((field_height * field_width * C, -1))
        self.save_for_backward((x.shape, field_height, field_width, padding, stride))
        return cols
    
    def _backward(self):
        if self._grad_track:
            x_shape, field_height, field_width, padding, stride = self.get_saved()
            cols = self._accumulated_grad
            N, C, H, W = x_shape
            H_padded, W_padded = H + 2 * padding, W + 2 * padding
            x_padded = core.zeros(N, C, H_padded, W_padded, dtype=cols.dtype, device=cols.device)
            k, i, j = self.get_im2col_indices(x_shape, field_height, field_width, padding, stride)
            cols_reshaped = cols.reshape((C * field_height * field_width, -1, N))
            cols_reshaped = core.movedim(cols_reshaped, (2, 0, 1), (0, 1, 2))
            if self.xp.__name__ == 'numpy':
                self.xp.add.at(x_padded._data, (slice(None), k, i, j), cols_reshaped._data)
            else:
                self.xp.cupyx.scatter_add(x_padded._data, (slice(None), k, i, j), cols_reshaped._data)
            if padding != 0:
                x_padded = x_padded[:, :, padding:-padding, padding:-padding]
            self._children[0].accumulate_grad(x_padded)

            
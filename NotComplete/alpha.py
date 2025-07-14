import math
import random

#la methode pour le determinant a un pb
        

class Array:

    def __init__(self, data):
        if isinstance(data, Array):
            self.data = data
            self.shape = data.shape
            self.dtype = data.dtype
            return
        if not isinstance(data, list):
            raise TypeError("Data must be a list")
        self.data = data
        self.shape = self._calculate_shape()
        self.size = self._calculate_size()
        self.dtype = self._dtype()
        
    def __repr__(self):
        return f'Array({self.data})'

    def __getitem__(self, key):
        if isinstance(key, int):
            try:
                result = self.data[0][key]
            except:
                pass
            finally:
                result = self.data[key]

            if isinstance(result, list):
                return Array(result)
            elif isinstance(result, Array):
                return result.data
            return result
        elif isinstance(key, slice):
            if len(self.shape) == 1:
                return Array(self.data[key])
            if len(self.shape) == 2:
                if self.shape[0] == 1:
                    return Array(self.data[0][key])
                elif self.shape[1] == 1:
                    l = self.ravel()
                    return Array(l[key])
                else:
                    start1, stop1, step1 = key.start, key.stop, key.step
                    slices = [slice(None)] * len(self.shape)
                    slices[1] = slice(start1, stop1, step1)
                    result_data = []
                    for row in self.data:
                        result_data.append(row[tuple(slices)])
                    return Array(result_data)
            else:
                raise ValueError("Array must have one or two dimensions")
        elif isinstance(key, list):
            return Array([self.data[i] for i in key])
        elif isinstance(key, tuple):
            result = self.data
            for i, k in enumerate(key):
                if i == 0:
                    if isinstance(k, slice):
                        start, stop, step = k.start, k.stop, k.step
                        if start is None and stop is None and step is None:
                            result = result[:]
                        else:
                            result = result[k]
                    elif isinstance(k, int):
                        result = result[k]
                    elif isinstance(k, (list)):
                        result = [result[i] for i in k]
                    else:
                        raise TypeError("Unsupported indexing type")
                else:
                    if isinstance(k, slice):
                        start, stop, step = k.start, k.stop, k.step
                        if start is None and stop is None and step is None:
                            result = result[:]
                        else:
                            result = [r[k] for r in result]
                    elif isinstance(k, int):
                        result = [r[k] for r in result]
                    elif isinstance(k, (list)):
                        result = [r[i] for r in result for i in k]
                    else:
                        raise TypeError("Unsupported indexing type")
            return Array(result) if isinstance(result, list) else result
        elif isinstance(key, bool):
            return Array([x for i, x in enumerate(self.data) if key[i]])
        elif isinstance(key, Array):
            if key.dtype != bool:
                raise TypeError("Boolean index array should contain booleans")
            if key.shape != self.shape:
                raise ValueError("Boolean index array shape mismatch")
            result = []
            if len(key.shape) == 1:
                for j in range(self.shape[0]):
                    if key.data[j]:
                        result.append(self.data[j])
            elif len(key.shape) > 1:
                for i in range(self.shape[0]):
                    r = []
                    for j in range(self.shape[1]):
                        if key.data[i][j]:
                            r.append(self.data[i][j])
                    result.append(r)
            return Array(result)
        elif isinstance(key, str):
            return Array([sub_dict[key] for sub_dict in self.data if isinstance(sub_dict, dict) and key in sub_dict])
        # elif isinstance(key, np.ndarray):
        #     if key.dtype == bool:
        #         return Array([self.data[i] for i in range(len(self.data)) if key[i]])
        #     else:
        #         return Array([self.data[i] for i in key])
        else:
            raise TypeError("Unsupported indexing type")
        
    def __setitem__(self, key, value):
        if isinstance(key, int):
            self.data[key] = value.data if isinstance(value, Array) else value
        elif isinstance(key, slice):
            self.data[key] = value.data if isinstance(value, Array) else value
        elif isinstance(key, list):
            for i, v in zip(key, value):
                self.data[i] = v.data if isinstance(v, Array) else v
        elif isinstance(key, tuple):
            target = self.data
            for k in key[:-1]:
                if isinstance(k, int):
                    target = target[k]
                elif isinstance(k, slice):
                    target = target[k]
                elif isinstance(k, (list, np.ndarray)): # type: ignore
                    target = [target[i] for i in k]
                else:
                    raise TypeError("Unsupported indexing type")
            if isinstance(key[-1], int):
                target[key[-1]] = value.data if isinstance(value, Array) else value
            elif isinstance(key[-1], slice):
                target[key[-1]] = value.data if isinstance(value, Array) else value
            elif isinstance(key[-1], (list, np.ndarray)): # type: ignore
                for i, v in zip(key[-1], value):
                    target[i] = v.data if isinstance(v, Array) else v
            else:
                raise TypeError("Unsupported indexing type")
        elif isinstance(key, bool):
            for i, v in enumerate(value):
                if key[i]:
                    self.data[i] = v.data if isinstance(v, Array) else v
        elif isinstance(key, Array):
            if key.dtype != bool:
                raise TypeError("Boolean index array should contain booleans")
            if key.shape != self.shape:
                raise ValueError("Boolean index array shape mismatch")
            if not isinstance(value, (int, float, Array)):
                raise TypeError("Value must be a number or an Array")
            value_array = value if isinstance(value, Array) else Array([[value]])
            value_index = 0
            for i in range(self.shape[0]):
                for j in range(self.shape[1]):
                    if key.data[i][j]:
                        self.data[i][j] = value_array.data[value_index % value_array.size]
                        value_index += 1
        elif isinstance(key, str):
            for sub_dict in self.data:
                if isinstance(sub_dict, dict) and key in sub_dict:
                    sub_dict[key] = value
        elif isinstance(key, np.ndarray): # type: ignore
            if key.dtype == bool:
                for i, v in enumerate(value):
                    if key[i]:
                        self.data[i] = v.data if isinstance(v, Array) else v
            else:
                for i, v in zip(key, value):
                    self.data[i] = v.data if isinstance(v, Array) else v
        else:
            raise TypeError("Unsupported indexing type")
    def __len__(self):
        return self.size

    def __contains__(self, x):
        def _contains(arr, x):
            if len(arr.shape) == 1:
                return x in arr.data
            else:
                for subarr in arr.data:
                    if _contains(subarr, x):
                        return True
                return False
        return _contains(self, x)

    def __concat__(self, other, axis=0):
        if isinstance(other, list):
            other = Array(other)
        if not isinstance(other, Array):
            raise ValueError("Operand must be of type Array or list")

        def _concat(arr1, arr2, axis=0):
            if isinstance(arr1, list) and isinstance(arr2, list):
                if axis == 0:
                    return arr1 + arr2
                else:
                    result_data = []
                    # if not isinstance(arr1, Array):
                    #     arr1 = Array(arr1)
                    # if not isinstance(arr2, Array):
                    #     arr2 = Array(arr2)
        
                    for subarr1, subarr2 in zip(arr1, arr2):
                        result_data.append(_concat(subarr1, subarr2, axis - 1))
                    return result_data
            elif isinstance(arr1, Array) and isinstance(arr2, Array):
                return Array(_concat(arr1.data, arr2.data, axis))
            else:
                raise ValueError("Incompatible types for concatenation")

        if axis < -len(self.shape) or axis >= len(self.shape):
            raise ValueError("Invalid axis")

        if axis < 0:
            axis += len(self.shape)

        return _concat(self, other, axis)


    def __or__(self, other):
        if not isinstance(other, Array):
            raise ValueError("Operand must be of type Array")

        def _or(arr1, arr2):
            if len(arr1.shape) == 1:
                return Array([a or b for a, b in zip(arr1.data, arr2.data)])
            else:
                result_data = []
                for subarr1, subarr2 in zip(arr1.data, arr2.data):
                    result_data.append(_or(subarr1, subarr2).data)
                return Array(result_data)

        return _or(self, other)

    def __and__(self, other):
        if not isinstance(other, Array):
            raise ValueError("Operand must be of type Array")

        def _and(arr1, arr2):
            if len(arr1.shape) == 1:
                return Array([a and b for a, b in zip(arr1.data, arr2.data)])
            else:
                result_data = []
                for subarr1, subarr2 in zip(arr1.data, arr2.data):
                    result_data.append(_and(subarr1, subarr2).data)
                return Array(result_data)

        return _and(self, other)

    def __not__(self):
        def _not(arr):
            if len(arr.shape) == 1:
                return Array([not elem for elem in arr.data])
            else:
                result_data = []
                for subarr in arr.data:
                    result_data.append(_not(subarr).data)
                return Array(result_data)

        return _not(self)
    def __eq__(self, other):
        return self.elementwise_op(other, lambda x, y: x == y)

    def __gt__(self, other):
        return self.elementwise_op(other, lambda x, y: x > y)

    def __lt__(self, other):
        return self.elementwise_op(other, lambda x, y: x < y)

    def __ge__(self, other):
        return self.elementwise_op(other, lambda x, y: x >= y)

    def __le__(self, other):
        return self.elementwise_op(other, lambda x, y: x <= y)

    def __ne__(self, other):
        return self.elementwise_op(other, lambda x, y: x != y)

    def _dtype(self):
        def _dt(arr):
            if len(arr.shape) == 0:
                return type(arr.data)
            elif len(arr.shape) == 1:
                return type(arr.data[0])
            else:
                return _dt(arr[0])

        return _dt(self)


    def __str__(self, decimal_places=4, digit=6):
        if len(self.shape) == 0:
            return "Array([])"

        def format_element(element):
            if isinstance(element, list):
                return " [" + " ".join(map(format_element, element)) + "]"
            elif isinstance(element, (int, float)):
                return "{:>{}.{}e}".format(element, digit + decimal_places + 1, decimal_places)
            else:  # Handle strings or other types
                return str(element)

        if len(self.shape) == 1:
            return f"\033[36;3;242mArray({', '.join(map(format_element, self.data))})\033[0m"

        array_str = "\033[36;3;242m["
        for index in range(len(self.data)):
            array_str += "\n"
            array_str += format_element(self.data[index])
            array_str += " "

        array_str += "\n]\033[0m"

        return array_str



    def __float__(self):
        return self._unary_elementwise_op(float)

    def __int__(self):
        return self._unary_elementwise_op(int)

         
    def __add__(self, other):
        return self.add(other)
    
    def __radd__(self, other):
        return self.add(other)


    def __sub__(self, other):
        return self.subtract(other)
    
    def __rsub__(self, other):
        return self.elementwise_op(other, lambda x, y: y - x)
    
    def __mod__(self, other):
        return self.mod(other)
    def __rmod__(self, other):
        return self.mod(other)
    
    def __truediv__(self, other):
        return self.divide(other)
    
    def __rtruediv__(self, other):
        return self.elementwise_op(other, lambda x, y: y/x)

    
    def __itruediv__(self, other):
        self = self/other
        return self
    
    def __mul__(self, other):
        return self.multiply(other)
    
    def __rmul__(self, other):
        return self * other

    def __floordiv__(self, other):
        return self.elementwise_op(other, lambda x, y: x // y)
        
    def __matmul__(self, other):
        return self.matmul(other)
    
    def __pow__(self, exp):
        return self.elementwise_op(exp, lambda x, y: x ** y)

    def __rpow__(self, other):
        return Array([[other]]).elementwise_op(self, lambda x, y: x ** y)

    def __neg__(self):
        return self * -1
    
    def __pos__(self):
        return self

    def __sqrt__(self):
        return self._unary_elementwise_op(lambda x: math.sqrt(x))
    def __abs__(self):
        return self._unary_elementwise_op(lambda x: abs(x))


    def contains(self, x):
        return self.__contains__(x)
    

    def _calculate_shape(self):
        def get_dimension_shape(arr):
            if isinstance(arr, list):
                if len(arr) == 0:
                    return (len(arr),)    
                return (len(arr),) + get_dimension_shape(arr[0])
            else:
                return ()
        shape = get_dimension_shape(self.data)
        return shape

    def _calculate_size(self):
        x = 1
        for i in range(len(self.shape)):
            x = x * self.shape[i]
        return x
    
    
    def float(self):
        return self.__float__()


    def int(self):
        return self.__int__()


    def to_list(self):
        return self.data

    def to_ndarray(self):
        try:
            import numpy as np
            return np.array(self.data)
        except Exception as e:
            print("Error:"+e)
            
    @classmethod
    def from_ndarray(cls, ndarray):
        return cls(ndarray.tolist())

    @staticmethod
    def _broadcast(arr1, arr2):
        if isinstance(arr1, Array): 
            shape1 = arr1.shape
        else:
            arr1 = Array(arr1)
            shape1 = arr1.shape
        
        if isinstance(arr2, Array): 
            shape2 = arr2.shape 
        else: 
            arr2 = Array(arr2)
            shape2 = arr2.shape

        # Determine the output shape
        output_shape = []
        max_dims = max(len(shape1), len(shape2))
        shape1 = (1,) * (max_dims - len(shape1)) + shape1
        shape2 = (1,) * (max_dims - len(shape2)) + shape2
        
        for s1, s2 in zip(shape1, shape2):
            if s1 == s2:
                output_shape.append(s1)
            elif s1 == 1:
                output_shape.append(s2)
            elif s2 == 1:
                output_shape.append(s1)
            elif s1 == s2 and s1 == -1:
                output_shape.append(s1)
            else:
                raise ValueError(f"Cannot broadcast shapes {shape1} and {shape2}")
        
        output_shape = tuple(output_shape)
        
        broadcasted_arr1 = Array._broadcast_to_shape(arr1, output_shape)
        broadcasted_arr2 = Array._broadcast_to_shape(arr2, output_shape)
             
        return broadcasted_arr1, broadcasted_arr2


    
    @staticmethod
    def _broadcast_to_shape(arr, shape):
        if arr.shape == shape:
            return arr
        try:
            if len(arr.shape) == 1 and len(shape) == 2 and arr.shape[0] == shape[1]:
                # print("This is the case 1 Arr.shape: ", arr.shape)
                return arr._stretch(0, shape[0])
            
            elif len(arr.shape) == 1 and len(shape) == 2 and arr.shape[0] == 1:
                # print("This is the case 2 Arr.shape: ", arr.shape)
                arr = arr._stretch(1, shape[1])
                return arr
            
            elif len(arr.shape) == 2 and len(shape) == 2 and arr.shape[0] == 1 and arr.shape[1] == 1 :
                # print("This is the case 3 Arr.shape: ", arr.shape)
                arr = arr._stretch(1, shape[1])
                arr = arr[0]._stretch(0, shape[0])
                return arr
            
            elif len(arr.shape) == 2 and len(shape) == 2 and arr.shape[1] == 1 and arr.shape[0] != 1:
                # print("This is the case 4 Arr.shape: ", arr.shape)
                arr = arr._stretch(0, shape[0])
                return arr
            
            elif len(arr.shape) == 2 and len(shape) == 2 and arr.shape[0] == 1 and arr.shape[1] != 1:
                # print("This is the case 5 Arr.shape: ", arr.shape)
                arr = arr._stretch(0, shape[0])
                return arr
             
            elif len(arr.shape) == 0 and len(shape) == 2:
                # print("This is the case 6 Arr.shape: ", arr.shape)
                return Array([arr] * shape[0], dtype=arr.dtype)._stretch(1, shape[1])
            else:
                raise ValueError(f"Cannot broadcast shape {arr.shape} to {shape}")

        except Exception as e:
            print(f"ERROR :{e}")

    
    def elementwise_op(self, other=None, op=None):
        if isinstance(other, (int, float)):
            other = Array([[other]])
        elif isinstance(other, (list)):
            other = Array(other)
        elif not isinstance(other, Array):
            raise TypeError("Operand must be an Array or a number or a list")

        arr1, arr2 = Array._broadcast(self, other)
        # print("-------------------------------------------")
        # print(arr1)
        # print(arr2)
            
        if len(arr1.shape) == 1:
            result_data = [op(arr1.data[i], arr2.data[i]) for i in range(arr1.shape[0])]
            return Array(result_data)
    
        elif len(arr1.shape) == 2:
            result_data = [[op(arr1.data[i][j], arr2.data[i][j]) for j in range(arr1.shape[1])] for i in range(arr1.shape[0])]
            return Array(result_data)
    
        elif len(arr1.shape) > 2:
            print(arr1.shape, arr2.shape)
            return self._elementwise_op(arr1[0], arr2[0], op)
    
    def _unary_elementwise_op(self, op):
        if len(self.shape) == 1:
            result_data = [op(self.data[i]) for i in range(self.shape[0])]
            return Array(result_data)
        elif len(self.shape) == 2:
            result_data = [[op(self.data[i][j]) for j in range(self.shape[1])] for i in range(self.shape[0])]
            return Array(result_data)
        elif len(self.shape) > 2:
            return self._unary_elementwise_op(self[0], op)
        
    
    
    @staticmethod
    def _elementwise_op(self, other, op):
        if isinstance(other, (int, float)):
            other = Array([[other]])
        elif isinstance(other, (list)):
            other = Array(other)
        elif not isinstance(other, Array):
            raise TypeError("Operand must be an Array or a number or a list")

        arr1, arr2 = Array._broadcast(self, other)

        if len(arr1.shape) == 1:
            result_data = [op(arr1.data[i], arr2.data[i]) for i in range(arr1.shape[0])]
            return Array(result_data)
        elif len(arr1.shape) == 2:
            result_data = [[op(arr1.data[i][j], arr2.data[i][j]) for j in range(arr1.shape[1])] for i in range(arr1.shape[0])]
            return Array(result_data)
        elif len(arr1.shape) > 2:
            return self._elementwise_op(arr1[0], arr2[0], op)
        


    def _stretch(self, axis, n_copies):
        temp = self.copy().data
        
        if axis == 0:
            temp = [[row for row in temp] for _ in range(n_copies)]
        elif axis == 1:
            if len(self.shape) == 1:
                temp = [[elem] for elem in temp]
            temp = [[col for col in row for _ in range(n_copies)] for row in temp]
        else:
            raise ValueError(f"Invalid axis: {axis}")
        return Array(temp)


    def _concat(self, row1, row2, axis):
        if axis == 0:
            return row1 + row2
        else:
            new_row = []
            for i in range(max(len(row1), len(row2))):
                elem1 = row1[i] if i < len(row1) else []
                elem2 = row2[i] if i < len(row2) else []
                new_row.append(self._concat(elem1, elem2, axis - 1))
            return new_row

    @property
    def T(self):
        return self.transpose()

    def transpose(self):
        def _trans_(arr):
            if arr.ndim == 1: 
                return arr._transpose_()
            elif arr.ndim == 2:  # If 2D array, perform transpose
                transposed_data = list(map(list, zip(*arr.data)))
                return Array(transposed_data)
            elif arr.ndim > 2:
                return _trans_(arr[0])
            else:
                raise ValueError("Invalid number of dimensions dimensions")
        return _trans_(self)



    def _transpose_(self):
        new_data = [[elem] for elem in self.data]  # Reshape the data
        return Array(new_data)

    
    def copy(self):
            temp = self.data.copy()
            return Array(temp)

    
    @staticmethod
    def zeros(shape):
        def _zeros(shape):
            if len(shape) == 1:
                return [[0] * shape[0]]
            else:
                return [_zeros((shape[1],)) for _ in range(shape[0])]
        return Array(_zeros(shape))

    @staticmethod
    def ones(shape):
        def _ones(shape):
            if isinstance(shape, int):
                return [[1] * shape]
            elif len(shape) == 1:
                return [[1] * shape[0]]
            else:
                return [_ones((shape[1],)) for _ in range(shape[0])]
        return Array(_ones(shape))
    
    
    @staticmethod
    def eye(shape):
        if len(shape) == 1:
            raise ValueError(f"Not a square matrix shape: {shape}")

        def _eye(shape):
            if len(shape) == 2:
                n = shape[0]
                m = shape[1]
                return [[1 if i == j else 0 for j in range(m)] for i in range(n)]
            else:
                return [_eye((1, shape[1])) for _ in range(shape[0])]
        return Array(_eye(shape))

    
    
    @staticmethod
    def linspace(start, end, endpoint=True, shape=None):
        # Determine the number of elements in the array
        if shape is None:
            raise ValueError("Shape must be specified for linspace method")
        num_elements = shape[0] * shape[1]

        # Calculate the step size based on the number of elements
        if endpoint:
            step = (end - start) / (num_elements - 1)
        else:
            step = (end - start) / num_elements

        # Generate array data
        def _linspace(start, end, step, shape):
            if len(shape) == 1:
                return [[start + i * step for i in range(shape[0])]]
            else:
                return [_linspace(start, end, step, (shape[1],)) for _ in range(shape[0])]
        return Array(_linspace(start, end, step, shape))


    @staticmethod
    def arange(start, stop, step, shape=None):
        # Determine the number of elements in the array
        if shape is None:
            raise ValueError("Shape must be specified for arange method")
        num_elements = shape[0] * shape[1]

        # Generate array data
        def _arange(start, stop, step, shape):
            if len(shape) == 1:
                return [[start + i * step for i in range(shape[0])]]
            else:
                return [_arange(start, stop, step, (shape[1],)) for _ in range(shape[0])]
        return Array(_arange(start, stop, step, shape))

    def round_values(self, decimals=2):
        def _round_values(arr, decimals):
            if len(arr.shape) == 1:
                return Array([round(val, decimals) for val in arr.data])
            else:
                return Array([_round_values(subarr, decimals).data for subarr in arr])
        return _round_values(self, decimals)

    @staticmethod
    def array_equal(arr1, arr2):
        def _array_equal(arr1, arr2):
            if len(arr1.shape) == 1:
                return all(a == b for a, b in zip(arr1.data, arr2.data))
            else:
                return all(_array_equal(subarr1, subarr2) for subarr1, subarr2 in zip(arr1.data, arr2.data))
        return _array_equal(arr1, arr2)


    def argmax(self, axis=None):
        if len(self.shape) == 1:
            return self.data.index([sorted(self.data)[self.shape[0]]])
    
        def _argmax(arr, axis):
            if axis is None:
                flattened_data = [val for row in arr.data for val in row]
                max_val = max(flattened_data)
                return flattened_data.index(max_val)
            elif axis == 0:
                max_indices = Array([max(enumerate(col), key=lambda x: x[1])[0] for col in zip(*arr.data)])
                return max_indices
            elif axis == 1:
                max_indices = Array([row.index(max(row)) for row in arr.data])
                return max_indices
            else:
                raise ValueError("Invalid axis value. Axis must be None, 0, or 1.")
        return _argmax(self, axis)


    def argmin(self, axis=None):
        if len(self.shape) == 1:
            return self.data.index([sorted(self.data)[0]])
        def _argmin(arr, axis):
            if axis is None:
                flattened_data = [val for row in arr.data for val in row]
                min_val = min(flattened_data)
                return flattened_data.index(min_val)
            elif axis == 0:
                min_indices = Array([min(enumerate(col), key=lambda x: x[1])[0] for col in zip(*arr.data)])
                return min_indices
            elif axis == 1:
                min_indices = Array([row.index(min(row)) for row in arr.data])
                return min_indices
            else:
                raise ValueError("Invalid axis value. Axis must be None, 0, or 1.")
        return _argmin(self, axis)


    def sum(self, axis=None):
        if isinstance(self.data, (int, float)):
            return self
        
        if len(self.shape) == 1:
            return sum(self.data)
        
        def _sum(arr, axis):
            if axis is None:
                return sum(sum(row) for row in arr.data)
            elif axis == 0:
                return Array([sum(col) for col in zip(*arr.data)])
            elif axis == 1:
                return Array([sum(row) for row in arr.data])
        return _sum(self, axis)



    def matmul(self, other): #for matrix vector everything is not ok so use dot
        def _matmul(arr1, arr2):
            if arr1.ndim > arr2.ndim:
                arr2 = arr2._stretch(1, arr1.ndim - arr2.ndim)
            elif arr2.ndim > arr1.ndim:
                arr1 = arr1._stretch(0, arr2.ndim - arr1.ndim)

            if arr1.ndim == 1:
                return (arr1 * arr2).sum() 
            if arr1.shape[1] != arr2.shape[0]:
                raise ValueError("Shapes {} and {} are not aligned".format(arr1.shape, arr2.shape))

            result_data = []
            for row in arr1.data:
                new_row = []
                for col in zip(*arr2.data):
                    element = sum(a * b for a, b in zip(row, col))
                    new_row.append(element)
                result_data.append(new_row)

            return Array(result_data)
        return _matmul(self, other)


    
    def dot(self, other):
        def _dot(arr1, arr2):
            if arr1.ndim > arr2.ndim:
                arr2 = arr2._stretch(1, arr1.ndim - arr2.ndim)
            elif arr2.ndim > arr1.ndim:
                arr1 = arr1._stretch(0, arr2.ndim - arr1.ndim)

            if arr1.ndim == 1:
                return (arr1 * arr2).sum() 
            elif arr1.ndim == 2:
                result = [[sum(a * b for a, b in zip(row, col)) for col in zip(*arr2.data)] for row in arr1.data]
                return Array(result)   
            elif arr1.ndim > 2:
                return _dot(arr1[0], arr2[0])             
            else:
                raise ValueError("Invalid shapes for dot multiplication: '{}' and '{}'".format(arr1.shape, arr2.shape))
        return _dot(self, other)


    def add(self, other):
        return self.elementwise_op(other, lambda x, y: x + y)

    def subtract(self, other):
        return self.elementwise_op(other, lambda x, y: x - y)

    def multiply(self, other):
        return self.elementwise_op(other, lambda x, y: x * y)

    def divide(self, other):
        return self.elementwise_op(other, lambda x, y: x / y)

    def power(self, other):
        return self.elementwise_op(other, lambda x, y: x ** y)

    def mod(self, other):
        return self.elementwise_op(other, lambda x, y: x % y)
    
    def exp(self):
        return self.elementwise_op(1, lambda x: math.exp(x))

    
    @classmethod
    def exp(cls, arr):
        return arr.exp()

    @staticmethod
    def log10(arr):
        return arr.elementwise_op(1, lambda x: math.log10(x))

    def acos(self):
        return self.elementwise_op(1, lambda x: math.acos(x))

    @classmethod
    def acos(cls, arr):
        return arr.acos()

    def atan(self):
        return self.elementwise_op(1, lambda x: math.atan(x))

    @classmethod
    def atan(cls, arr):
        return arr.atan()

    def asin(self):
        return self.elementwise_op(1, lambda x: math.asin(x))

    @classmethod
    def asin(cls, arr):
        return arr.asin()

    def ceil(self):
        return self.elementwise_op(1, lambda x: math.ceil(x))

    @classmethod
    def ceil(cls, arr):
        return arr.ceil()

    def floor(self):
        return self.elementwise_op(1, lambda x: math.floor(x))

    @classmethod
    def floor(cls, arr):
        return arr.floor()

    def log2(self):
        return self.elementwise_op(1, lambda x, y: math.log2(x))

    @classmethod
    def log2(cls, arr):
        return arr.log2()

    def erf(self):
        return self.elementwise_op(1, lambda x, y: math.erf(x))

    @classmethod
    def erf(cls, arr):
        return arr.erf()


    @classmethod
    def pow(cls, arr, power):
        return arr.pow(power=power)

    def pow(self, power):
        return self.__pow__(power)


    @classmethod
    def sqrt(cls, arr):
        return arr.sqrt()

    def sqrt(self):
            return self.__sqrt__()


    def log(self):
        return self.elementwise_op(1, lambda x, y: math.log(x))

    @classmethod
    def log(cls, arr):
        return arr.log()

    def sin(self):
        return self.elementwise_op(1, lambda x, y: math.sin(x))

    @classmethod
    def sin(cls, arr):
        return arr.sin()

    def cos(self):
        return self.elementwise_op(1, lambda x, y: math.cos(x))

    @classmethod
    def cos(cls, arr):
        return arr.cos()
    
    def abs(self):
        return self.__abs__()


    def repeat(self, repeats, axis=None):
            if axis is None:
                return Array([val for val in self._flatten() for _ in range(repeats)])
            else:
                data = self.data
                for _ in range(repeats):
                    data = self._concat(data, data, axis=axis)
                return Array(data)


    def min(self, axis=None):
        if axis is None:
            return min(self._flatten())
        else:
            new_data = []
            for i in range(self.shape[axis]):
                new_data.append(min(self._get_axis(i, axis)))
            return Array(new_data)

    def _get_axis(self, i, axis):
        if axis == 0:
            return self.data[i]
        else:
            return [self._get_axis(i, axis - 1) for row in self.data]

    def max(self, axis=None):
        if axis is None:
            return max(self._flatten())
        else:
            new_data = []
            for i in range(self.shape[axis]):
                new_data.append(max(self._get_axis(i, axis)))
            return Array(new_data)

  

    # def isclose(self, other):
    #     return Array([math.isclose(x, y) for x, y in zip(self._flatten(), other._flatten())])



    def isclose(self, other):
        data = self.data
        other_data = other.data
        result = []
        for i in range(len(data)):
            result.append(self._isclose(data[i], other_data[i]))
        return Array(result)

    def _isclose(self, arr1, arr2):
        result = []
        for i in range(len(arr1)):
            result.append(math.isclose(arr1[i], arr2[i]))
        return result

    def flatten(self, axis=None):
        if axis is None:
            return Array([self._flatten()])
        else:
            new_data = []
            for i in range(self.shape[axis]):
                new_data.extend(self._get_axis(i, axis))
            return Array(new_data)



    def concat(self, other, axis=0):
        return self.__concat__(other, axis)


    def vstack(self, other):
        return self.concat(other, axis=0)

    def hstack(self, other):
        return self.concat(other, axis=1)


    def reshape(self, shape):
        if math.prod(shape) != math.prod(self.shape):
            raise ValueError("Cannot reshape array of size {} into shape {}".format(math.prod(self.shape), shape))
        flat_data = self._flatten()
        new_data = self._reshape(flat_data, shape)
        return Array(new_data)

    def _flatten(self):
        flat_data = []
        self._flatten_helper(self.data, flat_data)
        return flat_data

    def _flatten_helper(self, data, flat_data):
        for element in data:
            if isinstance(element, list):
                self._flatten_helper(element, flat_data)
            else:
                flat_data.append(element)

    def _reshape(self, flat_data, shape):
        new_data = []
        self._reshape_helper(flat_data, shape, new_data)
        return new_data

    def _reshape_helper(self, flat_data, shape, new_data, index=0):
        if len(shape) == 1:
            new_data.append(flat_data[index:index + shape[0]])
        else:
            for _ in range(shape[0]):
                self._reshape_helper(flat_data, shape[1:], new_data, index)
                index += math.prod(shape[1:])
                

    def repeat(self, repeats, axis=None):
        if axis is None:
            return Array([val for val in self._flatten() for _ in range(repeats)])
        else:
            new_data = self.data
            for _ in range(repeats):
                new_data = self._insert_axis(new_data, axis)
            return Array(new_data)

    def _insert_axis(self, data, axis):
        if axis == 0:
            return [data]
        else:
            return [self._insert_axis(row, axis - 1) for row in data]

    def expand_dims(self, axis=None):
        if axis is None:
            return Array([self.data])
        else:
            data = self.data
            if axis == 0:
                data = [[elem] for elem in data]
            else:
                data = self._expand_dims(data, axis=axis-1)
            return Array(data)

    def _expand_dims(self, data, axis=0):
        result = []
        for elem in data:
            result.append(self._expand_dims(elem, axis=axis-1))
        return [[result]]

    def ravel(self):
        return self.flatten()
    
    
    def sort(self):
        data = self.data
        data.sort()
        return Array(data)


    def clip(self, a_min, a_max):
        return Array([min(max(val, a_min), a_max) for val in self._flatten()])

    def resize(self, new_shape):
        if math.prod(new_shape) != math.prod(self.shape):
            raise ValueError("Cannot resize array to new shape: sizes do not match")
        flat_data = self._flatten()
        new_data = self._reshape(flat_data, new_shape)
        return Array(new_data)

    def squeeze(self):
        new_shape = list(self.shape)
        for i in range(len(new_shape)):
            if new_shape[i] == 1:
                new_shape.pop(i)
                break
        return Array(self._reshape(self._flatten(), tuple(new_shape)))


    def partition(self, kth, axis=-1):
        if axis == -1:
            sorted_data = sorted(self._flatten())
            return Array(sorted_data[:kth]), Array(sorted_data[kth:])
        else:
            raise NotImplementedError("Partition along axis other than -1 is not implemented yet")

    def argpartition(self, kth, axis=-1):
        if axis == -1:
            sorted_indices = sorted(range(len(self.data)), key=lambda i: self.data[i])
            return Array(sorted_indices[:kth]), Array(sorted_indices[kth:])
        else:
            raise NotImplementedError("Argpartition along axis other than -1 is not implemented yet")

    def swapaxes(self, axis1, axis2):
        new_data = self.data
        new_data = self._swap_axes(new_data, axis1, axis2)
        return Array(new_data)

    def _swap_axes(self, data, axis1, axis2):
        if axis1 == 0 and axis2 == 1:
            return [list(row) for row in zip(*data)]
        elif axis1 == 1 and axis2 == 0:
            return [list(row) for row in zip(*data)]
        else:
            raise NotImplementedError("Swapaxes for axes other than 0 and 1 is not implemented yet")

    def put(self, indices, values):
        new_data = self.data
        self._put(new_data, indices, values)
        return Array(new_data)

    def _put(self, data, indices, values):
        for index, value in zip(indices, values):
            self._put_helper(data, index, value)

    def _put_helper(self, data, index, value):
        if isinstance(index, int):
            data[index] = value
        else:
            self._put_helper(data[index[0]], index[1:], value)

    def choose(self, choices):
        return Array([choices[val] for val in self._flatten()])

    def take(self, indices, axis=None):
        if axis is None:
            return Array([self._flatten()[index] for index in indices])
        else:
            new_data = []
            for index in indices:
                new_data.append(self._get_axis(index, axis))
            return Array(new_data)
        
    @staticmethod
    def array_equal(arr, other):
        if not isinstance(other, Array):
            raise TypeError("Unsupported operand type(s) for array_equal: 'Array' and '{}'".format(type(other)))
        if arr.shape != other.shape:
            return False
        for i in range(arr.shape[0]):
            for j in range(arr.shape[1]):
                if arr.ndim > 2:
                    if not Array.array_equal(Array([arr.data[i][j]]), Array([other.data[i][j]])):
                        return False
                else:
                    if arr.data[i][j] != other.data[i][j]:
                        return False
        return True
        
    #.............................................................................................

    

    # Random Module
    @staticmethod
    def _random_value():
        return random.random()

    @staticmethod
    def random(shape):
        if not isinstance(shape, tuple) or not all(isinstance(dim, int) for dim in shape):
            raise ValueError("Shape must be a tuple of integers")
        data = []
        for _ in range(shape[0]):
            row = []
            for _ in range(shape[1]):
                if len(shape) > 2:
                    row.append(Array.random(shape[2:]).data)
                else:
                    row.append(Array._random_value())
            data.append(row)
        return Array(data)
    
    def randint(self, low, high, shape=None):
        if shape is None:
            data = []
            for _ in range(self.shape[0]):
                row = []
                for _ in range(self.shape[1]):
                    if len(self.shape) > 2:
                        row.append(self.randint(low, high, shape=self.shape[2:]).data)
                    else:
                        row.append(random.randint(low, high))
                data.append(row)
            return Array(data)
        elif isinstance(shape, tuple) and len(shape) > 1:
            data = []
            for _ in range(shape[0]):
                row = []
                for _ in range(shape[1]):
                    if len(shape) > 2:
                        row.append(self.randint(low, high, shape=shape[2:]).data)
                    else:
                        row.append(random.randint(low, high))
                data.append(row)
            return Array(data)
        else:
            raise ValueError("Shape must be a tuple of two or more integers")
    
    
    
    def randn(self, shape=None):
        if shape is None:
            data = []
            for _ in range(self.shape[0]):
                row = []
                for _ in range(self.shape[1]):
                    if len(self.shape) > 2:
                        row.append(self.randn(shape=self.shape[2:]).data)
                    else:
                        row.append(random.gauss(0, 1))
                data.append(row)
            return Array(data)
        elif isinstance(shape, tuple) and len(shape) > 1:
            data = []
            for _ in range(shape[0]):
                row = []
                for _ in range(shape[1]):
                    if len(shape) > 2:
                        row.append(self.randn(shape=shape[2:]).data)
                    else:
                        row.append(random.gauss(0, 1))
                data.append(row)
            return Array(data)
        else:
            raise ValueError("Shape must be a tuple of two or more integers")

    def shuffle(self, axis=0):
        if axis != 0:
            raise ValueError("Cannot shuffle array along axis other than 0.")
        
        if self.shape[0] != 1:
            raise ValueError("Cannot shuffle array: array must be one-dimensional along the specified axis.")
        
        shuffled_data = self.data[0][:]
        random.shuffle(shuffled_data)
        return Array([shuffled_data])
    

    def choice(self):
        if self.shape[0] != 1:
            raise ValueError("Cannot choose element from array: array must be one-dimensional")
        return random.choice(self.data[0])

    #.....................................................................................................

    @property
    def ndim(self):
        return len(self.shape)

    def size(self):
        return self._calculate_size()

    def around(self, decimals=0):
        return Array([[round(val, decimals) for val in row] for row in self.data])

    def round(self, decimals=0):
        return self.around(decimals)

    def ptp(self):
        return self.amax() - self.amin()

    def all(self):
        return all(val for row in self.data for val in row)

    def any(self):
        return any(val for row in self.data for val in row)

    def compress(self, condition):
        return Array([[val for val in row if condition(val)] for row in self.data])
    
    def amax(self, axis=None):
        if axis is None:
            max_val = float('-inf')
            for row in self.data:
                for val in row:
                    if isinstance(val, list):
                        max_val = max(max_val, Array.amax(Array([val])))
                    else:
                        max_val = max(max_val, val)
            return max_val
        else:
            max_val = float('-inf')
            for row in self.data:
                if isinstance(row, list):
                    max_val = max(max_val, Array.amax(Array([row])))
                else:
                    max_val = max(max_val, row[axis])
            return max_val

    def amin(self, axis=None):
        if axis is None:
            min_val = float('inf')
            for row in self.data:
                for val in row:
                    if isinstance(val, list):
                        min_val = min(min_val, Array.amin(Array([val])))
                    else:
                        min_val = min(min_val, val)
            return min_val
        else:
            min_val = float('inf')
            for row in self.data:
                if isinstance(row, list):
                    min_val = min(min_val, Array.amin(Array([row])))
                else:
                    min_val = min(min_val, row[axis])
            return min_val

    def mean(self, axis=None):
        if axis is None:
            return sum(self.data) / self.size
        elif axis == 0:
            means = [sum(self[:, i]) / self.shape[0] for i in range(self.shape[1])]
            return Array(means)
        elif axis == 1:
            means = [sum(row) / self.shape[1] for row in self.data]
            return Array(means)
        elif axis == 2:
            means = [[[sum(self[i, j, k]) / self.shape[2] for k in range(self.shape[2])] for j in range(self.shape[1])] for i in range(self.shape[0])]
            return Array(means)
        else:
            raise ValueError("Axis out of bounds")

    def var(self, axis=None):
        if axis is None:
            mean_val = self.mean()
            total_sum = 0
            num_elements = self.size
            for idx in self.indexes():
                total_sum += (self[idx] - mean_val) ** 2
            return total_sum / num_elements
        else:
            mean_val = self.mean(axis)
            variances = []
            for idx in self.indexes(exclude_axis=axis):
                total_sum = 0
                num_elements = self.shape[axis]
                for i in range(self.shape[axis]):
                    total_sum += (self[idx + (slice(None),) * axis + (i,)] - mean_val[idx + (slice(None),) * axis + (i,)]) ** 2
                variances.append(total_sum / num_elements)
            return Array(variances)

    def std(self, axis=None):
        return math.sqrt(self.var(axis=axis))

    #...............................................................
    

    def cumsum(self, axis=None):
        if axis is None:
            result = Array(self.data)
            self._cumsum_recursive(result.data, 0)
            return result
        else:
            result = Array(self.data)
            self._cumsum_axis(result.data, axis)
            return result

    def _cumsum_recursive(self, data, index):
        if isinstance(data, list):
            for i in range(1, len(data)):
                self._cumsum_recursive(data[i], index + 1)
                data[i] = [x + y for x, y in zip(data[i - 1], data[i])]
        else:
            for i in range(1, len(data)):
                data[i] += data[i - 1]

    def _cumsum_axis(self, data, axis):
        if axis == 0:
            for i in range(1, len(data)):
                data[i] = [x + y for x, y in zip(data[i - 1], data[i])]
        else:
            for i in range(len(data)):
                self._cumsum_recursive(data[i], axis - 1)

    def cumprod(self, axis=None):
        if axis is None:
            result = Array(self.data)
            self._cumprod_recursive(result.data, 0)
            return result
        else:
            result = Array(self.data)
            self._cumprod_axis(result.data, axis)
            return result

    def _cumprod_recursive(self, data, index):
        if isinstance(data, list):
            for i in range(1, len(data)):
                self._cumprod_recursive(data[i], index + 1)
                data[i] = [x * y for x, y in zip(data[i - 1], data[i])]
        else:
            for i in range(1, len(data)):
                data[i] *= data[i - 1]

    def _cumprod_axis(self, data, axis):
        if axis == 0:
            for i in range(1, len(data)):
                data[i] = [x * y for x, y in zip(data[i - 1], data[i])]
        else:
            for i in range(len(data)):
                self._cumprod_recursive(data[i], axis - 1)

    def norm(self, axis=None, distance='euclidean'):
        if distance == 'euclidean':
            return self.euclidean_norm(axis)
        elif distance == 'manhattan':
            return self.manhattan_norm(axis)
        else:
            raise ValueError("Invalid distance type. Please choose 'euclidean' or 'manhattan'.")

    def euclidean_norm(self, axis):
        if axis is None:
            return math.sqrt(sum(val ** 2 for val in self.flatten()))
        elif isinstance(axis, int):
            return self.pow(2).sum(axis).sqrt()
        else:
            raise ValueError("Axis must be an integer or None")

    def manhattan_norm(self, axis):
        if axis is None:
            return sum(abs(val) for val in self.flatten())
        elif isinstance(axis, int):
            return sum(abs(val) for val in self.data)
        else:
            raise ValueError("Axis must be an integer or None")
    
    @property
    def i(self):
        return inv(self)
    
    @property
    def det(self):
        return det(self)


def inv(self):
    if not self.is_square_matrix(self):
        raise ValueError("Input self must be square")

    n = self.shape[0]
    id = self.eye((n,n))
    augmented_self = self.concat(id, axis=1)

    # Forward elimination
    for i in range(n):
        # Find pivot row
        pivot_row = max(range(i, n), key=lambda j: abs(augmented_self[j][i]))
        if augmented_self[pivot_row][i] == 0:
            raise ValueError("self is singular")
        # Swap rows
        augmented_self[i], augmented_self[pivot_row] = augmented_self[pivot_row], augmented_self[i]
        # Scale pivot row
        pivot_val = augmented_self[i][i]
        augmented_self[i] = [val / pivot_val for val in augmented_self[i]]
        # Eliminate other rows
        for j in range(i + 1, n):
            multiplier = augmented_self[j][i]
            augmented_self[j] = [augmented_self[j][k] - multiplier * val for k, val in enumerate(augmented_self[i])]

    # Backward elimination
    for i in range(n - 1, -1, -1):
        for j in range(i - 1, -1, -1):
            multiplier = augmented_self[j][i]
            augmented_self[j] = [augmented_self[j][k] - multiplier * val for k, val in enumerate(augmented_self[i])]

    return Array([row[n:].data for row in augmented_self])

def allclose(self, arr2, rtol=1e-05, atol=1e-08):
    if len(self) != len(arr2):
        return False

    for x, y in zip(self, arr2):
        if abs(x - y) > atol + rtol * max(abs(x), abs(y)):
            return False

    return True




def det(self):
    if not Array.is_square_matrix(self):
        raise ValueError("Cannot compute determinant: array is not square")

    determinant = 1.0
    arr_copy = self.copy()
    n = arr_copy.shape[0]

    for j in range(n):
        max_row = j
        max_val = abs(arr_copy[j, j])

        # Find the maximum absolute value element in column j from rows j to n
        for i in range(j + 1, n):
            abs_val = abs(arr_copy[i, j])
            if abs_val > max_val:
                max_val = abs_val
                max_row = i

        # Swap the row with maxVal with the current row
        if max_row != j:
            arr_copy[j], arr_copy[max_row] = arr_copy[max_row].copy(), arr_copy[j].copy()
            # Multiply the determinant by -1 due to row swap
            determinant *= -1

        # Divide the current row by the value of A[j][j] to make the leading coefficient 1
        pivot = arr_copy[j, j]
        arr_copy[j] = arr_copy[j] / pivot
        determinant *= pivot

        # Eliminate the jth column element in other rows
        for i in range(j + 1, n):
            factor = arr_copy[i, j]
            arr_copy[i] = arr_copy[i] - factor * arr_copy[j]

    # Multiply the determinant by the diagonal elements of the row-echelon form
    for i in range(n):
        determinant *= arr_copy[i, i]

    # Convert the list of lists of floats to an Array object
    arr_copy = Array(arr_copy)
    return determinant



def qr_decomposition(self, max_iterations = 1000, tolerance = 1e-9):
    n = self.shape[0]  # Assuming square matrix
    q = Array.eye((n, n))  # Initialize Q as the identity matrix
    r = Array(self.data)  # Initialize R as a copy of the input matrix


    for _ in range(max_iterations):
        # Iterate over columns of R
        for j in range(n):
            # Extract the j-th column of R
            v = [r.data[i][j] for i in range(j, n)]
            # Compute the norm of v and adjust the sign if necessary
            norm_v = sum([math.pow(x, 2) for x in v])
            norm_v = math.sqrt(norm_v)

            if v[0] < 0:
                norm_v = -norm_v

            # Check for convergence
            if norm_v < tolerance:
                return q, r

            # Create the Householder reflector
            v[0] += norm_v
            scale = sum([math.pow(x, 2) for x in v])
            scale = math.sqrt(scale)

            reflector = [x / scale for x in v]
            reflector = Array(reflector)

            # Update R and Q
            for i in range(j, n):
                dot_product = (r.dot(reflector.T)).sum()
                r.data[i][j] = dot_product
                for k in range(n):
                    q.data[i][k] -= 2 * reflector[k] * dot_product

    return q, r

def gram_schmidt(self):
    if self.shape[0] != self.shape[1]:
        raise ValueError("Cannot perform Gram-Schmidt process: array is not square")

    n = self.shape[0]
    u = Array(self.data)  # Copy of original vectors
    e = Array([[0] * n for _ in range(n)])  # Matrix of orthogonal vectors

    for j in range(n):
        # Calculate orthogonal vector
        for i in range(j):
            projection = (u[:, i] * e[:, i]).sum()
            u[:, j] -= projection * e[:, i]

        # Normalize orthogonal vector
        norm = (u[:, j] ** 2).sum() ** 0.5
        if norm == 0:
            raise ValueError("Cannot perform Gram-Schmidt process: vectors are linearly dependent")
        e[:, j] = u[:, j] / norm

    return e


 
def eig(self):
    if not Array.is_square_matrix(self):
        raise ValueError("Cannot compute eigenvalues: array is not square")

    n = self.shape[0]
    eigenvalues = []
    eigenvectors = []
    max_iterations = 10000
    tolerance = 1e-9

    # Create a copy of the original matrix
    A = self.copy()

    # Iterate to find eigenvalues and eigenvectors
    for _ in range(n):
        # Initialize a random unit vector
        v = Array.random((n, 1))
        v = v / v.norm()  # Normalize the initial vector

        # Iterate until convergence
        for i in range(max_iterations):
            v_new = A.dot(v)
            v_new = v_new / v_new.norm()  # Normalize the new vector

            # Check for convergence
            if (v_new - v).norm() < tolerance:
                break

            v = v_new

        # Compute the eigenvalue
        eigenvalue = v.transpose().dot(A).dot(v).data[0][0]
        eigenvalues.append(eigenvalue)
        eigenvectors.append(v)

        # Update the matrix by subtracting the contribution of this eigenvalue
        A = A - eigenvalue * v.dot(v.transpose())

    return eigenvalues, eigenvectors


def eigenvalues(self):
    eigv, _ =self.eig()
    return eigv

def eigvectors(self):
    _, eigv =self.eig()
    return eigv


def svd(self):
    m, n = self.shape
    
    # Calcul de A * A^T et A^T * A
    ata = self.dot(self.transpose())
    aat = self.transpose().dot(self)
    
    # Calcul des valeurs propres et des vecteurs propres
    eig_vals_ata, eig_vecs_ata = ata.eig()
    eig_vals_aat, eig_vecs_aat = aat.eig()
    
    # Tri des valeurs propres et des vecteurs propres par ordre décroissant
    sorted_indices_ata = sorted(range(len(eig_vals_ata)), key=lambda i: eig_vals_ata[i], reverse=True)
    sorted_indices_aat = sorted(range(len(eig_vals_aat)), key=lambda i: eig_vals_aat[i], reverse=True)
    
    # Calcul des valeurs singulières et des vecteurs singuliers
    singular_values = [math.sqrt(eig_vals_ata[i]) for i in sorted_indices_ata if eig_vals_ata[i] > 0]
    singular_vectors = [eig_vecs_aat[i] for i in sorted_indices_aat if eig_vals_aat[i] > 0]
    
    # Remplissage des vecteurs singuliers manquants pour obtenir la taille correcte
    num_singular_vectors = min(m, n)
    if len(singular_vectors) < num_singular_vectors:
        singular_vectors.extend([Array([[0] * m] * n) for _ in range(num_singular_vectors - len(singular_vectors))])
    
    return singular_values, singular_vectors



@staticmethod
def is_square_matrix(arr):
    return arr.shape[0] == arr.shape[1]


    

def _str_index_(string, char):
    for i, x in enumerate(string):
        if x == char:
            return i
    return None

        
def distance(x):
    if isinstance(x, Array):
        if isinstance(x[0], (int, float)):
            return max(x) - min(x)
    else:
        return x[x.argmax()] - x[x.argmin()]

def exp(x):
    if not isinstance(x, (int, float)):
        print(f"Cannot calculate exp of {type(x)}")
        return
    
    e = 2.718281828459045
    return pow(x, e)


def prod(x):
    if isinstance(x, (int, float)):
        return x
    elif isinstance(x, (tuple, list)):
        if len(x) == 0:
            return 1
        
        r = 1
        for j in x:
            r *= j
        return j
    

def _fft(self, x):
        N = len(x)
        if N <= 1:
            return x
        even = _fft(x[::2])
        odd = _fft(x[1::2])
        min_length = min(len(odd), N // 2)  # Ensure range does not exceed length of odd
        T = [math.e ** (-2j * math.pi * k / N) * odd[k] for k in range(min_length)]
        return [even[k] + T[k] for k in range(min_length)] + [even[k] - T[k] for k in range(min_length)]


def fft(self):
        if self.shape[0] != 1:
            raise ValueError("Cannot perform FFT: array must be one-dimensional")
        return Array(_fft(self.data))

    
def isclose(a, b, rel_tol=1e-9, abs_tol=0.0):
    if rel_tol <= 0.0 or abs_tol <= 0.0:
        raise ValueError("tolerances must be positive")

    diff = abs(a - b)
    if diff <= abs_tol:
        return True

    # Calculate the relative difference
    rel_diff = diff / (abs(a) + abs(b)) #fabs was here but used abs

    # Check if the relative difference is within the tolerance
    return rel_diff <= rel_tol

 
def sqrt(n, iter=100):
    x = n
    for _ in range(iter):
        x = 0.5 * ((x+n) / x)
    
    return x








@staticmethod
def rand(low, high, shape=None):
    if shape is None:
        raise ValueError("Shape must be specified.")
    data = []
    for _ in range(shape[0]):
        row = []
        for _ in range(shape[1]):
            if len(shape) > 2:
                row.append(rand(low, high, shape=shape[2:]).data)
            else:
                row.append(random.random() * (high - low) + low)
        data.append(row)
    return Array(data)

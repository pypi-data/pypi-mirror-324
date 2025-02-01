# coding: utf-8
# by Jules
# Time: 2025/1/31 12:49:36

__author__ = 'Jules'
__all__ = ['Link', 'Rect', 'Array']

from exceptions import *
from typing import *

class Link:
    """
    Link类用于创建一个链式数据结构，支持添加、插入、删除元素等操作，
    并通过图形化方式展示链表内容。
    可以使用print()函数，show()方法或print(get()方法)显示链表
    """
    def __init__(self, *args, target: list | tuple | set | None = None):
        if args:
            self.items = list(args)
        else:
            self.items = list(target) if target is not None else []
        self._update_data()

    def __str__(self) -> str:
        return self.data

    def __getitem__(self, index):
        """
        支持切片操作，并返回一个新的 link 对象。

        参数:
        index (slice): 切片对象。

        返回:
        新的 link 对象，包含切片后的元素。
        """
        if isinstance(index, slice):
            new_link = Link()
            new_link.items = self.items[index]
            new_link._update_data()
            return new_link
        else:
            return self.items[index]

    def append(self, item: Any) -> None:
        """
        向列表中追加元素，并更新数据表示。

        参数:
        item (any): 要追加到列表中的元素，可以是任意类型。

        返回:
        无返回值。
        """
        self.items.append(item)
        self._update_data()

    def insert(self, index: int, item: Any) -> None:
        """
        在指定索引处插入元素，并更新数据表示。

        参数:
        index (int): 要插入元素的位置索引。
        item (any): 要插入到列表中的元素，可以是任意类型。

        返回:
        无返回值。
        """
        self.items.insert(index, item)
        self._update_data()

    def remove(self, item: Any) -> None:
        """
        从列表中删除指定的元素，并更新数据表示。

        参数:
        item (any): 要从列表中删除的元素，可以是任意类型。

        返回:
        无返回值。
        """
        self.items.remove(item)
        self._update_data()

    def pop(self, index: int = -1) -> Any:
        """
        从列表中删除指定索引处的元素，并更新数据表示。

        参数:
        index (int): 要删除的元素的索引，默认为-1，表示删除最后一个元素。

        返回:
        被删除的元素。
        """
        removed_item = self.items.pop(index)
        self._update_data()
        return removed_item

    def reverse(self):
        """
        反转链表，并更新数据表示。

        参数:
        无参数。

        返回:
        无返回值。
        """
        self.items.reverse()
        self._update_data()

    def show(self):
        print(self.data)

    def get(self, index=None, cut=None, sci=None):
        # 输入验证
        if not all(isinstance(param, (int, type(None))) for param in [index, cut, sci]):
            raise TypeError("Parameters must be integers or None")

        try:
            if index is not None and cut is None and sci is None:
                return self[index]
            elif index is None and cut is not None and sci is not None:
                return self[:cut:sci]
            else:
                return self[index:cut:sci]
        except (IndexError, TypeError) as e:
            raise IndexError("Invalid slice parameters") from e

    def _update_data(self):
        self.data = '->'.join(map(str, self.items)) + '->'


class Rect:
    """
    Warning: Unsupported to **, %, //, only a little support to /.
    """
    def __init__(self, width: int | None = None, height: int | None = None, target: list[list[int | float]] | None = None):
        if target is not None:
            if not isinstance(target, list) or not all(isinstance(row, list) for row in target):
                raise ValueError("target must be a 2D list")
            if not target:
                raise ValueError("target must not be an empty list")
            row_lengths = [len(row) for row in target]
            if len(set(row_lengths)) != 1:
                raise ValueError("All rows in target must have the same length")
            self.width = len(target)
            self.height = len(target[0])
            self.matrix = target
        elif width is not None and height is not None:
            self.width = width
            self.height = height
            self.matrix = [[0 for _ in range(height)] for _ in range(width)]
        else:
            raise ValueError("Either target or both width and height must be provided")

    def __str__(self) -> str:
        return f"[{'\n '.join([' '.join(map(str, row)) for row in self.matrix])}]"

    def __getitem__(self, index):
        if isinstance(index, tuple):
            row, col = index
            if isinstance(row, slice) and isinstance(col, slice):
                new_matrix = [self.matrix[r][col] for r in range(self.width)[row]]
                return Rect(target=new_matrix)
            elif isinstance(row, slice):
                new_matrix = [self.matrix[r][col] for r in range(self.width)[row]]
                return Rect(target=new_matrix)
            elif isinstance(col, slice):
                new_matrix = [self.matrix[row][c] for c in range(self.height)[col]]
                return Rect(target=[new_matrix])
            else:
                return self.matrix[row][col]
        elif isinstance(index, slice):
            new_matrix = [self.matrix[r] for r in range(self.width)[index]]
            return Rect(target=new_matrix)
        else:
            raise TypeError("Unknown index type")

    def __add__(self, other: Self | int | float) -> 'Rect':
        if isinstance(other, Rect):
            if self.width != other.width or self.height != other.height:
                raise ValueError("Matrices must have the same dimensions for addition")
            result = Rect(width=self.width, height=self.height)
            for i in range(self.width):
                for j in range(self.height):
                    result.matrix[i][j] = self.matrix[i][j] + other.matrix[i][j]
        elif isinstance(other, (int, float)):
            result = Rect(width=self.width, height=self.height)
            for i in range(self.width):
                for j in range(self.height):
                    result.matrix[i][j] = self.matrix[i][j] + other
        else:
            raise TypeError("Unsupported operand type for +: 'Rect' and '{}'".format(type(other).__name__))
        return result

    def __radd__(self, other: int | float) -> 'Rect':
        return self.__add__(other)

    def __sub__(self, other: Self | int | float) -> 'Rect':
        if isinstance(other, Rect):
            if self.width != other.width or self.height != other.height:
                raise ValueError("Matrices must have the same dimensions for subtraction")
            result = Rect(width=self.width, height=self.height)
            for i in range(self.width):
                for j in range(self.height):
                    result.matrix[i][j] = self.matrix[i][j] - other.matrix[i][j]
        elif isinstance(other, (int, float)):
            result = Rect(width=self.width, height=self.height)
            for i in range(self.width):
                for j in range(self.height):
                    result.matrix[i][j] = self.matrix[i][j] - other
        else:
            raise TypeError("Unsupported operand type for -: 'Rect' and '{}'".format(type(other).__name__))
        return result

    def __rsub__(self, other: int | float) -> 'Rect':
        result = Rect(width=self.width, height=self.height)
        for i in range(self.width):
            for j in range(self.height):
                result.matrix[i][j] = other - self.matrix[i][j]
        return result

    def __mul__(self, other: Self | int | float) -> 'Rect':
        if isinstance(other, Rect):
            if self.height != other.width:
                raise ValueError(
                    "Number of columns in the first matrix must be equal to number of rows in the second matrix")
            result = Rect(width=self.width, height=other.height)
            for i in range(self.width):
                for j in range(other.height):
                    for k in range(self.height):
                        result.matrix[i][j] += self.matrix[i][k] * other.matrix[k][j]
        elif isinstance(other, (int, float)):
            result = Rect(width=self.width, height=self.height)
            for i in range(self.width):
                for j in range(self.height):
                    result.matrix[i][j] = self.matrix[i][j] * other
        else:
            raise TypeError("Unsupported operand type for *: 'Rect' and '{}'".format(type(other).__name__))
        return result

    def __rmul__(self, other: int | float) -> 'Rect':
        return self.__mul__(other)

    def __truediv__(self, other: Self | int | float) -> 'Rect':
        if isinstance(other, Rect):
            if self.height != other.width:
                raise ValueError(
                    "Number of columns in the first matrix must be equal to number of rows in the second matrix")
            if other.width != other.height:
                raise ValueError("The second matrix must be square for inversion")
            inv_other = self._inverse_matrix(other.matrix)
            result = self._matrix_multiply(self.matrix, inv_other)
        elif isinstance(other, (int, float)):
            if other == 0:
                raise ZeroDivisionError("division by zero")
            result = Rect(width=self.width, height=self.height)
            for i in range(self.width):
                for j in range(self.height):
                    result.matrix[i][j] = self.matrix[i][j] / other
        else:
            raise TypeError("Unsupported operand type for /: 'Rect' and '{}'".format(type(other).__name__))
        return Rect(target=result)

    def __rtruediv__(self, other: int | float) -> 'Rect':
        if other == 0:
            raise ZeroDivisionError("division by zero")
        result = Rect(width=self.width, height=self.height)
        for i in range(self.width):
            for j in range(self.height):
                result.matrix[i][j] = other / self.matrix[i][j]
        return result

    def __pow__(self, power: int) -> 'Rect':
        if not isinstance(power, int) or power < 0:
            raise ValueError("Power must be a non-negative integer")
        if self.width != self.height:
            raise RectNotSupport("Matrix must be square for exponentiation")
        if power == 0:
            # Return the identity matrix
            identity = Rect(self.width, self.height)
            for i in range(self.width):
                identity.set_value(i, i, 1)
            return identity
        elif power == 1:
            return self
        else:
            result = self
            for _ in range(1, power):
                result = result * self
            return result

    def _matrix_multiply(self, A: list[list[float]], B: list[list[float]]) -> list[list[float]]:
        result = [[0 for _ in range(len(B[0]))] for _ in range(len(A))]
        for i in range(len(A)):
            for j in range(len(B[0])):
                for k in range(len(B)):
                    result[i][j] += A[i][k] * B[k][j]
        return result

    def _inverse_matrix(self, matrix: list[list[float]]) -> list[list[float]]:
        n = len(matrix)
        if n != len(matrix[0]):
            raise ValueError("Matrix must be square for inversion")
        # Create an identity matrix of the same size
        identity = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        # Augment the matrix with the identity matrix
        augmented = [matrix[i] + identity[i] for i in range(n)]

        # Perform Gaussian elimination to transform the matrix into an upper triangular matrix
        for i in range(n):
            # Find the pivot row
            max_row = max(range(i, n), key=lambda r: abs(augmented[r][i]))
            augmented[i], augmented[max_row] = augmented[max_row], augmented[i]

            # Scale the pivot row
            pivot = augmented[i][i]
            if pivot == 0:
                raise ValueError("Matrix is not invertible")
            for j in range(2 * n):
                augmented[i][j] /= pivot

            # Eliminate other rows
            for r in range(n):
                if r != i:
                    factor = augmented[r][i]
                    for j in range(2 * n):
                        augmented[r][j] -= factor * augmented[i][j]

        # Extract the inverse matrix from the augmented matrix
        inverse = [row[n:] for row in augmented]
        return inverse

    def set_value(self, row: int, col: int, value: int) -> None:
        if row < 0 or row >= self.width or col < 0 or col >= self.height:
            raise IndexError("Index out of bounds")
        self.matrix[row][col] = value

    def get_value(self, row: int, col: int) -> int:
        if row < 0 or row >= self.width or col < 0 or col >= self.height:
            raise IndexError("Index out of bounds")
        return self.matrix[row][col]

    def show(self):
        print(self)


class Array:
    def __init__(self, data: list[int | float] | None = None):
        if data is not None:
            if not isinstance(data, list):
                raise ValueError("data must be a list")
            self.data = data
        else:
            self.data = []

    def __str__(self) -> str:
        return f"[{' '.join(str(x) for x in self.data)}]"

    def __getitem__(self, index: Union[int, slice]) -> Union[int, float, 'Array']:
        if isinstance(index, slice):
            return Array(self.data[index])
        elif isinstance(index, int):
            return self.data[index]
        else:
            raise TypeError("Unsupported index type")

    def __add__(self, other: Self | int | float) -> 'Array':
        if isinstance(other, Array):
            if len(self.data) != len(other.data):
                raise ValueError("Arrays must have the same length for addition")
            result = [a + b for a, b in zip(self.data, other.data)]
        elif isinstance(other, (int, float)):
            result = [a + other for a in self.data]
        else:
            raise TypeError("Unsupported operand type for +: 'Array' and '{}'".format(type(other).__name__))
        return Array(result)

    def __radd__(self, other: int | float) -> 'Array':
        return self.__add__(other)

    def __sub__(self, other: Self | int | float) -> 'Array':
        if isinstance(other, Array):
            if len(self.data) != len(other.data):
                raise ValueError("Arrays must have the same length for subtraction")
            result = [a - b for a, b in zip(self.data, other.data)]
        elif isinstance(other, (int, float)):
            result = [a - other for a in self.data]
        else:
            raise TypeError("Unsupported operand type for -: 'Array' and '{}'".format(type(other).__name__))
        return Array(result)

    def __rsub__(self, other: int | float) -> 'Array':
        result = [other - a for a in self.data]
        return Array(result)

    def __mul__(self, other: Self | int | float) -> 'Array':
        if isinstance(other, Array):
            if len(self.data) != len(other.data):
                raise ValueError("Arrays must have the same length for multiplication")
            result = [a * b for a, b in zip(self.data, other.data)]
        elif isinstance(other, (int, float)):
            result = [a * other for a in self.data]
        else:
            raise TypeError("Unsupported operand type for *: 'Array' and '{}'".format(type(other).__name__))
        return Array(result)

    def __rmul__(self, other: int | float) -> 'Array':
        return self.__mul__(other)

    def __truediv__(self, other: Self | int | float) -> 'Array':
        if isinstance(other, Array):
            if len(self.data) != len(other.data):
                raise ValueError("Arrays must have the same length for division")
            result = [a / b for a, b in zip(self.data, other.data)]
        elif isinstance(other, (int, float)):
            if other == 0:
                raise ZeroDivisionError("division by zero")
            result = [a / other for a in self.data]
        else:
            raise TypeError("Unsupported operand type for /: 'Array' and '{}'".format(type(other).__name__))
        return Array(result)

    def __rtruediv__(self, other: int | float) -> 'Array':
        if other == 0:
            raise ZeroDivisionError("division by zero")
        result = [other / a for a in self.data]
        return Array(result)

    def sum(self) -> float:
        return sum(self.data)

    def mean(self) -> float:
        if not self.data:
            raise ValueError("Cannot compute mean of an empty array")
        return self.sum() / len(self.data)

    def sort(self) -> 'Array':
        sorted_data = sorted(self.data)
        return Array(sorted_data)

    def append(self, value: int | float) -> None:
        self.data.append(value)

    def get_value(self, index: int) -> int | float:
        if index < 0 or index >= len(self.data):
            raise IndexError("Index out of bounds")
        return self.data[index]

    def set_value(self, index: int, value: int | float) -> None:
        if index < 0 or index >= len(self.data):
            raise IndexError("Index out of bounds")
        self.data[index] = value

    def show(self):
        print(self)
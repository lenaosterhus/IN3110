from functools import reduce

class Array:
    """A class for representing a grid of values.

    Attributes:
        shape (tuple): The shape of the array, represented as a tuple.
            A 1D array with n elements will have shape = (n,).
            A 2D array with n rows and m columns will have shape = (n, m).
        values (int, float or bool): The array's values.
        dimensions (type): The dimension of the array.

    """

    def __init__(self, shape, *values):
        """Checks that the arguments are of correct data type and initializes the array

        Args:
            shape (tuple): shape of the array as a tuple. A 1D array with n elements will have shape = (n,).
            *values: The values in the array. These should all be the same data type. Either numeric or boolean.
        Raises:
            ValueError: If shape is not a tuple.
            ValueError: If the values are not numberic or boolean and all of the same type.
            ValueError: If the number of values does not fit with the shape.
        """

        # Check that shape is a tuple that contains int values
        if (isinstance(shape, tuple) and all(isinstance(n, int) for n in shape)):
            self.shape = shape
        else:
            raise ValueError("Shape is not a tuple with int values")

        # Check that the first element is of numeric og boolean data type, if not raise ValueError
        if isinstance(values[0], (int, float, bool)):
            data_type = type(values[0])
        else:
            raise ValueError("Values must be numeric or boolean")
        # Check that all elements are of the same data type, if not raise TypeError
        if all(isinstance(element, data_type) for element in values):
            self.values = values
        else:
            raise ValueError("All values are not of same data type")

        self.dimensions = len(shape)

        # Check that the array contains the correct amount of elements
        if self.dimensions == 1: # 1D
            no_elements = shape[0]
        else: # 2D
            no_elements = shape[0] * shape[1]
        if no_elements != len(self.values):
            raise ValueError("The number of values does not fit with the shape")


    def __str__(self):
        """Returns a nicely printable string representation of the array.

        Returns:
            str: A string representation of the array. For example:
                "[1, 2, 3]" for a 1D Array or "[[8, 3]\n[4, 1]\n[6, 1]]" for 2D.

        """
        nice_string = "["
        if self.dimensions == 1:
            nice_string += ', '.join(map(str, self.values))
        else:
            columns = self.shape[1]  # number of columns
            rows = self.shape[0]  # number of rows

            for i in range(rows):
                nice_string += "[" + ', '.join(map(str, self.values[(i * columns):(i + 1) * columns])) + "]"
                if i < rows-1:
                    nice_string += "\n"

        return nice_string + "]"


    def __add__(self, other):
        """Element-wise adds Array with another Array or number.

        If other is an Array, it must have the same shape and contain the same
        data type as self.

        Args:
            other (Array, float, int): The array or number to add element-wise to this array.

        Returns:
            Array: the sum as a new array, or NotImplemented if supplied
            with unsupported arguments.

        """

        if isinstance(other, Array):
            if self.shape != other.shape:
                return NotImplemented

            sum_list = map(lambda x, y: x + y, self.values, other.values)

        elif isinstance(other, (int, float)):
            sum_list = map(lambda x: x + other, self.values)

        else:
            return NotImplemented

        return Array(self.shape, *sum_list)

    def __radd__(self, other):
        """Element-wise adds Array with another Array or number.

        If other is an Array, it must have the same shape and contain the same
        data type as self.

        Args:
            other (Array, float, int): The array or number to add element-wise to this array.

        Returns:
            Array: the sum as a new array, or NotImplemented if supplied
            with unsupported arguments.

        """
        return self + other


    def __sub__(self, other):
        """Element-wise subtracts an Array or number from this Array.

        If other is an Array, it must have the same shape and contain the same
        data type as self.

        Args:
            other (Array, float, int): The array or number to subtract element-
            wise from this array.

        Returns:
            Array: the difference as a new array, or NotImplemented if supplied
            with unsupported arguments.
        """
        if isinstance(other, Array):
            if self.shape != other.shape:
                return NotImplemented

            diff_list = map(lambda x, y: x - y, self.values, other.values)

        elif isinstance(other, (int, float)):
            diff_list = map(lambda x: x - other, self.values)

        else:
            return NotImplemented

        return Array(self.shape, *diff_list)

    def __rsub__(self, other):
        """Element-wise subtracts an Array or number from this Array.

        If other is an Array, it must have the same shape and contain the same
        data type as self.

        Args:
            other (Array, float, int): The array or number to subtract element-
            wise from this array.

        Returns:
            Array: the difference as a new array, or NotImplemented if supplied
            with unsupported arguments.
        """
        return self - other


    def __mul__(self, other):
        """Element-wise multiplies this Array with a number or array.

        If other is an Array, it must have the same shape and contain the same
        data type as self.

        Args:
            other (Array, float, int): The array or number to multiply
            element-wise to this array.

        Returns:
            Array: a new array with every element multiplied with `other`,
            or NotImplemented if supplied with unsupported arguments.

        """
        if isinstance(other, Array):
            if self.shape != other.shape:
                return NotImplemented

            product_list = map(lambda x, y: x * y, self.values, other.values)

        elif isinstance(other, (int, float)):
            product_list = map(lambda x: x * other, self.values)

        else:
            return NotImplemented

        return Array(self.shape, *product_list)

    def __rmul__(self, other):
        """Element-wise multiplies this Array with a number or array.

        If other is an Array, it must have the same shape and contain the same
        data type as self.

        Args:
            other (Array, float, int): The array or number to multiply
            element-wise to this array.

        Returns:
            Array: a new array with every element multiplied with `other`
            or NotImplemented, if supplied with unsupported arguments.

        """
        return self * other


    def __eq__(self, other):
        """Compares an Array with another Array.

        If the two array shapes do not match, it returns False.
        If `other` is an unexpected type, it returns False.

        Args:
            other (Array): The array to compare with this array.

        Returns:
            bool: True if the two arrays are equal. False otherwise.

        """
        if (isinstance(other, Array) and self.shape == other.shape):
            return self.values == other.values

        return False


    def __getitem__(self, key):
        """Gets the element at given key in Array.

        Args:
            key (int): The index of element to get.

        Returns:
            int, float, Array: The element at given key.

        """
        if self.dimensions == 1:
            return self.values[key]

        return self.values[key*self.shape[1]:]



    def is_equal(self, other):
        """Compares an Array element-wise with another Array or number.

        If `other` is an array and the two array shapes do not match,
        a ValueError is raised.

        Args:
            other (Array, float, int): The array or number to compare with this array.

        Returns:
            Array: An array of booleans with True where the two arrays match and
                   False where they do not.
                   Or if `other` is a number, it returns True where the array is equal
                   to the number and False where it is not.
        Raises:
            ValueError: If the shape of self and other are not equal, or if other
            is not an Array or a number.

        """
        if isinstance(other, Array):
            if self.shape != other.shape:
                raise ValueError("Arrays of different shapes")

            bool_list = map(lambda x, y: x == y, self.values, other.values)

        elif isinstance(other, (int, float)):
            bool_list = map(lambda x: x == other, self.values)

        else:
            raise ValueError("Other must be Array with same shape or number")

        return Array(self.shape, *bool_list)

    def mean(self):
        """Computes the mean of the array.

        Only works with numeric elements.

        Returns:
            float: The mean of the array values.

        Raises:
            ValueError: If the values are not numeric (int or float) elements.
        """
        if isinstance(self.values[0], (float, int)):
            return reduce(lambda x, y: x + y, self.values) / len(self.values)
        raise ValueError("Only works with numeric data types as values")

    def variance(self):
        """Computes the variance of the array.

        Only works with numeric elements.
        The variance is computed as: mean((x - x.mean())**2).

        Returns:
            float: The mean of the array values.

        Raises:
            ValueError: If the values are not numeric (int or float) elements.
            
        """
        if isinstance(self.values[0], (float, int)):
            avg = self.mean()
            return sum( map(lambda x: (x - avg)**2, self.values)) / len(self.values)
        raise ValueError("Only works with numeric data types as values")

    def min_element(self):
        """Returns the smallest value of the array.

        Only works with numeric elements.

        Returns:
            float: The value of the smallest element in the array.
        """
        return min(self.values, key=float)

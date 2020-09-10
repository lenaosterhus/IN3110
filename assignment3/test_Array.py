from Array import Array
import pytest

class TestStr:
    def test_str_1D(self):
        array1 = Array((3,), 1, 2, 3)

        assert str(array1) == "[1, 2, 3]"

    def test_str_2D(self):
        array1 = Array((3, 2), 8, 3, 4, 1, 6, 1)

        assert str(array1) == "[[8, 3]\n[4, 1]\n[6, 1]]"

class TestAdd:
    def test_add_1D_array(self):
        array1 = Array((3,), 1, 2, 3)
        array2 = Array((3,), 2, 3, 4)
        result = array1 + array2

        assert result[0] == 3
        assert result[1] == 5
        assert result[2] == 7

    def test_add_1D_float(self):
        array1 = Array((3,), 1.0, 2.0, 3.0)
        result = array1 + 2.0
        result2 = 2.0 + array1

        assert result[0] == 3.0
        assert result2[0] == 3.0
        assert result[1] == 4.0
        assert result[2] == 5.0
        assert result2[2] == 5.0

    def test_add_1D_incorrect_shape(self):
        array1 = Array((3,), 1, 2, 3)
        array2 = Array((4,), 2, 3, 4, 5)

        with pytest.raises(TypeError):
            array1 + array2

    def test_add_2D_array(self):
        array1 = Array((3,3), 1, 2, 3, 4, 5, 6, 7, 8, 9)
        array2 = Array((3,3), 2, 3, 4, 5, 6, 7, 8, 9, 10)
        result = array1 + array2

        assert result[0][0] == 3
        assert result[1][2] == 13
        assert result[2][2] == 19

class TestSub:
    def test_sub_1D_array(self):
        array1 = Array((3,), 1, 2, 3)
        array2 = Array((3,), 2, 3, 4)
        result = array2 - array1

        assert result[0] == 1
        assert result[1] == 1
        assert result[2] == 1

    def test_sub_1D_float(self):
        array1 = Array((3,), 1.0, 2.0, 3.0)
        result = array1 - 2.0
        result2 = 2.0 - array1

        assert result[0] == -1.0
        assert result2[0] == -1.0
        assert result[1] == 0.0
        assert result[2] == 1.0
        assert result2[2] == 1.0

    def test_sub_1D_incorrect_type(self):
        array1 = Array((3,), 1, 2, 3)

        with pytest.raises(TypeError):
            array1 - "string"

    def test_sub_2D_array(self):
        array1 = Array((2,3), 1, 2, 3, 4, 5, 6)
        array2 = Array((2,3), 2, 3, 4, 5, 6, 4)
        result = array1 - array2

        assert result[0][0] == -1
        assert result[1][1] == -1
        assert result[1][2] == 2

class TestMul:
    def test_mul_1D_array(self):
        array1 = Array((3,), 1, 2, 3)
        array2 = Array((3,), 2, 3, 4)
        result = array1 * array2

        assert result[0] == 2
        assert result[1] == 6
        assert result[2] == 12

    def test_mul_1D_float(self):
        array1 = Array((3,), 1.0, 2.0, 3.0)
        result = array1 * 2.0

        assert result[0] == 2.0
        assert result[1] == 4.0
        assert result[2] == 6.0

    def test_mul_1D_incorrect_type(self):
        array1 = Array((3,), 1, 2, 3)

        with pytest.raises(TypeError):
            array1 * "string"

    def test_mul_2D_array(self):
        array1 = Array((2,3), 1, 2, 3, 4, 5, 6)
        array2 = Array((2,3), 2, 3, 4, 5, 6, 4)
        result = array1 * array2

        assert result[0][0] == 2
        assert result[1][1] == 30
        assert result[1][2] == 24

class TestEq:
    def test_eq_1D_true_int(self):
        # Tests two 1D arrays that are of same shape and contains the same int values
        array1 = Array((3,), 1, 2, 3)
        array2 = Array((3,), 1, 2, 3)

        assert array1 == array2

    def test_eq_1D_true_bool(self):
        # Tests two 1D arrays that are of same shape and contains the same boolean values
        array1 = Array((3,), True, True, False)
        array2 = Array((3,), True, True, False)

        assert array1 == array2

    def test_eq_1D_false(self):
        # Tests that two 1D arrays that are of different shape returns false
        array1 = Array((3,), 1, 2, 3)
        array2 = Array((2,), 1, 2)

        assert array1 != array2
        assert array1 != "string"

    def test_eq_2D_array(self):
        # Tests that two 2D arrays that are of same shape and contains the same int values returns true
        # and that two 2D arrays that are of the same shape, but contains different values return false
        array1 = Array((2,3), 1, 2, 3, 4, 5, 6)
        array2 = Array((2,3), 1, 2, 3, 4, 5, 6)
        array3 = Array((2,3), 2, 3, 4, 5, 6, 4)

        assert array1 == array2
        assert array1 != array3

class TestIsEqual:
    def test_is_equal_array(self):
        # Tests two 1D arrays with integers
        array1 = Array((3,), 1, 2, 3)
        array2 = Array((3,), 1, 5, -3)
        result = array1.is_equal(array2)
        expected = Array((3,), True, False, False)

        assert result == expected

    def test_is_equal_int(self):
        # Tests one 1D array with integers and a integer as parameter
        array1 = Array((3,), 1, 2, 3)
        number = 2
        result = array1.is_equal(number)
        expected = Array((3,), False, True, False)

        assert result == expected

    def test_is_equal_incorrect(self):
        # Tests that a ValueError is raised when called on one 1D array with
        # another array of different shape and the wrong data type
        array1 = Array((3,), 1, 2, 3)
        array2 = Array((2,), 2, 3)

        with pytest.raises(ValueError):
            array1.is_equal(array2)
            array1.is_equal("string")

    def test_is_equal_2d_array(self):
        # Tests two 2D arrays with integers
        array1 = Array((2,3), 1, 2, 3, 4, 5, 6)
        array2 = Array((2,3), 2, 3, 3, 5, 6, 6)
        result = array1.is_equal(array2)
        expected = Array((2,3), False, False, True, False, False, True)

        assert result == expected

class TestMean:
    def test_mean_correct(self):
        array1 = Array((4,), 1, 2, 3, 2)
        result = array1.mean()

        assert result == 2.0

    def test_mean_incorrect(self):
        array1 = Array((3,), 1.0, 2.0, 3.0)
        result = array1.mean()

        assert result != 1

    def test_mean_2D_correct(self):
        array1 = Array((2,3), 1, 2, 3, 4, 5, 6)
        result = array1.mean()
        expected = sum([1, 2, 3, 4, 5, 6]) / 6

        assert result == expected

class TestVariance:
    def test_variance_correct(self):
        array1 = Array((3,), 1, 2, 3)
        result = array1.variance()
        expected = (((1-2)**2) + ((2-2)**2) + ((3-2)**2)) / 3

        assert result == expected

    def test_variance_incorrect(self):
        array1 = Array((3,), 1, 2, 3)
        result = array1.variance()
        incorrect = (((1-2)**2) + ((2-2)**2) + ((3-2)**2)) / 3 + 5

        assert result != incorrect

class TestMinElement:
    def test_min_element_correct(self):
        array1 = Array((3,), -1.0, 2.4, 1.0)
        array2 = Array((3,), -1, 2, 1)
        array3 = Array((2,), True, False)
        result1 = array1.min_element()
        result2 = array2.min_element()
        result3 = array3.min_element()

        assert result1 == -1.0
        assert result2 == -1
        assert result3 == False

    def test_min_element_incorrect(self):
        array1 = Array((4,), -1.0, 2.4, 1.0, -1.0)
        result = array1.min_element()

        assert result != 1.0

    def test_min_element_2D_correct(self):
        array1 = Array((2,3), 1, 2, 3, 4, 0, 6)
        result = array1.min_element()

        assert result == 0

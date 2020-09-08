from Array import Array
import pytest

class TestStr:
    def test_str_1d(self):
        array1 = Array((3,), 1, 2, 3)

        assert str(array1) == "[1, 2, 3]"

    def test_str_2d(self):
        array1 = Array((3, 2), 8, 3, 4, 1, 6, 1)

        assert str(array1) == "[8, 3]\n[4, 1]\n[6, 1]"

class TestAdd:
    def test_add_1d_array(self):
        array1 = Array((3,), 1, 2, 3)
        array2 = Array((3,), 2, 3, 4)
        result = array1 + array2

        assert result[0] == 3
        assert result[1] == 5
        assert result[2] == 7

    def test_add_1d_float(self):
        array1 = Array((3,), 1.0, 2.0, 3.0)
        result = array1 + 2.0

        assert result[0] == 3.0
        assert result[1] == 4.0
        assert result[2] == 5.0

    def test_add_1d_shape_error(self):
        array1 = Array((3,), 1, 2, 3)
        array2 = Array((4,), 2, 3, 4, 5)

        with pytest.raises(TypeError):
            array1 + array2

    def test_add_2d_array(self):
        array1 = Array((3,3), 1, 2, 3, 4, 5, 6, 7, 8, 9)
        array2 = Array((3,3), 2, 3, 4, 5, 6, 7, 8, 9, 10)
        result = array1 + array2

        assert result[0][0] == 3
        assert result[1][2] == 13
        assert result[2][2] == 19

class TestSub:
    def test_sub_1d_array(self):
        array1 = Array((3,), 1, 2, 3)
        array2 = Array((3,), 2, 3, 4)
        result = array2 - array1

        assert result[0] == 1
        assert result[1] == 1
        assert result[2] == 1

    def test_sub_1d_float(self):
        array1 = Array((3,), 1.0, 2.0, 3.0)
        result = array1 - 2.0

        assert result[0] == -1.0
        assert result[1] == 0.0
        assert result[2] == 1.0

    def test_sub_1d_type_error(self):
        array1 = Array((3,), 1, 2, 3)

        with pytest.raises(TypeError):
            array1 - "string"

    def test_sub_2d_array(self):
        array1 = Array((2,3), 1, 2, 3, 4, 5, 6)
        array2 = Array((2,3), 2, 3, 4, 5, 6, 4)
        result = array1 - array2

        assert result[0][0] == -1
        assert result[1][1] == -1
        assert result[1][2] == 2

class TestMul:
    def test_mul_1d_array(self):
        array1 = Array((3,), 1, 2, 3)
        array2 = Array((3,), 2, 3, 4)
        result = array1 * array2

        assert result[0] == 2
        assert result[1] == 6
        assert result[2] == 12

    def test_mul_1d_float(self):
        array1 = Array((3,), 1.0, 2.0, 3.0)
        result = array1 * 2.0

        assert result[0] == 2.0
        assert result[1] == 4.0
        assert result[2] == 6.0

    def test_mul_1d_error(self):
        array1 = Array((3,), 1, 2, 3)

        with pytest.raises(TypeError):
            array1 * "string"

    def test_mul_2d_array(self):
        array1 = Array((2,3), 1, 2, 3, 4, 5, 6)
        array2 = Array((2,3), 2, 3, 4, 5, 6, 4)
        result = array1 * array2

        assert result[0][0] == 2
        assert result[1][1] == 30
        assert result[1][2] == 24

class TestEq:
    def test_eq_true_int(self):
        array1 = Array((3,), 1, 2, 3)
        array2 = Array((3,), 1, 2, 3)

        assert array1 == array2

    def test_eq_true_bool(self):
        array1 = Array((3,), True, True, False)
        array2 = Array((3,), True, True, False)

        assert array1 == array2

    def test_eq_false(self):
        array1 = Array((3,), 1, 2, 3)
        array2 = Array((2,), 1, 2)

        assert array1 != array2
        assert array1 != "string"

    def test_eq_2d_array(self):
        array1 = Array((2,3), 1, 2, 3, 4, 5, 6)
        array2 = Array((2,3), 1, 2, 3, 4, 5, 6)
        array3 = Array((2,3), 2, 3, 4, 5, 6, 4)

        assert array1 == array2
        assert array1 != array3

class TestIsEqual:
    def test_is_equal_array(self):
            array1 = Array((3,), 1, 2, 3)
            array2 = Array((3,), 1, 5, -3)
            result = array1.is_equal(array2)
            expected = Array((3,), True, False, False)

            assert result == expected

    def test_is_equal_number(self):
            array1 = Array((3,), 1, 2, 3)
            number = 2
            result = array1.is_equal(number)
            expected = Array((3,), False, True, False)

            assert result == expected

    def test_is_equal_error_shape(self):
        array1 = Array((3,), 1, 2, 3)
        array2 = Array((2,), 2, 3)

        with pytest.raises(ValueError):
            array1.is_equal(array2)
            array1.is_equal("string")

    def test_is_equal_2d_array(self):
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

    def test_mean_2d_array(self):
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

    def test_min_element_2d_array(self):
        array1 = Array((2,3), 1, 2, 3, 4, 0, 6)
        result = array1.min_element()

        assert result == 0

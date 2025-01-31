import pytest
from roundai import roundai, round_from_right

def test_basic_rounding():
    """Test basic rounding functionality"""
    assert round_from_right(123.456789, 3) == 123.457
    assert round_from_right(123.456789, 2) == 123.46
    assert round_from_right(123.456789, 1) == 123.5
    assert round_from_right(123.449, 1) == 123.5

def test_round_half_up():
    """Test that values are rounded up at .5"""
    assert round_from_right(2.5, 0) == 3
    assert round_from_right(3.5, 0) == 4
    assert round_from_right(1.5, 0) == 2

def test_preserve_original_decimals():
    """Test that original decimals are preserved when fewer than requested"""
    assert round_from_right(123.4, 3) == 123.4
    assert round_from_right(1.2, 5) == 1.2

def test_small_differences():
    """Test consistent rounding for small numerical differences"""
    x = 1.23454999999
    y = 1.23460000000
    xr = round_from_right(x, 4)
    yr = round_from_right(y, 4)
    assert xr == 1.2346
    assert yr == 1.2346

def test_zero_places():
    """Test rounding to whole numbers"""
    assert round_from_right(1.6, 0) == 2
    assert round_from_right(1.4, 0) == 1
    assert round_from_right(5.5, 0) == 6

def test_integer_input():
    """Test handling of integer inputs"""
    assert round_from_right(123, 2) == 123
    assert round_from_right(100, 1) == 100

def test_edge_cases():
    """Test edge cases and special values"""
    assert round_from_right(0.0, 2) == 0.0
    assert round_from_right(0.001, 2) == 0.0
    assert round_from_right(999.999, 2) == 1000.0

def test_main_roundai_function():
    """Test the main roundai function works the same as round_from_right"""
    assert roundai(123.456789, 3) == round_from_right(123.456789, 3)
    assert roundai(2.5, 0) == round_from_right(2.5, 0)
    assert roundai(123.4, 3) == round_from_right(123.4, 3)

def test_negative_places():
    """Test that negative places raise ValueError"""
    with pytest.raises(ValueError):
        round_from_right(123.456, -1)

def run_tests():
    """Run all test functions and report results"""
    test_functions = [
        test_basic_rounding,
        test_round_half_up,
        test_preserve_original_decimals,
        test_small_differences,
        test_zero_places,
        test_integer_input,
        test_edge_cases,
        test_main_roundai_function,
        test_negative_places
    ]
    
    passed = 0
    failed = 0
    
    for test in test_functions:
        try:
            test()
            print(f"✓ {test.__name__} passed")
            passed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__} failed: {str(e)}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__} failed with error: {str(e)}")
            failed += 1
    
    print(f"\nTest Summary:")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Total: {passed + failed}")

if __name__ == "__main__":
    run_tests()
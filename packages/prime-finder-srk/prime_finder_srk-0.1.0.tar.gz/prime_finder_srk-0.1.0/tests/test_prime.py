import pytest
from prime_finder import get_nth_prime

def test_first_few_primes():
    """Test the first few prime numbers."""
    assert get_nth_prime(1) == 2
    assert get_nth_prime(2) == 3
    assert get_nth_prime(3) == 5
    assert get_nth_prime(4) == 7
    assert get_nth_prime(5) == 11
    assert get_nth_prime(6) == 13

def test_larger_prime():
    """Test a larger prime number."""
    assert get_nth_prime(25) == 97
    assert get_nth_prime(100) == 541

def test_invalid_input():
    """Test invalid inputs."""
    with pytest.raises(ValueError):
        get_nth_prime(0)
    with pytest.raises(ValueError):
        get_nth_prime(-1)

def test_is_prime():
    """Test the is_prime helper function."""
    from prime_finder.prime import is_prime
    
    # Test some known prime numbers
    assert is_prime(2)
    assert is_prime(3)
    assert is_prime(5)
    assert is_prime(7)
    assert is_prime(11)
    assert is_prime(13)
    assert is_prime(17)
    assert is_prime(19)
    assert is_prime(23)
    assert is_prime(29)
    
    # Test some known non-prime numbers
    assert not is_prime(-1)
    assert not is_prime(0)
    assert not is_prime(1)
    assert not is_prime(4)
    assert not is_prime(6)
    assert not is_prime(8)
    assert not is_prime(9)
    assert not is_prime(10)
    assert not is_prime(12)
    assert not is_prime(15)

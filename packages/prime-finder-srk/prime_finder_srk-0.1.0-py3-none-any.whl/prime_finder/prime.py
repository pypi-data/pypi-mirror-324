from typing import List

def is_prime(n: int) -> bool:
    """Check if a number is prime.
    
    Args:
        n: The number to check
        
    Returns:
        bool: True if the number is prime, False otherwise
    """
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    
    # Only check odd numbers up to the square root of n
    for i in range(3, int(n ** 0.5) + 1, 2):
        if n % i == 0:
            return False
    return True

def get_nth_prime(n: int) -> int:
    """Get the nth prime number.
    
    Args:
        n: The position of the prime number to find (1-based indexing)
        
    Returns:
        int: The nth prime number
        
    Raises:
        ValueError: If n is less than 1
    """
    if n < 1:
        raise ValueError("n must be greater than 0")
    
    if n == 1:
        return 2
    
    count = 1  # We've found one prime (2)
    num = 1    # Start checking from 3 (num + 2)
    
    while count < n:
        num += 2  # Check only odd numbers
        if is_prime(num):
            count += 1
    
    return num

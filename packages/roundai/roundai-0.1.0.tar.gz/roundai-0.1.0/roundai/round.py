from decimal import Decimal, ROUND_HALF_UP
import random

def roundai(value: float, places: int) -> float:
    return round_from_right(value, places)

def round_from_right(value: float, places: int) -> float:
    """Rounds a number starting from the rightmost digit and propagates leftward.
    
    Args:
        value: The float value to round
        places: Number of significant places to keep
        
    Examples:
        # Basic rounding from right
        round_from_right(123.456789, 3) -> 123.457
        round_from_right(123.456789, 2) -> 123.46
        round_from_right(123.456789, 1) -> 123.5
        round_from_right(123.449, 1) -> 123.5
        
        # Differences from built-in round():
        round_from_right(2.5, 0) -> 3        # Standard rounding
        round(2.5) -> 2                      # Python's "round to even"
        
        round_from_right(123.4, 3) -> 123.4  # Preserves original if fewer decimals
        round(123.4, 3) -> 123.400           # Adds trailing zeros

        x = 1.23454999999
        y = 1.23460000000
        round(x, 4) == 1.2345
        round(y, 4) == 1.2346
        round_from_right(x, 4) == 1.2346    # Consistently rounds from rightmost digit
        round_from_right(y, 4) == 1.2346  # Stable for small changes
    """
    if places < 0:
        raise ValueError("places must be non-negative")
    
    # Use Decimal for high-precision arithmetic
    d = Decimal(str(value))
    
    # Determine the current number of decimal places
    tuple_d = d.as_tuple()
    if tuple_d.exponent >= 0:
        return float(d)  # No decimal places
    
    current_places = -tuple_d.exponent
    if current_places <= places:
        return float(d)
    

    if places == 0:
        return float(d.quantize(Decimal('1'), rounding=ROUND_HALF_UP))

    # Apply rounding from the rightmost digit
    while current_places > places:
        # Round only the rightmost digit each time
        rounding_format = '0.' + '0' * (current_places - 1)
        d = d.quantize(Decimal(rounding_format), rounding=ROUND_HALF_UP)
        # Recalculate current_places after rounding
        new_exponent = d.as_tuple().exponent
        current_places = -new_exponent if new_exponent < 0 else 0
    
    return float(d)
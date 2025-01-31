# RoundAI

A smart rounding library that rounds numbers from right to left, providing more intuitive behavior than Python's built-in `round()` function in certain cases.

## Installation

```bash
pip install roundai
```

## Usage

```python
from roundai import roundai

# Basic rounding
print(roundai(123.456789, 3))  # -> 123.457
print(roundai(123.456789, 2))  # -> 123.46
print(roundai(123.456789, 1))  # -> 123.5

# Key differences from built-in round():
print(roundai(2.5, 0))         # -> 3        (Standard rounding)
print(round(2.5))              # -> 2        (Python's "round to even")

# Preserves original if fewer decimals
print(roundai(123.4, 3))       # -> 123.4    (Preserves original)
print(round(123.4, 3))         # -> 123.400  (Adds trailing zeros)

# Consistent rounding from rightmost digit
x = 1.23454999999
y = 1.23460000000
print(roundai(x, 4))           # -> 1.2346   (Consistently rounds from right)
print(roundai(y, 4))           # -> 1.2346   (Stable for small changes)
```

## Features

- Rounds numbers from right to left, propagating changes
- More intuitive behavior than Python's built-in round()
- Preserves original precision when possible
- Consistent rounding behavior for similar numbers
- No trailing zeros added
- Uses standard rounding rules (rounds up for .5)

## Development

To set up the development environment:

```bash
# Clone the repository
git clone https://github.com/BackFlipAI/roundai.git
cd roundai

# Install development dependencies
pip install -e ".[test]"
```

### Running Tests

To run the tests:

```bash
pytest
```

For test coverage:

```bash
pytest --cov=roundai
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes and add tests
4. Run the test suite to ensure everything works
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request 
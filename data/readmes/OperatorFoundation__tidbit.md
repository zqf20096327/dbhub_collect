# Tidbit Protocol

A compact radio messaging protocol that runs on top of WSPR (Weak Signal Propagation Reporter). Tidbit uses mixed-radix encoding to efficiently pack structured data into 50-bit packets.

## Features

- **Efficient Encoding**: Mixed-radix number system wastes no bits
- **Flexible Modes**: Define custom message formats with type safety
- **Multiple Interfaces**: CLI, TUI, and Python API
- **Type System**: Enums, Integers, Floats, Structures, and Conditionals
- **OTP Encryption**: One-time pad support for secure communications

## Installation

### Using uv (recommended)
```bash
uv pip install -e .
```

### Using pip
```bash
pip install -e .
```

### Or install dependencies only
```bash
pip install -r requirements.txt
```

## Quick Start

### Command Line Interface

```bash
# List available modes
tidbit list

# Inspect a mode
tidbit inspect "weather report"

# Encode a message
tidbit encode "weather report" '{"temperature": 22, "humidity": 65, ...}'

# Decode a message
tidbit decode "weather report" 123456
```

### Terminal User Interface

```bash
tidbit-tui
```

Interactive TUI with:
- Form-based message encoding with dropdowns and validation
- Message decoding with formatted output
- Support for all field types including conditionals

### Python API

```python
from tidbit import encode_message, decode_message, MODES

# Encode a weather report
weather_data = {
    "temperature": 22,
    "humidity": 65,
    "pressure": 1013,
    "wind speed": 15,
    "wind direction": "NE",
    "conditions": "partly cloudy",
    "visibility": "good",
    "trend": "steady"
}

encoded, total_combinations, bits = encode_message(
    MODES["weather report"], 
    weather_data
)
print(f"Encoded: {encoded} ({bits} bits)")

# Decode it back
decoded = decode_message(MODES["weather report"], encoded)
```

### Define Custom Modes

```python
from tidbit import Enum, Integer, Structure

LETTERS = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

CustomMode = {
    "priority": Enum(["low", "medium", "high", "urgent"]),
    "count": Integer(min=0, scale=1, max=100),
    "grid": Structure([Enum(LETTERS), Enum(LETTERS)]),
}

# Use it just like built-in modes
encoded, _, bits = encode_message(CustomMode, {
    "priority": "high",
    "count": 42,
    "grid": ["A", "B"]
})
```

## Field Types

- **Enum**: Choose from predefined options
- **Integer**: Range-based with min/max/scale
- **Float**: Mantissa and exponent representation
- **Mode**: Mode switching field
- **Structure**: Nested field container
- **Conditional**: Fields that vary based on discriminator
- **Text**: Compressed text (TODO)

## Built-in Modes

- **session init**: Session initiation and handshake
- **weather report**: Complete weather observations
- **rag chew question**: Common conversational topics
- **first message**: CQ, net check-in, directed calls

## Development

```bash
# Run tests
python test_tidbit.py

# Install dev dependencies
pip install -e ".[dev]"

# Format code
black tidbit/

# Lint
ruff check tidbit/
```

## How It Works

Tidbit uses a **mixed-radix number system** where each field has its own base:

```
Total = value₀ × 1 + value₁ × base₀ + value₂ × (base₀ × base₁) + ...
```

This allows perfect bit packing with zero waste. For example:
- 5 options + 8 options + 3 options = 120 combinations = 7 bits
- Traditional: 3 + 3 + 2 = 8 bits (wastes 1 bit)

## License

MIT License - See LICENSE file for details

## Contributing

Contributions welcome! Please open an issue or PR.

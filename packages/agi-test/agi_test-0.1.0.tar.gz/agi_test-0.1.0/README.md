# AGI Test Client

A Python client library for interacting with the General Reasoning platform API.

## Installation

You can install the package using pip:

```bash
pip install agi_test
```

## Making API Calls

```python
import agi

client = agi.Client(api_key=YOUR_API_KEY)

# Example data
client.get_data("math-word_problems")
```

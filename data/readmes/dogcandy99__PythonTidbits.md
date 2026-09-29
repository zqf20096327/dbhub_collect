# Medical Record Validator

A Python-based utility tool designed to sanitize and validate patient data structures. This script ensures that medical records meet specific formatting and business logic requirements before they are processed by a database.

## Features
* [cite_start]**Schema Validation**: Ensures all required fields (`patient_id`, `age`, etc.) are present[cite: 5, 6].
* [cite_start]**Data Integrity**: Uses Regular Expressions (Regex) to verify ID formats[cite: 3, 4].
* [cite_start]**Type Checking**: Validates that ages are integers and medications are stored in lists.

## Prerequisites
* Python 3.x
* `re` module (built-in)

## Usage
To validate your records, simply pass your list of dictionaries to the `validate()` function:

```python
from validator import validate

my_records = [...] 
validate(my_records)

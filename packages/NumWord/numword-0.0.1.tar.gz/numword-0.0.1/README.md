# NumWord

![Manual Test](https://github.com/HarshitDalal/numword/actions/workflows/manual_test.yml/badge.svg)
![Daily Test](https://github.com/HarshitDalal/numword/actions/workflows/daily_test.yml/badge.svg)
![PyPI](https://img.shields.io/pypi/v/NumWord)
![PyPI Downloads](https://img.shields.io/pypi/dm/NumWord)

NumWord is a Python package that converts numbers written in words to their numerical representation.

## Features

- Convert single digits, two digits, large numbers, decimal numbers, and mixed numbers from words to numbers.
- Supports English language.

## Installation

To install the package, use pip:

```bash
pip install -r requirements.txt
```

## Usage
Here is an example of how to use the NumWord package:
```python
from NumWord.word_to_num import WordToNum

converter = WordToNum(lang='en')
result = converter.words_to_number("one hundred twenty three point four five six")
print(result)  # Output: 123.456
``` 
## Running Tests
To run the tests, use the following command:
```bash
python -m unittest discover tests
```

## License
This project is licensed under the MIT License - see the [MIT License](LICENSE) file for details.


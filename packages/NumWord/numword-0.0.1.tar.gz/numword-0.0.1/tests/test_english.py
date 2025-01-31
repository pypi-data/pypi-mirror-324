import unittest

from Logs import LoggerConfig
from NumWord.word_to_num import WordToNum


class TestWordToNum(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.logger = LoggerConfig(__name__).get_logger()
        cls.word_to_num = WordToNum(lang='en')

    def test_single_digit(self):
        result = self.word_to_num.words_to_number("five")
        self.logger.info(f"Test single digit: 'five' -> {result}")
        self.assertEqual(result, 5)

    def test_two_digits(self):
        result = self.word_to_num.words_to_number("twenty one")
        self.logger.info(f"Test two digits: 'twenty one' -> {result}")
        self.assertEqual(result, 21)

    def test_large_number(self):
        result = self.word_to_num.words_to_number("one thousand two hundred thirty four")
        self.logger.info(f"Test large number: 'one thousand two hundred thirty four' -> {result}")
        self.assertEqual(result, 1234)

    def test_decimal_number(self):
        result = self.word_to_num.words_to_number("one point five")
        self.logger.info(f"Test decimal number: 'one point five' -> {result}")
        self.assertEqual(result, 1.5)

    def test_mixed_number(self):
        result = self.word_to_num.words_to_number("one hundred twenty three point four five six")
        self.logger.info(f"Test mixed number: 'one hundred twenty three point four five six' -> {result}")
        self.assertEqual(result, 123.456)


    def test_million_number(self):
        result = self.word_to_num.words_to_number("one million two hundred thirty four thousand five hundred sixty seven")
        self.logger.info(f"Test million number: 'one million two hundred thirty four thousand five hundred sixty seven' -> {result}")
        self.assertEqual(result, 1234567)

if __name__ == '__main__':
    unittest.main()

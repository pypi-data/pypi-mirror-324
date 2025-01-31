from NumWord import GetLanguage


class WordToNum:
    def __init__(self, lang="en"):
        self.word_to_num = GetLanguage().get_language(lang)

    def words_to_number(self, words):
        words = words.split()
        total = 0
        current = 0
        decimal_part = 0
        decimal_place = 0.1
        is_decimal = False

        for word in words:
            if word == "point":
                is_decimal = True
                continue

            if word.isdigit():
                scale = int(word)
                if is_decimal:
                    decimal_part += scale * decimal_place
                    decimal_place /= 10
                else:
                    current += scale
            elif word in self.word_to_num:
                scale = self.word_to_num[word]
                if is_decimal:
                    decimal_part += scale * decimal_place
                    decimal_place /= 10
                else:
                    if scale >= 1000:
                        if current == 0:
                            current = 1
                        current *= scale
                        total += current
                        current = 0
                    elif scale >= 100:
                        current *= scale
                    else:
                        current += scale
            else:
                raise ValueError(f"Word '{word}' is not recognized.")

        return total + current + decimal_part

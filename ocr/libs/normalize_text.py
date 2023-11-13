import re

from babel import numbers
from functools import lru_cache

class NormalizeText:

    map_string = {
        "0": ["o", "O", "Q"],
        "1": ["i, l"]
    }

    @staticmethod
    def format_currency(string: str, format: str = 'VND', locale: str = 'vi_VN') -> str:
        string = numbers.format_number(string, format, locale)
        string = string[:-1] + format
        return string

    @staticmethod
    def format_output(key: str, string: str) -> str:
        if key == "name":
            string = NormalizeText.format_name(string)
        string = NormalizeText.format_species_character(string)
        string = NormalizeText.format_double_spaces(string)
        return string

    @staticmethod
    def format_name(string: str) -> str:
        chars = re.escape('0123456789')
        string = re.sub(r'['+chars+']', '',string)
        return string


    @staticmethod
    def format_species_character(string: str) -> str:
        chars = re.escape('!"#$%&\'()*+:;<=>?@[\\]^_`{|}~')
        string = re.sub(r'['+chars+']', '',string)
        return string

    @staticmethod
    def format_double_spaces(string: str) -> str:
        string = " ".join(string.split())
        return string

    @staticmethod
    def format_number(string: str) -> str:
        return string

    @staticmethod
    @lru_cache
    def normalize_amount(string: str):
        count_1 = 0 # ","
        count_2 = 0 # "."
        for i in string:
            if i == ",":
                count_1 += 1
            elif i == ".":
                count_2 += 1
        if count_1 == 0 and count_2 == 0:
            return NormalizeText.convertStringToInt(string)

        # 1,000.00
        if count_1 >= count_2:
            pos = string.find(".")
        else:
            pos = string.find(",")

        # 1,000 or 1.000
        if pos != -1:
            string = string[:pos]
        amount = NormalizeText.convertStringToInt(string)
        # amount_currency = numbers.format_currency(amount, "VND", locale="vi_VN")
        # amount_currency = amount_currency[:-1] + "VND"
        return str(amount)

    @staticmethod
    def convertStringToInt(string: str):
        string = NormalizeText.auto_correct(string)
        try:
            string = "".join(
                value for value in string if value in "0123456789")
            if string != "":
                return int(string)
        except:
            return 0
        return 0

    @staticmethod
    def auto_correct(string: str):
        # string is upper
        numeric = "0123456789"
        check = {
            "O": "0",
            "Q": "0",
            "I": "1",
            "L": "1",
        }
        string = string.replace("Z", "2")
        string = list(string)
        for index in range(1,len(string)-1):
            if string[index] in check.keys():
                # 5l6 => 516
                # 1o.000 => 10.000
                # 10.o00 => 10.000
                # VNDI00.000 => VND100.000
                # 100.00OVND => 100.000VND
                if string[index-1] in numeric and string[index+1] in numeric \
                or string[index-1] in numeric and string[index+1] in ".,V" \
                or string[index-1] in ".,D" and string[index+1] in numeric:
                    string[index] = check[string[index]]
        return "".join(string)

    @staticmethod
    @lru_cache
    def normalize_date(string: str) -> str:
        def format_date(string: str, slice_char: str) -> str:
            # dd/MM/yyyy
            start = string.index(slice_char)
            # dd/
            if start >= 2:
                string = string[start-2:]
            # /yyyy
            end = string.rindex(slice_char)
            string = string[:end+5]
            return string

        if "/" not in string and "-" not in string:
            return ""

        # "/-" without number string
        elif "".join(i for i in string if i in '0123456789') == "":
            return ""

        else:
            string = "".join(
                value for value in string if value in "0123456789/-")
            # Remove /12/01/2022 => 12/01/2022
            if string[0] == "/" or string[0] == "-":
                string = string[1:]
            # Remove 12/01/2022/ => 12/01/2022
            if string[-1] == "/" or string[-1] == "-":
                string = string[:-1]

            if string.count("/") == 2:
                return format_date(string, "/")
            elif string.count("-") == 2:
                return format_date(string, "-")
            return string

    @staticmethod
    @lru_cache
    def normalize_time(string: str) -> str:
        def format_time(string: str, slice_char: str) -> str:
            # hh:mm:ss
            start = string.index(slice_char)
            # hh:
            if start >= 2:
                string = string[start-2:]
            # :ss
            end = string.rindex(slice_char)
            string = string[:end+3]
            return string

        string = string.replace(";", ":")
        string = string.replace(".", ":")
        string = string.replace(",", ":")
        if ":" not in string:
            return ""

        # "/-" without number string
        elif "".join(i for i in string if i in '0123456789') == "":
            return ""

        else:
            string = "".join(
                value for value in string if value in "0123456789:")

            # Remove :12:00:00 => 12:00:00
            if string[0] == ":":
                string = string[1:]

            # Remove 12:00:00: => 12:00:00
            if string[-1] == ":":
                string = string[:-1]

            if string.count(":") == 2:
                return format_time(string, ":")
            return string
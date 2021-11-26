import re
import enchant

snake_case_regex = "(_)?[a-z0-9]+(?:_[a-z0-9]+)*$"
two_caps_cons_regex = ".*[A-Z]{2,}.*"
caps_regex = "[A-Z]+"
external_underscore_regex = "_.*_$"
extern_under_snake_regex = "_[a-z]+_"
consecutive_underscore_regex = ".*__.*$"
camel_case_grab_regex = "([A-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$)))"
snake_case_grab_regex = "([a-z](?:[a-z]+|[A-Z]*(?=[A-Z]|$)))"
first_small_word_camel_case_regex = "^[a-z].*?(?=[A-Z])"
all_small_words_regex = "[a-z]+$"
dictionary = enchant.Dict("en_US")

preposition_list = ["aboard", "about", "above",
                    "across",
                    "after",
                    "against,"
                    "along",
                    "amid",
                    "among",
                    "anti",
                    "around,"
                    "as",
                    "at",
                    "before",
                    "behind",
                    "below",
                    "beneath",
                    "beside",
                    "besides",
                    "between",
                    "beyond",
                    "but",
                    "by",
                    "concerning",
                    "considering",
                    "despite",
                    'down',
                    "during",
                    "except",
                    "excepting",
                    "excluding",
                    "following",
                    "for",
                    "from",
                    "in",
                    "inside",
                    "into",
                    "like",
                    "minus",
                    "near",
                    "of",
                    "off",
                    "on",
                    "onto",
                    'opposite',
                    "outside",
                    "over",
                    "past",
                    "per",
                    "plus",
                    "regarding",
                    "round",
                    "save",
                    "since",
                    "than",
                    "through",
                    "to",
                    "toward",
                    "towards",
                    "under",
                    "underneath",
                    "unlike",
                    "until",
                    "up",
                    "upon",
                    "versus",
                    "via",
                    "with",
                    "within", "without"]
word_numbers = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve',
                'thirteen', 'fourteen',
                'fifteen', 'sixteen', 'seventeen', 'eighteen',
                'nineteen', 'twenty', 'thirty', 'forty',
                'fifty', 'sixty', 'seventy', 'eighty',
                'ninety', 'zero', 'hundred']

encoding_format = ['b', 'ch', 'c', 'dw', 'f', 'n', 'i', 'fp', 'db', 'p', 'rg', 'sz', 'u16', 'u32', 'st', 'fn', 'psz',
                   'rgfp', 'aul', 'hwnd', 'lpsz']

NAMING_CONVENTION_ANOMOLY = "Naming Convention Anomoly"
CAPITALISATION_ANOMOLY = "Capitalisation Anomaly"
LONG_IDENTIFIER_NAME = 'Long Identifier Name'
SHORT_IDENTIFIER_NAME = 'Short Identifier Name'
EXCESSIVE_WORDS = "Excessive Words or Number of Words"
EXTERNAL_UNDERSCORES = "External Underscores"
CONSECUTIVE_UNDERSCORES = "Consecutive Underscores"
DICTIONARY_WORDS = "Dictionary Words or Capitalization Anomaly"
NUMERIC_IDENTIFIER_NAME = "Numeric Identifier Name"
IDENTIFIER_ENCODING = "Identifier Encoding"


# This function validates if an identifier matches the snake case and validates accordingly
def snake_case_check(string, error_string):
    c = 0
    if '_' in string:

        if bool(re.match(extern_under_snake_regex, string)):
            return True

        if bool(re.match(snake_case_regex, string)):
            return True

        screaming_set = string.split("_")
        if len(screaming_set) > 1:
            for i in screaming_set:
                if i.upper() == i:
                    c += 1
                else:
                    if NAMING_CONVENTION_ANOMOLY not in error_string:
                        error_string.append(NAMING_CONVENTION_ANOMOLY)
                    return False
            if c == len(screaming_set):
                return True
        else:
            if NAMING_CONVENTION_ANOMOLY not in error_string:
                error_string.append(NAMING_CONVENTION_ANOMOLY)
                return False
            else:
                return True
    return True


# This function checks if there is any capitalization anomoly
def two_caps_check(string, error_string):
    # here check again
    if '_' in string:
        return snake_case_check(string, error_string)

    res = any(ele.isupper() for ele in string)

    if bool(re.match(caps_regex, string)):
        all_caps = re.findall(caps_regex, string)
        if len(all_caps) == 1:
            return True

    if res:
        if bool(re.match(two_caps_cons_regex, string)):
            if CAPITALISATION_ANOMOLY not in error_string:
                error_string.append(CAPITALISATION_ANOMOLY)
                return False
    return True


# This function checks whether the input identifier is a long identifier
def many_chars_check(string, error_string):
    if len(string) > 20:
        if LONG_IDENTIFIER_NAME not in error_string:
            error_string.append(LONG_IDENTIFIER_NAME)
            return False
    return True


# This function checks if an identifier is too short
def short_identifier_check(string, error_string):
    if string in ['c', 'd', 'g', 'e', 'i', 'in', 'inOut', 'j', 'k', 'm', 'n', 'o', 'out', 't', 'x', 'y', 'z']:
        return True
    elif len(string) < 8:
        if SHORT_IDENTIFIER_NAME not in error_string:
            error_string.append(SHORT_IDENTIFIER_NAME)
            return False
    return True


# This function checks if an identifier has too many words
def number_words_check(string, error_string):
    res = any(ele.isupper() for ele in string)
    if res:
        if string[0].lower() == string[0]:
            if len(re.findall(caps_regex, string)) > 3:
                if EXCESSIVE_WORDS not in error_string:
                    error_string.append(EXCESSIVE_WORDS)
                    return False
        if len(re.findall(caps_regex, string)) > 4:
            if EXCESSIVE_WORDS not in error_string:
                error_string.append(EXCESSIVE_WORDS)
                return False
    return True


# This function checks if an input identifier has external underscores
def external_underscore_check(string, error_string):
    if '_' in string:
        if string[0] == '_' or string[-1] == '_':
            if EXTERNAL_UNDERSCORES not in error_string:
                error_string.append(EXTERNAL_UNDERSCORES)
                return False
    return True


# This functions checks if there are any consecutive identifiers
def consecutive_underscore_check(string, error_string):
    if '_' in string:
        if bool(re.match(consecutive_underscore_regex, string)):
            if CONSECUTIVE_UNDERSCORES not in error_string:
                error_string.append(CONSECUTIVE_UNDERSCORES)
                return False
    return True


# This function checks whether the camel case identifier has meaningful dictionary words
def camel_case_dict_check(string, error_string):
    res = any(ele.isupper() for ele in string)
    if res:
        if string[0] == '_' or string[-1] == '_':
            return False

        if string[0].lower() == string[0]:
            if len(re.findall(first_small_word_camel_case_regex, string)) > 0:
                first_word = re.findall(first_small_word_camel_case_regex, string)[0]
                first_word_dict = dictionary.check(first_word)
                if not first_word_dict:
                    if DICTIONARY_WORDS not in error_string:
                        error_string.append(DICTIONARY_WORDS)
                        return False

                camel_strings = re.findall(camel_case_grab_regex, string)
                # print(camel_strings)
                for i in camel_strings:
                    if not dictionary.check(i.lower()):
                        if i.lower() not in preposition_list:
                            if DICTIONARY_WORDS not in error_string:
                                error_string.append(DICTIONARY_WORDS)
                                return False
    return True


# This function checks whether the snake case identifier has meaningful dictionary words
def snake_case_dict_check(string, error_string):
    if '_' in string:
        res = any(ele.islower() for ele in string)
        if res:
            snake_strings = re.findall(snake_case_grab_regex, string)
            c = 0
            for i in snake_strings:
                if dictionary.check(i.lower()):
                    c += 1
            if c == len(snake_strings):
                return True
            else:
                if DICTIONARY_WORDS not in error_string:
                    error_string.append(DICTIONARY_WORDS)
                    return False
    return True


# This functions checks for validation anomaly
def capitalization_anamaly(string, error_string):
    if re.match(all_small_words_regex, string):
        if not dictionary.check(string):
            if DICTIONARY_WORDS not in error_string:
                error_string.append(DICTIONARY_WORDS)
                return False
    return True


# This functions checks if an identifier is completely with numbers
def numeric_identifier_name(string, error_string):
    if '_' in string:
        c = 0
        res = string.split('_')

        for i in res:
            if i.lower() in word_numbers:
                c += 1
        if c == len(res):
            if NUMERIC_IDENTIFIER_NAME not in error_string:
                error_string.append(NUMERIC_IDENTIFIER_NAME)
                return False

    if string in word_numbers:
        if NUMERIC_IDENTIFIER_NAME not in error_string:
            error_string.append(NUMERIC_IDENTIFIER_NAME)
            return False

    res = any(ele.isupper() for ele in string)
    if res:
        c = 0
        camel_strings = re.findall(camel_case_grab_regex, string)
        for i in camel_strings:
            c = c + len(i)

        if len(string) == c:
            c = 0
            for j in camel_strings:
                if j.lower() in word_numbers:
                    c += 1
            if c == len(camel_strings):
                if NUMERIC_IDENTIFIER_NAME not in error_string:
                    error_string.append(NUMERIC_IDENTIFIER_NAME)
                    return False

    return True
    # elif bool(re.match(consecutive_underscore_regex, string)):

    # word_numbers


# This functions checks for identifier encoding check
# eg: iCount, bHype etc as i, b represent integer and bits/bytes
def identifier_encoding(string, error_string):
    build_string = ''
    res = any(ele.isupper() for ele in string)
    if res:
        index = string.index(re.findall("[A-Z]", string)[0])
        ident = string[0:index]
        if ident in encoding_format:
            if IDENTIFIER_ENCODING not in error_string:
                error_string.append(IDENTIFIER_ENCODING)
                return False
    return True


# This function iteratively validates the identifier for each validation type
def final_validator(string):
    error_lis = []
    snake_case_check(string, error_lis)
    two_caps_check(string, error_lis)
    many_chars_check(string, error_lis)
    short_identifier_check(string, error_lis)
    number_words_check(string, error_lis)
    external_underscore_check(string, error_lis)
    consecutive_underscore_check(string, error_lis)
    camel_case_dict_check(string, error_lis)
    snake_case_dict_check(string, error_lis)
    capitalization_anamaly(string, error_lis)
    numeric_identifier_name(string, error_lis)
    identifier_encoding(string, error_lis)
    return error_lis

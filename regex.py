import re

def is_vowel(word):
    return bool(re.search(r'^[aeiou]$', word.lower()))

def is_valid_username(word):
    return bool(re.search(r'^[a-z]{1,32}$', word))

def is_valid_phone(phone):
    return bool(re.search())
import string
from django.core.exceptions import ValidationError

NUMERIC_CHARS = string.digits
DASH_AND_UNDERLINE_CHARS = '-_'

A_TO_Z_CHARS = {
    'uppercase' : string.ascii_uppercase,
    'lowercase' : string.ascii_lowercase,
}
VALIDATE_CHARS_FOR_USERNAME = NUMERIC_CHARS + A_TO_Z_CHARS['uppercase'] + A_TO_Z_CHARS['lowercase'] + DASH_AND_UNDERLINE_CHARS
PUNCTUATION_CHARS = string.punctuation
VALIDATE_CHARS_FOR_PASSWORDS = NUMERIC_CHARS + A_TO_Z_CHARS['uppercase'] + A_TO_Z_CHARS['lowercase'] + PUNCTUATION_CHARS

def validate_username(value: str, message: str | None = None):
    if message is None:
        message = f'"{value}" is not a validate username! Please use characters or numbers (A-Z, a-z, 0-9, -, _).\nThe first character of your username cannot be a number.'
    if value[0] in NUMERIC_CHARS:
        raise ValidationError(message)
    for c in value[1:]:
        if not c in VALIDATE_CHARS_FOR_USERNAME:
            raise ValidationError(message)

def has_target_chars(value: str, target: str, min_num: int = 1, message: str | None = None):
    if message is None:
        message = f'No {min_num} common characters were found between "{value}" and "{target}"!'
    n = 0
    for c in value:
        if c in target:
            n += 1
            if n >= min_num:
                return
    raise ValidationError(message)

def is_safe_password(value: str, message: str | None = None):
    is_message_null = message is None
    messages = ['The password is not safe!'] if is_message_null else message
    has_except = False
    # has this 3 digits of 0-9?
    try:
        has_target_chars(value, NUMERIC_CHARS, 3)
    except ValidationError as e:
        has_except = True
        if is_message_null:
            messages.append(e.message.replace(f'"{value}"', 'the password').replace(f'"{NUMERIC_CHARS}"', 'numbers 0-9'))
        else:
            raise message
    # has this 1 letters of a-z?
    try:
        has_target_chars(value, A_TO_Z_CHARS['lowercase'], 1)
    except ValidationError as e:
        has_except = True
        if is_message_null:
            messages.append(e.message.replace(f'"{value}"', 'the password').replace(f'"{A_TO_Z_CHARS['lowercase']}"', 'letters a-z lowercase'))
        else:
            raise message
    # has this 1 letters of A-Z?
    try:
        has_target_chars(value, A_TO_Z_CHARS['uppercase'], 1)
    except ValidationError as e:
        has_except = True
        if is_message_null:
            messages.append(e.message.replace(f'"{value}"', 'the password').replace(f'"{A_TO_Z_CHARS['uppercase']}"', 'letters A-Z uppercase'))
        else:
            raise message
    # has this 8 letters of a-zA-Z?
    try:
        has_target_chars(value, A_TO_Z_CHARS['lowercase'] + A_TO_Z_CHARS['uppercase'], 8)
    except ValidationError as e:
        has_except = True
        if is_message_null:
            messages.append(e.message.replace(f'"{value}"', 'the password').replace(f'"{A_TO_Z_CHARS['lowercase'] + A_TO_Z_CHARS['uppercase']}"', 'letters a-zA-Z'))
        else:
            raise message
    # has this 1 character of punctuations?
    try:
        has_target_chars(value, PUNCTUATION_CHARS, 1)
    except ValidationError as e:
        has_except = True
        if is_message_null:
            messages.append(e.message.replace(f'"{value}"', 'the password'))
        else:
            raise message
    if not has_except:
        return value
    raise ValidationError(messages)

def validate_password(value: str, message: str | None = None):
    if message is None:
        message = f'The password is not validate!\nPlease use at least 8 letters, including at least 1 uppercase letter and 1 lowercase letter. plus 3 digits of 0-9 and 1 character of {PUNCTUATION_CHARS} .'
    for c in value:
        if not c in VALIDATE_CHARS_FOR_PASSWORDS:
            raise ValidationError(message)
    return value
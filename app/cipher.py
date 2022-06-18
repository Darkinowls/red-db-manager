from consts import KEY, CODE

def encrypt(code: str, key: int = KEY) -> str:
    cipher = ''
    for char in code:
        if char == '-':
            cipher += char
        elif char.isupper():
            cipher = cipher + chr((ord(char) + key - 65) % 26 + 65)
        elif char.isnumeric():
            cipher = cipher + chr((ord(char) + key - 48) % 10 + 48)
        elif char.islower():
            cipher = cipher + chr((ord(char) + key - 97) % 26 + 97)
    return cipher


def decrypt(code: str, key: int = KEY) -> str:
    return encrypt(code, -key)


def is_key(code: str) -> bool:
    return True if decrypt(code) == CODE else False

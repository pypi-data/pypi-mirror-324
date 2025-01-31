from random import choices

def generate_salt():
    return ''.join(choices("".join(chr(i) for i in range(33, 127)), k = 16))

def hash(data: str, salt: str = None, encoding: str = 'ascii', size: int = 128, iterations: int = 10, prime: int = 936804092255346578758038127681):
    encoding = encoding.lower()
    CHARS = {
        'ascii': "".join(chr(i) for i in range(33, 127)),
        'unicode': "".join(chr(i) for i in range(33, 10000))
    }

    if not encoding in list(CHARS.keys()):
        raise AttributeError(f"The format \"{encoding}\" is not supported by Linex Hash function.")
    
    CHARS_STRING = CHARS[encoding]
    CHARS_LEN = len(CHARS_STRING)

    SALT = salt if salt else generate_salt()
    if len(SALT) != 16:
        raise AttributeError(f"The salt has to be 16 characters long.")
    data = f"{SALT}{data}"

    SIZE = size * 8
    PRIME = prime
    hash_value = PRIME

    for i in range(iterations):
        temp_data = data + str(i)
        for char in temp_data:
            hash_value ^= (hash_value << 5) + (hash_value >> 3) + ord(char) * PRIME
            hash_value &= (2 ** SIZE - 1)
        hash_value <<= SIZE * 2

    result = ""
    for _ in range(SIZE // 8):
        result += CHARS_STRING[hash_value % CHARS_LEN]
        hash_value //= CHARS_LEN

    str_iterations = str(iterations)
    while len(str_iterations) < 4:
        str_iterations = f'0{str_iterations}'

    return str_iterations + SALT + result

def verify(data: str, hashed: str, encoding: str = 'ascii', prime: int = 936804092255346578758038127681):
    try:
        iterations = int(hashed[:4])
        salt = hashed[4:20]
        correct_hash = hash(data, salt = salt, encoding = encoding, iterations = iterations, prime = prime)
        return correct_hash == hashed
    except:
        raise AttributeError("Hash is invalid!")
def encrypt(key: str, text: str) -> str:
    key_len = len(key)
    output = []

    for i, text_char in enumerate(text):
        key_char = ord(key[i % key_len])
        text_char_val = ord(text_char)
        encrypted_value = text_char_val + key_char
        output.append(format(encrypted_value % 256, '02x'))

    return ''.join(output)
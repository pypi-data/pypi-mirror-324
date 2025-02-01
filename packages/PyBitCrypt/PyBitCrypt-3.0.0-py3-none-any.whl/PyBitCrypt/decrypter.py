def decrypt(key: str, text: str) -> str:
    key_len = len(key)
    output = []

    for i in range(0, len(text), 2):
        hex_pair = text[i:i+2]
        byte = int(hex_pair, 16)
        key_char = ord(key[(i // 2) % key_len])
        decrypted_value = (byte - key_char) % 256
        output.append(chr(decrypted_value))

    return ''.join(output)


def text_to_binary(text):
    return ' '.join(format(ord(char), '08b') for char in text)

def binary_to_text(binary_string):
    binary_value = binary_string.split()
    return ' '.join(chr(int(b, 2)) for b in binary_value)

def decimal_to_binary(decimal):
    return bin(int(decimal))[2:]

def binary_to_decimal(binary):
    return str(int(binary, 2))


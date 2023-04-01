import os
import sys


# Generate the string of valid characters and keep it in a constant
def generate_chars():
    chars = ""
    for i in range(33, 127):
        chars += chr(i)
    return chars

CHARS = '!"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~'

def encode_whitespace(s):
    """Replace spaces and newlines with ` and \\"""
    # Save actual backquotes and backslashes as regular quote and slash
    if '`' in s or '\\' in s:
        print("Warning: input contains a backquote and/or backslash, replacing them with quote and slash.")
    s = s.replace('`', "'").replace('\\', '/')
    return '\\'.join(line.replace(" ", "`") for line in s.splitlines())


def decode_whitespace(s):
    return s.replace('`', ' ').replace('\\', '\n')


def repeat_key_for_content_length(key, n):
    """Repeat the key to be at least n characters long"""
    times = (n // len(key)) + 1
    return key * times


def encrypt(s, key):
    encrypted = ""
    repeated_key = repeat_key_for_content_length(key, len(s))
    for secret_c, key_c in zip(s, repeated_key):
        try:
            s_ord = CHARS.index(secret_c)
            k_ord = CHARS.index(key_c)
        except:
            print(f"One of {secret_c}, {key_c} not found in CHARS. Cannot encrypt.")
            print("Exiting.")
            raise RuntimeError("Cannot encode non-ASCII characters.")
        encrypted += CHARS[(s_ord + k_ord) % len(CHARS)]
    return encrypted


def decrypt(c, key):
    decrypted = ""
    repeated_key = repeat_key_for_content_length(key, len(c))
    for enc_c, key_c in zip(c, repeated_key):
        c_ord = CHARS.index(enc_c)
        k_ord = CHARS.index(key_c)
        dec_ord = c_ord - k_ord
        if dec_ord < 0:
            dec_ord += len(CHARS)
        decrypted += CHARS[dec_ord]
    return decrypted


if __name__ == "__main__":
    desc = """Usage:

    To encrypt (generates secret-enc.txt):
    python vigenere.py enc secret.txt

    To decrypt (generates secret.txt):
    python vigenere.py dec secret-enc.txt
    """

    if len(sys.argv) != 3:
        print(desc)

    command = sys.argv[1]

    filename = sys.argv[2]
    base, extension = filename.split(".")

    if command == 'enc':
        print("Encrypting...")
        key = input("Enter the key: ")
        key = encode_whitespace(key)
        with open(f"{base}-enc.{extension}", "w", encoding="utf-8") as file_out:
            hint = input("Enter a hint (optional): ")
            if hint:
                print(f"Hint: {hint}", file=file_out)
            with open(filename, encoding="utf-8") as file_in:
                secret = file_in.read()
                secret = encode_whitespace(secret)
                encrypted = encrypt(secret, key)
                print(encrypted, file=file_out)
    elif command == 'dec':
        print("Decrypting...")
        with open(filename, encoding="utf-8") as file_in, open(filename.replace("-enc", "-dec"), 'w') as file_out:
            for line in file_in:
                if line.startswith("Hint:"):
                    print(line)
                    continue
                key = input("Enter the key: ")
                key = encode_whitespace(key)
                line = line.strip()
                decrypted = decrypt(line, key)
                decrypted = decode_whitespace(decrypted)
                print(decrypted, file=file_out)
        print(f"Wrote {filename.replace('-enc', '-dec')}")
    else:
        print(f"Unknown command: {command}")

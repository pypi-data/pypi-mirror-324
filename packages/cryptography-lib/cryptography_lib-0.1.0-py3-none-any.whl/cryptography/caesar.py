from .alphabet import get_letter, get_index

def encrypt(plaintext, shift):
    ciphertext = ''
    for letter in plaintext:
        if letter.isalpha():
            index = get_index(letter)
            index += shift
            letter = get_letter(index)
        ciphertext += letter
    
    return ciphertext

def decrypt(ciphertext, shift):
    return encrypt(ciphertext, -shift)


if __name__ == '__main__':
    plaintext = 'HELLO WORLD'
    shift = 3
    print("Cipher Text: %s" % encrypt(plaintext, shift))

    ciphertext = 'KHOOR ZRUOG'
    shift = 3
    print("Plain Text: %s" % decrypt(ciphertext, shift))

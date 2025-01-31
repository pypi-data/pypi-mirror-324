ALPHABET='ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def get_letter(index : int) -> chr:
    size = len(ALPHABET)
    
    return ALPHABET[index % size]

def get_index(letter : chr) -> int:
    return ALPHABET.index(letter)

if __name__ == '__main__':
    print(get_letter(30))
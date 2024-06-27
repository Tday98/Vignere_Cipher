import re  # regular expression library to strip everything but letters from plaintext
import itertools # using this library to generate a Cartesian product of lower case letters.

def main():
    '''Main function that will make calls to encrypt(), decrypt(), brute()'''
    exit_case = 1
    while (exit_case):
        print("Welcome to the Vignere Cipher algorithm program.\n")
        print("What would you like to do? (Please type the number 1-5)"
              "\n\t1. encrypt\n\t2. decrypt\n\t3. char brute\n\tt4. exit")
        user_number = input("Enter number: ")
        while True:
            # User input validation
            try:
                user_number = int(user_number)
            except:
                user_number = input("Try again: ")
            else:
                if user_number < 1 or user_number > 5:
                    user_number = input("Must be between 1-5: ")
                else:
                    break

        match user_number:
            case 1:  # encrypt case
                print("\n\nBe aware any numbers or symbols will be removed and uppercase letters will be set to lowercase.\n")
                plaintext = input("Enter plaintext to be encrypted: ")
                key = input("Enter key to encrypt plaintext: ")
                key = sanitize(key)
                plaintext = sanitize(plaintext)
                encrypted = encrypt(key, plaintext)
                print(encrypted)
            case 2:  # decrypt case
                print("\n\nBe aware any numbers or symbols will be removed and uppercase letters will be set to lowercase.\n")
                ciphertext = input("Enter ciphertext to be decrypted: ")
                key = input("Enter key to decrypt ciphertext: ")
                key = sanitize(key)
                ciphertext = sanitize(ciphertext)
                decrypted = decrypt(key, ciphertext)
                print(decrypted)
            case 3:  # brute case
                print("\n\nBe aware any numbers or symbols will be removed and uppercase letters will be set to lowercase.\n")
                ciphertext = input("Enter a ciphertext to be brute force decrypted: ")
                while True:
                    keysize = input("Enter a keysize by integer value between 1 and 10: ")
                    try:
                        keysize = int(keysize)
                    except:
                        keysize = input("Only integer numbers please between 1 - 10: ")
                    else:
                        if keysize < 0 or keysize > 10:
                            user_number = input("Must be between 1-10: ")
                        else:
                            break
                substring = input("Enter a substring believed to be in the plaintext: ")
                ciphertext = sanitize(ciphertext)
                substring = sanitize(substring)
                plaintext = brute_force(ciphertext,substring,keysize)
                print(plaintext)
            case 4:
                exit(0)


def sanitize(plaintext):
    '''Sanitizes user input to only allow lowercase letters with no spaces.'''
    san_plaintext = re.sub('[^A-Za-z]+', '', plaintext)
    san_plaintext = san_plaintext.lower()
    return san_plaintext.replace(" ", "")


def encrypt(key, plaintext):
    counter = 0
    encrypted_text = ""
    key = generate_key(key, plaintext)
    for i in range(0, len(plaintext)):
        '''For loop goes through each letter adding them together. modulus used to bring it back around to the starting letter a'''
        x = ord(key[i]) - ord('a')
        y = ord(plaintext[i]) - ord('a')
        combine = (x + y) % 26
        encrypted_text += chr(combine + ord('a'))
    return encrypted_text


def decrypt(key, ciphertext):
    decrypted_text = ""
    key = generate_key(key, ciphertext)
    for i in range(0, len(ciphertext)):
        '''For loop goes through each letter subtracting the key from the ciphertext. modulus used to bring it back around to the ending letter z'''
        x = ord(key[i]) - ord('a')
        y = ord(ciphertext[i]) - ord('a')
        combine = (y - x) % 26
        decrypted_text += chr(combine + ord('a'))
    return decrypted_text

def brute_force(ciphertext, substring, keySize):
    '''
    Calls the itertools function to generate the keys as we try every possible option.
    :param ciphertext:
    :param substring:
    :param keySize:
    :return:
    '''
    for key in itertools_generate_key(keySize):
        decrypted = decrypt(key, ciphertext)
        if substring in decrypted:
            print(f"Possible key! {key}")
            print(f"Plaintext: {decrypted}")

def itertools_generate_key(keySize):
    '''This function is super useful. It generates keys of the up to the specified keysize following
    the format (a-z)(a-z)(a-z)... and so on iterating over and over. It runs in O(26^n)'''
    lowercaseLetters = "abcdefghijklmnopqrstuvwxyz"
    counter = 0
    # This will generate all my keys a-z aa-az etc. for the specified keySize. Thankfully this is a generator function so it shouldnt gobble ram.
    for length in range(1, keySize + 1):
        for key in itertools.product(lowercaseLetters, repeat=length):
            yield ''.join(key)
        counter += 1
        user_input = input(f"Current key size {counter} completed. Continue? (y/n) ")
        if user_input == "n":
            exit(0)
        else:
            continue

def generate_key(key, text):
    '''This function does the heavy lifting of creating a key of the same length as the plaintext.'''
    temp_key = key
    counter = 0
    for i in range(0, (len(text) - len(key))):
        key += temp_key[counter]
        counter += 1
        if counter >= len(temp_key):
            counter = 0
        if len(key) == len(text):
            return key

main()
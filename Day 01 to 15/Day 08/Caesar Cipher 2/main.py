alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

direction = input("Type 'encode' to encrypt, type 'decode' to decrypt:\n").lower()
text = input("Type your message:\n").lower()
shift = int(input("Type the shift number:\n"))


# TODO-1: Create a function called 'decrypt()' that takes 'original_text' and 'shift_amount' as inputs.
def decrypt(original_text, shift_amount):

# TODO-2: Inside the 'decrypt()' function, shift each letter of the 'original_text' *backwards* in the alphabet
    decrypt_text = ""
    for letter in original_text:
        shifted_position = alphabet.index(letter) - shift_amount
        decrypt_text += alphabet[(alphabet.index(letter) - shift_amount)]
    print(f"Here is the decoded result: {decrypt_text}")

#  by the shift amount and print the decrypted text.
# TODO-3: Combine the 'encrypt()' and 'decrypt()' functions into one function called 'caesar()'.
#  Use the value of the user chosen 'direction' variable to determine which functionality to use.

def caesar(original_text, shift_amount, direction):
    cipher_text = ""
    if direction == "decode":
        shift_amount = -shift_amount
    for letter in original_text:
        cipher_text += alphabet[(alphabet.index(letter) + shift_amount) % 26]
    print(f"Here is the {direction}d result: {cipher_text}")

caesar(original_text=text, shift_amount=shift, direction=direction)


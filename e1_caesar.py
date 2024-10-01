def decrypt(text, shift):
    decrypted_text = ""
    
    for char in text:
        if char.isupper():
            decrypted_text += chr((ord(char) - shift - 65) % 26 + 65)
        elif char.islower():
            decrypted_text += chr((ord(char) - shift - 97) % 26 + 97)
        elif char.isdigit():
            decrypted_text += chr((ord(char) - shift - 48) % 10 + 48)
        else:
            decrypted_text += char
    
    return decrypted_text

text = "IY8763{iG9y0X_7y_sE_l0b6aXoZ9_y0RgJ}"
shift = 6

decrypted = decrypt(text, shift)
print("Decrypted Text:", decrypted)

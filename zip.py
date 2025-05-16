import pyzipper

def test_pass(zip_obj, password):
    try:
        # Set the password
        zip_obj.setpassword(password.encode())  # Password must be in bytes
        print(f"Trying password: {password}")  # Debugging: Show the password being tested
        zip_obj.testzip()  # Try to test the zip file
        return password  # If no error, the password is correct
    except RuntimeError:
        # This will occur if the password is incorrect
        return None  # Return None if the password doesn't work
    except Exception as ex:
        # Catch other unexpected errors
        print(f"An error occurred while trying password '{password}': {ex}")
        return None

def main():
    try:
        # Open the zip file with pyzipper to handle AES encryption
        zip_obj = pyzipper.AESZipFile("good.zip")
        # Check if the zip file is password protected
        zip_obj.testzip()  # Test the integrity of the zip file
        print("[+] The zip file is password protected.")
    except FileNotFoundError:
        print("The zip file 'good.zip' was not found.")
        return
    except pyzipper.zipfile.BadZipFile:
        print("The file 'good.zip' is not a valid zip file.")
        return
    except RuntimeError as e:
        print("[!] The zip file is encrypted, password required for extraction.")
    
    # Open the dictionary file
    try:
        with open("dictionary.txt", "r") as filepass:
            for word in filepass.readlines():
                password = word.strip()  # Remove newline and extra spaces
                if len(password) < 6:  # Skip very short passwords (optional)
                    continue

                # Debugging: Print each password attempt
                print(f"Trying password from dictionary: '{password}'")
                guess_password = test_pass(zip_obj, password)
                if guess_password:
                    print(f"[+] Password found: {guess_password}")
                    return  # Exit if the password is found
    except FileNotFoundError:
        print("The dictionary file 'dictionary.txt' was not found.")
        return

    print("[-] No password found in the dictionary.")

if __name__ == '__main__':
    main()

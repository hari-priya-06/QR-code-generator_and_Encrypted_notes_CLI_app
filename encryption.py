from cryptography.fernet import Fernet
import os
from datetime import datetime
import getpass

KEY_FILE = 'secret.key'
NOTES_FILE = 'notes.enc'
NOTES_DIR = 'Encrypted_Notes'

# Utility to get all note files
def get_note_files():
    if not os.path.exists(NOTES_DIR):
        os.makedirs(NOTES_DIR)
    files = [f for f in os.listdir(NOTES_DIR) if f.endswith('.txt')]
    files.sort()
    return files

def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, 'wb') as key_file:
        key_file.write(key)
    return key

def load_key():
    if not os.path.exists(KEY_FILE):
        return generate_key()
    with open(KEY_FILE, 'rb') as key_file:
        return key_file.read()

def encrypt_note(note: str, key: bytes) -> bytes:
    f = Fernet(key)
    return f.encrypt(note.encode())

def decrypt_note(token: bytes, key: bytes) -> str:
    f = Fernet(key)
    return f.decrypt(token).decode()

def write_note():
    key = load_key()
    note = input('Enter your note: ')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    full_note = f'[{timestamp}] {note}'
    encrypted = encrypt_note(full_note, key)
    with open(NOTES_FILE, 'ab') as f:
        f.write(encrypted + b'\n')
    print('Note saved and encrypted!')

def decrypt_note_file(filename: str, password: str):
    key = generate_key_from_password(password)
    f = Fernet(key)
    path = os.path.join(NOTES_DIR, filename)
    with open(path, 'rb') as file:
        encrypted = file.read()
    try:
        note = f.decrypt(encrypted).decode('utf-8')
        print(f'\n\033[96m{note}\033[0m')
    except Exception:
        print('\033[91mInvalid password or corrupted note!\033[0m')

def generate_key_from_password(password: str) -> bytes:
    import base64
    key = password.encode('utf-8')[:32].ljust(32, b'0')
    return base64.urlsafe_b64encode(key)

def encrypt_and_save_note(note: str, password: str):
    # Ensure the notes directory exists
    if not os.path.exists(NOTES_DIR):
        os.makedirs(NOTES_DIR)
    key = generate_key_from_password(password)
    f = Fernet(key)
    encrypted = f.encrypt(note.encode('utf-8'))
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M')
    filename = f'note_{timestamp}.txt'
    with open(os.path.join(NOTES_DIR, filename), 'wb') as file:
        file.write(encrypted)
    print(f'\n\033[92mNote saved as {filename}!\033[0m')

def print_menu():
    print("\n================= \U0001F512 Welcome to SecurePad =================\n")
    print("[1] \U0001F4DD Write a New Encrypted Note")
    print("[2] \U0001F441 View a Encrypted Note")
    print("[3] \u274C Exit\n")

def main():
    while True:
        print_menu()
        choice = input('Select an option [1/2/3]: ').strip()
        if choice == '1':
            print('\n\033[1mWrite your note below. Press Enter when done.\033[0m')
            note = input('\nNote: ')
            password = getpass.getpass('Enter a password to encrypt this note: ')
            encrypt_and_save_note(note, password)
        elif choice == '2':
            files = get_note_files()
            if not files:
                print('\033[91mNo notes found!\033[0m')
                continue
            print('\nSelect a Note to View\n')
            print('No.  Filename')
            for idx, fname in enumerate(files, 1):
                print(f'{idx:<5}{fname}')
            try:
                num = int(input('\nEnter note number [1/{}]: '.format(len(files))))
                if not (1 <= num <= len(files)):
                    raise ValueError
            except ValueError:
                print('\033[91mInvalid selection!\033[0m')
                continue
            password = getpass.getpass('Enter the password to decrypt this note: ')
            decrypt_note_file(files[num-1], password)
        elif choice == '3':
            print('\033[91mGoodbye!\033[0m')
            break
        else:
            print('\033[91mInvalid option!\033[0m')

if __name__ == '__main__':
    main()

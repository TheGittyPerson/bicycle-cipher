# bicycle-cipher

This is a Python module for encrypting and decrypting Bicycle cipher messages.

This project is intended for educational (fun) purposes only.

## The Bicycle cipher

The Bicycle cipher is a simple, time-based cipher built on top of a [Caesar cipher](#caesar-cipher). It uses three steps to encrypt text:

**STEP 1:** The whole text is ciphered using a Caesar cipher with the current day of the month as the key (1~31).

**STEP 2:** Every odd alphabetical character is ciphered using the current month as the key (1~12) and every even alphabetical character using the current year as the key (e.g., 2025). **Non-alphabetical characters are ignored and not indexed.**

**STEP 3:** The text is reversed.

### Caesar cipher

"The Caesar cipher is one of the simplest and most widely known encryption techniques used in cryptography. It is a type of substitution cipher in which each letter in the plaintext is replaced by a letter some fixed number of positions along the alphabet. For example, with a left shift of 3, D would be replaced by A, E would become B, and so on. The method is named after Julius Caesar, who used it in his private correspondence."

(Extracted from Wikipedia: https://en.wikipedia.org/wiki/Caesar_cipher)
        
Example with a left shift of 3 (key=-3):
    'Hello, world!' → 'Ebiil, tloia!'
    'This is an English sentence.' → 'Qefp fp xk Bkdifpe pbkqbkzb.'

## Reference

The `bicycle` module contains **four public functions**:

### `bicycle.cipher`
Cipher plaintext with the Bicycle cipher and return the ciphertext.
#### Parameters
##### `plaintext` (str):
The plaintext to cipher

### `bicycle.decipher`
Decipher ciphertext encrypted with the Bicycle cipher and return the plaintext.
#### Parameters
##### `ciphertext` (str):
The ciphertext to decipher

### `bicycle.clockcipher`
Cipher plaintext with the Bicycle cipher with a specific date and return the ciphertext.
#### Parameters
##### `plaintext` (str):
The plaintext to cipher
##### `date` (int | tuple[int, int, int] | list[int] | datetime.date):
The date on which the encryption is based.
- If an int is provided, it represents the number of days offset from today.
- If a tuple or list is provided, it must be in the form (YYYY, MM, DD)/\[YYYY, MM, DD\].
- If a datetime.date object is provided, it is used directly.

### `bicycle.clock_decipher`
Decipher ciphertext encrypted with the Bicycle cipher with a specific date and return the plaintext.
#### Parameters
##### `plaintext` (str):
The ciphertext to decipher
##### `date` (int | tuple[int, int, int] | list[int] | datetime.date):
The date on which the ciphertext was originally encrypted with.
- If an int is provided, it represents the number of days offset from today.
- If a tuple or list is provided, it must be in the form (YYYY, MM, DD)/\[YYYY, MM, DD\].
- If a datetime.date object is provided, it is used directly.

## Example usage

Run `bicycle.py` directly to execute the example program.

```
import sys
import traceback
from time import sleep

from bicycle import *

if __name__ == "__main__":
    def print_encrypting(encr: bool) -> None:
        print(f"\n{'🔐' if encr else '🔓'}"
              f" ——————————————— {'ENCRYPTING' if encr else 'DECRYPTING'} ——————————————— "
              f"{'🔐' if encr else '🔓'}")


    def print_clockmode(clock: bool) -> None:
        print(f"\n🕓 ~~~~~~~~~~ CLOCK MODE {'ON' if clock else 'OFF'} ~~~~~~~~~~ 🕥")
        if clock:
            print("\nYou can now enter the date value the encryption/decryption will be based on.")
            print("Enter either the number of offset days from today (e.g. -1 = yesterday) "
                  "or the exact date in the form 'yyyy-mm-dd'")


    def end() -> None:
        print("\nBye!")
        sys.exit()

    try:
        print("\n\033[1m🚲💻💬 Bicycle cipher encrypter/decrypter! 💬💻🚲\033[0m")
        sleep(0.5)
        print("\nWelcome!")
        sleep(0.5)
        print(
            "\n* --------------------------------------- *\n"
            "ℹ️ HOW TO USE:\n"
            "- Enter the text to encrypt or decrypt with the Bicycle cipher.\n"
            "- Enter a forward slash ('/') at any time to switch between cipher/decipher.\n"
            "- Enter '*' at any time to toggle clock mode.\n"
            "- Enter 'q' at any time to quit.\n"
            "- TIP: Triple-click output text to easily select (and copy) the whole line.\n"  
            "* --------------------------------------- *"
        )

        encrypting = True
        clock_mode = False
        while True:
            print_encrypting(encrypting)

            while True:
                txt = input(f"\nEnter text to {'ENCRYPT' if encrypting else 'DECRYPT'}: ")
                output = None

                if txt.strip() == '/':
                    encrypting = not encrypting
                    break

                if txt.strip() == '*':
                    clock_mode = not clock_mode
                    print_clockmode(clock_mode)
                    continue

                if txt.strip() == 'q':
                    print("\nBye!")
                    sys.exit()

                if not txt.strip():  # handle empty (or whitespace) inputs
                    print("\nError: Please enter valid text")
                    sleep(0.5)
                    continue

                # -------------------- CLOCK MODE -------------------- #

                if clock_mode:
                    while True:
                        dt = input("\nEnter date to be used "
                                   "(Enter offset days from today or 'yyyy-mm-dd'): ").strip()
                        if dt == '/':
                            encrypting = not encrypting
                            print_encrypting(encrypting)
                            output = None
                            break

                        if dt == '*':
                            clock_mode = not clock_mode
                            print_clockmode(clock_mode)
                            output = None
                            break

                        if dt == 'q':
                            print("\nBye!")
                            sys.exit()

                        if dt.removeprefix("-").isnumeric():
                            dt = int(dt)
                            output = clock_cipher(txt, dt) if encrypting else clock_decipher(txt, dt)
                            break

                        # Dates must be in 3 parts, each an integer, separated by '-'
                        elif (
                            len(dt.split('-')) == 3
                            and all(value.isdigit() for value in dt.split('-'))
                        ):
                            dt = dt.split('-')
                            try:
                                dt = datetime.date(int(dt[0]), int(dt[1]), int(dt[2]))
                            except ValueError:
                                print("\nError: Please enter a valid integer or date")
                                sleep(0.5)
                                continue
                            output = clock_cipher(txt, dt) if encrypting else clock_decipher(txt, dt)
                            break

                        else:  # handle empty (or whitespace) inputs
                            print("\nError: Please enter a valid integer or date")
                            sleep(0.5)
                            continue

                else:
                    output = cipher(txt) if encrypting else decipher(txt)

                if output is not None:
                    print(f"\n{"Encrypted" if encrypting else "Decrypted"} text:")
                    print(output)

    except KeyboardInterrupt:
        print("\n*❖* —————————————————————————————— *❖*")
        print("User ended the program.")
        sys.exit()
    except Exception:
        print("\n*!* —————————————————————————————— *!*")
        print("❌ \033[1m\033[31mERROR!\033[0m")
        print(traceback.format_exc())
        sys.exit(1)
```

## Project structure
- `bicycle.py` — contains the Bicycle cipher encrypter/decrypter
- `caesar.py` – contains the Caesar cipher encrypter/decrypter, which is required and imported by `bicycle.py`

## License

This project is licensed under the MIT License.

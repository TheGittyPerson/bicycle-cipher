"""
A Bicycle cipher encrypter/decrypter.

The Bicycle cipher is a simple, time-based cipher built on top of a
Caesar cipher. It uses three steps to encrypt text:

STEP 1: Cipher the whole text using a Caesar cipher with the current
        day of the month as the key.
STEP 2: Cipher every odd alphabetical character using the current month
        as the key and every even alphabetical character using the
        current year as the key. Non-alphabetical characters are ignored
        and not indexed.
STEP 3: Reverse the text.

Note: this cipher is intended for fun purposes only.
"""

import string
import datetime
import traceback
from datetime import timedelta

import caesar


def cipher(plaintext: str) -> str:
    """Encrypt text using the Bicycle cipher.

    Args:
        plaintext (str): the text to be encrypted

    Returns:
        str: the encrypted ciphertext
    """

    if not isinstance(plaintext, str):
        raise TypeError("Parameter 'plaintext' must be str.")

    today = datetime.date.today()

    # Step 1: Cipher the whole text using the day of the month as the key.
    step1 = caesar.cipher(plaintext, today.day)

    # Step 2: Cipher every odd character using the month as the key
    # and every even character using the year as the key.
    # Non-alphabetical characters are not indexed.
    step2 = _alternating_cipher(step1, True, today.month, today.year)

    # Step 3: Reverse the text.
    step3 = step2[::-1]

    return step3


def decipher(ciphertext: str) -> str:
    """Decrypt text encrypted using the Bicycle cipher.

    Args:
        ciphertext (str): the ciphertext to be decrypted

    Returns:
        str: the decrypted plaintext
    """

    if not isinstance(ciphertext, str):
        raise TypeError("Parameter 'ciphertext' must be str.")

    today = datetime.date.today()

    # Step 1: Reverse the text
    step1 = ciphertext[::-1]

    # Step 2: Decipher every odd character using the current month as the key
    # and every even character using the current year as the key.
    # Non-alphabetical characters are ignored.
    step2 = _alternating_cipher(step1, False, today.month, today.year)

    # Step 3: Decipher whole text using the current day of the month as the key.
    step3 = caesar.decipher(step2, today.day)

    return step3


def clock_cipher(plaintext: str,
                 date: int | tuple[int, int, int] | list[int] | datetime.date) -> str:
    """Encrypt text using the Bicycle cipher with an explicitly provided date.

    The encryption keys (day, month, and year) are derived from the given
    date instead of the current system date, allowing deterministic
    encryption and decryption across different runs.

    Args:
        plaintext (str):
            The plaintext to be encrypted.
        date (int | tuple[int, int, int] | list[int] | datetime.date):
            The date on which the encryption is based.
            - If an int is provided, it represents the number of days
              offset from today.
            - If an iterable is provided, the first three values must be
              in the form (year, month, day).
            - If a datetime.date object is provided, it is used directly.

    Returns:
        str:
            The encrypted ciphertext.

    Raises:
        TypeError:
            If `date` is not an int, tuple, or datetime.date.
    """

    if not isinstance(plaintext, str):
        raise TypeError("Parameter 'plaintext' must be str.")

    if isinstance(date, int):
        d = datetime.date.today() + timedelta(date)
    elif isinstance(date, (tuple, list)):
        y, m, d = date
        d = datetime.date(y, m, d)
    elif isinstance(date, datetime.date):
        d = date
    else:
        raise TypeError("Invalid date type")

    step1 = caesar.cipher(plaintext, d.day)
    step2 = _alternating_cipher(step1, True, d.month, d.year)
    step3 = step2[::-1]

    return step3


def clock_decipher(ciphertext: str,
                   date: int | tuple[int, int, int] | list[int] | datetime.date) -> str:
    """Decrypt text encrypted using the Bicycle cipher with a specific date.

    The same date used during encryption must be provided in order for
    decryption to succeed. The function reverses the character-wise
    Caesar shifts and text reversal applied during encryption.

    Args:
        ciphertext (str):
            The ciphertext to be decrypted.
        date (int | tuple[int, int, int] | list[int] | datetime.date):
            The date on which the ciphertext was originally encrypted.
            - If an int is provided, it represents the number of days
              offset from today.
            - If a tuple is provided, it must be in the form (year, month, day).
            - If a datetime.date object is provided, it is used directly.

    Returns:
        str:
            The decrypted plaintext.

    Raises:
        TypeError:
            If `date` is not an int, tuple[int, int, int], list[int],
            or datetime.date.
       """

    if not isinstance(ciphertext, str):
        raise TypeError("Parameter 'ciphertext' must be str.")

    if isinstance(date, int):
        d = datetime.date.today() + timedelta(date)
    elif isinstance(date, (tuple, list)):
        y, m, d = date
        d = datetime.date(y, m, d)
    elif isinstance(date, datetime.date):
        d = date
    else:
        raise TypeError("Invalid date type")

    step1 = ciphertext[::-1]
    step2 = _alternating_cipher(step1, False, d.month, d.year)
    step3 = caesar.decipher(step2, d.day)

    return step3


def _alternating_cipher(step1: str, encrypt: bool, m: int, y: int) -> str:
    """Ciphers or deciphers each odd alphabetic character using the given month
    as key and each even non-alphabetic character using the given year as key.
    """
    chars = []
    letter_index = 0

    for char in step1:
        if char.lower() in string.ascii_lowercase:
            if letter_index % 2 == 1:
                chars.append(caesar.cipher(char, m) if encrypt else caesar.decipher(char, m))
            else:
                chars.append(caesar.cipher(char, y) if encrypt else caesar.decipher(char, y))
            letter_index += 1
        else:
            chars.append(char)

    return "".join(chars)


if __name__ == "__main__":
    import sys
    from time import sleep


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
            "- TIP: Triple click output text to easily select (and copy) the whole line.\n"  
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

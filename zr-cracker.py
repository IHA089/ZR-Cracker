import os
import sys
import secrets
import string
import time
import argparse
import itertools
try:
    import pyzipper
except ImportError:
    print("`pyzipper` not insatlled, please install it")
    sys.exit()
try:
    import rarfile
except ImportError:
    print("`rarfile` not insatlled, please install it")
    sys.exit()

def home_logo():
    print("""
        ####   ##     ##      ###        #####      #######     ####### 
         ##    ##     ##     ## ##      ##   ##    ##     ##   ##     ##
         ##    ##     ##    ##   ##    ##     ##   ##     ##   ##     ##
         ##    #########   ##     ##   ##     ##    #######     ########
         ##    ##     ##   #########   ##     ##   ##     ##          ##
         ##    ##     ##   ##     ##    ##   ##    ##     ##   ##     ##
        ####   ##     ##   ##     ##     #####      #######     #######
    
IHA089: Navigating the Digital Realm with Code and Security - Where Programming Insights Meet Cyber Vigilance.
    """)


def update_terminal_lines(total_tries,  current_try, elapsed_time):
    print("===============================================")
    elapsed_time_line = f"Total time taken ::: {elapsed_time:.2f} seconds"
    total_tries_line = f"Total password tries ::: {total_tries}"
    current_try_line = f"Current Try ::: {current_try}"
    print(elapsed_time_line)
    print(total_tries_line)
    print(current_try_line)
    print("===============================================")
    print("\033[F\033[F\033[F\033[F\033[F", end="")
    print(end="", flush=True)

def check_zip_password(a, zip_path, password, start_time):
    try:
        with pyzipper.AESZipFile(zip_path, 'r') as zf:
            _ = zf.read(zf.namelist()[0], pwd=password.encode('utf-8'))
        total_time = time.time()-start_time
        password = password+"                  "
        print("===============================================")
        print(f"Total time taken ::: {total_time:.2f} seconds")
        print("Total password tries ::: {}".format(a))
        print("Password Found ::: {}".format(password))
        print("===============================================")
        return False
    except RuntimeError:
        end_time = time.time()
        time_taken = end_time-start_time
        update_terminal_lines(a, password, time_taken)
        return True
    except:
        time.sleep(4)

def check_rar_password(a, rar_path, password, start_time):
    with rarfile.RarFile(rar_path) as rf:
        try:
            rf.testrar(pwd=password.encode('utf-8'))
            total_time = time.time()-start_time
            password = password+"              "
            print("===============================================")
            print(f"Total time taken ::: {total_time:.2f} seconds")
            print("Total password tries ::: {}".format(a))
            print("Password Found ::: {}".format(password))
            print("===============================================")
            return False
        except rarfile.BadRarFile:
            end_time = time.time()
            time_taken = end_time-start_time
            update_terminal_lines(a, password, time_taken)
            return True
        except:
            time.sleep(4)

def Brute_Force_Attack(file_path, charset, max_length):
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} does not exist.")
        return

    file_ext = os.path.splitext(file_path)[1].lower()
    flag=True
    i=1

    if file_ext == ".zip":
        try:
            start_time = time.time()
            for length in range(1, max_length+1):
                for combo in itertools.product(charset, repeat=length):
                    password = ''.join(combo)
                    flag = check_zip_password(i, file_path, password, start_time)
                    i = i+1
                    if flag == False:
                        return 0
        except KeyboardInterrupt:
            print("\n\n\n\n\nExit by user....")
            return 1
    elif file_ext == ".rar":
        try:
            start_time = time.time()
            for length in range(1, max_length+1):
                for combo in itertools.product(charset, repeat=length):
                    password = ''.join(combo)
                    flag = check_rar_password(i, file_path, gen_pass, start_time)
                    i=i+1
                    if flag == False:
                        return 0
        except KeyboardInterrupt:
            print("\n\n\n\n\n\nExit by user....")
            return 1
    else:
        print(f"Error: Unsupported file format {file_ext}")
        return 

def Dictonary_Attack(file_path, wordlist_path):
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} does not exist.")
        return
    if not os.path.exists(wordlist_path):
        print(f"Error: Wordlist {wordlist_path} does not exist.")
        return

    file_ext = os.path.splitext(file_path)[1].lower()

    with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as passwords:
        i=0
        j=0

        if file_ext == ".zip":
            try:
                start_time = time.time()
                for password in passwords:
                    password = password.strip()
                    flag = check_zip_password(j, file_path, password, start_time)
                    j = j+1

                    if flag == False:
                        return
            except KeyboardInterrupt:
                print("Exit by user...")
                return
        elif file_ext == ".rar":
            try:
                start_time = time.time()
                for password in passwords:
                    password = password.strip()
                    flag = check_rar_password(j, file_path, password, start_time)
                    j=j+1
                    if flag == False:
                        return
            except KeyboardInterrupt:
                print("Exit by user...")
                return        
        
        if i==0:
            print("Password not found in wordlist...")
            return

def main():
    parser = argparse.ArgumentParser(
        description="zr-cracker: A tool for cracking zip/rar archives.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python3 zr_cracker.py --file locked.zip --bruteforce "
            "--charset abcdefghijklmnopqrstuvwxyz --max-length 4\n"
            "  python3 zr_cracker.py --file secret.rar --dictionary --wordlist rockyou.txt"
        )
    )

    parser.add_argument(
        "--file",
        type=str,
        help="Path to the zip/rar file to crack",
        required=True
    )
    parser.add_argument(
        "--bruteforce",
        action="store_true",
        help="Use brute-force cracking mode"
    )
    parser.add_argument(
        "--dictionary",
        action="store_true",
        help="Use dictionary-based cracking mode"
    )
    parser.add_argument(
        "--charset",
        type=str,
        help="Characters to use for brute-force (e.g., abcdefghijklmnopqrstuvwxyz)"
    )
    parser.add_argument(
        "--max-length",
        type=int,
        help="Maximum password length for brute-force"
    )
    parser.add_argument(
        "--wordlist",
        type=str,
        help="Path to the wordlist file for dictionary cracking"
    )

    args = parser.parse_args()

    if args.bruteforce and args.dictionary:
        parser.error("Cannot use both --bruteforce and --dictionary modes simultaneously.")
    if not args.bruteforce and not args.dictionary:
        parser.error("Must specify either --bruteforce or --dictionary mode.")
    if args.bruteforce and (not args.charset or not args.max_length):
        parser.error("--bruteforce requires --charset and --max-length.")
    if args.dictionary and not args.wordlist:
        parser.error("--dictionary requires --wordlist.")

    if args.bruteforce:
        Brute_Force_Attack(args.file, args.charset, args.max_length)
    elif args.dictionary:
        Dictonary_Attack(args.file, args.wordlist)

if __name__ == "__main__":
    home_logo()
    main()

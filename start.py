import os
import sys
import secrets
import string
import time
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

def Generate_Random_Password():
    length = secrets.choice(range(4, 11))  
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password

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

def Brute_Force_Attack(ftype, compressed_file_path):
    flag=True
    i=1
    try:
        start_time = time.time()
        while flag:
            gen_pass = Generate_Random_Password()
            if ftype == "zip":
                flag = check_zip_password(i, compressed_file_path, gen_pass, start_time)
            elif ftype == "rar":
                flag = check_rar_password(i, compressed_file_path, gen_pass, start_time)
            i=i+1
    except KeyboardInterrupt:
        print("\n\n\n\n\n\nExit by user....")
        sys.exit()

def Dictonary_Attack(ftype, compressed_file_path, passwod_list_path):
    file = open(passwod_list_path, 'r')
    passwords = file.readlines()
    file.close()

    i=0
    j=0
    try:
        start_time = time.time()
        for password in passwords:
            password = password.replace("\n", "")
            if ftype == "zip":
                flag = check_zip_password(j, compressed_file_path, password, start_time)
            elif ftype == "rar":
                flag = check_rar_password(j, compressed_file_path, password, start_time)
            j=j+1
            if flag == False:
                i=1
                break
    except KeyboardInterrupt:
        print("Exit by user...")
        sys.exit()
        
    if i==0:
        print("Password not found in wordlist...")
        sys.exit()


if __name__ == "__main__":
    home_logo()
    print("\n\nZIP & RAR file password cracker\n")
    try:
        compressed_file_name = input("Enter file name :")
    except KeyboardInterrupt:
        print("Exit by user...")
        sys.exit()
    pwd = os.getcwd()
    compressed_file_path = pwd+"/"+compressed_file_name

    if not os.path.isfile(compressed_file_path):
        print("File `{}` not found, please provide correct path".format(compressed_file_name))
        print("Exiting....")
        sys.exit()
    else:  
        ff = compressed_file_name.split(".")
        if ff[1] == "rar":
            compressed_file_path = pwd+"/"+compressed_file_name
        elif ff[1] == "zip":
            compressed_file_path = pwd+"/"+compressed_file_name
        else:
            print("This file not support...")
            sys.exit()

        print("1\tBrute Force Attack\n2\tDictionary Attack")
        try:
            select = int(input("Select ::: "))
        except KeyboardInterrupt:
            print("Exit by user...")
            sys.exit()
        if select == 1:
            if ff[1] == "zip":
                Brute_Force_Attack("zip", compressed_file_path)
            if ff[1] == "rar":
                Brute_Force_Attack("rar", compressed_file_path)
        elif select == 2:
            try:
                pass_file = input("Enter wordlist(full path) :")
            except KeyboardInterrupt:
                print("Exit by user...")
                sys.exit()
            if ff[1] == "zip":
                Dictonary_Attack("zip", compressed_file_path, pass_file)
            if ff[1] == "rar":
                Dictonary_Attack("rar", compressed_file_path, pass_file)            
        else:
            print("Please selct `1` or `2`")

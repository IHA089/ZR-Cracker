import os
import sys

def runner_create():
    file = open("/usr/local/bin/zrcracker",'w')
    file.write("#!/bin/bash")
    file.write("\n")
    file.write("python3 /usr/share/ihaahi/ZR-Cracker/start.py")
    file.close()
    os.system("chmod +x /usr/local/bin/zrcracker")
    print("type `zrcracker` to start this script\n")

def check_dependencies():
    try:
        import pyzipper
    except ImportError:
        print("pyzipper library not install")
        print("Installing pyzipper...")
        os.system("pip install pyzipper")

    try:
        import rarfile
    except ImportError:
        print("rarfile library not install")
        print("Installing rarfile...")
        os.system("pip install rarfile")

def iha089_dir():
    dir_path = "/usr/share/ihaahi"
    if not os.path.exists(dir_path) and os.path.isdir(dir_path):
        os.mkdir("/usr/share/ihaahi")

def check_root():
    return os.geteuid() == 0

def get_working_dir():
    return os.getcwd()

def main():
    check_dependencies()
    if sys.platform.startswith("linux"):
        if check_root():
            iha089_dir()
            pwd = get_working_dir()
            cmd = "cp -r {} /usr/share/ihaahi".format(pwd)
            os.system(cmd)
            runner_create()
        else:
            print("Please run with root permission\n")
    elif sys.platform.startswith("win"):
        print("type `python start.py` here")
    else:
        print("Your os not support\n")

if __name__=="__main__":
    main()

import os
import sys

def runner_create(os_type):
    if os_type == "linux":
        f_path = "/usr/local/bin/zrcracker"
    elif os_type == "termux":
        f_path = "/data/data/com.termux/usr/local/bin/zrcracker"

    file = open(f_path,'w')
    file.write("#!/bin/bash")
    file.write("\n")
    file.write("python3 /usr/share/ihaahi/ZR-Cracker/start.py")
    file.close()
    os.system("chmod +x {}".format(f_path))
    print("type `zrcracker` to start this script\n")

def check_os():
    if 'aarch64' in os.uname().machine.lower():
        return "termux"
    elif 'linux' in sys.platform.lower():
        return "linux"
    elif 'win' in sys.platform.lower():
        return "window"

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

def check_termux_runner():
    bash_path = "/data/data/com.termux/files/home/.bashrc_profile"
    f_open = open(bash_path, 'a')
    f.write("export PATH=$PATH:/data/data/com.termux/files/usr/local/bin")
    f.close()


def iha089_dir(os_type):
    if os_type == "linux":
        dir_path = "/usr/share/ihaahi"
        if not os.path.exists(dir_path) and os.path.isdir(dir_path):
            os.mkdir("/usr/share/ihaahi")
    elif os_type == "termux":
        dir_path = "/data/data/com.termux/usr/share/ihaahi"
        if not os.path.exists(dir_path) and os.path.isdir(dir_path):
            os.mkdir("/data/data/com.termux/usr/share/ihaahi")

        dir_path = "/data/data/com.termux/usr/local"
        if not os.path.exists(dir_path) and os.path.isdir(dir_path):
            os.mkdir("/data/data/com.termux/usr/local")
        
        dir_path = "/data/data/com.termux/usr/local/bin"
        if not os.path.exists(dir_path) and os.path.isdir(dir_path):
            os.mkdir("/data/data/com.termux/usr/local/bin")
        


def check_root():
    return os.geteuid() == 0

def get_working_dir():
    return os.getcwd()

def main():
    check_dependencies()
    if check_os() == "linux":
        if check_root():
            iha089_dir(check_os())
            pwd = get_working_dir()
            cmd = "cp -r {} /usr/share/ihaahi".format(pwd)
            os.system(cmd)
            runner_create(check_os())
        else:
            print("Please run with root permission\n")
    elif check_os() == "termux":
        iha089_dir(check_os())
        check_termux_runner()
        pwd = get_working_dir()
        cmd = "cp -r {} /data/data/com.termux/usr/share/ihaahi".format(pwd)
        os.system(cmd)
        runner_create(check_os())

    elif check_os() == "window":
        print("type `python start.py` here")
    else:
        print("Your os not support\n")

if __name__=="__main__":
    main()

import os
from shutil import copy2,SameFileError,rmtree
import hashlib
import argparse
from time import sleep,strftime,localtime

def msg_to_log(msg):
    curr_time = strftime('%Y-%m-%d %H:%M:%S',localtime())
    try:
        with open(args.log, 'a') as l:
            l.write(curr_time+msg+"\n")
    except:
        os.makedirs(args.log)
        with open(args.log, "w") as l:
            l.write(curr_time+msg+'\n')

def check_file_hash(file1,file2):
    bin_file1 = open(file1,'rb')
    bin_file2 = open(file2,'rb')
    if hashlib.md5(bin_file1.read()).hexdigest() == hashlib.md5(bin_file2.read()).hexdigest():
        bin_file1.close()
        bin_file2.close()
        return True
    else:
        bin_file1.close()
        bin_file2.close()
        return False

def check_file_tree(src,dest,log):
    if os.path.isdir(src):
        if not os.path.isdir(dest):
            os.makedirs(dest)
            msg_to_log(": Created folder "+dest+".")
            print("Created folder "+dest+".")
        else:
            msg_to_log(": Folder "+dest+" exists.")
            print("Folder "+dest+" exists.")
            
        subfolder_files = os.listdir(src)
        for file in subfolder_files:
            new_src = os.path.join(src,file)
            new_dest = os.path.join(dest,file)
            check_file_tree(new_src,new_dest,log)    
        
        subfolder_files = os.listdir(dest)
        for file in subfolder_files:
            new_src = os.path.join(src,file)
            if not os.path.exists(new_src):
                new_dest = os.path.join(dest,file)
                if os.path.isdir(new_dest):
                    rmtree(new_dest)
                    msg_to_log(": Deleted folder "+new_dest+".")
                    print("Deleted folder "+new_dest+".")
                else:
                    os.remove(new_dest)
                    msg_to_log(": Deleted file "+new_dest+".")
                    print("Deleted file "+new_dest)

    else:
        if os.path.isfile(dest):
            if os.path.isfile(src):
                if check_file_hash(src,dest):
                    msg_to_log(": "+dest+" is up to date.")
                    print(dest+' is up to date.')
                else:
                    try:
                        copy2(src,dest)
                        msg_to_log(": Updated "+dest+".")
                        print("Updated "+dest+".")
                    except SameFileError:
                        src.replace(dest)
                        msg_to_log(": Updated "+dest+".")
                        print("Updated "+dest+".")
            else:
                os.remove(dest)
                msg_to_log(": Removed "+dest+".")
                print("Removed "+dest+".")
        else:
            copy2(src,dest)
            msg_to_log(": Created "+dest+".")
            print("Created "+dest+".")

parser = argparse.ArgumentParser()

parser.add_argument("-s","--src",help="Source folder",default=os.getcwd()+'\\src')
parser.add_argument("-d","--dest",help="Destination folder",default=os.getcwd()+'\\dest')
parser.add_argument("-t","--time",help="Time between synchronizations(sec)",default=60)
parser.add_argument("-l","--log",help="Log file",default=os.getcwd()+'\\LOG.txt')

args = parser.parse_args()
#current_folder = os.getcwd()
#current_folder+'\\Folder-Sync\\src'
#current_folder+'\\Folder-Sync\\dest'
if not os.path.exists(args.src):
    os.makedirs(args.src)
src_path = args.src     
if not os.path.exists(args.dest):
    os.makedirs(args.dest)
dest_path = args.dest   
delay_time = float(args.time)
log_path = args.log

src_files = os.listdir(src_path)
dest_files = os.listdir(dest_path)
while True:   
    check_file_tree(src_path,dest_path,log_path)
    sleep(delay_time)

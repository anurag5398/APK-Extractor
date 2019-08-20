PATH = r"C:\Users\Anurag S\Documents"

import os
import time
import subprocess
import shutil
from zipfile import ZipFile
import glob



#########################
print("###|||###########|||#########|||||###################||||||#################\t")
print("####|||#########|||########||||##|||#################|||##|||###############\t")
print("#####|||#####|||#################|||#####|||||||#####|||####||##############\t")
print("######|||##|||#################|||###################|||####||##############\t")
print("#######||#||#################|||#####################|||##|||###############\t")
print("########||#################|||||||||||###############||||||#################\t")
#########################

print("\nPlease select your Os:\n")
print("1) Windows\t")
print("2) Linux\n")
os_val = input("Enter Choice: ")
if(os_val=="1"):
    separator = "\\"
if(os_val=="2"):
    separator = "/"

cont = 1
def full_adb():
    global cont
    # checking for connected devices
    print("\n###########################\t")
    device = os.popen("adb devices").read().split('\n', 1)[1].split("device")[0].strip()
    print("# Connected device ID is: ")
    device_name = device
    print("#",device,"               ")
    print("###########################")
    print("\n1) Correct Device\t")
    print("2) Incorrect Device\t")
    print("3) Exit\t")
    val = input("Enter Choice: ")
    if(val=="1"):
        print("\n1) View list of all Packages\t")
        print("2) View list of Honeywell Packages\t")
        print("3) Download all APKs\t")
        print("4) Download Honeywell APKs\t")
        print("5) Exit\t")
        val2 = input("Enter Choice: ")
        #b is package name list
        if(val2=="1"):
            print("\n")
            b = []
            packages = subprocess.check_output(["adb","shell","pm","list","packages"]).decode("utf-8")
            b = packages.split("\n")

            for nump in range(len(b)-1):
                print(b[nump])
            print("Total Apks are ", len(b)-1)
            print("Mission Accomplished")

        elif(val2=="3"):
            failed_download_list = []
            b = []
            print("\n")
            directory_create = PATH + separator + device_name
            if(os.path.isdir(directory_create)==True):
                shutil.rmtree(directory_create)
            subprocess.check_output(["mkdir",directory_create],shell=True)

            packages = subprocess.check_output(["adb","shell","pm","list","packages"]).decode("utf-8")
            b = packages.split("\n")#packge name with \r and package:
            for nump in range(len(b)-1):
                pname = b[nump].replace("package:","")
                pname = pname.replace("\r","")
                apkpath = subprocess.check_output(["adb","shell","pm","path",pname]).decode("utf-8")
                temp_path = apkpath.split("\n")

                current_path = temp_path[0].replace("package:","")
                current_path = current_path.replace("\r","")

                dest_path = PATH + separator + device_name + separator + pname + ".apk"
                try:
                    dwnld = subprocess.check_output(["adb","pull",current_path,dest_path],shell=True)
                    print(dwnld.decode("utf-8"))
                except:
                    failed_download_list.append(pname)
        
            zipname = PATH + separator + device_name + ".zip"
            if(os.path.isfile(zipname)==True):
                zipname = PATH + separator + device_name + "_v2.zip"
            zipObj = ZipFile(zipname, 'w')
            glob_temp = directory_create + separator + "*.apk"
            apksinfolder = glob.glob(glob_temp)
            for eachapk in apksinfolder:
                zipObj.write(eachapk)
            zipObj.close()
            print("Total aPKS in zip are ", len(apksinfolder))
            shutil.rmtree(directory_create)
            print("\nFAILED to Download APKs are (permission denied):\t")
            if(failed_download_list==[]):
                print("NONE\n")
            else:
                for e in failed_download_list:
                    print(e)
            print("Mission Accomplished")

        elif(val2=="2"):
            b = []
            hon_b = []
            print("\n")
            packages = subprocess.check_output(["adb","shell","pm","list","packages"]).decode("utf-8")
            b = packages.split("\n")

            for nump in range(len(b)-1):
                if(b[nump].find("honeywell")!= -1):
                    hon_b.append(b[nump])
                #lot of FalsePositives for Keyweord:hon
                #if(b[nump].find("hon")!= -1):
                #    hon_b.append(b[nump])
            if(hon_b!=[]):
                for eachh in hon_b:
                    print(eachh)
                print("Total Apks are ", len(hon_b))
            else:
                print("No Honeywell Apps are found on the device :(")
            print("Mission Accomplished")

        elif(val2=="4"):
            failed_download_list = []
            b = []
            bb = []
            print("\n")
            directory_create = PATH + separator + device_name
            if(os.path.isdir(directory_create)==True):
                shutil.rmtree(directory_create)
            subprocess.check_output(["mkdir",directory_create],shell=True)

            packages = subprocess.check_output(["adb","shell","pm","list","packages"]).decode("utf-8")
            b = packages.split("\n")#packge name with \r and package:
            for eachb in b:
                if(eachb.find("honeywell")!=-1):
                    bb.append(eachb)

            for nump in range(len(bb)):
                pname = bb[nump].replace("package:","")
                pname = pname.replace("\r","")
                apkpath = subprocess.check_output(["adb","shell","pm","path",pname]).decode("utf-8")
                temp_path = apkpath.split("\n")

                current_path = temp_path[0].replace("package:","")
                current_path = current_path.replace("\r","")

                dest_path = PATH + separator + device_name + separator + pname + ".apk"
                try:
                    dwnld = subprocess.check_output(["adb","pull",current_path,dest_path],shell=True)
                    print(dwnld.decode("utf-8"))
                except:
                    failed_download_list.append(pname)
        
            zipname = PATH + separator + device_name + "_hon.zip"
            if(os.path.isfile(zipname)==True):
                zipname = PATH + separator + device_name + "_v2_hon.zip"
            zipObj = ZipFile(zipname, 'w')
            glob_temp = directory_create + separator + "*.apk"
            apksinfolder = glob.glob(glob_temp)
            for eachapk in apksinfolder:
                zipObj.write(eachapk)
            zipObj.close()
            print("Total aPKS in zip are ", len(apksinfolder))
            shutil.rmtree(directory_create)
            print("\nFAILED to Download APKs are (permission denied):\t")
            if(failed_download_list==[]):
                print("NONE\n")
            else:
                for e in failed_download_list:
                    print(e)
            print("Mission Accomplished")

        elif(val2=="5"):
            cont = 0
            print("\nTerminated\n")
        else:
            print("\nDid you press the wrong key bi-mistake.\t")
            print("\n")

    elif(val=="2"):
        print("\nTry to reconnect device.\t")
        print("Note: Keep only one Android device conncted at a time.\t")
    
    elif(val=="3"):
        cont = 0
        print("\nTerminated\n")

    else:
        print("\nDid you press the wrong key bi-mistake.\t")
        print("\n")

while(cont==1):
    full_adb()
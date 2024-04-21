import os
import shutil
import requests
from bs4 import BeautifulSoup
import time
from pathlib import Path
from tqdm import tqdm,trange
import sys
import keyboard

file_types = {
    ".txt": "Text",
    ".docx": "Word",
    ".xlsx": "Excel",
    ".pdf": "PDF",
    ".html": "Webpage.html",
    ".js": "JavaScript",
    ".css": "Stylesheet",
    ".py": "Python Script",
    ".java": "Java Source Code",
    ".c": "C Source Code",
    ".cpp": "C++ Source Code",
    ".rb": "Ruby Script",
    ".php": "PHP Script",
    ".pl": "Perl Script",
    ".swift": "Swift Source Code",
    ".go": "Go Source Code",
    ".kt": "Kotlin Source Code",
    ".ts": "TypeScript",
    ".json": "JSON Data",
    ".xml": "XML Document",
    ".sql": "SQL Database",
    ".md": "Markdown Document",
    ".log": "Log File",
    ".bat": "Batch Script",
    ".ps1": "PowerShell Script",
    ".sh": "Shell Script",
    ".csv": "CSV File",
    ".tsv": "TSV File",
    ".yaml": "YAML Document",
    ".ini": "INI Configuration",
    ".rtf": "Rich Text Format",
    ".tex": "LaTeX Document",
    ".aspx": "ASP.NET Page",
    ".jar": "Java Archive",
    ".lnk": "Windows Shortcut",
    ".out": "Unix Executable",
    ".bin": "Binary Data",
    ".mp3": "MP3 Audio",
    ".mp4": "MP4 Video",
    ".jpg": "JPEG Image",
    ".png": "PNG Image",
    ".gif": "GIF Image",
    ".bmp": "Bitmap Image",
    ".wav": "WAV Audio",
    ".avi": "AVI Video",
    ".svg": "SVG Image",
    ".doc": "Legacy Word Document",
    ".xls": "Legacy Excel",
    ".ppt": "Legacy PowerPoint",
    ".odt": "OpenDocument Text",
    ".ods": "OpenDocument Spreadsheet",
    ".odp": "OpenDocument Presentation",
}

file_types_set = set(file_types.keys())

def countFiles(dir):
    count = 0
    for item in os.listdir(dir):
        item_path = os.path.join(dir, item)
        if os.path.isfile(item_path):
            count += 1
    return count

def create_move(folder_name,dir,f,x):
    newpath = os.path.join(dir,folder_name)
    #print("NewPath1000: ",newpath)
    #if not os.path.exists(newpath):
    isExist = os.path.exists(newpath)
    if not isExist:
        try: 
            os.mkdir(newpath) 
        except OSError as error: 
            print(error)       
    else:       
        #print("NewPath",newpath)
        shutil.move(f,newpath)
        namefinal = os.path.join(newpath,x)
        if os.path.exists(namefinal):
            #print("Move Successful \nPAth: ",namefinal)
            pass

def identify_file(ftype):
    search_url = f'https://fileinfo.com/extension/{ftype[1:]}'

    try:
        response = requests.get(search_url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            descript = soup.find('div', {'class': 'entryHeader'}).get_text()
            web_extract = descript.strip()
            file_name = web_extract.split("Developer")
            return file_name[0].strip()
    except requests.exceptions.RequestException:
        print("Request Error")
        pass
    
    return "Unknown"

def printDot(reps,delay):
    for i in range(0,reps):
        time.sleep(delay)
        print(".",end = ' ',flush = True) 
    time.sleep(delay)   

def olderExe(fname,ftype,f,x):
    #print("Check 1 older exe",f,"\n>>>>>>>>>>>>>>>>>>>>",x)
    current_time = time.time()
    folder_name = identify_file(ftype)
    exePath = os.path.join(dir,folder_name)
    modification_time = os.path.getmtime(os.path.join(exePath,x))
    #print(fname)
    file_life = current_time - modification_time
    if file_life > 15*24*60*60:
        #print("Check 2 older exe")
        print("ExePath: ",exePath)
        trash_folder = "OLD FILES"
        create_move(trash_folder,exePath,os.path.join(exePath,x),x)
        #print("Check 3 older exe")            

def sort(dir):
    total_files = countFiles(dir)
    print("Total Files: ",total_files)

    if total_files == 0:
        print("No file to sort.\nProcess Ended")
        #progress_bar.close()
    else:
        progress_bar = tqdm(total = total_files, unit = "file",desc="Sorting")
        for x in os.listdir(dir):
            f = os.path.join(dir,x)
            #print("CurrentFilePath",f)
            if os.path.isfile(f):
                fname , ftype = os.path.splitext(f)
                #print(fname,"    ",ftype)
                #print("CurrentFilePath",f,"    ","FileName",fname,"     ","Ftype",ftype)
                if ftype in file_types_set:   
                    folder_name = file_types[ftype]
                    create_move(folder_name,dir,f,x)
                else:
                    folder_name = identify_file(ftype)
                    create_move(folder_name,dir,f,x)
                    # if ftype == ".exe":
                    #     olderExe(fname,ftype,f,x)
                progress_bar.update(1)
        progress_bar.close()    
        print("\nSorted Successfully")

def deleteExe(dir):
    name = identify_file(".exe")
    destination = os.path.join(dir,name)
    trash = os.path.join(destination,"OLD FILES")
    ch = input("Do you want to delete exe older than 15 days (Y/N):...?")
    if ch.upper() == 'Y':
        for x in os.listdir(trash):
            f = os.path.join(trash,x)
            #print("CurrentFilePath",f)
            if os.path.isfile(f):
                fname , ftype = os.path.splitext(f)
                #print(fname,"    ",ftype)
                #print("CurrentFilePath",f,"    ","FileName",fname,"     ","Ftype",ftype)
                os.remove(f)
    else:
        print("OK, Files Sorted to folder OLDER FILES inside", identify_file(".exe"))

dirx = input("Enter the Parent Directory: ")
dir = rf"{dirx}"
print("Reading Directory...", end = ' ')
#printDot(3,2)
print("\n")
#or i in tqdm (range (100), desc="Loading..."):
sort(dir)
#deleteExe(dir);

print("Press any key to exit...")
keyboard.read_event()





            




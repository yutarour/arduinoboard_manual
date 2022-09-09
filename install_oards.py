import os
import zipfile
import json
import shutil
#non default packages
try:
    from tqdm import tqdm
except:
    os.system("python -m pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org --user tqdm")
    from tqdm import tqdm
try:
    import requests
    import urllib3
except:
    os.system("python -m pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org --user requests")
    import requests
    import urllib3

urllib3.disable_warnings()
arduino_path = r"C:\Users\{}\Documents\Arduino".format(os.environ["USERNAME"])
hardware_path = arduino_path+r"\hardware"
boards = []
with open("board_urls.json",'r') as file:
    boards = json.load(file)

def check_hardware_folder():
    if os.path.exists(arduino_path):
        if os.path.exists(hardware_path):
            return
        else:
            os.mkdir(hardware_path)
    else:
        print("Arduino is not installed or is not installed in the correct directory. Please edit the arduino preferences from file > preferences so that the sketch directory points to the documents folder. ")

def select_board():
    valid = False
    while valid == False:
        try:
            for board in range(len(boards)):
                print(board,boards[board]["Board_name"])
            print("q to quit")
            user_input = input("Which board do you want to add?: ")
            if user_input =="q":
                print("Quitting...")
                exit()
            board_choice = boards[int(user_input)]
            valid = True
        
        except Exception:
            print("error")
    return board_choice

def download_zip(url):
    req = requests.get(url,verify=False,stream=True)
    total_size_in_bytes= int(req.headers.get('content-length', 0))
    block_size = 1024 #1 Kibibyte
    progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)

    filename = url.split('/')[-1]
    os.chdir(hardware_path)
    with open(filename,"wb") as file:
        for data in req.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)
    progress_bar.close()
    return filename

def extract_zip(filename):
    with zipfile.ZipFile(filename) as zf:
        for member in tqdm(zf.infolist(), desc='Extracting '):
            try:
                zf.extract(member, hardware_path)
            except zipfile.error as e:
                pass
    os.remove(filename)
    return zf.namelist()[0]

def move_board_txt(folder_name):
    try:
        files = os.listdir(folder_name)
        if "boards.txt" not in files:
            print("Boards txt was not found")
        else:
            shutil.move(folder_name+"\\boards.txt",folder_name+"\\tools")
    except:
        print("something went wrong")

check_hardware_folder()
to_dl = select_board()
filename = download_zip(to_dl["URL"])
folder_name = extract_zip(hardware_path+"\\"+filename)
move_board_txt(folder_name)
print("Done")
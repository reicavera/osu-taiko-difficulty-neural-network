import zipfile
import os
import math
def get_number_of_files(path):
    counter = 0
    folders = [ f.path for f in os.scandir(path) if f.is_dir() ]
    for folder in folders:
        files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
        counter += len(files)
    return counter
def extract_osz_file(path, destination):
    total = get_number_of_files(path)
    padding = int(math.log10(total)) + 1
    i = 0
    folders = [ f.path for f in os.scandir(path) if f.is_dir() ]
    while(i < total):
        try:
            for folder in folders:
                files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
                for file in files:
                    if not os.path.exists(destination + '/' + str(i).zfill(padding)):
                        os.makedirs(destination + '/' + str(i).zfill(padding))
                        with zipfile.ZipFile(folder + '/' + file, 'r') as zip_ref:
                            zip_ref.extractall(destination + '/' + str(i).zfill(padding))
                    os.system('cls' if os.name == 'nt' else "printf '\033c'")
                    print(str(i + 1) + '/' + str(total))
                    i += 1
        except Exception as e:
            i = 0

extract_osz_file('./osz_files','./osu_files')
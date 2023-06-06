import os
import re
def note_density(notes, interval, limit):
    density = [0] * (limit // interval)
    for note in notes:
        density[note // interval] += 1
    return density
def filter_data(path):
    with open(path,'r',encoding="utf-8") as file:
        line = file.readline()
        while not re.match('Mode: +',line):
            line = file.readline()
        mode = int(re.findall('\d+', line )[0])
        if mode != 1:
            return None, None
        while not re.match('Version:+',line):
            line = file.readline()
        version = line.strip('\n').split(':',1)[1]
        while line != '[HitObjects]\n':
            line = file.readline()
        line = file.readline()
        notes = []
        while line:
            timestamp = int(line.split(',')[2])
            notes.append(timestamp)
            if timestamp >= 5 * 60 * 1000:
                return None, None
            line = file.readline()
        density = note_density(notes, 500, 5 * 60 * 1000)
        return version, density
def spread_difficulty(spread):
    diffs = []
    for diff in spread:
        version = diff[0]
        if re.match(".*kantan.*|.*easy.*|.*facil.*|.*beginner.*", version,re.IGNORECASE):
            diff[0] = 0
            diffs.append(0)
        if re.match(".*futsu.*|.*basic.*|.*normal.|.*past.*|.*advanced.*|.*whisper.*", version,re.IGNORECASE):
            diff[0] = 1
            diffs.append(0)
        if re.match(".*muzu.*|.*novice.*|.*hard.*|.*present.*|.*hyper.*|.*dificil.*|.*acoustic.*", version,re.IGNORECASE):
            diff[0] = 2
            diffs.append(0)
        if re.match(".*inner.*|.*ura.*|.*hell.*|.*maximum.*|.*heavenly.*|.*beyond.*|.*ex.*|.*master.*", version,re.IGNORECASE):
            diff[0] = 4
            diffs.append(0)
        if re.match(".*oni.*|.*exhaust.*|.*lunatic.*|.*insane.*|.*future.*|.*insano.*|.*ultra.*", version,re.IGNORECASE):
            diff[0] = 3
            diffs.append(0)
        
data = {
    "difficulty": ["Kantan", "Fuutsu", "Muzukashii", "Oni", "Inner Oni"],
    "density": [],
    "label": []
}

folders = [ f.path for f in os.scandir('./osu_files') if f.is_dir() ]
for folder in folders:
    spread = []
    files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f)) and f.endswith('.osu')]
    for f in files:
        path = (folder + '/' + f).replace('\\', '/')
        version, density = filter_data(path)
        if not version is None and not density is None:
            spread.append([version,density])
    if not len(spread) == 0:
        spread_difficulty(spread)
    for x in spread:
        if x[0] not in [0,1,2,3,4]:
            print(x[0])
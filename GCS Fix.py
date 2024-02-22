import os

def process_osu_file(file_path, artist, title):
    newfile = ""
    eventing = False   # Keeps track of if we're in the "Events" section of the osu file
    objecting = False  # Keeps track of if we're in the "HitObjects" section of the osu file
    timing = False     # Keeps track of if we're in the "TimingPoints" section of the osu file

    with open(file_path, "r", encoding="utf-8", errors='ignore') as f:
        for line in f.readlines():
            if '[TimingPoints]' in line:
                objecting = False
                eventing = False
                timing = True
            if eventing:
                continue
            if objecting:
                if ',' in line:
                    parts = line.strip().split(',')
                    if len(parts) >= 6:
                        last_colon_index = parts[-1].rfind(':')
                        if last_colon_index != -1:
                            parts[-1] = parts[-1][:last_colon_index + 1]  # Keep the last colon
                        newfile += ','.join(parts) + '\n'
                continue
            elif 'AudioFilename:' in line:
                newfile += f'AudioFilename: [{artist}] - {title}.ogg\n'
            elif 'Tags:' in line:
                newfile += 'Tags:BMS GCS 10K\n'
            elif 'Source:' in line:
                newfile += "Source:BMS\n"
            elif 'Creator:' in line:
                newfile += 'Creator:XDerbyX\n'
            elif 'HPDrainRate:' in line:
                newfile += 'HPDrainRate:8\n'
            elif 'OverallDifficulty:' in line:
                newfile += "OverallDifficulty:8\n"
            elif 'Version:' in line:
                parts = line.strip().split(':')
                if len(parts) >= 2:
                    version_info = parts[1].strip().split()  # Split version info
                    diffname = ' '.join(version_info[:-1])   # Join diffname
                    level = version_info[-1]                 # Extract level
                    newfile += f'Version:lv.{level} / ~{diffname}~\n'
            elif "[Events]" in line:
                eventing = True
                newfile += f'[Events]\n0,0,"[{artist}] {title}.jpg",0,0\n\n'
            elif timing and ',' in line:
                # If in TimingPoints section and line contains a comma
                values = line.strip().split(',')
                for i in range(len(values)):
                    if values[i] == '100':
                        values[i] = '10'  # Change the '100' slot to '10'
                        break
                newfile += ','.join(values) + '\n'
            elif "[HitObjects]" in line:
                eventing = False
                timing = False
                objecting = True
                newfile += "[HitObjects]\n"
            else:
                newfile += line

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(newfile)

if __name__ == '__main__':
    dir = "E:/soundsphere-master/soundsphere/userdata/export"
    count = 0  # Initialize the counter

    for file in os.listdir(dir):
        if file.endswith(".osu"):
            file_path = os.path.join(dir, file)
            with open(file_path,'r',encoding='utf-8',errors='ignore') as f:
                for line in f.readlines(): 
                    if 'Title:' in line:
                        title = line.split(':', 1)[1].strip() # Extracting title
                    if 'Artist:' in line:
                        artist = line.split(':', 1)[1].strip() # Extracting artist
            process_osu_file(file_path, artist, title)
            count += 1  # Counter
            print(f"#{count} Processed {file} successfully)")

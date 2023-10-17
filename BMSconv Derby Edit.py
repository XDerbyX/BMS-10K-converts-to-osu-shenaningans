import subprocess
import os
import shutil
from PIL import Image

if __name__ == '__main__':

    convert_path = "F:/BMS Pack/[NEW] GCS 10K 3.7 FULL PACK!" #Folder containing individual BMS song folders
    converter_path = "F:/Raindrop/convertOM.bat"
    converted_path = "F:/Converts"

    songs = os.listdir(convert_path)
    song_counter = 0 #Keep track of progress in the console

    size_counter = 0 #Keep track of the mapset file size
    Title = "Title:GCS 10K #1\n"
    TitleU = "TitleUnicode:GCS 10K #1\n"
    Title_Counter = 1 #Increment this every time we hit the upload limit and create a new mapset folder

    for song in songs:
        song_counter += 1
        parts = song.split(']')
    
        if len(parts) == 2:
            artist = parts[0][1:].strip()  # Remove the leading '[' and any extra spaces
            title_with_diffname = parts[1].strip()  # Remove any leading/trailing spaces
        
            # Split the title with diffname by '~' to separate the title
            title_parts = title_with_diffname.split('~')
        
            if len(title_parts) >= 1:
                title = title_parts[0].strip()  # Get the title, removing leading/trailing spaces
        audio_name = '[' + artist + ']' + ' - ' + title + '.ogg'    #Set a to-be name for the map audio
        songdir = convert_path + '/' + song
        bg = None

        for file in os.listdir(songdir):                                                   #For every chart file in the BMS folder
            if file[-4:] in ['.bms','.bme','.bml']:                                        #
                print("Song " + str(song_counter) + " of 403") #Progress indicator         #
                file_path = songdir + '/' + file                                           #
                                                                                           #
                is_dp = False                                                              #
                level = None                                                               #
                                                                                           #
                with open(file_path,'r',encoding='utf-8',errors='ignore') as f:            #
                    for line in f.readlines():                                             #
                        if '#PLAYER 3' in line:                                            #Check if it's DP
                            is_dp = True                                                   #
                        if '#PLAYER 1' in line:                                            #
                            break                                                          #
                        if '#TITLE' in line:
                            tilde_pos = line.find('~')
                            if tilde_pos != -1:                                            #Check if the tilde was found in the line
                                title = line[len("#TITLE"):tilde_pos]                      #Slice from '#TITLE' to the tilde
                                title = title.strip()                                      #Remove any leading/trailing whitespace
                        if '#TITLE' in line:                                               #
                            tilde_pos = line.find('~')                                     #
                            if tilde_pos != -1:                                            #Check if the tilde was found in the line
                                diffname = line[tilde_pos:]                                #Slice from the tilde to the end of the line
                                diffname = diffname.strip()                                #Remove any leading/trailing whitespace
                        if '#ARTIST' in line:
                            diffartist = line[8:-1]
                        if '#PLAYLEVEL' in line:                                           #To get the level
                            playlvl = line[11:-1]                                          #
                        if '#STAGEFILE' in line:                                           #
                            if '.' in line:                                                #
                                bg = line[11:-1]                                           #(Also get the BG image name if it uses one)
                            continue                                                       #
                                                                                           #
                if is_dp:                                                                  #
                    subprocess.call([converter_path,file_path])                            #And run it through Raindrop's converter (It outputs to the directory of the original BMS chart)

        if bg is not None:                        #If a BG name was found in the last part, create a jpg version and name it to audio_name.jpg for convenience
            im = Image.open(songdir + '/' + bg)                                                                
            im = im.convert("RGB")
            bg = '[' + artist + '] ' + title + ".jpg"
            im.save(songdir + '/' + bg)

        for file in os.listdir(songdir):        #In a new loop through the Song's directory:
            file_path = songdir + '/' + file        #Hold the path of the current file in a string for convenience
            if file[-4:] == '.osu':

                new_file = "" #Rewrite the osu file into this string with our changes

                with open(file_path,'r',encoding='utf-8',errors='ignore') as f:                           #Go through all the converted osu files, fix the metadata, and remove keysounds from everything
                    eventing = False  #Keeps track of if we're in the "Events" section of the osu file
                    objecting = False #Keeps track of if we're in the "Hitobjects" section of the osu file
                    for line in f.readlines():
                        if '[TimingPoints]' in line:
                            eventing = False
                        if eventing:
                            continue
                        if objecting:
                            if ',' in line[:3]:
                                new_file += line[:line.index(':')] + ":0:0:0:\n"
                            elif line[:3] == '272' and ',' not in line[:3]:
                                new_file += '496' + line[3:line.index(':')] + ":0:0:0:\n"
                            elif int(line[:3]) > 300 and ',' not in line[:3]:
                                new_file += str(int(line[:3])-32) + line[3:line.index(':')] + ":0:0:0:\n"
                            else:
                                new_file += line[:line.index(':')] + ":0:0:0:\n"
                            continue
                        if 'AudioFilename:' in line:                                #Yanderedev simulator
                            new_file += f'AudioFilename: {audio_name}\n'
                        elif 'osu file format' in line:
                            new_file += 'osu file format v14'
                        elif 'Creator:' in line:
                            new_file += "Creator:XDerbyX\n"
                        elif 'Title:' in line:
                            new_file += "Title:" + title + '\n'
                        elif 'TitleUnicode:' in line:
                            new_file += "TitleUnicode:" + title + '\n'
                        elif 'Artist:' in line:
                            new_file += "Artist:" + diffartist + '\n'
                        elif 'ArtistUnicode:' in line:
                            new_file += "ArtistUnicode:" + diffartist + '\n'
                        elif 'Version:' in line:
                            new_file += "Version:" + 'lv.' + playlvl + ' / ' + diffname + '\n'
                        elif 'Source:' in line:
                            new_file += "Source:BMS\n"
                        elif 'Tags:' in line:
                            new_file += "Tags:BMS GCS 10K\n"
                        elif 'HPDrainRate:' in line:
                            new_file += "HPDrainRate:8\n"
                        elif 'OverallDifficulty:' in line:
                            new_file += "OverallDifficulty:5\n"
                        elif 'ApproachRate:' in line:
                            new_file += "ApproachRate:9\n"
                        elif 'CircleSize:' in line:
                            new_file += "CircleSize:16\n"
                        elif 'SliderMultiplier:' in line:
                            new_file += "SliderMultiplier:1.4\n"
                        elif 'SliderTickRate:' in line:
                            new_file += "SliderTickRate:1\n"
                        elif "[Events]" in line:
                            eventing = True
                            new_file += f'[Events]\n0,0,"{bg}",0,0\n\n' if bg is not None else '[Events]\n0,0,"convertbg.jpg",0,0\n\n'  #"convertbg.jpg" is just a default BG I made for the mapset if the BMS chart didn't have a BG
                        elif "[HitObjects]" in line:
                            objecting = True
                            new_file += "[HitObjects]\n"
                        else:
                            new_file += line

                with open(file_path,'w',encoding='utf-8',errors='ignore') as f:    #Overwrite the convert with all the changes we made
                    f.write(new_file)

                shutil.move(file_path, converted_path + '/' + file)            #Move the polished osu file into a directory meant to be an osu mapset
                size_counter += os.path.getsize(converted_path + '/' + file)   #Keep track of the file size

            if file == 'audio.ogg':
                shutil.copy(file_path, converted_path + '/' + audio_name)            #This is copying the baked audio made using BMX2WAV into the osu mapset, naming it based on the song
                size_counter += os.path.getsize(converted_path + '/' + audio_name)   #Keep track of the file size
            
            if file == bg:
                shutil.copy(file_path, converted_path + '/' + bg)                    #Same for the background
                size_counter += os.path.getsize(converted_path + '/' + bg)
        
        if size_counter > 95000000:      #When the size of the osu mapset hits like 93mb, create a new mapset directory and build into that
            size_counter = 0
            converted_path += 'I'
            os.mkdir(converted_path)
            Title = Title[:-2] + str(Title_Counter + 1) + '\n'
            TitleU = TitleU[:-2] + str(Title_Counter + 1) + '\n'
        

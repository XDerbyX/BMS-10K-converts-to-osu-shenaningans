import os

#For changing 16k to 10K if so that no notes overlap happens
if __name__ == '__main__':
    dir = "E:/osu!/Songs/GCS 10K Pack #2"
    number_mapping = {
        21: 25,
        64: 76,
        106: 128,
        149: 178,
        191: 230,
        277: 281,
        288: 332,
        330: 384,
        373: 435,
        416: 486
    }

    def modify_first_number(line):
        if line.strip().startswith(('#', ';')): # Skip lines that start with comments
            return line

        parts = line.split(',')
        if len(parts) >= 1:
            try:
                first_number = int(parts[0])    # Check if the first number is in the mapping
                if first_number in number_mapping:
                    first_number = number_mapping[first_number]  # Replace with the new number
                parts[0] = str(first_number)
            except ValueError:
                pass
        return ','.join(parts)
    
    def exclude_string(line, string_to_exclude):
        if string_to_exclude in line:
            return line.replace(string_to_exclude, '')
        return line
    
    count = 0  # Initialize the counter

    for file in os.listdir(dir):
        if file.endswith(".osu"):
            with open(os.path.join(dir, file), "r", encoding="utf-8") as f:
                newfile = ""
                for line in f:
                    if 'PreviewTime' in line:
                        newfile += 'PreviewTime: 30000\n'
                    elif 'OverallDifficulty:' in line:
                        newfile += "OverallDifficulty:8\n"
                    elif 'CircleSize:16' in line:
                        newfile += 'CircleSize:10\n'
                    else:
                        line = exclude_string(line, ' / obj : GCS')
                        modified_line = modify_first_number(line)
                        newfile += modified_line

            with open(os.path.join(dir, file), "w", encoding="utf-8") as f:
                f.write(newfile)
            
            count += 1  # Counter
            print(f"Processed {file} ({count} lines changed)")

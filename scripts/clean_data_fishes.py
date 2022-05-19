file_r = open("../data/raw_data/fishes.txt", "r")
file_w = open("../data/raw_data/fishes_clean.txt", "w")

i=0
for line in file_r.readlines():
    if i==1 or i==2:
        file_w.write(line)
    i=i+1
    if i==4:
        i=0

file_w.close()
file_r.close()

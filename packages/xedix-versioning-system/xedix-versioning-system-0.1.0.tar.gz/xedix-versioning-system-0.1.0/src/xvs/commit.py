import time as tm

file = input()
message = input()

files = file.split(", ")

commits_file = open("commits.txt", "a")

time = tm.strftime("%H:%M %d:%m %Y")

commits_file.write("Made changes: " + message + " on " + time + "\n")

for file in files:
    commits_file.write(f"File: {file}\n")
    commits_file.write("------------------------------------------------\n")
    with open(file, "r") as f:
        for line in f:
            commits_file.write(line)
            
with open("status", "w") as f:
    f.write("Commited changes\non " + time + "\n")
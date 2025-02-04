import time as tm

class XVSCore:
    @staticmethod
    def handle_branch(name):
        with open("branches", "r") as branches_file:
            branches = branches_file.read()
            branches_list = branches.split(", ")

        if name not in branches_list:
            with open("branches", "w") as branches_file:
                branches_file.write(name + ", " + branches)

        commits_file = open("commits.txt", "a")
        time = tm.strftime("%H:%M %d:%m %Y")
        commits_file.write(f"\nCurrently on branch {name} on {time}\n")
        commits_file.close()

        with open("status", "w") as f:
            f.write(f"Changed branch to {name}\n")

    @staticmethod
    def handle_commit(files, message):
        files_list = files.split(", ")
        commits_file = open("commits.txt", "a")
        time = tm.strftime("%H:%M %d:%m %Y")
        
        commits_file.write(f"Made changes: {message} on {time}\n")
        
        for file in files_list:
            commits_file.write(f"File: {file}\n")
            commits_file.write("------------------------------------------------\n")
            try:
                with open(file, "r") as f:
                    for line in f:
                        commits_file.write(line)
            except FileNotFoundError:
                print(f"Error: File {file} not found")
                commits_file.close()
                return
                
        commits_file.close()
        
        with open("status", "w") as f:
            f.write(f"Committed changes\non {time}\n")

    @staticmethod
    def handle_status():
        with open("status", "r") as f:
            status = f.read()
        print(status)
        
    @staticmethod
    def handle_init():
        with open("branches", "w") as file:
            file.write("main")
        open("commits.txt", "w")
        open("status", "w")

    
    @staticmethod
    def handle_stage(files, message):
        files_list = files.split(", ")
        commits_file = open("commits.txt", "a")
        time = tm.strftime("%H:%M %d:%m %Y")
        
        commits_file.write(f"Started changing: {message} on {time}\n")
        
        for file in files_list:
            commits_file.write(f"File: {file}\n")
            commits_file.write("------------------------------------------------\n")
            try:
                with open(file, "r") as f:
                    for line in f:
                        commits_file.write(line)
            except FileNotFoundError:
                print(f"Error: File {file} not found")
                commits_file.close()
                return
                
        commits_file.close()
        
        with open("status", "w") as f:
            f.write("Waiting for commit")

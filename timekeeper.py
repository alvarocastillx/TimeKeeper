import os
import sys
import difflib
import json
import hashlib
from questionary import Style, select
from rich.console import Console

############
####aux#####

# get sha256 of file
def get_sha256_file(filepath):
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:   
        for chunk in iter(lambda: f.read(4096), b""):  
            sha256.update(chunk) 
    return sha256.hexdigest()

def exit():
    os._exit(0)
    
#############
console = Console()

def init():
    console.print(r"""
          
          
            
    _____  _  _      _____ _  __ _____ _____ ____  _____ ____ 
    /__ __\/ \/ \__/|/  __// |/ //  __//  __//  __\/  __//  __\
    / \  | || |\/|||  \  |   / |  \  |  \  |  \/||  \  |  \/|
    | |  | || |  |||  /_ |   \ |  /_ |  /_ |  __/|  /_ |    /
    \_/  \_/\_/  \|\____\\_|\_\\____\\____\\_/   \____\\_/\_\
                                                           
          
          
          """)
    if os.path.exists(".tkp"):
        console.print("Repository has been already initialized",style="bold red")
    else:
        os.makedirs(".tkp")
        os.makedirs(".tkp/objects")
        open(".tkp/index.tkp", "x")
        console.print("Repository has been created succesfully", style="bold green")
        
#TODO: delete deleted files
def add_all():
    src = os.getcwd()
    index_path = os.path.join(src, ".tkp", "index.tkp")

    existing_entries = []
    if os.path.exists(index_path):
        with open(index_path, "r") as f:
            for line in f:
                try:
                    parsed = json.loads(line.strip())
                    # actual files indexed by tkp
                    existing_entries.append(parsed)
                except:
                    pass

    updated_entries = existing_entries.copy()  
    
    # walk all folders and files, indexing only new or untracked files
    for root, dirs, files in os.walk(src):
        if ".git" in root or ".tkp" in root:
            continue

        for file in files:
            filepath = os.path.join(root, file)
            file_hash = get_sha256_file(filepath)

            found = False
            for i, entry in enumerate(updated_entries):
                if entry["file"] == filepath:
                    found = True
                    if entry["hash"] != file_hash:
                        console.print(f"Updating indexed {filepath}", style="bold blue")
                        updated_entries[i]["hash"] = file_hash
                    else:
                        console.print(f"Skipping unchanged {filepath}", style="bold yellow")
                    break

            if not found:
                console.print(f"Adding new file {filepath}", style="bold green")
                updated_entries.append({"file": filepath, "hash": file_hash})

    with open(index_path, "w") as f:
        for entry in updated_entries:
            f.write(json.dumps(entry) + "\n")
        

def help():
    console.print("""
        ======================================
                ⏳  Timekeeper v0.1
        A lightweight version control system
        ======================================

        Usage:
            timekeeper <command> [options]

        Available commands:
            init        Initialize a new repository
            add_all     Add all files to staging
            help        Show this help message

        Examples:
            timekeeper init
            timekeeper add_all
        """)

        
        
if __name__ == "__main__":
    possible_commands = {"init":init,"add_all":add_all,"help":help,"exit":exit}
    if len(sys.argv) >= 2 and sys.argv[1] in possible_commands:
        cmd = sys.argv[1]
        possible_commands[cmd]()
    else:
        custom_style = Style([
            ("qmark", "fg:#FF9D00 bold"),      
            ("question", "bold fg:#00FFFF"),   
            ("answer", "fg:#FFFF00 bold"),     
            ("pointer", "fg:#FF0000 bold"),    
            ("highlighted", "fg:#00FF00 bold"),
            ("selected", "fg:#FF00FF")         
        ])
        choice = select(
            "Timekeeper - choose an action:",
            choices=["init", "add_all", "help", "exit"],
            style=custom_style
        ).ask()

        possible_commands.get(choice)()


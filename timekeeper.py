import os
import sys
import json
import hashlib
from questionary import Style, select
from rich.console import Console
import datetime                                        

############
####aux#####
custom_style = Style([
            ("qmark", "fg:#FF9D00 bold"),      
            ("question", "bold fg:#00FFFF"),   
            ("answer", "fg:#FFFF00 bold"),     
            ("pointer", "fg:#FF0000 bold"),    
            ("highlighted", "fg:#00FF00 bold"),
            ("selected", "fg:#FF00FF")         
    ])

# get sha256 of file
def get_sha256_file(filepath):
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:   
        for chunk in iter(lambda: f.read(4096), b""):  
            sha256.update(chunk) 
    return sha256.hexdigest()

def exit():
    os._exit(0)

#creates objects of files
def objects_creator(file_hash, content):
    try:
        with open(f".tkp/objects/{file_hash}", "w", encoding="utf-8") as f:
            f.write(content)
    except:
        pass
    
def get_file_content(file):
    with open(file, "r", encoding="utf-8") as f:
        return f.read()
    
def staging_indexer():
    src = os.getcwd()
    version_files = [f for f in os.listdir(os.path.join(src, ".tkp")) if (str(f).__contains__("stage-"))]
    #if file doesnt exists is going to throw exception - creates file
    try:
        version_files.sort()
        choices = ["Create new stage","Stage current version"]
        choice = select(
            f"Last stage: {version_files[-1]} - choose an action:",
            choices= choices,
            style=custom_style
        ).ask()
        if (choice == choices[0]):
            last_num = int(version_files[-1].split('-')[1].split('.')[0])
            new_num = last_num + 1
            new_name = f"stage-{new_num}.tkp"
            index_path = os.path.join(src, ".tkp", new_name)
        else:
            index_path = os.path.join(src, ".tkp", version_files[-1])
    except:
        open(os.path.join(src, ".tkp", "stage-0.tkp"), "x")
        index_path = os.path.join(src, ".tkp", "stage-0.tkp")
    

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
    file_list = []
    for root, dirs, files in os.walk(src):
        if ".git" in root or ".tkp" in root or ".vscode" in root or "env" in root:
            continue 

        for file in files:
            #get filepath and hash
            filepath = os.path.join(root, file)
            file_hash = get_sha256_file(filepath)
            
            #add path to later compare whether the file has been removed or not
            file_list.append(filepath)

            #dont index nothing of git
            if file.__contains__("git") or file.__contains__("timekeeper") or file.__contains__("requirements"):
                continue
            
            #if tkp cant find file it indexes it, else skips or updates hash (file has changed since last add_all)
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
    
    #compares index.tkp with all found files, if files of index.tkp coulnt be found it means it has been deleted
    for entry in updated_entries:
        tracked_file = entry["file"]
        if tracked_file not in file_list:
            console.print(f"Removing index {tracked_file}", style="bold red")
            updated_entries.remove(entry)

    #updates index.tkp
    with open(index_path, "w") as f:
        #i dont delete objects no more, i cant revert stages if i do so     
        #TODO: arg --gc to remove non existent objects
        # shutil.rmtree(".tkp/objects/")
        # os.mkdir(".tkp/objects/")                                                             
        for entry in updated_entries:
            objects_creator(file_hash=entry["hash"], content=get_file_content(entry["file"]))
            f.write(json.dumps(entry) + "\n")
            

        
        
    
#############
console = Console()

def init():
    console.print(r"""
          
          
            
  _______ _                _  __                         
 |__   __(_)              | |/ /                         
    | |   _ _ __ ___   ___| ' / ___  ___ _ __   ___ _ __ 
    | |  | | '_ ` _ \ / _ \  < / _ \/ _ \ '_ \ / _ \ '__|
    | |  | | | | | | |  __/ . \  __/  __/ |_) |  __/ |   
    |_|  |_|_| |_| |_|\___|_|\_\___|\___| .__/ \___|_|   
                                        | |              
                                        |_|              
          
          
          """, style="bold red")
    if os.path.exists(".tkp"):
        console.print("Repository has been already initialized",style="bold red")
    else:
        os.makedirs(".tkp")
        os.makedirs(".tkp/objects")
        os.makedirs(".tkp/commits")
        # open(".tkp/stage-0.tkp", "x")
        console.print("Repository has been created succesfully", style="bold green")

#staging and objects creation 
def add_all():
    #indexes all files with its structure
    staging_indexer()
    
def commit():
    #creates snapshot of project
    choice = select(
            "Are you sure you want to commit last stage? Doing so will delete all stages and restart checkpoint. Check help for more information - choose an action:",
            choices=["Y", "N"],
            style=custom_style
        ).ask()
    if (choice=="Y"):
        console.print("Comitting...", style="bold blue")
        src = os.getcwd()
        tkp_path = os.path.join(src,".tkp")
        stage_files = [os.path.join(tkp_path,f) for f in os.listdir(tkp_path) if f.__contains__("stage")]
        try:
            if len(stage_files) == 0:
                console.print("ERROR - There is nothing to commit", style="bold red")
            else:
                #read content of last_stage #TODO: select stage to commit
                with open(stage_files[-1], "r", encoding="utf-8") as f:
                    last_stage_hash = get_sha256_file(stage_files[-1])
                    last_stage_content = f.read()

                commit_id = f"{str(last_stage_hash)}_{str(datetime.datetime.timestamp(datetime.datetime.now()))}.tkp"
                
                # write content of last stage into commits.tkp
                with open(os.path.join(tkp_path,"commits",commit_id), "w", encoding="utf-8") as f:
                    f.write(last_stage_content)
                    
                #remove all stage files 
                for stage_file in stage_files:
                    os.remove(stage_file)
                    
                console.print("Stage succesfully commited...", style="bold green")
        except Exception as e:
            console.print(f"An error ocurred during commit process. Err: {e}", style="bold red")
    else:
        console.print("Commit canceled by user", style="bold red")

#revert last stage
def revert_stage():
    choice = select(
            "Are you sure you want to revert project to last stage? - choose an action:",
            choices=["Y", "N"],
            style=custom_style
        ).ask()
    if choice == "Y":
        console.print("Reverting to previous stage...", style="bold blue")
        src = os.getcwd()
        tkp_path = os.path.join(src,".tkp")
        stage_files = [os.path.join(tkp_path,f) for f in os.listdir(tkp_path) if f.__contains__("stage")]
        try:
                
            if len(stage_files) == 0:
                console.print("ERROR - Stage to revert not found", style="bold red")
            else:
                #read lines of previous stage
                with open(stage_files[-1], "r", encoding="utf-8") as f:
                    stage_lines = f.read().splitlines()
                
                #delete files that werent in stage
                for root, dirs, files in os.walk(src):
                    if ".git" in root or ".tkp" in root or ".vscode" in root or "env" in root:
                        continue

                    for file in files:
                        #dont track nothing of git
                        if file.__contains__("git") or file.__contains__("timekeeper") or file.__contains__("requirements"):
                            continue
                        
                        filepath = os.path.join(root, file)
                        
                        if filepath not in [json.loads(line)["file"] for line in stage_lines]:
                            console.print(f"Removing {filepath}", style="bold red")
                            os.remove(filepath)

                #recovers previous state of all files
                for line in stage_lines:
                    entry = json.loads(line)
                    filepath = entry["file"]
                    filehash = entry["hash"]
                    
                    object_path = os.path.join(tkp_path, "objects", filehash)
                    with open(object_path, "r", encoding="utf-8") as obj_file:
                        content = obj_file.read()

                    os.makedirs(os.path.dirname(filepath), exist_ok=True)
                    with open(filepath, "w", encoding="utf-8") as f:
                        console.print(f"Recovering state of {filepath}...", style="bold green")
                        f.write(content)
                

                console.print("Stage restored successfully!", style="bold green")
                    
        except Exception as e:
            console.print(f"An error ocurred during revert process. Err: {e}", style="bold red")
    else:
        console.print("revert_stage canceled by user", style="bold red")
        pass
    
def revert_commit():
    choice = select(
        "Are you sure you want to revert project to last commit? - choose an action:",
        choices=["Y", "N"],
        style=custom_style
    ).ask()
    if choice == "Y":
        console.print("Reverting to previous commit...", style="bold blue")
        src = os.getcwd()
        commit_path = os.path.join(src,".tkp","commits")
        
        try:
            if len(os.listdir(commit_path)) == 0:
                console.print("ERROR - Commit to revert not found", style="bold red")
            else:
                #get commit file
                file_list = [f.split("_")[1] for f in os.listdir(commit_path)]
                file_list.sort(reverse=True)
                
                for f in os.listdir(commit_path):
                    if f.__contains__(file_list[0]):
                        commit_file = os.path.join(commit_path,f)
                
                #read lines of previous stage
                with open(commit_file, "r", encoding="utf-8") as f:
                    stage_lines = f.read().splitlines()
                
                #delete files that werent in stage
                for root, dirs, files in os.walk(src):
                    if ".git" in root or ".tkp" in root or ".vscode" in root or "env" in root:
                        continue

                    for file in files:
                        #dont track nothing of git
                        if file.__contains__("git") or file.__contains__("timekeeper") or file.__contains__("requirements"):
                            continue
                        
                        filepath = os.path.join(root, file)
                        
                        if filepath not in [json.loads(line)["file"] for line in stage_lines]:
                            console.print(f"Removing {filepath}", style="bold red")
                            os.remove(filepath)

                #recovers previous state of all files
                for line in stage_lines:
                    entry = json.loads(line)
                    filepath = entry["file"]
                    filehash = entry["hash"]
                    tkp_path = os.path.join(".tkp","")
                    
                    object_path = os.path.join(tkp_path, "objects", filehash)
                    with open(object_path, "r", encoding="utf-8") as obj_file:
                        content = obj_file.read()

                    os.makedirs(os.path.dirname(filepath), exist_ok=True)
                    with open(filepath, "w", encoding="utf-8") as f:
                        console.print(f"Recovering state of {filepath}...", style="bold green")
                        f.write(content)
                

                console.print("Commit restored successfully!", style="bold green")
                    
        except Exception as e:
            console.print(f"An error ocurred during commit process. Err: {e}", style="bold red")
    else:
        console.print("revert_commit canceled by user", style="bold red")
        pass

def uninstall():
    choice = select(
        "Are you sure you want to revert project to last commit? - choose an action:",
        choices=["Y", "N"],
        style=custom_style
    ).ask()
    if choice == "Y":
        console.print("Reverting to previous commit...", style="bold blue")
        src = os.getcwd()
        try:
            if os.path.exists(os.path.join(src,".tkp")):
                os.remove(os.path.join(src,".tkp"),)
            else:
                console.print("Timekeeper is not installed in this project",style="bold red")
        except PermissionError as e:
            console.print(f"An error ocurred while uninstalling. Do you have admin rights? Err: {e}", style="bold red")
        except Exception as e:
            console.print(f"An error ocurred while uninstalling. Err: {e}", style="bold red")
    else:
        console.print("uninstall canceled by user", style="bold red")

def help():
    console.print("""
        ======================================
                ⏳  Timekeeper v0.2
        A lightweight version control system
        ======================================
                  """, style="bold green")
    console.print("""
        Thanks for using TimeKeeper!           
                  
        
        Usage:
            timekeeper <command> [options]

        Available commands:
            init          Initialize a new repository
            add_all       Add all files to staging
            commit        Commit changes
            revert_stage  Revert project to last stage 
            revert_commit Revert project to last commit
            uninstall     Removes Timekeeper from your project
            help          Show this help message

        Examples:
            timekeeper init
            timekeeper add_all
        """)

        
        
if __name__ == "__main__":
    possible_commands = {"init":init,"add_all":add_all,"help":help,"commit":commit,"revert_stage":revert_stage,"revert_commit":revert_commit, "uninstall":uninstall, "exit":exit}
    if len(sys.argv) >= 2 and sys.argv[1] in possible_commands:
        cmd = sys.argv[1]
        possible_commands[cmd]()
    else:
        choice = select(
            "Timekeeper - choose an action:",
            choices=["init", "add_all", "commit","revert_stage","revert_commit","help","uninstall","exit"],
            style=custom_style
        ).ask()

        possible_commands.get(choice)()


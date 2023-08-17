# Packages
import openai, json, subprocess, os, re

# Environment Variables
from dotenv import load_dotenv

load_dotenv()

# Run the vma_config.json compiler
subprocess.run(["python", "vma_config.py"])

# These are the different steps of the VMA Pipeline
# 1. Initialization
# Load agent config

with open("vma_config.json", "r") as config:
    vma_config = json.load(config)

messages = [{"role": "system", "content": vma_config["Initialization"]["prompt"]}]
json_analysis = ""
root_dir = "to-migrate/"

# Recursive function to read everything of a directory
def scan_dir(dir):
    files = []
    for path in os.scandir(dir):
        if path.name == ".gitkeep":
            continue
        if path.is_file():
            files.append(f"{path.path}")
        elif path.is_dir():
            f = scan_dir(f"{dir}{path.name}/")
            for file in f:
                files.append(file)

    return files

# Scan the entire 'to-migrate' directory
# Read each file individually
files = {}
for file in scan_dir(root_dir):
    f = open(f"{file}", "r")
    files[file] = f.read()

# 1. Initialization
def initialization():
    print("1. Initialization\n")

    get_response(vma_config["Initialization"]["model"])


# 2. Parsing and Analysis
def parsing_and_analysis():
    print("\n2. Parsing and Analysis")

    message = f"{vma_config['Parsing and Analysis']['prompt']}{files}"
    
    global json_analysis
    add_message("user", message)
    json_analysis = get_response(vma_config["Parsing and Analysis"]["model"])


# 3. Transforming and Refactoring
def transforming_and_refactoring():
    print("\n3. Transforming and Refactoring\n")

    message = f"Provided is the JSON Analysis: {json_analysis}. {vma_config['Transformating and Refactoring']['prompt']}"
    add_message("user", message)

    response = get_response(vma_config["Transformating and Refactoring"]["model"])

    print("DEBUG DEBUG DEBUG DEBUG DEBUG DEBUG")
    print(response)
    # Write migrated code to 'migrated' folder

    # This is the whole message, not just the code
    # Sadly, GPT models aren't really able to just output their target without small talk
    # I'm scared some 'bugs' (more cases where you will need to re-run) will arrise here because
    # It's not really possible to ensure that the model will always format it's response correctly
    # This shouldn't be too much of an issue though, if it is, allow UMA to process this step with a more qualified model.

    global code
    code = re.search(r'```(.*?)```', response, re.DOTALL).group(1)
    print(code)


# 4. Processing and Parsing
def processing_and_parsing():
    print("4. Processing\n")
    add_message("user", vma_config["Processing and Parsing"]["prompt"])

    response = get_response(vma_config["Processing and Parsing"]["model"])
    global filename
    filename = re.search(r'```(.*?)```', response, re.DOTALL).group(1)

    print(filename)

    # Write content to the file
    with open(f"migrated/{filename}", "w") as f:
        f.write(code)

# 5. Collaboration
def collaboration():
    print("5. Collaboration\n")
    add_message("user", vma_config["Collaboration"]["prompt"])

    get_response(vma_config["Collaboration"]["model"])

    
    userInput = input("\nEnter your message (/exit to quit): ")
    while userInput != '/exit':
        add_message("user", userInput)
        get_response(vma_config["Collaboration"]["model"])
        userInput = input("\nEnter your message (/exit to quit): ")

def get_response(model):
    response = openai.ChatCompletion.create(
        model=model,
        stream=True,
        temperature=0,
        messages=messages,
        api_key=os.getenv("OPENAI_APIKEY"),
    )

    collected_messages = []
    for chunk in response:
        try:
            collected_messages.append(chunk['choices'][0]['delta']['content'])
            print(chunk['choices'][0]['delta']['content'], end='')
        except:
            continue


    return ''.join([str(elem) for elem in collected_messages])


def add_message(role, code):
    messages.append({"role": role, "content": code})


if __name__ == "__main__":
    if files == {}:
        print("'to-migrate/' directory is empty! Nothing to migrate.")
        print("Quiting...")
    else:
        initialization()
        parsing_and_analysis()
        transforming_and_refactoring()
        processing_and_parsing()
        collaboration()
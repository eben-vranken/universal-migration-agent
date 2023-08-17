# Packages
import openai, json, subprocess, os

# Environment Variables
from dotenv import load_dotenv

load_dotenv()

# Run the vma_config.json compiler
subprocess.run(["python", "vma_config.py"])


# These are the different steps of the VMA Pipeline
# 1. Initialization
# Load agent config
print("1. Initialization\n")

with open("vma_config.json", "r") as vma_config:
    vma_config = json.load(vma_config)

print("VMA_Config Initialized!")

# Initalize VMA
messages = [{"role": "system", "content": vma_config["init"]["prompt"]}]
root_dir = "to-migrate/"
json_analysis = ""


# Recursive function to read everything of a directory
def scan_dir(dir):
    files = []
    for path in os.scandir(dir):
        if path.is_file():
            files.append(f"{path.path}")
        elif path.is_dir():
            f = scan_dir(f"{dir}{path.name}/")
            for file in f:
                files.append(file)

    return files


# 2. Parsing and Analysis
def parsing_and_analysis():
    print("2. Parsing and Analysis")

    # Scan the entire 'to-migrate' directory
    # Read each file individually
    files = {}
    for file in scan_dir(root_dir):
        f = open(f"{file}", "r")
        files[file] = f.read()

    if files == {}:
        print("'to-migrate/' directory is empty! Nothing to migrate.")
        return False

    message = f"{vma_config['PAA']['prompt']}{files}"
    add_message("user", message)
    response = get_response(vma_config["PAA"]["model"])

    # Print Response
    global json_analysis
    json_analysis = response["choices"][0]["message"]["content"]

    print(json_analysis, "\n")

    return True


# 3. Transforming and Refactoring
def transforming_and_refactoring():
    print("3. Transforming and Refactoring\n")

    message = (
        f"Provided is the JSON Analysis: {json_analysis}. {vma_config['TAR']['prompt']}"
    )
    add_message("user", message)

    response = get_response(vma_config["TAR"]["model"])

    # Write migrated code to 'migrated' folder
    content = response["choices"][0]["message"]["content"]

    # This is the whole message, not just the code
    # Sadly, GPT models aren't really able to just output their target without small talk
    print(content, "\n")

    # Split content into just code
    global code
    code = content.split("```")[1].split("\n", 1)[1]


# Processing
def processing():
    print("4. Processing\n")
    add_message("user", vma_config["Processing"]["prompt"])

    response = get_response(vma_config["Processing"]["model"])
    content = response["choices"][0]["message"]["content"]

    global filename
    filename = content.split("```")[1].split("\n", 1)[0]
    print(filename)


def parsing():
    # Write content to the file
    with open(f"migrated/{filename}", "w") as f:
        f.write(code)


def get_response(model):
    response = openai.ChatCompletion.create(
        model=model,
        temperature=0,
        messages=messages,
        api_key=os.getenv("OPENAI_APIKEY"),
    )

    return response


def add_message(role, code):
    messages.append({"role": role, "content": code})


if __name__ == "__main__":
    parseSuccessful = parsing_and_analysis()
    if parseSuccessful:
        transforming_and_refactoring()

    processing()
    parsing()

# Packages
import openai, json, subprocess, os, re


# Run the vma_config.json compiler
subprocess.run(["python", "vma_config.py"])


# These are the different steps of the VMA Pipeline
# 1. Initialization
# Load agent config
print("1. Initialization\n")

with open("vma_config.json", "r") as vma_config:
    vma_config = json.load(vma_config)

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

    print(files)

    message = f"{vma_config['PAA']['prompt']}{files}"
    add_message("user", message)
    response = get_response(vma_config["PAA"]["model"])

    # Print Response
    global json_analysis
    json_analysis = response["choices"][0]["message"]["content"]

    print(json_analysis, "\n")


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
    code = content.split("```")[1].split("\n", 1)[1]

    print(code)

    # Write content to the file
    with open("migrated/index.py", "w") as f:
        f.write(code)


def get_response(model):
    response = openai.ChatCompletion.create(
        model=model,
        temperature=0,
        messages=messages,
        api_key="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",
    )

    return response


def add_message(role, code):
    messages.append({"role": role, "content": code})


if __name__ == "__main__":
    parsing_and_analysis()
    transforming_and_refactoring()

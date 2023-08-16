# Metadata Files
from config.metadata_loader import read_config, print_project_info

# Packages
import openai, json, subprocess


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


# 2. Parsing and Analysis
def parsing_and_analysis():
    print("2. Parsing and Analysis")
    add_message("user", vma_config["PAA"]["prompt"])

    with open("to-migrate\App.vue", "r") as to_migrate_code:
        add_message("user", to_migrate_code.read())
        to_migrate_code.close()

    response = get_response(vma_config["PAA"]["model"])

    # Print Response
    print(response['choices'][0], "\n")

# 3. Transforming and Refactoring
def transforming_and_refactoring():
    print("3. Transforming and Refactoring\n")
    add_message("user", vma_config["TAR"]["prompt"])

    response = get_response(vma_config["TAR"]["model"])

    # Print response
    print(response['choices'][0], "\n")

    # Write migrated code to 'migrated' folder
    content = response["choices"][0]["message"]

    # Write content to the file
    with open("migrated/App.vue", "w") as f:
        f.write(json.dumps(content))

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
    # Project information
    config_path = "config/metadata.json"
    project_config = read_config(config_path)
    print_project_info(project_config)

    parsing_and_analysis()
    transforming_and_refactoring()

    print("\nMigration Complete!")
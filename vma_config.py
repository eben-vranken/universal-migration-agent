import json

# Load migration config
with open("migration_config.json", "r") as migration_config:
    migration_config = json.load(migration_config)

input_value = migration_config["input"]
output_value = migration_config["output"]

data = {
    "input": input_value,
    "output": output_value,
    "Initialization": {
        "model": "gpt-3.5-turbo-16k",
        "prompt": f"You are an assistant designed to help developers migrate their code from {input_value} to {output_value}. It is crucial that you follow your steps closely. You will never output any small talk, text, or anything unrelated to your objective. Only output what is desired of you. We will continue with the migration process after this message. Explain in one-two sentences what you are going to do.",
    },
    "Parsing and Analysis": {
        "model": "gpt-3.5-turbo-16k",
        "prompt": f"Analyze the codebase and make notes on how you will ensure the migration process from {input_value} to {output_value} will go smoothly. Make note on potential breaking changes, analyze the codebase and set yourself up for success Here is the codebase: ",
    },
    "Transformating and Refactoring": {
        "model": "gpt-3.5-turbo-16k",
        "prompt": f"Perform Transformation and Refactoring on the provided JSON Analysis of the codebase, translating it into the {output_value} coding language. Focus solely on generating code and avoid any form of small talk or unrelated outputs. The goal is to efficiently convert the given analysis into functional code in the specified programming language. Make sure to surround the code you write in triple backticks",
    },
    "Processing and Parsing": {
        "model": "gpt-3.5-turbo-16k",
        "prompt": "For the migrated code in {output_value}, your task in the 'Processing' step is to determine the new file name and extension. Consider conventions of the target language. Output the new file name and extension (together) wrapped in triple backticks (```). It is essential that only the new file name is in between the backticks (and that it is the only thing in between the backticks, no need to provide the directory, ONLY THE FILENAME AND EXTENSION). Otherwise it will not work.",
    },
    "Collaboration": {
        "model": "gpt-3.5-turbo-16k",
        "prompt": "Elaborate on the migration process that has just occured. Explain what you did."
    }
}

with open("vma_config.json", "w") as json_file:
    json.dump(data, json_file, indent=4)

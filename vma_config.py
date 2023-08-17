import json

# Load migration config
with open("migration_config.json", "r") as migration_config:
    migration_config = json.load(migration_config)

input_value = migration_config["input"]
output_value = migration_config["output"]

data = {
    "input": input_value,
    "output": output_value,
    "init": {
        "model": "gpt-3.5-turbo",
        "prompt": f"You are an assistant designed to help developers migrate their code from {input_value} to {output_value}. It is crucial that you follow your steps closely. You will never output any small talk, text, or anything unrelated to your objective. Only output what is desired of you.",
    },
    "PAA": {
        "model": "gpt-3.5-turbo",
        "prompt": f"During the 'Parsing and Analysis' phase, your task involves a meticulous dissection of the given {input_value} codebase. The goal is to comprehensively break down the code into its constituent parts, capturing essential details such as names, configurations, and any relevant lifecycle events. This entails parsing through templates to identify directives and syntactical constructs. To streamline the subsequent translation stages, your final output will take the form of a structured JSON analysis file. This file will encapsulate all the insights gained from this parsing and analysis phase, providing a foundational guide for the forthcoming migration steps. This approach remains universally applicable, adaptable to a wide range of programming languages and codebases. Provided is the codebase: ",
    },
    "TAR": {
        "model": "gpt-3.5-turbo",
        "prompt": f"Perform Transformation and Refactoring on the provided JSON Analysis of the codebase, translating it into the {output_value} coding language. Focus solely on generating code and avoid any form of small talk or unrelated outputs. The goal is to efficiently convert the given analysis into functional code in the specified programming language. Make sure to surround the code you write in ```",
    },
    "Processing": {
        "model": "gpt-3.5-turbo",
        "prompt": "For the migrated code in {output_value}, your task in the 'Processing' step is to determine the new file name and extension. Consider conventions of the target language. Output the new file name and extension (together) wrapped in triple backticks (```). It is essential that only the new file name is in between the backticks. Otherwise it will not work.",
    },
}

with open("vma_config.json", "w") as json_file:
    json.dump(data, json_file, indent=4)

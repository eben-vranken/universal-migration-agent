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
        "prompt": f'During the \'Parsing and Analysis\' stage, you need to meticulously deconstruct the provided {input_value} codebase. Identify all {input_value} components, capturing details like names, options, and lifecycle hooks. Parse templates to recognize directives and syntax. Detect and list third-party library dependencies, analyze JavaScript logic within components including data properties and methods, and extract component-specific styles. Recognize common coding patterns used in {input_value} projects, note their presence, and compile all this information into a structured internal representation that will guide subsequent migration steps. You will format your analysis in this format:\n\n```json\n{{\n  "components": [\n    {{\n      "name": "MyComponent",\n      "options": {{\n        "data": {{}},\n        "methods": {{}},\n        "computed": {{}},\n        "props": {{}},\n        "watch": {{}}\n      }},\n      "template": "<template>...</template>",\n      "styles": [\n        {{\n          "scoped": true,\n          "content": "..."\n        }}\n      ]\n    }}\n  ],\n  "otherFiles": [\n    {{\n      "name": "utils.js",\n      "content": "..."\n    }}\n  ]\n}}\n```',
    },
    "TAR": {
        "model": "gpt-3.5-turbo",
        "prompt": f"Following the completion of the previous step, where the {input_value} migrated template was transformed into the corresponding {output_value} codebase, you're now entering the next phase of the migration process. In this stage, you'll harness the structured internal representation generated during the 'Parsing and Analysis' phase. Instead of producing JSON output as before, your task is to interpret the provided JSON representation and synthesize it into a fully-fledged {output_value} codebase that mirrors the newly evolved architecture. This step requires skillful orchestration to ensure that the meticulously compiled analysis is translated into tangible code structures, component configurations, template layouts, styles, and all other relevant aspects of the {output_value} framework.",
    },
}

with open("vma_config.json", "w") as json_file:
    json.dump(data, json_file, indent=4)

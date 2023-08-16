# Metadata Files
from config.metadata_loader import read_config, print_project_info

# Packages
import openai, json


# Load agent config
with open("vma_config.json", "r") as vma_config:
    vma_config = json.load(vma_config)


# Initalize VMA
messages = [{"role": "assistant", "content": vma_config["init"]["prompt"]}]


# These are the different steps of the VMA Pipeline
def parsing_and_analysis():
    add_message("system", vma_config["PAA"]["prompt"])

    with open("to-migrate\\test.html", "r") as code:
        add_message("user", code.read())
        code.close()

    response = get_response("gpt-3.5-turbo")


def get_response(model):
    response = openai.ChatCompletion.create(
        model=model,
        temperature=0,
        stream=True,
        messages=messages,
        api_key="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",
    )

    # get the refactored script
    for entry in response:
        choice = entry["choices"][0]
        if choice["finish_reason"] == "stop":
            break

        if choice["finish_reason"] is not None:
            print("ERR: Unexpected finish_reason", choice["finish_reason"])
            sys.exit(1)

        delta_content = choice["delta"].get("content")
        if delta_content is not None:
            print(delta_content, end="")

    return response


def add_message(role, code):
    messages.append({"role": role, "content": code})


if __name__ == "__main__":
    # Project information
    config_path = "config/metadata.json"
    project_config = read_config(config_path)
    print_project_info(project_config)

    parsing_and_analysis()

import json

def read_config(file_path):
    with open(file_path, 'r') as metadata:
        metadata = json.load(metadata)
    return metadata

def print_project_info(metadata):
    print(f"""
Project: {metadata['project_name']}
Version: {metadata['version']}
Author: {metadata['author']}
Description: {metadata['description']}
Release Date: {metadata['release_date']}
""")
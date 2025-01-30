import importlib
import json
import os
from hatchling.builders.hooks.plugin.interface import BuildHookInterface
from pathlib import Path
import sys
import toml

class CustomBuildHook(BuildHookInterface):
    # Code in this function will run before building
    def initialize(self, version, build_data):
        extract_info_from_pyproject(self, 'header')
        extract_info_from_pyproject(self, 'modules')
        extract_info_from_pyproject(self, 'help')

# Creates a meta file with data extracted from a pyproject.py section
def extract_info_from_pyproject(self, tool_section_name):

    # Read the pyproject.toml file
    pyproject_path = os.path.join(self.root, 'pyproject.toml')
    with open(pyproject_path, 'r', encoding='utf-8') as pyproject_file:
        pyproject_data = toml.load(pyproject_file)
    
    # Extract the [tool.section_name] section
    section_data = pyproject_data.get('tool', {}).get(tool_section_name, {})
    
    if not section_data:
        print(f"No {tool_section_name} section found in pyproject.toml")
    
    # Map to store the module names and paths
    section_map = {}

    for module_name, module_info in section_data.items():
        section_map[module_name] = module_info
    
    # Create the JSON file with the module map
    json_file_path = os.path.join(self.root, 'src', f"{tool_section_name}.json")
    
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(section_map, json_file, indent=4)

    sys.stdout.write(f"Selected section data extracted to: {json_file_path}")
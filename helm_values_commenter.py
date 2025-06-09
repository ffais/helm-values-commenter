import re
import argparse
from pathlib import Path

def add_comments_to_yaml(input_file, output_file):
    with open(input_file, 'r') as file:
        yaml_content = file.readlines()
    
    output_lines = []
    key_pattern = re.compile(r'^(\s*)([^#\s:]+)(\s*:\s*)(.*)$')
    current_path = []
    prev_indent = 0
    
    for i, line in enumerate(yaml_content):
        match = key_pattern.match(line)
        if match:
            indent, key, separator, value = match.groups()
            indent_level = len(indent)
            
            # Update current path based on indentation
            if indent_level > prev_indent:
                # Nested deeper
                pass
            elif indent_level < prev_indent:
                # Went up one or more levels
                levels_up = (prev_indent - indent_level) // 2  # Assuming 2 spaces per level
                current_path = current_path[:-levels_up]
            else:
                # Same level
                if current_path:
                    current_path = current_path[:-1]
            
            current_path.append(key)
            prev_indent = indent_level
            
            full_path = '.'.join(current_path)
            comment_line = f"{indent}# {full_path} --\n"
            
            # Check if previous line is already this comment
            if i > 0 and yaml_content[i-1].strip() == f"# {full_path} --":
                output_lines.append(line)
            else:
                output_lines.append(comment_line)
                output_lines.append(line)
        else:
            # Handle non-key lines (empty lines, comments, etc.)
            output_lines.append(line)
            # Reset path if we're not in a nested structure
            if line.strip() and not line.strip().startswith('#'):
                current_path = []
                prev_indent = 0
    
    with open(output_file, 'w') as file:
        file.writelines(output_lines)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Add comments with full paths above each key in a YAML file')
    parser.add_argument('input_file', help='Path to the input YAML file')
    parser.add_argument('output_file', help='Path to save the output YAML file with comments')
    
    args = parser.parse_args()
    
    add_comments_to_yaml(args.input_file, args.output_file)
    print(f"Processed YAML file with full path comments saved to {args.output_file}")

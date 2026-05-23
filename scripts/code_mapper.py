#!/usr/bin/env python3
import os
import sys
import re

class CodebaseMapper:
    def __init__(self, target_dir):
        self.target_dir = target_dir
        self.classes = {}  # name -> {parent: string, methods: list, fields: list}
        self.dependencies = []  # list of (file_a, file_b)

    def scan_files(self):
        for root, _, files in os.walk(self.target_dir):
            for file in files:
                if file.endswith(('.h', '.hpp', '.cpp', '.c', '.cc')):
                    filepath = os.path.join(root, file)
                    self.parse_file(filepath, file)

    def parse_file(self, filepath, filename):
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception:
            return

        # 1. Parse #includes for file-level dependencies
        includes = re.findall(r'#include\s+["<]([^">]+)[">]', content)
        for inc in includes:
            self.dependencies.append((filename, inc))

        # 2. Parse C++ Class Inheritance
        # Matches: class Dog : public Animal or class Dog:Animal, etc.
        class_regex = r'class\s+(\w+)\s*(?::\s*(?:public|protected|private)?\s*(\w+))?\s*\{'
        classes_found = re.findall(class_regex, content)
        for cls, parent in classes_found:
            parent_name = parent if parent else None
            self.classes[cls] = {
                "parent": parent_name,
                "file": filename
            }

    def generate_mermaid(self):
        lines = ["classDiagram"]
        
        # Add class relationships (Inheritance)
        has_relations = False
        for cls, meta in self.classes.items():
            if meta["parent"]:
                lines.append(f"    {meta['parent']} <|-- {cls}")
                has_relations = True
            else:
                lines.append(f"    class {cls}")
                
        # Add file include dependencies as dashed associations
        # To avoid cluttering, only show associations between files in the same scan
        file_list = {cls_meta["file"] for cls_meta in self.classes.values()}
        for src, dest in self.dependencies:
            if src in file_list and dest in file_list:
                lines.append(f"    %% Dependency: {src} includes {dest}")
                
        if not has_relations and len(self.classes) == 0:
            return "%% No classes detected in scan."
            
        return "\n".join(lines)

def main():
    if len(sys.argv) < 2:
        print("Usage: python code_mapper.py [directory]")
        sys.exit(1)
        
    directory = sys.argv[1]
    if not os.path.exists(directory):
        print(f"Error: Directory '{directory}' does not exist.")
        sys.exit(1)
        
    print(f"Scanning codebase under: {directory}")
    mapper = CodebaseMapper(directory)
    mapper.scan_files()
    
    print("\n--- Detected Classes ---")
    for cls, meta in mapper.classes.items():
        parent_info = f" inherits {meta['parent']}" if meta['parent'] else " (base)"
        print(f"Class: {cls}{parent_info} [in {meta['file']}]")
        
    print("\n--- Generated Mermaid Diagram ---")
    print(mapper.generate_mermaid())

if __name__ == "__main__":
    main()

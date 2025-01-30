#!/usr/bin/env python3

import argparse
import os
from typing import List
from ai_agent_toolbox import Toolbox, XMLParser, XMLPromptFormatter
from filecannon.file_manager import FileManager
from .ai_manager import AIManager

class FileCannon:
    def __init__(self):
        self.toolbox = Toolbox()
        self.parser = XMLParser(tag="use_tool")
        self.formatter = XMLPromptFormatter(tag="use_tool")

    def run(self, prompt: str, examples: List[str], model: str, output_dir: str):
        if not FileManager.validate_path(output_dir):
            print(f"Error: Invalid output directory '{output_dir}'")
            return

        # Setup tools with current output_dir
        def write_file(file_path: str, content: str):
            print("Writing to", file_path, "--", content)
            full_path = os.path.join(output_dir, file_path)
            FileManager.write_file(full_path, content)

        self.toolbox.add_tool(
            name="write_file",
            fn=write_file,
            args={
                "file_path": {"type": "string", "description": "File path relative to output directory"},
                "content": {"type": "string", "description": "Content to write to file"}
            },
            description="Write content to a file in the output directory"
        )

        # Build system prompt with tool instructions
        system_prompt = """You are FileCannon, an AI-powered file generation tool. Your task is to create new files based on examples and natural language descriptions. 
        Generate content that is practical and production-ready, following the structure and conventions shown in the example files.
        """
        system_prompt += self.formatter.usage_prompt(self.toolbox)

        # Prepare examples content
        example_contents = [FileManager.read_file(ex) for ex in examples]
        user_prompt = self._build_prompt(prompt, examples, example_contents)
        print("SYSTEM PROMPT", system_prompt)
        print("---")
        print("USER PROMPT", user_prompt)
        print("---")

        # Generate and parse response
        manager = AIManager(model)
        response = manager.generate_content(system_prompt, prompt)
        # Execute parsed tool calls
        for event in self.parser.parse(response):
            self.toolbox.use(event)

    def _build_prompt(self, prompt: str, examples: List[str], contents: List[str]) -> str:
        user_prompt = prompt
        if examples:
            user_prompt += "\n\nExisting files for reference:\n"
            for path, content in zip(examples, contents):
                user_prompt += f"File: {path}\n{content}\n\n"
        return user_prompt

def main():
    parser = argparse.ArgumentParser(description="filecannon: AI-powered file generation CLI tool")
    parser.add_argument("prompt", help="Description of the file to generate")
    parser.add_argument("-e", "--example", action="append", help="Path to example file(s)")
    parser.add_argument("-m", "--model", default="claude-3-5-sonnet-20241022", help="Model to use")
    parser.add_argument("-o", "--output", default=".", help="Output directory")

    args = parser.parse_args()
    FileCannon().run(args.prompt, args.example or [], args.model, args.output)

if __name__ == "__main__":
    main()


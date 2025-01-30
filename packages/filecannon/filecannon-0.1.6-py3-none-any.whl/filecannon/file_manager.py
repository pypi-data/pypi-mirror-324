import os
from typing import List

class FileManager:
    @staticmethod
    def list_files(directory: str) -> List[str]:
        """
        List all files in the given directory.

        Args:
            directory (str): Path to the directory to list files from.

        Returns:
            List[str]: A list of file names in the directory.
        """
        try:
            return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        except OSError as e:
            print(f"Error listing files in directory {directory}: {e}")
            return []

    @staticmethod
    def read_file(path: str) -> str:
        """
        Read the content of a file.

        Args:
            path (str): Path to the file to read.

        Returns:
            str: Content of the file as a string.
        """
        try:
            with open(path, 'r') as file:
                return file.read()
        except IOError as e:
            print(f"Error reading file {path}: {e}")
            return ""

    @staticmethod
    def write_file(path: str, content: str) -> bool:
        """
        Write content to a file.

        Args:
            path (str): Path to the file to write.
            content (str): Content to write to the file.

        Returns:
            bool: True if the file was written successfully, False otherwise.
        """
        try:
            directory = os.path.dirname(path)
            if not os.path.exists(directory):
                os.makedirs(directory)
            with open(path, 'w') as file:
                file.write(content)
            return True
        except IOError as e:
            print(f"Error writing to file {path}: {e}")
            return False

    @staticmethod
    def validate_path(path: str) -> bool:
        """
        Validate if a given path is safe to use.

        Args:
            path (str): Path to validate.

        Returns:
            bool: True if the path is valid and safe, False otherwise.
        """
        try:
            # Normalize the path
            normalized_path = os.path.normpath(path)
            
            # Check if the path is absolute
            if os.path.isabs(normalized_path):
                return False
            
            # Check if the path contains any parent directory references
            if '..' in normalized_path.split(os.sep):
                return False
            
            # Additional checks can be added here based on specific requirements
            
            return True
        except Exception as e:
            print(f"Error validating path {path}: {e}")
            return False

    @staticmethod
    def generate_xml_output(path: str, content: str) -> str:
        """
        Generate XML output for the write_file tool.

        Args:
            path (str): Path to the file.
            content (str): Content to be written to the file.

        Returns:
            str: XML formatted string for the write_file tool.
        """
        return f"""
        <use_tool>
            <name>write_file</name>
            <path>{path}</path>
            <content>
                {content}
            </content>
        </use_tool>
        """

# Example usage
if __name__ == "__main__":
    # List files in the current directory
    print("Files in current directory:", FileManager.list_files("."))

    # Read a file
    content = FileManager.read_file("example.txt")
    print("Content of example.txt:", content)

    # Write to a file
    success = FileManager.write_file("output/new_file.txt", "Hello, FileCannon!")
    print("File write success:", success)

    # Validate a path
    valid = FileManager.validate_path("safe/path/file.txt")
    print("Path validation result:", valid)

    # Generate XML output
    xml_output = FileManager.generate_xml_output("output/generated_file.py", "print('Hello, FileCannon!')")
    print("XML Output:", xml_output)
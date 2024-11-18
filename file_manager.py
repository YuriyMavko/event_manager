import os
import json
from datetime import datetime


class FileManager:
    def __init__(self, base_dir="data"):
        self.base_dir = base_dir
    @staticmethod
    def read_file(file_path):
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        return None

    @staticmethod
    def write_file(file_path, content, mode='w'):
        directory = os.path.dirname(file_path)
        if directory:  # Check if directory exists in path
            os.makedirs(directory, exist_ok=True)
        with open(file_path, mode, encoding='utf-8') as file:
            if isinstance(content, dict):
                json.dump(content, file, ensure_ascii=False, indent=4)
            else:
                file.write(content)

    @staticmethod
    def delete_file(file_path):
        if os.path.exists(file_path):
            os.remove(file_path)

    @staticmethod
    def read_json(file_path):
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        return None

    @staticmethod
    def write_json(file_path, data):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    @staticmethod
    def append_to_file(file_path, content):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'a', encoding='utf-8') as file:
            file.write(content)

    @staticmethod
    def read_lines(file_path):
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.readlines()
        return []

    @staticmethod
    def write_lines(file_path, lines):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as file:
            file.writelines(lines)

    @staticmethod
    def file_exists(file_path):
        return os.path.exists(file_path)

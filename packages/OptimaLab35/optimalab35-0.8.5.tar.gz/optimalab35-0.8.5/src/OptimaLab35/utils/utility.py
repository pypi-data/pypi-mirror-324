import yaml
import os

class Utilities:
    def __init__(self):
        pass

    def read_yaml(self, yaml_file):
        try:
            with open(yaml_file, "r") as file:
                data = yaml.safe_load(file)
                return data
        except (FileNotFoundError, PermissionError) as e:
            print(f"Error loading settings file: {e}")
            return

    def write_yaml(self, yaml_file, data):
        try:
            with open(yaml_file, "w") as file:
                yaml.dump(data, file)
        except PermissionError as e:
            print(f"Error saving setings: {e}")

    def program_configs(self):
        """Prepear folder for config and generate default exif if non aviable"""
        program_folder = self._ensure_program_folder_exists()
        if not os.path.isfile(f"{program_folder}/exif.yaml"):
            self._default_exif(f"{program_folder}/exif.yaml")

    def _ensure_program_folder_exists(self):
        program_folder = os.path.expanduser("~/.config/OptimaLab35")
        print(program_folder)
        if not os.path.exists(program_folder):
            print("in not, make folder")
            os.makedirs(program_folder)
        return program_folder

    def _default_exif(self, file):
        """Makes a default exif file."""
        print("Making default")
        def_exif = {
            "artist": [
                "Mr Finchum",
                "John Doe"
            ],
            "copyright_info": [
                "All Rights Reserved",
                "CC BY-NC 4.0",
                "No Copyright"
            ],
            "image_description": [
                "ILFORD DELTA 3200",
                "ILFORD ILFOCOLOR",
                "LomoChrome Turquoise",
                "Kodak 200"
            ],
            "iso": [
                "200",
                "400",
                "1600",
                "3200"
            ],
            "lens": [
                "Nikon LENS SERIES E 50mm",
                "AF NIKKOR 35-70mm",
                "Canon FD 50mm f/1.4 S.S.C"
            ],
            "make": [
                "Nikon",
                "Canon"
            ],
            "model": [
                "FG",
                "F50",
                "AE-1"
            ],
            "user_comment": [
                "Scanner: NORITSU-KOKI",
                "Scanner: NA"
            ]
        }
        self.write_yaml(file, def_exif)

    def append_number_to_name(self, base_name: str, current_image: int, total_images: int, invert: bool):
            """"Returns name, combination of base_name and ending number."""
            total_digits = len(str(total_images))
            if invert:
                ending_number = total_images - (current_image - 1)
            else:
                ending_number = current_image
            ending = f"{ending_number:0{total_digits}}"
            return f"{base_name}_{ending}"

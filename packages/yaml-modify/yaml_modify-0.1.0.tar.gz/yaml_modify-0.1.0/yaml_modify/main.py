import yaml
import os
from setuptools import setup, find_packages

def modify_yaml(file_path, key_path, new_value):
    """
    Изменяет значение указанного ключа в YAML-файле.

    :param file_path: Путь к YAML-файлу.
    :param key_path: Путь к ключу в виде списка (например, ["disks", "test1", "options", "test_time"]).
    :param new_value: Новое значение для ключа.
    """
    if not os.path.exists(file_path):
        print(f"Файл {file_path} не найден.")
        return

    try:
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file) or {}

        ref = data
        for key in key_path[:-1]:
            ref = ref.setdefault(key, {})
        old_value = ref.get(key_path[-1], None)
        ref[key_path[-1]] = new_value
        print(f"Изменение {'.'.join(key_path)}: {old_value} -> {new_value}")

        with open(file_path, 'w') as file:
            yaml.safe_dump(data, file, default_flow_style=False, allow_unicode=True)

        print(f"Файл {file_path} успешно изменён.")
    except Exception as e:
        print(f"Ошибка при обработке файла {file_path}: {e}")

def main():
    file_paths = {
        "gpu_test": "/etc/aquarius/testing/local/gpu_test/gpu_test.yml",
        "stressapptest": "/etc/aquarius/testing/local/stressapptest/stressapptest.yml",
        "fio_test": "/etc/aquarius/testing/local/fio_test/fio_test.yml",
    }

    modifications = [
        {"file": file_paths["gpu_test"], "key_path": ["duration"], "new_value": 1},
        {"file": file_paths["stressapptest"], "key_path": ["testing_time"], "new_value": 30},
        {"file": file_paths["fio_test"], "key_path": ["disks", "test1", "options", "test_time"], "new_value": "30s"},
    ]

    for modification in modifications:
        modify_yaml(modification["file"], modification["key_path"], modification["new_value"])

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import argparse
import json
import logging
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

# Пользовательские исключения для более точного управления ошибками.
class YAMLFileError(Exception):
    pass

class BackupError(Exception):
    pass

class CommandExecutionError(Exception):
    pass

@dataclass
class Modification:
    """
    Data class для описания изменения в YAML-файле.
    """
    file_path: Path
    key_path: List[str]
    new_value: Any

class YAMLFileHandler:
    """
    Обёртка для безопасного чтения и записи YAML-файлов.
    """
    def __init__(self, path: Path) -> None:
        self.path = path

    def read(self) -> Dict[str, Any]:
        if not self.path.exists():
            raise YAMLFileError(f"Файл не найден: {self.path}")
        with self.path.open("r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}

    def write(self, data: Dict[str, Any]) -> None:
        with self.path.open("w", encoding="utf-8") as f:
            yaml.safe_dump(data, f, default_flow_style=False, allow_unicode=True)

class BackupManager:
    """
    Менеджер резервного копирования и восстановления.
    """
    def __init__(self, backup_file: Path) -> None:
        self.backup_file = backup_file
        self.backups = self.load_backups()

    def load_backups(self) -> Dict[str, Dict[str, Any]]:
        if self.backup_file.exists():
            with self.backup_file.open("r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def save_backups(self) -> None:
        with self.backup_file.open("w", encoding="utf-8") as f:
            json.dump(self.backups, f, indent=4)

    def backup_data(self, file_path: Path, key_path: List[str], old_value: Any) -> None:
        file_str = str(file_path)
        if file_str not in self.backups:
            self.backups[file_str] = {}
        self.backups[file_str][".".join(key_path)] = old_value
        self.save_backups()

    def restore(self) -> None:
        if not self.backup_file.exists():
            return
        for file_str, changes in self.backups.items():
            file_path = Path(file_str)
            handler = YAMLFileHandler(file_path)
            data = handler.read()
            for key_path_str, old_value in changes.items():
                keys = key_path_str.split(".")
                ref = data
                for key in keys[:-1]:
                    ref = ref.setdefault(key, {})
                ref[keys[-1]] = old_value
            handler.write(data)
        self.backup_file.unlink()

class TestOrchestrator:
    """
    Выполнение набора тестовых команд.
    """
    def __init__(self) -> None:
        self.commands = [
            "testsystem --stage preburn --debug --output old_aq_test",
            "testsystem --stage inventory --debug --output old_aq_test",
            "testsystem --stage wifi --debug --output old_aq_test",
            "testsystem --stage bluetooth --debug --output old_aq_test",
            "testsystem --stage memory_stress --debug --output old_aq_test",
            "testsystem --stage gpu_stress --debug --output old_aq_test",
            "testsystem --stage fio_test --debug --output old_aq_test",
            "testsystem --stage os_install --debug --output old_aq_test",
        ]

    def run(self) -> None:
        for command in self.commands:
            subprocess.run(command, shell=True, check=True)

class Orchestrator:
    """
    Главный класс-оркестратор, объединяющий изменение YAML, восстановление и выполнение тестов.
    """
    def __init__(self, backup_file: Path) -> None:
        self.backup_manager = BackupManager(backup_file)
        self.test_orchestrator = TestOrchestrator()

    def run_restore(self) -> None:
        self.backup_manager.restore()

    def run_test_mode(self) -> None:
        self.test_orchestrator.run()

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Утилита для управления изменениями YAML и оркестрацией тестов."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-r", "--restore", action="store_true", help="Восстановление изменений из резервной копии")
    group.add_argument("-t", "--test", action="store_true", help="Запуск тестовых команд")
    return parser.parse_args()

def main() -> None:
    args = parse_args()
    orchestrator = Orchestrator(backup_file=Path("backup.json"))
    if args.restore:
        orchestrator.run_restore()
    elif args.test:
        orchestrator.run_test_mode()

if __name__ == "__main__":
    main()

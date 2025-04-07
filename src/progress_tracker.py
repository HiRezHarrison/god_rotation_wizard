from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional
import os
from pathlib import Path

class TaskStatus(Enum):
    PENDING = "Pending"
    PROCESSING = "Processing"
    SUCCESS = "Success"
    FAILURE = "Failure"

    def get_icon_path(self, icons_dir: str) -> str:
        """Get the path to the status icon."""
        return os.path.join(icons_dir, f"{self.value}.png")

@dataclass
class TaskResult:
    status: TaskStatus
    message: Optional[str] = None
    data: Optional[Dict] = None

class ChestCreationTracker:
    def __init__(self, icons_dir: str, logging_config: dict, has_bonus_chest: bool = False):
        self.icons_dir = icons_dir
        self.logging_config = logging_config
        
        # Initialize all tasks as pending
        self.tasks = {
            "Chest Item Created": TaskStatus.PENDING,
            "Treasure Choice Vendor Created": TaskStatus.PENDING,
            "Treasure Content Vendor Created": TaskStatus.PENDING,
            "Treasure Box to Choice Loot Created": TaskStatus.PENDING,
            "Treasure Choice to Content Loot Created": TaskStatus.PENDING,
            "Treasure Content Loots Created": TaskStatus.PENDING,
        }
        
        if has_bonus_chest:
            bonus_tasks = {
                "Bonus Chest Item Created": TaskStatus.PENDING,
                "Treasure BONUS Chance Vendor Created": TaskStatus.PENDING,
                "BONUS Treasure Box to Chance Loot Created": TaskStatus.PENDING,
                "Treasure Chance to Content Loot Created": TaskStatus.PENDING,
                "Zero Percent Drop Loot Created": TaskStatus.PENDING,
            }
            self.tasks.update(bonus_tasks)

        self.results = {}

    def update_task_status(self, task_name: str, status: TaskStatus, 
                          message: Optional[str] = None, 
                          data: Optional[Dict] = None) -> None:
        """Update the status of a task and store its result."""
        if task_name not in self.tasks:
            raise ValueError(f"Unknown task: {task_name}")
            
        self.tasks[task_name] = status
        self.results[task_name] = TaskResult(status, message, data)

    def all_tasks_completed(self) -> bool:
        """Check if all tasks are either Success or Failure."""
        return all(status in (TaskStatus.SUCCESS, TaskStatus.FAILURE) 
                  for status in self.tasks.values())

    def write_log(self, chest_name: str) -> None:
        """Write the detailed results to a log file."""
        log_dir = self.logging_config.get('log_directory', 'logs')
        log_prefix = self.logging_config.get('log_file_prefix', 'chest_creation_')
        log_path = os.path.join(log_dir, f"{log_prefix}{chest_name}.log")
        
        os.makedirs(log_dir, exist_ok=True)
        
        with open(log_path, 'w') as f:
            for task_name, result in self.results.items():
                f.write(f"Task: {task_name}\n")
                f.write(f"Status: {result.status.value}\n")
                if result.message:
                    f.write(f"Message: {result.message}\n")
                if result.data:
                    f.write("Data:\n")
                    for key, value in result.data.items():
                        f.write(f"  {key}: {value}\n")
                f.write("\n")

    def get_task_icon_path(self, task_name: str) -> str:
        """Get the icon path for a specific task's status."""
        if task_name not in self.tasks:
            raise ValueError(f"Unknown task: {task_name}")
        return self.tasks[task_name].get_icon_path(self.icons_dir)

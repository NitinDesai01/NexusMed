import sys
import os

# Get the root directory (NexusMed folder)
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, root_dir)

from custom_dataset_loader import CustomDatasetLoader

# Re-export for backward compatibility
DatasetLoader = CustomDatasetLoader

_loader = None

def get_dataset_loader(dataset_path=None):
    global _loader
    if _loader is None:
        _loader = CustomDatasetLoader(dataset_path)
    return _loader

if __name__ == "__main__":
    loader = get_dataset_loader()
    print("✅ Dataset loader ready!")

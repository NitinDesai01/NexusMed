import sys
import os

# Add root directory to path
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, root_dir)

from custom_dataset_loader import CustomDatasetLoader

# Re-export
DatasetLoader = CustomDatasetLoader

def get_dataset_loader(dataset_path=None):
    return CustomDatasetLoader(dataset_path)

if __name__ == "__main__":
    loader = get_dataset_loader()
    print("✅ Dataset loader ready!")

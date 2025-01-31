from typing import Optional
from torch.utils.data import random_split, Dataset, DataLoader
from valtra.dataloader import DynamicDataLoader

def split_dataset(
        dataset: Dataset, 
        train_ratio: float = 0.7, 
        val_ratio: Optional[float] = 0.15, 
        test_ratio: Optional[float] = 0.15,
        batch_size: int = 32
    ) -> DynamicDataLoader:
    """
    Splits a dataset into `train`, `val`, and `test` subsets and returns a DynamicDataLoader.

    Args:
        dataset (Dataset): The dataset to split.
        train_ratio (float, optional): Proportion of dataset for training (default: 0.7).
        val_ratio (float, optional): Proportion of dataset for validation (default: 0.15).
        test_ratio (float, optional): Proportion of dataset for testing (default: 0.15).
        batch_size (int, optional): Batch size for DataLoaders (default: 32).

    Returns:
        DynamicDataLoader: A dynamically switchable DataLoader for train, val, and test sets.
    
    Raises:
        ValueError: If the sum of provided ratios does not equal 1.
    """
    total_ratio = train_ratio + (val_ratio or 0) + (test_ratio or 0)
    if not (0.99 <= total_ratio <= 1.01):  # Allow small floating-point errors
        raise ValueError(f"Train, val, and test ratios must sum to 1. Got {total_ratio} instead.")

    split_sizes = [int(len(dataset) * ratio) for ratio in (train_ratio, val_ratio or 0, test_ratio or 0)]
    split_sizes[-1] = len(dataset) - sum(split_sizes[:-1])  # Ensure total dataset size matches

    names = ["train", "val", "test"]
    subsets = random_split(dataset, split_sizes)

    # Convert subsets into DataLoaders
    loaders = {
        name: DataLoader(subset, batch_size=batch_size, shuffle=(name == "train"))
        for name, subset, ratio in zip(names, subsets, (train_ratio, val_ratio, test_ratio)) if ratio > 0
    }

    return DynamicDataLoader(**loaders)

from typing import Iterator, Dict, Any, Union
import torch
from torch.utils.data import DataLoader

class DynamicDataLoader:
    def __init__(self, **dataloaders: DataLoader) -> None:
        """
        A flexible DataLoader wrapper that allows dynamically switching between multiple named DataLoaders.

        Args:
            **dataloaders (DataLoader): Named DataLoaders (e.g., train=..., test=..., val=...).
        
        Raises:
            ValueError: If no DataLoaders are provided.
        """
        if not dataloaders:
            raise ValueError("At least one DataLoader must be provided.")
        
        self.dataloaders: Dict[str, DataLoader] = dataloaders
        self.device: torch.device = torch.device("cpu")  # Default device

    def add_dataloaders(self, **dataloaders: DataLoader) -> None:
        """
        Adds more DataLoaders to the existing collection.

        Args:
            **dataloaders (DataLoader): Named DataLoaders to add (e.g., val=..., aug=...).
        """
        self.dataloaders.update(dataloaders)

    def __call__(self, **kwargs: bool) -> Iterator[Any]:
        """
        Returns an iterator over the selected DataLoader based on the keyword argument.

        Args:
            **kwargs (bool): The selected DataLoader name (e.g., train=True, test=True).

        Returns:
            Iterator[Any]: An iterator over the selected DataLoader.

        Raises:
            ValueError: If multiple or no DataLoaders are selected.
            ValueError: If the specified DataLoader does not exist.
        """
        selected_loaders = [name for name, value in kwargs.items() if value]
        
        if len(selected_loaders) == 0:
            raise ValueError(f"No DataLoader specified. Available options: {list(self.dataloaders.keys())}")
        if len(selected_loaders) > 1:
            raise ValueError("Only one DataLoader can be selected at a time.")

        loader_name = selected_loaders[0]
        if loader_name not in self.dataloaders:
            raise ValueError(f"DataLoader '{loader_name}' not found. Available: {list(self.dataloaders.keys())}")

        loader = self.dataloaders[loader_name]
        for batch in loader:
            yield self._move_to_device(batch)

    def _move_to_device(self, batch: Any) -> Any:
        """
        Moves batch data to the stored device.

        Args:
            batch (Any): The batch data.

        Returns:
            Any: The batch data moved to the correct device.
        """
        if isinstance(batch, (tuple, list)):
            return tuple(item.to(self.device) for item in batch)
        return batch.to(self.device)

    def to(self, device: Union[str, torch.device]) -> "DynamicDataLoader":
        """
        Sets the device for the DataLoader and ensures all batches are moved there dynamically.

        Args:
            device (Union[str, torch.device]): The device to move data to (e.g., 'cuda' or 'cpu').

        Returns:
            DynamicDataLoader: Returns itself for method chaining.
        """
        self.device = torch.device(device)
        return self  # Enable method chaining

    def __repr__(self) -> str:
        """
        Returns a string representation of the DynamicDataLoader.

        Returns:
            str: A string listing available DataLoaders and the current device.
        """
        return f"DynamicDataLoader(loaders={list(self.dataloaders.keys())}, device={self.device})"

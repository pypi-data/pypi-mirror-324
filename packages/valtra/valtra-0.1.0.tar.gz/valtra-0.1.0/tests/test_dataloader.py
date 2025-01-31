import unittest
import torch
from torch.utils.data import DataLoader, TensorDataset
from valtra.dataloader import DynamicDataLoader


class TestDynamicDataLoader(unittest.TestCase):
    def setUp(self):
        """Setup dummy datasets and dataloaders for testing."""
        self.data = torch.randn(100, 10)
        self.labels = torch.randint(0, 5, (100,))

        dataset = TensorDataset(self.data, self.labels)

        train_size = int(0.8 * len(dataset))
        test_size = len(dataset) - train_size
        self.train_dataset, self.test_dataset = torch.utils.data.random_split(dataset, [train_size, test_size])

        self.train_loader = DataLoader(self.train_dataset, batch_size=16, shuffle=True)
        self.test_loader = DataLoader(self.test_dataset, batch_size=16, shuffle=False)

        self.dataloader = DynamicDataLoader(train=self.train_loader, test=self.test_loader)

    def test_single_loader_access(self):
        """Test accessing training and test DataLoaders."""
        batch = next(iter(self.dataloader(train=True)))
        self.assertEqual(batch[0].shape[1], 10)  # Ensure feature size is correct

        batch = next(iter(self.dataloader(test=True)))
        self.assertEqual(batch[0].shape[1], 10)  # Ensure feature size is correct

    def test_invalid_loader_selection(self):
        """Test that selecting multiple loaders raises an error."""
        with self.assertRaises(ValueError):
            next(iter(self.dataloader(train=True, test=True)))

    def test_missing_loader(self):
        """Test that accessing a non-existent DataLoader raises an error."""
        with self.assertRaises(ValueError):
            next(iter(self.dataloader(val=True)))  # 'val' was not provided

    def test_to_device(self):
        """Test if .to() correctly updates the device."""
        self.dataloader.to("cuda")
        self.assertEqual(self.dataloader.device.type, "cuda")

        self.dataloader.to("cpu")
        self.assertEqual(self.dataloader.device.type, "cpu")


if __name__ == "__main__":
    unittest.main()

import unittest
import torch
from torch.utils.data import TensorDataset
from valtra.dataloader import DynamicDataLoader
from valtra.utils import split_dataset


class TestSplitDataset(unittest.TestCase):
    def setUp(self):
        """Create a sample dataset for testing."""
        self.data = torch.randn(100, 10)  # 100 samples, 10 features
        self.labels = torch.randint(0, 5, (100,))  # 100 labels, 5 classes
        self.dataset = TensorDataset(self.data, self.labels)

    def test_default_split(self):
        """Test default train/val/test split (70/15/15)."""
        dynamic_loader = split_dataset(self.dataset)

        self.assertIsInstance(dynamic_loader, DynamicDataLoader)

        # Check that data can be retrieved correctly
        train_batch = next(iter(dynamic_loader(train=True)))
        val_batch = next(iter(dynamic_loader(val=True)))
        test_batch = next(iter(dynamic_loader(test=True)))

        self.assertEqual(train_batch[0].shape[1], 10)  # 10 features
        self.assertEqual(val_batch[0].shape[1], 10)
        self.assertEqual(test_batch[0].shape[1], 10)

    def test_train_test_split_only(self):
        """Test train-test split without validation."""
        dynamic_loader = split_dataset(self.dataset, train_ratio=0.8, val_ratio=0, test_ratio=0.2)

        self.assertIsInstance(dynamic_loader, DynamicDataLoader)

        self.assertIsNotNone(dynamic_loader(train=True))
        self.assertIsNotNone(dynamic_loader(test=True))
        with self.assertRaises(ValueError):
            next(iter(dynamic_loader(val=True)))  # val shouldn't exist

    def test_train_val_split_only(self):
        """Test train-val split without test."""
        dynamic_loader = split_dataset(self.dataset, train_ratio=0.75, val_ratio=0.25, test_ratio=0)

        self.assertIsInstance(dynamic_loader, DynamicDataLoader)

        self.assertIsNotNone(dynamic_loader(train=True))
        self.assertIsNotNone(dynamic_loader(val=True))
        with self.assertRaises(ValueError):
            next(iter(dynamic_loader(test=True)))  # test shouldn't exist

    def test_custom_split(self):
        """Test a custom train-val-test split."""
        dynamic_loader = split_dataset(self.dataset, train_ratio=0.6, val_ratio=0.25, test_ratio=0.15)

        self.assertIsInstance(dynamic_loader, DynamicDataLoader)

        # Check that data can be retrieved correctly
        train_batch = next(iter(dynamic_loader(train=True)))
        val_batch = next(iter(dynamic_loader(val=True)))
        test_batch = next(iter(dynamic_loader(test=True)))

        self.assertEqual(train_batch[0].shape[1], 10)  # 10 features
        self.assertEqual(val_batch[0].shape[1], 10)
        self.assertEqual(test_batch[0].shape[1], 10)

    def test_invalid_ratio_sum(self):
        """Test that an error is raised if the ratios don't sum to 1."""
        with self.assertRaises(ValueError):
            split_dataset(self.dataset, train_ratio=0.5, val_ratio=0.3, test_ratio=0.3)

    def test_edge_case_full_train(self):
        """Test edge case where all data is allocated to training."""
        dynamic_loader = split_dataset(self.dataset, train_ratio=1.0, val_ratio=0, test_ratio=0)

        self.assertIsInstance(dynamic_loader, DynamicDataLoader)

        # Only "train" should exist
        self.assertIsNotNone(dynamic_loader(train=True))
        with self.assertRaises(ValueError):
            next(iter(dynamic_loader(val=True)))
        with self.assertRaises(ValueError):
            next(iter(dynamic_loader(test=True)))


if __name__ == "__main__":
    unittest.main()

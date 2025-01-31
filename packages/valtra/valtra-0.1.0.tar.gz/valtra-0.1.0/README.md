# Valtra (Validation - Train)

Valtra is a mini-project I created because I got sick of keeping track of train and validation/test datasets separately.  
It dynamically switches between training and validation/test data using a simple wrapper around PyTorch’s `DataLoader`.

## 📌 Why "Valtra"?
The name comes from **Val**idation and **Tra**in. Plus, it has a nice ring to it.

## 🚀 Installation
```bash
pip install valtra
```

## 🔧 Usage
```python
import torch
from valtra.dataloader import DynamicDataLoader
from valtra.utils import split_dataset

# Create dummy data
data = torch.randn(1000, 10)
labels = torch.randint(0, 5, (1000,))
dataset = torch.utils.Dataset(data, labels)

# Create DynamicDataLoader
dataloader = split_dataset(dataset, split_ratio=0.8, batch_size=32)

# Training loop (default behavior is training mode)
for batch in dataloader(train=True):
    print("Train batch:", batch[0].shape)

# Evaluation loop
for batch in dataloader(test=True):
    print("Test batch:", batch[0].shape)

# Evaluation loop
for batch in dataloader(other=True):
    print("Other batch:", batch[0].shape)
```

## Contribution
There are many ways to make code more readable in `torch`. If you have another idea feel free to contact me or create an issue!

## 📜 License
MIT License

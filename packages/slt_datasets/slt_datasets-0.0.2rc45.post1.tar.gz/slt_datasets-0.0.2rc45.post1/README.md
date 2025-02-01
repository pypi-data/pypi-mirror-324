# SLT Datasets Downloader

## Overview

SLT Datasets Downloader is a Python library that allows users to download and process multiple sign language translation (SLT) datasets from different languages. It is designed to facilitate the training of machine learning models for SLT tasks.

## Features
- Supports multiple sign language datasets.
- Provides tools for downloading, preprocessing, and tokenizing datasets.
- Compatible with PyTorch for model training.
- Handles different input types (video, pose) and output types (text, gloss).

## Supported Datasets
The following datasets are supported:

| Name | Input Language | Target Language | Status | # Samples | Hs | Video | Pose | Transcription | Gloss | Other data | # Words | # Singletons | # Signers | Source | BLEU (4) |
|------|---------------|----------------|--------|-----------|----|-------|------|--------------|-------|------------|---------|--------------|----------|--------|----------|
| RWTH-PHOENIX Weather 2014 T | GSL | German | Downloaded | 7,096 | 10 | Yes | No | Yes | Yes | - | 2,887 | 1,077 | 9 | TV | 28.95 |
| LSA-T | LSA | Spanish | Downloaded | 14,880 | 22 | Yes | Yes (MP) | Yes | No | - | 14,239 | 7,150 | 103 | Web | 0.93 (WER) |
| How2Sign | ASL | English | Downloaded | 35,000 | 80 | Yes | Yes | Yes | Yes | Multiple angles, 3D pose, Speech | 16,000 | - | 11 | - | 8.03 |
| LSFB-CONT | French-Belgian SL | French-Belgian Glosses | Downloaded | 85,000 | 25 | Yes | Yes (MP) | No | Yes | - | 6,883 | - | 100 | Laboratory | - |
| ISLTranslate | Indian SL | English | Downloaded | 31,222 | - | Yes | Yes (MP) | Yes | No | - | 11,655 | - | - | - | 6.09 |
| GSL | Greek SL (GSL) | Greek | Downloaded | 40,826 | 10 | Yes | No | No | Yes | Depth | 310 | 0 | 7 | Laboratory | 20.62 (WER) |                           |

## Installation
To install the library and its dependencies, run:
```bash
pip install -r requirements.txt
```

## Usage
### Loading a Dataset
```python
from slt_datasets.SLTDataset import SLTDataset

dataset = SLTDataset(
    data_dir="/path/to/dataset",
    input_mode="video",
    output_mode="text",
    split="train"
)
```
### Accessing Samples
```python
sample_input, sample_output = dataset[0]
```
### Visualizing Pose Data
```python
dataset.visualize_pose(0)
```

## Project Structure
```
 |-src
 | |-slt_datasets
 | | |-SLTDataset.py  # Main dataset loader
 | | |-WordLevelTokenizer.py  # Tokenizer for text processing
 | | |-dataset_comparison.ipynb  # Notebook for dataset comparison
 |-tests
 | |-test_methods.py  # Unit tests for the dataset loader
 |-docs  # Documentation files
 |-requirements.txt  # Dependency list
 |-pyproject.toml  # Project configuration
 |-README.md  # This file
```

## Contributing
Contributions are welcome! Please follow the guidelines in `CONTRIBUTING.md` and ensure your code passes all tests before submitting a pull request.

## License
This project is licensed under the terms of the `LICENSE` file.

## Support
For any issues or questions, please refer to `SUPPORT.md` or open an issue in the repository.


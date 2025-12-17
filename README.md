# Plant Village Corn

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/spMohanty/PlantVillage-Dataset)

Corn leaf disease classification dataset from Plant Village. This dataset contains images of corn leaves with various diseases and healthy samples for classification tasks.

- Project page: `https://github.com/spMohanty/PlantVillage-Dataset`
- Original dataset: `https://www.kaggle.com/datasets/abdallahalidev/plantvillage-dataset`

## TL;DR

- **Task**: classification (five classes: `healthy`, `common_rust`, `gray_leaf_spot`, `northern_leaf_blight`, `background`)
- **Modality**: RGB
- **Platform**: handheld/field
- **Real/Synthetic**: real
- **Images**: 44,096 images (16,412 with annotations)
- **Classes**: 5
- **Resolution**: 256×256 pixels (standardized)
- **Annotations**: COCO JSON (image-level via full-image boxes)
- **License**: CC BY 4.0 (see LICENSE)
- **Citation**: see below

## Table of contents

- [Download](#download)
- [Dataset structure](#dataset-structure)
- [Sample images](#sample-images)
- [Annotation schema](#annotation-schema)
- [Stats and splits](#stats-and-splits)
- [Quick start](#quick-start)
- [Evaluation and baselines](#evaluation-and-baselines)
- [Datasheet (data card)](#datasheet-data-card)
- [Known issues and caveats](#known-issues-and-caveats)
- [License](#license)
- [Citation](#citation)
- [Changelog](#changelog)
- [Contact](#contact)

## Download

- Original dataset: `https://www.kaggle.com/datasets/abdallahalidev/plantvillage-dataset`
- This repo hosts structure and conversion scripts only; place the downloaded folders under this directory.
- Local license file: see `LICENSE` (CC BY 4.0).

## Dataset structure

This dataset follows the standardized dataset structure specification:

```
corn/
├── csv/                      # CSV annotations per image
├── json/                     # JSON annotations per image
├── images/                   # All images
├── labelmap.json            # Label mapping
└── sets/                     # Dataset splits
    ├── train.txt
    ├── val.txt
    ├── test.txt
    ├── all.txt
    └── train_val.txt
├── annotations/              # COCO format JSON (generated)
│   ├── corn_instances_train.json
│   ├── corn_instances_val.json
│   └── corn_instances_test.json
├── scripts/
│   ├── reorganize_dataset.py # Dataset reorganization script
│   └── convert_to_coco.py    # COCO conversion script
├── LICENSE
├── README.md
└── requirements.txt
```

- Splits: `corn/sets/train.txt`, `corn/sets/val.txt`, `corn/sets/test.txt` (and also `all.txt`, `train_val.txt`) list image basenames (no extension). If missing, all images are used.

## Sample images

Below are example images for each category in this dataset. Paths are relative to this README location.

<table>
  <tr>
    <th>Category</th>
    <th>Sample</th>
  </tr>
  <tr>
    <td><strong>Healthy</strong></td>
    <td>
      <img src="corn/images/00031d74-076e-4aef-b040-e068cd3576eb___R.S_HL_8315_copy_2.jpg" alt="Healthy example" width="260"/>
      <div align="center"><code>corn/images/00031d74-076e-4aef-b040-e068cd3576eb___R.S_HL_8315_copy_2.jpg</code></div>
    </td>
  </tr>
  <tr>
    <td><strong>Common Rust</strong></td>
    <td>
      <img src="corn/images/00031d74-076e-4aef-b040-e068cd3576eb___R.S_HL_8315_copy_2.jpg" alt="Common Rust example" width="260"/>
      <div align="center"><code>corn/images/...</code></div>
    </td>
  </tr>
  <tr>
    <td><strong>Gray Leaf Spot</strong></td>
    <td>
      <img src="corn/images/00031d74-076e-4aef-b040-e068cd3576eb___R.S_HL_8315_copy_2.jpg" alt="Gray Leaf Spot example" width="260"/>
      <div align="center"><code>corn/images/...</code></div>
    </td>
  </tr>
  <tr>
    <td><strong>Northern Leaf Blight</strong></td>
    <td>
      <img src="corn/images/00031d74-076e-4aef-b040-e068cd3576eb___R.S_HL_8315_copy_2.jpg" alt="Northern Leaf Blight example" width="260"/>
      <div align="center"><code>corn/images/...</code></div>
    </td>
  </tr>
</table>

## Annotation schema

- CSV per-image schemas (stored under `corn/csv/` folder):
  - Classification task: columns include `item, x, y, width, height, label` (full-image bounding box: `[0, 0, image_width, image_height]`).
- COCO-style (generated):
```json
{
  "info": {"year": 2025, "version": "1.0.0", "description": "Plant Village Corn corn train split", "url": "https://www.kaggle.com/datasets/abdallahalidev/plantvillage-dataset"},
  "images": [{"id": 1, "file_name": "corn/images/IMG_0001.jpg", "width": 256, "height": 256}],
  "categories": [{"id": 0, "name": "background", "supercategory": "corn"}, {"id": 1, "name": "healthy", "supercategory": "corn"}, {"id": 2, "name": "common_rust", "supercategory": "corn"}, {"id": 3, "name": "gray_leaf_spot", "supercategory": "corn"}, {"id": 4, "name": "northern_leaf_blight", "supercategory": "corn"}],
  "annotations": [{"id": 10, "image_id": 1, "category_id": 1, "bbox": [0, 0, 256, 256], "area": 65536, "iscrowd": 0}]
}
```

- Label maps: `corn/labelmap.json` defines the category mapping; the provided converter normalizes to 5 categories (background=0, healthy=1, common_rust=2, gray_leaf_spot=3, northern_leaf_blight=4).

## Stats and splits

- Total images: 44,096
  - Healthy: 11,620 images
  - Common Rust: 11,920 images
  - Gray Leaf Spot: 6,104 images
  - Northern Leaf Blight: 9,880 images
  - Background: 4,572 images
- Images with annotations: 16,412
- Training set: 515 images (`corn/sets/train.txt`)
- Validation set: 111 images (`corn/sets/val.txt`)
- Test set: 780 images (`corn/sets/test.txt`)
- Classes: 5 (background=0, healthy=1, common_rust=2, gray_leaf_spot=3, northern_leaf_blight=4)
- Splits provided via `corn/sets/*.txt`. You may define your own splits by editing those files.

**Note**: The original dataset contains more images than the provided splits. The splits may need to be regenerated to include all images.

## Quick start

Python (COCO):
```python
from pycocotools.coco import COCO
coco = COCO("annotations/corn_instances_train.json")
img_ids = coco.getImgIds()
img = coco.loadImgs(img_ids[0])[0]
ann_ids = coco.getAnnIds(imgIds=img['id'])
anns = coco.loadAnns(ann_ids)
```

Convert CSV to COCO JSON:
```bash
python scripts/convert_to_coco.py --root . --out annotations --category corn --splits train val test
```

Dependencies:
```bash
python -m pip install pillow
```

Optional for the COCO API example:
```bash
python -m pip install pycocotools
```

## Evaluation and baselines

- Metric: Accuracy for classification; report F1 for historical comparison if desired.
- Reference results: See original Plant Village dataset papers for baseline results.

## Datasheet (data card)

- **Motivation**: Corn leaf disease classification to help farmers quickly identify plant diseases to prevent crop loss and ensure food security.
- **Composition**: RGB images of corn leaves; 5 classes (healthy, common_rust, gray_leaf_spot, northern_leaf_blight, background).
- **Collection process**: Field images of corn leaves; part of Plant Village dataset.
- **Preprocessing**: Images standardized to 256×256 pixels; COCO JSON produced by script.
- **Distribution**: Data hosted on Kaggle; this repo provides ancillary scripts and standardized structure.
- **Maintenance**: Community contributions via issue tracker.

## Known issues and caveats

- **Classification task**: This is a classification dataset. Each image has a full-image bounding box annotation indicating its class.
- **Dataset imbalance**: The dataset is imbalanced, with some classes having more samples than others.
- **Incomplete splits**: The provided splits (train/val/test) contain only a subset of all images. Consider regenerating splits to include all images.
- **Missing annotations**: Not all images have corresponding CSV/JSON annotations. Only 16,412 out of 44,096 images have annotations.
- **Coordinates**: Coordinates are in pixel units with origin at the image top-left. Ensure downstream tooling expects absolute COCO boxes.

## License

This dataset is released under the Creative Commons Attribution 4.0 International License (CC BY 4.0). See `LICENSE` for details.

Check the original dataset terms and cite appropriately.

## Citation

If you use this dataset, please cite:

```bibtex
@article{mohanty2016using,
  title={Using deep learning for image-based plant disease detection},
  author={Mohanty, Sharada P and Hughes, David P and Salath{\'e}, Marcel},
  journal={Frontiers in plant science},
  volume={7},
  pages={1419},
  year={2016},
  publisher={Frontiers Media SA}
}
```

## Changelog

- **V1.0.0** (2025): Initial standardized structure and COCO conversion utility

## Contact

- **Maintainers**: Dataset maintainers
- **Original authors**: Sharada P. Mohanty, David P. Hughes, Marcel Salathé
- **Source**: `https://github.com/spMohanty/PlantVillage-Dataset`

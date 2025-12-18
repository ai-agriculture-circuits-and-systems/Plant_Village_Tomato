# Plant Village Tomato

[![DOI](https://img.shields.io/badge/DOI-pending-lightgrey)](#citation)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-blue.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Version](https://img.shields.io/badge/version-1.0.0-blue)](#changelog)

Tomato leaf disease classification dataset from Plant Village. Contains images of tomato leaves labeled for disease classification (10 classes: healthy, bacterial spot, early blight, late blight, leaf mold, septoria leaf spot, spider mites two-spotted spider mite, target spot, tomato mosaic virus, tomato yellow leaf curl virus). This dataset follows the standardized layout specification.

- Project page: `https://www.kaggle.com/datasets/abdallahalidev/plantvillage-dataset`
- Issue tracker: use this repo

## TL;DR
- Task: classification (10 classes: `healthy`, `bacterial_spot`, `early_blight`, `late_blight`, `leaf_mold`, `septoria_leaf_spot`, `spider_mites_two_spotted_spider_mite`, `target_spot`, `tomato_mosaic_virus`, `tomato_yellow_leaf_curl_virus`)
- Modality: RGB
- Platform: handheld/field
- Real/Synthetic: real
- Images: see counts below
- Classes: 10
- Resolution: 256×256 pixels
- Annotations: COCO JSON (object detection with bounding boxes)
- License: CC BY 4.0 (see License)
- Citation: see below

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
- Local license file: see `LICENSE` (Creative Commons Attribution 4.0).

## Dataset structure

This dataset follows the standardized dataset structure specification with subcategory organization:

```
Plant_Village_Tomato/
├── tomatoes/
│   ├── healthy/              # Healthy images
│   │   ├── color/            # 彩色图像变体
│   │   │   ├── csv/          # CSV annotations per image
│   │   │   ├── json/         # Original JSON annotations
│   │   │   ├── images/       # Healthy images
│   │   │   └── sets/         # Dataset splits for this subcategory (optional)
│   │   │       ├── train.txt
│   │   │       ├── val.txt
│   │   │       ├── test.txt
│   │   │       └── all.txt
│   │   ├── grayscale/        # 灰度图像变体
│   │   ├── segmented/        # 分割图像变体
│   │   ├── with_augmentation/
│   │   └── without_augmentation/
│   ├── bacterial_spot/       # Bacterial Spot images
│   ├── early_blight/         # Early Blight images
│   ├── late_blight/          # Late Blight images
│   ├── leaf_mold/            # Leaf Mold images
│   ├── septoria_leaf_spot/   # Septoria Leaf Spot images
│   ├── spider_mites_two_spotted_spider_mite/ # Spider Mites images
│   ├── target_spot/          # Target Spot images
│   ├── tomato_mosaic_virus/  # Tomato Mosaic Virus images
│   ├── tomato_yellow_leaf_curl_virus/ # Yellow Leaf Curl Virus images
│   ├── labelmap.json        # Label mapping
│   └── sets/                 # Combined dataset splits
│       ├── train.txt
│       ├── val.txt
│       ├── test.txt
│       └── all.txt
├── annotations/              # COCO format JSON (generated)
│   ├── tomatoes_color_train.json
│   ├── tomatoes_color_val.json
│   └── tomatoes_color_test.json
├── scripts/
│   └── convert_to_coco.py   # COCO conversion script
├── LICENSE
├── README.md
└── requirements.txt
```

- Splits: `tomatoes/sets/*.txt` list image basenames (no extension). If missing, all images are used.

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
      <img src="tomatoes/healthy/color/images/sample.jpg" alt="healthy" width="260"/>
      <div align="center"><code>tomatoes/healthy/color/images/sample.jpg</code></div>
    </td>
  </tr>
  <tr>
    <td><strong>Bacterial Spot</strong></td>
    <td>
      <img src="tomatoes/bacterial_spot/color/images/sample.jpg" alt="bacterial_spot" width="260"/>
      <div align="center"><code>tomatoes/bacterial_spot/color/images/sample.jpg</code></div>
    </td>
  </tr>
  <!-- Additional rows for other 8 classes omitted for brevity but follow the same pattern -->
</table>

## Annotation schema

### CSV Format

Each image has a corresponding CSV file in `{category}/{variant}/csv/` with the following format:

```csv
#item,x,y,width,height,label
0,0,0,256,256,1
```

- `x, y`: top-left corner coordinates (pixels)
- `width, height`: bounding box dimensions (pixels)
- `label`: category ID (from labelmap.json)

### COCO Format

The COCO JSON files are generated from CSV annotations and follow the standard COCO format:

```json
{
  "info": {...},
  "images": [
    {
      "id": 1,
      "file_name": "tomatoes/healthy/color/images/image.jpg",
      "width": 256,
      "height": 256
    }
  ],
  "annotations": [
    {
      "id": 1,
      "image_id": 1,
      "category_id": 1,
      "bbox": [0, 0, 256, 256],
      "area": 65536,
      "iscrowd": 0
    }
  ],
  "categories": [
    {
      "id": 1,
      "name": "healthy",
      "supercategory": "plant"
    }
  ]
}
```

### Label Maps

Label mappings are defined in `tomatoes/labelmap.json`:

```json
[
  {
    "object_id": 0,
    "label_id": 0,
    "keyboard_shortcut": "0",
    "object_name": "background"
  },
  {
    "object_id": 1,
    "label_id": 1,
    "keyboard_shortcut": "1",
    "object_name": "bacterial_spot"
  },
  ...
]
```

## Stats and splits

Dataset statistics and split information:

- **Total images**: 18,160 original images across 10 classes.
- **Splits**: train/val/test (default: 70%/15%/15%)
- **Splits provided via** `tomatoes/sets/*.txt`. You may define your own splits by editing those files.

## Quick start

### Convert to COCO format

```bash
python scripts/convert_to_coco.py --root . --out annotations --splits train val test
```

### Load with COCO API

```python
from pycocotools.coco import COCO
import matplotlib.pyplot as plt

# Load annotations
coco = COCO('annotations/tomatoes_color_train.json')

# Get image IDs
img_ids = coco.getImgIds()
print(f"Total images: {len(img_ids)}")

# Get category IDs
cat_ids = coco.getCatIds()
print(f"Categories: {[coco.loadCats(cat_id)[0]['name'] for cat_id in cat_ids]}")
```

### Dependencies

- **Required**: Pillow (for image processing)
- **Optional**: pycocotools (for COCO API)

## Evaluation and baselines

- **Metrics**: Classification accuracy, mAP (if used for detection)
- **Baselines**: See original Plant Village paper

## Datasheet (data card)

### Motivation

This dataset was created to enable automated plant disease detection and classification using computer vision techniques.

### Composition

- **Image types**: RGB images of plant leaves
- **Classes**: 10 classes
- **Resolution**: 256×256 pixels
- **Format**: JPG/PNG

### Collection process

Images were collected from various sources and manually labeled by experts.

### Preprocessing

- Images resized to 256×256 pixels
- Annotations converted to bounding box format
- Dataset split into train/val/test sets

### Distribution

Dataset is available under CC BY 4.0 license.

### Maintenance

This standardized version is maintained by the dataset organization team.

## Known issues and caveats

- Images are preprocessed to 256×256 pixels
- coordinate system: top-left origin (0,0), pixel units
- File naming: UUID-based names are used to maintain uniqueness.

## License

This dataset is released under the Creative Commons Attribution 4.0 International License (CC BY 4.0).

Check the original dataset terms and cite appropriately.

See `LICENSE` file for full license text.

## Citation

If you use this dataset, please cite:

```bibtex
@article{mohanty2016using,
  title={Using Deep Learning for Image-Based Plant Disease Detection},
  author={Mohanty, Sharada P. and Hughes, David P. and Salathé, Marcel},
  journal={Frontiers in Plant Science},
  volume={7},
  pages={1419},
  year={2016},
  publisher={Frontiers Media SA}
}
```

## Changelog

- **V1.0.0**: initial standardized structure and COCO conversion utility

## Contact

- **Maintainers**: Dataset organization team
- **Original authors**: Plant Village team
- **Source**: `https://www.kaggle.com/datasets/abdallahalidev/plantvillage-dataset`

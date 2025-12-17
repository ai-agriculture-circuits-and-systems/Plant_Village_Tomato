#!/usr/bin/env python3
"""
重组 Plant Village Corn 数据集为标准结构
根据标准化数据集结构规范进行优化
"""

import os
import json
import shutil
from pathlib import Path
from collections import defaultdict

# 类别映射：从原始目录名到标准子类别名
CATEGORY_MAPPING = {
    "Corn___healthy": "healthy",
    "Corn___Common_rust": "common_rust",
    "Corn___Cercospora_leaf_spot Gray_leaf_spot": "gray_leaf_spot",
    "Corn___Northern_Leaf_Blight": "northern_leaf_blight",
    "Background_without_leaves": "background"
}

# 标准类别目录
CATEGORY_DIR = "corn"
ROOT_DIR = Path(__file__).parent.parent


def get_image_files(source_dir):
    """获取所有图像文件"""
    image_files = []
    for ext in ['*.jpg', '*.JPG', '*.png', '*.PNG']:
        image_files.extend(source_dir.rglob(ext))
    return image_files


def get_json_files(source_dir):
    """获取所有 JSON 标注文件"""
    return list(source_dir.rglob("*.json"))


def normalize_filename(filename):
    """规范化文件名，移除特殊字符"""
    # 移除空格和特殊字符，保留字母数字、下划线和连字符
    base = Path(filename).stem
    ext = Path(filename).suffix.lower()
    # 将空格替换为下划线
    base = base.replace(' ', '_').replace('(', '').replace(')', '')
    return f"{base}{ext}"


def read_json_annotation(json_path):
    """读取 JSON 标注文件"""
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error reading {json_path}: {e}")
        return None


def create_csv_from_json(json_data, csv_path):
    """从 JSON 数据创建 CSV 标注文件（分类任务使用全图像边界框）"""
    if not json_data or 'images' not in json_data or len(json_data['images']) == 0:
        return False
    
    image_info = json_data['images'][0]
    width = image_info.get('width', 256)
    height = image_info.get('height', 256)
    
    # 获取类别ID
    category_id = 0
    if 'categories' in json_data and len(json_data['categories']) > 0:
        category_id = json_data['categories'][0].get('id', 0)
        # 将大整数ID映射到标准ID（1-5）
        category_name = json_data['categories'][0].get('name', '').lower()
        if category_name == 'healthy':
            category_id = 1
        elif category_name == 'common_rust' or category_name == 'rust':
            category_id = 2
        elif category_name == 'gray_leaf_spot' or 'leaf_spot' in category_name:
            category_id = 3
        elif 'blight' in category_name.lower():
            category_id = 4
        elif category_name == 'background':
            category_id = 0
    
    # 检查是否有标注
    has_annotations = 'annotations' in json_data and len(json_data['annotations']) > 0
    
    # 对于分类任务，如果没有标注，创建全图像边界框
    if not has_annotations and category_id > 0:
        # 全图像边界框：[0, 0, width, height]
        bbox = [0, 0, width, height]
    elif has_annotations:
        # 使用第一个标注的边界框
        bbox = json_data['annotations'][0].get('bbox', [0, 0, width, height])
    else:
        return False
    
    # 写入 CSV 文件
    with open(csv_path, 'w', encoding='utf-8') as f:
        f.write("#item,x,y,width,height,label\n")
        f.write(f"0,{bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]},{category_id}\n")
    
    return True


def reorganize_dataset():
    """重组数据集"""
    print("开始重组数据集...")
    
    # 创建标准目录结构
    images_dir = ROOT_DIR / CATEGORY_DIR / "images"
    json_dir = ROOT_DIR / CATEGORY_DIR / "json"
    csv_dir = ROOT_DIR / CATEGORY_DIR / "csv"
    sets_dir = ROOT_DIR / CATEGORY_DIR / "sets"
    
    images_dir.mkdir(parents=True, exist_ok=True)
    json_dir.mkdir(parents=True, exist_ok=True)
    csv_dir.mkdir(parents=True, exist_ok=True)
    sets_dir.mkdir(parents=True, exist_ok=True)
    
    # 统计信息
    stats = defaultdict(int)
    image_mapping = {}  # 原始路径 -> 新路径
    all_images = set()
    
    # 处理每个类别
    for orig_dir_name, subcategory in CATEGORY_MAPPING.items():
        orig_dir = ROOT_DIR / orig_dir_name
        if not orig_dir.exists():
            print(f"警告: 目录不存在: {orig_dir}")
            continue
        
        print(f"\n处理类别: {orig_dir_name} -> {subcategory}")
        
        # 获取所有图像文件
        image_files = get_image_files(orig_dir)
        print(f"  找到 {len(image_files)} 个图像文件")
        
        # 获取所有 JSON 文件
        json_files = get_json_files(orig_dir)
        print(f"  找到 {len(json_files)} 个 JSON 文件")
        
        # 创建 JSON 文件映射（文件名 -> 路径）
        json_map = {}
        for json_file in json_files:
            stem = json_file.stem
            # 移除可能的后缀（如 _1）
            base_stem = stem.split('_')[0] if '_' in stem else stem
            json_map[base_stem] = json_file
        
        # 处理图像文件
        for img_file in image_files:
            # 规范化文件名
            normalized_name = normalize_filename(img_file.name)
            new_img_path = images_dir / normalized_name
            
            # 如果文件已存在，添加前缀避免冲突
            counter = 1
            while new_img_path.exists():
                stem = Path(normalized_name).stem
                ext = Path(normalized_name).suffix
                new_img_path = images_dir / f"{stem}_{counter}{ext}"
                counter += 1
            
            # 复制图像文件
            shutil.copy2(img_file, new_img_path)
            stats[f"{subcategory}_images"] += 1
            
            # 记录映射
            img_stem = new_img_path.stem
            image_mapping[img_stem] = {
                'original': str(img_file),
                'new': str(new_img_path),
                'subcategory': subcategory
            }
            all_images.add(img_stem)
            
            # 查找对应的 JSON 文件
            img_stem_orig = img_file.stem
            json_file = None
            
            # 尝试多种匹配方式
            for key in [img_stem_orig, img_stem_orig.split('_')[0], img_stem_orig.replace('_', ' ')]:
                if key in json_map:
                    json_file = json_map[key]
                    break
            
            if json_file and json_file.exists():
                # 复制 JSON 文件
                new_json_path = json_dir / f"{img_stem}.json"
                shutil.copy2(json_file, new_json_path)
                
                # 读取 JSON 并创建 CSV
                json_data = read_json_annotation(json_file)
                if json_data:
                    csv_path = csv_dir / f"{img_stem}.csv"
                    if create_csv_from_json(json_data, csv_path):
                        stats[f"{subcategory}_annotations"] += 1
            else:
                # 如果没有 JSON 文件，尝试从图像推断类别并创建标注
                # 这里可以根据需要实现自动标注逻辑
                pass
    
    print(f"\n重组完成!")
    print(f"总计图像: {len(all_images)}")
    for key, value in sorted(stats.items()):
        print(f"  {key}: {value}")
    
    return all_images, image_mapping


def create_labelmap():
    """创建 labelmap.json 文件"""
    labelmap = [
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
            "object_name": "healthy"
        },
        {
            "object_id": 2,
            "label_id": 2,
            "keyboard_shortcut": "2",
            "object_name": "common_rust"
        },
        {
            "object_id": 3,
            "label_id": 3,
            "keyboard_shortcut": "3",
            "object_name": "gray_leaf_spot"
        },
        {
            "object_id": 4,
            "label_id": 4,
            "keyboard_shortcut": "4",
            "object_name": "northern_leaf_blight"
        }
    ]
    
    labelmap_path = ROOT_DIR / CATEGORY_DIR / "labelmap.json"
    with open(labelmap_path, 'w', encoding='utf-8') as f:
        json.dump(labelmap, f, indent=2, ensure_ascii=False)
    
    print(f"创建 labelmap.json: {labelmap_path}")


def create_splits(all_images, image_mapping):
    """创建数据集划分文件"""
    # 读取原始划分文件
    all_dir = ROOT_DIR / "all"
    train_file = all_dir / "train.txt"
    val_file = all_dir / "val.txt"
    test_file = all_dir / "test.txt"
    
    # 读取原始划分（包含扩展名的完整文件名）
    train_images = set()
    val_images = set()
    test_images = set()
    
    if train_file.exists():
        with open(train_file, 'r', encoding='utf-8') as f:
            for line in f:
                name = line.strip()
                # 移除扩展名
                stem = Path(name).stem
                train_images.add(stem)
    
    if val_file.exists():
        with open(val_file, 'r', encoding='utf-8') as f:
            for line in f:
                name = line.strip()
                stem = Path(name).stem
                val_images.add(stem)
    
    if test_file.exists():
        with open(test_file, 'r', encoding='utf-8') as f:
            for line in f:
                name = line.strip()
                stem = Path(name).stem
                test_images.add(stem)
    
    # 映射到新的文件名
    def map_to_new_name(old_stem):
        # 尝试直接匹配
        if old_stem in image_mapping:
            return image_mapping[old_stem]['new']
        # 尝试规范化匹配
        normalized = normalize_filename(old_stem)
        normalized_stem = Path(normalized).stem
        for key, value in image_mapping.items():
            if key == normalized_stem or key.startswith(normalized_stem):
                return Path(value['new']).stem
        return None
    
    # 创建新的划分文件
    sets_dir = ROOT_DIR / CATEGORY_DIR / "sets"
    
    # 训练集
    train_new = set()
    for old_stem in train_images:
        new_stem = map_to_new_name(old_stem)
        if new_stem:
            train_new.add(new_stem)
        else:
            # 如果找不到映射，尝试直接使用（可能文件名已规范化）
            normalized = normalize_filename(old_stem)
            new_stem = Path(normalized).stem
            if new_stem in all_images:
                train_new.add(new_stem)
    
    # 验证集
    val_new = set()
    for old_stem in val_images:
        new_stem = map_to_new_name(old_stem)
        if new_stem:
            val_new.add(new_stem)
        else:
            normalized = normalize_filename(old_stem)
            new_stem = Path(normalized).stem
            if new_stem in all_images:
                val_new.add(new_stem)
    
    # 测试集
    test_new = set()
    for old_stem in test_images:
        new_stem = map_to_new_name(old_stem)
        if new_stem:
            test_new.add(new_stem)
        else:
            normalized = normalize_filename(old_stem)
            new_stem = Path(normalized).stem
            if new_stem in all_images:
                test_new.add(new_stem)
    
    # 写入划分文件（不含扩展名）
    def write_split_file(filename, image_set):
        filepath = sets_dir / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            for img_stem in sorted(image_set):
                f.write(f"{img_stem}\n")
        print(f"创建划分文件: {filepath} ({len(image_set)} 个图像)")
    
    write_split_file("train.txt", train_new)
    write_split_file("val.txt", val_new)
    write_split_file("test.txt", test_new)
    
    # 创建 all.txt
    write_split_file("all.txt", all_images)
    
    # 创建 train_val.txt
    train_val = train_new | val_new
    write_split_file("train_val.txt", train_val)
    
    print(f"\n划分统计:")
    print(f"  训练集: {len(train_new)}")
    print(f"  验证集: {len(val_new)}")
    print(f"  测试集: {len(test_new)}")
    print(f"  总计: {len(all_images)}")


if __name__ == "__main__":
    print("=" * 60)
    print("Plant Village Corn 数据集重组脚本")
    print("=" * 60)
    
    # 重组数据集
    all_images, image_mapping = reorganize_dataset()
    
    # 创建 labelmap.json
    create_labelmap()
    
    # 创建划分文件
    create_splits(all_images, image_mapping)
    
    print("\n重组完成！")

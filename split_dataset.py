import os
import random
import shutil
from pathlib import Path
import argparse

def split_dataset_from_labels(dataset_path, train_ratio=0.9):
    """
    从rawimg文件夹获取图片，按指定比例划分训练集和验证集，
    标签文件从txt文件夹获取
    
    参数:
        dataset_path: 数据集路径
        train_ratio: 训练集比例，默认为0.5
    """
    # 确保路径存在
    dataset_path = Path(dataset_path)
    rawimg_path = dataset_path / 'rawimg'  # 原始图像在rawimg文件夹
    txt_path = dataset_path / 'txt'  # 标签文件存放在txt文件夹
    
    if not rawimg_path.exists():
        raise FileNotFoundError(f"找不到图像文件夹: {rawimg_path}")
    
    if not txt_path.exists():
        raise FileNotFoundError(f"找不到标签文件夹: {txt_path}")
    
    # 获取rawimg文件夹中的图像文件
    image_files = [f for f in os.listdir(rawimg_path) if f.endswith(('.jpg', '.jpeg', '.png', '.bmp'))]
    
    if not image_files:
        raise FileNotFoundError(f"在rawimg文件夹中未找到图像文件")
    
    # 随机打乱文件列表
    random.shuffle(image_files)
    
    # 按比例划分
    split_index = int(len(image_files) * train_ratio)
    train_images = image_files[:split_index]
    val_images = image_files[split_index:]
    
    print(f"总图像数: {len(image_files)}")
    print(f"训练集图像数: {len(train_images)}")
    print(f"验证集图像数: {len(val_images)}")
    
    # 创建目标目录结构
    images_path = dataset_path / 'images'
    labels_path = dataset_path / 'labels'  # 修改为正确的标签目标路径
    
    image_train_dir = images_path / 'train'
    image_val_dir = images_path / 'val'
    label_train_dir = labels_path / 'train'  # 修改为正确的标签训练集路径
    label_val_dir = labels_path / 'val'  # 修改为正确的标签验证集路径
    
    for directory in [images_path, image_train_dir, image_val_dir, labels_path, label_train_dir, label_val_dir]:
        os.makedirs(directory, exist_ok=True)
    
    # 移动训练集文件
    for img_file in train_images:
        # 移动图像
        src_img = rawimg_path / img_file
        dst_img = image_train_dir / img_file
        shutil.copy(src_img, dst_img)
        print(f"复制图像: {src_img} -> {dst_img}")
        
        # 检查是否有对应的标签文件 (.txt)，从txt文件夹获取
        label_name = Path(img_file).stem + '.txt'
        src_label = txt_path / label_name  # 从txt文件夹获取标签
        if src_label.exists():
            dst_label = label_train_dir / label_name
            shutil.copy(src_label, dst_label)
            print(f"复制标签: {src_label} -> {dst_label}")
    
    # 移动验证集文件
    for img_file in val_images:
        # 移动图像
        src_img = rawimg_path / img_file
        dst_img = image_val_dir / img_file
        shutil.copy(src_img, dst_img)
        print(f"复制图像: {src_img} -> {dst_img}")
        
        # 检查是否有对应的标签文件 (.txt)，从txt文件夹获取
        label_name = Path(img_file).stem + '.txt'
        src_label = txt_path / label_name  # 从txt文件夹获取标签
        if src_label.exists():
            dst_label = label_val_dir / label_name
            shutil.copy(src_label, dst_label)
            print(f"复制标签: {src_label} -> {dst_label}")
    
    print("\n数据集划分完成:")
    print(f"训练集图像: {image_train_dir} ({len(train_images)}张)")
    print(f"验证集图像: {image_val_dir} ({len(val_images)}张)")
    print(f"训练集标签: {label_train_dir}")
    print(f"验证集标签: {label_val_dir}")

if __name__ == "__main__":
    # 路径应该放在引号中，并使用正斜杠或双反斜杠
    split_dataset_from_labels("D:/Github/Me/datasets", 0.9)
    
    # 或者使用原始字符串标记
    # split_dataset_from_labels(r"D:\Github\Me\datasets", 0.9)

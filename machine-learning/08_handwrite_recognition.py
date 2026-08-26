"""
08_handwrite_recognition.py - Handwriting Character Recognition (CNN)
=========================================================
基于 PyTorch 实现的手写字符分类，包括字符识别模型构建、训练、评估和推理。

这是一个完整的端到端手写字符识别系统，支持:
  - 自定义手写字符数据集
  - 预训练模型微调 (迁移学习)
  - 字符预测和可视化结果
  - 模型保存与加载

用法:
  python3 08_handwrite_recognition.py train <data_dir> <num_classes>
  # 训练新模型
  
  python3 08_handwrite_recognition.py infer --model model.pth --image image.png
  # 加载模型进行推理
"""

import os
import sys
import argparse
import time
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader, random_split, TensorDataset
from torchvision import transforms
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import numpy as np
import random
import json

# ---------------------------------------------------------------------------
# 1. Configuration and Constants
# ---------------------------------------------------------------------------

# Device configuration
DEVICE = torch.device("cuda" if torch.cuda.is_available() else 
                      "mps" if torch.backends.mps.is_available() else 
                      "cpu")

# Default hyperparameters
DEFAULT_CONFIG = {
    'batch_size': 32,
    'learning_rate': 0.001,
    'num_epochs': 20,
    'image_size': 64,
    'hidden_dim': 128,
    'num_workers': 4,
    'model_save_dir': './handwrite_models',
    'export_dir': './handwrite_outputs',
}

# Handwriting character classes (example: A-Z, 0-9)
DEFAULT_CLASSES = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                   'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
                   'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                   'U', 'V', 'W', 'X', 'Y', 'Z']

# ---------------------------------------------------------------------------
# 2. Utility Functions
# ---------------------------------------------------------------------------

def setup_seed(seed=42):
    """固定随机种子以确保可重复性"""
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    np.random.seed(seed)
    random.seed(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

def create_directories():
    """创建必要的目录"""
    for dir_path in [DEFAULT_CONFIG['model_save_dir'], 
                     DEFAULT_CONFIG['export_dir']]:
        os.makedirs(dir_path, exist_ok=True)

def save_config(config, path):
    """保存训练配置"""
    with open(path, 'w') as f:
        json.dump(config, f, indent=4)

def load_config(path):
    """加载训练配置"""
    with open(path, 'r') as f:
        return json.load(f)

# ---------------------------------------------------------------------------
# 3. Dataset Class
# ---------------------------------------------------------------------------

class HandwriteDataset(Dataset):
    """
    Handwriting Character Dataset Class

    This dataset generates synthetic handwriting characters for training.
    """

    def __init__(self, root_dir, num_classes, transform=None):
        self.root_dir = root_dir
        self.num_classes = num_classes
        self.transform = transform

        # 加载所有类别信息
        self.class_to_idx = {class_name: idx for idx, class_name in enumerate(DEFAULT_CLASSES[:num_classes])}
        self.idx_to_class = {idx: class_name for class_name, idx in self.class_to_idx.items()}

        # 存储每个类别的图像和标签
        self.images = []
        self.labels = []

        print(f"\n📊 Loading handwriting character dataset...")
        self._load_dataset()
        print(f"   ✅ Loading complete: total {len(self.images)} samples")

    def _load_dataset(self):
        """加载数据集"""
        # 检查是否有有效的图像文件
        if not os.path.exists(self.root_dir) or not os.listdir(self.root_dir):
            print(f"   ℹ️ 未找到数据集目录 '{self.root_dir}'，正在生成合成数据...")
            self._generate_synthetic_dataset()
            return

        # 遍历所有子目录 (每个类别一个目录)
        for class_name in sorted(os.listdir(self.root_dir)):
            class_dir = os.path.join(self.root_dir, class_name)
            if not os.path.isdir(class_dir):
                continue

            # 检查是否有有效的图像文件
            has_images = False
            for filename in os.listdir(class_dir):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                    img_path = os.path.join(class_dir, filename)
                    try:
                        self.images.append(img_path)
                        self.labels.append(self.class_to_idx[class_name])
                        has_images = True
                    except Exception as e:
                        print(f"   ⚠️ Loading {img_path} failed: {e}")

            if not has_images:
                print(f"   ⚠️ Class '{class_name}' has no valid image files")

    def _generate_synthetic_dataset(self):
        """生成合成手写字符数据集"""
        print(f"   🎨 Generating synthetic handwriting characters...")

        for class_idx, class_name in enumerate(self.class_to_idx.keys()):
            class_dir = os.path.join(self.root_dir, class_name)
            os.makedirs(class_dir, exist_ok=True)

            # 生成每个类别的图像
            num_samples = 100  # 每个类别 100 个样本

            for i in range(num_samples):
                # 创建一个随机形状的图像
                img_size = DEFAULT_CONFIG['image_size']
                img = Image.new('RGB', (img_size, img_size), color=(255, 255, 255))
                draw = ImageDraw.Draw(img)

                # 绘制手写风格的字符
                if class_idx < 10:  # 数字
                    self._draw_digit(draw, img_size, class_idx)
                else:  # 字母
                    self._draw_letter(draw, img_size, class_name)

                # 保存图像
                filename = f"{class_name}_{i:03d}.png"
                img_path = os.path.join(class_dir, filename)
                img.save(img_path)

                # 添加到数据集
                self.images.append(img_path)
                self.labels.append(class_idx)

        print(f"   ✅ Generated {len(self.images)} synthetic samples")

    def _draw_digit(self, draw, img_size, digit):
        """绘制数字"""
        scale = img_size // 8
        offset = scale

        # 根据数字绘制简单的形状
        if digit == 0:
            draw.rectangle([offset, offset, offset*6, offset*6], outline='black', width=2)
            draw.rectangle([offset*7, offset, offset*7, offset*6], outline='black', width=2)
            draw.rectangle([offset*7, offset*7, offset*7, offset*7], outline='black', width=2)

        elif digit == 1:
            draw.line([offset*4, offset, offset*4, offset*6], fill='black', width=2)

        elif digit == 2:
            draw.rectangle([offset, offset, offset*4, offset*3], outline='black', width=2)
            draw.line([offset*4, offset*3, offset*6, offset*6], fill='black', width=2)

        elif digit == 3:
            draw.rectangle([offset, offset, offset*6, offset*4], outline='black', width=2)
            draw.line([offset*4, offset*4, offset*6, offset*5], fill='black', width=2)

        elif digit == 4:
            draw.line([offset*3, offset, offset*3, offset*6], fill='black', width=2)
            draw.rectangle([offset, offset*3, offset*6, offset*6], outline='black', width=2)

        elif digit == 5:
            draw.rectangle([offset*6, offset, offset*6, offset*4], outline='black', width=2)
            draw.rectangle([offset, offset*3, offset*6, offset*4], outline='black', width=2)
            draw.line([offset, offset*4, offset*4, offset*6], fill='black', width=2)

        elif digit == 6:
            draw.rectangle([offset, offset, offset*6, offset*4], outline='black', width=2)
            draw.line([offset, offset*4, offset*4, offset*6], fill='black', width=2)

        elif digit == 7:
            draw.line([offset, offset, offset*6, offset], fill='black', width=2)
            draw.line([offset*4, offset, offset*4, offset*6], fill='black', width=2)

        elif digit == 8:
            draw.rectangle([offset, offset, offset*6, offset*6], outline='black', width=2)
            draw.rectangle([offset*2, offset*2, offset*4, offset*4], fill='white', outline='black')

        elif digit == 9:
            draw.rectangle([offset, offset, offset*6, offset*6], outline='black', width=2)
            draw.line([offset*4, offset, offset*2, offset*2], fill='black', width=2)

    def _draw_letter(self, draw, img_size, letter):
        """绘制字母"""
        scale = img_size // 8
        offset = scale

        if letter == 'A':
            draw.rectangle([offset, offset, offset*6, offset*6], outline='black', width=2)
            draw.line([offset, offset*3, offset*3, offset], fill='black', width=2)
            draw.line([offset*3, offset, offset*6, offset*3], fill='black', width=2)
        elif letter == 'B':
            draw.rectangle([offset, offset, offset*3, offset*6], outline='black', width=2)
            draw.ellipse([offset*3, offset, offset*5, offset*3], outline='black', width=2)
            draw.rectangle([offset*3, offset*3, offset*5, offset*6], outline='black', width=2)
        elif letter == 'C':
            draw.arc([offset, offset, offset*6, offset*6], start=180, end=360, fill='black', width=2)

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):
        img_path = self.images[idx]
        label = self.labels[idx]

        # 加载图像
        try:
            image = Image.open(img_path).convert('RGB')
        except Exception as e:
            print(f"   ⚠️ Loading {img_path} failed: {e}")
            # 生成一个空白图像作为备用
            image = Image.new('RGB', (DEFAULT_CONFIG['image_size'], DEFAULT_CONFIG['image_size']))

        # 应用变换
        if self.transform:
            image = self.transform(image)

        return image, torch.tensor(label, dtype=torch.long)

# ---------------------------------------------------------------------------
# 4. Model Definition
# ---------------------------------------------------------------------------

class HandwriteCNN(nn.Module):
    """
    Handwriting Character Recognition CNN Model

    Network structure:
      - 卷积层 + 批量归一化 + ReLU
      - 最大池化
      - 多次重复这种模式
      - 展平
      - 全连接层 + Dropout
      - 输出层
    """

    def __init__(self, num_classes):
        super().__init__()
        self.num_classes = num_classes

        # 特征提取
        self.features = nn.Sequential(
            # 第 1 块
            nn.Conv2d(3, 32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),

            # 第 2 块
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),

            # 第 3 块
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),

            # 第 4 块
            nn.Conv2d(128, 256, kernel_size=3, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),
        )

        # 分类器
        self.classifier = nn.Sequential(
            nn.Dropout(0.5),
            nn.Linear(256 * 4 * 4, 512),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(512, num_classes),
        )

    def forward(self, x):
        x = self.features(x)
        x = x.view(x.size(0), -1)
        x = self.classifier(x)
        return x

# ---------------------------------------------------------------------------
# 5. Data Preprocessing
# ---------------------------------------------------------------------------

# 训练图像变换
def get_train_transform(image_size=DEFAULT_CONFIG['image_size']):
    return transforms.Compose([
        transforms.Resize((image_size, image_size)),
        transforms.RandomHorizontalFlip(),
        transforms.RandomRotation(15),
        transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

# 测试图像变换
def get_test_transform(image_size=DEFAULT_CONFIG['image_size']):
    return transforms.Compose([
        transforms.Resize((image_size, image_size)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

# ---------------------------------------------------------------------------
# 6. Training Functions
# ---------------------------------------------------------------------------

def train_model(model, train_loader, criterion, optimizer, epoch, log_interval=10):
    """训练单个 epoch"""
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0

    for batch_idx, (inputs, labels) in enumerate(train_loader):
        inputs, labels = inputs.to(DEVICE), labels.to(DEVICE)

        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)

        loss.backward()
        optimizer.step()

        running_loss += loss.item()
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

        if batch_idx % log_interval == 0:
            print(f"       Batch {batch_idx:3d}/{len(train_loader):3d} | "
                  f"Loss: {loss.item():.4f} | "
                  f"Acc: {100.0 * correct / total:.1f}%")

    avg_loss = running_loss / len(train_loader)
    accuracy = 100.0 * correct / total

    return avg_loss, accuracy


def evaluate_model(model, test_loader, criterion):
    """评估模型"""
    model.eval()
    test_loss = 0.0
    correct = 0
    total = 0

    with torch.no_grad():
        for inputs, labels in test_loader:
            inputs, labels = inputs.to(DEVICE), labels.to(DEVICE)

            outputs = model(inputs)
            loss = criterion(outputs, labels)

            test_loss += loss.item()
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    avg_loss = test_loss / len(test_loader)
    accuracy = 100.0 * correct / total

    return avg_loss, accuracy

# ---------------------------------------------------------------------------
# 7. Visualization Functions
# ---------------------------------------------------------------------------

def visualize_prediction(model, image, true_label, idx_to_class, save_path=None):
    """可视化单个预测结果"""
    model.eval()

    with torch.no_grad():
        image_tensor = image.unsqueeze(0).to(DEVICE)
        output = model(image_tensor)
        probabilities = torch.softmax(output, dim=1)
        predicted_class = torch.argmax(probabilities, dim=1).item()

        probs = probabilities[0].cpu().numpy()
        predicted_class_name = idx_to_class[predicted_class]
        true_class_name = idx_to_class[true_label.item()]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    img_display = image.cpu().permute(1, 2, 0)
    mean = torch.tensor([0.485, 0.456, 0.406])
    std = torch.tensor([0.229, 0.224, 0.225])
    img_display = (img_display * std + mean).clamp(0, 1)
    ax1.imshow(img_display)
    ax1.set_title(f'Predicted: {predicted_class_name}\nTrue: {true_class_name}')
    ax1.axis('off')

    bars = ax2.bar(range(len(probs)), probs, color='skyblue')
    bars[predicted_class].set_color('red')
    ax2.set_xticks(range(len(probs)))
    ax2.set_xticklabels([idx_to_class[i] for i in range(len(probs))], rotation=45)
    ax2.set_ylabel('Probability')
    ax2.set_title('Class Probabilities')
    ax2.set_ylim(0, 1)

    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax2.text(i, height + 0.01, f'{height:.2f}', ha='center', va='bottom')

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"   💾 保存预测结果到: {save_path}")

    plt.close()

# ---------------------------------------------------------------------------
# 8. Training and Inference Functions
# ---------------------------------------------------------------------------

def train_handwrite_model(data_dir, num_classes, config=DEFAULT_CONFIG):
    """训练手写字符识别模型"""
    print("=" * 80)
    print("  🎯 Handwriting Character Recognition Model Training")
    print("=" * 80)

    setup_seed(42)

    create_directories()

    train_transform = get_train_transform(config['image_size'])
    test_transform = get_test_transform(config['image_size'])

    full_dataset = HandwriteDataset(data_dir, num_classes, transform=train_transform)

    train_size = int(0.8 * len(full_dataset))
    test_size = len(full_dataset) - train_size
    train_dataset, test_dataset = random_split(full_dataset, [train_size, test_size])

    # 为测试集创建新的 TensorDataset
    test_images = []
    test_labels = []
    for idx in test_dataset.indices:
        img_path = full_dataset.images[idx]
        label = full_dataset.labels[idx]
        image = Image.open(img_path).convert('RGB')
        image = test_transform(image)
        test_images.append(image)
        test_labels.append(label)

    test_images = torch.stack(test_images)
    test_labels = torch.tensor(test_labels)
    test_dataset = TensorDataset(test_images, test_labels)

    train_loader = DataLoader(
        train_dataset,
        batch_size=config['batch_size'],
        shuffle=True,
        num_workers=config['num_workers'],
        pin_memory=True if DEVICE.type == 'cuda' else False
    )
    test_loader = DataLoader(
        test_dataset,
        batch_size=config['batch_size'],
        shuffle=False,
        num_workers=config['num_workers'],
        pin_memory=True if DEVICE.type == 'cuda' else False
    )

    model = HandwriteCNN(num_classes).to(DEVICE)
    print(f"   📋 Model architecture:\n{model}")

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=config['learning_rate'])

    best_accuracy = 0.0
    best_model_path = os.path.join(config['model_save_dir'], 'best_model.pth')
    config_path = os.path.join(config['model_save_dir'], 'config.json')

    print(f"   🚀 Starting training...")
    print(f"      Epochs: {config['num_epochs']}, Batch size: {config['batch_size']}, "
          f"Learning rate: {config['learning_rate']}")
    print(f"      Device: {DEVICE}")
    print(f"      Training samples: {len(train_dataset)}, Test samples: {len(test_dataset)}")

    for epoch in range(1, config['num_epochs'] + 1):
        start_time = time.time()

        train_loss, train_acc = train_model(model, train_loader, criterion, optimizer, epoch)

        test_loss, test_acc = evaluate_model(model, test_loader, criterion)

        if test_acc > best_accuracy:
            best_accuracy = test_acc
            torch.save({
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'test_loss': test_loss,
                'test_accuracy': test_acc,
                'config': config,
                'class_to_idx': full_dataset.class_to_idx,
            }, best_model_path)
            print(f"       ✅ Saving best model (accuracy: {test_acc:.1f}%)")

        epoch_time = time.time() - start_time
        print(f"      Epoch {epoch:3d}/{config['num_epochs']} | "
              f"Training Loss: {train_loss:.4f} | Training Accuracy: {train_acc:.1f}% | "
              f"Test Loss: {test_loss:.4f} | Test Accuracy: {test_acc:.1f}% | "
              f"Time: {epoch_time:.1f}s")

    checkpoint = torch.load(best_model_path, map_location=DEVICE)
    model.load_state_dict(checkpoint['model_state_dict'])
    final_test_loss, final_test_acc = evaluate_model(model, test_loader, criterion)

    print(f"\n   🎉 Training completed!")
    print(f"      Best test accuracy: {best_accuracy:.1f}%")
    print(f"      Final test accuracy: {final_test_acc:.1f}%")

    save_config(config, config_path)

    return model, config


def load_and_predict(model_path, data_dir, num_classes, config_path=None, image_path=None):
    """加载训练好的模型并进行预测"""
    print("=" * 80)
    print("  🔍 Handwriting Character Recognition Inference")
    print("=" * 80)

    if config_path and os.path.exists(config_path):
        config = load_config(config_path)
    else:
        config = DEFAULT_CONFIG

    model = HandwriteCNN(num_classes).to(DEVICE)

    if os.path.exists(model_path):
        checkpoint = torch.load(model_path, map_location=DEVICE)
        model.load_state_dict(checkpoint['model_state_dict'])
        idx_to_class = {v: k for k, v in checkpoint.get('class_to_idx', {}).items()}
        print(f"   ✅ Loading model: {model_path}")
        if 'epoch' in checkpoint:
            print(f"      Training epoch: {checkpoint['epoch']}")
    else:
        print(f"   ❌ Model file not found: {model_path}")
        return None

    model.eval()

    transform = get_test_transform(config['image_size'])

    if image_path and os.path.exists(image_path):
        print(f"\n  📸 Processing image: {image_path}")

        image = Image.open(image_path).convert('RGB')
        image_tensor = transform(image).unsqueeze(0).to(DEVICE)

        with torch.no_grad():
            output = model(image_tensor)
            probabilities = torch.softmax(output, dim=1)
            predicted_class = torch.argmax(probabilities, dim=1).item()
            confidence = probabilities[0][predicted_class].item()

            idx_to_class = {i: DEFAULT_CLASSES[i] for i in range(len(DEFAULT_CLASSES))}
            predicted_char = idx_to_class[predicted_class]

            print(f"   🎯 Prediction results:")
            print(f"      Predicted character: {predicted_char}")
            print(f"      Confidence: {confidence:.2%}")
            print(f"      Probability distribution:")
            for i, prob in enumerate(probabilities[0].cpu().numpy()):
                print(f"        {idx_to_class[i]}: {prob:.2%}")

        return predicted_char, confidence

    else:
        print(f"\n  📊 Loading test set for batch prediction...")

        test_dataset = HandwriteDataset(data_dir, num_classes, transform=transform)
        test_loader = DataLoader(
            test_dataset,
            batch_size=config['batch_size'],
            shuffle=False,
            num_workers=config['num_workers'],
            pin_memory=True if DEVICE.type == 'cuda' else False
        )

        correct = 0
        total = 0
        visualizations_dir = os.path.join(
            config['export_dir'], 
            f"predictions_{int(time.time())}"
        )
        os.makedirs(visualizations_dir, exist_ok=True)

        with torch.no_grad():
            for i, (inputs, labels) in enumerate(test_loader):
                inputs, labels = inputs.to(DEVICE), labels.to(DEVICE)

                outputs = model(inputs)
                probabilities = torch.softmax(outputs, dim=1)
                _, predicted = torch.max(outputs.data, 1)

                total += labels.size(0)
                correct += (predicted == labels).sum().item()

                if i < 10:
                    idx_to_class = {v: k for k, v in enumerate(DEFAULT_CLASSES[:num_classes])}
                    for j in range(inputs.size(0)):
                        img = inputs[j].cpu()
                        pred = predicted[j].item()
                        true_label = labels[j].item()

                        save_path = os.path.join(
                            visualizations_dir, 
                            f"prediction_{i}_{j}.png"
                        )
                        visualize_prediction(
                            model, img, true_label, idx_to_class, save_path
                        )

        accuracy = 100.0 * correct / total
        print(f"   📈 Batch prediction results:")
        print(f"      Accuracy: {accuracy:.1f}%")
        print(f"      Visualization results saved to: {visualizations_dir}")

    return model

# ---------------------------------------------------------------------------
# 9. Command Line Argument Parsing
# ---------------------------------------------------------------------------

def parse_args():
    parser = argparse.ArgumentParser(description='Handwriting Character Recognition System')

    subparsers = parser.add_subparsers(dest='command', help='Command type', required=True)

    # 训练命令
    train_parser = subparsers.add_parser('train', help='训练模型')
    train_parser.add_argument('data_dir', type=str, help='数据集根目录')
    train_parser.add_argument('num_classes', type=int, help='类别数量')
    train_parser.add_argument('--config', type=str, help='配置文件路径')

    # 推理命令
    infer_parser = subparsers.add_parser('infer', help='模型推理')
    infer_parser.add_argument('--model', type=str, required=True, help='模型文件路径')
    infer_parser.add_argument('--data_dir', type=str, help='数据目录 (用于批量预测)')
    infer_parser.add_argument('--image', type=str, help='单张图像路径 (用于单个预测)')
    infer_parser.add_argument('--config', type=str, help='配置文件路径')

    return parser.parse_args()

# ---------------------------------------------------------------------------
# 10. Main Program
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    args = parse_args()

    if args.command == 'train':
        config = DEFAULT_CONFIG.copy()

        if args.config and os.path.exists(args.config):
            custom_config = load_config(args.config)
            config.update(custom_config)

        model, trained_config = train_handwrite_model(
            args.data_dir, 
            args.num_classes, 
            config
        )

    elif args.command == 'infer':
        num_classes = len(DEFAULT_CLASSES) if not args.data_dir else None

        if not num_classes:
            print("❌ Inference mode requires --data_dir or using default 62 classes")
            sys.exit(1)

        load_and_predict(
            args.model,
            args.data_dir,
            num_classes,
            args.config,
            args.image
        )
"""
06_cnn_mnist.py - CNN 图像分类 (MNIST 手写数字)
================================================
卷积神经网络 (CNN) 是图像处理的核心。
我们用经典的 MNIST 数据集来学习 CNN。

关键概念:
  - Conv2d (卷积层): 提取图像特征
  - MaxPool2d (池化层): 降低空间维度
  - Flatten: 展平为向量
  - torchvision: 数据集和图像变换
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

print("=" * 60)
print("  06 - CNN + MNIST (手写数字识别)")
print("=" * 60)

# ──────────────────────────────────────────────────────────
# 1. 理解卷积
# ──────────────────────────────────────────────────────────
print("\n📌 1. Understanding Convolution")
print("""
  图像是 3D tensor: [Channels, Height, Width]
    - 灰度图: [1, 28, 28]  (MNIST)
    - 彩色图: [3, 224, 224] (ImageNet)

  Conv2d 卷积核在图像上滑动, 提取局部特征:
    ┌───┐
    │ * │ ← 3x3 卷积核 (kernel)
    └───┘
    在图像上每个位置计算点积, 输出一个特征图 (feature map)

  池化 (Pooling) 降低尺寸:
    [2,4,3,1]
    [6,8,5,7]  → MaxPool(2x2) → [8,7]  (每 2x2 区域取最大值)
    [1,3,2,9]                     [3,9]
    [0,1,3,2]
""")

# ──────────────────────────────────────────────────────────
# 2. 准备 MNIST 数据
# ──────────────────────────────────────────────────────────
print("📌 2. Loading MNIST Dataset")

# transforms: 数据预处理流水线
transform = transforms.Compose([
    transforms.ToTensor(),                    # PIL Image → Tensor, 缩放到 [0, 1]
    transforms.Normalize((0.1307,), (0.3081,))  # MNIST 的均值和标准差
])

# 下载并加载 MNIST
train_dataset = datasets.MNIST(
    root='./data', train=True, download=True, transform=transform
)
test_dataset = datasets.MNIST(
    root='./data', train=False, download=True, transform=transform
)

BATCH_SIZE = 64
train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE)

print(f"  Training samples: {len(train_dataset)}")
print(f"  Test samples:     {len(test_dataset)}")

# 看看数据形状
images, labels = next(iter(train_loader))
print(f"  Batch images shape: {images.shape}")  # [64, 1, 28, 28]
print(f"  Batch labels shape: {labels.shape}")   # [64]
print(f"  Label examples:     {labels[:10]}")

# ──────────────────────────────────────────────────────────
# 3. 定义 CNN 模型
# ──────────────────────────────────────────────────────────
print("\n📌 3. Define CNN")


class CNN(nn.Module):
    def __init__(self):
        super().__init__()
        # 卷积层
        self.conv1 = nn.Conv2d(
            in_channels=1,     # 输入通道 (灰度=1, RGB=3)
            out_channels=16,   # 输出 16 个特征图
            kernel_size=3,     # 3x3 卷积核
            padding=1          # 保持尺寸不变
        )
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, padding=1)

        # 池化层
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)  # 尺寸减半

        # 全连接层
        # 28x28 → pool → 14x14 → pool → 7x7
        # 32 channels * 7 * 7 = 1568
        self.fc1 = nn.Linear(32 * 7 * 7, 128)
        self.fc2 = nn.Linear(128, 10)  # 10 个数字类别

        self.dropout = nn.Dropout(0.25)

    def forward(self, x):
        # x: [batch, 1, 28, 28]
        x = self.pool(F.relu(self.conv1(x)))   # → [batch, 16, 14, 14]
        x = self.pool(F.relu(self.conv2(x)))   # → [batch, 32, 7, 7]
        x = x.view(x.size(0), -1)              # Flatten: → [batch, 1568]
        x = self.dropout(F.relu(self.fc1(x)))  # → [batch, 128]
        x = self.fc2(x)                         # → [batch, 10]
        return x


# 设备
if torch.backends.mps.is_available():
    device = torch.device("mps")
elif torch.cuda.is_available():
    device = torch.device("cuda")
else:
    device = torch.device("cpu")
print(f"  Using device: {device}")

model = CNN().to(device)
print(f"  Model:\n{model}")

total_params = sum(p.numel() for p in model.parameters())
print(f"  Total parameters: {total_params:,}")

# ──────────────────────────────────────────────────────────
# 4. 训练
# ──────────────────────────────────────────────────────────
print("\n📌 4. Training")

criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

NUM_EPOCHS = 5  # MNIST 很简单, 5 个 epoch 就够了

for epoch in range(NUM_EPOCHS):
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0

    for batch_idx, (images, labels) in enumerate(train_loader):
        images, labels = images.to(device), labels.to(device)

        # 标准训练 5 步
        outputs = model(images)
        loss = criterion(outputs, labels)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        running_loss += loss.item()
        predicted = outputs.argmax(dim=1)
        correct += (predicted == labels).sum().item()
        total += labels.size(0)

    avg_loss = running_loss / len(train_loader)
    accuracy = correct / total * 100
    print(f"    Epoch {epoch + 1}/{NUM_EPOCHS}: "
          f"loss={avg_loss:.4f}, train_acc={accuracy:.1f}%")

# ──────────────────────────────────────────────────────────
# 5. 测试
# ──────────────────────────────────────────────────────────
print("\n📌 5. Testing")

model.eval()
correct = 0
total = 0

with torch.no_grad():
    for images, labels in test_loader:
        images, labels = images.to(device), labels.to(device)
        outputs = model(images)
        predicted = outputs.argmax(dim=1)
        correct += (predicted == labels).sum().item()
        total += labels.size(0)

test_acc = correct / total * 100
print(f"  Test Accuracy: {test_acc:.1f}%")

# 看几个预测
with torch.no_grad():
    images, labels = next(iter(test_loader))
    images, labels = images.to(device), labels.to(device)
    outputs = model(images)
    preds = outputs.argmax(dim=1)

    print(f"\n  Sample predictions (first 10):")
    for i in range(10):
        status = "✓" if preds[i] == labels[i] else "✗"
        print(f"    {status} True={labels[i].item()}, Pred={preds[i].item()}")

# ──────────────────────────────────────────────────────────
# 6. CNN 数据流总结
# ──────────────────────────────────────────────────────────
print("""
  📝 CNN 数据流:
    Input [1, 28, 28]
      ↓ Conv2d(1→16, 3x3) + ReLU
    [16, 28, 28]
      ↓ MaxPool(2x2)
    [16, 14, 14]
      ↓ Conv2d(16→32, 3x3) + ReLU
    [32, 14, 14]
      ↓ MaxPool(2x2)
    [32, 7, 7]
      ↓ Flatten
    [1568]
      ↓ Linear(1568→128) + ReLU + Dropout
    [128]
      ↓ Linear(128→10)
    [10] ← logits (10 个类别的分数)
""")

print("✅ 06_cnn_mnist.py 完成！")
print("   下一步: python 07_save_load.py")

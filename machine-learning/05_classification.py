"""
05_classification.py - 分类任务
================================
回归预测连续值 (如房价), 分类预测离散类别 (如猫/狗)。

关键概念:
  - CrossEntropyLoss (交叉熵损失)
  - Softmax 与概率
  - 准确率 (Accuracy)
  - DataLoader 批量加载数据
  - train/eval 模式
"""

import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset

print("=" * 60)
print("  05 - CLASSIFICATION (分类)")
print("=" * 60)

# ──────────────────────────────────────────────────────────
# 1. 理解 CrossEntropyLoss
# ──────────────────────────────────────────────────────────
print("\n📌 1. Understanding CrossEntropyLoss")

print("""
  分类问题中, 模型输出 logits (原始分数), 不是概率!

  例: 3 类分类, 模型输出 [2.0, 1.0, 0.5]
      ↓ Softmax
      [0.59, 0.27, 0.14]  ← 现在是概率了, 和为 1

  CrossEntropyLoss = Softmax + NLLLoss (一步到位)
  所以 model 最后一层 **不需要** 加 Softmax!
""")

# 演示
logits = torch.tensor([[2.0, 1.0, 0.5]])  # 模型输出 (1 个样本, 3 个类)
target = torch.tensor([0])                  # 真实标签: 第 0 类

loss_fn = nn.CrossEntropyLoss()
loss = loss_fn(logits, target)
print(f"  Logits: {logits}")
print(f"  Target: class {target.item()}")
print(f"  Loss:   {loss.item():.4f}")

# Softmax 概率
probs = torch.softmax(logits, dim=1)
print(f"  Probabilities: {probs}")
print(f"  Predicted class: {probs.argmax(dim=1).item()}")

# ──────────────────────────────────────────────────────────
# 2. 生成分类数据
# ──────────────────────────────────────────────────────────
print("\n📌 2. Generate Classification Data")

torch.manual_seed(42)
NUM_SAMPLES = 500
NUM_FEATURES = 4
NUM_CLASSES = 3

# 生成 3 个簇的数据
centers = torch.tensor([
    [2.0, 2.0, 0.0, 0.0],
    [-2.0, -2.0, 0.0, 0.0],
    [0.0, 0.0, 2.0, 2.0],
])

X_all = []
y_all = []
for cls in range(NUM_CLASSES):
    samples = centers[cls] + torch.randn(NUM_SAMPLES // NUM_CLASSES, NUM_FEATURES) * 0.8
    X_all.append(samples)
    y_all.append(torch.full((NUM_SAMPLES // NUM_CLASSES,), cls, dtype=torch.long))

X = torch.cat(X_all)
y = torch.cat(y_all)

# 打乱
perm = torch.randperm(len(X))
X, y = X[perm], y[perm]

# 分割 train/test
split = int(0.8 * len(X))
X_train, X_test = X[:split], X[split:]
y_train, y_test = y[:split], y[split:]

print(f"  X_train: {X_train.shape}, y_train: {y_train.shape}")
print(f"  X_test:  {X_test.shape},  y_test:  {y_test.shape}")
print(f"  Classes: {torch.unique(y)}")

# ──────────────────────────────────────────────────────────
# 3. DataLoader (批量加载)
# ──────────────────────────────────────────────────────────
print("\n📌 3. DataLoader")

# TensorDataset 把 X 和 y 打包在一起
train_dataset = TensorDataset(X_train, y_train)
test_dataset = TensorDataset(X_test, y_test)

# DataLoader 负责: 分批 (batch) + 打乱 (shuffle)
BATCH_SIZE = 32
train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE)

# 看看一个 batch
for batch_X, batch_y in train_loader:
    print(f"  One batch: X={batch_X.shape}, y={batch_y.shape}")
    break

# ──────────────────────────────────────────────────────────
# 4. 定义分类模型
# ──────────────────────────────────────────────────────────
print("\n📌 4. Define Classifier")


class Classifier(nn.Module):
    def __init__(self, in_dim, hidden_dim, num_classes):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(in_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.2),            # 防过拟合: 训练时随机丢弃 20% 的神经元
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(hidden_dim, num_classes),
            # ⚠️ 注意: 最后没有 Softmax! CrossEntropyLoss 会自动处理
        )

    def forward(self, x):
        return self.net(x)


model = Classifier(NUM_FEATURES, hidden_dim=64, num_classes=NUM_CLASSES)
print(f"  {model}")

criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.005)

# ──────────────────────────────────────────────────────────
# 5. 训练循环 (带 DataLoader)
# ──────────────────────────────────────────────────────────
print("\n📌 5. Training Loop")

NUM_EPOCHS = 30

for epoch in range(NUM_EPOCHS):
    model.train()  # 训练模式 (Dropout 生效)
    total_loss = 0
    correct = 0
    total = 0

    for batch_X, batch_y in train_loader:
        # Forward
        logits = model(batch_X)
        loss = criterion(logits, batch_y)

        # Backward
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        # 统计
        total_loss += loss.item() * batch_X.size(0)
        predicted = logits.argmax(dim=1)
        correct += (predicted == batch_y).sum().item()
        total += batch_y.size(0)

    avg_loss = total_loss / total
    accuracy = correct / total * 100

    if epoch % 5 == 0:
        print(f"    Epoch {epoch:2d}: loss={avg_loss:.4f}, "
              f"train_acc={accuracy:.1f}%")

# ──────────────────────────────────────────────────────────
# 6. 评估 (Evaluation)
# ──────────────────────────────────────────────────────────
print("\n📌 6. Evaluation")

model.eval()  # 评估模式 (Dropout 关闭)
correct = 0
total = 0

with torch.no_grad():  # 不计算梯度, 节省内存
    for batch_X, batch_y in test_loader:
        logits = model(batch_X)
        predicted = logits.argmax(dim=1)
        correct += (predicted == batch_y).sum().item()
        total += batch_y.size(0)

test_acc = correct / total * 100
print(f"  Test Accuracy: {test_acc:.1f}%")

# 看看几个预测
with torch.no_grad():
    sample_X = X_test[:5]
    sample_y = y_test[:5]
    logits = model(sample_X)
    probs = torch.softmax(logits, dim=1)
    preds = logits.argmax(dim=1)

    print(f"\n  Sample predictions:")
    for i in range(5):
        p = probs[i]
        print(f"    True={sample_y[i].item()}, "
              f"Pred={preds[i].item()}, "
              f"Probs=[{p[0]:.2f}, {p[1]:.2f}, {p[2]:.2f}]")

print("""
  📝 总结:
    - 分类用 CrossEntropyLoss, 模型最后一层不要加 Softmax
    - model.train() 打开 Dropout/BatchNorm 训练行为
    - model.eval()  关闭 Dropout, 用于推理
    - torch.no_grad() 推理时节省内存
    - DataLoader 自动处理分批和打乱
""")

print("✅ 05_classification.py 完成！")
print("   下一步: python 06_cnn_mnist.py")

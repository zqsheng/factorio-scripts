"""
04_nn_module.py - 构建神经网络 (nn.Module)
==========================================
nn.Module 是 PyTorch 中所有神经网络的基类。
学会用它构建任意复杂的模型。

关键概念:
  - 继承 nn.Module
  - __init__ 中定义层
  - forward() 中定义数据流
  - 查看参数
  - nn.Sequential 快速搭建
"""

import torch
from torch import nn

print("=" * 60)
print("  04 - nn.Module (构建神经网络)")
print("=" * 60)

# ──────────────────────────────────────────────────────────
# 1. 自定义 nn.Module
# ──────────────────────────────────────────────────────────
print("\n📌 1. Custom nn.Module")


class SimpleNet(nn.Module):
    """一个简单的 2 层全连接网络"""

    def __init__(self, input_dim, hidden_dim, output_dim):
        super().__init__()  # 必须调用!
        # 定义层 (可学习的参数)
        self.fc1 = nn.Linear(input_dim, hidden_dim)  # 全连接层 1
        self.fc2 = nn.Linear(hidden_dim, output_dim)  # 全连接层 2
        self.relu = nn.ReLU()  # 激活函数 (无参数)

    def forward(self, x):
        """定义数据如何流过网络"""
        x = self.fc1(x)  # 线性变换: x @ W1 + b1
        x = self.relu(x)  # 非线性激活: max(0, x)
        x = self.fc2(x)  # 线性变换: x @ W2 + b2
        return x


model = SimpleNet(input_dim=10, hidden_dim=32, output_dim=3)
print(f"  Model:\n{model}")

# 查看参数
print("\n  Parameters:")
for name, param in model.named_parameters():
    print(f"    {name:12s} shape={list(param.shape)}")

total_params = sum(p.numel() for p in model.parameters())
print(f"  Total parameters: {total_params}")

# 测试前向传播
dummy = torch.randn(5, 10)  # 5 个样本, 每个 10 维
output = model(dummy)
print(f"\n  Input:  {dummy.shape}")  # [5, 10]
print(f"  Output: {output.shape}")  # [5, 3]

# ──────────────────────────────────────────────────────────
# 2. nn.Sequential (快速搭建)
# ──────────────────────────────────────────────────────────
print("\n📌 2. nn.Sequential")

# 当网络是简单的层堆叠时, 可以用 Sequential 快速定义
seq_model = nn.Sequential(
    nn.Linear(10, 64),
    nn.ReLU(),
    nn.Linear(64, 32),
    nn.ReLU(),
    nn.Linear(32, 3),
)
print(f"  Sequential model:\n{seq_model}")

out = seq_model(dummy)
print(f"  Output shape: {out.shape}")

# ──────────────────────────────────────────────────────────
# 3. 常用层和激活函数
# ──────────────────────────────────────────────────────────
print("\n📌 3. Common Layers & Activations")
print("""
  常用层:
    nn.Linear(in, out)     全连接层 / Dense / MLP
    nn.Conv2d(in_ch, out_ch, kernel)  卷积层 (图像)
    nn.LSTM(in, hidden)    循环层 (序列)
    nn.Embedding(vocab, dim) 词嵌入 (NLP)
    nn.BatchNorm1d(features) 批归一化
    nn.Dropout(p)          随机丢弃 (防过拟合)

  常用激活函数:
    nn.ReLU()     max(0, x)          最常用
    nn.Sigmoid()  1/(1+e^-x)        输出 0~1
    nn.Tanh()     双曲正切            输出 -1~1
    nn.Softmax(dim)  归一化为概率     分类最后一层
    nn.LeakyReLU()   x<0 时有小斜率   避免"死神经元"
""")

# ──────────────────────────────────────────────────────────
# 4. 更复杂的网络: 有分支的结构
# ──────────────────────────────────────────────────────────
print("📌 4. Complex Architecture (Branching)")


class BranchNet(nn.Module):
    """带残差连接的网络 (ResNet 的核心思想)"""

    def __init__(self, dim):
        super().__init__()
        self.branch = nn.Sequential(
            nn.Linear(dim, dim),
            nn.ReLU(),
            nn.Linear(dim, dim),
        )
        self.relu = nn.ReLU()

    def forward(self, x):
        residual = x  # 保存输入
        out = self.branch(x)  # 通过分支
        out = out + residual  # 残差连接! (跳跃连接)
        out = self.relu(out)
        return out


branch_model = BranchNet(dim=16)
x = torch.randn(4, 16)
y = branch_model(x)
print(f"  BranchNet input:  {x.shape}")
print(f"  BranchNet output: {y.shape}")
print("  (输入和输出形状相同, 因为有残差连接)")

# ──────────────────────────────────────────────────────────
# 5. 实战: 训练一个小网络做回归
# ──────────────────────────────────────────────────────────
print("\n📌 5. Training a Small Network")

# 数据: y = sin(x)
torch.manual_seed(42)
X_train = torch.linspace(-3, 3, 200).unsqueeze(1)  # [200, 1]
y_train = torch.sin(X_train) + 0.1 * torch.randn_like(X_train)

# 模型: 3 层 MLP
net = nn.Sequential(
    nn.Linear(1, 64),
    nn.ReLU(),
    nn.Linear(64, 64),
    nn.ReLU(),
    nn.Linear(64, 1),
)

criterion = nn.MSELoss()
optimizer = torch.optim.Adam(net.parameters(), lr=0.01)

# 训练
for epoch in range(500):
    pred = net(X_train)
    loss = criterion(pred, y_train)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    if epoch % 100 == 0:
        print(f"    Epoch {epoch:3d}: loss={loss.item():.6f}")

# 验证
with torch.no_grad():
    test_x = torch.tensor([[1.0], [0.0], [-1.0]])
    pred = net(test_x)
    real = torch.sin(test_x)
    print("\n  Predictions vs Real (sin(x)):")
    for i in range(3):
        print(
            f"    x={test_x[i].item():5.1f}: "
            f"pred={pred[i].item():6.3f}, "
            f"real={real[i].item():6.3f}"
        )

print("\n✅ 04_nn_module.py 完成！")
print("   下一步: python 05_classification.py")

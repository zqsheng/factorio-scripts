"""
03_linear_regression.py - 用 PyTorch 实现线性回归
=================================================
线性回归是最简单的 ML 模型: y = wx + b
我们用它来学习完整的训练循环:

  1. 准备数据
  2. 定义模型
  3. 定义损失函数 (loss)
  4. 定义优化器 (optimizer)
  5. 训练循环 (forward -> loss -> backward -> update)

这是所有深度学习训练的模板!
"""

import torch
import torch.nn as nn

print("=" * 60)
print("  03 - LINEAR REGRESSION")
print("=" * 60)

# ──────────────────────────────────────────────────────────
# 1. 生成模拟数据
# ──────────────────────────────────────────────────────────
print("\n📌 1. Generate Data")

# 真实的关系: y = 3x + 7 (加一些噪声)
TRUE_W = 3.0
TRUE_B = 7.0

torch.manual_seed(42)
X = torch.rand(100, 1) * 10                      # 100 个样本, x ∈ [0, 10)
y = TRUE_W * X + TRUE_B + torch.randn(100, 1)    # 加噪声

print(f"  X shape: {X.shape}")  # [100, 1]
print(f"  y shape: {y.shape}")  # [100, 1]
print(f"  真实参数: w={TRUE_W}, b={TRUE_B}")

# ──────────────────────────────────────────────────────────
# 2. 方法 A: 纯手写 (理解原理)
# ──────────────────────────────────────────────────────────
print("\n📌 2. Method A: From Scratch")

w = torch.randn(1, requires_grad=True)
b = torch.zeros(1, requires_grad=True)
lr = 0.01

for epoch in range(100):
    # Forward: 预测
    y_pred = w * X + b

    # Loss: 均方误差
    loss = ((y_pred - y) ** 2).mean()

    # Backward: 计算梯度
    loss.backward()

    # Update: 更新参数 (不追踪梯度)
    with torch.no_grad():
        w -= lr * w.grad
        b -= lr * b.grad

    # 清零梯度
    w.grad.zero_()
    b.grad.zero_()

    if epoch % 20 == 0:
        print(f"    Epoch {epoch:3d}: loss={loss.item():.4f}, "
              f"w={w.item():.3f}, b={b.item():.3f}")

print(f"  From scratch result: w={w.item():.3f} (真实={TRUE_W}), "
      f"b={b.item():.3f} (真实={TRUE_B})")

# ──────────────────────────────────────────────────────────
# 3. 方法 B: 用 nn.Linear + optimizer (标准写法)
# ──────────────────────────────────────────────────────────
print("\n📌 3. Method B: Using nn.Linear (Standard)")

# 模型: 一个线性层 y = wx + b
model = nn.Linear(in_features=1, out_features=1)

# 损失函数: 均方误差
criterion = nn.MSELoss()

# 优化器: 随机梯度下降
optimizer = torch.optim.SGD(model.parameters(), lr=0.01)

print(f"  初始参数: w={model.weight.item():.3f}, b={model.bias.item():.3f}")

for epoch in range(100):
    # 1. Forward pass
    y_pred = model(X)

    # 2. Compute loss
    loss = criterion(y_pred, y)

    # 3. Zero gradients (⚠️ 别忘了!)
    optimizer.zero_grad()

    # 4. Backward pass
    loss.backward()

    # 5. Update parameters
    optimizer.step()

    if epoch % 20 == 0:
        print(f"    Epoch {epoch:3d}: loss={loss.item():.4f}, "
              f"w={model.weight.item():.3f}, b={model.bias.item():.3f}")

print(f"  nn.Linear result: w={model.weight.item():.3f} (真实={TRUE_W}), "
      f"b={model.bias.item():.3f} (真实={TRUE_B})")

# ──────────────────────────────────────────────────────────
# 4. 训练循环模板总结
# ──────────────────────────────────────────────────────────
print("\n📌 4. Training Loop Template")
print("""
  ┌─────────────────────────────────────────────┐
  │  for epoch in range(num_epochs):            │
  │      y_pred = model(X)          # Forward   │
  │      loss = criterion(y_pred, y) # Loss     │
  │      optimizer.zero_grad()       # Zero     │
  │      loss.backward()             # Backward │
  │      optimizer.step()            # Update   │
  └─────────────────────────────────────────────┘

  记住这 5 步! 无论多复杂的模型, 训练循环都是这个结构。
""")

print("✅ 03_linear_regression.py 完成！")
print("   下一步: python 04_nn_module.py")

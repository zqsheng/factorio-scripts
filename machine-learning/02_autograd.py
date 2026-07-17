"""
02_autograd.py - 自动微分 (Automatic Differentiation)
=====================================================
PyTorch 的 autograd 引擎可以自动计算梯度，这是训练神经网络的核心。

关键概念:
  - requires_grad: 告诉 PyTorch "请追踪这个 tensor 的所有操作"
  - .backward():   反向传播，计算梯度
  - .grad:         查看计算好的梯度
  - 计算图 (Computation Graph): PyTorch 如何记录操作

数学直觉:
  如果 y = f(x), 那么 dy/dx 就是 y 对 x 的梯度。
  梯度告诉我们: "x 变化一点点, y 会怎么变?"
"""

import torch

print("=" * 60)
print("  02 - AUTOGRAD (自动微分)")
print("=" * 60)

# ──────────────────────────────────────────────────────────
# 1. 基本梯度计算
# ──────────────────────────────────────────────────────────
print("\n📌 1. Basic Gradient")

# 创建一个需要追踪梯度的 tensor
x = torch.tensor(3.0, requires_grad=True)

# 定义一个函数: y = x^2 + 2x + 1
y = x ** 2 + 2 * x + 1

# 反向传播: 计算 dy/dx
y.backward()

# dy/dx = 2x + 2, 当 x=3 时, dy/dx = 8
print(f"  x = {x.item()}")
print(f"  y = x² + 2x + 1 = {y.item()}")
print(f"  dy/dx = 2x + 2 = {x.grad.item()}")  # 应该是 8.0

# ──────────────────────────────────────────────────────────
# 2. 向量的梯度
# ──────────────────────────────────────────────────────────
print("\n📌 2. Vector Gradient")

x = torch.tensor([1.0, 2.0, 3.0], requires_grad=True)

# y = sum(x^2) = 1 + 4 + 9 = 14
y = (x ** 2).sum()
y.backward()

# dy/dx_i = 2 * x_i
print(f"  x = {x.data}")
print(f"  y = sum(x²) = {y.item()}")
print(f"  dy/dx = 2x = {x.grad}")  # [2.0, 4.0, 6.0]

# ──────────────────────────────────────────────────────────
# 3. 计算图的理解
# ──────────────────────────────────────────────────────────
print("\n📌 3. Computation Graph")
print("""
  计算图示意 (y = x² + 2x + 1):

       x ──┬──→ [x²] ──→ [+] ──→ [+] ──→ y
            │              ↑        ↑
            └──→ [2x] ────┘   [1] ─┘

  backward() 从 y 出发，沿箭头反方向计算每个节点的梯度。
  这就是"反向传播" (Backpropagation)。
""")

# 验证: grad_fn 显示创建 tensor 的操作
a = torch.tensor(2.0, requires_grad=True)
b = a * 3
c = b + 1
print(f"  b = a * 3,  b.grad_fn = {b.grad_fn}")      # MulBackward
print(f"  c = b + 1,  c.grad_fn = {c.grad_fn}")       # AddBackward

# ──────────────────────────────────────────────────────────
# 4. 梯度累积 (重要陷阱!)
# ──────────────────────────────────────────────────────────
print("\n📌 4. Gradient Accumulation (⚠️ Common Pitfall)")

w = torch.tensor(1.0, requires_grad=True)

# 第一次
loss1 = (w * 2) ** 2  # loss = 4w², dloss/dw = 8w = 8
loss1.backward()
print(f"  After 1st backward: w.grad = {w.grad}")  # 8.0

# 第二次 - 梯度会累积!
loss2 = (w * 2) ** 2
loss2.backward()
print(f"  After 2nd backward: w.grad = {w.grad}")  # 16.0 (8+8, 累积了!)

# 正确做法: 每次 backward 前清零
w.grad.zero_()
loss3 = (w * 2) ** 2
loss3.backward()
print(f"  After zero_grad + backward: w.grad = {w.grad}")  # 8.0 ✓

print("""
  ⚠️  这就是为什么训练循环中总有 optimizer.zero_grad()
      如果忘了，梯度会越积越大，模型会爆炸!
""")

# ──────────────────────────────────────────────────────────
# 5. 停止追踪梯度
# ──────────────────────────────────────────────────────────
print("📌 5. Detaching from Graph")

x = torch.tensor(5.0, requires_grad=True)

# 方法 1: with torch.no_grad()  —— 推理时常用
with torch.no_grad():
    y = x * 2
    print(f"  no_grad: y.requires_grad = {y.requires_grad}")  # False

# 方法 2: .detach()  —— 从计算图中分离
z = (x * 2).detach()
print(f"  detach:  z.requires_grad = {z.requires_grad}")  # False

print("""
  什么时候用?
    - 推理 (inference) 时不需要梯度，用 torch.no_grad() 节省内存
    - 冻结部分网络时用 .detach()
    - 评估模型时用 model.eval() + torch.no_grad()
""")

# ──────────────────────────────────────────────────────────
# 6. 实际意义: 手动梯度下降
# ──────────────────────────────────────────────────────────
print("📌 6. Manual Gradient Descent (Preview)")

# 目标: 找到使 y = (x - 5)^2 最小化的 x (答案显然是 x=5)
x = torch.tensor(0.0, requires_grad=True)
learning_rate = 0.1

print(f"  Goal: minimize y = (x - 5)²")
print(f"  Starting x = {x.item():.2f}")

for step in range(20):
    y = (x - 5) ** 2          # 前向传播
    y.backward()               # 计算梯度: dy/dx = 2(x-5)

    with torch.no_grad():      # 更新时不追踪梯度
        x -= learning_rate * x.grad  # x = x - lr * gradient

    x.grad.zero_()             # 清零梯度!

    if step % 5 == 0:
        print(f"    Step {step:2d}: x={x.item():6.3f}, y={y.item():8.4f}")

print(f"  Final x = {x.item():.4f} (should be ≈ 5.0)")

print("\n✅ 02_autograd.py 完成！")
print("   下一步: python 03_linear_regression.py")

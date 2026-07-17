"""
01_tensors.py - PyTorch Tensor 基础
====================================
Tensor 是 PyTorch 的核心数据结构，类似于 NumPy ndarray，但可以在 GPU 上运行。

关键概念:
  - 创建 tensor 的多种方式
  - 形状操作 (reshape, view, squeeze)
  - 索引与切片
  - 设备管理 (CPU / MPS / CUDA)
  - 与 NumPy 的互转
"""

import torch
import numpy as np

print("=" * 60)
print("  01 - TENSOR BASICS")
print("=" * 60)

# ──────────────────────────────────────────────────────────
# 1. 创建 Tensor
# ──────────────────────────────────────────────────────────
print("\n📌 1. Creating Tensors")

# 从 Python list
a = torch.tensor([1, 2, 3, 4])
print(f"  From list:     {a}          dtype={a.dtype}")

# 指定 dtype
b = torch.tensor([1, 2, 3, 4], dtype=torch.float32)
print(f"  Float tensor:  {b}  dtype={b.dtype}")

# 常用工厂函数
zeros = torch.zeros(2, 3)         # 全 0
ones = torch.ones(2, 3)           # 全 1
rand = torch.rand(2, 3)           # [0, 1) 均匀分布
randn = torch.randn(2, 3)        # 标准正态分布
arange = torch.arange(0, 10, 2)  # 等差序列
linspace = torch.linspace(0, 1, 5)  # 等分

print(f"  zeros(2,3):\n{zeros}")
print(f"  rand(2,3):\n{rand}")
print(f"  arange(0,10,2): {arange}")
print(f"  linspace(0,1,5): {linspace}")

# ──────────────────────────────────────────────────────────
# 2. 形状 (Shape) 操作
# ──────────────────────────────────────────────────────────
print("\n📌 2. Shape Operations")

x = torch.rand(2, 3, 4)
print(f"  x.shape = {x.shape}")           # torch.Size([2, 3, 4])
print(f"  x.ndim  = {x.ndim}")            # 3
print(f"  x.numel()= {x.numel()}")        # 24 = 2*3*4

# reshape / view - 改变形状但不改变数据
y = x.reshape(6, 4)                       # 总元素数必须一致
print(f"  reshape(6,4) -> {y.shape}")

# -1 表示自动推断
z = x.reshape(-1, 4)
print(f"  reshape(-1,4) -> {z.shape}")     # [6, 4]

# squeeze / unsqueeze - 去除/增加维度为 1 的轴
s = torch.rand(1, 3, 1)
print(f"  Before squeeze: {s.shape}")      # [1, 3, 1]
print(f"  After squeeze:  {s.squeeze().shape}")  # [3]

u = torch.rand(3)
print(f"  Before unsqueeze: {u.shape}")    # [3]
print(f"  unsqueeze(0):     {u.unsqueeze(0).shape}")  # [1, 3]
print(f"  unsqueeze(1):     {u.unsqueeze(1).shape}")  # [3, 1]

# permute / transpose - 交换维度
p = torch.rand(2, 3, 4)
print(f"  permute(2,0,1): {p.permute(2, 0, 1).shape}")  # [4, 2, 3]

# ──────────────────────────────────────────────────────────
# 3. 索引与切片 (和 NumPy 完全一样)
# ──────────────────────────────────────────────────────────
print("\n📌 3. Indexing & Slicing")

m = torch.tensor([[1, 2, 3],
                   [4, 5, 6],
                   [7, 8, 9]])

print(f"  m[0]       = {m[0]}")            # 第 0 行: [1, 2, 3]
print(f"  m[1, 2]    = {m[1, 2]}")         # 第 1 行第 2 列: 6
print(f"  m[:, 1]    = {m[:, 1]}")         # 所有行的第 1 列: [2, 5, 8]
print(f"  m[0:2, :]  = \n{m[0:2, :]}")     # 前 2 行

# Boolean indexing
mask = m > 5
print(f"  m > 5 =\n{mask}")
print(f"  m[m > 5] = {m[mask]}")           # [6, 7, 8, 9]

# ──────────────────────────────────────────────────────────
# 4. 数学运算
# ──────────────────────────────────────────────────────────
print("\n📌 4. Math Operations")

a = torch.tensor([1.0, 2.0, 3.0])
b = torch.tensor([4.0, 5.0, 6.0])

# 逐元素运算
print(f"  a + b = {a + b}")               # [5, 7, 9]
print(f"  a * b = {a * b}")               # [4, 10, 18] 注意: 逐元素乘，不是矩阵乘
print(f"  a ** 2 = {a ** 2}")              # [1, 4, 9]

# 矩阵乘法
A = torch.rand(2, 3)
B = torch.rand(3, 4)
C = A @ B                                 # 等价于 torch.matmul(A, B)
print(f"  A(2x3) @ B(3x4) = C{C.shape}")  # [2, 4]

# 聚合运算
t = torch.tensor([1.0, 2.0, 3.0, 4.0, 5.0])
print(f"  sum={t.sum():.1f}, mean={t.mean():.1f}, "
      f"max={t.max():.1f}, min={t.min():.1f}, std={t.std():.2f}")

# dim 参数 - 沿指定维度聚合
matrix = torch.tensor([[1.0, 2.0],
                        [3.0, 4.0],
                        [5.0, 6.0]])
print(f"  sum(dim=0) 按列求和: {matrix.sum(dim=0)}")  # [9, 12]
print(f"  sum(dim=1) 按行求和: {matrix.sum(dim=1)}")  # [3, 7, 11]

# ──────────────────────────────────────────────────────────
# 5. 设备管理 (Device)
# ──────────────────────────────────────────────────────────
print("\n📌 5. Device Management")

# 自动选择最佳设备
if torch.backends.mps.is_available():
    device = torch.device("mps")
    print(f"  ✅ Using Apple Silicon GPU (MPS)")
elif torch.cuda.is_available():
    device = torch.device("cuda")
    print(f"  ✅ Using NVIDIA GPU (CUDA)")
else:
    device = torch.device("cpu")
    print(f"  ℹ️  Using CPU")

# 移动 tensor 到设备
cpu_tensor = torch.rand(3, 3)
gpu_tensor = cpu_tensor.to(device)
print(f"  cpu_tensor.device = {cpu_tensor.device}")
print(f"  gpu_tensor.device = {gpu_tensor.device}")

# 直接在设备上创建
on_device = torch.rand(3, 3, device=device)
print(f"  Created on device: {on_device.device}")

# 移回 CPU (和 numpy 交互前必须在 CPU 上)
back_to_cpu = gpu_tensor.cpu()
print(f"  Back to CPU: {back_to_cpu.device}")

# ──────────────────────────────────────────────────────────
# 6. Tensor <-> NumPy
# ──────────────────────────────────────────────────────────
print("\n📌 6. Tensor ↔ NumPy")

# Tensor -> NumPy (共享内存!)
t = torch.tensor([1.0, 2.0, 3.0])
n = t.numpy()
print(f"  Tensor -> NumPy: {n}, type={type(n)}")

# 修改 numpy 会影响 tensor (共享内存)
n[0] = 99.0
print(f"  After modifying numpy: tensor={t}")  # tensor 也变了!

# NumPy -> Tensor
arr = np.array([10, 20, 30], dtype=np.float32)
t2 = torch.from_numpy(arr)
print(f"  NumPy -> Tensor: {t2}")

print("\n✅ 01_tensors.py 完成！")
print("   下一步: python 02_autograd.py")

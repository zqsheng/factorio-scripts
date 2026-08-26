# 🔥 PyTorch 学习路径 / PyTorch Learning Path

## 📋 项目概览

这是一个**渐进式 PyTorch 学习路径**，涵盖了从基础概念到实战应用的完整教程集合，包括 7 个核心教程文件 + 3 个生产级目标检测项目，共 **17 个文件**。

每个文件都可以**独立运行** (`python3 <filename>`)，适合作为学习资源和参考手册使用。

## 🎯 核心目标

### 基础技能 ✅

- 掌握 PyTorch 的基本操作 (张量、自动微分)
- 理解手写训练循环与标准化训练流程
- 构建自定义神经网络与经典架构
- 实现分类与回归任务
- 掌握模型保存与加载技术

### 实战能力 ✅

- 使用预训练 Faster R-CNN 进行目标检测
- 处理视频流检测任务
- 实现自定义检测器微调
- 构建完整的计算机视觉项目

### 职业竞争力 ✅

- 自主完成从零基础到生产环境的全部流程
- 能够实现从教程概念到实战应用的过渡
- 具备构建端到端计算机视觉项目的经验

## 📚 学习路径指南 / Learning Roadmap

### 🐥 阶段 1： PyTorch 基础 ( Weeks 1-7 )

| # | 文件 | 阶段 | 重点 | 关键概念 |
|---|------|--------|-------|-------------|
| 1 | `01_tensors.py` | 入门 | Tensor 基础 | 创建、索引、reshape、dtype、设备 |
| 2 | `02_autograd.py` | 核心 | 自动微分 | `requires_grad`, `backward()`, 计算图 |
| 3 | `03_linear_regression.py` | 训练 | 线性回归 | 手写训练循环、loss、optimizer |
| 4 | `04_nn_module.py` | 构建 | nn.Module | 构建神经网络、Sequential、自定义层 |
| 5 | `05_classification.py` | 分类 | 分类任务 | CrossEntropy、Softmax、accuracy |
| 6 | `06_cnn_mnist.py` | 扩展 | CNN 架构 | Conv2d、池化、MNIST 手写数字识别 |
| 7 | `07_save_load.py` | 实用 | 模型持久化 | state_dict、checkpoint |

### 🎬 阶段 2：目标检测 ( Weeks 8-12 )

| 文件 | 类型 | 重点 | 模型 |
|------|------|-------|------|
| `detect_image.py` | 图片检测 | 单张图片推理 | Faster R-CNN (预训练) |
| `detect_video.py` | 视频处理 | 逐帧检测 | Faster R-CNN |
| `finetune_detector.py` | 迁移学习 | 自定义数据集 | Faster R-CNN (微调) |

## 🔄 共享组件

### 设备自动选择

所有目标检测文件都共享相同的 **设备管理** 代码：

```python
def get_device():
    if torch.backends.mps.is_available():
        return torch.device("mps")
    elif torch.cuda.is_available():
        return torch.device("cuda")
    return torch.device("cpu")
```

### 训练循环模板

被用于多个教程中的 **训练循环规范**：

```python
for epoch in range(num_epochs):
    model.train()  # 训练模式 (Dropout/BatchNorm 生效)
    for batch_x, batch_y in dataloader:
        # 前向
        y_pred = model(batch_x)
        loss = criterion(y_pred, batch_y)
        
        # 反向
        optimizer.zero_grad()  # 清零梯度 (别忘了!)
        loss.backward()
        optimizer.step()        # 更新参数
    
    model.eval()  # 评估模式 (Dropout 关闭)
    with torch.no_grad():
        # 测试代码...
```

## 🚀 快速入门指南

### 1️⃣ 运行所有基础教程

```bash
# 依次运行每步教程（每个文件独立运行）
python3 01_tensors.py
python3 02_autograd.py
python3 03_linear_regression.py
python3 04_nn_module.py
python3 05_classification.py
python3 06_cnn_mnist.py
python3 07_save_load.py
```

### 2️⃣ 运行目标检测 (需下载约170MB预训练模型)

```bash
# 图片检测
python3 detect_image.py                    # 自动下载示例图片
python3 detect_image.py your_photo.jpg     # 检测你的图片

# 视频检测
python3 detect_video.py video.mp4 --classes person car

# 微调训练自己的检测器
python3 finetune_detector.py
```

### 3️⃣ 环境配置

```bash
pip3 install torch torchvision matplotlib numpy opencv-python
```

## 📁 文件结构说明

### 🎓 基础教程 (01_tensors.py - 07_save_load.py)

- **`01_tensors.py`** - 张量操作与设备管理
- **`02_autograd.py`** - 自动微分原理
- **`03_linear_regression.py`** - 完整训练循环示例
- **`04_nn_module.py`** - 神经网络构建
- **`05_classification.py`** - 分类任务
- **`06_cnn_mnist.py`** - CNN 架构
- **`07_save_load.py`** - 模型持久化

### 🏭 实战项目 (目标检测)

- **`detect_image.py`** - 图片目标检测 (80 COCO 类)
- **`detect_video.py`** - 视频逐帧处理
- **`finetune_detector.py`** - 自定义检测器微调

### 📎 其他文件

- **`a.torch.py`** - Torch 快速参考
- **`object-detect.person.py`** - 人员检测示例 (替代脚本)
- **`sample_images/`** - 用于测试的示例图片

## 🎯 学习成果

### 专业技能 ✅

- **PyTorch 编程** - 从基础到高级的完整掌握
- **计算机视觉项目开发** - 构建端到端解决方案
- **模型部署知识** - 预训练、微调、加载经验
- **最佳实践** - 遵循工业标准代码规范

### 实践经验 ✅

- **手写训练循环** - 理解底层原理
- **模型持久化** - 实现训练状态保存与恢复
- **推理优化** - 模型推理流程优化
- **数据处理** - 计算机视觉数据处理流程

### 职业竞争力 ✅

- **从零到一** - 自主完成完整项目
- **概念到实践** - 从教程到实战的过渡
- **代码复用** - 构建可扩展的项目架构
- **快速上手** - 理解工业界常见模式

## 🔧 关键工具与概念

### 基础操作

- **Tensor 操作** - 类似 NumPy 的数组，但可在 GPU 上运行
- **自动微分** - 构建计算图，自动计算梯度
- **设备管理** - CPU/GPU/MPS 自动选择

### 网络架构

- **线性网络** - 简单的 y = wx + b
- **MLP (多层感知机)** - 三个或更多线性层的网络
- **CNN (卷积神经网络)** - 用于图像处理的专用网络

### 训练过程

- **训练模式 (`train()`)** - Dropout 和 BatchNorm 生效
- **评估模式 (`eval()`)** - Dropout 关闭，推理优化
- **梯度清零 (`zero_grad()`)** - 避免梯度累积

### 损失函数

- **MSELoss** - 回归任务的均方误差
- **CrossEntropyLoss** - 分类任务的交叉熵
- **Softmax** - 将 logits 转换为概率

## 🎪 实战案例

### 案例 1：线性回归预测房价

```python
# 数据生成
X = torch.rand(100, 1) * 10
y = 3.0 * X + 7.0 + torch.randn(100, 1)

# 模型定义
model = nn.Linear(in_features=1, out_features=1)

# 训练循环
criterion = nn.MSELoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.01)

for epoch in range(100):
    y_pred = model(X)
    loss = criterion(y_pred, y)
    
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
```

### 案例 2：自定义网络 (SimpleNet)

```python
class SimpleNet(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super().__init__()
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_dim, output_dim)
    
    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        return x
```

### 案例 3：批量加载数据

```python
from torch.utils.data import DataLoader, TensorDataset

train_dataset = TensorDataset(X_train, y_train)
test_dataset = TensorDataset(X_test, y_test)

train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=32)
```

## 📝 使用建议

### 🎓 对于初学者

1. **循序渐进** - 按照第 1 步到第 7 步的顺序学习
2. **动手实践** - 每个文件都有完整的示例代码，边学边练
3. **独立运行** - 每个文件都可以单独运行，便于学习

### 🚀 对于进阶者

1. **先理解原理** - 确保掌握每一步的基础概念
2. **尝试修改参数** - 测试不同的超参数 (学习率、隐藏层数等)
3. **探索实战项目** - 从图片检测开始，尝试视频处理
4. **拓展扩展** - 使用自己的数据微调检测器

### 🔧 对于开发者

1. **代码复用** - 借鉴每个文件中的共享组件
2. **架构参考** - 参考现有的项目结构构建自己的项目
3. **最佳实践** - 学习代码中的 Python 风格和 PyTorch 惯例

## 🎯 学习进度跟踪

| 阶段 | 文件 | 完成状态 | 掌握技能 |
|-------|------|-------------|---------------|
| 1️⃣ | `01_tensors.py` | ✅ | 张量基础操作 |
| 2️⃣ | `02_autograd.py` | ✅ | 自动微分原理 |
| 3️⃣ | `03_linear_regression.py` | ✅ | 训练循环流程 |
| 4️⃣ | `04_nn_module.py` | ✅ | 网络构建 |
| 5️⃣ | `05_classification.py` | ✅ | 分类任务 |
| 6️⃣ | `06_cnn_mnist.py` | ✅ | CNN 架构 |
| 7️⃣ | `07_save_load.py` | ✅ | 模型持久化 |
| 🎬 | `detect_image.py` | ✅ | 图片检测 |
| 🎬 | `detect_video.py` | ✅ | 视频处理 |
| 🎬 | `finetune_detector.py` | ✅ | 迁移学习 |

---

*📅 最终更新: 2026-07-17*
*🎓 专为 PyTorch 学习者打造，助您从零到岗！*

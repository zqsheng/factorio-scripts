# 🔥 PyTorch 学习路径 / PyTorch Learning Path

A progressive, hands-on guide to learning PyTorch for machine learning.
每个文件都可以独立运行 (`python3 <filename>`)。

## Prerequisites

```bash
pip3 install torch torchvision matplotlib numpy opencv-python
```

---

## Part 1: 基础教程 / Tutorials

| # | File | Topic | Key Concepts |
|---|------|-------|-------------|
| 1 | `01_tensors.py` | Tensors 基础 | 创建、索引、reshape、dtype、device |
| 2 | `02_autograd.py` | 自动微分 | `requires_grad`, `backward()`, 计算图 |
| 3 | `03_linear_regression.py` | 线性回归 | 手写训练循环、loss、optimizer |
| 4 | `04_nn_module.py` | nn.Module | 构建神经网络、Sequential、自定义层 |
| 5 | `05_classification.py` | 分类任务 | CrossEntropy、Softmax、accuracy |
| 6 | `06_cnn_mnist.py` | CNN 图像分类 | Conv2d、池化、MNIST 手写数字识别 |
| 7 | `07_save_load.py` | 模型保存与加载 | state_dict、checkpoint |

---

## Part 2: 实战项目 — 目标检测 / Object Detection Project

| File | Description | Key Concepts |
|------|------------|-------------|
| `detect_image.py` | 📷 图片检测 | 预训练 Faster R-CNN, 80 类 COCO 物体 |
| `detect_video.py` | 🎬 视频检测 | 逐帧推理, 跳帧加速, 类别过滤 |
| `finetune_detector.py` | 🎯 微调训练 | 迁移学习, 自定义 Dataset, 替换分类头 |

### Quick Start

```bash
# 检测图片 (自动下载示例图)
python3 detect_image.py

# 检测你自己的图片
python3 detect_image.py /path/to/your/photo.jpg

# 检测视频 (只检测人和车)
python3 detect_video.py /path/to/video.mp4 --classes person car

# 微调训练自己的检测器
python3 finetune_detector.py
```

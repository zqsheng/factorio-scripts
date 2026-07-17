"""
finetune_detector.py - 微调目标检测模型 (迁移学习)
===================================================
在预训练的 Faster R-CNN 基础上，微调检测你自己的自定义类别。

这个脚本演示完整的迁移学习流程:
  1. 自定义 Dataset (生成模拟数据用于演示)
  2. 修改模型输出头 (适配你的类别数)
  3. 训练循环
  4. 评估与推理

实际使用时，只需替换 Dataset 类来加载你自己的标注数据。

用法:
  python3 finetune_detector.py
"""

import os
import time
import torch
import torch.utils.data
import torchvision
from torchvision import transforms
from torchvision.models.detection import fasterrcnn_resnet50_fpn_v2, FasterRCNN_ResNet50_FPN_V2_Weights
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
from PIL import Image, ImageDraw
import random

print("=" * 60)
print("  🎯 Fine-tune Object Detector (迁移学习)")
print("=" * 60)


# ──────────────────────────────────────────────────────────
# 1. 自定义 Dataset
# ──────────────────────────────────────────────────────────
class SimpleShapeDataset(torch.utils.data.Dataset):
    """
    生成包含简单几何形状的图片用于演示。
    实际项目中替换为你自己的数据集。

    标注格式 (Faster R-CNN 要求):
        image: Tensor [C, H, W]
        target: dict {
            'boxes':  Tensor [N, 4]  格式 [x1, y1, x2, y2]
            'labels': Tensor [N]     类别 (从 1 开始, 0 是背景)
            'image_id': Tensor [1]
            'area':   Tensor [N]
            'iscrowd': Tensor [N]
        }
    """

    def __init__(self, num_samples=100, img_size=224):
        self.num_samples = num_samples
        self.img_size = img_size
        # 类别: 0=background, 1=circle, 2=rectangle
        self.class_names = ['__background__', 'circle', 'rectangle']

    def __len__(self):
        return self.num_samples

    def __getitem__(self, idx):
        # 生成随机背景图
        img = Image.new('RGB', (self.img_size, self.img_size),
                        color=(random.randint(200, 255),
                               random.randint(200, 255),
                               random.randint(200, 255)))
        draw = ImageDraw.Draw(img)

        boxes = []
        labels = []

        # 随机放 1~3 个形状
        num_objects = random.randint(1, 3)
        for _ in range(num_objects):
            # 随机位置和大小
            size = random.randint(30, 60)
            x1 = random.randint(0, self.img_size - size - 1)
            y1 = random.randint(0, self.img_size - size - 1)
            x2 = x1 + size
            y2 = y1 + size

            shape_type = random.choice([1, 2])  # 1=circle, 2=rectangle

            if shape_type == 1:  # Circle
                color = (random.randint(0, 100), random.randint(0, 100), 255)
                draw.ellipse([x1, y1, x2, y2], fill=color, outline='black', width=2)
            else:  # Rectangle
                color = (255, random.randint(0, 100), random.randint(0, 100))
                draw.rectangle([x1, y1, x2, y2], fill=color, outline='black', width=2)

            boxes.append([x1, y1, x2, y2])
            labels.append(shape_type)

        # 转换为 Tensor
        boxes = torch.as_tensor(boxes, dtype=torch.float32)
        labels = torch.as_tensor(labels, dtype=torch.int64)
        image_id = torch.tensor([idx])
        area = (boxes[:, 3] - boxes[:, 1]) * (boxes[:, 2] - boxes[:, 0])
        iscrowd = torch.zeros(len(boxes), dtype=torch.int64)

        target = {
            'boxes': boxes,
            'labels': labels,
            'image_id': image_id,
            'area': area,
            'iscrowd': iscrowd,
        }

        img_tensor = transforms.ToTensor()(img)
        return img_tensor, target


# ──────────────────────────────────────────────────────────
# 2. 修改模型 (迁移学习的关键)
# ──────────────────────────────────────────────────────────
print("\n📌 1. Modify Pre-trained Model")


def build_model(num_classes):
    """
    加载预训练的 Faster R-CNN, 替换分类头

    这就是迁移学习:
      - 保留骨干网络 (backbone) 的特征提取能力
      - 只替换最后的分类/回归头, 适配你的类别数
    """
    # 加载预训练模型
    weights = FasterRCNN_ResNet50_FPN_V2_Weights.DEFAULT
    model = fasterrcnn_resnet50_fpn_v2(weights=weights)

    # 获取分类头的输入特征数
    in_features = model.roi_heads.box_predictor.cls_score.in_features
    print(f"   Original predictor input features: {in_features}")

    # 替换分类头! (核心步骤)
    model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)
    print(f"   New predictor: {num_classes} classes (including background)")

    return model


NUM_CLASSES = 3  # background + circle + rectangle
model = build_model(NUM_CLASSES)

# ──────────────────────────────────────────────────────────
# 3. 设置训练
# ──────────────────────────────────────────────────────────
print("\n📌 2. Setup Training")

device = torch.device("cpu")  # 小数据集用 CPU 即可, 避免 MPS 兼容问题
# 如需 GPU: device = torch.device("mps") 或 "cuda"

model.to(device)

# 数据集
train_dataset = SimpleShapeDataset(num_samples=80)
val_dataset = SimpleShapeDataset(num_samples=20)

# DataLoader (注意: 目标检测的 collate_fn 比较特殊)
def collate_fn(batch):
    """目标检测数据的 collate: 不能简单 stack, 因为每张图的目标数不同"""
    return tuple(zip(*batch))

train_loader = torch.utils.data.DataLoader(
    train_dataset, batch_size=4, shuffle=True, collate_fn=collate_fn
)
val_loader = torch.utils.data.DataLoader(
    val_dataset, batch_size=4, shuffle=False, collate_fn=collate_fn
)

# 优化器: 只优化分类头 (可选: 也可以优化全部参数)
# 方法 A: 只训练新的分类头 (快, 适合小数据集)
# params = [p for p in model.roi_heads.box_predictor.parameters()]

# 方法 B: 训练全部参数, 但骨干用更小的学习率 (更好)
params = [
    {"params": [p for n, p in model.named_parameters()
                if "box_predictor" not in n and p.requires_grad],
     "lr": 0.0001},  # 骨干网络: 小学习率
    {"params": model.roi_heads.box_predictor.parameters(),
     "lr": 0.001},   # 分类头: 大学习率
]

optimizer = torch.optim.SGD(params, momentum=0.9, weight_decay=0.0005)

print(f"   Device: {device}")
print(f"   Train samples: {len(train_dataset)}")
print(f"   Val samples:   {len(val_dataset)}")
print(f"   Batch size: 4")

# ──────────────────────────────────────────────────────────
# 4. 训练循环
# ──────────────────────────────────────────────────────────
print("\n📌 3. Training")

NUM_EPOCHS = 5

for epoch in range(NUM_EPOCHS):
    model.train()  # 训练模式
    epoch_loss = 0.0

    for batch_idx, (images, targets) in enumerate(train_loader):
        images = [img.to(device) for img in images]
        targets = [{k: v.to(device) for k, v in t.items()} for t in targets]

        # Faster R-CNN 在训练模式下:
        #   输入: images + targets
        #   输出: loss_dict (包含各种损失)
        loss_dict = model(images, targets)

        # 总损失 = 分类损失 + 回归损失 + ...
        losses = sum(loss for loss in loss_dict.values())

        optimizer.zero_grad()
        losses.backward()
        optimizer.step()

        epoch_loss += losses.item()

    avg_loss = epoch_loss / len(train_loader)
    print(f"   Epoch {epoch + 1}/{NUM_EPOCHS}: loss={avg_loss:.4f}")

# ──────────────────────────────────────────────────────────
# 5. 推理测试
# ──────────────────────────────────────────────────────────
print("\n📌 4. Inference Test")

model.eval()
class_names = ['bg', 'circle', 'rectangle']

# 用验证集的第一张图测试
test_img, test_target = val_dataset[0]
test_img_device = test_img.to(device)

with torch.no_grad():
    prediction = model([test_img_device])

pred = prediction[0]
print(f"\n   Prediction results:")
print(f"   {'Class':<12s} {'Score':>8s}  {'Box (x1,y1,x2,y2)'}")
print(f"   {'─'*12} {'─'*8}  {'─'*25}")

for box, label, score in zip(pred['boxes'], pred['labels'], pred['scores']):
    if score > 0.5:
        b = box.cpu().tolist()
        print(f"   {class_names[label]:<12s} {score:.1%}  "
              f"[{b[0]:.0f}, {b[1]:.0f}, {b[2]:.0f}, {b[3]:.0f}]")

# Ground truth
print(f"\n   Ground truth:")
for box, label in zip(test_target['boxes'], test_target['labels']):
    b = box.tolist()
    print(f"   {class_names[label]:<12s}          "
          f"[{b[0]:.0f}, {b[1]:.0f}, {b[2]:.0f}, {b[3]:.0f}]")

# ──────────────────────────────────────────────────────────
# 6. 保存模型
# ──────────────────────────────────────────────────────────
print("\n📌 5. Save Model")

save_dir = "./saved_models"
os.makedirs(save_dir, exist_ok=True)
save_path = os.path.join(save_dir, "shape_detector.pth")

torch.save({
    'model_state_dict': model.state_dict(),
    'num_classes': NUM_CLASSES,
    'class_names': class_names,
}, save_path)

print(f"   ✅ Model saved to: {save_path}")

# ──────────────────────────────────────────────────────────
# 7. 加载并使用模型
# ──────────────────────────────────────────────────────────
print("\n📌 6. Load & Use Saved Model")

checkpoint = torch.load(save_path, weights_only=False)
loaded_model = build_model(checkpoint['num_classes'])
loaded_model.load_state_dict(checkpoint['model_state_dict'])
loaded_model.eval()
print(f"   ✅ Loaded model with classes: {checkpoint['class_names']}")

# ──────────────────────────────────────────────────────────
# 总结
# ──────────────────────────────────────────────────────────
print("""
📝 迁移学习总结:

  ┌─────────────────────────────────────────────────┐
  │  1. 加载预训练模型                               │
  │     model = fasterrcnn_resnet50_fpn_v2(          │
  │         weights="DEFAULT")                       │
  │                                                  │
  │  2. 替换分类头                                   │
  │     in_features = model.roi_heads                │
  │         .box_predictor.cls_score.in_features     │
  │     model.roi_heads.box_predictor =              │
  │         FastRCNNPredictor(in_features, N_CLASSES)│
  │                                                  │
  │  3. 训练 (模型自动计算 loss)                     │
  │     loss_dict = model(images, targets)           │
  │     loss = sum(loss_dict.values())               │
  │                                                  │
  │  4. 推理                                         │
  │     model.eval()                                 │
  │     predictions = model([image])                 │
  └─────────────────────────────────────────────────┘

  要检测你自己的物体:
    1. 标注数据 (推荐工具: LabelImg, Roboflow)
    2. 写 Dataset 类, 返回 image + target dict
    3. 运行这个脚本, 替换 SimpleShapeDataset

✅ finetune_detector.py 完成！
🎉 恭喜！你已经掌握了完整的目标检测流程！
""")

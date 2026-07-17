"""
detect_image.py - 用预训练模型检测图片中的物体
================================================
使用 torchvision 自带的 Faster R-CNN 模型，
无需训练，直接检测 COCO 数据集的 80 种物体。

用法:
  python3 detect_image.py <image_path>
  python3 detect_image.py              # 使用内置示例图片

输出:
  在 output/ 目录下生成标注后的图片
"""

import sys
import os
import torch
import torchvision
from torchvision import transforms
from torchvision.models.detection import fasterrcnn_resnet50_fpn_v2, FasterRCNN_ResNet50_FPN_V2_Weights
from PIL import Image, ImageDraw, ImageFont
import time

# ──────────────────────────────────────────────────────────
# COCO 数据集 80 类标签
# ──────────────────────────────────────────────────────────
COCO_LABELS = [
    '__background__', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus',
    'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'N/A', 'stop sign',
    'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
    'elephant', 'bear', 'zebra', 'giraffe', 'N/A', 'backpack', 'umbrella', 'N/A',
    'N/A', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard',
    'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard',
    'surfboard', 'tennis racket', 'bottle', 'N/A', 'wine glass', 'cup', 'fork',
    'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange', 'broccoli',
    'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch',
    'potted plant', 'bed', 'N/A', 'dining table', 'N/A', 'N/A', 'toilet', 'N/A',
    'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone', 'microwave',
    'oven', 'toaster', 'sink', 'refrigerator', 'N/A', 'book', 'clock', 'vase',
    'scissors', 'teddy bear', 'hair drier', 'toothbrush',
]

# 每个类别一个颜色 (方便区分)
COLORS = [
    (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255),
    (0, 255, 255), (128, 0, 0), (0, 128, 0), (0, 0, 128), (128, 128, 0),
    (128, 0, 128), (0, 128, 128), (255, 128, 0), (255, 0, 128), (128, 255, 0),
    (0, 255, 128), (128, 0, 255), (0, 128, 255), (255, 128, 128), (128, 255, 128),
]


def get_device():
    """自动选择最佳计算设备"""
    if torch.backends.mps.is_available():
        return torch.device("mps")
    elif torch.cuda.is_available():
        return torch.device("cuda")
    return torch.device("cpu")


def load_model(device):
    """加载预训练的 Faster R-CNN 模型"""
    print("📦 Loading Faster R-CNN model (first time will download ~170MB)...")
    t0 = time.time()

    weights = FasterRCNN_ResNet50_FPN_V2_Weights.DEFAULT
    model = fasterrcnn_resnet50_fpn_v2(weights=weights)
    model.to(device)
    model.eval()  # 推理模式

    print(f"   ✅ Model loaded in {time.time() - t0:.1f}s on {device}")
    return model, weights


def detect(model, image_path, device, confidence_threshold=0.5):
    """
    对一张图片进行目标检测

    Args:
        model: Faster R-CNN 模型
        image_path: 图片路径
        device: 计算设备
        confidence_threshold: 置信度阈值 (0~1), 低于此值的检测结果会被过滤

    Returns:
        image: PIL Image (原图)
        results: list of dict, 每个 dict 包含 box, label, score
    """
    # 1. 加载图片
    image = Image.open(image_path).convert("RGB")
    print(f"\n🖼️  Image: {image_path} ({image.width}x{image.height})")

    # 2. 预处理: PIL Image → Tensor
    transform = transforms.Compose([
        transforms.ToTensor(),  # [0,255] → [0.0,1.0], HWC → CHW
    ])
    img_tensor = transform(image).to(device)

    # 3. 推理
    t0 = time.time()
    with torch.no_grad():
        predictions = model([img_tensor])
    inference_time = time.time() - t0

    # 4. 解析结果
    pred = predictions[0]
    # pred 包含:
    #   'boxes':  Tensor [N, 4]  每个框 [x1, y1, x2, y2]
    #   'labels': Tensor [N]     类别索引
    #   'scores': Tensor [N]     置信度

    results = []
    for box, label, score in zip(pred['boxes'], pred['labels'], pred['scores']):
        if score >= confidence_threshold:
            results.append({
                'box': box.cpu().tolist(),       # [x1, y1, x2, y2]
                'label': COCO_LABELS[label],      # 类别名
                'label_id': label.item(),          # 类别 ID
                'score': score.item(),             # 置信度
            })

    print(f"   ⏱️  Inference: {inference_time:.3f}s")
    print(f"   🎯 Detected {len(results)} objects (threshold={confidence_threshold})")

    return image, results


def draw_results(image, results, output_path):
    """在图片上绘制检测框和标签"""
    draw = ImageDraw.Draw(image)

    # 尝试加载字体 (macOS)
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 16)
        font_small = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 12)
    except (OSError, IOError):
        font = ImageFont.load_default()
        font_small = font

    for det in results:
        x1, y1, x2, y2 = det['box']
        label = det['label']
        score = det['score']
        color = COLORS[det['label_id'] % len(COLORS)]

        # 画框
        draw.rectangle([x1, y1, x2, y2], outline=color, width=3)

        # 画标签背景
        text = f"{label} {score:.0%}"
        bbox = draw.textbbox((x1, y1), text, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        draw.rectangle([x1, y1 - text_h - 6, x1 + text_w + 6, y1], fill=color)
        draw.text((x1 + 3, y1 - text_h - 4), text, fill="white", font=font)

    # 保存
    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
    image.save(output_path)
    print(f"   💾 Saved: {output_path}")
    return image


def create_sample_image():
    """生成一张测试图片 (如果没有提供图片)"""
    sample_dir = "./sample_images"
    os.makedirs(sample_dir, exist_ok=True)
    sample_path = os.path.join(sample_dir, "sample.jpg")

    if not os.path.exists(sample_path):
        print("🎨 Generating sample image...")
        # 用 torchvision 内置的测试图片
        try:
            from torchvision.io import read_image
            # 使用 torchvision 内置数据集的一张图
            from torchvision.datasets import VOCDetection
            ds = VOCDetection(root='./data', year='2007', image_set='train',
                              download=True)
            img = ds[0][0]
            img.save(sample_path)
        except Exception:
            # 回退: 生成一张有物体的合成图片
            import random
            img = Image.new('RGB', (640, 480), color=(135, 206, 235))  # 天空蓝背景
            draw = ImageDraw.Draw(img)
            # 画一些形状模拟场景
            draw.rectangle([50, 200, 200, 450], fill=(139, 69, 19))    # 棕色 "建筑"
            draw.rectangle([250, 150, 450, 450], fill=(105, 105, 105)) # 灰色 "建筑"
            draw.rectangle([480, 250, 600, 450], fill=(160, 82, 45))   # 另一个
            draw.ellipse([100, 50, 200, 150], fill=(255, 255, 0))      # 太阳
            draw.rectangle([0, 450, 640, 480], fill=(34, 139, 34))     # 草地
            img.save(sample_path)
            print(f"   ℹ️  Generated synthetic image (for real results, provide your own photo)")

        print(f"   ✅ Saved to {sample_path}")

    return sample_path


# ──────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("  🔍 Object Detection with Faster R-CNN")
    print("=" * 60)

    # 获取图片路径
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
    else:
        print("\n  Usage: python3 detect_image.py <image_path>")
        print("  No image provided, downloading a sample...\n")
        image_path = create_sample_image()

    if not os.path.exists(image_path):
        print(f"  ❌ File not found: {image_path}")
        sys.exit(1)

    # 加载模型
    device = get_device()
    model, weights = load_model(device)

    # 检测
    image, results = detect(model, image_path, device, confidence_threshold=0.5)

    # 打印结果
    print(f"\n   Detection Results:")
    print(f"   {'Label':<20s} {'Score':>8s}  {'Box (x1,y1,x2,y2)'}")
    print(f"   {'─'*20} {'─'*8}  {'─'*30}")
    for det in results:
        box = det['box']
        print(f"   {det['label']:<20s} {det['score']:>7.1%}  "
              f"[{box[0]:.0f}, {box[1]:.0f}, {box[2]:.0f}, {box[3]:.0f}]")

    # 画结果
    basename = os.path.splitext(os.path.basename(image_path))[0]
    output_path = f"./output/{basename}_detected.jpg"
    draw_results(image, results, output_path)

    print(f"\n✅ Done! Open {output_path} to see the results.")

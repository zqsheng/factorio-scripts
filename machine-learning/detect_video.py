"""
detect_video.py - 实时视频目标检测
====================================
用 Faster R-CNN 对视频逐帧检测，输出标注后的视频。
这个脚本替代你之前 object-detect.person.py 中的 placeholder 逻辑。

用法:
  python3 detect_video.py <video_path>               # 检测视频文件
  python3 detect_video.py <video_path> --show         # 边检测边显示
  python3 detect_video.py <video_path> --classes person car  # 只检测指定类别

输出:
  output/<video_name>_detected.mp4
"""

import sys
import os
import argparse
import time
import torch
import torchvision
from torchvision import transforms
from torchvision.models.detection import fasterrcnn_resnet50_fpn_v2, FasterRCNN_ResNet50_FPN_V2_Weights
from PIL import Image, ImageDraw, ImageFont
import numpy as np

try:
    import cv2
    HAS_CV2 = True
except ImportError:
    HAS_CV2 = False
    print("⚠️  OpenCV not installed. Install with: pip3 install opencv-python")

# COCO 80 类标签
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

COLORS = [
    (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255),
    (0, 255, 255), (128, 0, 0), (0, 128, 0), (0, 0, 128), (128, 128, 0),
    (128, 0, 128), (0, 128, 128), (255, 128, 0), (255, 0, 128), (128, 255, 0),
    (0, 255, 128), (128, 0, 255), (0, 128, 255), (255, 128, 128), (128, 255, 128),
]


def get_device():
    if torch.backends.mps.is_available():
        return torch.device("mps")
    elif torch.cuda.is_available():
        return torch.device("cuda")
    return torch.device("cpu")


def load_model(device):
    """加载 Faster R-CNN 模型"""
    print("📦 Loading Faster R-CNN model...")
    t0 = time.time()
    weights = FasterRCNN_ResNet50_FPN_V2_Weights.DEFAULT
    model = fasterrcnn_resnet50_fpn_v2(weights=weights)
    model.to(device)
    model.eval()
    print(f"   ✅ Loaded in {time.time() - t0:.1f}s on {device}")
    return model


def detect_frame(model, frame_bgr, device, threshold=0.5, target_classes=None):
    """
    对一帧 BGR 图像进行检测

    Args:
        model: 检测模型
        frame_bgr: OpenCV BGR 格式的图像 (numpy array)
        device: 计算设备
        threshold: 置信度阈值
        target_classes: 只检测指定类别 (list of str), None 表示所有

    Returns:
        detections: list of dict {box, label, score, color}
    """
    # BGR → RGB → Tensor
    frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
    img_tensor = transforms.ToTensor()(frame_rgb).to(device)

    with torch.no_grad():
        predictions = model([img_tensor])

    pred = predictions[0]
    detections = []

    for box, label_id, score in zip(pred['boxes'], pred['labels'], pred['scores']):
        if score < threshold:
            continue

        label_name = COCO_LABELS[label_id]

        # 如果指定了类别过滤
        if target_classes and label_name not in target_classes:
            continue

        detections.append({
            'box': box.cpu().numpy().astype(int),  # [x1, y1, x2, y2]
            'label': label_name,
            'score': score.item(),
            'color': COLORS[label_id.item() % len(COLORS)],
        })

    return detections


def draw_detections(frame, detections):
    """在帧上绘制检测结果 (使用 OpenCV)"""
    for det in detections:
        x1, y1, x2, y2 = det['box']
        color = det['color']
        label = f"{det['label']} {det['score']:.0%}"

        # 画框
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

        # 画标签背景
        (text_w, text_h), baseline = cv2.getTextSize(
            label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2
        )
        cv2.rectangle(frame, (x1, y1 - text_h - 10), (x1 + text_w + 4, y1), color, -1)
        cv2.putText(frame, label, (x1 + 2, y1 - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    return frame


def process_video(video_path, output_path, model, device,
                  threshold=0.5, target_classes=None,
                  show=False, skip_frames=0):
    """
    处理整个视频

    Args:
        video_path: 输入视频路径
        output_path: 输出视频路径
        model: 检测模型
        device: 计算设备
        threshold: 置信度阈值
        target_classes: 类别过滤
        show: 是否实时显示
        skip_frames: 每 N 帧检测一次 (跳帧加速)
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"❌ Cannot open video: {video_path}")
        return

    # 获取视频信息
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    print(f"\n🎬 Video: {video_path}")
    print(f"   Resolution: {width}x{height}, FPS: {fps}, Frames: {total_frames}")

    # 输出视频
    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    frame_count = 0
    total_detections = 0
    start_time = time.time()
    last_detections = []  # 跳帧时复用上一次的检测结果

    print(f"   Processing{'  (press q to stop)' if show else ''}...")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1

        # 跳帧: 每 skip_frames+1 帧检测一次
        if skip_frames > 0 and frame_count % (skip_frames + 1) != 1:
            detections = last_detections
        else:
            detections = detect_frame(model, frame, device, threshold, target_classes)
            last_detections = detections

        total_detections += len(detections)

        # 绘制
        annotated = draw_detections(frame.copy(), detections)

        # 添加帧信息
        elapsed = time.time() - start_time
        processing_fps = frame_count / elapsed if elapsed > 0 else 0
        info = f"Frame {frame_count}/{total_frames} | {processing_fps:.1f} FPS | {len(detections)} objects"
        cv2.putText(annotated, info, (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        writer.write(annotated)

        # 实时显示
        if show:
            cv2.imshow("Object Detection", annotated)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("   ⏹️  Stopped by user")
                break

        # 进度
        if frame_count % 30 == 0:
            progress = frame_count / total_frames * 100
            print(f"   [{progress:5.1f}%] Frame {frame_count}/{total_frames}, "
                  f"FPS: {processing_fps:.1f}")

    # 清理
    cap.release()
    writer.release()
    if show:
        cv2.destroyAllWindows()

    elapsed = time.time() - start_time
    print(f"\n   ✅ Done!")
    print(f"   Processed: {frame_count} frames in {elapsed:.1f}s ({frame_count/elapsed:.1f} FPS)")
    print(f"   Total detections: {total_detections}")
    print(f"   Output: {output_path}")


# ──────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    if not HAS_CV2:
        print("❌ OpenCV required. Install: pip3 install opencv-python")
        sys.exit(1)

    parser = argparse.ArgumentParser(description="Video Object Detection with Faster R-CNN")
    parser.add_argument("video", help="Path to input video file")
    parser.add_argument("--threshold", type=float, default=0.5,
                        help="Detection confidence threshold (default: 0.5)")
    parser.add_argument("--classes", nargs="+", default=None,
                        help="Only detect specific classes, e.g. --classes person car")
    parser.add_argument("--show", action="store_true",
                        help="Show real-time detection window")
    parser.add_argument("--skip", type=int, default=2,
                        help="Skip frames for speed (default: 2, detect every 3rd frame)")
    parser.add_argument("--output", default=None,
                        help="Output video path (default: output/<name>_detected.mp4)")

    args = parser.parse_args()

    if not os.path.exists(args.video):
        print(f"❌ Video not found: {args.video}")
        sys.exit(1)

    print("=" * 60)
    print("  🎬 Video Object Detection")
    print("=" * 60)

    # 输出路径
    if args.output:
        output_path = args.output
    else:
        basename = os.path.splitext(os.path.basename(args.video))[0]
        output_path = f"./output/{basename}_detected.mp4"

    # 加载模型
    device = get_device()
    model = load_model(device)

    if args.classes:
        print(f"\n   🏷️  Filtering classes: {args.classes}")

    # 处理视频
    process_video(
        video_path=args.video,
        output_path=output_path,
        model=model,
        device=device,
        threshold=args.threshold,
        target_classes=args.classes,
        show=args.show,
        skip_frames=args.skip,
    )

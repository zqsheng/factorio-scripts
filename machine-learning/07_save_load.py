"""
07_save_load.py - 模型保存与加载
================================
训练好的模型需要保存下来，下次直接加载使用。

关键概念:
  - state_dict: 模型的所有可学习参数
  - torch.save / torch.load
  - Checkpoint: 保存训练中间状态 (可恢复训练)
"""

import os
import torch
import torch.nn as nn

print("=" * 60)
print("  07 - SAVE & LOAD (模型保存与加载)")
print("=" * 60)

SAVE_DIR = "./saved_models"
os.makedirs(SAVE_DIR, exist_ok=True)

# ──────────────────────────────────────────────────────────
# 1. 创建一个示例模型
# ──────────────────────────────────────────────────────────
print("\n📌 1. Create Model")


class DemoNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(10, 32)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(32, 3)

    def forward(self, x):
        return self.fc2(self.relu(self.fc1(x)))


model = DemoNet()
print(f"  Model: {model}")

# ──────────────────────────────────────────────────────────
# 2. 理解 state_dict
# ──────────────────────────────────────────────────────────
print("\n📌 2. Understanding state_dict")

# state_dict 是一个 OrderedDict, 映射参数名 -> 参数值
state = model.state_dict()
print(f"  state_dict keys:")
for key, value in state.items():
    print(f"    {key:15s} shape={list(value.shape)}")

# ──────────────────────────────────────────────────────────
# 3. 方法 A: 保存 state_dict (✅ 推荐)
# ──────────────────────────────────────────────────────────
print("\n📌 3. Method A: Save state_dict (Recommended)")

# 保存
path_a = os.path.join(SAVE_DIR, "model_state.pth")
torch.save(model.state_dict(), path_a)
print(f"  ✅ Saved state_dict to: {path_a}")

# 加载: 先创建模型, 再加载参数
loaded_model = DemoNet()  # 必须知道模型结构!
loaded_model.load_state_dict(torch.load(path_a, weights_only=True))
loaded_model.eval()  # 设为推理模式

# 验证: 两个模型输出应该一样
test_input = torch.randn(1, 10)
with torch.no_grad():
    orig_out = model(test_input)
    load_out = loaded_model(test_input)
    print(f"  Original output:  {orig_out}")
    print(f"  Loaded output:    {load_out}")
    print(f"  Match: {torch.allclose(orig_out, load_out)}")

# ──────────────────────────────────────────────────────────
# 4. 方法 B: 保存整个模型 (⚠️ 不推荐)
# ──────────────────────────────────────────────────────────
print("\n📌 4. Method B: Save Entire Model (Not Recommended)")
print("""
  torch.save(model, 'model.pth')       # 保存整个对象
  model = torch.load('model.pth')      # 加载

  ⚠️ 问题:
    - 依赖 pickle, 和代码结构绑定
    - 如果改了类定义或文件路径, 加载会失败
    - 不安全: pickle 可以执行任意代码

  ✅ 始终用方法 A (state_dict) !
""")

# ──────────────────────────────────────────────────────────
# 5. Checkpoint: 保存训练状态 (可恢复训练)
# ──────────────────────────────────────────────────────────
print("📌 5. Checkpoint (Resume Training)")

# 模拟训练
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# 假设训练到 epoch 15 时保存 checkpoint
current_epoch = 15
current_loss = 0.0342

checkpoint_path = os.path.join(SAVE_DIR, "checkpoint.pth")
torch.save({
    'epoch': current_epoch,
    'model_state_dict': model.state_dict(),
    'optimizer_state_dict': optimizer.state_dict(),
    'loss': current_loss,
    # 可以加任何你需要的信息
    'learning_rate': 0.001,
    'config': {'hidden_dim': 32, 'num_classes': 3},
}, checkpoint_path)
print(f"  ✅ Saved checkpoint at epoch {current_epoch}")

# 恢复训练
print(f"\n  Loading checkpoint...")
checkpoint = torch.load(checkpoint_path, weights_only=False)

resume_model = DemoNet()
resume_optimizer = torch.optim.Adam(resume_model.parameters())

resume_model.load_state_dict(checkpoint['model_state_dict'])
resume_optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
resume_epoch = checkpoint['epoch']
resume_loss = checkpoint['loss']

print(f"  Resumed from epoch {resume_epoch}, loss={resume_loss}")
print(f"  Config: {checkpoint['config']}")

# 继续训练从 epoch 16 开始
print(f"  Continue training from epoch {resume_epoch + 1}...")

# ──────────────────────────────────────────────────────────
# 6. 设备间转移
# ──────────────────────────────────────────────────────────
print("\n📌 6. Cross-Device Loading")
print("""
  # 在 GPU 上保存, 在 CPU 上加载:
  model.load_state_dict(
      torch.load('model.pth', map_location='cpu', weights_only=True)
  )

  # 加载后移到目标设备:
  model.to(device)

  map_location 常用值:
    'cpu'         → 加载到 CPU
    'cuda:0'      → 加载到第 0 个 GPU
    'mps'         → 加载到 Apple Silicon GPU
    torch.device() → 加载到指定设备
""")

# ──────────────────────────────────────────────────────────
# 7. 总结
# ──────────────────────────────────────────────────────────
print("📌 7. Summary")
print("""
  ┌─────────────────────────────────────────────────────┐
  │  保存模型参数 (推荐):                               │
  │    torch.save(model.state_dict(), 'model.pth')      │
  │                                                     │
  │  加载模型参数:                                      │
  │    model = MyModel()                                │
  │    model.load_state_dict(torch.load('model.pth'))   │
  │    model.eval()                                     │
  │                                                     │
  │  保存 Checkpoint (可恢复训练):                      │
  │    torch.save({                                     │
  │        'epoch': epoch,                              │
  │        'model_state_dict': model.state_dict(),      │
  │        'optimizer_state_dict': opt.state_dict(),    │
  │        'loss': loss,                                │
  │    }, 'checkpoint.pth')                             │
  └─────────────────────────────────────────────────────┘
""")

# 清理
import shutil
if os.path.exists(SAVE_DIR):
    shutil.rmtree(SAVE_DIR)
    print(f"  🧹 Cleaned up {SAVE_DIR}")

print("\n✅ 07_save_load.py 完成！")
print("   🎉 恭喜！你已经完成了 PyTorch 基础学习路径！")
print("\n   接下来可以探索:")
print("     - 迁移学习 (Transfer Learning)")
print("     - Transformer / Attention")
print("     - GAN (生成对抗网络)")
print("     - 强化学习 (Reinforcement Learning)")

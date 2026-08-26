"""
09_rnn_demo.py - Recurrent Neural Network (RNN) Demo
===================================================
一个简单且可运行的循环神经网络示例：
  - 输入：长度固定的二值序列
  - 目标：判断序列中 1 的数量是否超过阈值
  - 模型：PyTorch 中的 nn.RNN

特点：
  - 不依赖大型数据集
  - 适合学习 RNN 的输入/输出形状和训练流程
  - 代码可以直接运行，输出训练结果和示例预测
"""

import torch
from torch import nn

torch.manual_seed(42)

print("=" * 70)
print("  09 - Recurrent Neural Network (RNN) Demo")
print("=" * 70)


class SimpleRNN(nn.Module):
    """一个很小的 RNN 分类器。"""

    def __init__(self, input_size=1, hidden_size=16, output_size=1):
        super().__init__()
        self.rnn = nn.RNN(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=2,
            batch_first=True,
            nonlinearity="tanh",
        )
        self.head = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        # x shape: [batch, seq_len, input_size]
        rnn_out, _ = self.rnn(x)
        # 取最后一个时间步的输出作为序列表示
        last_step = rnn_out[:, -1, :]
        return self.head(last_step).squeeze(-1)


# ──────────────────────────────────────────────────────────
# 1. 生成一个小型数据集
# ──────────────────────────────────────────────────────────
sequence_length = 8
num_samples = 512

X = torch.randint(0, 2, (num_samples, sequence_length, 1), dtype=torch.float32)
y = (X.sum(dim=1).squeeze(-1) > 4).float()

# 训练集 / 验证集
train_x = X[:420]
train_y = y[:420]
val_x = X[420:]
val_y = y[420:]

print("\n📌 1. Dataset")
print(f"  Sequence length: {sequence_length}")
print(f"  Train samples:   {train_x.shape[0]}")
print(f"  Val samples:     {val_x.shape[0]}")
print(f"  Example sequence: {X[0].squeeze(-1).tolist()}")
print(f"  Example label:    {int(y[0].item())} (1 means > 4 ones)")

# ──────────────────────────────────────────────────────────
# 2. 创建模型与训练器
# ──────────────────────────────────────────────────────────
model = SimpleRNN(input_size=1, hidden_size=16, output_size=1)
criterion = nn.BCEWithLogitsLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

print("\n📌 2. Training")
for epoch in range(200):
    model.train()
    logits = model(train_x)
    loss = criterion(logits, train_y)

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    if (epoch + 1) % 25 == 0 or epoch == 0:
        model.eval()
        with torch.no_grad():
            train_pred = (torch.sigmoid(model(train_x)) >= 0.5).float()
            train_acc = (train_pred == train_y).float().mean().item()

            val_pred = (torch.sigmoid(model(val_x)) >= 0.5).float()
            val_acc = (val_pred == val_y).float().mean().item()

        print(
            f"  Epoch {epoch + 1:3d} | loss={loss.item():.4f} | "
            f"train_acc={train_acc:.3f} | val_acc={val_acc:.3f}"
        )

# ──────────────────────────────────────────────────────────
# 3. 评估一组示例
# ──────────────────────────────────────────────────────────
print("\n📌 3. Demo inference")
model.eval()
examples = torch.tensor(
    [
        [[0.0], [1.0], [1.0], [0.0], [1.0], [1.0], [0.0], [0.0]],
        [[1.0], [0.0], [0.0], [0.0], [0.0], [1.0], [0.0], [1.0]],
        [[1.0], [1.0], [1.0], [1.0], [1.0], [0.0], [0.0], [0.0]],
    ],
    dtype=torch.float32,
)

with torch.no_grad():
    probs = torch.sigmoid(model(examples))

for i, seq in enumerate(examples):
    seq_list = seq.squeeze(-1).tolist()
    prob = probs[i].item()
    pred = 1 if prob >= 0.5 else 0
    print(f"  Sequence {i + 1}: {seq_list} -> prob={prob:.3f}, pred={pred}")

print("\n✅ RNN demo completed.")
print("   Concept: the RNN reads the sequence step by step and keeps a hidden state.")
print("   This is the core idea behind time-series, text, and speech models.")

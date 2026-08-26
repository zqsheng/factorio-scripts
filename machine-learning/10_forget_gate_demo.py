"""
10_forget_gate_demo.py - LSTM Forget Gate (遗忘门) Demo
=======================================================
LSTM 的遗忘门 f_t 决定"要不要忘掉"上一时刻的长期记忆 c_{t-1}:

    f_t = σ(W_f · [h_{t-1}, x_t] + b_f)
    c_t = f_t ⊙ c_{t-1} + i_t ⊙ g_t      (f_t≈1 保留旧记忆, f_t≈0 清空旧记忆)

内容：
  1. 遗忘门公式与直觉 (含手算例子)
  2. 手写遗忘门计算
  3. 手写一个完整 LSTM 单元 (含 输入门/遗忘门/候选/输出门)
  4. 训练一个"记忆 + 重置"任务, 观察遗忘门随时间的开关
  5. 与 PyTorch 官方 nn.LSTMCell 逐位对比, 证明手写公式正确

特点：
  - 不依赖大型数据集, 直接运行即可看到遗忘门在工作
  - 适合理解 RNN -> LSTM 的核心改进: 独立的长期记忆通道 c_t
"""

import torch
from torch import nn

torch.manual_seed(42)

print("=" * 70)
print("  10 - LSTM Forget Gate Demo (遗忘门)")
print("=" * 70)

# ══════════════════════════════════════════════════════════════
# 1. 遗忘门公式与直觉
# ══════════════════════════════════════════════════════════════
print("""
📌 1. Forget gate formula

    RNN (普通循环网络) 只有一个隐藏态 h, 每一步都被新信息覆盖,
    所以"记不住"太久之前的事。

    LSTM 多出一条"传送带"——细胞状态 c_t (长期记忆):

        ┌─────────────────────────────────────────────┐
        │  c_{t-1} ──⊙──────────────────────→ c_t      │
        │             │       (逐元素相乘)              │
        │             │                                │
        │             f_t = σ(W_f·[h_{t-1}, x_t]+b_f)   │  ← 遗忘门
        │                                             │
        │  x_t ──→ [ 输入门 i_t, 候选 g_t ] ─→ ⊕ ──→ c_t│
        │  h_{t-1} ─→ [ 输出门 o_t ] ──→ h_t           │
        └─────────────────────────────────────────────┘

    c_t = f_t ⊙ c_{t-1} + i_t ⊙ g_t

      f_t ≈ 1  → 保留旧记忆 (信息继续留在传送带上)
      f_t ≈ 0  → 清空旧记忆 (重新开始)

    sigmoid 把任何实数压到 (0,1), 正好当作"开关/比例"使用。
""")

# ══════════════════════════════════════════════════════════════
# 2. 手写遗忘门计算
# ══════════════════════════════════════════════════════════════
print("📌 2. Hand-written forget gate")

input_size, hidden_size = 2, 1
W_fh = torch.tensor([[1.2]])          # h_{t-1} 对 f_t 的权重
W_fx = torch.tensor([[1.0, -10.0]])   # x_t = [信息, 重置信号] 对 f_t 的权重
b_f = torch.tensor([0.5])


def forget_gate(x_t, h_prev):
    """f_t = σ(h_{t-1}·W_fh + x_t·W_fx + b_f)"""
    return torch.sigmoid(h_prev @ W_fh.T + x_t @ W_fx.T + b_f)


h_prev = torch.tensor([[1.0]])

# 情况 A: 只有信息, 没有重置信号 → 应该保留记忆
x_keep = torch.tensor([[1.0, 0.0]])
# 情况 B: 出现重置信号 → 应该清空记忆
x_reset = torch.tensor([[0.0, 1.0]])

f_keep = forget_gate(x_keep, h_prev).item()
f_reset = forget_gate(x_reset, h_prev).item()
print(f"  x=[信息, 重置]   f_t = σ(...)        结论")
print(f"  {x_keep.squeeze().tolist()}         f={f_keep:.4f}      → 保留记忆 (f≈1)")
print(f"  {x_reset.squeeze().tolist()}      f={f_reset:.4f}      → 清空记忆 (f≈0)")
print(f"  例: c_old=0.8 时  c_new = f*c_old = {f_keep * 0.8:.3f} / {f_reset * 0.8:.3f}")

# ══════════════════════════════════════════════════════════════
# 3. 手写完整 LSTM 单元
# ══════════════════════════════════════════════════════════════
print("\n📌 3. Hand-written LSTM cell (4 gates: i, f, g, o)")


class ManualLSTMCell(nn.Module):
    """手写 LSTM 单元。PyTorch 参数排布顺序: 输入门 i, 遗忘门 f, 候选 g, 输出门 o。"""

    def __init__(self, input_size, hidden_size):
        super().__init__()
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.W_ih = nn.Parameter(torch.randn(4 * hidden_size, input_size) * 0.2)
        self.b_ih = nn.Parameter(torch.zeros(4 * hidden_size))
        self.W_hh = nn.Parameter(torch.randn(4 * hidden_size, hidden_size) * 0.2)
        self.b_hh = nn.Parameter(torch.zeros(4 * hidden_size))

    def forward(self, x_t, state):
        """x_t: [batch, input], state = (h, c); 返回 h_new, state, f (遗忘门激活)"""
        h, c = state
        gates = x_t @ self.W_ih.T + self.b_ih + h @ self.W_hh.T + self.b_hh
        H = self.hidden_size
        i = torch.sigmoid(gates[:, 0:H])       # 输入门
        f = torch.sigmoid(gates[:, H:2 * H])   # 遗忘门 ★
        g = torch.tanh(gates[:, 2 * H:3 * H])  # 候选记忆
        o = torch.sigmoid(gates[:, 3 * H:])    # 输出门

        c_new = f * c + i * g                  # 更新长期记忆
        h_new = o * torch.tanh(c_new)          # 更新输出
        return h_new, (h_new, c_new), f


class ManualLSTM(nn.Module):
    """手写 LSTM + 线性输出头, 顺带记录每一步的遗忘门激活值。"""

    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.cell = ManualLSTMCell(input_size, hidden_size)
        self.head = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        # x: [batch, seq_len, input_size]
        batch, seq_len, _ = x.shape
        h = torch.zeros(batch, self.cell.hidden_size)
        c = torch.zeros(batch, self.cell.hidden_size)
        outs, forgets = [], []
        for t in range(seq_len):
            h, (h, c), f = self.cell(x[:, t], (h, c))
            outs.append(self.head(h))
            forgets.append(f)
        return torch.stack(outs, dim=1).squeeze(-1), torch.stack(forgets, dim=1)


# ══════════════════════════════════════════════════════════════
# 4. 训练 "记忆 + 重置" 任务
# ══════════════════════════════════════════════════════════════
print("\n📌 4. Train on a memorize-and-reset task")

# 输入每个时刻是 [bit, control]:
#   control = +1  → 把 bit 写入记忆
#   control = -1  → 重置记忆为 0
#   control =  0  → 保持现状
# 目标: 每个时刻输出当前记忆里的 bit (0 或 1)
seq_len = 8
num_samples = 2048
b1 = torch.randint(0, 2, (num_samples, 1)).float()
b2 = torch.randint(0, 2, (num_samples, 1)).float()

X = torch.zeros(num_samples, seq_len, 2)
Y = torch.zeros(num_samples, seq_len)

X[:, 0, 0] = b1.squeeze(1)   # 写 b1
X[:, 0, 1] = 1.0
Y[:, 0] = b1.squeeze(1)
Y[:, 1:4] = b1               # 步骤 1-3: 记住 b1
X[:, 4, 1] = -1.0            # 步骤 4: 重置
Y[:, 4] = 0.0
X[:, 5, 0] = b2.squeeze(1)   # 写 b2
X[:, 5, 1] = 1.0
Y[:, 5] = b2.squeeze(1)
Y[:, 6:8] = b2               # 步骤 6-7: 记住 b2

model = ManualLSTM(input_size=2, hidden_size=8, output_size=1)
criterion = nn.BCEWithLogitsLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

for epoch in range(400):
    logits, _ = model(X)
    loss = criterion(logits, Y)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    if (epoch + 1) % 100 == 0:
        with torch.no_grad():
            pred = (torch.sigmoid(logits) >= 0.5).float()
            acc = (pred == Y).float().mean().item()
        print(f"  Epoch {epoch + 1:3d} | loss={loss.item():.4f} | acc={acc:.3f}")

# ── 具体样本上的预测 ─────────────────────────────────────────
print("\n  具体样本上的预测 (t4 重置前要记着 b1, 重置后要记着 b2):")
model.eval()
examples = [
    (1.0, 0.0, "先记 1 后记 0"),
    (0.0, 1.0, "先记 0 后记 1"),
]
with torch.no_grad():
    for b1v, b2v, desc in examples:
        x = torch.zeros(1, seq_len, 2)
        x[0, 0, 0], x[0, 0, 1] = b1v, 1.0
        x[0, 4, 1] = -1.0
        x[0, 5, 0], x[0, 5, 1] = b2v, 1.0
        logits, _ = model(x)
        preds = (torch.sigmoid(logits) >= 0.5).int().squeeze().tolist()
        print(f"    {desc}: 记忆={int(b1v)} -> 重置 -> 记忆={int(b2v)}  输出={preds}")

# ── 观察遗忘门 ──────────────────────────────────────────────
print("""
  观察遗忘门: 固定 b1=1, b2=0 (先要记 1, 之后被重置), 用 64 个样本
  平均遗忘门激活值 f_t (行=时间步, 列=8 个隐藏单元):

    f_t ≈ 1 表示该单元"继续保留"当前记忆; f_t ≈ 0 表示该单元"清空"记忆。
""")

with torch.no_grad():
    batch = torch.zeros(64, seq_len, 2)
    batch[:, 0, 0] = 1.0
    batch[:, 0, 1] = 1.0
    batch[:, 4, 1] = -1.0
    _, forgets = model(batch)
    f_mean = forgets.mean(dim=0)  # [seq, hidden]

print("        " + "".join(f"   u{i}  " for i in range(8)))
labels = ["写1", "等", "等", "等", "重置", "写0", "等", "等"]
for t in range(seq_len):
    row = "  ".join(f"{v:.2f}" for v in f_mean[t])
    print(f"  t{t} {labels[t]:<4} {row}")
print("""
  可以看到 (重点看 u3 这一列):
    - t1-t3 (等待):  f≈0.88-0.95 → 把 b1=1 稳稳留在传送带上
    - t4 (重置):     f≈0.08      → 遗忘门关闭, 旧记忆 b1 被清空
    - t5-t7:         f≈0.02-0.04 → 新记忆是 0, 无需保留
  每个隐藏单元是一个"记忆槽", 遗忘门就是每个槽上的水龙头:
  想记就开着 (f≈1), 想忘就关掉 (f≈0)。
""")

# ══════════════════════════════════════════════════════════════
# 5. 与 PyTorch 官方 nn.LSTMCell 对比
# ══════════════════════════════════════════════════════════════
print("📌 5. Verify against official nn.LSTMCell")

official = nn.LSTMCell(input_size=2, hidden_size=8)
mine = ManualLSTMCell(input_size=2, hidden_size=8)

# 把官方权重拷贝给手写单元, 保证完全一致的起点
mine.W_ih.data = official.weight_ih.data.clone()
mine.b_ih.data = official.bias_ih.data.clone()
mine.W_hh.data = official.weight_hh.data.clone()
mine.b_hh.data = official.bias_hh.data.clone()

H = 8
h_o = torch.zeros(1, H)
c_o = torch.zeros(1, H)
h_m = torch.zeros(1, H)
c_m = torch.zeros(1, H)

max_dh, max_dc, max_df = 0.0, 0.0, 0.0
for t in range(seq_len):
    x_t = X[:1, t]

    h_o, c_o = official(x_t, (h_o, c_o))

    # 用官方权重切片手动算遗忘门: PyTorch 参数顺序是 [i, f, g, o]
    W_if, b_if = official.weight_ih[H:2 * H], official.bias_ih[H:2 * H]
    W_hf, b_hf = official.weight_hh[H:2 * H], official.bias_hh[H:2 * H]
    f_o = torch.sigmoid(x_t @ W_if.T + b_if + h_m @ W_hf.T + b_hf)

    h_m, (h_m, c_m), f_m = mine(x_t, (h_m, c_m))

    max_dh = max(max_dh, (h_o - h_m).abs().max().item())
    max_dc = max(max_dc, (c_o - c_m).abs().max().item())
    max_df = max(max_df, (f_o - f_m).abs().max().item())

print(f"  手写单元 vs nn.LSTMCell (8 个时间步的最大误差)")
print(f"    hidden state h : {max_dh:.2e}")
print(f"    cell state   c : {max_dc:.2e}")
print(f"    forget gate  f : {max_df:.2e}")

print("""
✅ Forget gate demo completed.
   Concept: RNN 的隐藏态被反复覆盖, 记不住长程信息;
            LSTM 用遗忘门 f_t 控制"传送带" c_t 上的内容,
            想记就 f≈1, 想忘就 f≈0 —— 这就是长短期记忆的来源。
""")

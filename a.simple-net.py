import torch
import torch.nn as nn


class SimpleNet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size) -> None:
        super(SimpleNet, self).__init__()
        self.layer1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.layer2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = self.layer1(x)  # Input goes into Layer 1
        x = self.relu(x)  # Apply ReLU activation
        output = self.layer2(x)  # Output goes into Layer 2
        return output


INPUT_DIM = 10
HIDDEN_DIM = 20
OUTPUT_DIM = 3

model = SimpleNet(INPUT_DIM, HIDDEN_DIM, OUTPUT_DIM)
dummy_input = torch.randn(1, INPUT_DIM)  # Create a sample input tensor
prediction = model(dummy_input)

print("Model successfully built and executed!")
# print(prediction.shape) # Should show the output dimension (e.g., torch.Size([1, 3]))
#

criterion = nn.MSELoss()  # Mean Squared Error is common for regression tasks
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)  # Adam is a popular choice

# --- Simulation of the Training Loop ---
learning_rate = 0.01
epochs = 10

for epoch in range(epochs):
    # 1. Get Data (In a real scenario, you load batches of images/labels here)
    X_train, y_train = #nil, NIL   load_data()

    # --- (Inside the epoch loop) ---

    # 2. Forward Pass: Get the prediction from the model
    predictions = model(X_train)

    # 3. Calculate Loss: Measure the error
    loss = criterion(predictions, y_train)

    # 4. Zero Gradients: Clear any previous gradient calculations
    optimizer.zero_grad()

    # 5. Backward Pass: Calculate gradients (how much each parameter contributed to the error)
    loss.backward()

    # 6. Optimization Step: Update the weights based on the gradients and learning rate
    optimizer.step()

    print(f"Epoch {epoch}: Loss = {loss.item()}")

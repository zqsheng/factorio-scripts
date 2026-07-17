import torch

print("--- PyTorch Demonstration ---")

# ==============================================
# 1. DEVICE SETUP (Crucial for Apple Silicon)
# ==============================================

# Check if the Apple Silicon GPU (MPS) is available
if torch.backends.mps.is_available():
    device = torch.device("mps")
    print("\n✅ Success: Using Apple Silicon GPU (MPS) for computation.")
elif torch.cuda.is_available():
    device = torch.device("cuda")
    print("\n✅ Success: Using NVIDIA GPU (CUDA) for computation.")
else:
    device = torch.device("cpu")
    print("\n⚠️ Warning: Using CPU only, as GPU acceleration is not available.")


# ==============================================
# 2. TENSOR CREATION (The Basic Data Structure)
# ==============================================

print("\n--- 2. Creating Tensors ---")

# Create a simple Tensor (a numerical array) on the CPU
cpu_tensor = torch.tensor([1.0, 2.5, 3.0, 4.5])
print(f"Original CPU Tensor:\n{cpu_tensor}")
print(f"Tensor Data Type: {cpu_tensor.dtype}")


# ==============================================
# 3. BASIC TENSOR OPERATIONS
# ==============================================

print("\n--- 3. Performing Operations ---")

# Operation 1: Scalar operation
addition = cpu_tensor + 5.0
print(f"Tensor + 5.0: {addition}")

# Operation 2: Matrix multiplication (Dot product)
tensor_a = torch.tensor([[1, 2], [3, 4]])
tensor_b = torch.tensor([[5, 6], [7, 8]])

matrix_mult = torch.matmul(tensor_a, tensor_b)
print(f"\nMatrix A:\n{tensor_a}")
print(f"Matrix B:\n{tensor_b}")
print(f"Matrix Multiplication Result:\n{matrix_mult}")


# ==============================================
# 4. DEVICE TRANSFER (Moving Data)
# ==============================================

print("\n--- 4. Moving Data to the Device ---")

# Move the tensor from CPU memory to the selected device (MPS or CPU)
tensor_on_device = cpu_tensor.to(device)

print(f"Tensor successfully moved to the {device} device.")


# ==============================================
# 5. FINAL EXECUTION (Testing the Speed)
# ==============================================

print("\n--- 5. Final Check ---")

# We can perform an operation on the tensor that is now on the GPU/MPS
result_on_device = tensor_on_device * 2.0

print(f"Result after operation on device:\n{result_on_device}")
print("\nDemonstration Complete!")

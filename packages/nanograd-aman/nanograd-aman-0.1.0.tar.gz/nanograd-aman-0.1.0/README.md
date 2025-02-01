# 🧠 Nanograd - Lightweight Autograd Engine for Deep Learning  

**Nanograd** is a minimalistic automatic differentiation engine for building and training neural networks. Inspired by PyTorch’s autograd, it provides an easy-to-use framework for defining computational graphs, performing backpropagation, and training models.  

## 🚀 Features  
✅ **Automatic Differentiation** - Compute gradients with ease using backpropagation.  
✅ **Graph-Based Computation** - Uses a dynamic computation graph to track operations.  
✅ **Lightweight & Fast** - No unnecessary dependencies, optimized for speed.  
✅ **Custom Neural Networks** - Build and train models from scratch.  
✅ **Graph Visualization** - Visualize computational graphs using `graphviz`.  

---

## 📦 Installation  

You can install **Nanograd** directly from PyPI:  

```bash
pip install nanograd
```


## 🔧 Usage

### 1️⃣ Defining Computation

```python
from nanograd.engine import Value

a = Value(2.0)
b = Value(3.0)
c = a * b + 5
c.backward()

print(f"Value of c: {c.data}")        # Output: 11.0
print(f"Gradient of a: {a.grad}")     # Output: 3.0
print(f"Gradient of b: {b.grad}")     # Output: 2.0

```

### 2️⃣ Building a Neural Network
```python
from nanograd.nn import MLP
import numpy as np

# Create a 2-layer neural network (2 inputs, 4 hidden, 1 output)
model = MLP(2, [4, 1])

# Dummy data
X = np.array([[1.0, 2.0]])
y = np.array([1.0])

# Forward pass
pred = model.forward(X)
print(f"Prediction: {pred}")

```

### 3️⃣ Visualizing Computational Graph

```python
from nanograd.graph import draw_graph
draw_graph(c)  # Generates a graph of computations

```



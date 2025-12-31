import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# -----------------------------
# Dataset
# -----------------------------
data = np.array([12, 15, 18, 20, 22, 22, 25, 30, 30, 30, 35, 40])

# -----------------------------
# Statistical Calculations
# -----------------------------
mean = np.mean(data)
median = np.median(data)
mode = stats.mode(data, keepdims=True)[0][0]
variance = np.var(data)
std_dev = np.std(data)
p25 = np.percentile(data, 25)
p50 = np.percentile(data, 50)
p75 = np.percentile(data, 75)

# -----------------------------
# Display Results
# -----------------------------
print("Statistical Measures:\n")
print(f"Mean               : {mean}")
print(f"Median             : {median}")
print(f"Mode               : {mode}")
print(f"Variance           : {variance}")
print(f"Standard Deviation : {std_dev}")
print(f"25th Percentile    : {p25}")
print(f"50th Percentile    : {p50}")
print(f"75th Percentile    : {p75}")

# -----------------------------
# Visualization
# -----------------------------

# Histogram
plt.figure()
plt.hist(data, bins=6)
plt.title("Histogram")
plt.xlabel("Values")
plt.ylabel("Frequency")
plt.show()

# Box Plot
plt.figure()
sns.boxplot(x=data)
plt.title("Box Plot")
plt.show()

# Density Plot
plt.figure()
sns.kdeplot(data, fill=True)
plt.title("Density Plot")
plt.show()

# Line Plot
plt.figure()
plt.plot(data, marker='o')
plt.title("Line Plot")
plt.xlabel("Index")
plt.ylabel("Value")
plt.show()

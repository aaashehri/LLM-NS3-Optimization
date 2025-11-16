import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file
data = pd.read_csv("log_clean.csv")

# Convert iteration column to integer (if not already)
data["Iteration"] = data["Iteration"].astype(int)

# --- Plot 1: Throughput vs. Iteration ---
plt.figure(figsize=(6,4))
plt.plot(data["Iteration"], data["Throughput(Mbps)"], marker="o", linestyle="-")
plt.xlabel("Iteration")
plt.ylabel("Throughput (Mbps)")
plt.title("Throughput Improvement Across Iterations")
plt.grid(True)
plt.tight_layout()
plt.savefig("throughput_vs_iteration.png", dpi=300)
plt.show()

# --- Plot 2: Latency vs. Iteration ---
plt.figure(figsize=(6,4))
plt.plot(data["Iteration"], data["Latency(ms)"], marker="s", color="orange", linestyle="--")
plt.xlabel("Iteration")
plt.ylabel("Latency (ms)")
plt.title("Latency Stability Across Iterations")
plt.grid(True)
plt.tight_layout()
plt.savefig("latency_vs_iteration.png", dpi=300)
plt.show()

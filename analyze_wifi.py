import pandas as pd
import matplotlib.pyplot as plt

# === Load CSV ===
data = pd.read_csv("results.csv")

# Ensure columns exist
data.columns = [c.strip() for c in data.columns]

# === Separate metrics ===
throughput = data["Throughput(Mbps)"]
latency = data["Latency(ms)"]
loss = data["PacketLoss(%)"]

# === Plot Throughput over Iterations ===
plt.figure(figsize=(8,5))
plt.plot(throughput, marker='o', linewidth=2)
plt.title("Wi-Fi Adaptive Optimization — Throughput Trend")
plt.xlabel("Iteration")
plt.ylabel("Throughput (Mbps)")
plt.grid(True)
plt.tight_layout()
plt.savefig("wifi_throughput_trend.png")
plt.show()

# === Plot Packet Loss over Iterations ===
plt.figure(figsize=(8,5))
plt.plot(loss, color='red', marker='x', linewidth=2)
plt.title("Wi-Fi Adaptive Optimization — Packet Loss Trend")
plt.xlabel("Iteration")
plt.ylabel("Packet Loss (%)")
plt.grid(True)
plt.tight_layout()
plt.savefig("wifi_loss_trend.png")
plt.show()

# === Summary Comparison ===
baseline = data.iloc[0]
final = data.iloc[-1]

print("\n📊 Baseline vs Final Results")
print(f"Baseline Throughput: {baseline['Throughput(Mbps)']:.2f} Mbps")
print(f"Final Throughput:    {final['Throughput(Mbps)']:.2f} Mbps")
print(f"Baseline Loss:       {baseline['PacketLoss(%)']:.2f} %")
print(f"Final Loss:          {final['PacketLoss(%)']:.2f} %")

improvement = ((final['Throughput(Mbps)'] - baseline['Throughput(Mbps)'])
               / baseline['Throughput(Mbps)']) * 100

print(f"\n✅ Improvement in Throughput: {improvement:.1f}%")

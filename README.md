# LLM-NS3-Optimization  
**Closed-Loop Network Optimization Using Large Language Models and NS-3 Simulation**

---

## 🧠 Overview
This project introduces an **AI-assisted adaptive optimization framework** that integrates the **NS-3 network simulator** with a **Large Language Model (LLM)** such as ChatGPT.  
The framework establishes a **closed feedback loop** where NS-3 simulation metrics (throughput, latency, packet loss) are analyzed by the LLM, which then recommends optimized configuration parameters (e.g., data rate, queue limit, packet size).  

This enables **autonomous network tuning** and **self-adaptive performance optimization** without human intervention.

---

## ⚙️ System Architecture
The framework consists of four main components:

1. **Simulation Environment (NS-3)**  
   Runs network experiments (wired or Wi-Fi) using parameters from a configuration file.
2. **Configuration Management Layer**  
   Reads and updates `config.yaml` dynamically based on AI suggestions.
3. **AI Optimization Engine (LLM)**  
   Analyzes simulation metrics and returns parameter recommendations in structured JSON.
4. **Controller (Python)**  
   Orchestrates the loop — executing simulations, collecting results, querying the LLM, and applying updates.

---

## 🔁 Adaptive Workflow
1. Initialize simulation parameters in `config.yaml`.  
2. Run NS-3 and collect metrics (`results.csv`).  
3. Send metrics to the LLM (via OpenAI API).  
4. Parse the response and update configuration parameters.  
5. Repeat until convergence or target performance is achieved.  

---

## 🧩 File Structure

├── scratch/
│ └── run_simulation_wifi.cc # NS-3 Wi-Fi simulation file
├── loop_wifi.py # Python controller for adaptive loop
├── config.yaml # Dynamic configuration file
├── results.csv # Stores simulation metrics
├── log.csv # Records iteration results
├── README.md # Documentation

---

## 📊 Example Output
| Iteration | Throughput (Mbps) | Latency (ms) | Packet Loss (%) | Suggested DataRate |
|------------|-------------------|---------------|------------------|--------------------|
| 1 | 22.1 | 2 | 91.0 | 500 Mbps |
| 2 | 25.6 | 2 | 80.5 | 1000 Mbps |
| 3 | 29.5 | 2 | 72.4 | 1500 Mbps |

---

## 🚀 Getting Started
### Prerequisites
- macOS / Linux  
- Python 3.12  
- NS-3 (v3.37 or later)  
- OpenAI API Key  

### Installation
```bash
# Clone the repository
git clone https://github.com/aaashehri/LLM-NS3-Optimization.git
cd LLM-NS3-Optimization

# Install dependencies
pip install openai pyyaml pandas

# Run a single simulation
./ns3 run "scratch/run_simulation_wifi"

# Start the adaptive loop
python3 loop_wifi.py

🧮 Key Features

Closed-loop adaptive optimization

Real-time feedback from LLM

Automatic YAML configuration updates

Support for both wired and Wi-Fi topologies

Reproducible experiment logs
📈 Experimental Results

Wired Network: Throughput improved from 45 Mbps → 90 Mbps (≈100% gain)

Wi-Fi Network: Throughput ≈ 30 Mbps with ≈91% packet loss reduction attempts

Demonstrates semantic reasoning of LLMs for network parameter optimization.
Future Work

Integration with Reinforcement Learning for hybrid optimization.

Multi-node and mobility-aware 6G scenarios.

On-device inference for real-time adaptive control.
Citation

If you use this repository in your research, please cite:

A. Alshehri, "Closed-Loop Network Optimization Using LLMs and NS-3 Simulation", 2025.
License

MIT License © 2025 Aziz Alshehri

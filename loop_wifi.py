import os, yaml, csv, time, json, re
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key="OPENAI_API_KEY")



# ---------- Helper Functions ----------

def read_results():
    """Read latest Wi-Fi simulation results from results.csv"""
    if not os.path.exists("results.csv"):
        print("⚠️ results.csv not found")
        return None
    
    try:
        with open("results.csv", "r") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            if not rows:
                print("⚠️ results.csv is empty")
                return None
            
            # Get the last row (latest results)
            latest = rows[-1]
            return {
                "Throughput": float(latest.get("Throughput", 0)),
                "Latency": float(latest.get("Latency", 0)),
                "PacketLoss": float(latest.get("PacketLoss", 0))
            }
    except Exception as e:
        print(f"⚠️ Error reading results.csv: {e}")
        return None


def read_config():
    """Read current configuration"""
    if not os.path.exists("config.yaml"):
        default = {"DataRate": "54Mbps", "QueueLimit": 100, "PacketSize": 1024}
        with open("config.yaml", "w") as f:
            yaml.safe_dump(default, f)
        return default
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)


def update_config(new_config):
    """Update config.yaml"""
    try:
        with open("config.yaml", "w") as f:
            yaml.safe_dump(new_config, f)
        print("✅ Updated config.yaml:", new_config)
    except Exception as e:
        print("⚠️ Could not update config:", e)


def parse_llm_response(content):
    """Parse LLM response, handling code blocks"""
    # Clean any code block wrappers like ```json
    cleaned = re.sub(r"```[a-zA-Z]*", "", content).replace("```", "").strip()
    try:
        return json.loads(cleaned)
    except Exception as e:
        print("⚠️ LLM response not valid JSON. Skipping update.")
        print("Error:", e)
        return None


def ask_llm(metrics, config):
    """Ask LLM to suggest new parameters"""
    prompt = f"""
You are optimizing a Wi-Fi network in NS-3.
Current metrics:
- Throughput: {metrics['Throughput']} Mbps
- Latency: {metrics['Latency']} ms
- Packet Loss: {metrics['PacketLoss']} %

Current configuration:
{json.dumps(config, indent=2)}

Suggest new parameter values (DataRate, QueueLimit, PacketSize) to improve throughput while keeping latency < 5 ms and packet loss < 5%.
Return your response strictly as JSON with these exact keys: DataRate, QueueLimit, PacketSize.
Example: {{"DataRate": "108Mbps", "QueueLimit": 150, "PacketSize": 1500}}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4
        )
        content = response.choices[0].message.content
        print("🤖 LLM Suggestion:", content)
        
        return parse_llm_response(content)
    except Exception as e:
        print(f"⚠️ Error calling LLM API: {e}")
        return None


def run_ns3():
    """Run NS-3 Wi-Fi simulation"""
    print("▶️ Running NS-3 simulation...")
    result = os.system("./ns3 run 'scratch/run_simulation_wifi' > /dev/null 2>&1")
    if result != 0:
        print(f"⚠️ NS-3 simulation returned non-zero exit code: {result}")
    return result == 0


# ---------- Main Optimization Loop ----------

def main():
    print("🚀 Starting Wi-Fi Adaptive Optimization\n")
    
    for iteration in range(3):
        print(f"\n{'='*50}")
        print(f"🌀 Iteration {iteration+1}/3")
        print('='*50)

        # Run simulation
        if not run_ns3():
            print("⚠️ Simulation failed, skipping iteration")
            continue
        
        time.sleep(2)

        # Read results
        metrics = read_results()
        if not metrics:
            print("⚠️ No metrics available, skipping iteration")
            continue

        print("📊 Metrics:", metrics)

        # Get current config and ask LLM for suggestions
        config = read_config()
        new_params = ask_llm(metrics, config)

        if new_params:
            update_config(new_params)
        else:
            print("⚠️ No valid parameters from LLM")

    print("\n" + "="*50)
    print("✅ Wi-Fi adaptive optimization completed.")
    print("="*50)


if __name__ == "__main__":
    main()

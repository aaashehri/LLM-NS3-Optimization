import os
import yaml
import csv
from openai import OpenAI

# Initialize the OpenAI client
client = OpenAI(api_key="Key")

def run_ns3(config):
    """Run NS-3 simulation using parameters from config.yaml"""
    cmd = f'./ns3 run "scratch/run_simulation --dataRate={config["DataRate"]} --queueSize={config["QueueLimit"]} --packetSize={config["PacketSize"]}"'
    os.system(cmd)

def read_results():
    """Read simulation results from results.csv"""
    with open("results.csv") as f:
        reader = csv.DictReader(f)
        return list(reader)[0]

def ask_llm(metrics, config):
    """Send performance metrics to LLM for optimization suggestions"""
    prompt = f"""
    You are optimizing a network simulation.
    Current metrics:
    - Throughput: {metrics['Throughput(Mbps)']} Mbps
    - Latency: {metrics['Latency(ms)']} ms
    Current configuration:
    {config}

    Suggest new numeric values for DataRate (Mbps), QueueLimit, and PacketSize
    to improve throughput and reduce latency.
    Respond in JSON only, like this:
    {{ "DataRate": "XXMbps", "QueueLimit": Y, "PacketSize": Z }}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def update_config(new_config):
    """Update the config.yaml file with new values"""
    try:
        data = yaml.safe_load(new_config)
    except Exception:
        print("⚠️ LLM response not valid YAML/JSON. Skipping update.")
        return

    with open("config.yaml", "w") as f:
        yaml.dump(data, f)
    print("✅ Updated config.yaml:", data)
    return data

if __name__ == "__main__":
    # Ensure log file header exists
    if not os.path.exists("log.csv"):
        with open("log.csv", "w") as f:
            f.write("Iteration,Throughput(Mbps),Latency(ms),DataRate\n")

    for iteration in range(3):
        print(f"\n🌀 Iteration {iteration + 1}")
        with open("config.yaml") as f:
            config = yaml.safe_load(f)

        run_ns3(config)
        metrics = read_results()
        print("📊 Results:", metrics)

        llm_response = ask_llm(metrics, config)
        print("🤖 LLM Suggestion:", llm_response)

        new_config = update_config(llm_response)

        # Log current iteration results
        with open("log.csv", "a") as f:
            f.write(f"{iteration+1},{metrics['Throughput(Mbps)']},{metrics['Latency(ms)']},{config['DataRate']}\n")

    
    print(f"✅ Logged iteration {iteration+1} results to log.csv")



import os
import yaml
import csv
import openai

# ضع مفتاح OpenAI هنا
openai.api_key = "Key"

def run_ns3(config):
    """تشغيل محاكاة NS-3 باستخدام القيم من config.yaml"""
    cmd = f'./ns3 run "scratch/run_simulation --dataRate={config["DataRate"]} --queueSize={config["QueueLimit"]} --packetSize={config["PacketSize"]}"'
    os.system(cmd)

def read_results():
    """قراءة نتائج المحاكاة من ملف results.csv"""
    with open("results.csv") as f:
        reader = csv.DictReader(f)
        return list(reader)[0]

def ask_llm(metrics, config):
    """إرسال النتائج إلى LLM ليقترح إعدادات جديدة"""
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
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def update_config(new_config):
    """تحديث ملف config.yaml بالقيم الجديدة"""
    try:
        data = yaml.safe_load(new_config)
    except Exception:
        print("⚠️ LLM response not valid YAML/JSON. Skipping update.")
        return
    with open("config.yaml", "w") as f:
        yaml.dump(data, f)
    print("✅ Updated config.yaml:", data)

if __name__ == "__main__":
    for iteration in range(3):
        print(f"\n🌀 Iteration {iteration + 1}")
        with open("config.yaml") as f:
            config = yaml.safe_load(f)
        run_ns3(config)
        metrics = read_results()
        print("📊 Results:", metrics)
        llm_response = ask_llm(metrics, config)
        print("🤖 LLM Suggestion:", llm_response)
        update_config(llm_response)


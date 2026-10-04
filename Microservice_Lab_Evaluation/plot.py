import pandas as pd, matplotlib.pyplot as plt

df = pd.read_csv("results.csv")
cpu_cols = [c for c in df if c.endswith("_cpu%")]
mem_cols = [c for c in df if c.endswith("_mem_MiB")]
x = df["concurrency"]

def plot(cols, title, ylabel, fname):
    plt.figure()
    for c in cols:
        label = c.split("-")[1].capitalize() + " Service" if "-" in c else c
        plt.plot(x, df[c], marker="o", label=label)
    plt.xlabel("Concurrent Requests")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xticks(x)
    plt.grid(True)
    if len(cols) > 1:
        plt.legend()
    plt.savefig(fname, dpi=150)

plot(["avg_rt_ms"], "Concurrency vs Avg Response Time", "ms", "g1_response_time.png")
plot(["throughput_rps"], "Concurrency vs Throughput", "req/s", "g2_throughput.png")
plot(cpu_cols, "Concurrency vs CPU", "CPU %", "g3_cpu.png")
plot(mem_cols, "Concurrency vs Memory", "MiB", "g4_memory.png")
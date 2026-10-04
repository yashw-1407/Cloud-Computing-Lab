import subprocess, threading, time, csv, os, re, sys

HOST = "http://localhost:5002"     # Service 1 URL
LEVELS = [1, 2, 4, 8, 16]
DURATION = "30s"
os.makedirs("results", exist_ok=True)

def to_mib(s):
    v, u = re.match(r"([\d.]+)\s*([A-Za-z]+)", s.strip()).groups()
    v = float(v)
    return v * {"KiB": 1/1024, "MiB": 1, "GiB": 1024, "B": 1/1048576}.get(u, 1)

def sampler(stop, data):
    while not stop.is_set():
        out = subprocess.run(
            ["docker", "stats", "--no-stream", "--format",
             "{{.Name}},{{.CPUPerc}},{{.MemUsage}}"],
            capture_output=True, text=True).stdout
        for line in out.strip().splitlines():
            name, cpu, mem = line.split(",")
            d = data.setdefault(name, {"cpu": [], "mem": []})
            d["cpu"].append(float(cpu.strip("%")))
            d["mem"].append(to_mib(mem.split("/")[0]))

rows = []
for n in LEVELS:
    print(f"\n=== Running {n} users ===")
    stats, stop = {}, threading.Event()
    t = threading.Thread(target=sampler, args=(stop, stats)); t.start()

    subprocess.run([sys.executable, "-m", "locust", "-f", "locustfile.py", "--headless",
                    "-u", str(n), "-r", str(n), "-t", DURATION,
                    "--host", HOST, "--csv", f"results/w{n}", "--only-summary"])
    stop.set(); t.join()

    with open(f"results/w{n}_stats.csv") as f:
        agg = [r for r in csv.DictReader(f) if r["Name"] == "Aggregated"][0]

    row = {
        "concurrency": n,
        "requests": int(agg["Request Count"]),
        "failed": int(agg["Failure Count"]),
        "avg_rt_ms": round(float(agg["Average Response Time"]), 2),
        "p95_ms": agg["95%"],
        "throughput_rps": round(float(agg["Requests/s"]), 2),
    }
    for name, d in stats.items():
        row[f"{name}_cpu%"] = round(sum(d["cpu"]) / len(d["cpu"]), 2)
        row[f"{name}_mem_MiB"] = round(sum(d["mem"]) / len(d["mem"]), 2)
    rows.append(row)
    time.sleep(10)   # cool-down between levels

keys = sorted({k for r in rows for k in r}, key=lambda k: list(rows[0]).index(k) if k in rows[0] else 99)
with open("results.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=keys); w.writeheader(); w.writerows(rows)
print("\nSaved results.csv")
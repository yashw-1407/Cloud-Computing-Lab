# Performance Analysis of Virtual Machines and Containers

## Abstract

This study provides an empirical evaluation of the performance differences between Virtual Machines (VMs) and Docker containers. By employing a series of controlled experiments on a MacBook M3 host running an Ubuntu 24.04 environment via UTM, we assess key system metrics. The comparison encompasses CPU, memory, disk I/O, network capabilities, application throughput, startup duration, and scalability. All testing was strictly controlled, limiting Docker to the exact same resource constraints as the VM (2 vCPUs and 3 GB RAM). The outputs have been collected, processed into CSVs, and visualized to ensure full reproducibility.

## Objectives

The primary goals of this project include:
- Conducting a direct, controlled comparison of VM and container performance.
- Measuring CPU computational capacity with Sysbench.
- Evaluating memory read/write speeds using Sysbench.
- Assessing both sequential and random disk I/O performance via fio.
- Testing network bandwidth using iperf3.
- Benchmarking a sample FastAPI application under load.
- Measuring and comparing environment startup times.
- Evaluating system scalability under increasing concurrent workloads.
- Providing raw data, structured CSVs, and graphical comparisons.

## Research Questions

This evaluation seeks to answer:
1. What is the overhead difference in memory operations between a full VM and a Docker container?
2. How do storage access patterns (sequential vs. random) impact the relative performance of VMs and containers?
3. How do application-level workloads perform differently when deployed in these two environments?
4. How do the environments scale as the number of parallel requests increases?
5. What is the impact of virtualization on environment startup times?

## Experimental Environment

Both environments were hosted on the same physical hardware to maintain consistency. The VM was directly benchmarked, while the container was executed within the VM to allow for strict resource limitation and direct comparison against the VM's baseline.

## Hardware Configuration

- **Host Device:** MacBook M3
- **Hypervisor:** UTM
- **CPU Limits:** 2 Virtual CPUs
- **Memory Limits:** 3 GB RAM
- **Storage Allocation:** 54 GB Virtual Disk

## Software Configuration

- **Guest OS:** Ubuntu 24.04 LTS
- **Container Runtime:** Docker
- **Benchmarking Tools:** Sysbench (1.0.20), fio, iperf3, Apache Benchmark (`ab`)
- **Application Stack:** Python 3.12, FastAPI, Uvicorn

## Architecture

The structural setup for the benchmarking process:

```text
                        [ MacBook M3 ]
                              |
                        [    UTM     ]
                              |
                   [ Ubuntu 24.04 Guest VM ]
                  ( 2 vCPU / 3 GB RAM Limit )
                              |
             +----------------+----------------+
             |                                 |
 [ Native VM Execution ]             [ Docker Container ]
             |                                 |
             +----------------+----------------+
                              |
                    [ Unified Workloads ]
                              |
       +--------------+---------------+--------------+
       |              |               |              |
    [ CPU ]       [ Memory ]     [ Disk I/O ]    [ FastAPI ]
  (Sysbench)      (Sysbench)        (fio)       (Apache ab)
                              |
                      [ Raw Outputs ]
                              |
                   [ Processed CSV Data ]
                              |
                 [ Performance Visualizations ]
```

## Methodology

The testing methodology involved running identical workload configurations across both the VM and the Docker container. 
To ensure a fair comparison, Docker was launched with CPU and memory limits exactly matching the VM's allocation. Tests were repeated multiple times to account for variance, with raw data stored in `results/raw/`. Processing scripts (`scripts/analyze_results.py`) were used to parse this data into `results/processed/`, which were subsequently used to generate visual plots (`scripts/generate_plots.py`) saved in `results/figures/`.

## CPU Experiment

Sysbench was utilized to calculate prime numbers up to 20,000 using 4 threads over a 30-second duration. This established a baseline computational score for the host environment.

## Memory Experiment

Sysbench executed memory operations involving a 1 MiB block size up to a total transfer of 10 GB. Throughput (events per second) and latency were recorded across 10 distinct runs to calculate the average performance.

## Disk I/O Experiment

The `fio` utility tested storage performance across four scenarios:
- Sequential Read (1 MiB blocks)
- Sequential Write (1 MiB blocks)
- Random Read (4 KiB blocks)
- Random Write (4 KiB blocks)

Metrics collected included bandwidth (MiB/s), IOPS, and average latency.

## Network Experiment

Network throughput and retransmissions were evaluated using `iperf3`. The test involved a client-server architecture measuring bandwidth under multiple parallel streams for 30 seconds.

## Application Experiment

A FastAPI server running via Uvicorn was benchmarked using Apache Benchmark (`ab`). The server exposed endpoints for health checks (`/health`), computational load (`/compute`), and memory allocation (`/memory`). Requests per second and response times were aggregated.

## Startup-Time Experiment

The time required to boot the VM and reach an application-ready state was compared against the time required to spin up the Docker container. Repeated trials were conducted to find the average startup delay.

## Scalability Experiment

Scalability was tested by running the CPU and API benchmarks under progressively heavier loads (e.g., scaling threads from 1 to 8, and increasing concurrent HTTP connections). This highlighted how each environment handles resource contention.

## Results

A high-level summary of the collected data:
- **CPU Baseline:** ~4888 events/sec
- **Memory Throughput:** VM (~47,070 ev/s) vs Docker (~46,703 ev/s)
- **Sequential Disk Read:** VM (2831 MiB/s) vs Docker (4122 MiB/s)
- **Random Disk Read:** VM (1777 MiB/s) vs Docker (34.4 MiB/s)
- **FastAPI Health Check:** VM (2853 req/s) vs Docker (2230 req/s)

## Statistical Analysis

Data was aggregated using Pandas to compute the mean, median, standard deviation, minimum, and maximum values across all trial runs. This mitigated the impact of temporary system spikes.

## VM vs Container Comparison

| Metric | VM Performance | Container Performance | Difference (Estimated) |
|---|---|---|---|
| Memory Throughput | 47,070 ev/s | 46,703 ev/s | Container slightly slower (~0.7%) |
| Sequential Read | 2831 MiB/s | 4122 MiB/s | Container faster |
| Random Read | 1777 MiB/s | 34.4 MiB/s | Container significantly slower |
| Sequential Write | 3061 MiB/s | 3324 MiB/s | Container slightly faster |
| Random Write | 3740 MiB/s | 32.0 MiB/s | Container significantly slower |
| FastAPI `/health` | 2853 req/s | 2230 req/s | VM handled more requests |

*(Note: These values are derived from specific experimental configurations and may vary based on storage drivers and volume mounts).*

## Discussion

The experiments indicate that neither environment is universally superior. While memory and CPU execution showed negligible overhead in containers, disk I/O—especially random reads and writes with small block sizes—was drastically impacted in the Docker environment. This is likely due to the overhead of the storage overlay or volume mounting configuration. Conversely, the VM handled random I/O much more gracefully but lagged behind the container in sequential throughput. Application performance favored the VM slightly, potentially due to fewer abstraction layers in the network stack during local testing.

## Limitations

- Testing was restricted to a single hardware host (MacBook M3).
- Fixed CPU and memory limits were used; dynamically scaling environments were not tested.
- Disk I/O is heavily dependent on the hypervisor's virtual storage driver and Docker's storage backend.
- Background OS tasks may have introduced slight variance.

## Conclusion

Docker containers offer near-native CPU and memory performance with minimal overhead compared to traditional Virtual Machines. However, for workloads requiring heavy random disk I/O, the storage abstraction of containers can introduce significant bottlenecks. VMs provide more consistent random I/O but may suffer from slower startup times and slightly lower sequential speeds. The choice between VM and Container should be strictly dictated by the application's specific resource requirements.

## Future Work

- Expansion to Kubernetes to test orchestration overhead.
- Testing across different hardware architectures (e.g., x86_64 vs ARM64).
- Varying the storage drivers (e.g., overlay2 vs. direct volume mounts) to optimize disk I/O.
- Long-duration stability tests under continuous load.

## Reproduction Instructions

To reproduce this experiment:

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd vm-vs-container-performance
   ```

2. **Prepare the environments:**
   Follow instructions in `docs/methodology.md` to setup the Ubuntu VM and Docker limits.

3. **Run Benchmarks:**
   Execute the automated bash scripts:
   ```bash
   ./scripts/run_cpu.sh
   ./scripts/run_memory.sh
   ./scripts/run_disk.sh
   ```

4. **Process Data and Plot:**
   Ensure Python requirements are installed:
   ```bash
   pip install -r api/requirements.txt pandas matplotlib
   python3 scripts/analyze_results.py
   python3 scripts/generate_plots.py
   ```

# Performance Analysis

## Test Configuration

The virtual machines were configured identically to ensure a fair comparison:

| Parameter | Configuration |
|---|---|
| Guest OS | Ubuntu |
| vCPU | 2 |
| RAM | 2 GB |
| Disk | 20 GB |

## Benchmark Command

The following Sysbench command was used for the CPU performance test:

```bash
sysbench cpu --cpu-max-prime=20000 run
```

## Results

| Metric | Proxmox VE | VMware Workstation |
|---|---|---|
| Total Execution Time | 10.0030 s | 10.0002 s |
| Total Events | 14,548 | 10,381 |
| Events per Second | 1,453.98 | 1,037.93 |
| Average Latency | 0.69 ms | 0.96 ms |

## Analysis

The recorded benchmark results show measurable differences between the two hypervisor environments:

1. **Execution Time:** Both environments ran the benchmark for approximately 10 seconds, which is the default behavior for Sysbench.
2. **Throughput:** Proxmox VE (Type-1) completed significantly more total events (14,548) compared to VMware Workstation (Type-2), which completed 10,381 events in the same time frame. Consequently, Proxmox VE demonstrated a higher throughput at 1,453.98 events per second, while VMware Workstation recorded 1,037.93 events per second.
3. **Latency:** Proxmox VE recorded a lower average latency of 0.69 ms, indicating faster processing per event, whereas VMware Workstation recorded a higher average latency of 0.96 ms.

## Observation

The measurements show that the Ubuntu virtual machine running on the Type-1 hypervisor (Proxmox VE) achieved higher CPU throughput and lower average latency compared to the identically configured virtual machine running on the Type-2 hypervisor (VMware Workstation) under the specific conditions of this experiment.

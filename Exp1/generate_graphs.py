import matplotlib.pyplot as plt
import numpy as np
import os

# Data
hypervisors = ['Proxmox VE (Type-1)', 'VMware Workstation (Type-2)']
total_events = [14548, 10381]
events_per_second = [1453.98, 1037.93]
avg_latency = [0.69, 0.96]
exec_time = [10.0030, 10.0002]

# Create graphs directory
os.makedirs('graphs', exist_ok=True)

# Common styling
plt.style.use('ggplot')
colors = ['#1f77b4', '#ff7f0e']

# 01_hypervisor_architecture.png
fig, ax = plt.subplots(figsize=(8, 6))
ax.axis('off')
ax.text(0.5, 0.8, 'Type-1 Hypervisor (Proxmox VE)', ha='center', va='center', fontsize=14, weight='bold', bbox=dict(facecolor='#1f77b4', alpha=0.5))
ax.text(0.5, 0.6, 'Hardware -> Hypervisor -> Guest OS', ha='center', va='center', fontsize=12)
ax.text(0.5, 0.4, 'Type-2 Hypervisor (VMware Workstation)', ha='center', va='center', fontsize=14, weight='bold', bbox=dict(facecolor='#ff7f0e', alpha=0.5))
ax.text(0.5, 0.2, 'Hardware -> Host OS -> Hypervisor -> Guest OS', ha='center', va='center', fontsize=12)
plt.title('Hypervisor Architecture Comparison')
plt.savefig('graphs/01_hypervisor_architecture.png')
plt.close()

# 02_events_per_second.png
fig, ax = plt.subplots(figsize=(8, 6))
bars = ax.bar(hypervisors, events_per_second, color=colors)
ax.set_ylabel('Events per Second')
ax.set_title('Events per Second Comparison')
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval + 10, round(yval, 2), ha='center', va='bottom')
plt.savefig('graphs/02_events_per_second.png')
plt.close()

# 03_total_events_and_time_per_event.png
fig, ax1 = plt.subplots(figsize=(8, 6))
ax2 = ax1.twinx()
x = np.arange(len(hypervisors))
width = 0.35
bars1 = ax1.bar(x - width/2, total_events, width, label='Total Events', color='#1f77b4')
bars2 = ax2.bar(x + width/2, avg_latency, width, label='Average Latency (ms)', color='#ff7f0e')
ax1.set_ylabel('Total Events', color='#1f77b4')
ax2.set_ylabel('Average Latency (ms)', color='#ff7f0e')
ax1.set_xticks(x)
ax1.set_xticklabels(hypervisors)
ax1.set_title('Total Events and Latency per Event')
fig.legend(loc='upper right', bbox_to_anchor=(0.9, 0.9))
plt.savefig('graphs/03_total_events_and_time_per_event.png')
plt.close()

# 04_latency_comparison.png
fig, ax = plt.subplots(figsize=(8, 6))
bars = ax.bar(hypervisors, avg_latency, color=['#2ca02c', '#d62728'])
ax.set_ylabel('Average Latency (ms)')
ax.set_title('Average Latency Comparison')
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval + 0.02, round(yval, 2), ha='center', va='bottom')
plt.savefig('graphs/04_latency_comparison.png')
plt.close()

# 05_latency_consistency.png
# Since we only have average latency, we will plot it as a line to represent consistency
fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(hypervisors, avg_latency, marker='o', linestyle='-', color='#9467bd', markersize=10, linewidth=2)
ax.set_ylabel('Latency (ms)')
ax.set_title('Latency Consistency Trend')
plt.grid(True)
plt.savefig('graphs/05_latency_consistency.png')
plt.close()

# 06_relative_performance.png
fig, ax = plt.subplots(figsize=(8, 6))
performance = [100, (events_per_second[1]/events_per_second[0])*100]
bars = ax.bar(hypervisors, performance, color=['#8c564b', '#e377c2'])
ax.set_ylabel('Relative Performance (%)')
ax.set_title('Relative Performance (Proxmox as Baseline)')
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval + 2, f"{round(yval, 1)}%", ha='center', va='bottom')
plt.savefig('graphs/06_relative_performance.png')
plt.close()

# 07_type2_vm_resources.png
resources = ['vCPU', 'RAM (GB)', 'Disk (GB)']
values = [2, 2, 20]
fig, ax = plt.subplots(figsize=(8, 6))
ax.pie(values, labels=resources, autopct='%1.1f%%', startangle=90, colors=['#bcbd22', '#17becf', '#7f7f7f'])
ax.axis('equal')
plt.title('Type-2 VM Resources Allocation')
plt.savefig('graphs/07_type2_vm_resources.png')
plt.close()

# 08_summary_dashboard.png
fig, axs = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Performance Summary Dashboard', fontsize=16)

# Total Events
axs[0, 0].bar(hypervisors, total_events, color=colors)
axs[0, 0].set_title('Total Events')

# Events per second
axs[0, 1].bar(hypervisors, events_per_second, color=colors)
axs[0, 1].set_title('Events per Second')

# Avg Latency
axs[1, 0].bar(hypervisors, avg_latency, color=['#2ca02c', '#d62728'])
axs[1, 0].set_title('Average Latency (ms)')

# Relative Perf
axs[1, 1].bar(hypervisors, performance, color=['#8c564b', '#e377c2'])
axs[1, 1].set_title('Relative Performance (%)')

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig('graphs/08_summary_dashboard.png')
plt.close()

print("All graphs generated successfully!")

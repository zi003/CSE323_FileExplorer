import time
import psutil

##function to monitor app usage
def monitor_app_usage(duration=30):
    start_time = time.time()
    usage_stats = {}

    psutil.cpu_percent(interval=None)  # prime CPU stats

    while time.time() - start_time < duration:
        for proc in psutil.process_iter(['pid', 'name', 'memory_percent']):
            try:
                name = proc.info['name']
                cpu = proc.cpu_percent(interval=None)
                mem = proc.info['memory_percent']

                if name:
                    if name not in usage_stats:
                        usage_stats[name] = {'cpu': 0, 'mem': 0, 'samples': 0}

                    usage_stats[name]['cpu'] += cpu
                    usage_stats[name]['mem'] += mem
                    usage_stats[name]['samples'] += 1

            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        time.sleep(1)

    return usage_stats

##currently hard coded apps
SOCIAL_APPS = ["chrome.exe", "msedge.exe", "firefox.exe", "discord.exe"]

def analyze_usage(usage_stats, cpu_threshold=20):
    for app, stats in usage_stats.items():
        avg_cpu = stats['cpu'] / stats['samples']

        if app.lower() in SOCIAL_APPS and avg_cpu > cpu_threshold:
            print(f"⚠ ALERT: High usage detected for {app} (Avg CPU: {avg_cpu:.2f}%)")
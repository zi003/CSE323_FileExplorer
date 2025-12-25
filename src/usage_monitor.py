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

def analyze_usage(usage_stats, cpu_threshold=20, time_threshold_minutes = 30):
    alerts = []

    for app, stats in usage_stats.items():
        if stats['samples'] == 0:
            continue

        avg_cpu = stats['cpu'] / stats['samples']
        ##assuming 1 sample per second
        minutes_active = stats['samples'] / 60

        if app.lower() in SOCIAL_APPS and avg_cpu > cpu_threshold:
            alerts.append(
                f"⚠ ALERT: {app} avg CPU {avg_cpu:.2f}%"
            )
        if app.lower() in SOCIAL_APPS and minutes_active > time_threshold_minutes:
            alerts.append(f"⚠ TIME LIMIT: {app} used for {minutes_active:.1f} minutes")
    if not alerts:
        return "No Usage or Time Limit Alerts!"

    return "\n".join(alerts)

##using a single function to combine both the above functions
def monitor_and_analyze(duration=10, cpu_threshold=20, time_threshold_minutes = 30):
    usage_stats = monitor_app_usage(duration)
    return analyze_usage(usage_stats, cpu_threshold, time_threshold_minutes)
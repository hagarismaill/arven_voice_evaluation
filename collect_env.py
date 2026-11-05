import platform, subprocess, sys, psutil
def run(cmd):
    try: return subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=60).stdout.strip()
    except Exception as e: return "ERROR: " + str(e)
def ps(q): return run(["powershell", "-NoProfile", "-Command", q])
lines = ["OS: " + platform.platform(), "CPU: " + ps("(Get-CimInstance Win32_Processor).Name"), "CPU cores/threads: %s / %s" % (psutil.cpu_count(logical=False), psutil.cpu_count(logical=True)), "RAM total GB: " + str(round(psutil.virtual_memory().total / 1024**3, 1)), "GPU: " + ps("(Get-CimInstance Win32_VideoController).Name"), "Python: " + sys.version.split()[0], "Ollama: " + run(["ollama", "--version"]), "--- ollama list ---", run(["ollama", "list"])]
text = "\n".join(lines) + "\n"
open("env.txt", "w", encoding="utf-8").write(text)
print(text)
# Flight Executive in Python
# ==========================
# 1. Multiprocessing with inter-process communication.
# 2. FE is main process (daemon) with minimal functionality and maximum robustness.
# 3. FE starts on power on.
# 4. CLI commands: start, stop, power-saving, preflight-check, etc.
# 5. Controlling (starting, stoping) and monitoring other processes (aka flight services).
# 6. Gracefull shutdown by poison pill: first communicate with processes to stop their loops, then join them, then shutdown.
# 7. Main services: telemetry, communications, multimedia.
# 8. Monitor co-process for FE.
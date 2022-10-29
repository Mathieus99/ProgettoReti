import psutil
from psutil._common import bytes2human
import platform
import os
def cmd_list():
    print ("\nLista comandi\n")
    print ("os\tVisualizza informazioni sul sistema operativo\n")
    print ("ls\tVisualizza il contenuto della directory corrente\n")
    print ("cd\tConsente di spostarsi in un altra drectory specificata dal path\n")
    print ("pwd\tConsente di visualizzare il path della directory corrente\n")
    print ("cpu\tVisualizza informazioni sulla CPU\n")
    print("memory\tVisualizza informazioni sulla memoria\n")
    print("disk\tVisualizza informazioni sulla memoria di massa(punto di mount, FS, ecc...)\n")
    print("read \"nome file\"\tVisualizza il contenuto di un file\n")

#Preleva e formatta le informazioni sulla CPU
def CPUInfo():
    cpu = platform.processor()
    freq = psutil.cpu_freq()
    times = psutil.cpu_times()
    messaggio = "CPU: " + cpu + "\nCPU frequency: " + str(freq[0]) + " MHz (current) , " + str(freq[2]) + " MHz (max)\n"
    messaggio = messaggio + "Logical Cores: " + str(psutil.cpu_count(logical=True)) + "\nPhysical Cores: " + str(psutil.cpu_count(logical=False)) + "\n"
    messaggio = messaggio + "CPU percent: " + str(psutil.cpu_percent()) + "%\n"
    messaggio = messaggio + "Times\nUser Mode: " + str(times[0]) + "\nKernel Mode: " + str(times[1]) + "\nIdle: " + str(times[2]) + "\nServicing HW Interrupts: " + str(times[3]) + "\nServicing procedure calls: " + str(times[4]) + "\n"
    stats = psutil.cpu_stats()
    messaggio = messaggio + "Stats\nContext switches (voluntary + involuntary)(since boot): " + str(stats[0]) + "\nInterrupts (since boot): " + str(stats[1]) + "\nSoftware interrupts (since boot): " + str(stats[2]) + "\nSystem calls (since boot): " + str(stats[3]) + "\n"
    return messaggio

#Preleva e formatta le informazioni sulla memoria
def MemoryInfo():
    messaggio = "MEMORY\n------\n"
    for name in psutil.virtual_memory()._fields:
        value = getattr(psutil.virtual_memory(), name)
        if name != 'percent':
            value = bytes2human(value)
        if name == "percent":
            messaggio = messaggio + "%-10s : %7s" % (name.capitalize(),value) + "%\n"
        else:
            messaggio = messaggio + "%-10s : %7s\n" % (name.capitalize(),value)
    messaggio = messaggio + "\nSWAP\n----\n"
    for name in psutil.swap_memory()._fields:
        value = getattr(psutil.swap_memory(), name)
        if name != 'percent':
            value = bytes2human(value)
        if name == "percent":
            messaggio = messaggio + "%-10s : %7s" % (name.capitalize(),value) + "%\n"
        else:
            messaggio = messaggio + "%-10s : %7s\n" % (name.capitalize(),value)
    return messaggio

#Preleva e formatta le informazioni sui dischi e le memorie montate
def DiskInfo():
    templ = "%-17s %8s %8s %8s %5s%% %9s  %s"
    messaggio = templ % ("Device", "Total", "Used", "Free", "Use ", "Type", "Mount") + "\n"
    for part in psutil.disk_partitions(all=False):
        if os.name == "nt":
            if "cdrom" in part.opts or part.fstype == "":
                # skip cd-rom drives with no disk in it; they may raise
                # ENOENT, pop-up a Windows GUI error for a non-ready
                # partition or just hang.
                continue
        usage = psutil.disk_usage(part.mountpoint)
        messaggio = messaggio + templ % (
            part.device,
            bytes2human(usage.total),
            bytes2human(usage.used),
            bytes2human(usage.free),
            int(usage.percent),
            part.fstype,
            part.mountpoint) + "\n"
    return messaggio
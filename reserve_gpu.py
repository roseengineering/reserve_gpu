
import os
import csv
import subprocess

from IPython.core.magic import Magics, magics_class, line_magic


gpu_devices = None

def available_device():
    global gpu_devices

    if gpu_devices is None: 
        r = subprocess.run([
                "nvidia-smi", 
                "--format=csv,noheader,nounits",
                "--query-gpu=index,pci.bus_id,name,memory.total"
            ], stdout=subprocess.PIPE)
        lines = r.stdout.decode('utf-8').strip().split('\n')
        gpu_devices = list(csv.reader(lines))

    r = subprocess.run([ 
            "nvidia-smi", 
            "--format=csv,noheader", 
            "--query-compute-apps=gpu_bus_id" 
        ], stdout=subprocess.PIPE)

    lines = r.stdout.decode('utf-8').strip().split('\n')
    compute_apps = list(csv.reader(lines))

    for n in range(len(gpu_devices)):
        dev = gpu_devices[n]
        found = False
        for app in compute_apps:
            if not app:
                continue
            if app[0].strip() == dev[1].strip():
                found = True
        if not found:
            return dev[0]


@magics_class
class VisibleDevices(Magics):
    def __init__(self, ip):
        self.shell = ip

    def __init__(self, shell):
        super(VisibleDevices, self).__init__(shell=shell)

    @line_magic
    def reserve_gpu(self, index):
        if not index:
            index = available_device()
            if index is None:
                print("No available GPU devices to reserve")
                return

        self.shell.ex("import os")

        try:
            n = int(index)
            dev = gpu_devices[n]
            bus = dev[1].strip()
            name = dev[2].strip()
            memory = dev[3].strip()
            print("Reserving GPU %s: %s %s" % (n, bus, name))
            print("CUDA_DEVICE_MEMORY = '%s'" % memory)
            self.shell.ex("os.environ['CUDA_DEVICE_MEMORY'] = '%s'" % memory)
        except:
            pass

        print("CUDA_VISIBLE_DEVICES = '%s'" % index)
        self.shell.ex("os.environ['CUDA_VISIBLE_DEVICES'] = '%s'" % index)
        

def load_ipython_extension(ip):
    magics = VisibleDevices(ip)
    ip.register_magics(magics)


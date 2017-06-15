
import os
import csv
import subprocess

from IPython.core.magic import Magics, magics_class, line_magic


gpu_devices = None

def available_device():
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
            if app:
                bus = app[0].strip()
                if bus == dev['bus']:
                    found = True
        if not found:
            return n


@magics_class
class VisibleDevices(Magics):
    def __init__(self, ip):
        self.shell = ip

    def __init__(self, shell):
        super(VisibleDevices, self).__init__(shell=shell)

    @line_magic
    def reserve_gpu(self, index):
        global gpu_devices

        if gpu_devices is None: 
            r = subprocess.run([
                    "nvidia-smi", 
                    "--format=csv,noheader,nounits",
                    "--query-gpu=pci.bus_id,name,memory.total,vbios_version,pcie.link.width.current"
                ], stdout=subprocess.PIPE)
            lines = r.stdout.decode('utf-8').strip().split('\n')
            gpu_devices = list(map(lambda d: { 
                    'bus': d[0].strip(),
                    'name': d[1].strip(),
                    'memory': d[2].strip(),
                    'vbios': d[3].strip(),
                    'width': d[4].strip()
                }, csv.reader(lines)))

        if not index:
            index = available_device()
            if index is None:
                print("No available GPU devices to reserve")
                return

        self.shell.ex("import os")

        try:
            n = int(index)
            dev = gpu_devices[n]
            print("Reserving GPU%s: %s %sx %s (VBIOS %s)" % (n, 
                  dev['bus'], dev['width'], dev['name'], dev['vbios']))
            print("CUDA_DEVICE_MEMORY = '%s'" % dev['memory'])
            self.shell.ex("os.environ['CUDA_DEVICE_MEMORY'] = '%s'" % dev['memory'])
        except:
            pass

        print("CUDA_DEVICE_ORDER = 'PCI_BUS_ID'")
        print("CUDA_VISIBLE_DEVICES = '%s'" % index)
        self.shell.ex("os.environ['CUDA_DEVICE_ORDER'] = 'PCI_BUS_ID'")
        self.shell.ex("os.environ['CUDA_VISIBLE_DEVICES'] = '%s'" % index)
        

def load_ipython_extension(ip):
    magics = VisibleDevices(ip)
    ip.register_magics(magics)


## %reserve\_gpu

As you know deep learning is a very computational intensive task and as such
relies on GPUs to train its neural networks.  In a way today's GPUs
are yesterday's 8087 math coprocessors, only now a computer can have
more than one GPUs inside it.

This is where the jupyter extension %reserve\_gpu provided here helps.
Instead of only being able to train one net at a time with jupyter,
with this extension you can open multiple jupyter notebooks and train as
many nets concurrently as you have GPUs without having to hard code the GPU
number.  The extension automatically finds the first free GPU and reserves it.

For example here is sample jupyter notebook cell:


The extension does the reservation by setting the environment variable
CUDA\_VISIBLE\_DEVICES to the device number of the GPU it found.  As a convenience,
the amount of ram on the free GPU is set in the environment variable CUDA\_DEVICE\_MEMORY.
If no GPUs are free the extension displays a message saying there are no free GPU devices.
The extension also takes the GPU device number as an argument if you want to reserve
a specific or multiple GPUs.  It also displays information about the GPU if it can find it.

To install this extension you can run "sh install.sh" as a non-root user.
This will copy the extension, reserve\_gpu.py into ~/.ipython/extensions/
as well as overwrite the file ~/.ipython/profile\_default/ipython\_config.py
in order to make the extension load automatically.  If you want the extension to be
a python library instead you can copy this repo into your python dist-packages
directory.  If you want to load the extension manually you can use %load\_ext in
your jupyter notebook instead of modifying ipython\_config.py



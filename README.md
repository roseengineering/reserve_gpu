## %reserve\_gpu

As you know deep learning is a very computational intensive task and as such
relies on GPUs to train its neural networks.  In a way today's GPUs
are yesterday's 8087 math coprocessors, only now a computer can have
more than one GPUs inside it.

This is where the jupyter extension %reserve\_gpu provided here was made to
help.  Instead of being only able to train one net at a time with jupyter, 
you can now open multiple jupyter notebooks and train as many nets concurrently 
as you have GPUs without having to hard code the GPU number.  The extension 
automatically finds the first free GPU and reserves it.

It does this by setting the environment variable CUDA\_VISIBLE\_DEVICES to the 
device number of the GPU found.  As a convenience, the amount of ram on the free GPU 
is set in the environment variable CUDA\_DEVICE\_MEMORY.  If no GPUs are free 
the extension displays a message saying there are no free GPU devices.  
The extension can also take the GPU device as an argument if you want to reserve 
a specific or multiple GPUs.  It also displays information about the GPU it found.

Below is an example jupyter notebook cell:



To install this extension you can run "sh install.sh" as a non-root user.  
This will copy the extension, reserve\_gpu.py into ~/.ipython/extensions/ 
as well as overwrite the file ~/.ipython/profile\_default/ipython\_config.py 
in order to make the extension load automatically.  If you want the extension to be 
a python library instead you can copy this repo into your python dist-packages 
directory.  If you want to load the extension manually you can use %load\_ext in
your jupyter notebook instead of modifying ipython\_config.py



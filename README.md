## %reserve\_gpu

Deep learning is a very computational intensive task and as such
relies on GPUs to train its neural networks.  Today's GPUs
are yesterday's math coprocessors, only now a computer can have
multiple GPUs inside it, not just one.

This is where %reserve\_gpu comes in.
Normally you can only train one net at a time with jupyter
unless the GPU device number is hard coded in your notebooks.  

This extension finds the first free GPU and reserves it -- and only it.
This leaves the other GPUs free to be used by other notebooks.
In this way each notebook will have its own personal GPU.
So you can train as many nets concurrently as you have GPUs.

For example here is sample jupyter notebook cell:

```python
# Fit the model
%reserve_gpu
from time import perf_counter
model = baseline_model()
t = perf_counter()
model.fit(X_train, y_train, validation_data=(X_test, y_test), 
          epochs=10, batch_size=200, verbose=0)
print("Training time: %.2fs" % (perf_counter() - t))
scores = model.evaluate(X_test, y_test, verbose=0)
print("Baseline Error: %.2f%%" % (100-scores[1]*100))
```
```
Reserving GPU2: 0000:03:00.0 16x GeForce GTX 1050 Ti (VBIOS 86.07.22.00.A8)
CUDA_DEVICE_MEMORY = '4038'
CUDA_DEVICE_ORDER = 'PCI_BUS_ID'
CUDA_VISIBLE_DEVICES = '2'
Training time: 191.74s
Baseline Error: 1.02%
```

The extension does the reservation by setting the environment variable
CUDA\_VISIBLE\_DEVICES to the device number of the GPU it found.  As a convenience,
the amount of ram in MB on the free GPU is set in the environment variable CUDA\_DEVICE\_MEMORY.
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

Copyright 2017 roseengineering

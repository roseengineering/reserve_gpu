## %reserve\_gpu

Deep learning is a very computational intensive task and as such
relies on GPUs to train its neural networks.  Today's GPUs
are yesterday's math coprocessors, only now a computer can have
multiple GPUs inside it, not just one.

This is where the extension %reserve\_gpu here helps.
Normally you can only train one net at a time with jupyter
unless the GPU device number is hard coded in your notebooks.  
But by using this extension you can train as many nets concurrently as you have GPUs
The extension automatically finds the first free GPU and reserves it, and only it.
This leaves the other GPUs free to be used by other notebooks.
In this way each notebook will have its own personal GPU.

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

Reserving GPU 0: 0000:01:00.0 GeForce 940MX
CUDA_DEVICE_MEMORY = '2002'
CUDA_VISIBLE_DEVICES = '0'
Training time: 191.74s
Baseline Error: 1.02%
```

The extension does the reservation by setting the environment variable
CUDA\_VISIBLE\_DEVICES to the device number of the GPU it found.  As a convenience,
the amount of MB on the free GPU is set in the environment variable CUDA\_DEVICE\_MEMORY.
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



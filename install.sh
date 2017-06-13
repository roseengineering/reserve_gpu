
mkdir -p ~/.ipython/extensions
mkdir -p ~/.ipython/profile_default

cp reserve_gpu.py ~/.ipython/extensions
tee ~/.ipython/profile_default/ipython_config.py <<EOF
c.InteractiveShellApp.extensions = [ 'reserve_gpu' ]
EOF


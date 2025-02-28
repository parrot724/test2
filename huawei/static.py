import os

if not os.path.exists(os.path.abspath('./tmp/classes')):
    os.makedirs(os.path.abspath('./tmp/classes'))
else:
    os.chdir(os.path.abspath('./tmp/classes'))
print('serving files in: %s' % os.getcwd())
os.system(r'python -m http.server 5500 --bind 127.0.0.1')

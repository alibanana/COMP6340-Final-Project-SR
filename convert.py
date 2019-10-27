import os
import sys
import site

print("Designer Path : ", site.getsitepackages())

command = 'cd ' + os.path.dirname(sys.executable)
os.system(command)

command1 = 'pyuic5 -x ""'
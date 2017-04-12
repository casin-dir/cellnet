import os
import subprocess
import sys


child = os.path.join(os.path.dirname(__file__), "./child.py")
word = 'word'
file = ['./parent.py', './child.py']

# print(__file__)

pipes = []
for i in range(0,2):
  # command = [sys.executable, child, параметр 1]
  command = [sys.executable, child, 'COM{0}'.format(i)]
  # pipe = subprocess.Popen(command, stdin=subprocess.PIPE)
  pipe = subprocess.Popen(command)
  pipes.append(pipe)
  # pipes.append(pipe)
  # pipe.stdin.write(word.encode("utf8") + b"\n")
  # pipe.stdin.write(file[i].encode("utf8") + b"\n")
  # pipe.stdin.close()

while pipes:
    pipe = pipes.pop()
    pipe.wait()
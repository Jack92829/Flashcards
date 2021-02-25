import subprocess

proc = subprocess.Popen(('python','Test.py'), stdout=subprocess.PIPE)

for line in proc.stdout.readlines():
    print(line)
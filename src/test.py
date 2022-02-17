import os

total_memory, used_memory, free_memory = map(int, os.popen('free -t -m').readlines()[-1].split()[1:])
# Memory usage
ramuseint = (used_memory/total_memory) * 100, 2
ramusestr = str(ramuseint)
print("Benutzter RAM: " + ramusestr)
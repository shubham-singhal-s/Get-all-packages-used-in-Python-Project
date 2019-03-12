import os, re, subprocess, json, sys

p1 = re.compile(r'import (.+)\n')
p2 = re.compile(r'from (.+) import .*\n')
imports = []
path1 = sys.argv[1]
for root, dirs, files in os.walk("./"+path1):
    path = root.split(os.sep)
    for file in files:
        if file[-3:]=='.py':
            f = open(root+'/'+file,'r').read()
            arr = p1.findall(f)
            arr += p2.findall(f)
            for i in arr:
                ele = [x.split(' as')[0].split('.')[0].replace('_','-').strip() for x in i.split(',')]
                for x in ele:
                    if x not in imports:
                        imports.append(str(x))

x = subprocess.Popen('pip list --format=json', stdout=subprocess.PIPE)
string  = json.loads(x.stdout.read().decode('utf8'))

for i in imports:
    for j in string:
        if i.lower() in j['name'].lower().split('.'):
            print(j['name']+':'+j['version'])
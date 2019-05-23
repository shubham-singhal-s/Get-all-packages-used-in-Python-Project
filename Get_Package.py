import os, re, subprocess, json, sys

p1 = re.compile(r'import (.+)\n')
p2 = re.compile(r'from (\S+) import.*\n')
p3 = re.compile(r'import (\S+) as.*\n')
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
print(imports)
x = subprocess.Popen('pip list --format=json', stdout=subprocess.PIPE)
pack_dict  = json.loads(x.stdout.read().decode('utf8'))
ans_arr = []
for i in imports:

    for j in pack_dict:
        if i.lower().replace('-','') in j['name'].lower().replace('-','').split('.'):
            ans_arr.append(j['name']+'=='+j['version'])
f = open('requirements1.txt','w+')
[f.write(a+'\n') for a in ans_arr]
f.close()

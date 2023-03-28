from os import listdir
from os.path import isfile, join


def getNameOfFiles(mypath):
  onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
  return onlyfiles

def makeNet():
  path = "./OSPFNeighbor"
  path2 = "./OSPFStatus"
  routers = getNameOfFiles(path)
  print(routers)
  data = {}
  for r in routers:
    f = open(path + "/"+ r, 'r')
    lines = f.readlines()
    f.close()
    print("----------------------------------------------------------------------------------")
    temp = []
    for l in lines:
      if l != '\n':
        l = l[:-1]
        if "show" not in l and r.split('.')[0] not in l and "Neighbor" not in l:
          print(l)
          temp.append(l.split())
        if r not in l:
          name = r
    f = open(path2 + "/"+ r, 'r')
    lines = f.readlines()
    f.close()
    for l in lines:
      if l != '\n':
        l = l[:-1]
        if "Routing Process" in l:
          print(l)
          id = l.split()[-1]


    data[name] = {'table':temp.copy(), 'id': id}
  f = open("myfile.txt", "w")
  for n, d in data.items():
    print("----------------------------------------------------------------")
    print(n)
    for row in d['table']:
      print(row)
      f.write(d['id'] + "-->" + row[0] + '\n')
  f.close()


makeNet()
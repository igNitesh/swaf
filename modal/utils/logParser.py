f = open('/home/eliot/Desktop/major project/swaf/modal/dataset/normalTrafficTraining.txt','r')

data = f.readlines()


for i in data:
    print(i.split())
    if(i[0] == '\n'):
        break
'''
filei = open("./KGAT/ml1m/item_list.txt", 'r')
reader = csv.reader(filei, delimiter=" ")
maxitemlist = 0
maxorgitemlist = 0
next(reader, None)
for row in reader:
    maxitemlist = int(row[1]) if int(row[1]) > maxitemlist else maxitemlist
    maxorgitemlist = int(row[0]) if int(row[0]) > maxorgitemlist else maxorgitemlist
filei.close()

filei = open("KGAT/ml1m/kg_final.txt", 'r')
reader = csv.reader(filei, delimiter=" ")
maxkg = 0
next(reader, None)
for row in reader:
    maxkg = int(row[0]) if int(row[0]) > maxkg else maxkg
filei.close()

print("max newid: {}, max orgid: {}, maxkg: {}".format(maxitemlist, maxorgitemlist, maxkg))
exit(-1)
'''
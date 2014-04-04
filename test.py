#!/usr/bin/python

import psycopg2
import pprint
import yaml

conn = psycopg2.connect(host="localhost",database="newdakdb",user="postgres",password="postgres")
cur = conn.cursor()
#cur.execute("select * from binaries_metadata")
#cur.execute("select  id,package,type from binaries")

#cur.execute("select * from files")

#cur.execute("select bin,s.suite_name from bin_associations b, suite s where b.suite = s.id")

sql2='''select b.package,b.version, s.source, a.arch_string 
        from binaries b, architecture a, source s
        where
        b.architecture = a.id and s.id = b.source;'''

cur.execute(sql2)

res = cur.fetchall()
ofile = open("Components.yml","w")

for r in res:
    dic = {'Package':r[0],'Version':r[1],'Source':r[2],'Arch':r[3]}
    data = yaml.dump(dic,default_flow_style=False,explicit_start=True)
    ofile.write(data)
    ofile.write("\n")

conn.close()
ofile.close()

#pprint.pprint(res)
#print res


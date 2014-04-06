#!/usr/bin/python

import psycopg2
import pprint
import yaml

conn = psycopg2.connect(host="localhost",database="newdakdb",user="postgres",password="postgres")
cur = conn.cursor()

sql_str1='''select b.package,b.version, s.source, a.arch_string, su.suite_name, f.filename, ar.name, su.id, ar.path
        from binaries b, architecture a, source s, bin_associations ba,suite su, files f, archive ar
        where
        b.architecture = a.id and s.id = b.source and b.id = ba.bin and su.id = ba.suite and f.id = b.file and ar.id = su.archive_id'''

cur.execute(sql_str1)

res = cur.fetchall()
ofile = open("Components.yml","w")

for r in res:
    dic = {'Package':r[0],'Version':r[1],'Source':r[2],'Arch':r[3],'Suite':r[4],'File':r[5],'Archive':r[6],'Path':r[8]}
    ##Query is used to get the Component field##
    sql_str2 = '''select c.name 
              from  component_suite cs, component c 
              where 
              cs.suite_id = %s and cs.component_id = c.id;'''%(r[7])
    cur.execute(sql_str2)
    comp = cur.fetchall()
    comp_str = ""
    for c in comp:
        comp_str = comp_str + c[0] + " "

    dic['Component']=comp_str
    data = yaml.dump(dic,default_flow_style=False,explicit_start=True)
    ofile.write(data)
    ofile.write("\n")

conn.close()
ofile.close()

#pprint.pprint(res)
#print res


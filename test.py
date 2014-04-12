#!/usr/bin/python

import pprint
import yaml
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost/newdakdb')
Session = sessionmaker(bind=engine)
session = Session()

sql_str1='''select b.package,b.version, s.source, a.arch_string, su.suite_name, f.filename, ar.name, su.id, ar.path
        from binaries b, architecture a, source s, bin_associations ba,suite su, files f, archive ar
        where
        b.created > '2014-01-01' and b.architecture = a.id and s.id = b.source and b.id = ba.bin and su.id = ba.suite and f.id = b.file and ar.id = su.archive_id'''

result = session.execute(sql_str1)
res = result.fetchall()
ofile = open("components.yml","w")

for r in res:
    dic = {'Package':str(r[0]),'Version':str(r[1]),'Source':str(r[2]),'Arch':str(r[3]),'Suite':str(r[4]),'File':str(r[5]),'Archive':str(r[6]),'Path':str(r[8])}

    ##Query is used to get the Component field##
    sql_str2 = '''select c.name 
              from  component_suite cs, component c 
              where 
              cs.suite_id = %s and cs.component_id = c.id;'''%(str(r[7]))
    comp=session.execute(sql_str2)
    comp_str = ""
    for c in comp:
        comp_str = comp_str + str(c[0]) + " "

    dic['Component']=comp_str.rstrip()
    
    data = yaml.dump(dic,default_flow_style=False,explicit_start=True)
    ofile.write(data)
    ofile.write("\n")
    
session.flush()
ofile.close()

#pprint.pprint(res)
#print res

import mysql.connector
from collections import namedtuple

student = namedtuple("student","id name dob grade address parent_name")

myCon = mysql.connector.connect(
    host="localhost",
    user="sachin",
    password="rockey@123",
    database="pypos"
)

csr = myCon.cursor()

sql = "INSERT INTO student(name,dob,grade,address,parent_name) VALUES(%s,%s,%s,%s,%s)"
values = ("Nimal","1997-12-06","6","Panadura","ABC")

csr.execute(sql,values)

myCon.commit()

print(csr.rowcount)

sql =  "SELECT * FROM student"

csr.execute(sql)
result = csr.fetchall()

for re in result:
    st = student(*re)
    print(st)
    print(st.name)

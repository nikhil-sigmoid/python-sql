#Importing Psycopg as the PostgreSQL database adapter
import psycopg2

import pandas as pd

from config import config
import logging

logging.basicConfig(level=logging.INFO)

#Write a Python program to list employee numbers, names and their managers and save in a xlsx file.

def solution1(cur):
    cur.execute("select e.empno,e.ename,m.ename from emp as e inner join emp as m on e.mgr=m.empno")
    df=pd.DataFrame(cur.fetchall())
    df.to_excel('Solu.xlsx',header=["E_Id","E_Name","M_Name"],index=False)

#Write a python program to list the Total compensation  given till his/her last date or till now of all the employees till date in a xlsx file.
 #columns required: Emp Name, Emp No, Dept Name, Total Compensation, Months Spent in Organization

def solution2(cur):
    cur.execute(
        "select e.empno,e.ename,d.dname,comms.comm*comms.mon,comms.mon "
        "from (select empno,Cast(((Cast (Current_date-min(startdate) as float))/365.0*12) as Int) as mon,"
        ""
        "sum(CASE when comm is not null then comm else 0 end) comm from jobhist group by(empno)) comms "
        "inner join emp e on e.empno=comms.empno inner join dept d on d.deptno=e.deptno")
    df2 = pd.DataFrame(cur.fetchall())
    df2.to_excel('compensation.xlsx',
                 header=[ "Emp No","Emp Name", "Dept Name", "Total Compensation", "Months Spent in Organization"],
                 index=False)
    df2.to_csv('c.csv',
               header=["Emp No","Emp Name", "Dept Name", "Total Compensation", "Months Spent in Organization"],
               index=False)

#Read and upload the above xlsx in 2) into a new table in the Postgres DB

def solution3(cur):
    ''' From 40-41  Should  have  to read excel first then convert to csv '''
    cur.execute("COPY EmpTable FROM '/Users/nikhil/python-sql-assignment/c.csv' "
                "DELIMITER ',' CSV HEADER;")

#From the xlsx in 2) create another xlsx to list total compensation given at Department level till date. Columns: Dept No, Dept,Name, Compensation

def solution4(cur):

    cur.execute(
        "select d.deptno,d.dname,Case when e.c is null then 0 else e.c end from "
        "(select deptname,sum(comm)as c from EmpTable group by(deptname)) e right join dept d on d.dname=e.deptname")
    df3 = pd.DataFrame(cur.fetchall())
    df3.to_excel('deptcomm.xlsx', header=["Dept No", "Dept Name", "Compensation"], index=False)


#Connect to the PostgreSQL database server

def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        '''Should use logging'''
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        '''Shoud use logging'''
        print('PostgreSQL database version:')

        # display the PostgreSQL database server version


        # close the communication with the PostgreSQL

        solution1(cur)

        solution2(cur)

        solution3(cur)

        solution4(cur)

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        '''Should use logging'''
        print(error)
    finally:
        if conn is not None:
            conn.close()
            '''Should use logging'''
            print('Database connection closed.')


if __name__ == '__main__':
    connect()

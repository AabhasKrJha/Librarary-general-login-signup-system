import mysql.connector as sql
from sql_syntax import *
from basic_operations import gen_libID, hash, check_email, create_libID_file, make_list
import config as cfg

try:
    user = cfg.mysql['user']
    pwd = cfg.mysql['password']
    host = cfg.mysql['host']
except:
    pass


def create_db_model(db_name, user=user, host=host, db_pwd=pwd):

    create_libID_file()

    conn = sql.connect(user=user, host=host,
                       password=db_pwd, database='mysql')
    cur = conn.cursor()

    def create_tables():
        create_table(db_name, create_table_sql, 'reader')
        create_table(db_name, create_table_sql, 'authority')
        create_table(db_name, create_table_sql, 'author')
        create_table(db_name, create_authCode_table_sql, 'code')
        create_table(db_name, job_applicant_table_sql, 'job_applicants')

    try:
        cur.execute(f'create database {db_name}')
        create_tables()

    except:
        create_tables()

    cur.close()
    conn.commit()
    conn.close()


def create_connection(db_name, user=user, host=host, db_pwd=pwd):
    try:
        conn = sql.connect(user=user, host=host,
                           password=db_pwd, database=db_name)
        return conn
    except:
        create_db_model(db_name)
        return create_connection(db_name)


def create_table(db_name, table_sql, tablename):
    conn = create_connection(db_name)
    cur = conn.cursor()

    cur.execute(table_sql.format(tablename=tablename))

    cur.close()
    conn.close()


def add_user(db_name, name, email, phone, designation, password):

    conn = create_connection(db_name)
    cur = conn.cursor()

    tablename = designation
    libraryID = gen_libID(designation)
    password = hash(password)

    sql = insert_table_data_sql.format(tablename=tablename)
    values = (name, libraryID, email, phone, password)
    cur.execute(sql, values)

    conn.commit()
    cur.close()
    conn.close()


def login_reader(db_name, tablename, ID, password):

    conn = create_connection(db_name)
    cur = conn.cursor()

    password = hash(password)
    values = (ID,)
    credential = check_email(ID)

    if credential:
        sql = f'select * from {tablename} where email=%s'
    else:
        sql = f'select * from {tablename} where libraryID=%s'

    cur.execute(sql, values)
    row = cur.fetchall()

    conn.commit()
    cur.close()
    conn.close()

    if row:
        data = row[0]
        if password == data[5]:
            return True
        else:
            return 'password'
    else:
        if credential:
            return 'email'
        else:
            return 'libID'


def add_auth(db_name, name, email, phone, password):

    conn = create_connection(db_name)
    cur = conn.cursor()

    tablename = 'authority'
    libraryID = gen_libID("authority")
    password = hash(password)

    sql = insert_table_data_sql.format(tablename=tablename)
    values = (name, libraryID, email, phone, password)

    cur.execute(sql, values)

    conn.commit()
    cur.close()
    conn.close()


def insert_code(db_name, email, code, designation):

    conn = create_connection(db_name)
    cur = conn.cursor()

    sql = 'INSERT INTO code VALUES(%s,%s,%s)'
    values = (email, code, designation)
    cur.execute(sql, values)

    conn.commit()
    cur.close()
    conn.close()


def find_code(db_name, email, code):

    conn = create_connection(db_name)
    cur = conn.cursor()

    sql = 'select * from code where email=%s and code=%s'
    values = (email, code)

    cur.execute(sql, values)
    row = cur.fetchall()

    cur.close()
    conn.close()

    if row:
        return True
    else:
        return False


def send_job_applications(db_name, name, email, phone, designation):

    conn = create_connection(db_name)
    cur = conn.cursor()

    sql = insert_job_applications_sql
    values = (name, email, phone, designation)

    cur.execute(sql, values)

    conn.commit()
    cur.close()
    conn.close()


def reset_password(db_name, email, password, designation):

    conn = create_connection(db_name)
    cur = conn.cursor()

    sql = "UPDATE {tablename} SET password=%s where email=%s".format(
        tablename=designation)

    pwd = hash(password)
    values = (pwd, email)

    cur.execute(sql, values)

    conn.commit()
    cur.close()
    conn.close()


def check_job_availability(db_name, designation):

    conn = create_connection(db_name)
    cur = conn.cursor()

    if designation == 'head':
        sql = "select * from authority where libraryID='auth01'"
    else:
        sql = 'select * from authority'

    cur.execute(sql)

    data = cur.fetchall()

    cur.close()
    conn.close()

    if len(data) == 4:
        return False
    else:
        return True


def get_applications(db_name):

    conn = create_connection(db_name)
    cur = conn.cursor()

    sql = 'select * from job_applicants'

    cur.execute(sql)
    rows = cur.fetchall()

    data = []
    for row in rows:
        data.append(list(row))

    cur.close()
    conn.close()

    return data

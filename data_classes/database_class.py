import os.path
import sqlite3
import datetime
from helper import consts

primaryTb = 'primaryTb'
finalTb = 'finalTb'

CREATE_PRIMARY_TABLE = 'CREATE TABLE IF NOT EXISTS primaryTb (doc_num TEXT NOT NULL,vol_no TEXT,cap_strt INTEGER NOT ' \
                       'NULL, cap_cmplet INTEGER NOT NULL, pross_strt INTEGER NOT NULL, pross_cmplet INTEGER NOT ' \
                       'NULL, pdf_cretd INTEGER NOT NULL); '
CREATE_FINAL_TABLE = 'CREATE TABLE IF NOT EXISTS finalTb(sl_no INTEGER  PRIMARY KEY AUTOINCREMENT , doc_num  TEXT NOT NULL, ' \
                     'created_on TEXT NOT NULL );'
INSERT_DOC_PRIMARY = 'INSERT INTO primaryTb(doc_num, vol_no, cap_strt, cap_cmplet, pross_strt, pross_cmplet, ' \
                     'pdf_cretd  ) VALUES (?,?,?,?,?,?,?);'
INSERT_DOC_FINAL = 'INSERT INTO finalTb(doc_num,created_on) VALUES (?,?);'
GET_ALL_DOC_FROM_PRIMARY = 'SELECT * FROM primaryTb;'
GET_ALL_DOC_FROM_FINAL = 'SELECT * FROM finalTb;'
update_c_strt = 'UPDATE primaryTb set cap_strt = ? WHERE doc_num = ?'
update_c_cmplte = 'UPDATE primaryTb set cap_cmplet = ? WHERE doc_num = ?'
update_p_strt = 'UPDATE primaryTb set pross_strt = ? WHERE doc_num = ?'
update_p_cmplte = 'UPDATE primaryTb set pross_cmplet = ? WHERE doc_num = ?'
update_pdf = 'UPDATE primaryTb set pdf_cretd = ? WHERE doc_num = ?'

delete_pri_doc_row = 'DELETE FROM primaryTb WHERE doc_num = ?'


def connect():
    return sqlite3.connect(os.path.join(consts.db_dir,'document.db' ))


def create_primary_table(connection):
    try:
        with connection:
            connection.execute(CREATE_PRIMARY_TABLE)
    except:
        pass


def create_final_table(connection):
    try:
        with connection:
            connection.execute(CREATE_FINAL_TABLE)
    except:
        pass


def add_doc_to_primary_tb(connection, doc_no, volume='', c_strt=0, c_cmpt=0, p_strt=0, p_cmplt=0, pdf=0):
    try:
        with connection:
            connection.execute(INSERT_DOC_PRIMARY, (doc_no, volume, c_strt, c_cmpt, p_strt, p_cmplt, pdf))
    except:
        pass


def set_capture_start(connection, doc_no):
    try:
        with connection:
            connection.execute(update_c_strt, (1, doc_no))
    except:
        pass



def set_capture_complete(connection, doc_no):
    try:
        with connection:
            connection.execute(update_c_cmplte, (1, doc_no))
    except:
        pass



def set_process_start(connection, doc_no):
    try:
        with connection:
            connection.execute(update_p_strt, (1, doc_no))
    except:
        pass



def set_process_cmplete(connection, doc_no):
    try:
        with connection:
            connection.execute(update_p_cmplte, (1, doc_no))
    except:
        pass



def set_pdf(connection, doc_no):
    try:
        with connection:
            connection.execute(update_pdf, (1, doc_no))
    except:
        pass



def del_doc_from_primaryTb(connection, doc_num):
    try:
        with connection:
            connection.execute(delete_pri_doc_row, (doc_num,))
    except:
        pass



def add_doc_to_final_tb(connection, doc_num):
    try:
        insert_date = (str(datetime.datetime.now())).split('.')[0]
        with connection:
            connection.execute(INSERT_DOC_FINAL, (doc_num, insert_date))
    except:
        pass



def get_doc_from_primary(connection):
    try:
        with connection:
            return connection.execute(GET_ALL_DOC_FROM_PRIMARY).fetchall()
    except:
        pass
def get_docs_from_final_table(connection):
    try:
        with connection:
            return connection.execute(GET_ALL_DOC_FROM_FINAL).fetchall()
    except:
        pass


# ---------FOR ALL VALUE
# INSERT INTO INITIALDOC VALUES ('01-01-2013', '10', False, False, False, False, False)
# -------------FOR SPECIFIC VALUES
# INSERT INTO INITIALDOC (doc_num,vol_no,cap_cmplet,) VALUES ('01-01-2013', '10', False,)
# --TO SELECT ALL
# SELECT * FROM  INITIALDOC
# ----- TO SELECT SOME THINF
# SELECT cap_strt cap_cmplet  FROM INITIALDOC

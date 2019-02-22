import pymysql

connection = pymysql.connect(host='localhost',
                             user='test',
                             password='test')

connection.cursor().execute('CREATE DATABASE IF NOT EXISTS atlanta_zoo')

tables = dict()

tables['USER'] = ('CREATE TABLE IF NOT EXISTS USER '
                  '(USERNAME CHAR(30),'
                  'EMAIL CHAR(30) NOT NULL UNIQUE ,'
                  'TYPE CHAR(30)NOT NULL, '
                  'PASSWORD_HASH CHAR(255) NOT NULL,'
                  'PRIMARY KEY (USERNAME))')

tables['ADMIN'] = ('CREATE TABLE IF NOT EXISTS ADMIN'
                   '(USERNAME CHAR(30),'
                   'PRIMARY KEY (USERNAME),'
                   'FOREIGN KEY (USERNAME) REFERENCES USER(USERNAME) ON DELETE CASCADE)')

tables['VISITOR'] = ('CREATE TABLE IF NOT EXISTS VISITOR'
                     '(USERNAME CHAR(30),'
                     'PRIMARY KEY (USERNAME),'
                     'FOREIGN KEY (USERNAME) REFERENCES USER(USERNAME) ON DELETE CASCADE)')

tables['STAFF'] = ('CREATE TABLE IF NOT EXISTS STAFF'
                   '(USERNAME CHAR(30),'
                   'PRIMARY KEY (USERNAME),'
                   'FOREIGN KEY (USERNAME) REFERENCES USER(USERNAME) ON DELETE CASCADE)')

tables['EXHIBIT'] = ('CREATE TABLE IF NOT EXISTS EXHIBIT'
                     '(NAME CHAR(30),'
                     'WATER BOOL,'
                     'SIZE INT,'
                     'PRIMARY KEY (NAME))')

tables['ANIMAL'] = ('CREATE TABLE IF NOT EXISTS ANIMAL'
                    '(NAME CHAR(30),'
                    'SPECIES CHAR(30),'
                    'TYPE CHAR(30),'
                    'AGE INT,'
                    'EXHIBIT CHAR(30),'
                    'PRIMARY KEY (NAME, SPECIES),'
                    'FOREIGN KEY (EXHIBIT) REFERENCES EXHIBIT(NAME))')

tables['SHOW'] = ('CREATE TABLE IF NOT EXISTS SHOW'
                  '(NAME CHAR(30),'
                  'DATE_TIME DATETIME,'
                  'HOST CHAR(30),'
                  'EXHIBIT CHAR(30),'
                  'PRIMARY KEY (NAME, DATE_TIME),'
                  'FOREIGN KEY (EXHIBIT) REFERENCES EXHIBIT(NAME),'
                  'FOREIGN KEY (HOST) REFERENCES STAFF(USERNAME) ON DELETE SET NULL)')

tables['ANIMAL_CARE'] = ('CREATE TABLE IF NOT EXISTS ANIMAL_CARE'
                         '(ANIMAL CHAR(30),'
                         'SPECIES CHAR(30),'
                         'STAFF_MEMBER CHAR(30),'
                         'DATE_TIME DATETIME,'
                         'NOTE TEXT,'
                         'PRIMARY KEY (ANIMAL, SPECIES, STAFF_MEMBER, DATE_TIME),'
                         'FOREIGN KEY (ANIMAL, SPECIES) REFERENCES ANIMAL(NAME, SPECIES) ON DELETE CASCADE,'
                         'FOREIGN KEY (STAFF_MEMBER) REFERENCES STAFF(USERNAME) ON DELETE CASCADE)')

tables['VISIT_SHOW'] = ('CREATE TABLE IF NOT EXISTS VISIT_SHOW'
                        '(SHOW_NAME CHAR(30),'
                        'DATE_TIME DATETIME,'
                        'VISITOR CHAR(30),'
                        'PRIMARY KEY (SHOW_NAME, DATE_TIME, VISITOR),'
                        'FOREIGN KEY (SHOW_NAME, DATE_TIME) REFERENCES SHOW(NAME, DATE_TIME) ON DELETE CASCADE,'
                        'FOREIGN KEY (VISITOR) REFERENCES VISITOR(USERNAME) ON DELETE CASCADE)')

tables['VISIT_EXHIBIT'] = ('CREATE TABLE IF NOT EXISTS VISIT_EXHIBIT'
                           '(EXHIBIT CHAR(30),'
                           'DATE_TIME DATETIME,'
                           'VISITOR CHAR(30),'
                           'PRIMARY KEY (EXHIBIT, DATE_TIME, VISITOR),'
                           'FOREIGN KEY (EXHIBIT) REFERENCES EXHIBIT(NAME),'
                           'FOREIGN KEY (VISITOR) REFERENCES VISITOR(USERNAME) ON DELETE CASCADE)')

for table_name in tables:
    table_description = tables[table_name]
    try:
        print("Creating table {}: ".format(table_name), end='')
        connection.cursor().execute(table_description)
    except Exception as e:
        print(e)

    else:
        print('OK')

connection.cursor().close()

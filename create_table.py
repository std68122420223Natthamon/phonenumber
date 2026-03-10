sql = '''
  create table phone(
    id integer primary key,
    email text not null,
    name integer not null,
    surname integer not null,
    phonenumber text not null
  );
'''

from db_connect import db, cursor
cursor.execute(sql)
db.commit()

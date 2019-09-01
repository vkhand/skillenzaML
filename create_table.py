import sqlite3

conn = sqlite3.connect("database.db")
c = conn.cursor()

def createTable():
    c.execute('create table if not exists features(field_id varchar(10), work_interface varchar(2), remote_work varchar(2), care_options varchar(2), wellness varchar(2), anonimity varchar(2), leave varchar(2), mental_health varchar(2), phy_health varchar(2), supervisor varchar(2), ment_vs_phy varchar(2), obs varchar(2),treatment varchar(4) NULL, constraint pk_feature primary key(field_id))')
    c.execute('create table if not exists employer(name varchar(20),hr_id varchar(10),no_employees varchar(2),tech_company varchar(2), benifits varchar(2), seek_help varchar(2), constraint pk_hr primary key(hr_id))')
    c.execute('create table if not exists employee(w_id varchar(10),hr_id varchar(10),name varchar(20),age varchar(2),gender varchar(2), family_history varchar(2), constraint pk_emp primary key(w_id,hr_id), constraint fk_emp foreign key(hr_id) references employer(hr_id) on delete cascade)')
    c.execute('create table if not exists fe_em(field_id varchar(10), w_id varchar(10),hr_id varchar(10), constraint pk_feem primary key(field_id,w_id,hr_id), constraint fk1_fe foreign key(field_id) references features(field_id) on delete cascade, constraint fk2_fe foreign key(w_id,hr_id) references employee(w_id,hr_id) on delete cascade)')

createTable()
c.execute("insert into employee values('vik','mayank','vik','20','1','0')")
conn.commit()
c.execute("select * from features")
rows = c.fetchall()
print(rows)
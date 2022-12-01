import sqlite3

from ImportXlsx import XlsxImport


class DataBase:
    def __init__(self):
        self.id = None
        self.conn = sqlite3.connect('patients.db')
        self.cur = self.conn.cursor()
        self.create_table()

    def create_table(self):  # создаем постоянные таблицы

        self.cur.execute(  # Пациенты
            '''CREATE TABLE IF NOT EXISTS patients(
           id integer primary key,
           story text NOT NULL UNIQUE,
           fio text NOT NULL, 
           date_start_illness TEXT,
           date_end_illness TEXT,
           cost real,
           status TEXT,
            UNIQUE ("story") ON CONFLICT IGNORE)''')
        self.conn.commit()

        self.cur.execute(  # Материалы (расходники)
            '''CREATE TABLE IF NOT EXISTS materials(            
           id integer primary key,
           name text NOT NULL UNIQUE, 
           price REAL NOT NULL,
           unit text NOT NULL,
            UNIQUE ("name") ON CONFLICT IGNORE)''')
        self.conn.commit()

        self.cur.execute(  # Все что израсходовано
            '''CREATE TABLE IF NOT EXISTS operations(
           id integer primary key,
           id_patients integer,
           id_materials integer,
           quantity real NOT NULL,
           sum_of real,
           FOREIGN KEY (id_patients)
           REFERENCES patients (id) 
           ON UPDATE CASCADE
           ON DELETE CASCADE,
           FOREIGN KEY (id_materials)
           REFERENCES materials (id) 
           ON UPDATE CASCADE
           ON DELETE CASCADE)''')
        self.conn.commit()

    def add_items(self, name, price, unit):  # создаем расходник
        self.cur.execute("INSERT INTO materials(name, price, unit) VALUES(?,?,?)", (name, price, unit,))
        self.conn.commit()
        return self.cur.lastrowid

    def add_patient(self, story, fio, date_start_illness, date_end_illness, cost, status):  # создаем пациента
        self.cur.execute("INSERT INTO patients(story, fio, date_start_illness, date_end_illness, cost, status) VALUES(?,?,?,?,?,?)",
                         (story, fio, date_start_illness, date_end_illness, cost, status,))
        self.conn.commit()
        return self.cur.lastrowid

    def add_position_cost(self, id_patients, id_materials, quantity, sum_of):
        self.cur.execute("INSERT INTO operations(id_patients, id_materials, quantity, sum_of) VALUES(?,?,?,?)",
                         (id_patients, id_materials, quantity, sum_of,))
        self.conn.commit()
        return self.cur.lastrowid

    def import_from_xls(self, file_name):  # импортируем из экселя
        p = XlsxImport()
        data = p.import_into_list(file_name)
        del p
        for i in data:
            self.add_items(i[0], i[4], i[1])

    def show_patients(self):
        return self.cur.execute('''SELECT * FROM patients''').fetchall()

    def show_materials(self):
        return self.cur.execute('''SELECT * FROM materials''').fetchall()

    def delete_patient(self, id_patient: int):
        self.cur.execute('DELETE from patients where id = {}'.format(id_patient))
        self.conn.commit()

    def delete_operations_of_patient(self, id_patient: int):
        self.cur.execute('DELETE from operations where id_patients = {}'.format(id_patient))
        self.conn.commit()

    def delete_operations_by_id(self, id: int):
        self.cur.execute('DELETE from operations where id = {}'.format(id))
        self.conn.commit()

    def show_operations_of_patient(self, id_patient):
        return self.cur.execute('''SELECT * FROM operations
                                LEFT JOIN materials ON operations.id_materials = materials.id
                                where id_patients = {}'''.format(id_patient)).fetchall()

    def update_patient_sum(self, cost, id):
        self.cur.execute("UPDATE patients SET cost = {} where id = {}".format(cost, id))
        self.conn.commit()


if __name__ == "__main__":
    db = DataBase()
    # print(db.show_materials())
    print(db.show_operations_of_patient(1))
    # db.import_from_xls('obor.xlsx')
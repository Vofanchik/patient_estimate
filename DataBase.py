import sqlite3

# from ImportXlsx import XlsxImport, ODTExport
from odf.opendocument import OpenDocumentText
from odf.style import ParagraphProperties, Style, TableColumnProperties
from odf.table import Table, TableColumn, TableRow, TableCell
from odf.text import P


def form_odt_for_sum_of(data):
    textdoc = OpenDocumentText()

    tablecontents = Style(name="Table Contents", family="paragraph")
    tablecontents.addElement(ParagraphProperties(numberlines="false", linenumber="0"))
    textdoc.styles.addElement(tablecontents)

    widthshort = Style(name="Wshort", family="table-column")
    widthshort.addElement(TableColumnProperties(columnwidth="0.5cm"))
    textdoc.automaticstyles.addElement(widthshort)

    widthmed = Style(name="Wmed", family="table-column")
    widthmed.addElement(TableColumnProperties(columnwidth="2.0cm"))
    textdoc.automaticstyles.addElement(widthmed)

    widthwide = Style(name="Wwide", family="table-column")
    widthwide.addElement(TableColumnProperties(columnwidth="5.5cm"))
    textdoc.automaticstyles.addElement(widthwide)

    table = Table()
    table.addElement(TableColumn(numbercolumnsrepeated=1, stylename=widthwide))
    table.addElement(TableColumn(numbercolumnsrepeated=1, stylename=widthmed))
    table.addElement(TableColumn(numbercolumnsrepeated=1, stylename=widthshort))
    table.addElement(TableColumn(numbercolumnsrepeated=1, stylename=widthmed))
    table.addElement(TableColumn(numbercolumnsrepeated=1, stylename=widthmed))

    col_names = ['Наименование', 'Ед. измерения', 'Кол-во', 'Стоимость за еденицу', 'Сумма за позицию']

    tr = TableRow()
    table.addElement(tr)

    for val in col_names:
        tc = TableCell()
        tr.addElement(tc)
        p = P(stylename=tablecontents, text=val)
        tc.addElement(p)

    for lst in data:
        tr = TableRow()
        table.addElement(tr)

        list_of_cols = [lst[0][0], lst[0][1], lst[0][2], lst[0][3], lst[0][4]]

        for i in list_of_cols:
            tc = TableCell()
            tr.addElement(tc)
            p = P(stylename=tablecontents, text=i)
            tc.addElement(p)

    textdoc.text.addElement(table)

    textdoc.save('itog.odt')


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
           category INTEGER DEFAULT 0,                                                                                                                                                                                                                                                                                                                                                                                                                                             
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

        # cur.execute('''alter table materials add column category integer default 1''')
        # cur.execute('''alter table materials drop column category''')

    def add_items(self, name, price, unit):  # создаем расходник
        self.cur.execute("INSERT INTO materials(name, price, unit) VALUES(?,?,?)", (name, price, unit,))
        self.conn.commit()
        return self.cur.lastrowid

    def add_patient(self, story, fio, date_start_illness, date_end_illness, cost, status):  # создаем пациента
        self.cur.execute(
            "INSERT INTO patients(story, fio, date_start_illness, date_end_illness, cost, status) VALUES(?,?,?,?,?,?)",
            (story, fio, date_start_illness, date_end_illness, cost, status,))
        self.conn.commit()
        return self.cur.lastrowid

    def add_position_cost(self, id_patients, id_materials, quantity, sum_of):
        self.cur.execute("INSERT INTO operations(id_patients, id_materials, quantity, sum_of) VALUES(?,?,?,?)",
                         (id_patients, id_materials, quantity, sum_of,))
        self.conn.commit()
        return self.cur.lastrowid

    # def import_from_xls(self, file_name):  # импортируем из экселя
    #     p = XlsxImport()
    #     data = p.import_into_list(file_name)
    #     del p
    #     for i in data:
    #         self.add_items(i[0], i[4], i[1])

    def show_patients(self):
        return self.cur.execute('''SELECT * FROM patients''').fetchall()

    def show_materials(self):
        return self.cur.execute('''SELECT * FROM materials''').fetchall()

    def show_material_by_id(self, id_material):
        return self.cur.execute('''SELECT * FROM materials where id = {}'''.format(id_material)).fetchone()

    def delete_patient(self, id_patient: int):
        self.cur.execute('DELETE from patients where id = {}'.format(id_patient))
        self.conn.commit()

    def delete_operations_of_patient(self, id_patient: int): # Удаление операции по id пациента
        self.cur.execute('DELETE from operations where id_patients = {}'.format(id_patient))
        self.conn.commit()

    def delete_operations_by_id(self, _id: int):  # Удаление операции по ЕЁ id
        self.cur.execute('DELETE from operations where id = {}'.format(_id))
        self.conn.commit()

    def show_operations_of_patient(self, id_patient):
        return self.cur.execute('''SELECT * FROM operations
                                LEFT JOIN materials ON operations.id_materials = materials.id
                                where id_patients = {}'''.format(id_patient)).fetchall()

    def update_patient_sum(self, cost, _id):
        self.cur.execute("UPDATE patients SET cost = {} where id = {}".format(cost, _id))
        self.conn.commit()


    def show_materials_by_quantity(self):
        return self.cur.execute('''SELECT * FROM operations
                                LEFT JOIN materials ON operations.id_materials = materials.id''').fetchall()

    def show_quantity_of_materials(self):
        id_of_founded_materials = set([a[0] for a in self.cur.execute('''SELECT id_materials FROM operations''')
                                      .fetchall()])
        _all = []
        for items in id_of_founded_materials:
            _all.append(self.cur.execute('''SELECT name, unit, sum(quantity), price, sum(sum_of)  FROM operations
             LEFT JOIN materials ON operations.id_materials = materials.id
             WHERE id_materials = {}'''.format(items)).fetchall())

        return _all

    def update_category_of_materials(self, id_material, new_category):
        self.cur.execute("UPDATE materials SET category = {} where id = {}".format(new_category, id_material))
        self.conn.commit()
        return new_category

if __name__ == "__main__":
    db = DataBase()
    print(db.show_material_by_id(1))
    # data = db.show_quantity_of_materials()
    # pprint(data)
    # db.form_odt_for_sum_of(data)
    # print(db.show_operations_of_patient(1))
    # db.import_from_xls('obor.xlsx')

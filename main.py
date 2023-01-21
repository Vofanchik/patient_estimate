#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import sys
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QFileDialog, QDialog, QTableWidgetItem, QMessageBox, QCompleter

from PyQt5 import QtWidgets, QtCore
from docxtpl import DocxTemplate

from DataBase import DataBase
from ImportXlsx import ODTExport
from UI_files.AddItem import Ui_AddItem
from UI_files.AddPositionToPatient import Ui_AddPositionToPatient
from UI_files.MainWindow import Ui_MainWindow
from UI_files.NewPatient import Ui_NewPatient
from UI_files.PatientAll_costs import Ui_PatientAllCosts
from UI_files.WaitingWindow import Ui_WaitingWidget
from UI_files.AddComplexPosition import Ui_AddComplexMaterial
from UI_files.AddItemtoComplexMaterial import Ui_AddItemToComplexMaterial
#from qt_material import apply_stylesheet

class AddItemToComplexMaterial(QDialog):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ui = Ui_AddItemToComplexMaterial()
        self.ui.setupUi(self)
        self.completer_items()
        self.ui.pushButton.clicked.connect(self.add_item)

    def completer_items(self):
        self.strList_list = db.show_materials()
        self.strList = [i[1] for i in self.strList_list]

        self.completer = QCompleter(self.strList, self.ui.lineEdit)
        self.completer.setCaseSensitivity(False)
        self.completer.setFilterMode(QtCore.Qt.MatchContains)
        self.completer.activated.connect(self.onActivated_competer)
        self.ui.lineEdit.setCompleter(self.completer)

    def onActivated_competer(self):
        self.id_of_position = list(filter(lambda x: x[1] == self.ui.lineEdit.text(), self.strList_list))[0][0]
        self.ui.textEdit.setText(self.ui.lineEdit.text() + ', ' + db.show_material_by_id(self.id_of_position)[3])
        QTimer.singleShot(0, self.ui.lineEdit.clear)

    def update_sum(self):
        try:summa = round(db.show_sum_binded_complex_item(acm.new_material_id)[0],2)
        except: summa = 0
        acm.ui.label_2.setText(str(summa))
        db.update_complex_material_sum(summa, acm.new_material_id)

    def add_item(self):

        info_to_add = {'quantity': round(self.ui.doubleSpinBox_2.value()/self.ui.doubleSpinBox.value(), 2),
                       'id_materials': self.id_of_position,
                       'id_materials_new': acm.new_material_id}
        db.add_complex_material_bind(info_to_add['id_materials'], info_to_add['id_materials_new'],
                                     info_to_add['quantity'])
        # pac.fill_table_operations_of_patient()
        # pac.sum_of_operations()
        # db.update_patient_sum(pac.sum_of_costs, mw.selected_patient_id)
        # mw.fill_table_patients()
        acm.fill_table_items_of_complex_material()
        self.update_sum()
        self.hide()
        self.__init__()


class AddComplexMaterial(QDialog):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.new_material_id = None
        self.ui = Ui_AddComplexMaterial()
        self.ui.setupUi(self)
        self.ui.tableWidget.setColumnHidden(5, True)
        self.sum_of_costs = 0.0
        self.ui.pushButton.clicked.connect(self.open_add_position)
        self.ui.pushButton_3.clicked.connect(self.add_new_material_to_db)
        self.ui.pushButton_2.clicked.connect(self.delete_position)
        self.names_all_materials = [a[0] for a in db.show_materials_names()]

    def add_new_material_to_db(self):
        try:
            if self.ui.lineEdit.text() in self.names_all_materials:
                QMessageBox().warning(self, 'Предупреждение', "Позиция существует",
                                      QMessageBox().Ok)

            else:
                self.new_material_id = db.add_items(self.ui.lineEdit.text(), 0.0, self.ui.lineEdit_2.text(),
                            self.ui.comboBox.currentIndex())
                self.ui.lineEdit.setDisabled(True)
                self.ui.lineEdit_2.setDisabled(True)
                self.ui.comboBox.setDisabled(True)
                self.ui.pushButton_3.setDisabled(True)
                self.ui.pushButton_2.setDisabled(False)
                self.ui.pushButton.setDisabled(False)

        except: QMessageBox().critical(self, 'Предупреждение', "Возникла ошибка", QMessageBox().Ok)

    # def sum_of_operations(self):
    #     try:
    #         self.sum_of_costs = 0.0
    #         for i in db.show_operations_of_patient(mw.selected_patient_id):
    #             self.sum_of_costs += i[4]
    #         self.sum_of_costs = round(self.sum_of_costs, 2)
    #         self.ui.label_4.setText(str(self.sum_of_costs))
    #     except: pass

    def open_add_position(self):
        aitcm.__init__()
        aitcm.show()

    def fill_table_items_of_complex_material(self):  # заполняет виджет таблицы пациентами из бд
        try:
            lst = db.show_binded_complex_item(self.new_material_id)
            if lst == []:
                self.ui.tableWidget.setRowCount(0)
            else:
                for co, it in enumerate(lst):
                    self.ui.tableWidget.setRowCount(co + 1)
                    self.ui.tableWidget.setItem(co, 0, QTableWidgetItem("{}".format(it[0])))
                    self.ui.tableWidget.setItem(co, 1, QTableWidgetItem("{}".format(it[1])))
                    self.ui.tableWidget.setItem(co, 2, QTableWidgetItem("{}".format(it[2])))
                    self.ui.tableWidget.setItem(co, 3, QTableWidgetItem("{}".format(it[3])))
                    self.ui.tableWidget.setItem(co, 4, QTableWidgetItem("{}".format(it[4])))
                    self.ui.tableWidget.setItem(co, 5, QTableWidgetItem("{}".format(it[5])))

        except:
            pass

    def delete_position(self):
        try:
            self.selected_id_position = self.ui.tableWidget.item(self.ui.tableWidget.currentRow(), 5).text()
            db.delete_item_in_new_complex_material_by_id(self.selected_id_position)
            self.fill_table_items_of_complex_material()
            aitcm.update_sum()

            # pac.fill_table_operations_of_patient()
            # pac.sum_of_operations()
            # db.update_patient_sum(pac.sum_of_costs, mw.selected_patient_id)
            # mw.fill_table_patients()
        except:
            QMessageBox().critical(self, 'Предупреждение', "Выберите операцию для удаления из таблицы",
                                   QMessageBox().Ok)


class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.tableWidget.setColumnHidden(6, True)
        self.ui.pushButton.clicked.connect(self.add_patient)
        self.ui.pushButton_3.clicked.connect(self.make_costs_for_patient)
        self.ui.pushButton_2.clicked.connect(self.delete_patient)
        self.fill_table_patients()

        def add_menu():
            layout = QHBoxLayout()
            bar = self.menuBar()
            menu = bar.addMenu("Действия")
            menu.addAction("Импортировать расходные материалы из .xlsx файла")
            menu.addAction("Добавить расходную позицию")
            menu.addAction("Добавить комплексную позицию")
            menu.triggered.connect(self.menu_bar_triggered)
            self.setLayout(layout)

        add_menu()

    def menu_bar_triggered(self, press):
        if press.text() == "Импортировать расходные материалы из .xlsx файла":
            fname = QFileDialog.getOpenFileName(self, 'Open file',
                                                '', "Xlsx files (*.xls *.xlsx)")
            try:
                ww.show()
                db.import_from_xls(fname[0])
                ww.hide()
            except:
                pass
        elif press.text() == "Добавить расходную позицию":
            ai.__init__()
            ai.show()

        elif press.text() == "Добавить комплексную позицию":
            acm.__init__()
            acm.show()

    def add_patient(self):
        np.__init__()
        np.show()

    def make_costs_for_patient(self):
        pac.__init__()
        try:
            self.selected_patient_id = self.ui.tableWidget.item(self.ui.tableWidget.currentRow(), 6).text()
            pac.ui.label.setText(mw.ui.tableWidget.item(mw.ui.tableWidget.currentRow(), 0).text())
            pac.ui.label_2.setText(mw.ui.tableWidget.item(mw.ui.tableWidget.currentRow(), 1).text())
            pac.fill_table_operations_of_patient()
            pac.sum_of_operations()
            pac.show()
        except:
            QMessageBox().critical(self, 'Предупреждение', "Выберите пациента из таблицы или создайте нового",
                                   QMessageBox().Ok)

    def delete_patient(self):
        try:
            self.selected_patient_id = self.ui.tableWidget.item(self.ui.tableWidget.currentRow(), 6).text()
            db.delete_patient(self.selected_patient_id)
            db.delete_operations_of_patient(self.selected_patient_id)
            self.fill_table_patients()
        except:
            QMessageBox().critical(self, 'Предупреждение', "Выберите пациента из таблицы или создайте нового",
                                   QMessageBox().Ok)

    def fill_table_patients(self):  # заполняет виджет таблицы пациентами из бд
        lst = db.show_patients()
        if lst == []:
            self.ui.tableWidget.setRowCount(0)
        else:
            for co, it in enumerate(lst):
                self.ui.tableWidget.setRowCount(co + 1)
                self.ui.tableWidget.setItem(co, 0, QTableWidgetItem("{}".format(it[2])))
                self.ui.tableWidget.setItem(co, 1, QTableWidgetItem("{}".format(it[1])))
                self.ui.tableWidget.setItem(co, 2, QTableWidgetItem("{}".format(it[6])))
                self.ui.tableWidget.setItem(co, 3, QTableWidgetItem("{}".format(it[5])))
                self.ui.tableWidget.setItem(co, 4, QTableWidgetItem("{}".format(it[3])))
                self.ui.tableWidget.setItem(co, 5, QTableWidgetItem("{}".format(it[4])))
                self.ui.tableWidget.setItem(co, 6, QTableWidgetItem("{}".format(it[0])))


class WaitingWindow(QDialog):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ui = Ui_WaitingWidget()
        self.ui.setupUi(self)


class AddItem(QDialog):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ui = Ui_AddItem()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.add_item)

    def add_item(self):
        inf_to_fill = {
            'name': self.ui.lineEdit.text(),
            'price': self.ui.doubleSpinBox.value(),
            'unit': self.ui.lineEdit_2.text(),
            'category': self.ui.comboBox.currentIndex()
        }
        db.add_items(inf_to_fill['name'], inf_to_fill['price'], inf_to_fill['unit'], inf_to_fill['category'])
        self.hide()


class NewPatient(QDialog):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ui = Ui_NewPatient()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.add_new_patient)

    def add_new_patient(self):
        patient_info = {'story': self.ui.lineEdit_2.text(),
                        'fio': self.ui.lineEdit.text(),
                        'date_start_illness': self.ui.dateEdit.text(),
                        'date_end_illness': self.ui.dateEdit_2.text(),
                        'cost': 0.0,
                        'status': self.ui.comboBox.currentText()}

        db.add_patient(patient_info['story'], patient_info['fio'], patient_info['date_start_illness'],
                       patient_info['date_end_illness'], patient_info['cost'], patient_info['status'])
        mw.fill_table_patients()
        self.hide()


class PatientAllCosts(QDialog):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ui = Ui_PatientAllCosts()
        self.ui.setupUi(self)
        self.ui.tableWidget.setColumnHidden(6, True)
        self.ui.pushButton.clicked.connect(self.open_add_position)
        self.ui.pushButton_2.clicked.connect(self.delete_position)
        self.ui.pushButton_3.clicked.connect(self.export_to_docx)
        try:
            self.fill_table_operations_of_patient(mw.selected_patient_id)
        except:
            pass
        self.sum_of_costs = 0.0

    def sum_of_operations(self):
        try:
            self.sum_of_costs = 0.0
            for i in db.show_operations_of_patient(mw.selected_patient_id):
                self.sum_of_costs += i[4]
            self.sum_of_costs = round(self.sum_of_costs, 2)
            self.ui.label_4.setText(str(self.sum_of_costs))
        except:
            pass

    def open_add_position(self):
        atp.__init__()
        atp.show()

    def fill_table_operations_of_patient(self):  # заполняет виджет таблицы пациентами из бд
        try:
            lst = db.show_operations_of_patient(mw.selected_patient_id)
            if lst == []:
                self.ui.tableWidget.setRowCount(0)
            else:
                names_cat=['Расходник', 'Препарат', 'Дез', 'Прочее', 'Перевязка']
                a=''


                for co, it in enumerate(lst):
                    self.ui.tableWidget.setRowCount(co + 1)
                    self.ui.tableWidget.setItem(co, 0, QTableWidgetItem("{}".format(it[6])))
                    self.ui.tableWidget.setItem(co, 1, QTableWidgetItem("{}".format(it[8])))
                    self.ui.tableWidget.setItem(co, 2, QTableWidgetItem("{}".format(it[3])))
                    self.ui.tableWidget.setItem(co, 3, QTableWidgetItem("{}".format(it[4])))
                    self.ui.tableWidget.setItem(co, 4, QTableWidgetItem("{}".format(it[7])))
                    if it[9]==0:
                        a=names_cat[0]
                    elif it[9]==1:
                        a=names_cat[1]
                    elif it[9]==2:
                        a=names_cat[2]
                    elif it[9]==3:
                        a=names_cat[3]
                    elif it[9]==4:
                        a=names_cat[4]
                    self.ui.tableWidget.setItem(co, 5, QTableWidgetItem("{}".format(a)))
                    self.ui.tableWidget.setItem(co, 6, QTableWidgetItem("{}".format(it[0])))
        except:
            pass

    def delete_position(self):
        try:
            self.selected_id_position = self.ui.tableWidget.item(self.ui.tableWidget.currentRow(), 6).text()
            db.delete_operations_by_id(self.selected_id_position)
            pac.fill_table_operations_of_patient()
            pac.sum_of_operations()
            db.update_patient_sum(pac.sum_of_costs, mw.selected_patient_id)
            mw.fill_table_patients()
        except:
            QMessageBox().critical(self, 'Предупреждение', "Выберите операцию для удаления из таблицы",
                                   QMessageBox().Ok)

    def export_to_odt(self):
        inf_to_fill = {
            'patient_fio': mw.ui.tableWidget.item(mw.ui.tableWidget.currentRow(), 0).text(),
            'story': mw.ui.tableWidget.item(mw.ui.tableWidget.currentRow(), 1).text(),
            'from': mw.ui.tableWidget.item(mw.ui.tableWidget.currentRow(), 4).text(),
            'to': mw.ui.tableWidget.item(mw.ui.tableWidget.currentRow(), 5).text(),
            'status': mw.ui.tableWidget.item(mw.ui.tableWidget.currentRow(), 2).text(),
            'total_sum': mw.ui.tableWidget.item(mw.ui.tableWidget.currentRow(), 3).text(),
            'positions': db.show_operations_of_patient(
                mw.ui.tableWidget.item(mw.ui.tableWidget.currentRow(), 6).text(), )
        }

        fname = QFileDialog.getSaveFileName(self, 'Save file',
                                            '', "Open Office Document text files (*.odt)")

        odt.form_odt(file_name=fname[0], **inf_to_fill)
        # ODTExport.form_odt(file_name=fname[0], **inf_to_fill)
        # pprint(inf_to_fill)

    def export_to_docx(self):
        context = db.show_all_information_by_id_patient_with_devide_by_category(mw.selected_patient_id)
        fname = QFileDialog.getSaveFileName(self, 'Save file',
                                            '', "MS Office Document text files (*.docx)")
        # fname += '.docx' if '.docx' not in fname else True
        tpl = DocxTemplate('Appendix_template.docx')
        tpl.render(context)
        tpl.save(fname[0])



class AddPositionToPatient(QDialog):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id_of_position = None
        self.ui = Ui_AddPositionToPatient()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.add_position_quantity_sum)
        self.completer_items()
        self.ui.comboBox.currentIndexChanged.connect(self.index_category_changed)

    def index_category_changed(self):
        db.update_category_of_materials(self.id_of_position, self.ui.comboBox.currentIndex())

    def completer_items(self):
        self.strList_list = db.show_materials()
        self.strList = [i[1] for i in self.strList_list]

        self.completer = QCompleter(self.strList, self.ui.lineEdit)
        self.completer.setCaseSensitivity(False)
        self.completer.setFilterMode(QtCore.Qt.MatchContains)
        self.completer.activated.connect(self.onActivated_competer)
        self.ui.lineEdit.setCompleter(self.completer)

    def onActivated_competer(self):
        self.id_of_position = list(filter(lambda x: x[1] == self.ui.lineEdit.text(), self.strList_list))[0][0]
        # self.id_of_position = [n for n, x in enumerate(self.strList_list) if self.ui.lineEdit.text() in x][0] #
        # неправильно!!!
        self.ui.textEdit.setText(self.ui.lineEdit.text() + ', ' + db.show_material_by_id(self.id_of_position)[3])
        QTimer.singleShot(0, self.ui.lineEdit.clear)
        self.ui.comboBox.setCurrentIndex(db.show_material_by_id(self.id_of_position)[4])
        self.ui.comboBox.setEnabled(True)

    def add_position_quantity_sum(self):
        info_to_add = {'sum_of': round(self.ui.doubleSpinBox_2.value() / self.ui.doubleSpinBox.value() * db.
                                       show_material_by_id(self.id_of_position)[2], 2),
                       'quantity': round(self.ui.doubleSpinBox_2.value() / self.ui.doubleSpinBox.value(), 2),
                       'id_materials': self.id_of_position,
                       'id_patients': mw.selected_patient_id}
        db.add_position_cost(info_to_add['id_patients'], info_to_add['id_materials'], info_to_add['quantity'],
                             info_to_add['sum_of'])
        pac.fill_table_operations_of_patient()
        pac.sum_of_operations()
        db.update_patient_sum(pac.sum_of_costs, mw.selected_patient_id)
        mw.fill_table_patients()
        self.hide()
        self.__init__()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # extra = {
    #
    #     # Density Scale
    #     'density_scale': '-1',
    # }
    # apply_stylesheet(app, theme='light_red.xml', invert_secondary=True, extra=extra)
    ww = WaitingWindow()
    db = DataBase()
    mw = mywindow()
    np = NewPatient()
    pac = PatientAllCosts()
    atp = AddPositionToPatient()
    ai = AddItem()
    odt = ODTExport()
    acm = AddComplexMaterial()
    aitcm = AddItemToComplexMaterial()
    mw.show()

    sys.exit(app.exec_())

import sys
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QAction, QFileDialog, QDialog, QTableWidgetItem, QMessageBox, \
    QCompleter

from PyQt5 import QtWidgets, QtCore

from DataBase import DataBase
from UI_files.AddPositionToPatient import Ui_AddPositionToPatient
from UI_files.MainWindow import Ui_MainWindow
from UI_files.NewPatient import Ui_NewPatient
from UI_files.PatientAll_costs import Ui_PatientAllCosts
from UI_files.WaitingWindow import Ui_WaitingWidget


class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # self.selected_patient_id = None

        self.ui.pushButton.clicked.connect(self.add_patient)
        self.ui.pushButton_3.clicked.connect(self.make_costs_for_patient)
        self.fill_table_patients()

        def add_menu():
            layout = QHBoxLayout()
            bar = self.menuBar()
            menu = bar.addMenu("Действия")
            menu.addAction("Импортировать расходные материалы из .xlsx файла")
            menu.triggered[QAction].connect(self.menu_bar_triggered)
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

    def add_patient(self):
        np.__init__()
        np.show()

    def make_costs_for_patient(self):
        try:
            self.selected_patient_id = self.ui.tableWidget.item(self.ui.tableWidget.currentRow(), 6).text()
            pac.__init__()
            pac.ui.label.setText(mw.ui.tableWidget.item(mw.ui.tableWidget.currentRow(), 0).text())
            pac.ui.label_2.setText(mw.ui.tableWidget.item(mw.ui.tableWidget.currentRow(), 1).text())
            pac.show()
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
        print(patient_info)
        db.add_patient(patient_info['story'], patient_info['fio'], patient_info['date_start_illness'],
                       patient_info['date_end_illness'], patient_info['cost'], patient_info['status'])
        mw.fill_table_patients()
        self.hide()

class PatientAllCosts(QDialog):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ui = Ui_PatientAllCosts()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.open_add_position)

    def open_add_position(self):
        atp.__init__()
        atp.show()

class AddPositionToPatient(QDialog):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ui = Ui_AddPositionToPatient()
        self.ui.setupUi(self)

    # def completer_items(self):
    #     self.strList = [i[1] for i in db.show_data()]  # Создаём список слов
    #     # Создаём QCompleter, в который устанавливаем список, а также указатель на родителя
    #     completer = QCompleter(self.strList, self.ui.lineEdit)
    #     completer.setCaseSensitivity(False)
    #     completer.setFilterMode(QtCore.Qt.MatchContains)
    #     completer.activated.connect(self.onActivated_competer)
    #     self.ui.lineEdit.setCompleter(completer)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ww = WaitingWindow()
    db = DataBase()
    mw = mywindow()
    np = NewPatient()
    pac = PatientAllCosts()
    atp = AddPositionToPatient()
    mw.show()

    sys.exit(app.exec_())
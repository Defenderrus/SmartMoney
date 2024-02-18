import sys
import pathlib
import pandas as pd

import data
from graph_1 import Charts
from graph_2 import Curves

from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QDesktopWidget, QLabel, QHeaderView, QTableWidgetItem


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi("design//main_win.ui", self)

        self.lines, self.my_task = 30, 0
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.horizontalHeader().setVisible(True)
        self.tableWidget.verticalHeader().setVisible(True)
        self.tableWidget.sortByColumn(0, Qt.AscendingOrder)
        self.tabWidget.setMaximumSize(QDesktopWidget().geometry().width()*3//5,
                                      QDesktopWidget().geometry().height())
        pixmap = QPixmap("icons//SmartMoney.png")
        self.label_4.setPixmap(pixmap)

        self.action_1.triggered.connect(self.clear_all)
        self.action_2.triggered.connect(self.add_task)
        self.action_3.triggered.connect(self.save_act)
        self.action_4.triggered.connect(self.warning)
        self.action_5.triggered.connect(self.exit_act)
        self.pushButton.clicked.connect(self.update_data)
        self.pushButton_1.clicked.connect(self.add_row)
        self.pushButton_2.clicked.connect(self.remove_row)
        self.pushButton_3.clicked.connect(self.clear_all)

        self.graphic1 = Charts()
        self.graphic2 = Curves()
        self.label_chart = QLabel()
        self.label_curve = QLabel()
        self.label_chart.setAlignment(Qt.AlignCenter)
        self.label_curve.setAlignment(Qt.AlignCenter)

    def add_task(self):
        self.dialog = uic.loadUi("design//task_dial.ui")
        self.dialog.buttonBox.accepted.connect(self.new_task)
        self.dialog.buttonBox.rejected.connect(self.rejecting)
        self.dialog.show()

    def save_act(self):
        directory = pathlib.Path(pathlib.Path.home(), "documents", "untitled.xlsx")
        self.dialog = QFileDialog.getSaveFileName(self, "Сохранение", str(directory), "Таблица Excel (*.xlsx *.xls)")[0]
        if self.dialog:
            df = pd.DataFrame(data.save([[self.tableWidget.item(i, j).text() for j in range(5)]
                                         for i in range(self.tableWidget.rowCount())
                                         if self.tableWidget.item(i, 0) is not None]))
            with pd.ExcelWriter(self.dialog, date_format="dd.mm.YYYY", engine='xlsxwriter') as writer:
                df.to_excel(writer, sheet_name='Таблица', index=False)

    def warning(self):
        self.dialog = uic.loadUi("design//error_mes.ui")
        self.dialog.setFixedSize(400, 160)
        self.dialog.setWindowTitle("Внимание!")
        self.dialog.label.setText("В вашем импортируемом файле должны присутствовать:\n"
                                  "- Заголовки столбцов (столбец 'Комментарии' необязателен);\n"
                                  "- Заполненные строчки с данными (соблюдая формат данных);\n"
                                  "Никаких лишних данных быть не должно!")
        self.action_4.disconnect()
        self.action_4.triggered.connect(self.load_act)
        self.dialog.buttonBox.accepted.connect(self.load_act)
        self.dialog.show()

    def load_act(self):
        directory = pathlib.Path(pathlib.Path.home(), "documents")
        self.dialog = QFileDialog.getOpenFileName(self, "Загрузка", str(directory), "Таблица Excel (*.xlsx *.xls)")[0]
        if self.dialog:
            array = data.load(pd.read_excel(self.dialog, engine="openpyxl"))
            if type(array) == str:
                self.dialog = uic.loadUi("design//error_mes.ui")
                self.dialog.setFixedSize(400, 160)
                self.dialog.label.setText(array)
                self.dialog.buttonBox.accepted.connect(self.rejecting)
                self.dialog.show()
            else:
                self.tableWidget.setSortingEnabled(False)
                self.lines = (len(array[0])//30+1)*30
                self.tableWidget.setRowCount(0)
                self.tableWidget.setRowCount(self.lines)
                for line in range(len(array[0])):
                    date, value = QTableWidgetItem(), QTableWidgetItem()
                    date.setData(Qt.EditRole, QDate(array[0][line]))
                    value.setData(Qt.EditRole, array[4][line])
                    self.tableWidget.setItem(line, 0, date)
                    self.tableWidget.setItem(line, 1, QTableWidgetItem(array[1][line]))
                    self.tableWidget.setItem(line, 2, QTableWidgetItem(array[2][line]))
                    self.tableWidget.setItem(line, 3, QTableWidgetItem(array[3][line]))
                    self.tableWidget.setItem(line, 4, value)
                self.tableWidget.setSortingEnabled(True)

    def exit_act(self):
        self.dialog = uic.loadUi("design//main_dial.ui")
        self.dialog.setWindowTitle("Выйти")
        self.dialog.show()
        self.dialog.buttonBox.accepted.connect(self.leaving)
        self.dialog.buttonBox.rejected.connect(self.rejecting)

    def update_data(self):
        array = [[self.tableWidget.item(i, j).text() for j in range(5)]
                 for i in range(self.tableWidget.rowCount())
                 if self.tableWidget.item(i, 0) is not None]
        if array:
            for i in reversed(range(self.gridLayout_4.count())):
                self.gridLayout_4.takeAt(i).widget().setParent(None)
            for i in reversed(range(self.gridLayout_5.count())):
                self.gridLayout_5.takeAt(i).widget().setParent(None)
            incomes_categories, expenses_categories, incomes, expenses = data.get(array)
            text1, text2 = data.stats(incomes_categories, expenses_categories, incomes, expenses)
            if self.my_task:
                text2 += (f"\nВы близки к своей цели на {'{:.2f}'.format((sum(incomes.values())-sum(expenses.values()))*100/self.my_task)}% "
                          f"({'{:,.2f}'.format(sum(incomes.values())-sum(expenses.values()))}/{'{:,.2f}'.format(self.my_task)})")
            self.graphic1.plot(incomes_categories, expenses_categories)
            self.graphic2.plot(incomes, expenses)
            self.label_chart.setText(text1)
            self.label_curve.setText(text2)
            self.gridLayout_4.addWidget(self.graphic1.toolbar)
            self.gridLayout_4.addWidget(self.graphic1.canvas)
            self.gridLayout_4.addWidget(self.label_chart)
            self.gridLayout_5.addWidget(self.graphic2.toolbar)
            self.gridLayout_5.addWidget(self.graphic2.canvas)
            self.gridLayout_5.addWidget(self.label_curve)
        else:
            self.dialog = uic.loadUi("design//error_mes.ui")
            self.dialog.label.setText("Недостаточно данных!")
            self.dialog.buttonBox.accepted.connect(self.rejecting)
            self.dialog.show()

    def add_row(self):
        if self.tableWidget.selectedIndexes():
            self.dialog = uic.loadUi("design//add_dial.ui")
            self.select_2 = self.dialog.comboBox_1.currentText()
            self.select_3 = self.dialog.comboBox_2.currentText()
            self.dialog.dateEdit.setDate(QDate.currentDate())
            self.dialog.dateEdit.setMaximumDate(QDate.currentDate())
            self.dialog.comboBox_1.currentTextChanged.connect(self.combo_1)
            self.dialog.comboBox_2.currentTextChanged.connect(self.combo_2)
            self.dialog.buttonBox.accepted.connect(self.adding)
            self.dialog.buttonBox.rejected.connect(self.rejecting)
        else:
            self.dialog = uic.loadUi("design//error_mes.ui")
            self.dialog.label.setText("Сначала выберите строчку, с которой хотите выполнить действие!")
            self.dialog.buttonBox.accepted.connect(self.rejecting)
        self.dialog.show()

    def remove_row(self):
        if self.tableWidget.selectedIndexes():
            self.removing()
        else:
            self.dialog = uic.loadUi("design//error_mes.ui")
            self.dialog.label.setText("Сначала выберите строчку, с которой хотите выполнить действие!")
            self.dialog.buttonBox.accepted.connect(self.rejecting)
            self.dialog.show()

    def clear_all(self):
        self.dialog = uic.loadUi("design//main_dial.ui")
        self.dialog.setWindowTitle("Начать заново")
        self.dialog.show()
        self.dialog.buttonBox.accepted.connect(self.clearing)
        self.dialog.buttonBox.rejected.connect(self.rejecting)

    def new_task(self):
        self.my_task = self.dialog.doubleSpinBox.value()
        self.dialog.close()

    def leaving(self):
        self.dialog.close()
        self.close()

    def adding(self):
        if self.select_2 and self.select_3:
            self.tableWidget.setSortingEnabled(False)
            date, value = QTableWidgetItem(), QTableWidgetItem()
            date.setData(Qt.EditRole, self.dialog.dateEdit.date())
            value.setData(Qt.EditRole, self.dialog.doubleSpinBox.value())
            self.cur_row = self.tableWidget.currentRow()
            self.tableWidget.setItem(self.cur_row, 0, date)
            self.tableWidget.setItem(self.cur_row, 1, QTableWidgetItem(self.select_2))
            self.tableWidget.setItem(self.cur_row, 2, QTableWidgetItem(self.select_3))
            self.tableWidget.setItem(self.cur_row, 3, QTableWidgetItem(self.dialog.textEdit.toPlainText()))
            self.tableWidget.setItem(self.cur_row, 4, value)
            self.tableWidget.setSortingEnabled(True)
            self.cur_row = self.tableWidget.currentRow()
            if self.tableWidget.item(self.lines-1, 0) is not None:
                self.lines += 30
                self.tableWidget.setRowCount(self.lines)
            self.rejecting()

    def combo_1(self):
        self.select_2 = self.dialog.comboBox_1.currentText()
        self.dialog.comboBox_2.clear()
        if self.select_2 == "Доход":
            self.dialog.comboBox_2.addItems(["", "Работа/Подработка", "Пенсия", "Проценты по вкладам",
                                             "Дивиденды", "Рента", "Соц.выплаты/Пособия", "Вознаграждение",
                                             "Подарки", "Другое"])
        elif self.select_2 == "Расходы":
            self.dialog.comboBox_2.addItems(["", "Налоги", "Кредит", "Аренда/Съём", "ЖКУ", "Продукты питания",
                                             "Одежда и обувь", "Здравоохранение", "Образование", "Транспорт",
                                             "Бытовая техника", "Электроника", "Машина", "Недвижимость",
                                             "Предметы роскоши", "Хобби и отдых", "Внезапные расходы",
                                             "Другое"])
        else:
            self.dialog.comboBox_2.addItem("")
        self.select_3 = ""

    def combo_2(self):
        self.select_3 = self.dialog.comboBox_2.currentText()

    def removing(self):
        self.cur_row = self.tableWidget.currentRow()
        self.tableWidget.removeRow(self.cur_row)
        if self.lines > 30:
            if self.tableWidget.item(self.lines-31, 0) is None:
                self.lines -= 30
        self.tableWidget.setRowCount(self.lines)

    def clearing(self):
        self.tableWidget.setRowCount(0)
        self.tableWidget.setRowCount(30)
        self.lines = 30
        self.dialog.close()

    def rejecting(self):
        self.dialog.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

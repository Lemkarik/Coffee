import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QWidget
import sys


class Form(QWidget):
    def __init__(self, anc):
        super().__init__()
        uic.loadUi('UI/addEditCoffeeForm.ui', self)
        self.pushButton.clicked.connect(self.close)
        self.pushButton_2.clicked.connect(self.u)
        self.anc = anc

    def u(self):
        a = [self.lineEdit.text(), self.lineEdit_2.text(), self.lineEdit_3.text(),
             self.lineEdit_4.text(), self.lineEdit_5.text(), self.lineEdit_6.text(), self.lineEdit_7.text()]
        con = sqlite3.connect('data/coffee.sqlite')
        cur = con.cursor()
        if cur.execute("""SELECT * FROM coffee WHERE ID = ?""", (a[0],)).fetchone():
            for i, v in enumerate(['ID', 'Название', 'Степень_обжарки', 'Молотый_в_зернах', 'Описание_вкуса', 'Цена',
                                   'Объём_упаковки']):
                if i:
                    if a[i].isdigit():
                        cur.execute(f"""UPDATE coffee SET {v} = {int(a[i])} WHERE ID = {a[0]}""")
                    else:
                        cur.execute(f"""UPDATE coffee SET {v} = '{a[i]}' WHERE ID = {a[0]}""")
                    con.commit()
        else:
            p1 = []
            p2 = []
            for i, v in enumerate(['ID', 'Название', 'Степень_обжарки', 'Молотый_в_зернах', 'Описание_вкуса', 'Цена',
                                   'Объём_упаковки']):
                p1.append(v)
                if a[i].isdigit():
                    p2.append(int(a[i]))
                else:
                    p2.append(a[i])
            cur.execute(f"""INSERT INTO coffee{tuple(p1)} VALUES{tuple(p2)}""")
            con.commit()
        self.close()
        self.anc.update()


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('UI/main.ui', self)
        self.update()
        self.pushButton.clicked.connect(self.t)

    def t(self):
        self.form = Form(self)
        self.form.show()

    def update(self):
        con = sqlite3.connect("data/coffee.sqlite")
        cur = con.cursor()
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(0)
        for i, v in enumerate(['ID', 'Название', 'Степень обжарки', 'Молотый/в зернах', 'Описание вкуса', 'Цена',
                               'Объём упаковки']):
            self.tableWidget.setHorizontalHeaderItem(i, QTableWidgetItem(v))
        for i, row in enumerate(cur.execute("""SELECT * FROM coffee""")):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        con.close()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())

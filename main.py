import sys
import sqlite3

from PyQt5 import uic
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QTableWidget,
    QTableWidgetItem
)

class Coffee(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.initCoffeeData()
        self.initUI()

    def initCoffeeData(self):
        self.curs = sqlite3.connect('coffee.sqlite').cursor()
        self.coffeeData = self.curs.execute('select * from coffee').fetchall()

    def initUI(self):
        self.fillCoffeeTable()
        self.coffeeTable.resizeColumnsToContents()

    def fillCoffeeTable(self):
        table: QTableWidget = self.coffeeTable
        for i in range(len(self.coffeeData)):
            table.insertRow(i)
            for j in range(len(self.coffeeData[i])):
                table.setItem(i, j, QTableWidgetItem(str(self.coffeeData[i][j])))
                print(i , j)
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    arif = Coffee()
    arif.show()
    sys.exit(app.exec())
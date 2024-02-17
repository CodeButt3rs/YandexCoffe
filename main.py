import sys
import sqlite3

from pydantic import BaseModel
from PyQt5 import uic
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QDialog,
    QLabel,
    QVBoxLayout
)

class CoffeeModel(BaseModel):
    name: str
    sort: str
    grilled: int
    grains: bool
    description: str
    price: int
    volume: int

class Coffee(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.editCoffeeWindow: QWidget = uic.loadUi('editCoffee.ui')
        self.addCoffeeWindow: QWidget = uic.loadUi('addCoffee.ui')
        self.initCoffeeData()
        self.initAddCoffeeWindow()
        self.initUI()

    def initCoffeeData(self):
        self.dbConnect = sqlite3.connect('coffee.sqlite')
        self.curs = self.dbConnect.cursor()
        self.coffeeData = self.curs.execute('select * from coffee').fetchall()

    def initAddCoffeeWindow(self):
        window = self.addCoffeeWindow
        btn: QPushButton = window.addCoffee_buttonAdd
        btn.clicked.connect(self.addCoffeeWindowButtonClick)
        
    def addCoffeeWindowButtonClick(self):
        window = self.addCoffeeWindow
        try:
            name = window.addCoffee_nameField.toPlainText()
            sort = window.addCoffee_sortField.toPlainText()
            grill = int(window.addCoffee_grilledField.toPlainText())
            description = window.addCoffee_descriptionField.toPlainText()
            price = int(window.addCoffee_priceField.toPlainText())
            volume = int(window.addCoffee_volumeField.toPlainText())
        except Exception as e:
            self.showAddCoffeeWindowError()
            return
        coff = CoffeeModel(name=name, sort=sort, grilled=grill, grains=window.addCoffee_inGraings.isChecked(), description=description, price=price, volume=volume)
        self.addCoffeeToDB(coff)
        window.close()
        self.addLastRow(data=[1] + [v for v in coff.model_dump().values()])

    def showAddCoffeeWindowError(self):
        errorWin = QDialog()
        layt = QVBoxLayout()
        layt.addWidget(QLabel(text="Неправильно заполнены данные!"))
        errorWin.setLayout(layt)
        errorWin.setWindowTitle("Ошибка")
        errorWin.exec()

    def showAddCoffeeWindowSuccess(self):
        errorWin = QDialog()
        layt = QVBoxLayout()
        layt.addWidget(QLabel(text="Данные успешно добавлены!"))
        errorWin.setLayout(layt)
        errorWin.setWindowTitle("Успешно")
        errorWin.exec()

    def addCoffeeToDB(self, coffee: CoffeeModel):
        lastid = int(self.curs.execute('SELECT * FROM coffee ORDER BY id DESC LIMIT 1').fetchone()[0])
        values = f'"{coffee.name}", "{coffee.sort}",{coffee.grilled},{coffee.grains},"{coffee.description}",{coffee.price},{coffee.volume}'
        self.curs.execute(f'insert into coffee(id, name, sort, grilled, grains, description, price, volume)values({lastid + 1}, {values})')
        self.dbConnect.commit()

    def initUI(self):
        self.fillCoffeeTable()
        self.coffeeTable.resizeColumnsToContents()
        btn: QPushButton = self.addCoffeeButton
        btn.clicked.connect(lambda x: self.addCoffeeWindow.show())

    def addLastRow(self, data):
        table: QTableWidget = self.coffeeTable
        row = table.rowCount()
        table.insertRow(row)
        for j in range(len(data)):
            table.setItem(row, j, QTableWidgetItem(str(data[j])))

    def fillCoffeeTable(self):
        table: QTableWidget = self.coffeeTable
        for i in range(len(self.coffeeData)):
            table.insertRow(i)
            for j in range(len(self.coffeeData[i])):
                table.setItem(i, j, QTableWidgetItem(str(self.coffeeData[i][j])))

            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    arif = Coffee()
    arif.show()
    sys.exit(app.exec())
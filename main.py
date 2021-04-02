from PyQt5 import uic, QtWidgets
import sqlite3


database = sqlite3.connect('products.db')
cursor = database.cursor()

cursor.execute('CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, codigo INTEGER, nome TEXT, estoque INTEGER, categoria TEXT)')

def erase():
    line = form2.tableWidget.currentRow()
    form2.tableWidget.removeRow(line)
    
    cursor.execute('SELECT id FROM products')
    datas = cursor.fetchall()
    id_value = datas[line][0]
    cursor.execute("DELETE FROM products WHERE id="+str(id_value))
    database.commit()
    


def code_analisys(code_):
    variable = True
    cursor.execute('SELECT codigo FROM products')
    for k in cursor.fetchall():
        if code_ in k:
            variable = True
            break
        else:
            variable = False
            
    return variable

def main():
    code = int(form.lineEdit.text())
    name = form.lineEdit_2.text()
    stock = int(form.lineEdit_3.text())
    verify = code_analisys(code)
    print(verify)
    while verify:
        code += 1
        verify = code_analisys(code)
        
    print(f'{code}\n{name}\n{stock}')
    
    if form.radioButton.isChecked():
        category = 'Eletronico'
    elif form.radioButton_2.isChecked():
        category = 'Alimento'
    elif form.radioButton_3.isChecked():
        category = 'Higiene'
    
    cursor.execute('INSERT INTO products(codigo, nome, estoque, categoria) VALUES (?, ?, ?, ?)', (code, name, stock, category))
    database.commit()
    form.lineEdit.setText('')
    form.lineEdit_2.setText('')
    form.lineEdit_3.setText('')
    
def second_view():
    form2.show()
    cursor.execute('SELECT * FROM products')
    data = cursor.fetchall()
    form2.tableWidget.setRowCount(len(data))
    form2.tableWidget.setColumnCount(5)

    
    for k in range(0, len(data)):
        for v in range(0, 5):
            form2.tableWidget.setItem(k, v, QtWidgets.QTableWidgetItem(str(data[k][v])))
    

app = QtWidgets.QApplication([])
form = uic.loadUi('design.ui')
form2 = uic.loadUi('design2.ui')
form.pushButton.clicked.connect(main)
form.pushButton_2.clicked.connect(second_view)
form2.pushButton.clicked.connect(erase)

form.show()
app.exec()


    

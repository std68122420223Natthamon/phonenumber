import sys
from PyQt6 import uic
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from db_connect import db, cursor

class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()
    uic.loadUi('natthamon.ui', self)
    self.id = 0

    self.numberdata.setColumnWidth(0, 50)
    self.numberdata.setColumnWidth(1, 150)
    self.numberdata.setColumnWidth(2, 150)
    self.numberdata.setColumnWidth(3, 100)
    self.numberdata.setColumnWidth(4, 180)

    self.show_all_phones()
    self.btn_add.clicked.connect(self.insert_phone)
    self.pushButton.clicked.connect(self.search_phone)
    self.btn_clear.clicked.connect(self.clear)
    self.btn_update.clicked.connect(self.update_phone)
    self.btn_delete.clicked.connect(self.delete_phone)
    self.numberdata.cellClicked.connect(self.selected_row)

  def say_hi(self):
    QMessageBox.information(self, 'Information', 'Hello World!')

  def update_phone(self):
    phonenumber = int(self.txt_phonenumber.text())
    sql = 'update phone set phonenumber = ? where id = ?'
    values = (phonenumber, self.id)

    row = cursor.execute(sql, values)
    db.commit()

    if row.rowcount>0:
      QMessageBox.information(self, 
                              'Information', 
                              'Update phone successful!')
      self.show_all_phones()
    else:
      QMessageBox.warning(self, 
                              'Warning', 
                              'Unable to update phone!')
    self.clear()

  def delete_phone(self):
    sql = 'delete from phone where id = ?'
    values = (self.id, )

    row = cursor.execute(sql, values)
    db.commit()

    if row.rowcount>0:
      QMessageBox.information(self, 
                              'Information', 
                              'Delete phone successful!')
      self.show_all_phones()
    else:
      QMessageBox.warning(self, 
                              'Warning', 
                              'Unable to delete phone!')
    self.clear()

  def selected_row(self):
    row = self.numberdata.currentRow()
    self.id = self.numberdata.item(row, 0).text()
    self.txt_email.setText(self.numberdata.item(row, 1).text())
    self.txt_name.setText(self.numberdata.item(row, 2).text())
    self.txt_surname.setText(self.numberdata.item(row, 3).text())
    self.txt_phonenumber.setText(self.numberdata.item(row, 4).text())

    self.btn_update.setEnabled(True)
    self.btn_delete.setEnabled(True)
    self.btn_add.setEnabled(False)

    self.txt_email.setEnabled(False)
    self.txt_name.setEnabled(False)
    self.txt_surname.setEnabled(False)

  def search_phone(self):
    email = self.lineEdit.text()
    # print(brand)
    sql = 'select * from phone where email like ?'
    values = (f'%{email}%', )

    phones = cursor.execute(sql, values).fetchall()
    self.show_phones(phones)

    self.pushButton.setText('')

  def show_all_phones(self):
    sql = 'select * from phone'
    phones = cursor.execute(sql).fetchall()

    self.show_phones(phones)

  def show_phones(self, phones):
      n = len(phones)
      self.numberdata.setRowCount(n)
      row = 0
      for phone in phones:  #phone[0] => (1, 'Toyota', 'Yaris Cross', 2025, 867778)
        self.numberdata.setItem(row, 0, QTableWidgetItem(str(phone[0])))
        self.numberdata.setItem(row, 1, QTableWidgetItem(phone[1]))
        self.numberdata.setItem(row, 2, QTableWidgetItem(phone[2]))
        self.numberdata.setItem(row, 3, QTableWidgetItem(str(phone[3])))
        self.numberdata.setItem(row, 4, QTableWidgetItem(str(phone[4])))

        row += 1

  def insert_phone(self):
    email = self.txt_email.text()
    name = self.txt_name.text()
    surname = self.txt_surname.text()
    phonenumber = self.txt_phonenumber.text()
    

    sql = 'insert into phone( email, name, surname, phonenumber) values( ?, ?, ?, ?)'
    values = ( email, name, surname, phonenumber)
    
    rs = cursor.execute(sql, values)
    db.commit()
    if rs.rowcount>0:
      QMessageBox.information(self, 
                              'Information', 
                              'Insert phone successful!')
      self.show_all_phones()
    else:
      QMessageBox.warning(self, 
                              'Warning', 
                              'Unable to insert phone!')

    self.clear()

  def clear(self):
    self.txt_email.setText('')
    self.txt_name.setText('')
    self.txt_surname.setText('')
    self.txt_phonenumber.setText('')

    self.txt_email.setEnabled(True)
    self.txt_name.setEnabled(True)
    self.txt_surname.setEnabled(True)

    self.numberdata.clearSelection()

    self.btn_add.setEnabled(True)
    self.btn_update.setEnabled(False)
    self.btn_delete.setEnabled(False)

    self.show_all_phones()


  
if __name__ == '__main__':
  app = QApplication(sys.argv)
  window = MainWindow()
  window.show()
  app.exec()
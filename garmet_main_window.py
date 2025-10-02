import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, \
    QLabel, QLineEdit, QPushButton, QMessageBox
from garmet_helper import DB, DB_CONFIG

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("옷 재고 관리")
        self.db = DB(**DB_CONFIG)

        central = QWidget()
        self.setCentralWidget(central)
        vbox = QVBoxLayout(central)

        # 입력폼
        form_box = QHBoxLayout()
        self.input_Numbers = QLineEdit()
        self.input_sort = QLineEdit()
        self.input_size = QLineEdit()
        self.input_price = QLineEdit()
        self.input_stock = QLineEdit()
        self.btn_add = QPushButton("추가")
        self.btn_add.clicked.connect(self.add_garmet)

       
        form_box.addWidget(QLabel("번호"))
        form_box.addWidget(self.input_Numbers)
        form_box.addWidget(QLabel("종류"))
        form_box.addWidget(self.input_sort)
        form_box.addWidget(QLabel("사이즈"))
        form_box.addWidget(self.input_size)
        form_box.addWidget(QLabel("가격"))
        form_box.addWidget(self.input_price)
        form_box.addWidget(QLabel("재고"))
        form_box.addWidget(self.input_stock)
        form_box.addWidget(self.btn_add)

        # 테이블
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Numbers", "Sort", "Size", "Price", "Stock"])
        self.table.setEditTriggers(self.table.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)

        vbox.addLayout(form_box)
        vbox.addWidget(self.table)

        self.load_stock()

    def load_stock(self):
        rows = self.db.fetch_stock()
        self.table.setRowCount(len(rows))
        for r, (Numbers, Sort, Size, Price, Stock) in enumerate(rows):
            self.table.setItem(r, 0, QTableWidgetItem(str(Numbers)))
            self.table.setItem(r, 1, QTableWidgetItem(Sort))
            self.table.setItem(r, 2, QTableWidgetItem(Size))
            self.table.setItem(r, 3, QTableWidgetItem(str(Price)))
            self.table.setItem(r, 4, QTableWidgetItem(str(Stock)))
        self.table.resizeColumnsToContents()

    def add_garmet(self) :
        Numbers = self.input_Numbers.text().strip()
        Sort = self.input_sort.text().strip()
        Size = self.input_size.text().strip()
        Price = self.input_price.text().strip()
        Stock = self.input_stock.text().strip()

        if not (Numbers or Sort or Size or Price or Stock):
            QMessageBox.warning(self, "오류", "번호, 종류, 사이즈, 가격, 재고를 모두 입력하세요.")
            return
        ok = self.db.insert_stock(Numbers, Sort, Size, Price, Stock)
        if ok:
            QMessageBox.information(self, "완료", "추가되었습니다.")
            self.input_Numbers.clear()
            self.input_sort.clear()
            self.input_size.clear()
            self.input_price.clear()
            self.input_stock.clear()
            
            self.load_stock()
        else:
            QMessageBox.critical(self, "실패", "추가 중 오류가 발생했습니다.")

import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton,
    QLineEdit, QMessageBox, QListWidget, QInputDialog, QComboBox
)
from PyQt5.QtCore import Qt
import shelve

CATEGORIS = ["전자제품", "생활용품", "식품", "의류", "기타"]

products = []

# 기존 데이터 로드
with shelve.open('products_db') as db:
    products = db.get('products', [])


def save_products():
    with shelve.open('products_db') as db:
        db['products'] = products


class Login(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("로그인")
        self.setGeometry(500, 100, 800, 600)

        self.title_label = QLabel("로그인")
        self.title_label.setAlignment(Qt.AlignCenter)

        self.id_label = QLabel("아이디")
        self.id_input = QLineEdit(self)
        self.id_input.setPlaceholderText("아이디를 입력하세요")

        self.pw_label = QLabel("비밀번호")
        self.pw_input = QLineEdit(self)
        self.pw_input.setPlaceholderText("비밀번호를 입력하세요")
        self.pw_input.setEchoMode(QLineEdit.Password)

        self.id_input.returnPressed.connect(self.pw_input.setFocus)
        self.pw_input.returnPressed.connect(self.login)

        self.login_btn = QPushButton("로그인")
        self.login_btn.clicked.connect(self.login)

        layout = QVBoxLayout()
        layout.addWidget(self.title_label)
        layout.addWidget(self.id_label)
        layout.addWidget(self.id_input)
        layout.addWidget(self.pw_label)
        layout.addWidget(self.pw_input)
        layout.addWidget(self.login_btn)
        self.setLayout(layout)

    def login(self):
        user_id = self.id_input.text()
        user_pw = self.pw_input.text()

        if user_id == "60251838" and user_pw == "3933":
            self.open_main_window()
        else:
            QMessageBox.warning(self, "로그인 실패", "아이디 또는 비밀번호가 잘못되었습니다.")

    def open_main_window(self):
        self.main = MainWindow()
        self.main.show()
        self.close()


class AddProductWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("상품 등록")
        self.setGeometry(500, 100, 800, 600)

        self.name_label = QLabel("상품명")
        self.name_input = QLineEdit()

        self.qty_label = QLabel("수량")
        self.qty_input = QLineEdit()

        self.category_label = QLabel("카테고리")
        self.category_combo = QComboBox()
        self.category_combo.addItems(CATEGORIS)

        self.qty_input.returnPressed.connect(self.add_product)

        self.btn = QPushButton("등록")
        self.btn.clicked.connect(self.add_product)

        layout = QVBoxLayout()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.qty_label)
        layout.addWidget(self.qty_input)
        layout.addWidget(self.category_label)
        layout.addWidget(self.category_combo)
        layout.addWidget(self.btn)
        self.setLayout(layout)

    def add_product(self):
        name = self.name_input.text()
        qty_text = self.qty_input.text()
        category = self.category_combo.currentText()

        if name == "" or qty_text == "":
            QMessageBox.warning(self, "오류", "상품명과 수량을 입력하세요")
            return

        if not qty_text.isdigit():
            QMessageBox.warning(self, "오류", "숫자만 입력 가능합니다.")
            return

        qty = int(qty_text)
        products.append({"name": name, "qty": qty, "category": category})

        QMessageBox.information(self, "성공", f"{name} 상품이 등록되었습니다.")
        self.close()
        save_products()


class ViewProductWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("상품 조회")
        self.setGeometry(500, 100, 800, 600)

        self.list = QListWidget()
        self.load_products()

        self.delete_btn = QPushButton("상품 삭제")
        self.delete_btn.clicked.connect(self.delete_product)
        self.delete_btn.setShortcut(Qt.Key_Return)
        self.delete_btn.setShortcut(Qt.Key_Enter)

        layout = QVBoxLayout()
        layout.addWidget(self.list)
        layout.addWidget(self.delete_btn)
        self.setLayout(layout)

    def load_products(self):
        self.list.clear()

        if len(products) == 0:
            self.list.addItem("등록된 상품이 없습니다.")
        else:
            for p in products:
                category = p.get('category', '미분류')
                self.list.addItem(f"[{category}] {p['name']} - 재고 {p['qty']}개")

    def delete_product(self):
        selected = self.list.currentRow()

        if selected == -1:
            QMessageBox.warning(self, "오류", "삭제할 상품을 선택하세요.")
            return

        name = products[selected]['name']
        confirm = QMessageBox.question(self, "확인",
                                       f"{name} 상품을 삭제하시겠습니까?",
                                       QMessageBox.Yes | QMessageBox.No)

        if confirm == QMessageBox.Yes:
            del products[selected]
            QMessageBox.information(self, "성공", f"{name} 상품이 삭제되었습니다.")
            self.load_products()
            save_products()


class UpdateStockWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("입출고 관리")
        self.setGeometry(500, 100, 800, 600)

        self.list = QListWidget()
        self.load_products()

        self.list.itemActivated.connect(self.update_stock)

        self.btn = QPushButton("수량 변경")
        self.btn.clicked.connect(self.update_stock)

        layout = QVBoxLayout()
        layout.addWidget(self.list)
        layout.addWidget(self.btn)
        self.setLayout(layout)

    def load_products(self):
        self.list.clear()
        for p in products:
            category = p.get('category', '미분류')
            self.list.addItem(f"[{category}] {p['name']} - 재고 {p['qty']}개")

    def update_stock(self):
        selected = self.list.currentRow()

        if selected == -1:
            QMessageBox.warning(self, "오류", "변경할 상품을 선택하세요.")
            return

        name = products[selected]['name']
        value, ok = QInputDialog.getInt(
            self, "입출고 관리",
            f"{name}의 변경할 수량 입력 (+입고, -출고):", 0
        )

        if ok:
            products[selected]['qty'] += value
            QMessageBox.information(self, "성공", f"{name}의 재고가 변경되었습니다.")
            self.load_products()
            save_products()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("공장 재고 관리 프로그램")
        self.setGeometry(500, 100, 800, 600)

        self.label = QLabel("공장 재고 관리 프로그램 실행", self)
        self.label.setAlignment(Qt.AlignCenter)

        self.btn1 = QPushButton("상품 등록")
        self.btn2 = QPushButton("상품 조회")
        self.btn3 = QPushButton("입출고 관리")
        self.btn4 = QPushButton("종료")

        self.btn1.clicked.connect(self.open_add_product)
        self.btn2.clicked.connect(self.open_view_product)
        self.btn3.clicked.connect(self.open_update_stock)
        self.btn4.clicked.connect(self.close)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.label)

        v_layout = QVBoxLayout()
        v_layout.addWidget(self.btn1)
        v_layout.addWidget(self.btn2)
        v_layout.addWidget(self.btn3)
        v_layout.addWidget(self.btn4)

        main_layout = QVBoxLayout()
        main_layout.addLayout(h_layout)
        main_layout.addLayout(v_layout)

        self.setLayout(main_layout)

    def open_add_product(self):
        self.add_product_window = AddProductWindow()
        self.add_product_window.show()

    def open_view_product(self):
        self.view_product_window = ViewProductWindow()
        self.view_product_window.show()

    def open_update_stock(self):
        self.update_stock_window = UpdateStockWindow()
        self.update_stock_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    login = Login()
    login.show()
    sys.exit(app.exec_())

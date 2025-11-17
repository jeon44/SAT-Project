import sys
from PyQt5.QtWidgets import (QApplication,QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QMessageBox,
                             QListWidget, QInputDialog)
from PyQt5.QtCore import Qt

products = []

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

        self.qty_input.returnPressed.connect(self.add_product)

        self.btn = QPushButton("등록")
        self.btn.clicked.connect(self.add_product)

        layout = QVBoxLayout()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.qty_label)
        layout.addWidget(self.qty_input)
        layout.addWidget(self.btn)
        self.setLayout(layout)

    def add_product(self):
        name = self.name_input.text()
        qty_text = self.qty_input.text()

        if name == "" or qty_text == "":
            QMessageBox.warning(self, "오류", "상품명과 수량을 입력하세요")
            return
        
        if not qty_text.isdigit():
            QMessageBox.warning(self, "오류", "숫자만 입력 가능합니다.")
            return
        
        qty = int(qty_text)
        products.append({"name": name, "qty": qty})

        QMessageBox.information(self, "성공", f"{name} 상품이 등록되었습니다.")
        self.close()

class ViewProductWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("상품 조회")
        self.setGeometry(500, 100, 800, 600)

        self.list = QListWidget()
        self.load_products()

        layout = QVBoxLayout()
        layout.addWidget(self.list)
        self.setLayout(layout)

    def load_products(self):
        self.list.clear()

        if len(products) == 0:
            self.list.addItem("등록된 상품이 없습니다.")
        else:
            for p in products:
                self.list.addItem(f"{p['name']} - 재고 {p['qty']}개")


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
            self.list.addItem(f"{p['name']} - 재고 {p['qty']}개")

    def update_stock(self):
        selected = self.list.currentRow()

        if selected == -1:
            QMessageBox.warning(self, "오류", "변경할 상품을 선택하세요.")
            return
        
        name = products[selected]['name']
        value, ok = QInputDialog.getInt(self, "입출고 관리", f"{name}의 변경할 수량 입력 (+입고, -출고):", 0)

        if ok:
            products[selected]['qty'] += value
            QMessageBox.information(self, "성공", f"{name}의 재고가 변경되었습니다.")
            self.load_products()

class MainWindow(QWidget): #메인 윈도우 클래스 정의 (QWidget 상속)
    def __init__(self):
        super().__init__() #부모 클래스(QWidget)의 초기화자 호출
        #윈도우 창 제목, 창의 위치와 크기를 숫자로 지정함
        self.setWindowTitle("공장 재고 관리 프로그램")
        self.setGeometry(500, 100, 800, 600) 
        #화면에 표시할 라벨 위젯 생성
        self.label=QLabel("공장 재고 관리 프로그램 실행", self)
        self.label.setAlignment(Qt.AlignCenter)
        #버튼 생성
        self.btn1 = QPushButton("상품 등록")
        self.btn2 = QPushButton("상품 조회")
        self.btn3 = QPushButton("입출고 관리")
        self.btn4 = QPushButton("종료")

        self.btn1.clicked.connect(self.open_add_product)
        self.btn2.clicked.connect(self.open_view_product)
        self.btn3.clicked.connect(self.open_update_stock)
        self.btn4.clicked.connect(self.close)

        # 수평 레이아웃: 라벨과 버튼을 옆으로 배치하게 함
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.label)


        # 수직 레이아웃: 위의 수평 레이아웃을 위에서 아래로 배치
        v_layout = QVBoxLayout()
        v_layout.addWidget(self.btn1)
        v_layout.addWidget(self.btn2)
        v_layout.addWidget(self.btn3)
        v_layout.addWidget(self.btn4)

        # 메인 레이아웃을 윈도우세 설정함
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


#프로그램의 시작
if __name__=="__main__":
    app=QApplication(sys.argv)
    login = Login()
    login.show()

    #PyQt 앱 실행 (이벤트 루프 시작)
    sys.exit(app.exec_())


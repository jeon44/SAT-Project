import sys
from PyQt5.QtWidgets import (QApplication,QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit)
from PyQt5.QtCore import Qt


class Login(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("로그인")
        self.setGeometry(500, 100, 800, 600)

        self.title_label = QLabel("로그인")
        self.title_label.setAlignCenter(Qt.AlignCenter)

        self.id_label = QLabel("아이디")
        self.id_input = QLineEdit(self)
        self.id_input.setPlaceholderText("아이디를 입력하세요")

        self.pw_label = QLabel("비밀번호")
        self.pw_input = QLineEdit(self)
        self.pw_input.setPlaceholderText("비밀번호를 입력하세요")

        self.pw_input.setEchoMode(QLineEdit.Password)

        self.login_btn = QPushButton("로그인")
        self.login_btn.clicked.connect(self.check_login)
        
        layout = QVBoxLayout()
        layout.addWidget(self.label)
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
        print("로그인 성공")
    else:
        print("ERROR")


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

        self.btn1.clicked.connect(lambda: print("상품 등록"))
        self.btn2.clicked.connect(lambda: print("상품 조회"))
        self.btn3.clicked.connect(lambda: print("입출고 관리"))
        self.btn4.clicked.connect(lambda: print("종료"))

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


products = []  # 상품의 정보를 저장할 리스트 (전역변수 사용)

#상품 등록 함수
def add_product():
    print("[상품 등록]")
    name = input("상품명 입력: ") #상품 등록
    qty = int(input("수량 입력: ")) #상품의 수량을 입력 후 정수 변환
    product = {"name": name, "qty": qty}
    products.append(product) #product 리스트에 추가
    print(f"상품이 {qty}개 등록되었습니다.\n")

#상품 조회 함수
def view_products():
    print("[상품 조회]")
    if len(products) == 0: #등록된 상품으 존재하지 않을 경우
        print("조회한 상품이 등록되어있지 않습니다.\n")
        return
    # 등록된 상품 목록 출력
    for i in range(len(products)):
        p = products[i]
        print(f"{i + 1}. {p['name']} - 재고: {p['qty']}개")
    print()

#재고 수정 함수
def update_stock():
    print("[입출고 상품]")
    name = input("상품명 입력: ") #수정할 상품명 입력
    for j in products: #등록된 상품 중에서 이름이 같은 것 찾음
        if j["name"] == name:
            #수량이 변동값 입력
            change = int(input("수정할 수량 (+는 입고, -는 출고): "))
            j["qty"] += change #기존 재고에서 추가 or 제거
            print(f"'{name}'의 수량이 {j['qty']}개로 변경되었습니다.\n")
            return
    print("해당 상품이 존재하지 않습니다.\n")

#프로그램의 시작
if __name__=="__main__":
    app=QApplication(sys.argv)
    login = Login()
    login.show()

    #PyQt 앱 실행 (이벤트 루프 시작)
    sys.exit(app.exec_())


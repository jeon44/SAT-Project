import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("공장 재고 관리 프로그램")
        self.setGeometry(200, 200, 600, 400)

        self.label=QLabel("공장 재고 관리 프로그램 실행", self)

        self.btn1 = QPushButton("버튼1")

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.label)
        h_layout.addWidget(self.btn1)

        main_layout = QVBoxLayout()
        main_layout.addLayout(h_layout)

        self.setLayout(main_layout)


products = [] 

def add_product():
    print("[상품 등록]")
    name = input("상품명 입력: ")
    qty = int(input("수량 입력: "))
    product = {"name": name, "qty": qty}
    products.append(product)
    print(f"상품이 {qty}개 등록되었습니다.\n")

def view_products():
    print("[상품 조회]")
    if len(products) == 0:
        print("조회한 상품이 등록되어있지 않습니다.\n")
        return
    for i in range(len(products)):
        p = products[i]
        print(f"{i + 1}. {p['name']} - 재고: {p['qty']}개")
    print()

def update_stock():
    print("[입출고 상품]")
    name = input("상품명 입력: ")
    for j in products:
        if j["name"] == name:
            change = int(input("수정할 수량 (+는 입고, -는 출고): "))
            j["qty"] += change
            print(f"'{name}'의 수량이 {j['qty']}개로 변경되었습니다.\n")
            return
    print("해당 상품이 존재하지 않습니다.\n")


if __name__=="__main__":
    app=QApplication(sys.argv)
    window=MainWindow()
    window.show()


    while True:
        print("1. 상품 등록")
        print("2. 상품 조회")
        print("3. 입출고 관리")
        print("4. 종료")
        choice=input("선택: ")


        if choice=="1":
            add_product()
        elif choice=="2":
            view_products()
        elif choice=="3":
            update_stock()
        elif choice=="4":
            print("프로그램을 종료합니다.")
            break
        else:
            print("ERROR")

    sys.exit(app.exec_())


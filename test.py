products=[] #임시 데이터
def add_product():
    print("[상품 등록]")
    name=input("상품명 입력: ")
    qty=int(input("수량 입력: "))
    product={"name": name, "qty": qty}
    products.append(product)
    print("상품이 {qty}개 등록되었습니다.")

def view_products():
    print("[상품 조회]")
    if len(products)==0:
        print("조회한 상품이 등록되어있지 않습니다.")
        return
    for i in range(len(products)):
        p=products[i]
        print(f"{i+1}.{p['name']} - 재고: {p['qty']}개")
    print()

def update_stock():x
    print("[입출고 상품]")
    name=input("상품명 입력: ")
    for j in products:
        if j["name"]==name:
            change=int(input("수정할 수량: "))
            j["qty"]+=change
            print(f"'{name}'의 수량이 {j['qty']}개로 변경되었습니다.")
            return
    print("해당 상품이 존재하지 않습니다.")
            

   
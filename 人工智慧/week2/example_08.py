# example08.py

age = 20
is_member = True

if age >= 18 and is_member:
    print("恭喜！您符合優惠資格")
else:
    print("抱歉，您不符合優惠資格")

if age < 12 or age > 65:
    print("您可以享受免費票")
else:
    print("需要購票")

if not is_member:
    print("加入會員可享受更多優惠")

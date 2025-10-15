# 依據使用者輸入的數字進行運算

# 讀取使用者輸入
x = int(input("請輸入 X："))
y = int(input("請輸入 Y："))

# 判斷 y 的奇偶
if y % 2 == 1:  # 奇數
    result = x ** 2
else:           # 偶數
    result = x ** y

# 判斷結果是否超過 100
if result > 100:
    print("結果超過 100，不輸出答案。")
else:
    print("運算結果為：", result)

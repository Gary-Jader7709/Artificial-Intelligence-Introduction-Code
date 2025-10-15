import random

# 隨機產生體重（40~100 公斤之間）
weight = random.uniform(40, 100)

# 隨機產生身高（1.4~2.0 公尺之間）
height = random.uniform(1.4, 2.0)

# BMI 計算公式
bmi = weight / (height ** 2)

# 結果輸出
print(f"隨機體重：{weight:.1f} 公斤")
print(f"隨機身高：{height:.2f} 公尺")
print(f"您的 BMI 值為：{bmi:.2f}")

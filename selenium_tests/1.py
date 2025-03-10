import random

def generate_japanese_phone_number():
    # 日本手機號碼的開頭號段
    prefixes = ['070', '080', '090']
    
    # 隨機選擇一個號段
    prefix = random.choice(prefixes)
    
    # 隨機生成後面的 8 位數字
    remaining_digits = ''.join([str(random.randint(0, 9)) for _ in range(8)])
    
    # 組合成完整的手機號碼
    phone_number = prefix + remaining_digits
    
    return phone_number

# 測試生成多個手機號碼
if __name__ == "__main__":
    for _ in range(1):  # 生成 5 個隨機手機號碼
        phone_number = generate_japanese_phone_number()
        print(phone_number)
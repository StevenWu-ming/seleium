import random

def generate_chinese_phone_number():
    # 中國大陸常見的行動電話號段（僅列出部分作為範例）
    prefixes = [
        '130', '131', '132', '133', '134', '135', '136', '137', '138', '139',  # 中國聯通
        '145', '147',  # 中國聯通（數據卡）
        '150', '151', '152', '153', '155', '156', '157', '158', '159',  # 中國聯通
        '166', '167', '170', '171', '173', '175', '176', '177', '178',  # 中國聯通
        '180', '181', '182', '183', '184', '185', '186', '187', '188', '189',  # 中國電信
        '190', '191', '193', '195', '196', '197', '198', '199',  # 中國電信
    ]
    
    # 隨機選擇一個號段
    prefix = random.choice(prefixes)
    # 隨機生成剩餘的 8 位數字
    remaining_digits = ''.join([str(random.randint(0, 9)) for _ in range(8)])
    return prefix + remaining_digits

# 測試函數
for _ in range(5):
    print(generate_chinese_phone_number())
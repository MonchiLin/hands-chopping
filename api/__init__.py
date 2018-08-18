import re


def clear_text(text):
    return re.sub("[\s+\.\!\/_,$%^*(+\"\')]+|[+——()?【】“”！，。？、~@#￥%……&*（）]+'",'', text)



name = '探险家斯皮兰卡 (中文版)'

print(clear_text(name))
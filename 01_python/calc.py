__version__ = 0.1  #변수

def plus(num1, num2):
    return num1 + num2

def minus(num1, num2):
    return num1 - num2

def multiply(num1, num2):
    return num1 * num2

def divide(num1, num2):
    return num1 / num2

# 실행코드 -> main 모듈로 실행될때만 실행되도록 처리.
print(__name__)
if __name__ == "__main__":
    result = minus(10, 5)  # 함수를 호출 -> 기본: 같은 모듈에 정의 된 함수를 호출
    print(result)

# python calc.py


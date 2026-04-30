# run.py
# calc 모듈의 함수들을 호출 하려면 calc 모듈을 import 해야한다.
# calc.py -> 모듈이름: 파일명까지.
# import calc  # calc 모듈을 사용하겠다.
import calc as c  # calc 모듈을 c라는 이름으로 사용하겠다. 

def test():
    pass
test()

# result = calc.plus(20, 30) # 모듈이름.사용할함수() 호출
result = c.plus(20, 30)
print(result)
# print(calc.minus(100, 20))
print(c.minus(100, 20))

# python run.py
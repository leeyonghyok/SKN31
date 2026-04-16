# run.py
# calc 모듈의 함수들을 호출 하려면 calc 모듈을 import 해야한다.
# calc.py -> 모듈이름: 파일명까지.
import calc

result = calc.plus(20, 30) # 모듈이름.사용할함수() 호출
print(result)
print(calc.minus(100, 20))

# python run.py
# run2.py

def plus(n1, n2):
    print("안녕")

# 모듈에 있는 일부 함수, 클래스, 변수를 import -> 이름으로 호출가능
from calc import plus as p, minus  # calc의 plus, minus 두 함수를 사용

# from 사용할 것이 있는 경로  import 사용할것(모듈, 모듈안에 함수,클래스,변수)

result1 = p(100, 200)
result2 = minus(200, 300)
print(result1, result2)


# 다른 패키지의 모듈 호출
import my_package.greet # as h
my_package.greet.hello_eng()

from my_package import greet
greet.hello_kor()

from my_package import greet as g
g.hello_kor()

print(g.__version__)

# 패키지 -> 모듈 -> 함수 를 import
from my_package.greet import hello_kor, hello_eng
hello_kor()
hello_eng()

# import 를 하면 PYTHONPATH 경로에서 찾는다. 현재실행중인 디렉토리.
import sys
sys.path.append(r'c:\temp\lib')   # PATHONPATH 에 new_package가 있는 경로 등록
from new_package import new_module
new_module.test_func()


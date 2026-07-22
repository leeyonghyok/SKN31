# 1. JavaScript 소개

JavaScript는 웹 페이지에 동작을 추가하는 프로그래밍 언어이다.

HTML이 웹 문서의 구조를 만들고 CSS가 화면 모양을 꾸민다면, JavaScript는 사용자의 동작에 반응하고 데이터를 처리하며 화면의 내용을 바꾸는 역할을 한다.

예를 들어 다음과 같은 기능을 JavaScript로 구현할 수 있다.

- 버튼을 클릭했을 때 메뉴를 열고 닫는다.
- 입력한 값이 올바른지 검사한다.
- 서버에서 데이터를 받아 화면에 표시한다.
- 목록을 추가하거나 삭제한다.
- 화면을 새로 고치지 않고 일부 내용만 변경한다.

JavaScript는 브라우저뿐 아니라 Node.js 환경에서도 실행할 수 있다.

## 1.1 JavaScript 실행 환경

JavaScript 코드를 실행하는 대표적인 환경은 다음과 같다.

### 브라우저

Chrome, Edge, Firefox, Safari 등의 브라우저에는 JavaScript 엔진이 포함되어 있다.

브라우저에서 실행되는 JavaScript는 다음 기능을 사용할 수 있다.

- HTML 문서 접근
- 사용자 이벤트 처리
- 네트워크 요청
- 로컬 저장소 사용

### Node.js

Node.js는 브라우저 밖에서 JavaScript를 실행할 수 있게 해 주는 런타임 환경이다.

Node.js를 사용하면 다음과 같은 프로그램을 만들 수 있다.

- 웹 서버
- 명령줄 프로그램
- 빌드 도구
- 자동화 프로그램

## 1.2 대표적인 JavaScript Library, Framework

| 기술 | 설명 |
|---|---|
| React | 사용자 인터페이스를 만들기 위한 라이브러리 |
| Vue.js | 사용자 인터페이스를 만들기 위한 프레임워크 |
| Svelte | 컴파일 방식으로 UI를 만드는 프레임워크 |
| Express | Node.js 기반 웹 서버 프레임워크 |
| Electron | JavaScript로 데스크톱 애플리케이션을 만드는 도구 |

---

# 2. JavaScript 작성 개요

## 2.1 HTML 문서 안에 작성하기

JavaScript 코드는 `<script>` 태그 안에 작성할 수 있다.

```html
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <title>JavaScript 예제</title>
</head>
<body>
  <h1>JavaScript 시작</h1>

  <script>
    console.log("안녕하세요.");
  </script>
</body>
</html>
```

> `console.log()`는 개발자 도구의 콘솔에 값을 출력한다.

## 2.2 외부 JavaScript 파일 사용하기

JavaScript 코드는 별도의 `.js` 파일로 분리하는 것이 좋다.

```html
<script src="./app.js"></script>
```

```javascript
// app.js
console.log("외부 JavaScript 파일을 실행합니다.");
```

`src` 속성을 사용한 `<script>` 태그 안에는 별도의 JavaScript 코드를 작성하지 않는다.


## 2.3 `defer` 속성 사용하기

HTML 문서를 모두 읽은 뒤 JavaScript를 실행하려면 `defer` 속성을 사용한다.

```html
<head>
  <script src="./app.js" defer></script>
</head>
```
`<script>` 를 만나면 문서 파싱을 멈추고 script 파일을 다운로드 받는다.  
`defer`를 사용하면 JavaScript 파일을 다운로드하는 동안에도 문서파싱을 계속 진행한다.

> **Parsing**(**파싱**): 문자열로 된 내용을 컴퓨터가 이해하고 처리할 수 있는 구조로 바꾸는 과정을 말한다.

## 2.4 모듈 방식으로 실행하기

현대 JavaScript 프로젝트는 파일을 모듈 단위로 나누어 작성한다.

```html
<script type="module" src="./main.js"></script>
```

`type="module"`을 사용하면 `import`, `export` 문법을 사용할 수 있다.

> JavaScript 모듈은 프로그램을 기능별로 나눈 독립적인 JavaScript 파일이다. 필요한 기능은 export로 외부에 공개하고, 다른 파일에서는 import로 가져와 사용한다. 이를 통해 코드의 재사용성과 유지보수성을 높일 수 있다.
---

## 2.5 주석

- **한 줄 주석**
  - `//` 사용
    ```javascript
    // 한 줄 주석이다.
    const age = 20;
    ```

- **여러 줄 주석**
  - `/* 주석내용 */` 사용
    ```javascript
    /*
      여러 줄에 걸쳐
      설명을 작성할 수 있다.
    */
    const name = "홍길동";
    ```

## 2.6 코드 블록

중괄호 `{ }`는 여러 문장을 하나의 코드 블록으로 묶는다.

```javascript
if (age >= 19) {
  console.log("성인입니다.");
  console.log("서비스를 이용할 수 있습니다.");
}
```

## 2.7 세미콜론
세미콜론은 하나의 문장(명령문)이 끝났음을 표시하는 기호이다.
JavaScript는 세미콜론이 없어도 자동으로 문장의 끝을 판단하는 ASI(Automatic Semicolon Insertion, 자동 세미콜론 삽입) 기능이 있지만, 예상하지 못한 오류를 줄이기 위해 보통 **세미콜론을 작성하는 것이 권장**된다.

```javascript
const name = "홍길동";
console.log(name);
```

---

# 3. 변수와 상수

변수는 값을 저장하거나 참조하기 위해 붙인 이름, 즉 값의 식별자이다.

JavaScript에서는 변수를 선언할 때 `const`와 `let`을 사용한다.

## 3.1 `const`

`const`는 다른 값으로 다시 대입하지 않을 변수를 선언할 때 사용한다.

```javascript
const name = "홍길동";
const birthYear = 2000;
```

다른 값을 다시 대입하면 오류가 발생한다.

```javascript
const age = 20;
age = 21; // TypeError
```

객체나 배열을 `const`로 선언하더라도 내부 값은 변경할 수 있다.

```javascript
const user = {
  name: "홍길동",
  age: 20,
};

user.age = 21; // 가능
user = {};     // 불가능
```

`const`는 객체 자체를 완전히 변경할 수 없게 만드는 문법이 아니다. 변수에 새로운 객체를 다시 대입하지 못하게 한다.

## 3.2 `let`

`let`은 값이 바뀌는 변수를 선언할 때 사용한다.

```javascript
let score = 80;
score = 90;
```

반복 횟수를 세거나 상태가 변하는 값을 저장할 때 사용한다.

```javascript
let count = 0;
count += 1;
```

## 3.3 `var`

`var`는 오래된 JavaScript 코드에서 볼 수 있는 변수 선언 방식이다.

```javascript
var message = "안녕하세요.";
```

`var`는 함수 단위의 유효 범위를 가지며 같은 이름으로 다시 선언할 수 있다. 이 때문에 예상하지 못한 오류가 생길 수 있다.

새로 작성하는 코드에서는 다음 원칙을 따른다.

1. 기본적으로 `const`를 사용한다.
2. 재할당이 필요한 경우에만 `let`을 사용한다.
3. `var`는 가능하면 사용하지 않는다. 기존 코드를 읽기 위한 목적으로 이해한다.

## 3.4 유효 범위

`let`과 `const`는 선언된 영역 안에서만 사용할 수 있다. 자신이 선언된 block 밖에서는 호출 할 수 없다. (Block Scope)

```javascript
if (true) {
  const message = "블록 안의 값";
  console.log(message);
}

console.log(message); // ReferenceError
```

## 3.5 변수 이름 규칙

변수 이름에는 다음 문자를 사용할 수 있다.

- 영문자와 유니코드 문자
- 숫자
- `_`
- `$`

숫자로 시작할 수는 없다.

```javascript
const userName = "홍길동";
const score20 = 90;
const _temp = 10;
```

다음과 같은 이름은 사용할 수 없다.

```javascript
const 1score = 90; // 숫자로 시작해서 오류
const const = 10;  // 예약어를 사용해서 오류
const my@score = 20; // _, $ 이외의 특수문자를 사용해서 오류
```

관례적으로 변수의 이름은 **카멜 표기법**을 사용한다.

```javascript
const userName = "홍길동";
const totalPrice = 30000;
```

---

# 4. 데이터 타입

JavaScript의 데이터는 크게 원시 타입(Primitive Type)과 객체 타입(Object Type)으로 나뉜다.

## 4.1 원시 타입(Primitive Type)

| 타입 | 설명 | 예 |
|---|---|---|
| `string` | 문자열 | `"hello"` |
| `number` | 숫자(정수, 실수) | `10`, `3.14` |
| `bigint` | 매우 큰 정수<br>(number 범위를 넘어선 정수(±9007199254740991) 표현) | `9007199254740998n` |
| `boolean` | 논리값 | `true`, `false` |
| `undefined` | 값이 아직 정해지지 않음 | `undefined` |
| `null` | 값이 없음을 의도적으로 표현 | `null` |
| `symbol` | 고유한 식별값 | `Symbol("id")` |

## 4.2 문자열(string)

- 문자열 값은 작은따옴표, 큰따옴표 또는 백틱으로 감싸준다.

  ```javascript
  const message1 = "안녕하세요.";
  const message2 = 'JavaScript입니다.';
  ```

- 백틱 문자열은 **여러 줄 문자열**과 **템플릿 문자열**을 만들 때 사용한다.

  ```javascript
  const name = "홍길동";
  const age = 20;

  const message = `이름: ${name}
  나이: ${age}`;

  console.log(message);
  ```

- `${ }` 안에는 계산식도 작성할 수 있다.

  ```javascript
  const price = 10000;
  const quantity = 3;

  console.log(`총액: ${price * quantity}원`);
  ```

## 4.3 숫자(number)

- JavaScript의 정수와 실수는 모두 `number` 타입이다.

  ```javascript
  const age = 20;
  const height = 175.5;
  ```

- 계산할 수 없는 숫자 결과는 `NaN`으로 나타난다.

  ```javascript
  const result = Number("hello");

  console.log(result); // NaN
  ```

## 4.4 `null`과 `undefined`

- `undefined`는 값이 아직 값이 `할당되지 않은 상태를 나타낸다.

  ```javascript
  let userName;

  console.log(userName); // undefined
  ```

- `null`은 개발자가 값이 없음을 의도적으로 표시할 때 사용한다.

  ```javascript
  const selectedUser = null;
  ```

## 4.5 객체 타입

- 객체는 여러 값을 하나로 묶어 관리한다.

  ```javascript
  const user = {
    name: "홍길동",
    age: 20,
  };
  ```

- **배열**과 **함수**도 객체의 한 종류이다.

  ```javascript
  const numbers = [10, 20, 30];

  function add(a, b) {
    return a + b;
  }
  ```

## 4.6 `typeof`

`typeof` 연산자는 값의 타입을 문자열로 반환한다.

```javascript
console.log(typeof "hello");    // "string"
console.log(typeof 20);         // "number"
console.log(typeof true);       // "boolean"
console.log(typeof undefined);  // "undefined"
console.log(typeof {});         // "object"
console.log(typeof []);         // "object"
console.log(typeof function(){}); // "function"
```

`null`과 배열의 타입은 `"object"`로 반환한다.

> `null`이 `"object"`인 것은 JavaScript 초기 설계에서 생긴 특수한 동작이다. `null`이 실제 객체라는 뜻은 아니다.

배열인지 여부를 확인할 때는 `Array.isArray()`를 사용한다.

```javascript
console.log(Array.isArray([1, 2, 3])); // true
```

---

# 5. 연산자와 형 변환

## 5.1 산술 연산자

```javascript
const a = 10;
const b = 3;

console.log(a + b); // 덧셈. 
console.log(a - b); // 뺄셈. 
console.log(a * b); // 곱셈. 
console.log(a / b); // 나눗셈. 3.333...
console.log(a % b); // 나머지 연산(모듈러스 연산)1
console.log(a ** b); // 제곱연산. 
```

## 5.2 대입 연산자

```javascript
let score = 10;

// 복합 대입 연산자
score += 5; // score = score + 5
score -= 2;
score *= 3;
score /= 2;
```

## 5.3 증가와 감소 연산자

변수가 가진 값을 1 증가, 감소 시킨다.

```javascript
let count = 10;

count++;
count--;
```

증감 연산자는 변수 앞(전위 연산)과 뒤(후위 연산)에 붙일 수 있다.
전위 연산(`++x`)과 후위 연산(`x++`)은 다른 연산과 같이 사용될 때 값을 반환하는 시점이 다르다.

```javascript
let a = 10;
let b = a++; // 대입 연산을 먼저한다.

console.log(a, b); // 11, 10
```

```javascript
let x = 10;
let y = ++x; // 증가 연산을 먼저 한다.

console.log(x, y); // 11, 11
```

## 5.4 비교 연산자

**크기 비교**
```javascript
console.log(10 > 5);   // true
console.log(10 >= 10); // true
console.log(5 < 3);    // false
console.log(5 <= 5);   // true
```

**동등 비교**는 `===`와 `!==`를 사용한다.
```javascript
console.log(10 === 10);   // true
console.log(10 === "10"); // false
console.log(10 !== "10"); // true
```

`==`와 `!=` 는 비교하기 전에 타입을 자동으로 변환한다. 그래서 타입이 다르더라도 값이 같으면 `true`가 된다.

```javascript
console.log(10 == "10"); // true
```

타입 변환으로 인한 혼동을 줄이기 위해 일반적으로 `===`, `!==`를 사용한다.


## 5.5 truthy와 falsy
**Truthy(참 같은 값)와 Falsy**(**거짓 같은 값**)는 참(true)이나 거짓(false)을 뜻하는 불리언(Boolean) 데이터가 아니더라도, 조건문 등에서 참이나 거짓처럼 취급되는 값을 말한다.
JavaScript의 조건식에서는 모든 타입의 값이 참 또는 거짓으로 변환된다.
대표적인 falsy 값은 다음과 같다. (falsy가 아닌 값들은 다 truthy 이다.)

```javascript
false
0
-0
0n
""  // 빈문자열
null
undefined
NaN
```

이 값을 제외한 값은 truthy이다.

```javascript
if ("hello") {
  console.log("실행됩니다.");
}
```

## 5.6 논리 연산자
JavaScript의 논리 AND(`&&`)와 OR(`||`) 연산자는 boolean 값뿐만 아니라 피연산자 자체를 반환할 수도 있다.
  
### `&&` (논리 AND 연산자)

왼쪽 값이 falsy면 왼쪽 값을 반환한다. 왼쪽 값이 truthy면 오른쪽 값을 반환한다.

```javascript
console.log(false && "실행"); // false
console.log(true && "실행");  // "실행"
console.log("" && 100);        // ""
console.log("hello" && 100);   // 100
```

### `||` (논리 OR 연산자)

왼쪽 값이 truthy면 왼쪽 값을 반환한다. 왼쪽 값이 falsy면 오른쪽 값을 반환한다.

```javascript
console.log("값" || "기본값"); // "값"
console.log("" || "기본값");   // "기본값"
```

### `!` (논리 NOT 연산자)

논리값을 반대로 바꾼다.

```javascript
console.log(!true);  // false
console.log(!false); // true
```

## 5.7 삼항 연산자

삼항 연산자는 조건에 따라 두 값 중 하나를 선택한다.
`조건식 ? value1 : value2`

```javascript
const age = 20;
const result = age >= 19 ? "성인" : "미성년자";

console.log(result);
```

## 5.8 형 변환

| 변환 대상 | 함수 또는 표현 |
|---|---|
| 문자열 | `String(value)`, value+"" |
| 숫자 | `Number(value)` |
| 불리언 | `Boolean(value)` |
| 정수 해석 | `parseInt(value, radix)` |
| 실수 해석 | `parseFloat(value)` |
| 큰 정수 | `BigInt(value)` |


**문자열을 숫자**로 바꿀 때는 `Number()`를 사용할 수 있다.

```javascript
console.log(Number("123"));        // 123
console.log(Number("12.5"));       // 12.5
console.log(Number(""));           // 0
console.log(Number(true));         // 1
console.log(Number(false));        // 0
console.log(Number(null));         // 0
console.log(Number("hello"));      // NaN
console.log(Number(undefined));    // NaN
```

**문자열을 정수와 실수**로 해석

```javascript
console.log(parseInt("123px", 10));  // 123 // 문자열의 왼쪽부터 숫자로 해석할 수 있는 부분까지 읽어 정수로 변환한다. 두 번째 인수 10은 문자열을 10진수로 해석하라는 의미이다.
console.log(parseInt("12.9", 10));  // 12
console.log(parseInt("101", 2));    // 5 // 문자열을 2진수로 해석하라는 의미이다.
console.log(parseInt("hello"));   // NaN

console.log(parseFloat("12.9"));   // 12.9
console.log(parseFloat("3.14kg")); // 3.14
console.log(parseFloat("hello"));   // NaN
```
- `parseInt()`의 두번째 인수는 진법이다. 
- `Number()`는 문자열 전체가 올바른 숫자여야 하지만, `parseInt()`, `parseFloat`은 앞부분부터 정수로 해석할 수 있는 부분까지만 읽는다.


---

# 6. 제어문
JavaScript의 조건문은 **if문**과 **switch case문**이 있다.

## 6.1 조건문

### if문
조건식이 true이면 if 블록을 실행하고, false이면 실행하지 않는다.  
else if를 사용하면 여러 조건을 순서대로 검사할 수 있으며, 모든 조건이 거짓이면 else 블록을 실행한다.  
조건은 위에서 아래 순서대로 검사하며, 처음으로 true가 된 블록만 실행하고 나머지는 검사하지 않는다.
```javascript
const score = 85;

if (score >= 90) {
  console.log("A");
} else if (score >= 80) {
  console.log("B");
} else {
  console.log("C");
}
```

조건식에는 비교식뿐 아니라 모든 값이 올 수 있다.

```javascript
const userName = "홍길동";

if (userName) {
  console.log("이름이 입력되었습니다.");
}
```

### Switch Case 문

하나의 값을 여러 경우와 비교할 때 사용할 수 있다.

```javascript
const menu = "save";

switch (menu) {
  case "save":
    console.log("저장을 시작합니다.");
    console.log("저장했습니다.");
    break;

  case "delete":
    console.log("삭제를 시작합니다.");
    console.log("삭제했습니다.");
    break;

  default:
    console.log("알 수 없는 명령입니다.");
}
```
- `menu`의 값을 `case`와 순서대로 비교해서 일치하는 case구문을 실행한다.

`break`는 일치하는 case의 코드를 실행한 뒤 switch문을 종료한다. `break`를 생략하면 다음 case의 코드까지 계속 실행된다.
```javascript
const month = 3;

switch(month) { //동등비교 연산
    case 1: case 3: case 5: case 7: case 8: case 10: case 12:
        console.log(month+"월은 31일까지 입니다.");
        break;
    case 4: case 6: case 9: case 11:
        console.log(month+"월은 30일까지 입니다.");
        break;
    case 2:
        console.log(month+"월은 28일까지 입니다.");
        break;
    default:  //if문에 else
        console.log(month+"는 잘못된 값입니다.");
}
```

`switch`는 타입을 자동으로 변환하지 않고 값을 비교한다.

```javascript
const value = 10;

switch (value) {
  case "10":
    console.log("문자열 10");
    break;

  case 10:
    console.log("숫자 10");
    break;
}
```

실행 결과는 `숫자 10`이다.

---

## 6.2 반복문

### `for` 문

반복 횟수가 분명할 때 주로 사용한다.

```javascript
for (let i = 0; i < 5; i++) {
  console.log(i);
}
```

### `while` 문

조건이 참인 동안 반복한다.

```javascript
let count = 0;

while (count < 5) {
  console.log(count);
  
  count++;
}
```

### `do...while` 문

조건을 검사하기 전에 반복문 본문을 한 번 실행한다.

```javascript
let count = 0;

do {
  console.log(count);
  count++;
} while (count < 5);
```

### `for...of`

배열이나 문자열처럼 **순서가 있는 값의 요소를 반복**할 때 사용한다.

```javascript
const numbers = [10, 20, 30];

for (const number of numbers) {
  console.log(number);
}
```

인덱스와 값을 함께 사용하려면 `entries()`를 사용할 수 있다.

```javascript
const fruits = ["사과", "배", "포도"];

for (const [index, fruit] of fruits.entries()) {
  console.log(index, fruit);
}
```

### `for...in`

객체의 속성 이름을 반복할 때 사용한다.

```javascript
const user = {
  name: "홍길동",
  age: 20,
};

for (const key in user) {
  console.log(key, user[key]);
}
```


### `break`와 `continue`

`break`는 반복문을 즉시 종료한다.

```javascript
for (let i = 0; i < 10; i++) {
  if (i === 3) {
    break;
  }

  console.log(i);
}
```

`continue`는 현재 반복을 건너뛰고 다음 반복을 실행한다.

```javascript
for (let i = 0; i < 10; i++) {
  if (i % 3 === 0) {
    continue;
  }

  console.log(i);
}
```

---

# 7. 함수

함수는 여러 명령문들을 하나의 작업 단위로 묶은 것이다.
JavaScript의 함수는 변수에 저장하거나 다른 함수에 전달하고 함수의 결과로 반환할 수 있다. (First Class Citizen - 일급객체)
Javascript는 함수를 정의 하는 다양한 방법이 있다.

## 7.1 함수 선언문

```javascript
function add(a, b) {
  return a + b;
}

const result = add(10, 20);

console.log(result); // 30
```

## 7.2 함수 표현식(Function Expression)

**함수 표현식**(**Function Expression**)은 함수를 하나의 값으로 만들어 변수에 저장하는 방식이다. 함수는 표현식의 결과로 생성되며, 생성된 함수를 변수에 할당하여 사용한다.
함수 표현식은 변수에 할당된 이후부터 사용할 수 있다.

```javascript
const add = function(a, b) {
  return a + b;
};

console.log(add(10, 20));
```

## 7.3 화살표 함수(Arrow Function)

**화살표 함수**(**Arrow Function**)는 function 키워드 대신 `=>` 기호를 사용하여 함수를 간결하게 작성하는 문법이다. 화살표 함수도 함수 표현식처럼 생성된 함수를 변수에 저장하여 사용한다.

```javascript
const add = (a, b) => {
  return a + b;
};
```
- (a, b) => { ... }는 화살표 함수이고, 생성된 함수 객체를 add 변수에 저장
  
함수 본문이 하나의 표현식이면 중괄호와 `return`을 생략할 수 있다.

```javascript
const add = (a, b) => a + b;
```

매개변수가 하나이면 괄호를 생략할 수 있다.

```javascript
const double = number => number * 2;
```

매개변수가 없으면 빈 괄호(필수)를 작성한다.

```javascript
const greet = () => console.log("안녕하세요.");
```

객체를 바로 반환할 때는 객체를 괄호로 감싼다.

```javascript
const createUser = (name, age) => ({
  name,
  age,
});
```

## 7.4 다양한 함수의 매개변수

### 기본값이 있는 매개변수

호출할 때 인수를 전달하지 않으면 기본값을 사용할 수 있다.

```javascript
function greet(name = "무명") {
  return `안녕하세요, ${name}님`;
}

console.log(greet());
console.log(greet("홍길동"));
```

### 나머지 매개변수(Rest Parameter)
전달된 여러 인수들을 하나의 배열로 받는다. 매개변수 앞에 ...을 붙인다.
```javascript
function sum(...numbers) {
  console.log(numbers);
}

sum(1, 2, 3, 4);
```

### 구조 분해 할당(Destructuring Assignment)

전달 된 배열이나 객체에서 필요한 값을 꺼내 매개변수로 받는다.
```javascript
function printPoint([x, y]) {
  console.log(x, y);
}

printPoint([10, 20]);
```

> 나머지 매개변수와 구조 분해 할당은 뒤(11, 12)에서 좀 더 자세하게 살펴 본다.

## 7.5 콜백 함수
함수를 **매개변수로 받거나** 함수를 **반환하는** 함수를 **고차함수** 라고 한다. 그리고 고차함수에 전달되는 함수를 **콜백 함수**(**callback**)라고 한다.
JavaScript는 함수를 일급 객체로 취급하므로 고차 함수를 지원한다.

```javascript
function repeat(count, callback) {
  for (let i = 0; i < count; i++) {
    callback(i);
  }
}

repeat(3, console.log);
```
- `repeat`: 고차 함수
- `console.log`: 콜백 함수

배열 메서드와 이벤트 처리에서 콜백 함수를 자주 사용한다.

---

# 8. 배열

배열은 여러 값을 순서대로 관리하는 객체이다. 배열에 저장된 각 값은 요소(element)라고 하며, 각 요소는 0부터 시작하는 인덱스를 가진다.

```javascript
const fruits = ["사과", "배", "포도"];
```

## 8.1 배열 요소 접근

배열의 요소는 인덱스를 이용해 조회, 변경 한다.

```javascript
console.log(fruits[0]); // "사과"
console.log(fruits[1]); // "배"

fruits[0] = '참외';
console.log(fruits);
```

## 8.2 배열 길이

```javascript
console.log(fruits.length); // 3
```

## 8.3 주요 배열 메서드

### `push()`

배열 끝에 값을 추가한다.

```javascript
const numbers = [1, 2];

numbers.push(3);

console.log(numbers); // [1, 2, 3]
```

### `pop()`

배열 끝(마지막 인덱스)의 값을 제거하고 반환한다.

```javascript
const numbers = [1, 2, 3];
const removed = numbers.pop();

console.log(removed); // 3
console.log(numbers); // [1, 2]
```

### `unshift()`

배열 앞에 값을 추가한다.

```javascript
const numbers = [2, 3];

numbers.unshift(1);

console.log(numbers); // [1, 2, 3]
```

### `shift()`

배열 앞의 값을 제거하고 반환한다.

```javascript
const numbers = [1, 2, 3];
const removed = numbers.shift();

console.log(removed); // 1
```

### `slice()`

배열의 일부를 복사해 새 배열을 반환한다.

```javascript
const numbers = [10, 20, 30, 40, 50];
const result = numbers.slice(1, 4); // index 1 ~ index 3 까지 조회

console.log(result); // [20, 30, 40]
console.log(numbers); // 원본 유지
```

### `splice()`

배열의 요소를 삭제하거나 추가하거나 교체한다.

```javascript
const numbers = [1, 2, 3, 4];

numbers.splice(1, 2, 10, 20, 30);  // index 1 부터 2개의 요소를 그 이후 값들(10, 20)으로 변경한다.

console.log(numbers); // [1, 10, 20, 30, 4]
```

`splice()`는 원본 배열을 직접 변경한다.

### `concat()`

배열을 합쳐 새 배열을 반환한다.

```javascript
const a = [1, 2];
const b = [3, 4];

const result = a.concat(b);

console.log(result); // [1, 2, 3, 4]
```

### `join()`

배열의 값을 문자열로 연결한다.

```javascript
const words = ["JavaScript", "React", "Vue"];

console.log(words.join(", ")); // "JavaScript, React, Vue"
```

### `includes()`

배열에 특정 값이 있는지 확인한다.

```javascript
const fruits = ["사과", "배", "포도"];

console.log(fruits.includes("배")); // true
```

---

# 9. 배열 고차 함수

배열 고차 함수는 함수를 인수로 받아 각 요소를 처리한다.
> **고차함수:** 함수를 인수로 받는 함수. 고차함수에 전달되는 함수를 **Callback 함수** 라고 한다.

## 9.1 `forEach()`

배열의 각 요소의 값과 index를 받아서 처리하는 함수를 실행한다.

```javascript
const numbers = [10, 20, 30];

//forEach()에 전달되는 함수는 파라미터로 배열의 개별 요소와 index를 받는다.
numbers.forEach((number, index) => {  
  console.log(index, number);
});
```

## 9.2 `map()`

배열의 각 요소들 변환(처리)한 값으로 구성된 새로운 배열을 반환한다.

```javascript
const numbers = [1, 2, 3, 4, 5];
const doubled = numbers.map(number => number * 2); // numbers의 값들을 두배한 배열을 만든다.

console.log(doubled); // [2, 4, 6, 8, 10]
```

객체 배열에서도 자주 사용한다.

```javascript
const users = [
  { id: 1, name: "홍길동" },
  { id: 2, name: "이순신" },
];

const names = users.map(user => user.name); // 각 user의 이름을 배열로 모아서 반환한다.

console.log(names); // ["홍길동", "이순신"]
```

## 9.3 `filter()`

배열의 각 요소들 중 조건을 만족하는 것들만 모아 새로운 배열을 만든다.

```javascript
const numbers = [1, 2, 3, 4, 5];
const evenNumbers = numbers.filter(number => number % 2 === 0);

console.log(evenNumbers); // [2, 4]
```

```javascript
const users = [
  { id: 1, name: "홍길동", active: true },
  { id: 2, name: "이순신", active: false },
];

const activeUsers = users.filter(user => user.active);
```

## 9.4 `find()`

조건을 만족하는 첫 번째 요소를 반환한다. 찾지 못하면 `undefined`를 반환한다.

```javascript
const users = [
  { id: 1, name: "홍길동" },
  { id: 2, name: "이순신" },
];

const user = users.find(item => item.id === 2);

console.log(user);
```

## 9.5 `findIndex()`

조건을 만족하는 첫 번째 요소의 인덱스를 반환한다. 찾지 못하면 `-1`을 반환한다.

```javascript
const numbers = [10, 20, 30];
const index = numbers.findIndex(number => number === 20);

console.log(index); // 1
```

## 9.6 `some()`

조건을 만족하는 요소가 하나라도 있으면 `true`를 반환한다.

```javascript
const scores = [70, 80, 95];

const hasExcellentScore = scores.some(score => score >= 90);

console.log(hasExcellentScore); // true
```

## 9.7 `every()`

모든 요소가 조건을 만족하면 `true`를 반환한다.

```javascript
const scores = [70, 80, 95];

const allPassed = scores.every(score => score >= 60);

console.log(allPassed); // true
```

## 9.8 `reduce()`
`reduce(callback, 누적시작값)`
배열의 여러 값을 하나의 값으로 누적한다.
callback 함수는 파라미터로 **누적값**과 **현재값**를 받는다.

```javascript
const numbers = [10, 20, 30];

const total = numbers.reduce((sum, number) => {
  return sum + number;
}, 0);

console.log(total); // 60
```

두 번째 인수인 `0`은 누적값의 초기값이다.

| 반복 | `sum` | `number` | 반환값 |
|---|---:|---:|---:|
| 1회 | 0 | 10 | 10 |
| 2회 | 10 | 20 | 30 |
| 3회 | 30 | 30 | 60 |

## 9.9 메서드 연결 (Method Chaining)

위에서 살펴본 여러 배열 메서드는 이어서 사용할 수 있다. 이를 메서드 체이닝(Method Chaining)이라고 하며, **여러 작업을 하나의 표현식**으로 처리할 수 있다.

```javascript
const users = [
  { name: "홍길동", age: 20, active: true },
  { name: "이순신", age: 17, active: true },
  { name: "강감찬", age: 30, active: false },
];

const names = users
  .filter(user => user.active)
  .filter(user => user.age >= 19)
  .map(user => user.name);

console.log(names); // ["홍길동"]
```

---

# 10. 객체

**객체(Object)**는 관련된 여러 값을 이름(속성-Property)과 값(Value)의 쌍으로 묶어 저장하는 자료형이다. 배열이 숫자 인덱스로 요소에 접근하는 반면, 객체는 속성 이름을 사용하여 데이터에 접근한다.

```javascript
const person = {
  name: "홍길동",
  age: 20,
  address: "서울",
};
```

## 10.1 속성 접근

점 표기법을 사용할 수 있다.

```javascript
console.log(person.name);
person.age = 21;
```

대괄호 표기법도 사용할 수 있다. 이 경우 속성명은 문자열로 지정한다.

```javascript
console.log(person["name"]);
person["age"] = 22;
```

속성 이름이 변수에 저장되어 있으면 대괄호 표기법을 사용한다.

```javascript
const key = "address";

console.log(person[key]);
```

## 10.2 메서드

객체 **속성에 함수를 저장**하면 메서드가 된다.

```javascript
const person = {
  name: "홍길동",

  introduce() {
    console.log(`저는 ${this.name}입니다.`);
  },
};

person.introduce();
```

## 10.3 속성 단축 문법

속성에 값으로 넣을 변수 이름과 속성 이름이 같으면 값을 생략할 수 있다.

```javascript
const name = "홍길동";
const age = 20;

const user = {
  name,
  age,
};

console.log(user);
```

## 10.4 객체 관련 메서드

```javascript
const user = {
  name: "홍길동",
  age: 20,
};
```

**속성명들 조회**

```javascript
console.log(Object.keys(user));
// ["name", "age"]
```
**속성값들 조회**

```javascript
console.log(Object.values(user));
// ["홍길동", 20]
```
**속성의 이름과 값을 배열로 조회**

```javascript
console.log(Object.entries(user));
// [["name", "홍길동"], ["age", 20]]
```

```javascript
for (const [key, value] of Object.entries(user)) {
  console.log(key, value);
}
```

## 10.5 `this`

객체의 메서드 안에서 `this`는 일반적으로 메서드를 호출한 객체를 가리킨다.  예를들어 `person.greet()` 호출 했을 때 `greet()` 메소드 안에서의 `this`는 메소드를 호출한 객체인 `person`을 가리킨다.
this를 사용하면 같은 객체의 속성과 메서드에 접근할 수 있다. 단, this는 함수가 정의된 위치가 아니라 함수가 호출된 방식에 따라 결정된다.

```javascript
const user = {
  name: "홍길동",

  introduce() {
    console.log(this.name);
  },
};

user.introduce();
```

화살표 함수는 자신만의 `this`를 만들지 않는다.

```javascript
const user = {
  name: "홍길동",

  introduce: () => {
    console.log(this.name);
  },
};

user.introduce(); // undefined
```

따라서 객체의 메서드에서 `this`를 사용할 때는 일반 메서드 문법을 사용하는 것이 자연스럽다.


---

# 11. 구조 분해 할당(Destructuring Assignment)

구조 분해 할당은 배열이나 객체의 값을 여러 변수에 나누어 저장하는 문법이다.

## 11.1 배열 구조 분해

```javascript
const colors = ["red", "green", "blue"];

const [first, second, third] = colors;

console.log(first);  // "red"
console.log(second); // "green"
console.log(third); // "blue"
```

일부 값은 건너뛸 수 있다.

```javascript
const numbers = [10, 20, 30];

const [first1, second] = numbers
const [first2, , third] = numbers;

console.log(first1, first2, second, third);
```

기본값을 지정할 수 있다.

```javascript
const values = [10];

const [a, b = 0] = values;

console.log(a, b); // 10, 0
```

나머지 값을 배열로 받을 수 있다.

```javascript
const numbers = [1, 2, 3, 4, 5];

const [first, second, ...rest] = numbers;

console.log(rest); // [3, 4, 5]
```

## 11.2 객체 구조 분해

속성과 같은 이름의 변수에 값을 대입한다.

```javascript
const user = {
  name: "홍길동",
  age: 20,
  address: "서울"
};

const { name, age } = user;  // name 속성은 name변수에 age속성은 age 변수에 대입 된다.

console.log(name, age);
```

다른 변수 이름으로 받을 수 있다.

```javascript
const { name: userName, age: userAge } = user;

console.log(userName, userAge);
```

기본값 지정할 수 있다.

```javascript
const user = {
  name: "홍길동",
};

const { name, age = 0 } = user;
```

## 11.3 함수 매개변수에서 구조 분해

**배열 구조 분해**
```javascript
function printElement([a,b]) {
  console.log(a, b);
}

printElement([10, 20, 30]);
```

**객체 구조 분해**
```javascript
function printUser({ name, age }) {
  console.log(`${name}, ${age}세`);
}

const user = {
  name: "홍길동",
  age: 20,
};

printUser(user);
```

---

# 12. 나머지 매개변수(Rest Parameter)와 전개(Spread)

나머지 매개변수와 전개 문법은 모두 마침표 세 개 `...`를 사용한다.

## 12.1 나머지 매개변수(rest parameter)

함수에 전달된 여러 값을 배열로 모은다.

```javascript
function sum(first, second, ...rest) {
  console.log(first);
  console.log(second);
  console.log(rest);
}

sum(10, 20, 30, 40, 50);
```

실행 결과:

```text
10
20
[30, 40, 50]
```

나머지 매개변수는 마지막 매개변수에 한 번만 사용할 수 있다.

## 12.2 배열 전개 (spread)

배열 전개(spread)는 배열의 요소들을 하나씩 꺼내어 개별 값처럼 펼쳐 사용하는 문법이다.

```javascript
const numbers = [1, 2, 3];
const copied = [100, 200, ...numbers];

console.log(copied);
```

배열을 합칠 때 사용할 수 있다.

```javascript
const a = [1, 2];
const b = [3, 4];

const result = [...a, ...b];

console.log(result); // [1, 2, 3, 4]
```

나머지 매개변수(rest parameter)를 받는 함수 호출에 배열의 값을 펼쳐서 전달할 때 사용할 수 있다.

```javascript
const numbers = [10, 20, 30];

console.log(Math.max(...numbers)); // 30
```

## 12.3 객체 전개

객체의 속성을 새 객체에 복사한다. 이를 이용해 원본을 변경하지 않고 요소들을 

```javascript
const user = {
  name: "홍길동",
  age: 20,
};

const copiedUser = {
  ...user,
  address: "서울"
};

console.log(copiedUser); // { name: '홍길동', age: 20, address: '서울' }
```

---

# 13. 예외 처리와 JSON

## 13.1 `try...catch`

실행 중 발생할 수 있는 오류를 처리한다. 
오류 발생 가능성 있는 코드는 try block에 작성한다. 오류가 발생했을 때 처리할 구문은 catch block에 작성한다. 

```javascript
try {
  const result = JSON.parse("잘못된 JSON");
  console.log(result);
} catch (error) {
  console.error("JSON 변환에 실패했습니다.");
  console.error(error.message);
}
```

## 13.2 `finally`

오류 발생 여부와 관계없이 실행할 코드를 작성한다.

```javascript
try {
  console.log("작업 시작");
} catch (error) {
  console.error(error);
} finally {
  console.log("작업 종료");
}
```

## 13.3 오류 발생시키기

함수나 메서드에서 정상적으로 작업을 계속할 수 없는 상황이 발생하면 `throw`문을 사용하여 오류를 발생시킬 수 있다. 발생한 오류는 함수를 호출한 쪽으로 전달되며, 호출한 곳에서는 `try...catch`문을 사용하여 이를 처리할 수 있다.

```javascript
function divide(a, b) {
  if (b === 0) {
    throw new Error("0으로 나눌 수 없습니다.");
  }

  return a / b;
}

// Caller
try {
  const result = divide(10, 0);
  console.log(result);
} catch (error) {
  console.log(error.message);
}
```

---

# 14. 모듈

모듈(Module)은 JavaScript 코드를 파일 단위로 나누어 관리하는 방식이다. 하나의 파일에 모든 코드를 작성하지 않고, 기능이나 역할에 따라 여러 파일로 분리한 뒤 필요한 코드를 내보내고 가져와 사용할 수 있다.

모듈을 사용하면 다음과 같은 장점이 있다.

- 관련된 코드를 파일별로 분리할 수 있다.
- 다른 파일에서 동일한 코드를 재사용할 수 있다.
- 변수와 함수의 이름이 다른 파일의 코드와 충돌하는 것을 줄일 수 있다.
- 프로그램의 구조를 파악하고 유지보수하기 쉬워진다.

JavaScript의 표준 모듈 시스템을 **ES Modules(ESM)**라고 한다. **ES Modules에서는 `export` 키워드로 값을 내보내고, `import` 키워드로 다른 파일의 값을 가져온다.**

React와 Vue.js 같은 프런트엔드 라이브러리들도 일반적으로 모듈을 기본으로 사용한다. 컴포넌트, 함수, 객체 등을 각각의 파일로 분리한 뒤 필요한 곳에서 가져와 조합하는 방식으로 애플리케이션을 구성한다.

## 14.1 이름 있는 내보내기 (Named Export)

**이름 있는 내보내기**는 변수, 함수, 클래스 등을 지정된 이름으로 내보내는 방식이다. 한 파일에서 여러 개의 값을 이름 있는 내보내기로 내보낼 수 있다.

```javascript
// math.js
export function add(a, b) {
  return a + b;
}

export const PI = 3.141592;
```
- 위 코드에서 `math.js` 파일은 `add` 함수와 `PI` 상수를 각각의 이름으로 내보낸다.

**다른 파일에서 이름 있는 내보내기를 가져올 때는 중괄호 `{}`를 사용한다.**

```javascript
// main.js
import { add, PI } from "./math.js";

console.log(add(10, 20));
console.log(PI);
```


**가져올 때는 내보낸 이름과 같은 이름을 사용해야 한다.**

```javascript
import { add, PI } from "./math.js";
```

**필요한 값만 선택하여 가져오기**

```javascript
import { add } from "./math.js";
```

**이름 있는 내보내기를 할 때 선언과 내보내기를 분리**하여 작성할 수도 있다.

```javascript
// math.js
function add(a, b) {
  return a + b;
}

function subtract(a, b) {
  return a - b;
}

const PI = 3.141592;

export { add, subtract, PI };
```

**이름을 바꾸어 가져오기**. `as` 키워드를 사용한다.

```javascript
import { add as sum } from "./math.js";

console.log(sum(10, 20));
```

- 위 코드에서는 `math.js`가 내보낸 `add` 함수를 현재 파일에서 `sum`이라는 이름으로 사용한다.

**내보내는 쪽에서 이름을 변경**

```javascript
function add(a, b) {
  return a + b;
}

export { add as sum };
```

- 이 경우 가져오는 파일에서는 변경된 이름인 `sum`을 사용해 가져 온다.

```javascript
import { sum } from "./math.js";
```

이름 있는 내보내기는 한 파일에서 여러 값을 제공할 때 적합하다.

## 14.2 기본 내보내기

**기본 내보내기(Default Export)**는 파일의 대표 값을 하나 지정하여 내보내는 방식이다. 한 모듈에서는 **기본 내보내기를 하나**만 사용할 수 있다.

```javascript
// User.js
export default class User {
  constructor(name) {
    this.name = name;
  }
}
```

**기본 내보내기 가져오기**

```javascript
import User from "./User.js";

const user = new User("Kim");
console.log(user.name);
```
- `{ }` 를 사용하지 않는다. 위 코드는 기본 내보내기로 export된 것을 `User`라는 이름으로 사용하겠다는 의미이다.
  
기본 내보내기는 **가져오는 쪽에서 이름을 자유롭게** 정할 수 있다.

```javascript
import Member from "./User.js";

const member = new Member("Lee");
```

- `User.js`에서는 `User`라는 이름으로 클래스를 작성했지만, 가져오는 파일에서는 `Member`라는 이름으로 사용할 수 있다.

기본 내보내기도 **선언과 분리하여 작성**할 수 있다.

```javascript
// User.js
class User {
  constructor(name) {
    this.name = name;
  }
}

export default User;
```

**함수나 객체도 기본값으로 내보낼 수 있다.**

```javascript
// logger.js
export default function log(message) {
  console.log(message);
}
```

```javascript
// config.js
const config = {
  apiUrl: "https://example.com",
  timeout: 3000,
};

export default config;
```

**하나의 파일에서는 이름 있는 내보내기와 기본 내보내기를 함께 사용**할 수도 있다.

```javascript
// math.js
export default function add(a, b) {
  return a + b;
}

export const PI = 3.141592;
```

가져올 때는 **기본 내보내기를 중괄호 밖에 작성하고, 이름 있는 내보내기를 중괄호 안**에 작성한다.

```javascript
import add, { PI } from "./math.js";

console.log(add(10, 20));
console.log(PI);
```

> 기본 내보내기는 파일의 대표 기능이나 대표 객체를 내보낼 때 주로 사용한다. 이름 있는 내보내기는 한 파일에서 여러 기능을 제공할 때 적합하다.

## 14.3 브라우저에서 모듈 사용하기

브라우저에서 JavaScript 모듈을 사용하려면 `<script>` 태그의 `type` 속성을 `"module"`로 지정한다.

```html
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <title>모듈 예제</title>
</head>
<body>
  <script type="module">
    import { add } from "./math.js";

    console.log(add(10, 20));
  </script>
</body>
</html>
```


### 외부 스크립트에서 모듈 사용하기

HTML에서는 `<script type="module">`을 사용하여 시작 모듈인 JavaScript 파일을 불러올 수 있다.

```html
<!-- index.html -->
<button id="calculate">계산</button>
<p id="result"></p>

<script type="module" src="./main.js"></script>
```

`main.js`는 일반적으로 애플리케이션의 시작 모듈로 사용된다. HTML의 DOM 요소를 가져와 이벤트를 연결하고 화면을 변경하며, 다른 모듈에서 가져온 함수나 클래스를 조합하여 프로그램의 전체 동작을 실행한다.

```javascript
// main.js
import { add } from "./math.js";

const button = document.querySelector("#calculate");
const result = document.querySelector("#result");

button.addEventListener("click", () => {
  result.textContent = add(10, 20);
});
```

```javascript
// math.js
export function add(a, b) {
  return a + b;
}
```

HTML은 `main.js`만 불러오며, `main.js`가 필요한 다른 모듈을 `import`하면 브라우저가 해당 파일도 자동으로 불러온다.

/*
  =============================================
  4. 데이터 타입
  =============================================
  JavaScript의 데이터는 크게 원시 타입(Primitive Type)과
  객체 타입(Object Type)으로 나뉜다.
*/

/*
  ---------------------------------------------
  4.1 원시 타입(Primitive Type)
  ---------------------------------------------
  | 타입      | 설명                                        | 예                  |
  |-----------|---------------------------------------------|--------------------|
  | string    | 문자열                                      | "hello"             |
  | number    | 숫자(정수, 실수)                             | 10, 3.14           |
  | bigint    | 매우 큰 정수 (number 범위를 넘어선 정수       | 9007199254740998n  |
  |           | (±9007199254740991) 표현)                   |                     |
  | boolean   | 논리값                                      | true, false         |
  | undefined | 값이 아직 정해지지 않음                      | undefined           |
  | null      | 값이 없음을 의도적으로 표현                  | null                |
  | symbol    | 고유한 식별값                                | Symbol("id")        |
*/

/*
  ---------------------------------------------
  4.2 문자열(string)
  ---------------------------------------------
  문자열 값은 작은따옴표, 큰따옴표 또는 백틱으로 감싸준다.
*/
{
  const message1 = "안녕하세요.";
  const message2 = 'JavaScript입니다.';
}

/* 백틱 문자열은 여러 줄 문자열과 템플릿 문자열을 만들 때 사용한다. */
{
  const name = "홍길동";
  const age = 20;

  const message = `이름: ${name}
나이: ${age}
반갑습니다.`;

  console.log(message);
}

/* ${ } 안에는 계산식도 작성할 수 있다. */
{
  const price = 10000;
  const quantity = 3;

  console.log(`총액: ${price * quantity}원`);
}

/*
  ---------------------------------------------
  4.3 숫자(number)
  ---------------------------------------------
  JavaScript의 정수와 실수는 모두 number 타입이다.
*/
{
  // const age = 20;
  // const height = 175.5;
}

/* 계산할 수 없는 숫자 결과는 NaN으로 나타난다. */
{
  const result = Number("hello");  // 전달된 문자열을 number로 변환
  console.log(result); // NaN
}

/*
  ---------------------------------------------
  4.4 null과 undefined
  ---------------------------------------------
  undefined는 값이 아직 할당되지 않은 상태를 나타낸다.
*/
{
  let userName;
  console.log(userName); // undefined
}

/* null은 개발자가 값이 없음을 의도적으로 표시할 때 사용한다. */
{
  // const selectedUser = null;
}

/*
  ---------------------------------------------
  4.5 객체 타입
  ---------------------------------------------
  객체는 여러 값을 하나로 묶어 관리한다.
*/
{
  // const user = {
  //   name: "홍길동",
  //   age: 20,
  // };
}

/* 배열과 함수도 객체의 한 종류이다. */
{
  // const numbers = [10, 20, 30];

  // function add(a, b) {
  //   return a + b;
  // }
}

/*
  ---------------------------------------------
  4.6 typeof
  ---------------------------------------------
  typeof 연산자는 값의 타입을 문자열로 반환한다.
*/
{
  console.log(typeof "hello");    // "string"
  console.log(typeof 20);         // "number"
  console.log(typeof true);       // "boolean"
  console.log(typeof undefined);  // "undefined"
  console.log(typeof {});         // "object"
  console.log(typeof []);         // "object"
  console.log(typeof function(){}); // "function"
}

/*
  null과 배열의 타입은 "object"로 반환한다.

  > null이 "object"인 것은 JavaScript 초기 설계에서 생긴 특수한 동작이다.
  > null이 실제 객체라는 뜻은 아니다.
*/

/* 배열인지 여부를 확인할 때는 Array.isArray()를 사용한다. */

console.log(Array.isArray([1, 2, 3])); // true

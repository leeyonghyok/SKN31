/*
  =============================================
  5. 연산자와 형 변환
  =============================================
*/

/*
  ---------------------------------------------
  5.1 산술 연산자
  ---------------------------------------------
*/
{
  // const a = 10;
  // const b = 3;

  // console.log(a + b); // 덧셈.
  // console.log(a - b); // 뺄셈.
  // console.log(a * b); // 곱셈.
  // console.log(a / b); // 나눗셈. 3.333...
  // console.log(a % b); // 나머지 연산(모듈러스 연산)1
  // console.log(a ** b); // 제곱연산.
}

/*
  ---------------------------------------------
  5.2 대입 연산자
  ---------------------------------------------
*/
{
  let score = 10;

  // 복합 대입 연산자
  // score += 5; // score = score + 5
  // console.log(score);

  // score -= 2;
  // console.log(score);

  // score *= 3;
  // console.log(score);

  // score /= 2;
  // console.log(score);
}

/*
  ---------------------------------------------
  5.3 증가와 감소 연산자
  ---------------------------------------------
  변수가 가진 값을 1 증가, 감소 시킨다.
*/
{
  // let count = 10;

  // count++; // count += 1
  // console.log(count);

  // count--; // count -= 1
  // console.log(count);
}

/*
  증감 연산자는 변수 앞(전위 연산)과 뒤(후위 연산)에 붙일 수 있다.
  전위 연산(++x)과 후위 연산(x++)은 다른 연산과 같이 사용될 때 값을 반환하는 시점이 다르다.
*/
{
  // let a = 10;
  // let b = a++; // 대입 연산을 먼저한다.

  // console.log(a, b); // 11, 10
}

{
  // let x = 10;
  // let y = ++x; // 증가 연산을 먼저 한다.

  // console.log(x, y); // 11, 11
}

/*
  ---------------------------------------------
  5.4 비교 연산자
  ---------------------------------------------
*/

/* [크기 비교] */
{
  // console.log(10 > 5);   // true
  // console.log(10 >= 10); // true
  // console.log(5 < 3);    // false
  // console.log(5 <= 5);   // true
}

/* [동등 비교]는 ===와 !==를 사용한다. */
{
  // console.log(10 === 10);   // true
  // console.log(10 === "10"); // false
  // console.log(10 !== "10"); // true
}
/*
  ==와 != 는 비교하기 전에 타입을 자동으로 변환한다.
  그래서 타입이 다르더라도 값이 같으면 true가 된다.
*/
// console.log(10 == "10"); // true

/* 타입 변환으로 인한 혼동을 줄이기 위해 일반적으로 ===, !==를 사용한다. */

/*
  ---------------------------------------------
  5.5 truthy와 falsy
  ---------------------------------------------
  Truthy(참 같은 값)와 Falsy(거짓 같은 값)는 참(true)이나 거짓(false)을 뜻하는 불리언(Boolean) 데이터가 아니더라도, 조건문 등에서 참이나 거짓처럼 취급되는 값을 말한다.
  JavaScript의 조건식에서는 모든 타입의 값이 참 또는 거짓으로 변환된다.
  대표적인 falsy 값은 다음과 같다. (falsy가 아닌 값들은 다 truthy 이다.)

  false
  0
  -0
  0n
  ""  // 빈문자열
  null
  undefined
  NaN
*/

/* 이 값을 제외한 값은 truthy이다. */
if ("hello") {
  // console.log("실행됩니다.");
}

/*
  ---------------------------------------------
  5.6 논리 연산자
  ---------------------------------------------
  JavaScript의 논리 AND(&&)와 OR(||) 연산자는 boolean 값뿐만 아니라 피연산자 자체를 반환할 수도 있다.
*/

/*
  [&& (논리 AND 연산자)]
  왼쪽 값이 falsy면 왼쪽 값을 반환한다. 왼쪽 값이 truthy면 오른쪽 값을 반환한다.
*/
console.log(false && "실행"); // false
console.log(true && "실행");  // "실행"
console.log("" && 100);        // ""
console.log("hello" && 100);   // 100

/*
  [|| (논리 OR 연산자)]
  왼쪽 값이 truthy면 왼쪽 값을 반환한다. 왼쪽 값이 falsy면 오른쪽 값을 반환한다.
*/
console.log("값" || "기본값"); // "값"
console.log("" || "기본값");   // "기본값"

/*
  [! (논리 NOT 연산자)]
  논리값을 반대로 바꾼다.
*/
console.log(!true);  // false
console.log(!false); // true

/*
  ---------------------------------------------
  5.7 삼항 연산자
  ---------------------------------------------
  삼항 연산자는 조건에 따라 두 값 중 하나를 선택한다.
  조건식 ? value1 : value2
*/
{
  const age = 10;
  const result = age >= 19 ? "성인" : "미성년자";

  console.log(result);
}

/*
  ---------------------------------------------
  5.8 형 변환
  ---------------------------------------------
  | 변환 대상 | 함수 또는 표현              |
  |-----------|-----------------------------|
  | 문자열    | String(value), value+""     |
  | 숫자      | Number(value)               |
  | 불리언    | Boolean(value)              |
  | 정수 해석 | parseInt(value, radix)      |
  | 실수 해석 | parseFloat(value)           |
  | 큰 정수   | BigInt(value)               |
*/

/* 문자열을 숫자로 바꿀 때는 Number()를 사용할 수 있다. */
{
  // console.log(Number("123"));        // 123
  // console.log(Number("12.5"));       // 12.5
  // console.log(Number(""));           // 0
  // console.log(Number(true));         // 1
  // console.log(Number(false));        // 0
  // console.log(Number(null));         // 0
  // console.log(Number("hello"));      // NaN
  // console.log(Number(undefined));    // NaN
}

/* 문자열을 정수와 실수로 해석 */
{
  // console.log(parseInt("123px", 10) + 20);  // 123 // 문자열의 왼쪽부터 숫자로 해석할 수 있는 부분까지 읽어 정수로 변환한다. 두 번째 인수 10은 문자열을 10진수로 해석하라는 의미이다.
  // console.log(parseInt("12.9", 10));  // 12
  // console.log(parseInt("101", 2));    // 5 // 문자열을 2진수로 해석하라는 의미이다.
  // console.log(parseInt("hello"));   // NaN

  console.log(parseFloat("12.9"));   // 12.9
  console.log(parseFloat("3.14kg")); // 3.14
  console.log(parseFloat("hello"));   // NaN
}

/*
  - parseInt()의 두번째 인수는 진법이다.
  - Number()는 문자열 전체가 올바른 숫자여야 하지만,
    parseInt(), parseFloat은 앞부분부터 정수로 해석할 수 있는 부분까지만 읽는다.
*/

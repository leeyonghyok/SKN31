/*
  =============================================
  9. 배열 고차 함수
  =============================================
  배열 고차 함수는 함수를 인수로 받아 각 요소를 처리한다.
  > 고차함수: 함수를 인수로 받는 함수.
  > 고차함수에 전달되는 함수를 Callback 함수 라고 한다.
*/

/*
  ---------------------------------------------
  9.1 forEach()
  ---------------------------------------------
  배열의 각 요소의 값과 index를 받아서 처리하는 함수를 실행한다.
*/
{
  const numbers = [10, 20, 30];

  //forEach()에 전달되는 함수는 파라미터로 배열의 개별 요소와 index를 받는다.
  // numbers.forEach((number, index) => {
  //   console.log(index, number);
  // });
  // for (const num of numbers) {
  //   console.log(num);
  // }
}

/*
  ---------------------------------------------
  9.2 map()
  ---------------------------------------------
  배열의 각 요소들 변환(처리)한 값으로 구성된 새로운 배열을 반환한다.
*/
{
  // const numbers = [1, 2, 3, 4, 5];
  // const doubled = numbers.map(number => number * 2); // numbers의 값들을 두배한 배열을 만든다.

  // console.log(doubled); // [2, 4, 6, 8, 10]
}

/* 객체 배열에서도 자주 사용한다. */
{
  // const users = [
  //   { id: 1, name: "홍길동" },
  //   { id: 2, name: "이순신" },
  // ];

  // const names = users.map(user => user.name); // 각 user의 이름을 배열로 모아서 반환한다.
  // console.log(names); // ["홍길동", "이순신"]
}

/*
  ---------------------------------------------
  9.3 filter()
  ---------------------------------------------
  배열의 각 요소들 중 조건을 만족하는 것들만 모아 새로운 배열을 만든다.
*/
{
  // const numbers = [1, 2, 3, 4, 5];
  // const evenNumbers = numbers.filter(number => number % 2 === 0);

  // console.log(evenNumbers); // [2, 4]
}

{
  // const users = [
  //   { id: 1, name: "홍길동", active: true },
  //   { id: 2, name: "이순신", active: false },
  // ];

  // const activeUsers = users.filter(user => user.active);
  // console.log(activeUsers);
}

/*
  ---------------------------------------------
  9.4 find()
  ---------------------------------------------
  조건을 만족하는 첫 번째 요소를 반환한다. 찾지 못하면 undefined를 반환한다.
*/
{
  // const users = [
  //   { id: 1, name: "홍길동" },
  //   { id: 2, name: "이순신" },
  //   { id: 3, name: "이순신" },
  //   { id: 4, name: "이순신" }
  // ];

  // const user = users.find(item => item.name === "이순신");
  // // const user = users.filter(item => item.name === "이순신");

  // console.log(user);
}

/*
  ---------------------------------------------
  9.5 findIndex()
  ---------------------------------------------
  조건을 만족하는 첫 번째 요소의 인덱스를 반환한다. 찾지 못하면 -1을 반환한다.
*/
{
  // const numbers = [10, 20, 30, 20, 20, 20];
  // const index = numbers.findIndex(number => number === 20);

  // console.log(index); // 1
}

/*
  ---------------------------------------------
  9.6 some()
  ---------------------------------------------
  조건을 만족하는 요소가 하나라도 있으면 true를 반환한다.
*/
{
  const scores = [70, 80, 95];

  const hasExcellentScore = scores.some(score => score >= 90);

  console.log(hasExcellentScore); // true
}

/*
  ---------------------------------------------
  9.7 every()
  ---------------------------------------------
  모든 요소가 조건을 만족하면 true를 반환한다.
*/
{
  const scores = [70, 80, 95];

  const allPassed = scores.every(score => score >= 80);

  console.log(allPassed); // true
}

/*
  ---------------------------------------------
  9.8 reduce()
  ---------------------------------------------
  reduce(callback, 누적시작값)
  배열의 여러 값을 하나의 값으로 누적한다.
  callback 함수는 파라미터로 누적값과 현재값를 받는다.
*/
{
  const numbers = [10, 20, 30];

  let total1 = 0;

  for (const number of numbers) {
    total1 += number;
  }
  console.log(total1);


  const total = numbers.reduce((sum, number) => {
    return sum + number;
  }, 0);

  console.log(total); // 60
}
/*
  두 번째 인수인 0은 누적값의 초기값이다.
*/

/*
  ---------------------------------------------
  9.9 메서드 연결 (Method Chaining)
  ---------------------------------------------
  위에서 살펴본 여러 배열 메서드는 이어서 사용할 수 있다.
  이를 메서드 체이닝(Method Chaining)이라고 하며,
  여러 작업을 하나의 표현식으로 처리할 수 있다.
*/
{
  const users = [
    { name: "홍길동", age: 20, active: true },
    { name: "이순신", age: 17, active: true },
    { name: "강감찬", age: 30, active: false },
  ];
  // users의 사용자들중에서 "활성상태(active=true)"이고
  // 나이가 19세 이상인 사용자의 이름들을 조회.
  const names = users
    .filter(user => user.active)
    .filter(user => user.age >= 19)
    .map(user => user.name);

  console.log(names); // ["홍길동"]
}

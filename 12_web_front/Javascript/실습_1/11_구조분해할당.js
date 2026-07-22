/*
  =============================================
  11. 구조 분해 할당(Destructuring Assignment)
  =============================================
  구조 분해 할당은 배열이나 객체의 값을 여러 변수에 나누어 저장하는 문법이다.
*/

/*
  ---------------------------------------------
  11.1 배열 구조 분해
  ---------------------------------------------
*/
{
  // const colors = ["red", "green", "blue"];

  // const [first, second, third] = colors;

  // console.log(first);  // "red"
  // console.log(second); // "green"
  // console.log(third); // "blue"
}

/* 일부 값은 건너뛸 수 있다. */
{
  // const numbers = [10, 20, 30];

  // const [first1, second] = numbers
  // const [first2, , third] = numbers;

  // console.log(first1, first2, second, third);
}

/* 기본값을 지정할 수 있다. */
{
  // const values = [10];

  // // const [a, b = 0] = values;
  //   const [a, b] = values;

  // console.log(a, b); // 10, 0
}

/* 나머지 값을 배열로 받을 수 있다. */
{
  // const numbers = [1, 2, 3, 4, 5];

  // const [first, second, ...rest] = numbers;

  // console.log(first, second);
  // console.log(rest); // [3, 4, 5]
}

/*
  ---------------------------------------------
  11.2 객체 구조 분해
  ---------------------------------------------
  속성과 같은 이름의 변수에 값을 대입한다.
*/
{
  // const user = {
  //   name: "홍길동",
  //   age: 20,
  //   address: "서울"
  // };
  // const { name, age } = user;  // name 속성은 name변수에 age속성은 age 변수에 대입 된다.

  // console.log(name, age);

  // /* 다른 변수 이름으로 받을 수 있다. */
  // const { name: userName, age: userAge } = user;
  // // name: userName - name 속성의 값을 userName 변수에 대입.
  // console.log(userName, userAge);
}

/* 기본값 지정할 수 있다. */
{
  // const user = {
  //   name: "홍길동",
  // };

  // const { name, age = 0} = user;
  // console.log(name, age);
}

/*
  ---------------------------------------------
  11.3 함수 매개변수에서 구조 분해
  ---------------------------------------------
*/

/* [배열 구조 분해] */
{
  function printElement([a,b]) {
    console.log(a, b);
  }

  printElement([10, 20, 30]);
}

/* [객체 구조 분해] */
{
  function printUser({ name, age }) {
    console.log(`${name}, ${age}세`);
  }

  const user = {
    name: "홍길동",
    age: 20,
  };

  printUser(user);
}

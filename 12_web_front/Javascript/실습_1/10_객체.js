/*
  =============================================
  10. 객체
  =============================================
  객체(Object)는 관련된 여러 값을 이름(속성-Property)과 값(Value)의 쌍으로
  묶어 저장하는 자료형이다. 배열이 숫자 인덱스로 요소에 접근하는 반면,
  객체는 속성 이름을 사용하여 데이터에 접근한다.
*/

// const person = {
//   name: "홍길동",
//   age: 20,
//   address: "서울",
// };

/*
  ---------------------------------------------
  10.1 속성 접근
  ---------------------------------------------
*/

/* 점 표기법을 사용할 수 있다. */
// console.log(person.name);
// person.age = 21;
// console.log(person);

/* 대괄호 표기법도 사용할 수 있다. 이 경우 속성명은 문자열로 지정한다. */
// console.log(person["name"]);
// person["age"] = 22;
// console.log(person);
// const age = "name";
// console.log(person[age]); 
// age변수의 값을 property 이름으로 넣어서 조회


/* 속성 이름이 변수에 저장되어 있으면 대괄호 표기법을 사용한다. */
{
  // const key = "address";
  // console.log(person[key]);
}

/*
  ---------------------------------------------
  10.2 메서드
  ---------------------------------------------
  객체 속성에 함수를 저장하면 메서드가 된다.
*/
{
  // const person = {
  //   name: "홍길동",

  //   introduce() {
  //   // introduce: function() {
  //     console.log(`저는 ${this.name}입니다.`);
  //   },
  // };

  // person.introduce();
}

/*
  ---------------------------------------------
  10.3 속성 단축 문법
  ---------------------------------------------
  속성에 값으로 넣을 변수 이름과 속성 이름이 같으면 값을 생략할 수 있다.
*/
{
  // const name = "홍길동";
  // const age = 20;

  // const user = {
  //   name, // name: name,
  //   age,
  // };

  // console.log(user);
}

/*
  ---------------------------------------------
  10.4 객체 관련 메서드
  ---------------------------------------------
*/
{
  const user = {
    name: "홍길동",
    age: 20,
  };

  /* [속성명들 조회] */
  // console.log(Object.keys(user));
  // ["name", "age"]

  /* [속성값들 조회] */
  // console.log(Object.values(user));
  // ["홍길동", 20]

  /* [속성의 이름과 값을 배열로 조회] */
  // console.log(Object.entries(user));
  // [["name", "홍길동"], ["age", 20]]

  // for (const [key, value] of Object.entries(user)) {
  //   console.log(key, value);
  // }

  // for (const key in user) {
  //   console.log(key, user[key]);
  // }
}

/*
  ---------------------------------------------
  10.5 this
  ---------------------------------------------
  객체의 메서드 안에서 this는 일반적으로 메서드를 호출한 객체를 가리킨다.
  예를들어 person.greet() 호출 했을 때 greet() 메소드 안에서의 this는
  메소드를 호출한 객체인 person을 가리킨다.
  this를 사용하면 같은 객체의 속성과 메서드에 접근할 수 있다.
  단, this는 함수가 정의된 위치가 아니라 함수가 호출된 방식에 따라 결정된다.
*/
{
  // const user = {
  //   name: "홍길동",
  //   age: 20,
  //   introduce() {
  //     console.log(this.name, this.age); // this: user
  //     this.test()
  //   },
  //   test() {
  //     console.log("test");
  //   }
  // };

  // user.introduce();
}

/*
 화살표 함수는 자신만의 this를 만들지 않는다.
 따라서 객체의 메서드에서 this를 사용할 때는 일반 메서드 문법을 사용하는 것이 자연스럽다.
 */
{
  const user = {
    name: "홍길동",

    introduce: () => {
      console.log(this, this.name);
    },
  };

  user.introduce(); // undefined
}


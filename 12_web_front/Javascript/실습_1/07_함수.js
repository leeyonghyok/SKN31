/*
  =============================================
  7. 함수
  =============================================
  함수는 여러 명령문들을 하나의 작업 단위로 묶은 것이다.
  JavaScript의 함수는 변수에 저장하거나 다른 함수에 전달하고   함수의 결과로 반환할 수 있다. (First Class Citizen - 일급객체)
  Javascript는 함수를 정의 하는 다양한 방법이 있다.
*/

/*
  ---------------------------------------------
  7.1 함수 선언문
  ---------------------------------------------
*/
{
  // 함수 정의
  // function add(a, b) {
  //   return a + b;
  // }
  // // 함수 호출
  // const result = add(10, 20);

  // console.log(result); // 30
  // console.log(add(100, 2030));
}

/*
  ---------------------------------------------
  7.2 함수 표현식(Function Expression)
  ---------------------------------------------
  함수 표현식(Function Expression)은 함수를 하나의 값으로 만들어   변수에 저장하는 방식이다. 함수는 표현식의 결과로 생성되며,
  생성된 함수를 변수에 할당하여 사용한다.
  함수 표현식은 변수에 할당된 이후부터 사용할 수 있다.
*/
{
  // const add = function(a, b) {
  //   return a + b;
  // };

  // console.log(add(10, 20));
}

/*
  ---------------------------------------------
  7.3 화살표 함수(Arrow Function)
  ---------------------------------------------
  화살표 함수(Arrow Function)는 function 키워드 대신 => 기호를 사용하여   함수를 간결하게 작성하는 문법이다. 화살표 함수도 함수 표현식처럼
  생성된 함수를 변수에 저장하여 사용한다.
*/
// {
//   // (파라미터) => {실행구문}
//   const add = (a, b) => {
//     return a + b;
//   };
//   console.log(add(200, 300));
// }
// /* - (a, b) => { ... }는 화살표 함수이고, 생성된 함수 객체를 add 변수에 저장 */

// /* 함수 본문이 하나의 표현식이면 중괄호와 return을 생략할 수 있다. */
// {
//   const add = (a, b) => a + b;
//   console.log(add(220, 300));
// }

// /* 매개변수가 하나이면 괄호를 생략할 수 있다. */
// {
//   const double = number => number * 2;
//   console.log(double(200));
// }

// /* 매개변수가 없으면 빈 괄호(필수)를 작성한다. */
// {
//   const greet = () => console.log("안녕하세요.");
//   r = greet();
//   console.log(r);
// }

// /* 객체를 바로 반환할 때는 객체를 괄호로 감싼다. */
// {
//   const createUser = (name, age) => ({
//     name, //name:name key와 값을가진 변수가 같으면 key만지정.
//     age,
//   });
//   console.log(createUser("이순신", 33));
// }

/*
  ---------------------------------------------
  7.4 다양한 함수의 매개변수
  ---------------------------------------------
*/

/*
  [기본값이 있는 매개변수]
  호출할 때 인수를 전달하지 않으면 기본값을 사용할 수 있다.
*/
{
  // function greet(name = "무명") {
  //   return `안녕하세요, ${name}님`;
  // }

  // console.log(greet());
  // console.log(greet("홍길동"));
}

/*
  [나머지 매개변수(Rest Parameter)]
  전달된 여러 인수들을 하나의 배열로 받는다. 매개변수 앞에 ...을 붙인다.
*/
{
  // function sum(...numbers) {
  //function sum(a, b, c, ...numbers) {
  // function sum(...a, ...numbers) {
//     console.log(a, b, c);
//     console.log(numbers);
//   }

//   sum(1, 2, 3, 4, 5, 6, 7);
}

/*
  [구조 분해 할당(Destructuring Assignment)]
  전달 된 배열이나 객체에서 필요한 값을 꺼내 매개변수로 받는다.
*/
{
  function printPoint([x, y]) {
    console.log(x, y);
  }

  printPoint([10, 20]);
}

/*
  ---------------------------------------------
  7.5 콜백 함수
  ---------------------------------------------
  함수를 매개변수로 받거나 함수를 반환하는 함수를 고차함수 라고 한다.
  그리고 고차함수에 전달되는 함수를 콜백 함수(callback)라고 한다.
  JavaScript는 함수를 일급 객체로 취급하므로 고차 함수를 지원한다.
*/
{
  function repeat(count, callback) {
    for (let i = 0; i < count; i++) {
      callback(i);
    }
  }

  // repeat(5, console.log);
  repeat(100, x => {
    if (x % 10 === 0) {
      console.log(x);
    }
  })
  
}
/*
  - repeat: 고차 함수
  - console.log: 콜백 함수

  배열 메서드와 이벤트 처리에서 콜백 함수를 자주 사용한다.
*/

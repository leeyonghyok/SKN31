/*
  =============================================
  6. 제어문
  =============================================
  JavaScript의 조건문은 if문과 switch case문이 있다.
*/

/*
  ---------------------------------------------
  6.1 조건문
  ---------------------------------------------
*/

/*
  [if 문]
  조건식이 true이면 if 블록을 실행하고, false이면 실행하지 않는다.
  else if를 사용하면 여러 조건을 순서대로 검사할 수 있으며, 모든 조건이 거짓이면 else 블록을 실행한다.
  조건은 위에서 아래 순서대로 검사하며, 처음으로 true가 된 블록만 실행하고 나머지는 검사하지 않는다.
*/
{
  // const score = 65;

  // if (score >= 90) {
  //   console.log("A");
  // } else if (score >= 80) {
  //   console.log("B");
  // } else {
  //   console.log("C");
  // }
}

/* 조건식에는 비교식뿐 아니라 모든 값이 올 수 있다. */
{
  // const userName = "";

  // console.log(Boolean(userName));

  // if (userName) {
  //   console.log("이름이 입력되었습니다.");
  // }else {
  //   console.log("이름을 입력하세요.");
  // }
}

/*
  [switch 문]
  하나의 값을 여러 경우와 비교할 때 사용할 수 있다.
*/
{
  // const menu = "delete";

  // switch (menu) {
  //   case "save":
  //     console.log("저장을 시작합니다.");
  //     console.log("저장했습니다.");
  //     break;

  //   case "delete":
  //     console.log("삭제를 시작합니다.");
  //     console.log("삭제했습니다.");
  //     break;

  //   default:
  //     console.log("알 수 없는 명령입니다.");
  // }
}
/* - menu의 값을 case와 순서대로 비교해서 일치하는 case구문을 실행한다. */

/*
  break는 일치하는 case의 코드를 실행한 뒤 switch문을 종료한다.
  break를 생략하면 다음 case의 코드까지 계속 실행된다.
*/
{
  // const month = 16;

  // switch(month) { //동등비교 연산
  //     case 1: case 3: case 5: case 7: case 8: case 10: case 12:
  //         console.log(month+"월은 31일까지 입니다.");
  //         break;
  //     case 4: case 6: case 9: case 11:
  //         console.log(month+"월은 30일까지 입니다.");
  //         break;
  //     case 2:
  //         console.log(month+"월은 28일까지 입니다.");
  //         break;
  //     default:  //if문에 else
  //         console.log(month+"는 잘못된 값입니다.");
  // }
}

/* switch는 타입을 자동으로 변환하지 않고 값을 비교한다. */
{
  // const value = 10; 

  // switch (value) {
  //   case "10":
  //     console.log("문자열 10");
  //     break;

  //   case 10:
  //     console.log("숫자 10");
  //     break;
  // }
}


/*
  ---------------------------------------------
  6.2 반복문
  ---------------------------------------------
*/

/*
  [for 문]
  반복 횟수가 분명할 때 주로 사용한다.
*/
// for (초기식 ; 조건식; 증감식) {반복구문}
/*
 초기식 -> 조건식-true->반복구문->증감식
        -> 조건식-true->반복구문->증감식    
        -> 조건식-false->종료
*/
// for (let i = 0; i < 5; i++) {
//   console.log(i);
// }

// for (let i=0, j=5; i < 5 && j > 0; i++, j--) {
//   console.log(i, j);
// }

/*
  [while 문]
  조건이 참인 동안 반복한다.
*/
{
  // while (true) {
  //   console.log("hello");
    
  // }

  // let count = 0; // 초기식

  // while (count < 5) { // 조건식
  //   console.log(count); // 반복구문
  //   count++; //증감식
  // }
}

/*
  [do...while 문]
  조건을 검사하기 전에 반복문 본문을 한 번 실행한다.
*/
{
  // let count = 5;
  // do {
  //   console.log(count);
  //   count++;
  // } while (count < 5);
}

/*
  [for...of]
  배열이나 문자열처럼 순서가 있는 값의 요소를 반복할 때 사용한다.
*/
{
  // const numbers = [10, 20, 30];

  
  // for (const number of numbers) {
  //   console.log(number);
  // }
}

/* 인덱스와 값을 함께 사용하려면 entries()를 사용할 수 있다. */
{
//   const fruits = ["사과", "배", "포도"];
//  // [index, value]
//   for (const [index, fruit] of fruits.entries()) {
//     // if (index == 1) {
//     //   continue;
//     // }
//     console.log(index, fruit);
//   }
}

/*
  [for...in]
  객체의 속성 이름을 반복할 때 사용한다.
*/
{
  const user = {
    name: "홍길동",
    age: 20,
  };

  // console.log(user.name, user["name"]);

  // for (const key in user) { // key: string
  //   console.log(key, user[key]);
  // }
}

/*
  [break와 continue]
  break는 반복문을 즉시 종료한다.
*/
for (let i = 0; i < 10; i++) {
  if (i === 3) {
    break;
  }

  console.log(i);
}

/* continue는 현재 반복을 건너뛰고 다음 반복을 실행한다. */
for (let i = 0; i < 10; i++) {
  if (i % 3 === 0) { // 3의 배수
    continue;
  }

  console.log(i);
}

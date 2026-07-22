/*
  =============================================
  8. 배열
  =============================================
  배열은 여러 값을 순서대로 관리하는 객체이다.
  배열에 저장된 각 값은 요소(element)라고 하며,
  각 요소는 0부터 시작하는 인덱스를 가진다.
*/

const fruits = ["사과", "배", "포도"];

/*
  ---------------------------------------------
  8.1 배열 요소 접근
  ---------------------------------------------
  배열의 요소는 인덱스를 이용해 조회, 변경 한다.
*/
// const fruits = ["사과", "배", "포도"];
// console.log(fruits[0]); // "사과"
// console.log(fruits[1]); // "배"
// console.log(fruits[5]); //없는 index - undefined

// fruits[0] = '참외';
// console.log(fruits);

/*
  ---------------------------------------------
  8.2 배열 길이
  ---------------------------------------------
*/
// console.log(fruits.length); // 3

/*
  ---------------------------------------------
  8.3 주요 배열 메서드
  ---------------------------------------------
*/

/*
  [push()]
  배열 끝에 값을 추가한다.
*/
{
  // const numbers = [1, 2];
  // numbers.push(3);
  // console.log(numbers); // [1, 2, 3]
}

/*
  [pop()]
  배열 끝(마지막 인덱스)의 값을 제거하고 반환한다.
*/
{
  // const numbers = [1, 2, 3];
  // const removed = numbers.pop();

  // console.log(removed); // 3
  // console.log(numbers); // [1, 2]
  // console.log(numbers[numbers.length-1]); 
}

/*
  [unshift()]
  배열 앞에 값을 추가한다.
*/
{
  // const numbers = [2, 3];

  // numbers.unshift(1);

  // console.log(numbers); // [1, 2, 3]
}

/*
  [shift()]
  배열 앞의 값을 제거하고 반환한다.
*/
{
  // const numbers = [1, 2, 3];
  // const removed = numbers.shift();

  // console.log(removed); // 1
  // console.log(numbers);
}

/*
  [slice()]
  배열의 일부를 복사해 새 배열을 반환한다.
*/
{
  // const numbers = [10, 20, 30, 40, 50];
  // const result = numbers.slice(1, 4); // index 1 ~ index 3 까지 조회

  // console.log(result); // [20, 30, 40]
  // console.log(numbers); // 원본 유지
}

/*
  [splice()]
  배열의 요소를 삭제하거나 추가하거나 교체한다.
*/
{
  // const numbers = [1, 2, 3, 4];
  // // numbers.splice(1, 2, 10, 20, 30);  // index 1 부터 2개의 요소를 그 이후 값들(10, 20)으로 변경한다.
  // numbers.splice(1, 2); //변경할 값이 없으면 삭제.

  // console.log(numbers); // [1, 10, 20, 30, 4]
}
/* splice()는 원본 배열을 직접 변경한다. */

/*
  [concat()]
  배열을 합쳐 새 배열을 반환한다.
*/
{
  // const a = [1, 2];
  // const b = [3, 4];

  // const result = a.concat(b);

  // console.log(result); // [1, 2, 3, 4]
  // console.log(a);
  // console.log(b);
}

/*
  [join()]
  배열의 값을 문자열로 연결한다.
*/
{
  // const words = ["JavaScript", "React", "Vue"];

  // console.log(words.join(", ")); // "JavaScript, React, Vue"
}

/*
  [includes()]
  배열에 특정 값이 있는지 확인한다.
*/
{
  const fruits = ["사과", "배", "포도"];

  console.log(fruits.includes("수박")); // true
}

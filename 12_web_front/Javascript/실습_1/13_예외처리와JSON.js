/*
  =============================================
  13. 예외 처리와 JSON
  =============================================
*/

/*
  ---------------------------------------------
  13.1 try...catch
  ---------------------------------------------
  실행 중 발생할 수 있는 오류를 처리한다.
  오류 발생 가능성 있는 코드는 try block에 작성한다.
  오류가 발생했을 때 처리할 구문은 catch block에 작성한다.
*/
// try {
  // '{"name":"홍길동", "age":20}'
  //JSON.parse("JSON 문자열"): JSON을 객체로 변환
//   const result = JSON.parse("잘못된 JSON");
//   const result = JSON.parse('{"name":"홍길동", "age":20}');
//   console.log(result);
//   console.log(result.name, result.age)
// } catch (error) {
//   console.error("JSON 변환에 실패했습니다.");
//   console.error(error.message);
// }

/*
  ---------------------------------------------
  13.2 finally
  ---------------------------------------------
  오류 발생 여부와 관계없이 실행할 코드를 작성한다.
*/
// try {
//   console.log("작업 시작");
// } catch (error) {
//   // console.error(error);
//   console.log("에러발생");
// } finally {
//   console.log("작업 종료");
// }

/*
  ---------------------------------------------
  13.3 오류 발생시키기
  ---------------------------------------------
  함수나 메서드에서 정상적으로 작업을 계속할 수 없는 상황이 발생하면
  throw문을 사용하여 오류를 발생시킬 수 있다.
  발생한 오류는 함수를 호출한 쪽으로 전달되며,
  호출한 곳에서는 try...catch문을 사용하여 이를 처리할 수 있다.
*/
function divide(a, b) {
  if (b === 0) {
    throw new Error("0으로 나눌 수 없습니다.");
  }

  return a / b;
}

/* Caller */
try {
  const result = divide(10, 0);
  console.log(result);
} catch (error) {
  console.log(error.message);
}

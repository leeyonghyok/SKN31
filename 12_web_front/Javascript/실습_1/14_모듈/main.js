// =============================================
// 14.3 브라우저에서 모듈 사용하기 - main.js (브라우저 시작 모듈)
// =============================================
// main.js는 일반적으로 애플리케이션의 시작 모듈로 사용된다.
// HTML의 DOM 요소를 가져와 이벤트를 연결하고 화면을 변경하며,
// 다른 모듈에서 가져온 함수나 클래스를 조합하여 프로그램의 전체 동작을 실행한다.
//
// HTML은 main.js만 불러오며, main.js가 필요한 다른 모듈을 import하면
// 브라우저가 해당 파일도 자동으로 불러온다.
//
// ※ 이 파일은 document를 사용하므로 브라우저에서 index.html을 통해 실행한다.
//    (모듈은 file:// 로 열면 CORS 오류가 나므로 Live Server 등 웹서버로 연다.)

import { add } from "./math.js";

const button = document.querySelector("#calculate");
const result = document.querySelector("#result");

button.addEventListener("click", () => {
  result.textContent = add(10, 20);
});

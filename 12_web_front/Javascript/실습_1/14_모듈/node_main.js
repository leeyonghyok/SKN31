// =============================================
// 14. 모듈 - node_main.js (Node.js로 실행하는 시작 모듈)
// =============================================
// 실행 방법: 이 폴더(14_모듈)에서  node node_main.js
// (같은 폴더의 package.json에 "type": "module" 이 있어서
//  .js 파일에서 import/export 문법을 사용할 수 있다.)

// ---------------------------------------------
// 14.1 이름 있는 내보내기 가져오기
// ---------------------------------------------
// 다른 파일에서 이름 있는 내보내기를 가져올 때는 중괄호 {}를 사용한다.
// 가져올 때는 내보낸 이름과 같은 이름을 사용해야 한다.
// 필요한 값만 선택하여 가져올 수도 있다. 예) import { add } from "./math.js";

//   node  node_main.js
// import { add, PI } from "./math.js";

// console.log(add(10, 20));
// console.log(PI);
// // console.log(subtract(1, 2));

// // // 이름을 바꾸어 가져오기. as 키워드를 사용한다.
// import { add as sum, subtract } from "./math.js";

// console.log(sum(100, 20));
// // // - math.js가 내보낸 add 함수를 현재 파일에서 sum이라는 이름으로 사용한다.

// // // 선언과 분리하여 내보낸 값도 같은 방법으로 가져온다.
// // import { subtract } from "./math.js";

// console.log(subtract(30, 10));

// // ---------------------------------------------
// // 14.2 기본 내보내기 가져오기
// // ---------------------------------------------
// // { } 를 사용하지 않는다.
// // 아래 코드는 기본 내보내기로 export된 것을 User라는 이름으로 사용하겠다는 의미이다.
import User from "./User.js";

const user = new User("홍길동"); //객체 생성. 
console.log(user.name);

// // 기본 내보내기는 가져오는 쪽에서 이름을 자유롭게 정할 수 있다.
import Member from "./User.js"; 

const member = new Member("Lee");
console.log(member.name);
// // - User.js에서는 User라는 이름으로 클래스를 작성했지만,
// //   가져오는 파일에서는 Member라는 이름으로 사용할 수 있다.

// // 함수나 객체도 기본값으로 내보낼 수 있다.
import log from "./logger.js";
import config from "./config.js";

log("logger.js의 기본 내보내기 함수 실행");
console.log(config);

// // 하나의 파일에서는 이름 있는 내보내기와 기본 내보내기를 함께 사용할 수도 있다.
// // 가져올 때는 기본 내보내기를 중괄호 밖에 작성하고,
// // 이름 있는 내보내기를 중괄호 안에 작성한다.
// // (md 예시)
import add, { PI } from "./math.js";
//
console.log(add(10, 20));
console.log(PI);

// // > 기본 내보내기는 파일의 대표 기능이나 대표 객체를 내보낼 때 주로 사용한다.
// // > 이름 있는 내보내기는 한 파일에서 여러 기능을 제공할 때 적합하다.

// =============================================
// 14.2 기본 내보내기 - User.js
// =============================================
// 기본 내보내기(Default Export)는 파일의 대표 값을 하나 지정하여 내보내는 방식이다.
// 한 모듈에서는 기본 내보내기를 하나만 사용할 수 있다.

export default class User {
  constructor(name) {
    this.name = name;
  }
}

// 기본 내보내기도 선언과 분리하여 작성할 수 있다.
// (md 예시)
// class User {
//   constructor(name) {
//     this.name = name;
//   }
// }
//
// export default User;

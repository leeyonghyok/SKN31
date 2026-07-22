// 17.1.1 querySelector() — 하나의 요소 선택
const selectOneButton = document.querySelector("#select-one-button");

function selectSingleElements() {
  const title = document.querySelector("h3");            // 태그 선택자
  const paragraph = document.querySelector("#target-paragraph"); // 아이디 선택자
  const firstItem = document.querySelector(".item");     // 클래스 선택자

  console.log("태그 선택자(h3)로 찾은 요소:", title);
  console.log("아이디 선택자(#target-paragraph)로 찾은 요소:", paragraph);
  console.log("클래스 선택자(.item)로 찾은 요소:", firstItem);

  // 일치하는 요소가 없으면 null을 반환한다.
  const missing = document.querySelector("#not-exist");
  console.log("없는 요소를 찾은 결과:", missing);
}

// 17.1.2 querySelectorAll() — 모든 요소 선택
const selectAllButton = document.querySelector("#select-all-button");
const selectAllResult = document.querySelector("#select-all-result");

function selectAllFruits() {
  const fruits = document.querySelectorAll(".fruit");
  // [li, li, li]
  console.log("찾은 요소 개수(length):", fruits.length);

  fruits.forEach(fruit => {
    console.log("fruit 항목:", fruit.textContent);
  });

  selectAllResult.textContent = `fruit 클래스 요소를 ${fruits.length}개 찾았습니다.`;
}

// 17.1.3 NodeList와 배열의 차이
const nodelistCheckButton = document.querySelector("#nodelist-check-button");

function checkNodeListType() {
  const fruits = document.querySelectorAll(".fruit");

  console.log("NodeList가 배열인가?", Array.isArray(fruits)); // false

  // 전개 구문으로 NodeList를 새 배열로 변환한다.
  const fruitArray = [...fruits];

  console.log("변환한 결과가 배열인가?", Array.isArray(fruitArray)); // true

  // 배열이 되면 map() 같은 배열 메서드를 사용할 수 있다.
  const fruitNames = fruitArray.map(fruit => fruit.textContent);
  console.log("과일 이름 배열:", fruitNames);
}

// 이벤트 등록
selectOneButton.addEventListener("click", selectSingleElements);
selectAllButton.addEventListener("click", selectAllFruits);
nodelistCheckButton.addEventListener("click", checkNodeListType);

// 17.7 요소 생성 + 17.8 요소 삽입 (createElement / prepend / append)
const itemInput = document.querySelector("#item-input");
const prependButton = document.querySelector("#prepend-button");
const appendButton = document.querySelector("#append-button");
const todoList = document.querySelector("#todo-list");

// 입력값으로 새 li 요소를 만들어 반환한다.
function createListItem() {
  const item = document.createElement("li"); // <li></li>

  item.textContent = itemInput.value; //<li>value</li>

  return item;
}

function prependListItem() {
  const item = createListItem();

  todoList.prepend(item); // 첫 번째 자식 앞에 삽입
  console.log("목록 맨 앞에 추가했습니다:", item.textContent);
}

function appendListItem() {
  const item = createListItem();

  todoList.append(item); // 마지막 자식 뒤에 삽입
  console.log("목록 맨 뒤에 추가했습니다:", item.textContent);
}

// 17.8 형제 위치 삽입 (before / after)
const baseParagraph = document.querySelector("#base-paragraph");
const insertBeforeButton = document.querySelector("#insert-before-button");
const insertAfterButton = document.querySelector("#insert-after-button");

function insertParagraphBefore() {
  // baseParagraph 앞에 삽입
  const newParagraph = document.createElement("p");//<p></p>
  newParagraph.style.color = "blue";//<p style="color:blue;"></p>

  newParagraph.textContent = "기준 문단 앞에 삽입된 문단";
  //<p style="color:blue;">기준 문단 앞에 삽입된 문단</p>

  baseParagraph.before(newParagraph);
}

function insertParagraphAfter() {
  const newParagraph = document.createElement("p");
  newParagraph.style.color = "red";

  newParagraph.textContent = "기준 문단 뒤에 삽입된 문단";
  baseParagraph.after(newParagraph);
}

// 17.9 요소 삭제 (remove / removeChild)
const removeButton = document.querySelector("#remove-button");
const removeChildButton = document.querySelector("#remove-all-button");
const fruitList = document.querySelector("#fruit-list");

function removeAppleItem() {

  const appleItem = document.querySelector("#apple-item");//삭제할 노드

  if (!appleItem) {
    console.log("사과 항목이 이미 삭제되었습니다.");
    return;
  }

  appleItem.remove(); // 요소 자신을 삭제
  console.log("remove()로 사과 항목을 삭제했습니다.");
}

function removeAllItem() {

  // ElementNode.hasChildNodes(): 자식노드가 있는지 여부.
  // ElementNode.firstChild/lastChild : 첫번째/마지막 자식 노드 객체를 반환.
  // ElementNode.parentNode // 부모노드 반환
  // ElementNode.children   // 모든 자식노드들을 Node List로 반환.
  while (fruitList.hasChildNodes()) {
      // 부모노드.removeChild(삭제할 자식노드);
      fruitList.removeChild(fruitList.firstChild);
  }


  console.log("모든 목록 아이템삭제:", fruitList.children.length);
}

// 17.10 요소 교체 (replaceWith)
const replaceButton = document.querySelector("#replace-button");

function replaceOldParagraph() {
  const oldParagraph = document.querySelector("#old-paragraph");

  if (!oldParagraph) {
    console.log("이미 교체된 문단입니다.");
    return;
  }

  const newElement = document.createElement("p");//<p></p>
  const strongElement = document.createElement("strong")//<strong></strong>
  newElement.append(strongElement);//<p><strong></strong></p>

  strongElement.textContent = "교체된 새 요소(p strong)";//<p><strong>교체된 새 요소(p strong)</strong></p>
  oldParagraph.replaceWith(newElement);
}

// 이벤트 등록
prependButton.addEventListener("click", prependListItem);
appendButton.addEventListener("click", appendListItem);
insertBeforeButton.addEventListener("click", insertParagraphBefore);
insertAfterButton.addEventListener("click", insertParagraphAfter);
removeButton.addEventListener("click", removeAppleItem);
removeChildButton.addEventListener("click", removeAllItem);
replaceButton.addEventListener("click", replaceOldParagraph);

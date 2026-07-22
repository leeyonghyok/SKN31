// 15.1 이벤트 등록
const confirmButton = document.querySelector("#confirm-button");
const clickResult = document.querySelector("#click-result");

let clickCount = 0;

function showClickMessage() {
  clickCount = clickCount + 1;
  clickResult.textContent = `버튼을 ${clickCount}번 클릭했습니다.`;
  //<p>textContent</p>
  
  console.log("클릭 횟수:", clickCount);
}

// 15.2 이벤트 객체
const eventInfoButton = document.querySelector("#event-info-button");
const eventInfoResult = document.querySelector("#event-info-result");

function showEventInfo(event) {
  console.log("이벤트 이름(event.type):", event.type);
  console.log("이벤트가 시작된 요소(event.target):", event.target);
  console.log("처리 함수가 등록된 요소(event.currentTarget):", event.currentTarget);

  eventInfoResult.textContent = `이벤트 이름: ${event.type} / 발생 한 소스 노드: ${event.target.tagName}`;
}

// 15.3 입력 이벤트
const nameInput = document.querySelector("#name-input");
const inputResult = document.querySelector("#input-result");

function showCurrentInputValue(event) {
  const currentValue = event.target.value;
  
  inputResult.textContent = `현재 입력값: ${currentValue}`;
  console.log("현재 입력값:", currentValue);
}

// 15.4 기본 동작 막기
const simpleForm = document.querySelector("#simple-form");
const messageInput = document.querySelector("#message-input");
const submitResult = document.querySelector("#submit-result");

function handleFormSubmit(event) {
  event.preventDefault(); // 페이지 새로고침(기본 동작)을 막는다.
  
  submitResult.textContent = `제출된 메시지: ${messageInput.value}`;
  console.log("폼 제출을 JavaScript에서 처리했습니다. 메시지:", messageInput.value);


}

// 15.5 이벤트 전파(이벤트 위임)
const userList = document.querySelector("#user-list");
const delegationResult = document.querySelector("#delegation-result");

function showClickedUser(event) {
  const item = event.target.closest("li");

  if (!item) {
    return;
  }

  delegationResult.textContent = `선택한 사용자: ${item.textContent} (id: ${item.dataset.userId})`;
  console.log("클릭한 사용자 id:", item.dataset.userId);
}

// 이벤트 등록
confirmButton.addEventListener("click", showClickMessage);
eventInfoButton.addEventListener("click", showEventInfo);
nameInput.addEventListener("change", showCurrentInputValue);
simpleForm.addEventListener("submit", handleFormSubmit);
userList.addEventListener("click", showClickedUser);

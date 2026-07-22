// 17.2 텍스트 변경 (textContent)
const changeTextButton = document.querySelector("#change-text-button");
const textTarget = document.querySelector("#text-target");

function changeTextContent() {
  // 태그 문자열을 넣어도 HTML로 해석하지 않고 글자 그대로 표시한다.
  console.log("textTarget.textContent:", textTarget.textContent); //변경전 값
  textTarget.textContent = "변경된 텍스트 <strong>태그도 글자로 표시</strong>";
  console.log("textContent로 텍스트를 변경했습니다.");
}

// 17.3 HTML 변경 (innerHTML)
const changeHtmlButton = document.querySelector("#change-html-button");
const htmlTarget = document.querySelector("#html-target");

function changeInnerHtml() {
  // innerHTML은 문자열의 태그를 실제 요소로 만든다.
  htmlTarget.innerHTML = "<strong>강조된 내용</strong>과 일반 텍스트";
  console.log("innerHTML로 HTML 구조를 변경했습니다.", htmlTarget.innerHTML);
}

// 17.4 속성 변경 (setAttribute / getAttribute / removeAttribute)
const changeAttributeButton = document.querySelector("#change-attribute-button");
const sampleLink = document.querySelector("#sample-link");
const attributeResult = document.querySelector("#attribute-result");

function changeLinkAttributes() {
  sampleLink.setAttribute("href", "https://www.naver.com");
  sampleLink.removeAttribute("target");

  const currentHref = sampleLink.getAttribute("href");

  attributeResult.textContent = `현재 href 속성값: ${currentHref} (target 속성은 삭제됨)`;
  console.log("getAttribute로 읽은 href:", currentHref);
  console.log("삭제한 target 속성값:", sampleLink.getAttribute("target")); // null
}

// 17.5 클래스 속성 변경 (classList)
const toggleClassButton = document.querySelector("#toggle-class-button");
const classTarget = document.querySelector("#class-target");
const classResult = document.querySelector("#class-result");

function toggleActiveClass() {
  // 클래스가 있으면 제거하고 없으면 추가한다.
  classTarget.classList.toggle("active");

  const hasActive = classTarget.classList.contains("active");

  classResult.textContent = `현재 active 클래스 여부: ${hasActive}`;
  console.log("active 클래스 포함 여부:", hasActive);
}

// 17.6 스타일 변경 (style)
const changeStyleButton = document.querySelector("#change-style-button");
const styleTarget = document.querySelector("#style-target");

function changeInlineStyle() {
  // CSS의 font-size는 JavaScript에서 fontSize(카멜 표기법)로 쓴다.
  styleTarget.style.color = "blue";// {color:blue;}
  styleTarget.style.fontSize = "30px"; // {font-size:"30px"}
  //styleTarget.setAttribute("style", "font-weight:bold;border:1px solid blue;")
  console.log("인라인 스타일을 변경했습니다. color: blue, fontSize: 20px");
}

// 17.11 dataset (data-* 속성)
const userButton1 = document.querySelector("#user-button1");
const userButton2 = document.querySelector("#user-button2");
const datasetResult = document.querySelector("#dataset-result");

function showUserDataset(event) {
  // data-user-id 속성은 dataset.userId로 접근한다. 값은 문자열이다.
  const userId = event.target.dataset.userId;

  datasetResult.textContent = `data-user-id 값: ${userId} (타입: ${typeof userId})`;
  console.log("dataset.userId 값:", userId+1000);
  console.log("숫자로 변환한 값:", Number(userId)+1000);
}

// 이벤트 등록
changeTextButton.addEventListener("click", changeTextContent);
changeHtmlButton.addEventListener("click", changeInnerHtml);
changeAttributeButton.addEventListener("click", changeLinkAttributes);
toggleClassButton.addEventListener("click", toggleActiveClass);
changeStyleButton.addEventListener("click", changeInlineStyle);
userButton1.addEventListener("click", showUserDataset);
userButton2.addEventListener("click", showUserDataset);

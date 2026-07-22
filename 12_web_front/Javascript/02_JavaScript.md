# 15. 이벤트(Event) 처리

이벤트는 사용자의 클릭이나 입력, 문서 로딩처럼 브라우저에서 발생하는 동작이나 상태 변화를 의미한다. JavaScript는 이벤트가 발생한 시점에 실행할 함수를 등록하여 사용자와 상호작용하는 화면을 만들 수 있다. 

대표적인 이벤트는 다음과 같다.

| 이벤트 이름 | 발생 시점 |
|---|---|
| `click` | 요소를 클릭했을 때 |
| `input` | 입력값이 바뀔 때. 입력값이 바뀔 때 마다 발생한다. |
| `change` | 입력값 변경이 확정될 때. 입력이 끝나고 포커스를 잃을 때 발생한다. |
| `focus` | 요소가 입력 포커스를 얻을 때 |
| `blur` | 요소가 입력 포커스를 잃을 때 |
| `keydown` | 키를 누를 때 |
| `keyup` | 키에서 손을 뗄 때 |
| `submit` | 폼을 제출할 때 |
| `DOMContentLoaded` | HTML 문서 분석이 끝났을 때 |

## 15.1 이벤트 등록

`addEventListener(이벤트명, 처리함수)`는 특정 요소에서 이벤트가 발생했을 때 실행할 함수를 등록한다. 첫 번째 인수에는 `"click"` 같은 이벤트 이름을, 두 번째 인수에는 실행할 콜백 함수를 전달하며 반환값은 없다.

```html
<button id="confirmButton" type="button">확인</button>
```

```javascript
const button = document.querySelector("#confirmButton");

button.addEventListener("click", () => {
  console.log("버튼을 클릭했습니다.");
});
```

위 코드는 `button`에서 `click` 이벤트가 발생할 때마다 등록한 화살표 함수를 실행하여 콘솔에 메시지를 출력한다.

> **인라인 이벤트 처리**: Tag에 on이벤트이름(예: `onclick`, `onblur`) 와 같은 event handler 속성에 처리 로직을 넣는 방식으로 이벤트 처리를 할 수있다. 이는 JavaScript classic 방식으로 지금도 동작하지만 현대적인 웹 개발에서는 일반적으로 권장하지 않고, JavaScript의 addEventListener()를 사용하는 것이 권장된다   
> `<button onclick="checkValue();">값 검증</button>`

## 15.2 이벤트 객체

이벤트 처리 함수는 발생한 이벤트의 정보를 담은 이벤트 객체를 첫 번째 매개변수로 받을 수 있다. 이벤트 객체에는 이벤트 종류, 시작 요소, 현재 처리 중인 요소와 같은 정보와 이벤트 동작을 제어하는 메서드가 들어 있다.

```javascript
button.addEventListener("click", event => {
  console.log(event.type);
  console.log(event.target);
  console.log(event.currentTarget);
});
```

- `event.type`: 발생한 이벤트 이름을 문자열로 반환한다.
- `event.target`: 실제 이벤트가 시작된 요소를 가리킨다.
- `event.currentTarget`: 현재 이벤트 처리 함수가 등록된 요소를 가리킨다.

자식 요소를 클릭한 이벤트가 부모 요소로 전달되면 `target`과 `currentTarget`이 서로 다를 수 있다.

## 15.3 입력 이벤트

`input` 이벤트는 텍스트 입력, 붙여넣기, 삭제 등으로 입력 요소의 값이 바뀔 때마다 발생한다. 입력 요소의 현재 값은 이벤트가 시작된 요소를 나타내는 `event.target`의 `value` 속성으로 읽는다.

```html
<input id="nameInput" type="text">
```

```javascript
const input = document.querySelector("#nameInput");

input.addEventListener("input", event => {
  console.log(event.target.value);
});
```

`value`는 입력 요소에 현재 들어 있는 값을 문자열로 반환하며, `type="number"`인 입력 요소에서도 기본적으로 문자열을 반환한다.

## 15.4 기본 동작 막기

링크 이동이나 폼 제출처럼 이벤트에 연결된 브라우저의 기본 동작은 `event.preventDefault()`로 취소할 수 있다. 이 메서드는 인수와 반환값이 없으며, 이벤트가 취소 가능한 경우에만 효과가 있다.

```javascript
form.addEventListener("submit", event => {
  event.preventDefault();
});
```

폼의 `submit` 이벤트에서 기본 동작을 막으면 페이지가 새로고침되거나 지정된 주소로 즉시 전송되지 않으므로, JavaScript로 입력값을 검사하거나 비동기 요청을 보낼 수 있다.

## 15.5 이벤트 전파

중첩된 요소에서 이벤트가 발생하면 일반적으로 이벤트가 시작된 안쪽 자손 요소에서 바깥쪽 조상 요소로 전달되는데, 이를 **이벤트 버블링**이라고 한다. 
부모 요소에 처리 함수 하나를 등록하고 실제 클릭된 자식 요소를 구분하면 여러 자식의 이벤트를 한곳에서 처리할 수 있다.
기본적으로 자식 요소의 핸들러 실행 후에도 이벤트는 계속 조상 요소로 버블링된다. 

```html
<ul id="userList">
  <li data-user-id="1">홍길동</li>
  <li data-user-id="2">이순신</li>
</ul>
```

```javascript
const userList = document.querySelector("#userList");

userList.addEventListener("click", event => {
  const item = event.target.closest("li");

  if (!item) {
    return;
  }

  console.log(item.dataset.userId);  // data- 다음부분만 사용해서 조회. `-`은 제거하고 Camel 표기법으로 변경. 
});
```

`closest(선택자)`는 현재 요소부터 부모 방향으로 올라가며 CSS 선택자와 일치하는 가장 가까운 요소를 반환하고, 찾지 못하면 `null`을 반환한다. 위 코드에서는 실제 클릭된 위치가 `li` 내부의 다른 요소여도 가장 가까운 `li`를 찾는다.

부모 요소 **하나에 이벤트를 등록하여 여러 자식 요소의 이벤트를 처리하는 방식을 이벤트 위임**이라고 한다. 동적으로 추가된 자식 요소도 별도의 이벤트 등록 없이 같은 처리 함수로 다룰 수 있다는 장점이 있다.

> `data-*` 속성은 HTML Element(요소) 에 값을 저장해두는 변수 같은 역할을 한다. JavaScript에서 `Node.dataset` 사용해 그 값을 조회할 수 있다.

---

# 16. DOM 기초

DOM(Document Object Model)은 HTML 문서를 JavaScript에서 읽고 변경할 수 있도록 객체와 트리 구조로 표현한 것이다. 브라우저는 HTML을 분석하여 문서, 요소, 텍스트를 각각 노드 객체로 만들고 부모와 자식 관계로 연결한다.

- 브라우저는 문서를 구성하는 요소(element)들을 객체로 생성하고 이들을 계층적인 트리 구조로 관리한다.
- 문서를 구성하는 객체들을 **노드(Node)**라고 하며, HTML 문서의 태그와 텍스트 등은 모두 노드로 표현된다.

노드의 종류는 다음과 같다.

- **Element Node(요소 노드)**: HTML 태그를 나타내는 노드이다. `<html>`, `<body>`, `<h1>`, `<p>` 등이 요소 노드이다.
- **Text Node(텍스트 노드)**: 태그 안에 있는 문자열을 나타내는 노드이다.

```html
<h1>제목</h1>
```

위 코드에서 `<h1>`은 Element Node이고, `"제목"`은 그 요소의 자식인 Text Node이다.

**예)**

```html
<html>
  <head></head>
  <body>
    <h1>제목</h1>
    <p>내용</p>
  </body>
</html>
```

```text
Document
└─ html (Element)
   ├─ head (Element)
   └─ body (Element)
      ├─ h1 (Element)
      │  └─ "제목" (Text)
      └─ p (Element)
         └─ "내용" (Text)
```

JavaScript는 DOM을 통해 다음 작업을 수행할 수 있다.

- 요소 찾기
- 텍스트 변경
- 속성 변경
- 스타일 변경
- 요소 생성과 삭제
- 이벤트 등록

JavaScript에서 Element Node를 선택하면 해당 HTML 요소를 나타내는 객체를 얻는다. 이 객체의 속성과 메서드를 사용해 텍스트, 속성, 스타일, 자식 요소 등을 읽거나 변경할 수 있다.

---

# 17. DOM Element(요소) 선택과 변경

화면의 HTML을 변경하려면 먼저 DOM에서 대상 요소를 선택한 뒤 해당 요소의 속성이나 메서드를 사용한다. 이 장에서는 요소를 찾고 내용·속성·스타일을 바꾸며 새로운 요소를 추가하거나 삭제하는 방법을 다룬다.

## 17.1 요소 선택

DOM 요소 선택 메서드는 CSS 선택자를 사용해 문서 안의 Element 객체를 찾는다. 하나의 요소가 필요할 때는 `querySelector()`를, 조건에 맞는 모든 요소가 필요할 때는 `querySelectorAll()`을 사용한다.

### `querySelector()`

`querySelector(선택자)`는 메서드를 호출한 문서나 요소 내부에서 CSS 선택자와 일치하는 첫 번째 Element를 반환한다. 일치하는 요소를 찾지 못하면 `null`을 반환하므로, 요소가 존재하지 않을 수 있는 경우에는 사용 전에 확인해야 한다.

```javascript
const title = document.querySelector("h1");
const button = document.querySelector("#submitButton");
const item = document.querySelector(".item");
```

`"h1"`은 태그 선택자, `"#submitButton"`은 아이디 선택자, `".item"`은 클래스 선택자이다.

### `querySelectorAll()`

`querySelectorAll(선택자)`는 CSS 선택자와 일치하는 모든 Element를 정적인 `NodeList`로 반환한다. 찾은 요소가 없어도 `null`이 아니라 길이가 0인 `NodeList`를 반환한다.

```javascript
const items = document.querySelectorAll(".item");

items.forEach(item => {
  console.log(item.textContent);
});
```

`NodeList`는 배열과 비슷하게 `length`와 `forEach()`를 사용할 수 있지만 실제 배열은 아니므로 `map()`이나 `filter()` 같은 배열 메서드를 바로 사용할 수는 없다.

```javascript
console.log(Array.isArray(items)); // false
```

전개 구문을 사용하면 `NodeList`를 새 배열로 변환할 수 있다.

```javascript
const itemArray = [...items];
```

## 17.2 텍스트 변경

Element의 `textContent` 속성은 요소와 그 자손에 들어 있는 텍스트를 문자열로 읽거나 새 문자열로 바꾼다. 값을 대입하면 기존 자식 내용이 모두 제거되고 입력한 문자열이 하나의 텍스트로 들어간다.

```javascript
const title = document.querySelector("h1");

title.textContent = "변경된 제목";
```

`textContent`에 `<strong>` 같은 문자열을 넣어도 HTML 태그로 해석하지 않고 그대로 표시하므로 일반 텍스트를 안전하게 출력할 때 적합하다.

## 17.3 HTML 변경

Element의 `innerHTML` 속성은 요소 내부의 HTML 문자열을 읽거나 새로운 HTML 구조로 교체한다. 값을 대입하면 문자열의 태그를 분석하여 실제 자식 노드로 생성한다.

```javascript
const container = document.querySelector("#container");

container.innerHTML = "<strong>강조된 내용</strong>";
```

사용자가 입력한 문자열을 검증 없이 `innerHTML`에 넣으면 악성 스크립트나 이벤트 속성이 실행되는 XSS 보안 문제가 생길 수 있다.

```javascript
container.innerHTML = userInput; // 사용에 주의
```

HTML 구조를 만들 필요가 없는 일반 텍스트는 `textContent`를 사용한다.

## 17.4 속성 변경

HTML 속성(attribute)은 Element의 `setAttribute()`, `getAttribute()`, `removeAttribute()` 메서드로 추가·조회·삭제할 수 있다. 속성 이름은 첫 번째 인수로 전달하고, 값을 설정할 때는 두 번째 인수로 문자열 값을 전달한다.

```javascript
const link = document.querySelector("a");

link.setAttribute("href", "https://example.com");
console.log(link.getAttribute("href"));
link.removeAttribute("target");
```

- `setAttribute(이름, 값)`은 속성을 새로 만들거나 기존 값을 변경하며 반환값은 없다.
- `getAttribute(이름)`은 HTML에 기록된 속성값을 문자열로 반환하고, 속성이 없으면 `null`을 반환한다.
- `removeAttribute(이름)`은 해당 속성을 삭제하며 반환값은 없다.

일부 표준 속성은 Element 객체의 프로퍼티에 점 표기법으로 직접 접근할 수도 있다.

```javascript
link.href = "https://example.com";
```

프로퍼티로 읽은 `href`는 브라우저가 절대 주소로 해석한 값일 수 있지만, `getAttribute("href")`는 HTML에 지정된 원래 문자열을 반환한다.

## 17.5 클래스 속성 변경

Element의 `classList` 속성은 요소의 CSS 클래스 목록을 관리하는 객체를 반환한다. 문자열 전체를 직접 수정하지 않고 클래스를 하나씩 추가·삭제·전환하거나 포함 여부를 확인할 수 있다.

```javascript
const box = document.querySelector(".box");

box.classList.add("active");
box.classList.remove("hidden");
box.classList.toggle("selected");

console.log(box.classList.contains("active"));
```

- `add(클래스명)`은 클래스를 추가하고, 이미 있으면 중복해서 추가하지 않는다.
- `remove(클래스명)`은 클래스를 제거하며, 해당 클래스가 없어도 오류가 발생하지 않는다.
- `toggle(클래스명)`은 클래스가 있으면 제거하고 없으면 추가하며, 처리 후 클래스가 존재하면 `true`를 반환한다.
- `contains(클래스명)`은 해당 클래스의 존재 여부를 불리언 값으로 반환한다.

## 17.6 스타일 변경

Element의 `style` 속성은 HTML의 인라인 스타일을 나타내며, CSS 속성 이름을 JavaScript의 카멜 표기법으로 바꾸어 값을 설정한다. 예를 들어 CSS의 `background-color`는 `backgroundColor`로 작성한다.

```javascript
box.style.backgroundColor = "yellow";
box.style.fontSize = "20px";
```

`style`로 읽을 수 있는 값은 주로 인라인으로 지정한 스타일이며, 외부 CSS까지 계산된 최종 스타일이 필요하면 `getComputedStyle(요소)`를 사용한다. 여러 스타일을 관리할 때는 JavaScript에서 각각 지정하기보다 CSS 클래스를 추가하고 제거하는 방식이 좋다.

## 17.7 Element Node 생성

화면에 추가할 Element Node는 `document.createElement("태그명")`을 사용해 생성할 수 있다. 새로 만든 요소는 메모리에만 존재하므로 `append()` 같은 삽입 메서드로 문서에 추가해야 화면에 나타난다.

```javascript
const list = document.querySelector("#list");
const item = document.createElement("li");

item.textContent = "새 항목";

list.append(item);
```

`createElement()`는 만들 태그 이름을 문자열 인수로 받고 새 Element 객체를 반환한다. 위 코드에서는 `li` 요소를 만든 뒤 텍스트를 설정하고 `list`의 마지막 자식으로 삽입한다.

## 17.8 요소 삽입

새로 만들었거나 기존에 존재하는 요소는 `prepend()`, `append()`, `before()`, `after()`로 원하는 DOM 위치에 삽입할 수 있다. 네 메서드는 Node 객체나 문자열을 하나 이상 인수로 받을 수 있고 반환값은 없다.

```javascript
list.prepend(item);
list.append(item);

element.before(newElement);
element.after(newElement);
```

- `부모.prepend(노드)`는 전달한 노드를 부모 요소의 첫 번째 자식 앞에 삽입한다.
- `부모.append(노드)`는 전달한 노드를 부모 요소의 마지막 자식 뒤에 삽입한다.
- `기준요소.before(노드)`는 기준 요소의 바로 앞에 형제 노드로 삽입한다.
- `기준요소.after(노드)`는 기준 요소의 바로 뒤에 형제 노드로 삽입한다.

이미 DOM에 들어 있는 같은 Node를 다른 위치에 삽입하면 복사본이 생기는 것이 아니라 기존 위치에서 새 위치로 이동한다. 같은 모양의 요소가 여러 개 필요하면 각각 생성하거나 `cloneNode()`로 복제해야 한다.

## 17.9 요소 삭제

### 노드를 삭제
`remove()`는 메서드를 호출한 요소를 DOM에서 삭제한다. `item.remove()`처럼 삭제할 Element 객체에서 호출하며, 별도의 인수와 반환값은 없다.

```javascript
item.remove();
```

### 자식 노드 삭제
`removeChild()` 를 사용해서 부모 노드의 특정 자식노드를 제거한다. 그리고 제거한 자식노드를 반환한다.

```javascript
부모노드.removeChild(제거할자식노드);
```

```html
<ul id="list">
  <li id="item">사과</li>
  <li>바나나</li>
</ul>
```
```javascript
const list = document.querySelector("#list");
const item = document.querySelector("#item");

list.removeChild(item);
```


## 17.10 요소 교체

`replaceWith(새노드)`는 메서드를 호출한 기존 요소를 전달한 Node나 문자열로 교체한다. 인수로 여러 값을 전달할 수도 있으며, 기존 요소는 DOM에서 제거되고 반환값은 없다.

```javascript
oldElement.replaceWith(newElement);
```

`newElement`가 이미 다른 위치에 존재하는 Node라면 새 위치로 이동하면서 `oldElement`를 대신한다.

## 17.11 `dataset`

HTML의 `data-*` 사용자 정의 속성은 Element의 `dataset` 객체로 읽고 변경할 수 있다. `data-user-id`처럼 하이픈으로 구분한 이름은 JavaScript에서 `userId`와 같은 카멜 표기법 프로퍼티로 접근한다.

```html
<button data-user-id="10">사용자 선택</button>
```

```javascript
const button = document.querySelector("button");

console.log(button.dataset.userId); // "10"
```

`dataset`으로 읽은 값은 숫자처럼 보여도 문자열이다. `button.dataset.userId = "20"`처럼 값을 대입하면 대응하는 `data-user-id` 속성이 변경되며, 숫자 계산이 필요하면 `Number()` 등으로 명시적으로 변환한다.

---

# 18. 폼 처리

폼 처리는 사용자가 입력한 값을 읽고 검증한 뒤 서버 전송이나 화면 갱신에 사용하는 과정이다. JavaScript에서는 폼의 `submit` 이벤트, `elements` 속성, `FormData` 객체를 이용해 입력 요소와 값을 다룬다.

## 18.1 폼 제출

폼의 제출 버튼을 누르거나 입력 요소에서 Enter 키를 누르면 `submit` 이벤트가 발생한다. `addEventListener("submit", 처리함수)`로 제출 시점의 작업을 등록하고, JavaScript에서 처리하려면 `preventDefault()`로 기본 전송 동작을 막는다.

```html
<form id="signupForm">
  <label>
    이름
    <input name="name" type="text" required>
  </label>

  <label>
    나이
    <input name="age" type="number">
  </label>

  <button type="submit">가입</button>
</form>
```

```javascript
const form = document.querySelector("#signupForm");

form.addEventListener("submit", event => {
  event.preventDefault();

  console.log("폼 제출");
});
```

제출 이벤트는 버튼의 `click` 이벤트가 아니라 `form` 요소에서 처리하는 것이 좋다. 이렇게 하면 버튼 클릭뿐 아니라 Enter 키 제출과 같은 폼의 모든 제출 경로를 함께 처리할 수 있다.

## 18.2 `FormData`

`new FormData(form)`은 폼에서 이름과 값을 가진 입력 항목을 읽어 `FormData` 객체로 만든다. 각 입력 요소의 `name` 속성이 데이터의 키가 되며, `name`이 없는 요소와 선택되지 않은 체크박스·라디오 버튼은 포함되지 않는다.

```javascript
form.addEventListener("submit", event => {
  event.preventDefault();

  const formData = new FormData(form);

  const name = formData.get("name");
  const age = formData.get("age");

  console.log(name, age);
});
```

`formData.get(이름)`은 해당 이름의 첫 번째 값을 문자열 또는 `File` 객체로 반환하고, 값이 없으면 `null`을 반환한다. 텍스트와 숫자 입력값은 모두 문자열이므로 숫자가 필요하면 `Number(age)`처럼 변환한다.

`entries()`는 폼의 모든 `[이름, 값]` 쌍을 순회하는 이터레이터를 반환하고, `Object.fromEntries()`는 이를 일반 객체로 변환한다.

```javascript
const data = Object.fromEntries(formData.entries());

console.log(data);
```

같은 이름의 값이 여러 개이면 일반 객체의 키 하나에 모두 담을 수 없으므로, 위 변환에서는 마지막 값만 남을 수 있다. 여러 개의 체크박스처럼 같은 이름을 가진 값을 모두 가져올 때는 `getAll()`을 사용한다.

```javascript
const hobbies = formData.getAll("hobby");
```

`getAll(이름)`은 같은 이름으로 등록된 모든 값을 배열로 반환하며, 값이 없으면 빈 배열을 반환한다.

## 18.3 폼 요소 접근

폼의 `elements` 속성은 폼에 포함된 입력 컨트롤의 모음을 반환한다. 입력 요소의 `name`을 사용해 `form.elements.name` 또는 `form.elements["name"]` 형식으로 접근할 수 있다.

```javascript
const nameInput = form.elements.name;

console.log(nameInput.value);
```

입력 요소의 `value` 속성은 현재 값을 문자열로 반환한다. 같은 `name`을 가진 요소가 여러 개이면 단일 요소 대신 `RadioNodeList`와 같은 목록 객체가 반환될 수 있다.

## 18.4 체크박스

체크박스의 선택 여부는 `checked` 속성으로 확인하거나 변경한다. `checked`는 선택되어 있으면 `true`, 선택되어 있지 않으면 `false`인 불리언 값이다.

```html
<label>
  <input name="agree" type="checkbox">
  약관 동의
</label>
```

```javascript
const agreeInput = form.elements.agree;

console.log(agreeInput.checked);
```

`value`는 체크박스가 선택되었는지를 나타내지 않으므로 선택 여부를 확인할 때는 반드시 `checked`를 사용한다. 선택된 체크박스의 전송값이 필요하면 `value` 속성을 함께 지정한다.

## 18.5 라디오 버튼

같은 `name`을 가진 라디오 버튼은 하나의 그룹을 이루며 그룹에서 한 항목만 선택할 수 있다. `FormData.get(이름)`은 선택된 라디오 버튼의 `value`를 문자열로 반환하고, 선택된 항목이 없으면 `null`을 반환한다.

```html
<label>
  <input name="level" type="radio" value="beginner">
  초급
</label>

<label>
  <input name="level" type="radio" value="advanced">
  고급
</label>
```

```javascript
const formData = new FormData(form);
const level = formData.get("level");
```

위 코드에서 초급을 선택하면 `level`은 `"beginner"`, 고급을 선택하면 `"advanced"`가 된다.

## 18.6 입력값 검증

입력값 검증은 빈 문자열, 허용되지 않은 형식, 범위를 벗어난 값 등을 제출 전에 확인하는 작업이다. 문자열의 앞뒤 공백은 `trim()`으로 제거하고, 문제가 있는 입력 요소에는 `focus()`를 호출해 사용자가 바로 수정할 수 있게 한다.

```javascript
form.addEventListener("submit", event => {
  event.preventDefault();

  const name = form.elements.name.value.trim();

  if (!name) {
    console.log("이름을 입력하세요.");
    form.elements.name.focus();
    return;
  }

  console.log("입력값이 올바릅니다.");
});
```

`trim()`은 원본 문자열을 바꾸지 않고 양끝 공백을 제거한 새 문자열을 반환한다. `focus()`는 해당 입력 요소로 입력 포커스를 이동하며 반환값은 없다. 브라우저의 `required`, `min`, `pattern` 같은 HTML 검증 속성과 JavaScript 검증을 함께 사용하면 기본적인 오류를 더 일관되게 처리할 수 있다.

---

# 19. Fetch API

Fetch API는 브라우저에서 서버로 HTTP 요청을 보내고 응답을 비동기로 처리하는 기능이다. `fetch()`는 즉시 응답 데이터를 주는 대신 작업의 완료 상태를 나타내는 `Promise<Response>`를 반환한다.

## 19.1 GET 요청

`fetch(주소)`는 별도의 옵션이 없으면 GET 방식으로 요청을 보내며, `await`를 사용하면 Promise가 처리될 때까지 현재 비동기 함수의 실행을 기다렸다가 `Response` 객체를 얻는다. JSON 본문은 `response.json()`으로 읽으며 이 메서드도 Promise를 반환하므로 `await`가 필요하다.

```javascript
async function fetchUsers() {
  const response = await fetch("/api/users");
  const users = await response.json();

  console.log(users);
}
```

`async`로 선언한 함수는 항상 Promise를 반환한다. 따라서 `fetchUsers()`의 완료 결과를 사용하려면 호출하는 쪽에서도 `await` 또는 `then()`을 사용해야 한다.

## 19.2 HTTP 상태 확인

`fetch()`는 서버가 404 또는 500 상태를 반환하더라도 HTTP 응답 자체를 받았다면 Promise를 성공 상태로 처리한다. 따라서 응답 본문을 사용하기 전에 `response.ok`나 `response.status`로 HTTP 상태를 확인해야 한다.

```javascript
async function fetchUsers() {
  const response = await fetch("/api/users");

  if (!response.ok) {
    throw new Error(`HTTP 오류: ${response.status}`);
  }

  return response.json();
}
```

`response.ok`는 상태 코드가 200~299 범위이면 `true`이고, `response.status`는 `200`, `404` 같은 숫자 상태 코드이다. `throw`로 생성한 오류는 현재 함수 실행을 중단하고 반환되는 Promise를 거부 상태로 만든다.

## 19.3 오류 처리

`try...catch`는 `await`한 Promise가 거부되거나 코드에서 `throw`한 오류를 처리한다. 네트워크 연결 실패와 직접 발생시킨 HTTP 오류를 한곳에서 처리해 사용자에게 실패 메시지를 보여 줄 수 있다.

```javascript
async function loadUsers() {
  try {
    const users = await fetchUsers();
    console.log(users);
  } catch (error) {
    console.error("사용자 조회에 실패했습니다.");
    console.error(error.message);
  }
}
```

`catch`의 `error` 매개변수에는 발생한 오류 객체가 전달되고, `error.message`로 오류 메시지를 읽을 수 있다. `fetch()`는 네트워크 오류에서는 거부되지만 HTTP 404·500만으로는 거부되지 않으므로 앞 절처럼 상태 검사를 함께 작성해야 한다.

## 19.4 POST 요청

POST 요청은 `fetch(주소, 옵션)`의 두 번째 인수에 HTTP 메서드, 헤더, 본문을 지정한다. JavaScript 객체를 JSON으로 보낼 때는 `JSON.stringify()`로 문자열로 변환하고 `Content-Type` 헤더를 `application/json`으로 설정한다.

```javascript
async function createUser(user) {
  const response = await fetch("/api/users", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(user),
  });

  if (!response.ok) {
    throw new Error(`HTTP 오류: ${response.status}`);
  }

  return response.json();
}
```

`JSON.stringify(user)`는 객체를 JSON 문자열로 변환한다. `createUser()`는 `async` 함수이므로 서버 응답의 JSON 값으로 처리되는 Promise를 반환한다.

사용 예:

```javascript
const newUser = {
  name: "홍길동",
  age: 20,
};

createUser(newUser)
  .then(result => console.log(result))
  .catch(error => console.error(error));
```

`then()`에는 Promise가 성공했을 때 실행할 함수를, `catch()`에는 실패했을 때 실행할 함수를 전달한다. 두 메서드 모두 새 Promise를 반환하므로 여러 비동기 작업을 이어서 연결할 수 있다.

## 19.5 응답 객체

`fetch()`가 성공하면 HTTP 응답 정보를 담은 `Response` 객체를 반환한다. 상태 코드와 헤더는 속성으로 확인하고, 응답 본문은 데이터 형식에 맞는 메서드로 비동기 변환한다.

주요 속성과 메서드는 다음과 같다.

| 항목 | 설명 |
|---|---|
| `response.ok` | 상태 코드가 200~299 범위인지 불리언 값으로 나타냄 |
| `response.status` | HTTP 상태 코드를 숫자로 반환 |
| `response.headers` | 응답 헤더를 다루는 `Headers` 객체를 반환 |
| `response.json()` | JSON 응답을 JavaScript 값으로 변환하는 Promise를 반환 |
| `response.text()` | 응답 본문을 문자열로 변환하는 Promise를 반환 |
| `response.blob()` | 파일이나 이미지 본문을 `Blob`으로 변환하는 Promise를 반환 |

응답 본문은 스트림이므로 일반적으로 한 번만 읽을 수 있다. 같은 `Response`에서 `json()`을 호출한 뒤 다시 `text()`를 호출하면 본문이 이미 사용되어 오류가 발생한다.

---

# 20. 종합 실습

다음 예제는 사용자 배열을 목록으로 출력하고 검색창의 입력값에 따라 이름이 일치하는 사용자만 다시 표시하는 프로그램이다. 배열 메서드, DOM 요소 생성, 이벤트 처리 과정을 하나의 흐름으로 연결한다.

## 20.1 사용자 목록 검색 프로그램

프로그램은 HTML에서 검색 입력창과 결과 목록 영역을 만들고, JavaScript에서 사용자 데이터를 필터링하여 `ul` 요소 안에 `li` 요소로 출력한다. 입력값이 바뀔 때마다 검색 함수와 출력 함수를 차례로 호출한다.

### HTML

HTML은 검색어를 입력할 `searchInput`과 사용자 항목이 들어갈 빈 `userList`를 정의한다. `type="module"` 스크립트는 HTML 분석을 막지 않고 실행되며 모듈 문법을 사용할 수 있게 한다.

```html
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>사용자 검색</title>
  <script type="module" src="./main.js"></script>
</head>
<body>
  <h1>사용자 목록</h1>

  <label>
    이름 검색
    <input id="searchInput" type="search">
  </label>

  <ul id="userList"></ul>
</body>
</html>
```

`label` 안에 입력 요소를 넣으면 화면의 "이름 검색" 문구와 입력창이 연결된다. `ul`은 처음에는 비어 있으며 JavaScript가 사용자별 `li`를 생성해 추가한다.

### JavaScript

JavaScript는 사용자 데이터를 배열로 보관하고, 검색어가 바뀔 때 조건에 맞는 새 배열을 만든 뒤 목록을 다시 그린다. `renderUsers()`는 화면 출력을 담당하고 `searchUsers()`는 데이터 검색을 담당한다.

```javascript
const users = [
  { id: 1, name: "홍길동", age: 20, active: true },
  { id: 2, name: "이순신", age: 25, active: false },
  { id: 3, name: "강감찬", age: 30, active: true },
];

const searchInput = document.querySelector("#searchInput");
const userList = document.querySelector("#userList");

/**
 * 사용자 배열을 목록 요소에 출력한다.
 *
 * @param {Array<{id: number, name: string, age: number, active: boolean}>} items
 * 출력할 사용자 배열
 * @returns {void}
 */
function renderUsers(items) {
  userList.innerHTML = "";

  items.forEach(user => {
    const item = document.createElement("li");

    const status = user.active ? "활성" : "비활성";
    item.textContent = `${user.name} (${user.age}세, ${status})`;

    userList.append(item);
  });
}

/**
 * 검색어가 이름에 포함된 사용자를 반환한다.
 *
 * @param {string} keyword 검색어
 * @returns {Array<{id: number, name: string, age: number, active: boolean}>}
 * 검색 결과
 */
function searchUsers(keyword) {
  const normalizedKeyword = keyword.trim().toLowerCase();

  return users.filter(user =>
    user.name.toLowerCase().includes(normalizedKeyword)
  );
}

searchInput.addEventListener("input", event => {
  const filteredUsers = searchUsers(event.target.value);

  renderUsers(filteredUsers);
});

renderUsers(users);
```

`renderUsers(items)`는 출력할 사용자 배열을 인수로 받고 반환값 없이 DOM 목록을 갱신한다. 먼저 `innerHTML = ""`로 기존 항목을 비운 다음 `forEach()`로 각 사용자의 `li`를 만들어 `append()`로 추가한다.

`searchUsers(keyword)`는 검색어 문자열을 인수로 받고 이름에 검색어가 포함된 사용자만 담은 새 배열을 반환한다. `trim()`과 `toLowerCase()`로 검색어를 정리하고, `filter()`와 `includes()`로 포함 여부를 검사한다.

`input` 이벤트가 발생하면 현재 입력값으로 사용자를 검색한 뒤 결과 배열을 다시 출력한다. 마지막의 `renderUsers(users)`는 페이지가 처음 표시될 때 전체 사용자 목록을 한 번 출력한다.

## 20.2 실습에서 사용한 문법

다음 문법과 API가 사용자 데이터의 선언, 검색, 화면 출력, 입력 이벤트 처리에 사용되었다. 각 항목이 예제에서 맡은 역할을 함께 살펴보면 전체 실행 흐름을 이해하기 쉽다.

- `const`: 다시 대입하지 않을 변수에 사용자 배열, DOM 요소, 계산 결과를 저장한다.
- 객체와 배열: 여러 사용자의 속성을 구조화해 하나의 목록으로 관리한다.
- 함수: 화면 출력과 검색 작업을 각각 독립된 코드로 묶는다.
- 화살표 함수: 이벤트 처리 함수와 배열 메서드에 전달할 콜백 함수를 간결하게 작성한다.
- 삼항 연산자: `active` 값에 따라 `"활성"` 또는 `"비활성"` 문자열을 선택한다.
- `forEach()`: 배열의 각 사용자를 순서대로 처리하며 반환값은 없다.
- `filter()`: 조건식이 `true`인 사용자만 모아 새 배열을 반환한다.
- `includes()`: 이름 문자열에 검색어가 포함되어 있는지 불리언 값으로 반환한다.
- DOM 요소 선택: `querySelector()`로 입력창과 목록 요소를 찾는다.
- DOM 요소 생성: `createElement()`와 `append()`로 사용자별 목록 항목을 만든다.
- 이벤트 처리: `addEventListener()`로 검색어가 바뀔 때 실행할 함수를 등록한다.

## 20.3 확장 과제

다음 항목은 현재 검색 프로그램에 데이터 필터링, 정렬, 입력, 삭제, 서버 통신, 상태 표시 기능을 추가하는 예이다. 각 기능은 기존 `users` 데이터와 `renderUsers()` 흐름을 확장하여 구현할 수 있다.

1. 활성 사용자만 표시하는 체크박스
2. 나이순 정렬 버튼
3. 사용자 추가 폼
4. 사용자 삭제 버튼
5. `fetch()`를 이용한 서버 데이터 조회
6. 로딩 중 메시지와 오류 메시지 표시

체크박스는 `checked`와 `filter()`, 정렬 버튼은 `sort()`, 사용자 폼은 `FormData`를 활용할 수 있다. 서버 조회를 추가할 때는 요청 중·성공·실패 상태에 따라 화면 메시지를 갱신한다.

---

# 참고 자료

다음 자료는 JavaScript 문법과 브라우저 API의 세부 동작을 확인하거나 이후 프레임워크 사용법으로 범위를 넓힐 때 참고할 수 있다. API의 인수와 반환값처럼 정확한 명세가 필요할 때는 공식 문서를 우선 확인하는 것이 좋다.

- MDN JavaScript 안내서: JavaScript 문법과 DOM, 이벤트, Fetch API의 표준 사용법을 확인할 수 있다.
- 모던 JavaScript 튜토리얼: JavaScript 개념을 주제별 설명과 예제로 복습할 수 있다.
- React 공식 문서: JavaScript로 구성 요소 기반 사용자 인터페이스를 만드는 방법을 확인할 수 있다.
- Vue.js 공식 문서: 템플릿과 반응형 데이터를 이용해 사용자 인터페이스를 구성하는 방법을 확인할 수 있다.

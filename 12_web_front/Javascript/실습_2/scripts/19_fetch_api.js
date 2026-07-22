// 연습용 무료 API 서버 주소
const API_BASE_URL = "https://jsonplaceholder.typicode.com";

// 19.1 GET 요청 + 19.2 HTTP 상태 확인 + 19.5 응답 객체
const getUsersButton = document.querySelector("#get-users-button");
const getStatus = document.querySelector("#get-status");
const userList = document.querySelector("#user-list");

async function fetchUsers() {
  const response = await fetch(`${API_BASE_URL}/users`);

  // 19.5 응답 객체의 주요 속성 확인
  console.log("response.ok:", response.ok);
  console.log("response.status:", response.status);

  if (!response.ok) {
    throw new Error(`HTTP 오류: ${response.status}`);
  }

  return response.json();
}

async function loadUsers() {
  getStatus.textContent = "불러오는 중...";
  userList.innerHTML = "";

  try {
    const users = await fetchUsers();

    users.forEach(user => {
      const item = document.createElement("li");

      item.textContent = `${user.id}. ${user.name} (${user.email})`;
      userList.append(item);
    });

    getStatus.textContent = `사용자 ${users.length}명을 불러왔습니다.`;
    console.log("조회한 사용자 목록:", users);
  } catch (error) {
    getStatus.textContent = "사용자 조회에 실패했습니다.";
    console.error("오류 메시지:", error.message);
  }
}

// 19.2 HTTP 상태 확인 + 19.3 오류 처리
const errorTestButton = document.querySelector("#error-test-button");
const errorResult = document.querySelector("#error-result");

async function requestWrongUrl() {
  errorResult.textContent = "요청 중...";

  try {
    // 존재하지 않는 주소이므로 404 응답이 온다.
    const response = await fetch(`${API_BASE_URL}/wrong-address`);

    console.log("404여도 fetch 자체는 성공한다. response.ok:", response.ok);

    if (!response.ok) {
      // 상태 코드를 확인해서 직접 오류를 발생시킨다.
      throw new Error(`HTTP 오류: ${response.status}`);
    }

    errorResult.textContent = "요청이 성공했습니다.";
  } catch (error) {
    errorResult.textContent = `오류 발생: ${error.message}`;
    console.error("catch에서 처리한 오류:", error.message);
  }
}

// 19.4 POST 요청
const createPostButton = document.querySelector("#create-post-button");
const titleInput = document.querySelector("#title-input");
const postResult = document.querySelector("#post-result");

async function createPost(post) {
  const response = await fetch(`${API_BASE_URL}/posts`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(post), // 객체를 JSON 문자열로 변환
  });

  if (!response.ok) {
    throw new Error(`HTTP 오류: ${response.status}`);
  }

  return response.json();
}

async function handleCreatePost() {
  postResult.textContent = "등록 중...";

  const newPost = {
    title: titleInput.value,
    body: "실습용 본문입니다.",
    userId: 1,
  };

  try {
    const result = await createPost(newPost);

    postResult.textContent = `등록 성공! 서버가 부여한 글 번호: ${result.id}`;
    console.log("서버 응답 결과:", result);
  } catch (error) {
    postResult.textContent = "글 등록에 실패했습니다.";
    console.error("오류 메시지:", error.message);
  }
}

// 이벤트 등록
getUsersButton.addEventListener("click", loadUsers);
errorTestButton.addEventListener("click", requestWrongUrl);
createPostButton.addEventListener("click", handleCreatePost);

const add_btn = document.querySelector("#choice-add-btn");
const del_btn = document.querySelector("#choice-del-btn");
// 보기 추가 버튼 이벤트 처리.
add_btn.addEventListener("click", () => {
    // input[name$='choice_text']: input 태그중, name 속성의 값이 choice_text로 끝나는것
    // ^= : 시작하는것, *=: 포함하는 것, $=: 끝나는 것. = : 일치
    const choice_text_cnt = document.querySelectorAll("input[name$='choice_text']").length;
    const choice_text_input_name = `form-${choice_text_cnt}-choice_text`;


    const div = document.createElement("div"); // <div></div>
    const input = document.createElement("input"); // <input>
    input.setAttribute("type", "text"); // <input type="text" >
    input.setAttribute("name", choice_text_input_name);
    input.setAttribute("id", `id_${choice_text_input_name}`);
    input.setAttribute("required", true);

    //class: form-control 추가
    input.classList.add('form-control');

    div.append(input);//<div><input..></div>
    document.querySelector("#choice-layer").append(div);//choice layer에 생성한 div추가

    // TOTAL_FORMS 의 value를 1 증가
    const totalForms = document.querySelector("#id_form-TOTAL_FORMS");
    totalForms.value = parseInt(totalForms.value) + 1
}); 

// 보기 삭제 버튼 event 처리
del_btn.addEventListener("click", ()=>{
    // 보기 input 하나를 삭제. 
    // 보기 input은 최소 두개는 유지(두개 이하일 경우는 삭제하지 않는다.)
    const choice_layer = document.querySelector("#choice-layer");
    // Node.children : 자식노드들을 nodelist로 반환.
    if (choice_layer.children.length > 2) {
        // 부모노드.removeChild(삭제할자식노드)
        // 부모노드.lastChild -> 마지막 자식 노드반환. 
        choice_layer.removeChild(choice_layer.lastChild);
        // TOTAL_FORMS 의 value를 1 감소
        const totalForms = document.querySelector("#id_form-TOTAL_FORMS");
        totalForms.value = parseInt(totalForms.value) - 1;
    } else {
        // 경고창 (alert("메세지"))
        alert("보기는 세개 이상일 경우만 삭제할 수 있습니다.")
    }

});
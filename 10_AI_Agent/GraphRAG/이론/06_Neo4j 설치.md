# 6. Neo4j 사용하기


## 6.1 Neo4j Aura DB 기본 사용법

**Neo4j Aura**는 Neo4j가 제공하는 클라우드 관리형 그래프 DB 서비스다. 별도 설치 없이 브라우저에서 바로 사용할 수 있어 실습에 적합하다.

**AuraDB Free 인스턴스 생성**

1. [https://console.neo4j.io](https://console.neo4j.io) 접속 후 회원가입(구글 계정 사용 가능)
2. **New Instance** → **AuraDB Free** 선택
3. 인스턴스 이름 지정 후 **Create** 클릭
4. 생성 직후 표시되는 **Username / Password / Connection URI** 를 반드시 저장한다.
   - 이 정보는 이후 다시 확인할 수 없으므로 안전한 곳에 보관한다.
5. 인스턴스 상태가 `Running`으로 바뀌면 사용 가능하다.

**접속 정보 예시**

```
URI:      neo4j+s://xxxx.databases.neo4j.io
Username: neo4j
Password: (생성 시 제공된 임의 비밀번호)
```

**AuraDB Free(무료) 제한사항**

| 항목 | 제한 |
|------|------|
| 노드 수 | 50,000개 |
| 관계 수 | 175,000개 |
| 스토리지 | 약 200MB |
| 인스턴스(DB) 수 | 1개 |


## 6.2 Neo4j Desktop 설치

- Neo4j Desktop은 로컬에서 Neo4j를 실행할 수 있는 GUI 애플리케이션이다. 인터넷 없이 Local에 설치해서 사용 가능하고, DB 생성 개수 제한 없이 사용할 수 있다.
- [설치 가이드 문서](https://neo4j.com/docs/desktop/current/installation/)

### 설치 방법

1. [https://neo4j.com/download/](https://neo4j.com/download/) 에서 OS에 맞는 설치 파일 다운로드
   - 개인 정보 입력 후 다운로드 
2. 설치 완료 후 실행
3. 최초 실행 시 활성화 키(Activation Key) 입력 → 다운로드 페이지에서 이메일로 받은 키 사용
4. **Projects** → **New Project** → **Add** → **Local DBMS** 로 새 DB 생성
5. 생성한 DB 옆 **Start** 버튼으로 실행

## 주의

db instance 생성 후
- apoc 플러그인 install 
- open > neo4j.config  에 `dbms.security.procedures.unrestricted=apoc.*,apoc.meta.*` 설정. apoc.meta.* 추가
# 🐳 Docker 입문

## 1. Docker란 무엇인가?

### 1.1 Docker 개요

Docker는 애플리케이션을 **컨테이너(Container)** 라는 독립된 실행환경에 패키징해 어디서든 동일하게 실행할 수 있도록 도와주는 **오픈소스 플랫폼**이다.    
흔히 "내 PC에서는 되는데 서버에서 안 된다"는 문제를 해결하기 위해 탄생했다. 즉 Docker를 쓰면 개발자 컴퓨터, 테스트 서버, 운영 서버등 여러 다른 플랫폼에서 최대한 같은 환경으로 실행할 수 있다.


### 1.2 가상 머신(VM)과의 차이

Docker 컨테이너는 **가상 머신(VM)** 과 자주 비교된다.

| 항목 | 가상 머신 (VM) | Docker 컨테이너 |
|------|--------------|----------------|
| 운영체제 | OS 전체를 포함 (수 GB) | 호스트 OS 커널 공유 (수 MB) |
| 시작 시간 | 수 분 | 수 초 |
| 리소스 사용 | 무거움 | 가벼움 |
| 격리 수준 | 완전한 독립 OS | 프로세스 수준 격리 |
| 이식성 | 이미지 크기가 큼 | 이미지가 작고 빠름 |

### 1.3 Docker 핵심 개념 3가지

#### 이미지 (Image)

- 컨테이너를 만들기 위한 **'설계도'** 또는 **'틀'** 이다.
- Docker Hub에 미리 만들어진 이미지가 수십만 개 공개되어 있다.
- 예) `ubuntu`, `nginx`, `mysql`, `python` 등

#### 컨테이너 (Container)

- 이미지를 실제로 **실행한 '인스턴스'** 이다.
- 한 이미지로 여러 컨테이너를 동시에 실행할 수 있다.
- 프로세스처럼 시작 · 중지 · 삭제가 가능하다.

#### Docker Hub

- 이미지를 저장하고 공유하는 **'중앙 저장소(Registry)'** 이다.
- GitHub의 이미지 버전이라고 생각하면 된다.
- <https://hub.docker.com> 에서 검색할 수 있다.

### 1.4 Docker의 필요성

- **환경 일관성** : 개발 · 테스트 · 운영 환경을 완전히 동일하게 유지한다.
- **빠른 시작** : 복잡한 소프트웨어(DB, 웹서버 등)를 명령어 한 줄로 실행한다.
- **이식성** : OS에 관계없이 어디서나 동일하게 동작한다.
- **업계 표준** : 현재 개발/DevOps 분야의 필수 기술이다.


## 2. Docker 설치

Docker Desktop은 Windows와 macOS 모두에서 **GUI와 CLI를 함께 제공**하는 공식 설치 패키지이다.

### 2.1 Windows 설치

#### 시스템 요구사항

| 항목 | 요구사항 |
|------|---------|
| 운영체제 | Windows 10 64-bit (버전 1903 이상) 또는 Windows 11 |
| WSL2 | WSL2(Windows Subsystem for Linux 2) 활성화 필요 |
| 가상화 | BIOS에서 가상화(Virtualization) 활성화 필요 |
| RAM | 최소 4GB (8GB 권장) |

#### 설치 단계

1. Docker 공식 사이트에 접속한다 : <https://www.docker.com/products/docker-desktop>
2. **"Download for Windows"** 버튼을 클릭해 `Docker Desktop Installer.exe`를 다운로드한다.
3. 다운로드된 설치 파일을 실행하고 설치 마법사 안내에 따라 진행한다.
4. 설치 중 **"Use WSL 2 instead of Hyper-V"** 옵션을 체크한다 (권장).
5. 설치 완료 후 PC를 재시작한다.
6. 바탕화면 또는 시작 메뉴에서 Docker Desktop을 실행한다.

> ⚠️ **WSL2 관련 오류 발생 시**
>
> PowerShell을 **관리자 권한**으로 실행한 후 아래 명령어를 입력한다.
>
> ```powershell
> wsl --install
> wsl --set-default-version 2
> ```
>
> 설치 후 PC를 재시작하면 해결되는 경우가 대부분이다.

### 2.2 macOS 설치

#### 설치 단계

1. Docker 공식 사이트에 접속한다 : <https://www.docker.com/products/docker-desktop>
2. 본인 Mac에 맞는 버전을 선택한다.
   - Apple Silicon (M1/M2/M3) → **"Download for Mac – Apple Silicon"**
   - Intel → **"Download for Mac – Intel Chip"**
3. 다운로드된 `Docker.dmg` 파일을 실행한다.
4. Docker 아이콘을 **Applications** 폴더로 드래그한다.
5. Applications에서 Docker를 실행한다.

### 2.3 설치 확인

설치가 완료되면 터미널(명령 프롬프트)을 열고 아래 명령어로 설치를 확인한다.

```bash
# Docker 버전 확인
docker --version

# 출력 예시
Docker version 26.1.0, build a72a000

# Docker 정상 동작 확인 (Hello World 실행)
docker run hello-world
```

> **성공 메시지 확인**
>
> `"Hello from Docker!"` 메시지가 출력되면 설치가 완료된 것이다.
> 이 명령어는 `hello-world` 이미지를 Hub에서 자동으로 내려받아 컨테이너로 실행한다.


## 3. Docker 기본 명령어

Docker의 모든 명령어는 `docker` 로 시작한다. 입문 단계에서 꼭 알아야 할 명령어만 정리한다.


### 3.1 명령어 전체 흐름

이미지를 받아서 컨테이너로 실행하는 흐름은 아래와 같다.

```
Docker Hub
    │
    ├─ 이미지 검색    docker search
    ├─ 이미지 다운로드 docker pull
    ├─ 컨테이너 실행  docker run
    ├─ 목록 확인      docker ps
    ├─ 컨테이너 중지  docker stop
    └─ 삭제          docker rm / docker rmi
```

### 3.2 이미지 관련 명령어

#### 이미지 검색 — `docker search`

```bash
docker search <검색어>

# 예시 : nginx 이미지 검색
docker search nginx
```

Docker Hub에서 이미지를 검색한다. **STARS 수가 높을수록** 많이 사용되는 검증된 이미지이다.

#### 이미지 다운로드 — `docker pull`

```bash
docker pull <이미지이름>:<태그>

# 예시 : 최신 nginx 이미지 다운로드
docker pull nginx

# 특정 버전 다운로드
docker pull nginx:1.25

# Ubuntu 22.04 다운로드
docker pull ubuntu:22.04
```

> 💡 **태그(Tag)란?**
>
> 이미지 이름 뒤에 콜론(`:`)으로 붙이는 버전 표시이다.
> 태그를 생략하면 자동으로 `:latest` (최신 버전)이 다운로드된다.
> 예) `nginx:latest`, `ubuntu:22.04`, `python:3.11-slim`


#### 로컬 이미지 목록 조회 — `docker images`

```bash
docker images

# 출력 예시
REPOSITORY   TAG       IMAGE ID       CREATED        SIZE
nginx        latest    a6bd71f48f68   2 weeks ago    187MB
ubuntu       22.04     52882761a72a   4 weeks ago    77.9MB
```

#### 이미지 삭제 — `docker rmi`

```bash
docker rmi <이미지이름 또는 IMAGE ID>

# 예시
docker rmi nginx
docker rmi a6bd71f48f68
```

### 3.3 컨테이너 실행 — `docker run`

가장 중요한 명령어이다. 이미지를 컨테이너로 실행한다.

```bash
docker run [옵션] <이미지이름> [명령어]

# 가장 기본적인 실행
docker run nginx

# 자주 쓰는 옵션 조합
docker run -d -p 8080:80 --name my-nginx nginx
```

#### 주요 옵션 설명

| 옵션 | 의미 |
|------|------|
| `-d` | 백그라운드(detached) 모드로 실행한다 — 터미널이 점유되지 않는다 |
| `-p 호스트포트:컨테이너포트` | 포트를 연결한다. `-p 8080:80` 이면 브라우저에서 `localhost:8080`으로 접근한다 |
| `--name 이름` | 컨테이너에 이름을 지정한다 (미지정 시 랜덤 이름이 자동 부여된다) |
| `-it` | 인터랙티브 모드로 실행한다. 터미널로 직접 컨테이너 내부를 조작할 때 사용한다 |
| `--rm` | 컨테이너 종료 시 자동으로 컨테이너가 삭제된다 |

### 3.4 컨테이너 관리 명령어

#### 실행 중인 컨테이너 목록 — `docker ps`

```bash
# 현재 실행 중인 컨테이너만 표시한다
docker ps

# 중지된 컨테이너 포함 전체 목록을 표시한다
docker ps -a
```

#### 컨테이너 중지 · 시작 · 재시작

```bash
# 컨테이너를 중지한다
docker stop <컨테이너이름 또는 ID>
docker stop my-nginx

# 중지된 컨테이너를 다시 시작한다
docker start my-nginx

# 컨테이너를 재시작한다
docker restart my-nginx
```

#### 컨테이너 삭제 — `docker rm`

```bash
# 컨테이너를 삭제한다 (중지 후 삭제 가능하다)
docker rm my-nginx

# 실행 중인 컨테이너를 강제 삭제한다
docker rm -f my-nginx
```

#### 컨테이너 로그 확인 — `docker logs`

```bash
# 컨테이너 로그를 출력한다
docker logs my-nginx

# 실시간으로 로그 스트림을 확인한다 (Ctrl+C로 종료한다)
docker logs -f my-nginx
```

### 3.5 명령어 요약표

| 명령어 | 설명 |
|--------|------|
| `docker search <이름>` | Docker Hub에서 이미지를 검색한다 |
| `docker pull <이미지>` | 이미지를 다운로드한다 |
| `docker images` | 로컬에 저장된 이미지 목록을 확인한다 |
| `docker rmi <이미지>` | 이미지를 삭제한다 |
| `docker run [옵션] <이미지>` | 컨테이너를 생성하고 실행한다 |
| `docker ps` | 실행 중인 컨테이너 목록을 확인한다 |
| `docker ps -a` | 전체 컨테이너 목록을 확인한다 (중지 포함) |
| `docker stop <컨테이너>` | 컨테이너를 중지한다 |
| `docker start <컨테이너>` | 컨테이너를 시작한다 |
| `docker rm <컨테이너>` | 컨테이너를 삭제한다 |
| `docker logs <컨테이너>` | 컨테이너 로그를 확인한다 |

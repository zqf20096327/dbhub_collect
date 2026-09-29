# WY Components — Backend Server

> `my-components` 프론트엔드 프로젝트의 REST API + Socket.IO 서버  
> **Node.js + Express + Socket.IO + TiDB Cloud (MySQL)**

---

## 목차

1. [프로젝트 개요](#1-프로젝트-개요)
2. [기술 스택](#2-기술-스택)
3. [프로젝트 구조](#3-프로젝트-구조)
4. [설치 및 실행](#4-설치-및-실행)
5. [환경변수](#5-환경변수)
6. [DB 구조 (TiDB Cloud)](#6-db-구조-tidb-cloud)
7. [API 명세](#7-api-명세)
8. [Socket.IO 이벤트](#8-socketio-이벤트)
9. [인증 구조 (JWT)](#9-인증-구조-jwt)
10. [주요 구현 포인트](#10-주요-구현-포인트)
11. [배포 (Railway)](#11-배포-railway)

---

## 1. 프로젝트 개요

`my-components-server`는 WY Components 프론트엔드와 연동하는 백엔드 서버입니다.

- REST API: 게시판 · 댓글 · 캘린더 · 채팅 · 설문 · 파일 업로드 · 인증
- 실시간 채팅: Socket.IO (메시지 저장 + 브로드캐스트)
- DB: TiDB Cloud Serverless (MySQL 호환, 무료 플랜)
- 인증: JWT (헤더 `X-AUTH-TOKEN`)
- **배포 주소**: https://my-components-server.onrender.com (Render Free) — 프론트엔드: https://my-components-eta.vercel.app ([저장소](https://github.com/elese0821/my-components))

---

## 2. 기술 스택

| 패키지 | 버전 | 용도 |
|---|---|---|
| Node.js | 18+ | 런타임 |
| Express | 4.18 | REST API 서버 프레임워크 |
| Socket.IO | 4.7 | 웹소켓 실시간 채팅 |
| mysql2 | 3.9 | TiDB Cloud (MySQL) 연결 풀 |
| jsonwebtoken | 9.0 | JWT 발급 · 검증 |
| bcrypt | 5.1 | 비밀번호 해싱 (salt 10) |
| multer | 1.4 | 멀티파트 파일 업로드 |
| uuid | 9.0 | 채팅방 채널 ID 생성 |
| cors | 2.8 | CORS 허용 설정 |
| dotenv | 16.4 | 환경변수 로드 |
| nodemon | 3.1 | 개발 자동 재시작 |

---

## 3. 프로젝트 구조

```
my-components-server/
├── src/
│   ├── app.js                   # 앱 진입점 — Express + Socket.IO 초기화
│   ├── db.js                    # mysql2 연결 풀 (TiDB Cloud SSL 지원)
│   ├── socket.js                # Socket.IO 이벤트 핸들러
│   │
│   ├── middleware/
│   │   └── auth.js              # JWT 검증 미들웨어 (authMiddleware)
│   │
│   └── routes/
│       ├── auth.js              # POST /login, POST /regist
│       ├── board.js             # GET/POST/PATCH/DELETE /user/board/info
│       ├── reply.js             # GET/POST/DELETE /user/reply
│       ├── schedule.js          # GET/POST/PATCH/DELETE /user/schedule
│       ├── chat.js              # GET/POST /user/chat, GET /user/chat/:channelId
│       ├── survey.js            # GET/POST/DELETE /user/survey/*
│       └── file.js              # POST /user/file/upload
│
├── uploads/                     # multer 업로드 저장 경로
├── .env                         # 환경변수 (gitignore)
├── .env.example                 # 환경변수 템플릿
└── package.json
```

---

## 4. 설치 및 실행

### 사전 요구사항

- Node.js 18 이상
- TiDB Cloud 계정 및 클러스터 (또는 MySQL 5.7+)

### 설치

```bash
cd my-components-server
npm install
```

### 환경변수 설정

```bash
cp .env.example .env
# .env 파일 편집 (아래 섹션 참조)
```

### DB 초기화

TiDB Cloud SQL Editor 또는 MySQL 클라이언트에서 `schema.sql` 실행:

```bash
# MySQL 클라이언트 예시
mysql -h <host> -P <port> -u <user> -p <database> < schema.sql
```

### 개발 서버 실행

```bash
npm run dev
# nodemon → 코드 변경 시 자동 재시작
# → http://localhost:4000
```

### 프로덕션 실행

```bash
npm start
# → node src/app.js
```

---

## 5. 환경변수

`.env` 파일:

```env
# 서버 포트 (기본 4000)
PORT=4000

# 프론트엔드 URL (CORS 허용 origin)
CLIENT_URL=http://localhost:5173

# JWT 서명 시크릿 (충분히 길고 랜덤한 문자열)
JWT_SECRET=your_very_long_and_random_jwt_secret_key

# TiDB Cloud (MySQL) 접속 정보
DB_HOST=gateway01.ap-northeast-1.prod.aws.tidbcloud.com
DB_PORT=4000
DB_USER=your_tidb_user
DB_PASSWORD=your_tidb_password
DB_NAME=your_database_name
DB_SSL=true
```

> TiDB Cloud는 기본적으로 SSL 연결을 요구합니다. `DB_SSL=true` 설정 필수.

---

## 6. DB 구조 (TiDB Cloud)

### 테이블 목록

| 테이블 | 설명 |
|---|---|
| `users` | 회원 정보 (id, pw_hash, username, email) |
| `board` | 게시글 (title, contents, usr_nm, usr_idx, file_idx, reg_dt, views) |
| `files` | 업로드 파일 (org_nm, save_nm, file_path, reg_dt) |
| `reply` | 댓글 (board_idx, usr_nm, usr_idx, contents, reg_dt) |
| `schedule` | 캘린더 일정 (schedule_title, from_dt, to_dt, color, contents, usr_idx) |
| `chat_room` | 채팅방 (channel_id UUID, chat_nm, last_chat, reg_dt, usr_nm) |
| `chat_message` | 채팅 메시지 (channel_id, usr_idx, usr_nm, contents, chat_type, reg_dt, file_name) |
| `survey` | 설문 (title, contents, finish_survey) |
| `quest` | 설문 질문 (survey_idx, quest_title, quest_desc, quest_type, quest_order_no) |
| `quest_sel` | 질문 선택지 (quest_idx, answer_title, answer_weight, answer_order_no) |
| `user_survey_answer` | 설문 응답 (survey_idx, quest_idx, usr_idx, sel_idx, text_answer) |

### 스키마 예시

```sql
CREATE TABLE users (
    usr_idx   INT AUTO_INCREMENT PRIMARY KEY,
    id        VARCHAR(50)  NOT NULL UNIQUE,
    pw_hash   VARCHAR(255) NOT NULL,
    username  VARCHAR(50)  NOT NULL,
    email     VARCHAR(100),
    reg_dt    DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE board (
    board_idx INT AUTO_INCREMENT PRIMARY KEY,
    title     VARCHAR(200) NOT NULL,
    contents  TEXT,
    usr_nm    VARCHAR(50),
    usr_idx   INT,
    file_idx  INT,
    views     INT DEFAULT 0,
    reply_cnt INT DEFAULT 0,
    reg_dt    DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE files (
    file_idx  INT AUTO_INCREMENT PRIMARY KEY,
    org_nm    VARCHAR(255),
    save_nm   VARCHAR(255),
    file_path VARCHAR(500),
    reg_dt    DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE reply (
    reply_idx INT AUTO_INCREMENT PRIMARY KEY,
    board_idx INT NOT NULL,
    usr_nm    VARCHAR(50),
    usr_idx   INT,
    contents  TEXT,
    reg_dt    DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE schedule (
    schedule_idx   INT AUTO_INCREMENT PRIMARY KEY,
    schedule_title VARCHAR(200) NOT NULL,
    from_dt        DATE,
    to_dt          DATE,
    color          VARCHAR(20) DEFAULT '#3b82f6',
    contents       TEXT,
    usr_idx        INT,
    reg_dt         DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE chat_room (
    channel_id VARCHAR(36) PRIMARY KEY,   -- UUID
    chat_nm    VARCHAR(100) NOT NULL,
    last_chat  VARCHAR(300),
    reg_dt     VARCHAR(20),
    usr_nm     VARCHAR(50)
);

CREATE TABLE chat_message (
    msg_idx   INT AUTO_INCREMENT PRIMARY KEY,
    channel_id VARCHAR(36) NOT NULL,
    usr_idx   INT,
    usr_nm    VARCHAR(50),
    contents  TEXT,
    chat_type VARCHAR(5) DEFAULT 'C',     -- C: 채팅, F: 파일
    reg_dt    VARCHAR(20),
    file_name VARCHAR(255)
);

CREATE TABLE survey (
    survey_idx   INT AUTO_INCREMENT PRIMARY KEY,
    title        VARCHAR(200) NOT NULL,
    contents     TEXT,
    finish_survey VARCHAR(1) DEFAULT 'N', -- Y: 완료
    reg_dt       DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE quest (
    quest_idx      INT AUTO_INCREMENT PRIMARY KEY,
    survey_idx     INT NOT NULL,
    quest_title    VARCHAR(300) NOT NULL,
    quest_desc     VARCHAR(500),
    quest_type     VARCHAR(2) DEFAULT 'S',  -- S: 선택, T: 주관식
    quest_order_no INT DEFAULT 0
);

CREATE TABLE quest_sel (
    sel_idx         INT AUTO_INCREMENT PRIMARY KEY,
    quest_idx       INT NOT NULL,
    answer_title    VARCHAR(200) NOT NULL,
    answer_weight   INT DEFAULT 0,
    answer_order_no INT DEFAULT 0
);

CREATE TABLE user_survey_answer (
    answer_idx  INT AUTO_INCREMENT PRIMARY KEY,
    survey_idx  INT NOT NULL,
    quest_idx   INT NOT NULL,
    usr_idx     INT NOT NULL,
    sel_idx     INT,
    text_answer TEXT,
    UNIQUE KEY uq_answer (quest_idx, usr_idx)  -- ON DUPLICATE KEY UPDATE 활용
);
```

---

## 7. API 명세

### 인증 (auth.js)

#### `POST /login`

로그인 → JWT 발급

```json
// Request Body
{ "id": "test", "pw": "Test1234!" }

// Response (성공)
{
    "result": "success",
    "username": "테스터",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "USR_IDX": "1"
}
```

#### `POST /regist`

회원가입

```json
// Request Body
{ "id": "newuser", "pw": "Pass1234!", "usrNm": "홍길동", "email": "hong@example.com" }

// Response
{ "result": "success", "msg": "회원가입이 완료되었습니다." }
```

---

### 게시판 (board.js)

모든 경로: `/user/board/info`

#### `GET /user/board/info` — 목록 또는 단건

```
// 목록 조회
GET /user/board/info?row=10&pageNo=1&searchStr=키워드

// 단건 조회 (+ 조회수 +1)
GET /user/board/info?boardIdx=3
```

```json
// 목록 Response
{ "result": "success", "list": [...], "total": 30 }

// 단건 Response
{ "result": "success", "one": { "boardIdx": 3, "title": "...", "regDt": "2024-01-15", ... } }
```

**목록 필드**: `boardIdx, title, usrNm, usrIdx, replyCnt, views, regDt, fileOrgNm, fileIdx`  
**단건 추가 필드**: `contents`

> `regDt`는 `COALESCE(DATE_FORMAT(reg_dt, '%Y-%m-%d'), DATE_FORMAT(NOW(), '%Y-%m-%d'))` 로 NULL 처리됨.

#### `POST /user/board/info` 🔒 — 게시글 작성

```json
// Request Body
{ "title": "제목", "contents": "<p>내용</p>", "fileIdx": 5 }
```

#### `PATCH /user/board/info` 🔒 — 게시글 수정

```json
{ "boardIdx": 3, "title": "수정 제목", "contents": "<p>수정 내용</p>" }
```

#### `DELETE /user/board/info` 🔒 — 게시글 삭제

```
DELETE /user/board/info?boardIdx=3
```

---

### 댓글 (reply.js)

#### `GET /user/reply?boardIdx=3`

```json
{ "result": "success", "list": [{ "replyIdx": 1, "usrNm": "홍길동", "contents": "댓글 내용", "regDt": "..." }] }
```

#### `POST /user/reply` 🔒

```json
{ "boardIdx": 3, "contents": "댓글 내용" }
```

#### `DELETE /user/reply` 🔒

```
DELETE /user/reply?replyIdx=1
```

---

### 캘린더 (schedule.js)

#### `GET /user/schedule` 🔒

```json
{
    "result": "success",
    "list": [
        {
            "scheduleIdx": 1,
            "scheduleTitle": "회의",
            "fromDt": "2024-06-10",
            "toDt": "2024-06-10",
            "color": "#3b82f6",
            "contents": "메모"
        }
    ]
}
```

#### `POST /user/schedule` 🔒

```json
{ "scheduleTitle": "회의", "fromDt": "2024-06-10", "toDt": "2024-06-10", "color": "#ef4444", "contents": "메모" }
```

#### `PATCH /user/schedule` 🔒

```json
{ "scheduleIdx": 1, "scheduleTitle": "회의 수정", "fromDt": "2024-06-11", "toDt": "2024-06-11", "color": "#10b981" }
```

#### `DELETE /user/schedule` 🔒

```
DELETE /user/schedule?scheduleIdx=1
```

---

### 채팅 (chat.js)

#### `GET /user/chat` 🔒 — 채팅방 목록

```json
{
    "result": "success",
    "list": [{ "channelId": "uuid-...", "chatNm": "일반 채팅", "lastChat": "안녕!", "regDt": "2024-06-01 10:30", "usrNm": "홍길동" }]
}
```

#### `POST /user/chat` 🔒 — 채팅방 생성

```json
// Request
{ "chatNm": "새 채팅방" }

// Response
{ "result": "success", "channelId": "550e8400-e29b-41d4-a716-446655440000" }
```

#### `GET /user/chat/:channelId` 🔒 — 채팅 기록 조회

```json
{
    "result": "success",
    "list": [
        { "msgIdx": 1, "channelId": "...", "usrIdx": 1, "usrNm": "홍길동",
          "contents": "안녕하세요!", "chatType": "C", "regDt": "2024-06-01 10:30", "fileName": null }
    ]
}
```

---

### 설문 (survey.js)

#### `GET /user/survey/info` — 목록

```json
{ "result": "success", "list": [{ "surveyIdx": 1, "title": "만족도 조사", "contents": "...", "finishSurvey": "N" }] }
```

#### `GET /user/survey/info?surveyIdx=1` — 단건 (질문+선택지)

```json
{
    "result": "success",
    "one": [
        {
            "questIdx": 1, "questOrderNo": 1, "questTitle": "만족도는?",
            "questType": "S", "selIdx": 1, "answerTitle": "매우 만족", "answerWeight": 5, "userAnswer": ""
        }
    ]
}
```

#### `POST /user/survey/create` 🔒 — 설문 생성 (트랜잭션)

```json
{
    "title": "만족도 조사",
    "contents": "설명",
    "questions": [
        {
            "questTitle": "서비스 만족도는?",
            "questType": "S",
            "orderNo": 1,
            "options": [
                { "answerTitle": "매우 만족", "answerWeight": 5, "orderNo": 1 },
                { "answerTitle": "만족",      "answerWeight": 4, "orderNo": 2 }
            ]
        },
        {
            "questTitle": "개선 의견을 작성해주세요.",
            "questType": "T",
            "orderNo": 2
        }
    ]
}
```

> `survey → quest → quest_sel` 을 하나의 트랜잭션으로 처리.  
> 실패 시 전체 롤백.

#### `POST /user/survey/info` 🔒 — 설문 응답 제출

```json
{
    "surveyIdx": 1,
    "contents": [
        { "questIdx": 1, "questType": "S", "answers": 1 },
        { "questIdx": 2, "questType": "T", "answers": "좋았습니다." }
    ]
}
```

> `ON DUPLICATE KEY UPDATE` 로 재응답(수정) 허용.  
> 제출 완료 후 `survey.finish_survey = 'Y'` 로 업데이트.

#### `DELETE /user/survey/info` 🔒

```
DELETE /user/survey/info?surveyIdx=1
```

---

### 파일 업로드 (file.js)

#### `POST /user/file/upload` 🔒

`multipart/form-data` 형식으로 파일 전송.

```
Content-Type: multipart/form-data
Body: file (파일 바이너리)
```

```json
// Response
{ "result": "success", "fileIdx": 7, "fileOrgNm": "원본파일명.jpg", "filePath": "/uploads/uuid-저장명.jpg" }
```

---

## 8. Socket.IO 이벤트

### 서버 → 클라이언트

| 이벤트명 | 데이터 | 설명 |
|---|---|---|
| `message` | `{ channelId, usrIdx, usrNm, contents, chatType, regDt, fileName }` | 새 메시지 수신 |

### 클라이언트 → 서버

| 이벤트명 | 데이터 | 설명 |
|---|---|---|
| `join` | `{ channelId }` | 채팅방 입장 (Socket.IO Room join) |
| `message` | `{ channelId, usrIdx, usrNm, contents, chatType, fileName }` | 메시지 전송 |

### 메시지 흐름

```
클라이언트 A                서버                 클라이언트 B
    │                         │                         │
    │──── emit('join') ───────▶│                         │
    │                         │──── socket.join(room)   │
    │                         │                         │
    │──── emit('message') ────▶│                         │
    │                         │── INSERT chat_message   │
    │                         │── UPDATE chat_room      │
    │                         │                         │
    │  (자신은 로컬에서 추가)  │──── emit('message') ───▶│
    │                         │  (socket.to → 발신자 제외)
```

> `io.to(room).emit()` 대신 `socket.to(room).emit()` 사용.  
> **발신자는 자신이 보낸 메시지를 로컬에서 즉시 추가하고, 서버는 나머지 클라이언트에게만 브로드캐스트.**

---

## 9. 인증 구조 (JWT)

### 발급

`POST /login` 성공 시:

```js
const token = jwt.sign(
    { usrIdx: user.usr_idx, id: user.id, username: user.username },
    process.env.JWT_SECRET,
    { expiresIn: '7d' }
);
```

### 검증 미들웨어 (`authMiddleware`)

```js
export function authMiddleware(req, res, next) {
    const token = req.headers['x-auth-token'];
    if (!token || token === 'null') {
        return res.status(401).json({ result: 'fail', message: '로그인이 필요합니다.' });
    }
    try {
        const decoded = jwt.verify(token, process.env.JWT_SECRET);
        req.user = decoded;  // { usrIdx, id, username }
        next();
    } catch {
        return res.status(401).json({ result: 'fail', message: '세션이 만료되었습니다.' });
    }
}
```

### 헤더 이름

```
X-AUTH-TOKEN: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

프론트엔드 Axios 인터셉터가 모든 요청에 자동으로 주입합니다.

---

## 10. 주요 구현 포인트

### ① TiDB Cloud SSL 연결

```js
const pool = mysql.createPool({
    host:     process.env.DB_HOST,
    user:     process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    database: process.env.DB_NAME,
    port:     Number(process.env.DB_PORT || 3306),
    waitForConnections: true,
    connectionLimit: 10,
    charset: 'utf8mb4',
    ssl: process.env.DB_SSL === 'true' ? { rejectUnauthorized: false } : undefined,
});
```

TiDB Cloud Serverless는 SSL 연결을 요구합니다.  
`DB_SSL=true` 설정 후 `rejectUnauthorized: false` 로 자체 서명 인증서 허용.

---

### ② 설문 트랜잭션 처리

설문 생성 시 `survey → quest → quest_sel` 3개 테이블에 순차 INSERT.  
중간에 실패하면 전체 롤백:

```js
const conn = await pool.getConnection();
try {
    await conn.beginTransaction();
    const [surveyResult] = await conn.execute('INSERT INTO survey ...', [...]);
    const surveyIdx = surveyResult.insertId;
    for (const q of questions) {
        const [questResult] = await conn.execute('INSERT INTO quest ...', [...]);
        const questIdx = questResult.insertId;
        if (q.questType === 'S' && q.options?.length) {
            for (const opt of q.options) {
                await conn.execute('INSERT INTO quest_sel ...', [...]);
            }
        }
    }
    await conn.commit();
    res.json({ result: 'success', surveyIdx });
} catch (e) {
    await conn.rollback();
    res.status(500).json({ result: 'fail' });
} finally {
    conn.release();
}
```

---

### ③ 설문 응답 중복 처리

같은 질문에 재응답(수정) 허용: `ON DUPLICATE KEY UPDATE`

```sql
INSERT INTO user_survey_answer (survey_idx, quest_idx, usr_idx, sel_idx, text_answer)
VALUES (?, ?, ?, ?, ?)
ON DUPLICATE KEY UPDATE sel_idx = VALUES(sel_idx), text_answer = VALUES(text_answer)
```

`UNIQUE KEY (quest_idx, usr_idx)` 가 걸려 있어 동일 사용자가 같은 질문에 재응답하면 업데이트로 처리됩니다.

---

### ④ snake_case → camelCase SQL 별칭

프론트엔드 코드에서 일관된 camelCase를 사용하기 위해 SQL 별칭으로 변환합니다.

```sql
-- board.js 예시
SELECT
    b.board_idx  AS boardIdx,
    b.usr_nm     AS usrNm,
    b.reply_cnt  AS replyCnt,
    COALESCE(DATE_FORMAT(b.reg_dt, '%Y-%m-%d'), DATE_FORMAT(NOW(), '%Y-%m-%d')) AS regDt
FROM board b
```

---

### ⑤ CORS 설정

```js
app.use(cors({
    origin: process.env.CLIENT_URL || '*',
    allowedHeaders: ['Content-Type', 'X-AUTH-TOKEN'],
    methods: ['GET', 'POST', 'PATCH', 'DELETE', 'OPTIONS'],
    credentials: true,
}));
```

프로덕션 환경에서는 `CLIENT_URL` 에 프론트엔드 도메인을 정확히 명시하세요.

---

## 11. 배포 (Railway)

Railway는 Node.js 앱을 GitHub 연동으로 자동 배포해주는 무료 PaaS입니다.  
무료 플랜에서 월 $5 크레딧 제공.

### 배포 단계

1. [railway.app](https://railway.app) 회원가입
2. **New Project** → **Deploy from GitHub** → `my-components-server` 레포 선택
3. **Variables** 탭에서 `.env` 내용 전부 입력:
   ```
   PORT=4000
   CLIENT_URL=https://your-frontend.vercel.app
   JWT_SECRET=...
   DB_HOST=...
   DB_PORT=...
   DB_USER=...
   DB_PASSWORD=...
   DB_NAME=...
   DB_SSL=true
   ```
4. 자동 빌드 · 배포 완료
5. **Settings** → **Domains** → 발급된 URL 확인

### 프론트엔드 연결 (배포 후)

`my-components/.env.production`:

```env
VITE_APP_API_BASE_URL=https://your-server.up.railway.app
VITE_APP_WS_BASE_URL=https://your-server.up.railway.app
```

---

## 데모 계정

```
아이디  : test
비밀번호: Test1234!
```

---

## 라이선스

개인 포트폴리오 프로젝트입니다. 참고·학습 목적의 코드 활용은 자유롭게 하셔도 됩니다.

# 온라인 매칭 서버 개발 과제

> 초기 설계/과제와 현재 완료 상태는 다릅니다. [2026-10-16 구현 현황](../project/implementation-status.md)을 먼저 확인하세요. 직접 P2P·실물 BLE·Windows 실기는 별도 증거가 필요합니다.

저장소: [digital-tennis-match-server](https://github.com/digital-tennis/digital-tennis-match-server)  
초기 담당 역할: C / A 검토

6자리 방 코드, 2인 방, WebSocket 시그널링, 릴레이를 구현합니다. 아래 과제는 아직 구현하지 않은 문제 명세입니다. 각 입력·출력과 예제를 먼저 재현하고 예외 조건을 추가하세요. [WBS](../planning/wbs.md)의 과제 번호로 작업을 연결합니다. 초기 숫자 설정은 실제 환경 검증 후 변경 이력과 함께 조정할 수 있습니다.

## 공통 준비

- D1 [환경·물품 확인](../project/overview.md)에서 실제 도구와 버전을 기록합니다.
- [컨트롤러 계약](../contracts/controller-protocol.md)과 [온라인 계약](../contracts/online-protocol.md) 중 관련 경계를 읽습니다.
- [작업·PR 방법](../guides/contributing.md)에 따라 작은 결과와 증거를 제출합니다.
- 정상 예제와 실패 예제를 확인한 뒤 다른 제품에 연결합니다.

## 과제 목록

- [MS-01 6자리 방 코드와 2인 방 관리](#ms-01)
- [MS-02 WebSocket 요청과 응답 및 검증](#ms-02)
- [MS-03 P2P 연결 정보 시그널링](#ms-03)
- [MS-04 릴레이와 전송 모드 합의](#ms-04)
- [MS-05 heartbeat와 재접속 유예 및 종료 정리](#ms-05)
- [MS-06 서버 실행과 배포 및 운영 확인](#ms-06)

## MS-01

### 구현할 동작

**6자리 방 코드와 2인 방 관리**

처음에는 WebSocket 없이 방 생성·참가·퇴장을 순수 함수로 만듭니다. 방 코드는 서버가 생성하고 활성 방 사이에서 중복되면 다시 뽑습니다.

### 선행 조건과 입력

선행 조건: 온라인 계약

CreateRoom(client), JoinRoom(client, code), LeaveRoom(client), 현재 단조 시각과 테스트용 난수 공급자.

### 출력과 반환값

code, host/guest 역할, RoomState 또는 명시적인 오류.

### 동작 규칙

- 32문자 alphabet의 6자리 코드이며 활성 충돌 시 최대 10회 재시도합니다.
- 호스트를 포함해 2명까지만 참가합니다. 한 client가 여러 방에 동시에 속할 수 없습니다.
- 코드 입력의 앞뒤 공백 제거·대문자 변환 후 길이와 alphabet을 검사합니다.
- WAITING은 생성 10분 후 만료하며 PLAYING은 같은 TTL로 삭제하지 않습니다.

### 입력과 기대 결과 예제

```text
난수결과 AB2CD3→이미있음→다음 EF4GH5 채택
Join(" ef4gh5 ")→guest
3번째참가→ROOM_FULL
길이 5→INVALID_CODE
```

### 예외와 경계 조건

10회 연속 충돌, 이미 참가한 client, 없는 방, 동시 참가 요청 2개, 만료 직전 참가, 호스트 퇴장을 확인합니다.

### 권장 구현 순서

1. 메모리 RoomMap을 만듭니다.
2. 주입 가능한 시계·난수로 충돌·만료를 검증합니다.
3. 원자적인 참가 처리로 동시 요청의 인원 제한을 보장합니다.

### 완료 판정

- 동시 참가에서도 2명을 넘지 않습니다.
- 코드 충돌·만료·정규화 예제가 맞습니다.

### 제출할 결과

방 관리 모듈, 순수 테스트, 생명주기 표.

## MS-02

### 구현할 동작

**WebSocket 요청과 응답 및 검증**

두 모의 클라이언트를 연결해 JSON 계약으로 방을 만들고 참가합니다. 이 단계에서는 테니스 게임과 P2P가 없어도 검증할 수 있어야 합니다.

### 선행 조건과 입력

선행 조건: MS-01

WebSocket 문자열 메시지의 v/type/requestId/payload와 현재 socket.

### 출력과 반환값

room.created/joined/ready/left 또는 error. 요청 ID와 socket membership.

### 동작 규칙

- 지원 version 1, type 목록, payload 필드·범위·최대 16KiB를 검사합니다.
- 요청 응답은 같은 requestId를 반환하고 알림은 null입니다.
- 방과 playerId는 서버가 socket에 연결하며 클라이언트 주장으로 변경하지 않습니다.
- 정해진 rate limit 초과는 RATE_LIMITED로 처리합니다. 잘못된 JSON이 전체 서버를 중단하지 않습니다.
- 재접속 token은 예측 불가능하게 생성하여 최초 응답에 필요한 상대에게 전달합니다.

### 입력과 기대 결과 예제

```text
socketA room.create r1→room.created r1 codeAB2CD3 rolehost
socketB room.join r2→room.joined r2;A/B에게 room.ready
"{"→INVALID_JSON;다른 socket은계속정상동작
```

### 예외와 경계 조건

누락 requestId, 틀린 version, 초대형 메시지, NaN 대신 문자열을 넣은 값, 두 방 동시 참가, rate limit을 검사합니다.

### 권장 구현 순서

1. 선택한 서버 런타임 버전을 고정합니다.
2. 한 socket의 요청·응답을 성공시킵니다.
3. 두 socket과 입력 검증·메모리 membership을 연결합니다.

### 완료 판정

- 게임 없이 두 클라이언트가 같은 방에 들어갑니다.
- 잘못된 입력의 오류 코드와 요청 ID가 명확합니다.
- 서버 로그에 reconnectToken을 남기지 않습니다.

### 제출할 결과

서버 entrypoint, 스키마 검증, 모의 클라이언트·실행법.

## MS-03

### 구현할 동작

**P2P 연결 정보 시그널링**

WebSocket 서버는 PC 간 직접 연결을 준비하도록 offer·answer·ICE를 전달합니다. 서버가 정보를 전달했다는 사실과 실제 P2P 연결 성공을 구분합니다.

### 선행 조건과 입력

선행 조건: MS-02,GM-07의 D3 후보

peer.signal {kind, data}, 발신 socket의 room·role, 선택한 P2P 후보의 연결 데이터.

### 출력과 반환값

같은 방의 상대 socket에만 전달된 peer.signal 또는 오류.

### 동작 규칙

- offer는 host, answer는 guest, ICE는 양쪽을 허용합니다.
- 상대가 없으면 PEER_NOT_READY를 반환합니다.
- 외부 roomCode·targetPlayerId를 payload로 지정해 다른 방에 보낼 수 없습니다.
- candidate 도착 순서와 중복 처리는 클라이언트가 선택 라이브러리 규칙으로 처리하며 서버는 임의로 SDP를 수정하지 않습니다.
- data의 형식·크기·kind는 D3 후보 확정 결정에 맞춰 검사합니다.

### 입력과 기대 결과 예제

```text
A/B는방 1,C/D는방 2
A offer→B 만수신
B offer→INVALID_ROLE
A payload에방 2code 추가→방 2로전달되지않음
```

### 예외와 경계 조건

빈 SDP, 없는 상대, 퇴장 직후 signal, 다른 방을 지정한 요청, 지나치게 큰 candidate 목록을 검사합니다.

### 권장 구현 순서

1. 모의 클라이언트로 전달 대상을 검증합니다.
2. D3 후보의 offer·answer를 통과시킵니다.
3. 실제 Unity MatchClient와 연결합니다.

### 완료 판정

- 같은 방 상대만 정보를 받습니다.
- P2P 성공은 GM-07 증거로 별도 검증합니다.

### 제출할 결과

시그널링 handler, 방 격리·role 테스트, 연결 정보 전달 로그.

## MS-04

### 구현할 동작

**릴레이와 전송 모드 합의**

P2P가 실패하는 네트워크에서도 같은 경기 메시지를 서버로 중계합니다. 한쪽은 P2P, 다른 쪽은 릴레이인 상태에서 경기가 시작하지 않도록 합의 절차를 만듭니다.

### 선행 조건과 입력

선행 조건: MS-03,GM-07

transport.propose/ack/commit, mode·epoch, game.relay의 게임 message와 발신 role.

### 출력과 반환값

양쪽 transport.committed와 같은 방 relay.message 또는 명시적인 오류.

### 동작 규칙

- host propose → guest ack → host commit 순서를 검사합니다. ack 없이는 PEER_NOT_ACKED입니다.
- mode·epoch는 room에서 관리하고 오래된 epoch는 중계하지 않습니다.
- input은 guest가 host로, snapshot·result는 host가 guest로 전달합니다. 잘못된 역할은 INVALID_ROLE입니다.
- relay는 공·점수를 계산하지 않습니다. 게임 message의 스키마·범위·크기는 검사합니다.
- 현재 mode=p2p 인 방의 경기 relay는 거절하되 제어 채널은 유지합니다.

### 입력과 기대 결과 예제

```text
hostpropose relay epoch1→guestack1→hostcommit1→양쪽 committed
guest input42→host 수신
guest snapshot→INVALID_ROLE
old epoch0→INVALID_EPOCH
```

### 예외와 경계 조건

일치하지 않는 ack, 중복 commit, 발신 역할을 속인 요청, 다른 방 전달, 초과 크기, 중계 중단을 검사합니다.

### 권장 구현 순서

1. 릴레이 상대 지정을 membership으로 구현합니다.
2. 역할·epoch·스키마 검사를 추가합니다.
3. 전환 합의와 강제 P2P 실패 시나리오를 연결합니다.

### 완료 판정

- AT-14에서 8초 후 양쪽 relay 합의와 경기 진행이 보입니다.
- 다른 방·잘못된 역할 메시지가 전달되지 않습니다.
- mode 변경 중 중복 경기가 시작하지 않습니다.

### 제출할 결과

전환 상태기계, 릴레이 handler, 역할·epoch·격리 테스트.

## MS-05

### 구현할 동작

**heartbeat와 재접속 유예 및 종료 정리**

소켓이 끊겼을 때 방을 즉시 없애면 재접속이 불가능하고 계속 유지하면 유령 방이 남습니다. 끊김·유예·만료를 구분합니다.

### 선행 조건과 입력

선행 조건: MS-04,GM-08

5초 주기의 heartbeat, 마지막 활동 시각, socket close, session.resume의 code·token, 현재 시각.

### 출력과 반환값

peer.disconnected/pause, resumed/closed와 정리된 room·membership·token.

### 동작 규칙

- heartbeat 15초 누락 또는 close를 끊김으로 판정하고 상대에게 알립니다.
- 끊김 판정 후 15초 유예 내 유효 token 만 기존 역할을 복구합니다.
- token은 다른 방·역할에서 사용할 수 없고 성공 resume 시 교체합니다. 이전 socket은 무효화합니다.
- 유예 중 새 guest가 빈자리를 차지하지 못하게 합니다.
- 호스트 미복귀는 무효 종료·방 정리, 게스트 미복귀도 온라인 경기를 종료하고 종료 원인을 보여줍니다.

### 입력과 기대 결과 예제

```text
t0close→pause,t0+10초유효 token→resume
t0+16초 resume→RESUME_EXPIRED
다른방 token→INVALID_TOKEN
기존 socket 뒤늦은메시지→거절
```

### 예외와 경계 조건

동시 resume 요청 2개, close와 heartbeat의 경쟁, 서버 재시작, 오래된 token, 완료 방 resume를 검사합니다.

### 권장 구현 순서

1. 가짜 시계로 유예와 TTL을 검증합니다.
2. token과 socket 세대 검사를 추가합니다.
3. Unity의 checkpoint·새 epoch 재개와 연결합니다.

### 완료 판정

- AT-16·17에서 pause·resume·무효 종료가 일치합니다.
- 종료 방의 메모리·membership·token이 정리됩니다.

### 제출할 결과

연결 생명주기, 시계 기반 테스트, 2PC 단절·재접속 로그.

## MS-06

### 구현할 동작

**서버 실행과 배포 및 운영 확인**

다른 PC가 서버 주소에 연결할 수 있도록 실행·설정·확인 방법을 제공합니다. 실제 배포 서비스는 팀이 D1~D9에 결정하며 임의의 유료 서비스를 전제하지 않습니다.

### 선행 조건과 입력

선행 조건: MS-05

서버 런타임 버전, PORT·허용 설정·공개 endpoint, 테스트 클라이언트.

### 출력과 반환값

재현 가능한 설치·시작·검증 명령, 설정 예제, health와 연결 로그.

### 동작 규칙

- 비밀값 없는 .env.example을 제공하고 실제 .env는 제외합니다.
- health 경로는 프로세스 상태·버전만 반환하며 token·개인정보를 노출하지 않습니다.
- localhost 개발 ws와 공개 환경 wss 주소를 구분합니다.
- 호스팅 재시작·idle sleep이 방을 종료시키는 동작을 설명합니다.
- 로그에는 roomId·role·mode·메시지 카운터를 남기고 token·SDP 원문·민감한 주소는 제외합니다.

### 입력과 기대 결과 예제

```text
안내대로서버시작→health 정상
두다른 PC→같은 endpoint→방생성/참가
서버재시작→기존방소멸,클라이언트종료안내
```

### 예외와 경계 조건

PORT 충돌, endpoint 오타, 프록시의 WebSocket 미지원, 서버 sleep, 일부 설정 누락을 검사합니다.

### 권장 구현 순서

1. 로컬 실행을 다른 팀원이 재현합니다.
2. 선택 환경의 WebSocket 지원·접근을 확인합니다.
3. 다른 네트워크 2PC로 연결·재접속을 검증합니다.

### 완료 판정

- README에 실제 명령과 버전이 있습니다.
- AT-12~17 실행 환경과 관측값이 남습니다.

### 제출할 결과

실행 안내·설정 예제·배포 환경표·health·시연 로그.


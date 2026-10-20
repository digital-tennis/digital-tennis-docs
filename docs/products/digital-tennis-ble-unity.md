# Windows BLE와 Unity 입력 SDK 개발 과제

> 후속 변경: [물리 이벤트 v3와 책임 분리](../project/physical-controller-events.md)를 우선합니다. 초기 과제의 샷 분류·v1/v2 표는 최초 계획이며, 새 제품에서 펌웨어는6종 물리 패턴/버튼edge, 게임은 서브/스매시 등을 소유합니다.

저장소: [digital-tennis-ble-unity](https://github.com/digital-tennis/digital-tennis-ble-unity)  
초기 담당 역할: C / A 검토

BLE 검색·연결·재연결, 메인 스레드 입력 전달, 가상 컨트롤러를 구현합니다. 아래 과제는 최초 문제 명세이며 현재의 구현 완료표가 아닙니다. 소프트웨어 구조·코덱·SDK는 [검토 중인 구현 PR](https://github.com/digital-tennis/digital-tennis-ble-unity/pull/1)과 [현재 확장 작업](../project/software-completion.md)에서 확인합니다. 실제 외장 IMU/라디오 검증은 유예 상태입니다. 각 입력·출력과 예제를 먼저 재현하고 예외 조건을 추가하세요. [WBS](../planning/wbs.md)의 과제 번호로 작업을 연결합니다. 초기 숫자 설정은 실제 환경 검증 후 변경 이력과 함께 조정할 수 있습니다.

## 현재 구현과 최초 과제의 관계

아래 수치·절차는 최초 코딩 과제다. 현재 main과 후속 검토 브랜치의 구현/검증 범위는 [컨트롤러 준비 상태](../project/controller-readiness.md)를 기준으로 구분한다. 펌웨어 FW-04는 구간·peak·release와 선택 모드/주입 규칙을, FW-05는 유한 큐·독립 송신·센서 없는 왕복을, FW-06은30ms 디바운스와 선택 alias를 구현했다. 합성 데이터·컴파일 성공은 실물 IMU/핀/라디오 성공을 뜻하지 않는다.

## 공통 준비

- D1 [환경·물품 확인](../project/overview.md)에서 실제 도구와 버전을 기록합니다.
- [컨트롤러 계약](../contracts/controller-protocol.md)과 [온라인 계약](../contracts/online-protocol.md) 중 관련 경계를 읽습니다.
- [작업·PR 방법](../guides/contributing.md)에 따라 작은 결과와 증거를 제출합니다.
- 정상 예제와 실패 예제를 확인한 뒤 다른 제품에 연결합니다.

## 과제 목록

- [BL-01 표준 입력과 가상 컨트롤러](#bl-01)
- [BL-02 Windows BLE 검색과 Notify 구독](#bl-02)
- [BL-03 패킷 검증과 Unity 메인 스레드 전달](#bl-03)
- [BL-04 재연결과 보정 UI 및 지연 측정](#bl-04)

## BL-01

### 구현할 동작

**표준 입력과 가상 컨트롤러**

보드가 아직 준비되지 않아도 Unity 담당자가 게임을 개발할 수 있어야 합니다. 실제 BLE와 가상 입력이 같은 인터페이스를 사용하도록 만듭니다.

### 선행 조건과 입력

선행 조건: PR-01

키보드·UI 버튼 또는 녹화 이벤트; 선택한 ControllerSource.

### 출력과 반환값

RacketInput {sessionId,eventId,kind,power01,aimX,aimZ,receivedAtMs,source}; ConnectionState이벤트.

### 동작 규칙

- IControllerSource에 Start/Stop, 입력·상태 알림 경계를 정의합니다.
- 가상 입력에서 forehand/backhand/serve, power0~1과 aim-1~1을 선택합니다.
- 누른 키 반복은 별도 스윙이 되지 않도록 press-edge에서 한 번만 생성합니다.
- game이 실제·가상 source를 바꾸어도 샷 코드가 바뀌지 않습니다.

### 입력과 기대 결과 예제

```text
Space 한 번 누름, kind=forehand,power=0.8,aimX=-0.2
출력: RacketInput 1개, source=virtual
키 1초 유지→추가 입력 0
```

### 예외와 경계 조건

Stop 뒤 이벤트, source 교체 중 남은 큐, 동일 eventId, 잘못된 파워를 처리합니다.

### 권장 구현 순서

1. game 없이 콘솔/테스트에서 이벤트를 봅니다.
2. Unity 테스트 씬에 입력 표시를 붙입니다.
3. 녹화 재생과 source 교체를 추가합니다.

### 완료 판정

- 실물 장치 없이 게임 서브·타격을 개발할 수 있습니다.
- Stop 뒤와 source 교체 뒤 이전 입력이 없습니다.

### 제출할 결과

표준 인터페이스, 가상 입력, 표시 씬, 예제 이벤트.

## BL-02

### 구현할 동작

**Windows BLE 검색과 Notify 구독**

BLE는 운영체제 기능과 Unity 빌드 환경의 영향을 받습니다. 실제 Windows 실행 파일에서 한 개 Notify를 받는 작은 검증을 먼저 통과해야 합니다.

### 선행 조건과 입력

선행 조건: FW-05 준비 전에는 고정 STATUS 샘플 가능; D2 후보 검증

Windows BLE 어댑터, Service UUID, 사용자가 선택한 deviceId, 연결/구독 취소 요청.

### 출력과 반환값

Idle→Scanning→Connecting→Connected 또는 Error 상태, 수신 byte 배열.

### 동작 규칙

- 광고의 Service UUID로 필터하고 이름만으로 장치를 믿지 않습니다.
- 검색된 여러 장치는 사용자가 하나를 선택합니다. 두 PC가 실수로 같은 컨트롤러를 잡지 않게 선택을 표시합니다.
- 연결 후 정확한 Service와 TX를 찾고 Notify 속성·CCCD 구독 결과를 확인합니다.
- Windows API 후보와 Unity Editor/standalone, Mono/IL2CPP 등 실제 선택 환경을 기록합니다. D2 결과 없이 호환성을 보장하지 않습니다.

### 입력과 기대 결과 예제

```text
장치 A: 같은 이름, 다른 UUID → 목록 제외
장치 B: 올바른 UUID → 선택·연결·CCCD 성공
STATUS Notify 20 바이트 → RawPacketReceived
```

### 예외와 경계 조건

BLE 없음·꺼짐, 권한 거절, 장치 사라짐, CCCD 실패, 취소·타임아웃(초기 8초), 여러 동일 이름 장치를 각각 상태로 보고합니다.

### 권장 구현 순서

1. Windows 공식 GATT 예제로 Notify를 확인합니다.
2. 선택한 어댑터를 Unity 밖 또는 최소 Windows 빌드에서 검증합니다.
3. 표준 source에 연결하고 취소·정리를 추가합니다.

### 완료 판정

- Editor와 Windows 실행 파일 결과를 구분하여 기록합니다.
- 실제 firmware STATUS 수신과 잘못된 UUID 제외를 확인합니다.
- 취소 후 장치와 이벤트 핸들러를 해제합니다.

### 제출할 결과

Windows 어댑터, 지원 환경표, 검색/구독/실패 로그.

## BL-03

### 구현할 동작

**패킷 검증과 Unity 메인 스레드 전달**

BLE 알림 콜백에서 Unity 오브젝트를 직접 다루지 않습니다. 검증된 이벤트를 큐에 넣고 Unity Update에서 꺼내며 중복 스윙을 제거합니다.

### 선행 조건과 입력

선행 조건: PR-02/03, BL-01/02

RawPacketReceived byte 배열, 연결 sessionId, PC 단조 수신 시각.

### 출력과 반환값

정상 RacketInput·STATUS·ACK, 오류/누락/중복 카운터, 메인 스레드 알림.

### 동작 규칙

- PR-02를 사용해 CRC·범위·version을 검사합니다.
- sequence와 최근 64개(sessionId,type,eventId)를 검사합니다. 반복 스윙 3개는 game이벤트 1개입니다.
- 보정/센서 flag가 충족되지 않은 SWING은 게임에 전달하지 않습니다.
- 최대 128개 큐, 가득 차면 가장 오래된 스윙 입력을 제거하고 dropCount를 남깁니다. ACK·상태는 별도 큐 또는 유지 정책으로 유실되지 않게 합니다.
- Update에서 프레임당 최대 32개 처리합니다. 250ms 보다 오래 기다린 스윙은 버리고 staleCount를 기록합니다.
- power·각도는 공통 변환을 사용하며 game 속도는 SDK에서 계산하지 않습니다.

### 입력과 기대 결과 예제

```text
sequence42/43/44, eventId7의 동일 SWING→RacketInput1개
bad_crc→게임 입력 0개, badCrcCount+1
yaw=-12.5 도→aimX≈-0.27778
```

### 예외와 경계 조건

역순 sequence, 지원하지 않는 version, 큐 지연, 재연결 후 동일 eventId, Stop 후 콜백, 보정 미완료를 확인합니다.

### 권장 구현 순서

1. 콜백을 가짜 배열로 호출해 파싱합니다.
2. 스레드 안전 큐와 Update 소비를 나눕니다.
3. 중복·오래된 입력·카운터를 추가합니다.

### 완료 판정

- Unity API 호출은 메인 스레드에서만 발생합니다.
- 한 스윙의 3회 전송이 한 번 타격됩니다.
- 오류·보정 미완료가 정상 타격이 되지 않습니다.

### 제출할 결과

수신 큐, 패킷→입력 변환, 중복/역순/지연 테스트, 디버그 카운터.

## BL-04

### 구현할 동작

**재연결과 보정 UI 및 지연 측정**

컨트롤러 전원이 꺼지거나 센서가 움직이는 중 보정하면 플레이어가 원인을 알아야 합니다. 무한 재연결로 UI를 멈추지 않도록 상태를 관리합니다.

### 선행 조건과 입력

선행 조건: BL-03, FW-05

연결 종료, 재연결 요청, CALIBRATE 버튼, firmware ACK·STATUS.

### 출력과 반환값

상태·사용자 안내, 새 sessionId, 보정 결과, PC 내 수신→소비 지연 통계.

### 동작 규칙

- 단절 시 큐·순번·이벤트 이력을 초기화하고 source sessionId를 바꿉니다.
- 초기 재시도는 1/2/4초 뒤 최대 3회, 실패하면 사용자가 다시 선택하게 합니다. 취소는 즉시 가능한 상태여야 합니다.
- 보정 중 입력을 중단하며 ACK5초 타임아웃과 실패 원인을 표시합니다.
- ACK requestId(eventId)를 대응시키고 이전 세션 ACK는 무시합니다.
- 수신·소비를 같은 PC 단조 시계로 측정하고 MCU 시각을 빼지 않습니다.

### 입력과 기대 결과 예제

```text
Connected→전원 OFF→Disconnected→재시도→Connected(session2)
이전 session1 스윙은 0개 전달
보정 버튼→ACK kind3→라켓을 정지시키고 다시 보정 안내
```

### 예외와 경계 조건

사용자 취소, 반복 단절, 앱 종료, 재시도 중 Stop, ACK 누락, 다른 명령 ACK, sensorReady=false를 확인합니다.

### 권장 구현 순서

1. 단절을 모의 source로 재현합니다.
2. 취소 가능한 재시도와 자원 정리를 만듭니다.
3. 실물 전원 OFF/ON과 보정 실패를 검증합니다.

### 완료 판정

- 재연결 뒤 과거 입력이 타격되지 않습니다.
- 구독 핸들러가 중복 등록되지 않습니다.
- AT-07과 PC 내 p95 측정 결과가 기록됩니다.

### 제출할 결과

재연결 상태기계, 보정 UI·ACK 테스트, 실제 환경·지연 로그.

# 컨트롤러 통신 규격 개발 과제

저장소: [digital-tennis-protocol](https://github.com/digital-tennis/digital-tennis-protocol)  
초기 담당 역할: C / A 검토

보드와 PC가 공유하는 바이너리 규격, C 및 C# 코덱과 테스트 벡터를 구현합니다. 아래 과제는 최초 문제 명세이며 현재의 구현 완료표가 아닙니다. 소프트웨어 구조·코덱·SDK는 [검토 중인 구현 PR](https://github.com/digital-tennis/digital-tennis-protocol/pull/1)과 [현재 확장 작업](../project/software-completion.md)에서 확인합니다. 실제 외장 IMU/라디오 검증은 유예 상태입니다. 각 입력·출력과 예제를 먼저 재현하고 예외 조건을 추가하세요. [WBS](../planning/wbs.md)의 과제 번호로 작업을 연결합니다. 초기 숫자 설정은 실제 환경 검증 후 변경 이력과 함께 조정할 수 있습니다.

## 공통 준비

- D1 [환경·물품 확인](../project/overview.md)에서 실제 도구와 버전을 기록합니다.
- [컨트롤러 계약](../contracts/controller-protocol.md)과 [온라인 계약](../contracts/online-protocol.md) 중 관련 경계를 읽습니다.
- [작업·PR 방법](../guides/contributing.md)에 따라 작은 결과와 증거를 제출합니다.
- 정상 예제와 실패 예제를 확인한 뒤 다른 제품에 연결합니다.

## 과제 목록

- [PR-01 하드웨어와 PC가 합의하는 계약 작성](#pr-01)
- [PR-02 C와 C# 패킷 인코더 및 디코더](#pr-02)
- [PR-03 공통 벡터와 순번 비교 검증](#pr-03)
- [PR-04 버전과 소비 제품 의존성 관리](#pr-04)

## PR-01

### 구현할 동작

**하드웨어와 PC가 합의하는 계약 작성**

펌웨어와 PC가 다른 byte 위치나 단위를 사용하면 연결에 성공해도 타격이 틀립니다. 구현 전에 어떤 바이트가 어떤 뜻인지 한 장의 계약과 예제로 확정합니다.

### 선행 조건과 입력

선행 조건: 없음

컨트롤러 통신 규격 v1의 GATT UUID·20 바이트 배치·타입별 제한.

### 출력과 반환값

spec/controller-v1.md, 필드/단위표, 정상·오류 벡터 파일, 변경 이력.

### 동작 규칙

- 각 오프셋은 겹치지 않고 0~19 전체를 채웁니다.
- 각 필드에 단위·부호·범위·기본값을 기록합니다.
- CALIBRATE의 write 성공과 보정 ACK 완료를 구별합니다.
- deviceTime과 PC 시각은 다른 시계라고 명시합니다.

### 입력과 기대 결과 예제

```text
SWING seq=42, eventId=7, power=80, yaw=-12.5 도
기대 필드: yawCdeg=-1250; little-endian int16
문서: 실제 완성된 20 바이트 hex와 CRC를 함께 제공
```

### 예외와 경계 조건

예약 비트, 미정 타입, 배터리 미측정, 재연결, eventId/sequence wrap과 중복을 계약에 포함합니다.

### 권장 구현 순서

1. 바이트 표를 코드보다 먼저 검토합니다.
2. 정상 예제를 손으로 해석합니다.
3. A/C가 값과 예외를 확인하고 소비 제품에 같은 버전을 기록합니다.

### 완료 판정

- FW·SDK 담당자가 예제 하나를 같은 값으로 읽습니다.
- 20 바이트 합계와 CRC 설정·좌표 변환이 확정됩니다.

### 제출할 결과

v1 규격, 검토 기록, spec 버전.

## PR-02

### 구현할 동작

**C와 C# 패킷 인코더 및 디코더**

실제 BLE와 Unity가 없어도 byte 배열을 처리할 수 있는 순수 라이브러리를 만듭니다. 실패한 패킷으로 정상 스윙을 만들어서는 안 됩니다.

### 선행 조건과 입력

선행 조건: PR-01

Encode(Packet) 또는 Decode(byte[20]); C는 buffer 포인터+길이, C#은 byte 배열 또는 선택 런타임에 맞는 span.

### 출력과 반환값

Packet 또는 Result {success, error}; Decode 성공 필드는 계약 값과 정확히 일치.

### 동작 규칙

- 검사 순서: length→magic→version→CRC→type/kind→flags→필드 범위입니다.
- 실패 코드는 INVALID_LENGTH, INVALID_MAGIC, UNSUPPORTED_VERSION, BAD_CRC, INVALID_TYPE, INVALID_KIND, INVALID_FLAGS, OUT_OF_RANGE로 구별합니다.
- little-endian과 signed 각도를 명시적으로 처리하며 구조체 메모리 배치를 그대로 송신하지 않습니다.
- 잘못된 객체 Encode 도 실패 결과를 반환합니다. UnityEngine·BLE·센서에 의존하지 않습니다.

### 입력과 기대 결과 예제

```text
valid_swing 벡터→eventId7, power80, yawCdeg-1250, pitchCdeg300
bad_crc→BAD_CRC
길이 19→INVALID_LENGTH
Encode(Decode(valid))→원본 byte 배열과 일치
```

### 예외와 경계 조건

음수 각도 -18000, 최대 power100, battery255, null/짧은 배열, 잘못된 version, 불가능한 kind를 검사합니다.

### 권장 구현 순서

1. little-endian 정수 읽기를 먼저 만듭니다.
2. CRC 알려진 예제로 검증합니다.
3. 타입별 범위 검사를 넣고 C/C# 왕복을 비교합니다.

### 완료 판정

- 공통 정상·오류 벡터의 결과가 양쪽 언어에서 같습니다.
- CRC 123456789=F4를 통과합니다.
- 실패에서 예외·메모리 범위 접근·정상 이벤트가 없습니다.

### 제출할 결과

C/C# 라이브러리, 테스트 실행법, 벡터 결과.

## PR-03

### 구현할 동작

**공통 벡터와 순번 비교 검증**

값이 맞는지와 최신 메시지인지의 판단을 분리합니다. SDK와 펌웨어가 같은 벡터를 사용하고 wrap 상황을 정상 처리해야 합니다.

### 선행 조건과 입력

선행 조건: PR-02

protocol-vectors.json, uint16 old/new sequence, uint32 deviceTime.

### 출력과 반환값

벡터별 decode 값·오류 결과, SequenceRelation=first/new/duplicate/old, 시간 간격.

### 동작 규칙

- 순번 함수는 상태 없는 비교 함수와 첫 패킷 처리를 분리합니다.
- 65535→0은 new이고 42→42는 duplicate, 42→41은 old입니다.
- delta=32768은 new로 인정하지 않습니다.
- 코덱은 통신 세션의 eventId 캐시를 소유하지 않습니다. 실제 스윙 중복 제거는 BL-03 책임입니다.

### 입력과 기대 결과 예제

```text
old=65535,new=0→new
old=0,new=65535→old
old=10,new=32778→old/ambiguous
deviceTime old=4294967290,new=4→간격 10ms
```

### 예외와 경계 조건

한 번에 반 주기 이상 건너뛴 값은 연결 재설정 대상으로 보고 오래된 값처럼 게임에 넣지 않습니다.

### 권장 구현 순서

1. decode 벡터를 언어별 같은 테스트 입력으로 사용합니다.
2. 정상·CRC 오류·version 오류·flags 오류·범위오류를 자동 실행합니다.
3. 두 언어 결과를 표로 비교합니다.

### 완료 판정

- 정상 벡터와 오류 벡터가 모두 기대값과 일치합니다.
- wrap과 반 주기 경계가 문서대로 처리됩니다.

### 제출할 결과

테스트 벡터, 교차 검증 로그, 순번 함수 예제.

## PR-04

### 구현할 동작

**버전과 소비 제품 의존성 관리**

별도 저장소의 규격이 바뀌면 구버전 firmware와 SDK가 잘못 연결될 수 있습니다. 같은 숫자를 다른 의미로 재사용하지 않도록 변경 정책을 둡니다.

### 선행 조건과 입력

선행 조건: PR-03

현재 v1 규격, 변경 요청, 함께 검증한 firmware/SDK/game SHA.

### 출력과 반환값

CHANGELOG, 호환성 표, 소비 제품의 고정 버전, 릴리스 후보 태그 계획.

### 동작 규칙

- 기존 바이트 의미나 길이를 바꾸면 wire version을 올립니다.
- 구버전/신버전 불일치는 SDK가 명시적인 경고로 표시합니다.
- 단순 문서 오타 수정과 wire 변경을 구분합니다.
- 제품이 사용할 태그·SHA를 기록하고 미구현 기능을 완료로 표시하지 않습니다.

### 입력과 기대 결과 예제

```text
요청: power 필드를 0~100에서 0~255로 변경
기대: v1의미를 덮어쓰지 않음; 새 버전·새 벡터·소비 제품 변경 제시
요청: README 오타→wire version 변경 없음
```

### 예외와 경계 조건

같은 릴리스명에 다른 패킷 의미, main 자동 추적, 오래된 SDK 혼용을 확인합니다.

### 권장 구현 순서

1. 변경 이력 양식을 만듭니다.
2. 함께 통합한 commit을 기록합니다.
3. 지원 버전 불일치 테스트와 안내를 추가합니다.

### 완료 판정

- 팀원이 해당 버전 조합을 재현할 수 있습니다.
- 지원하지 않는 패킷은 타격으로 전달되지 않습니다.

### 제출할 결과

CHANGELOG·호환성 표·고정 버전 안내.

# 컨트롤러 통신 규격 v1/v2

v1 배치를 보존하면서 v2의 명시적 의도를 추가한 계약입니다. [정본 코덱·규격 PR](https://github.com/digital-tennis/digital-tennis-protocol/pull/1)을 함께 확인합니다. D1에 A/C가 검토하고 동일 테스트 벡터로 고정합니다. 게임 규칙과 온라인 메시지는 포함하지 않습니다.

## GATT와 전송

| 용도 | UUID | 속성 |
| --- | --- | --- |
| 컨트롤러 Service | 6d7c1000-9d40-4cb7-a381-5e908be0a001 | 사용자 정의 서비스 |
| 이벤트 TX | 6d7c1001-9d40-4cb7-a381-5e908be0a001 | Notify |
| 명령 RX | 6d7c1002-9d40-4cb7-a381-5e908be0a001 | Write with response |

한 알림은 정확히 20바이트입니다. 이벤트 TX는 SWING·BUTTON·STATUS·ACK를, 명령 RX는 CALIBRATE와 v2 LINK_PROBE를 받습니다. v2 LINK_REPLY는 이벤트 TX로 돌아옵니다. CCCD 구독이 성공한 연결에만 Notify합니다. 센서 원시값은 우선 USB/시리얼 디버그로 확인하며 임의로 이벤트 패킷 안에 끼워 넣지 않습니다.

## 패킷 배치

모든 다중 바이트 정수는 little-endian입니다. 부호 있는 값은 2의 보수입니다.

| 오프셋 | 길이 | 이름 | 형식과 의미 |
| --- | --- | --- | --- |
| 0 | 1 | magic | 0x44 |
| 1 | 1 | version | 1 또는2 |
| 2 | 1 | type | 1 SWING, 2 BUTTON, 3 STATUS, 128 CALIBRATE, 129 ACK, v2 전용 130 LINK_PROBE / 131 LINK_REPLY |
| 3 | 1 | flags | bit0 보정 완료, bit1 센서 준비, bit2 왼손; bit3~7=0 |
| 4 | 2 | sequence | uint16, 송신 방향별 패킷 순번 |
| 6 | 4 | deviceTimeMs | uint32, MCU 부팅 후 단조 밀리초; CALIBRATE는 0 |
| 10 | 2 | eventId | uint16, 스윙/버튼 ID 또는 명령 ID; STATUS는 0 |
| 12 | 1 | kind | type별 아래 표 참조 |
| 13 | 1 | power | SWING 0~100; 다른 type은 0 |
| 14 | 2 | yawCdeg | SWING -18000~18000, 0.01도; 다른 type은 0 |
| 16 | 2 | pitchCdeg | SWING -9000~9000, 0.01도; 다른 type은 0 |
| 18 | 1 | battery | 0~100 또는 측정 불가 255; CALIBRATE는 255 |
| 19 | 1 | crc8 | 앞 19바이트 CRC-8/ATM |

| type | kind | 추가 조건 |
| --- | --- | --- |
| SWING v1/v2 | 1 포핸드, 2 백핸드, 3 서브 | flags의 bit0·bit1이 모두 1일 때만 게임 입력으로 사용 |
| SWING v2 전용 | 4 스매시,5 발리,6 슬라이스,7 로브,8 스킬 | v1에서4~8은 INVALID_KIND, 버전3이상은 UNSUPPORTED_VERSION |
| BUTTON | 1 확인, 2 시작, 3 일시정지 | power·각도는 0 |
| STATUS | 0 | eventId·power·각도는 0, 준비/보정 상태 보고 |
| CALIBRATE | 0 | flags·deviceTimeMs·power·각도=0, eventId는 PC 명령 ID |
| ACK | 0 성공, 1 바쁨, 2 센서 미준비, 3 보정 실패 | eventId는 해당 명령 ID, power·각도=0 |

ACK는 보정 작업이 끝난 후 결과를 한 번 보냅니다. GATT write 성공은 명령이 센서 보정까지 성공했다는 뜻이 아닙니다. SDK는 ACK를 5초 기다리고, 없으면 타임아웃을 표시합니다. 같은 명령 ID가 반복되면 보정을 다시 시작하지 않고 진행 중이면 BUSY, 완료했다면 저장한 결과를 반환합니다. 명령 ID는 연결 내에서 최근 64개 이력에 재사용하지 않습니다.

CRC 매개변수는 polynomial=0x07, init=0x00, refin=false, refout=false, xorout=0x00입니다. 검증용 ASCII `123456789`의 CRC는 0xF4입니다. CRC는 전송 오류 검출용입니다.

## 센서 없이 통신만 확인하기

검토 브랜치의 v2 LINK_PROBE/REPLY는 센서 연결/보정과 독립된 PC↔기기 왕복 검사다. 두 타입의 kind·power·각도는0, eventId는0이 아닌 nonce다. PROBE의 flags·deviceTimeMs는0, battery는255이고 REPLY는 실제 센서 flags·기기 시각을 보고한다. v1에서는 새 타입을 거부한다. PC는 현재 연결에서 같은 nonce 응답을2초 안에 받을 때만 성공으로 표시한다. CRC가 맞아도 이전 연결/다른 nonce/늦은 응답은 성공이 아니다. 왕복 성공으로 보정·동작 테스트·설정 저장을 허용하지 않는다.

정본은 protocol d9a36826afbafa27a0e276cc53e44c904d05be53의 spec/controller-v2.md와 공통 벡터다. [후속 검수와 실기 경계](../project/controller-readiness.md)를 함께 읽는다.

## 순번과 중복

패킷 sequence는 65535 다음 0이 됩니다. `delta=(new-old)&0xffff`로 계산하여 `0<delta<32768`이면 새로운 패킷, 0이면 중복, 그 외는 오래된 패킷으로 처리합니다. 첫 패킷은 기준으로 수용합니다. 한 번에 32768개 이상을 건너뛴 연결은 새 연결 세션으로 초기화합니다.

스윙 이벤트는 같은 eventId와 원래 deviceTimeMs로 총3회 보내는 설계입니다. 후속 펌웨어는 BLE 역압에 대비해20ms 재시도 간격, 입력200ms/제어1000ms 만료와32개 유한 큐를 사용합니다. 최초 설계의10/20ms 예정값과 구분합니다. 각 전송의 sequence는 증가합니다. SDK는 최근 64개의 `(sessionId,type,eventId)`를 저장하여 한 스윙을 한 번만 전달합니다. STATUS와 ACK는 스윙 중복 처리와 별도로 처리합니다. 연결이 끊기면 SDK의 sessionId와 수신 이력을 바꾸고 이전 스윙을 재생하지 않습니다.

deviceTimeMs는 약 49.7일에 wrap합니다. 연속 MCU 샘플의 간격은 uint32 차로 계산합니다. MCU 시각과 PC 시각을 빼서 입력 지연으로 해석하지 않습니다. 지연 측정은 같은 PC의 수신→게임 소비 시간 또는 별도 동기화 실험으로 구분합니다.

## 좌표와 샷 방향

센서 고유 축을 그대로 게임 축으로 사용하지 않습니다. FW-03에서 센서 장착 변환 행렬과 정지 기준 자세를 기록합니다. 기준 자세에서 라켓 전방을 +Z, 오른쪽을 +X, 위를 +Y로 정합니다. 좌표 변환과 왼손 처리 순서를 그림·테스트로 고정합니다.

SDK는 yawCdeg/100, pitchCdeg/100으로 각도를 복원한 뒤 `aimX=clamp(yawDeg/45,-1,1)`, `aimZ=clamp(pitchDeg/45,-1,1)`로 전달합니다. 왼손 보정은 firmware 좌표 변환에서 한 번만 적용하므로 SDK가 다시 반전하지 않습니다. game은 플레이어 0·1의 코트 방향을 별도로 변환하고 방향·파워를 샷 속도로 매핑합니다.

## 잘못된 입력

길이≠20, magic/version 불일치, 알려지지 않은 type/kind, 예약 flags, 범위를 벗어난 필드, CRC 오류는 파싱 실패 코드로 반환합니다. 실행이 중단되거나 0값의 정상 스윙을 만들어서는 안 됩니다. 보정 미완료 SWING은 패킷 해석 자체는 가능하지만 SDK에서 게임 이벤트로 내보내지 않고 상태 경고를 표시합니다.

정상·오류 데이터는 [공통 테스트 벡터](../testing/protocol-vectors.json)에 있습니다. 입력은 테스트용이며 실기 로그가 아닙니다.

## 소프트웨어 지원과 실물 인식

v2의8종 의도는 소프트웨어 전송 계약이며 실제8제스처 인식률을 의미하지 않습니다. 기본 스윙/버튼·경기 문맥 매핑과 실제 모델·임계값 튜닝을 구분합니다. SDK는 보정중 BUSY ACK를 최종 성공/실패로 간주하지 않고 원래5초 제한 안에서 완료ACK를 기다립니다. 연결/보정/서브·스윙·스킬 테스트를 구분하며 저장만 입력 소스를 바꿉니다.

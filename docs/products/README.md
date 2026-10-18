# 제품별 상세 개발 과제

각 문제는 상황, 선행 조건, 입력, 출력, 동작 규칙, 예제, 예외, 구현 순서, 완료 판정, 제출 결과를 제공합니다. 초기 개발의 학습·분담 기준을 보존한 과제집이며 현재 미완료 목록은 아닙니다. 처음 참여하면 제품 README로 환경을 준비하고, 과제를 읽어 역할과 수용 기준을 이해한 뒤 최신 검수 기록을 확인합니다. [WBS](../planning/wbs.md)는 원래 선행 관계를 제공합니다.

| 제품 | 과제 수 | 먼저 구현할 것 |
| --- | --- | --- |
| [외장 IMU 펌웨어](digital-tennis-firmware.md) | 6 | FW-01 외장 IMU를 연결하고 배선을 설명하기 |
| [컨트롤러 통신 규격](digital-tennis-protocol.md) | 4 | PR-01 하드웨어와 PC가 합의하는 계약 작성 |
| [PC BLE와 Unity 입력 SDK](digital-tennis-ble-unity.md) | 4 | BL-01 표준 입력과 가상 컨트롤러 |
| [Unity PC 테니스 게임](digital-tennis-game.md) | 9 | GM-01 공통 Unity 환경과 테스트 코트 |
| [독립 AI 플레이어](digital-tennis-ai.md) | 4 | AI-01 Unity에 의존하지 않는 AI 상태와 결정 API |
| [온라인 매칭 서버](digital-tennis-match-server.md) | 6 | MS-01 6자리 방 코드와 2인 방 관리 |
| [개발 문서와 WBS](digital-tennis-docs.md) | 4 | DC-01 제품 과제와 환경표를 한 곳에 정리 |

총 37개 제품 과제를 72개 반일 작업으로 나누어 진행합니다. 같은 과제 번호가 여러 WBS에 나타나면 순수 기능·실물 통합·측정으로 나눈 것입니다. 코드와 완료 증거가 생기면 제품 README의 현재 상태를 갱신합니다.

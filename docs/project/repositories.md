# 제품별 저장소와 책임

7개 제품을 기능별로 분리합니다. 각 저장소의 루트 README가 해당 제품의 소개·실행·기여 시작점이며, 아래 역할 A/B/C는 초기 12일·3인 계획의 분담입니다.

| 저장소 | 책임 | 담당 역할 | 개발 과제 |
| --- | --- | --- | --- |
| [digital-tennis-firmware](https://github.com/digital-tennis/digital-tennis-firmware) | NU40-DK에 별도로 부착한 IMU의 데이터 획득, 보정, 스윙 인식, BLE 전송 | A | [상세 과제](../products/digital-tennis-firmware.md) |
| [digital-tennis-protocol](https://github.com/digital-tennis/digital-tennis-protocol) | 보드와 PC가 공유하는 바이너리 규격, C 및 C# 코덱과 테스트 벡터 | C / A 검토 | [상세 과제](../products/digital-tennis-protocol.md) |
| [digital-tennis-ble-unity](https://github.com/digital-tennis/digital-tennis-ble-unity) | macOS·Windows BLE 검색·OS 본딩·연결 수명, 패킷 검증과 정규화 입력 | C / A 검토 | [상세 과제](../products/digital-tennis-ble-unity.md) |
| [digital-tennis-game](https://github.com/digital-tennis/digital-tennis-game) | 공·코트·서브·점수, 자동 이동, 1인 플레이, 온라인 2인 플레이 | B | [상세 과제](../products/digital-tennis-game.md) |
| [digital-tennis-ai](https://github.com/digital-tennis/digital-tennis-ai) | 예상 착지점, 이동·타격 의사결정, 하·중·상 난이도 | B | [상세 과제](../products/digital-tennis-ai.md) |
| [digital-tennis-match-server](https://github.com/digital-tennis/digital-tennis-match-server) | 6자리 방 코드, 2인 방, WebSocket 시그널링, 릴레이 | C / A 검토 | [상세 과제](../products/digital-tennis-match-server.md) |
| [digital-tennis-docs](https://github.com/digital-tennis/digital-tennis-docs) | GitBook 목차, 제품별 과제, 일정, 수용 테스트, 포트폴리오 증거 | C / 전원 검토 | [상세 과제](../products/digital-tennis-docs.md) |

## 이름 변경 대응

| 이전 계획명 | 확정 이름 |
| --- | --- |
| motion-tennis-firmware | digital-tennis-firmware |
| motion-tennis-protocol | digital-tennis-protocol |
| motion-tennis-ble-unity | digital-tennis-ble-unity |
| motion-tennis-game | digital-tennis-game |
| motion-tennis-ai | digital-tennis-ai |
| motion-tennis-match-server | digital-tennis-match-server |
| 문서 저장소 추가 | digital-tennis-docs |

## 저장소 사이의 경계

```text
외장 IMU → firmware ── BLE 패킷 ──→ ble-unity → RacketInput → game
                 ↑ protocol 규격 ↑                       ↑ ai 의사결정
                                                         ↕
                         match-server ← 방 코드·시그널링·릴레이
                                  PC 호스트 ↔ PC 게스트 P2P
```

- `protocol`은 UnityEngine 또는 실제 BLE를 참조하지 않습니다.
- `firmware`는 게임 점수·충돌 규칙을 알지 않습니다.
- `ble-unity`는 공·득점을 계산하지 않습니다.
- `ai`는 Unity 씬·GameObject 없이 상태를 받아 의사결정만 반환합니다.
- `game`은 호스트 권위의 공·득점과 `MatchClient`, P2P 전송 어댑터를 소유합니다.
- `match-server`는 같은 방의 메시지만 전달하며 테니스 물리를 계산하지 않습니다.
- `docs`는 통합 계약·과제·검증 안내를 연결합니다. 제품별 현재 실행 명령은 각 제품 README를 따릅니다.

## 의존성 사용 방법

현재 C 코덱은 CMake의 고정 Git 커밋으로, C# protocol·BLE·AI는 Git UPM의 고정 커밋으로 소비합니다. 최초 D1의 도구 선택 과제는 원래 WBS에 보존합니다. `main`의 변화에 자동으로 따라가지 않도록 소비 제품에 버전과 커밋을 기록합니다. 별도의 온라인 규격은 docs에서 관리하며 BLE 패킷과 혼용하지 않습니다.

각 제품은 하드웨어나 다른 제품 없이 가짜 입력으로 단독 검증하는 방법을 제공해야 합니다. 게임 동작을 제품 간에 복사하지 않습니다.

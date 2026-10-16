# 12일 3인 개발 WBS

> 초기 설계/과제와 현재 완료 상태는 다릅니다. [2026-10-16 구현 현황](../project/implementation-status.md)을 먼저 확인하세요. 직접 P2P·실물 BLE·Windows 실기는 별도 증거가 필요합니다.

총 공수는 **3명 × 12일 = 36인일**입니다. 한 사람의 하루를 0.5인일 작업 두 개로 나누어 **72개 세부 작업**을 배치했습니다. 아래 시간은 계획값이며 완료 기록이 아닙니다. A·B·C는 사람 이름 대신 역할입니다.

## 단계와 마일스톤

| 기한 | 제출 결과 | 지연 시 판단 |
| --- | --- | --- |
| D1 | 실제 부품·도구 버전·v1 입력 계약 | 미정 항목을 결정 기록에 남김 |
| D2 | 외장 IMU ID·샘플, Windows BLE 초기 수신 | 실물 경로 위험을 즉시 표시 |
| D3 | 두 Windows 빌드 P2P spike 결과 | 후보 고정 또는 차단 원인·대체 검증 |
| D4 | 가상 입력 서브·랠리·득점 | 물리·점수에 우선 집중 |
| D8 | 실물 타격·AI, P2P/릴레이 전송 통합 | 선택 기능 추가 중단 |
| D11 | 다른 PC 온라인 경기·QA 결과 | 결함 수정과 재현에 집중 |
| D12 | 실행 자산·기술 문서·시연·남은 문제 | 미완료를 완료로 바꾸지 않음 |

## 공수와 운영

A 12인일, B 12인일, C 12인일이며 어떤 사람도 하루 1인일을 초과하지 않습니다. D11~D12의 6인일은 QA·결함 수정·릴리스·문서로 예약했습니다. 멘토링과 통합 지원도 해당 작업 안의 공수입니다. 여러 과제의 선행 검증은 가짜 데이터로 진행하고 실제 의존성이 완성될 때 통합합니다. 같은 날짜에 의존성이 있으면 1번 슬롯 결과를 확인한 뒤 2번 슬롯을 진행합니다.

## 세부 작업

| WBS | 일자 | 담당 | 반일 슬롯 | 인일 | 과제 | 작업 | 선행 조건 | 제출 증거 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| W-01 | D1 | A | 1 | 0.5 | [FW-01](../products/digital-tennis-firmware.md#fw-01) | 외장 IMU·보드 사양과 배선 확정 | 없음 | 부품표·핀맵 |
| W-02 | D1 | A | 2 | 0.5 | [PR-01](../products/digital-tennis-protocol.md#pr-01) | 공통 패킷·역할 계약 검토 | C D1 초안 | v1 계약 검토 기록 |
| W-03 | D1 | B | 1 | 0.5 | [GM-01](../products/digital-tennis-game.md#gm-01) | Unity 버전·Windows 빌드 확인 | 없음 | 빈 실행 파일 |
| W-04 | D1 | B | 2 | 0.5 | [GM-01](../products/digital-tennis-game.md#gm-01) | 코트·공·플레이어 좌표 배치 | B D1 빌드 | 테스트 씬 |
| W-05 | D1 | C | 1 | 0.5 | [DC-01](../products/digital-tennis-docs.md#dc-01) | 저장소·문서 읽기와 환경표 | 없음 | 환경표·README |
| W-06 | D1 | C | 2 | 0.5 | [PR-01](../products/digital-tennis-protocol.md#pr-01) | 패킷 표와 정상 벡터 정리 | A D1 합의 | 계약 초안·벡터 |
| W-07 | D2 | A | 1 | 0.5 | [FW-02](../products/digital-tennis-firmware.md#fw-02) | 외장 센서 ID·통신 검증 | FW-01 | 실기 ID 로그 |
| W-08 | D2 | A | 2 | 0.5 | [FW-02](../products/digital-tennis-firmware.md#fw-02) | 100Hz 샘플·단위 변환 | A D2 ID | 6축 샘플 로그 |
| W-09 | D2 | B | 1 | 0.5 | [GM-02](../products/digital-tennis-game.md#gm-02) | 공 물리·바운스기초 | GM-01 | 바운스 씬 |
| W-10 | D2 | B | 2 | 0.5 | [GM-03](../products/digital-tennis-game.md#gm-03) | 서브 상태와 가상 입력 | GM-01 | 서브 시연 |
| W-11 | D2 | C | 1 | 0.5 | [BL-01](../products/digital-tennis-ble-unity.md#bl-01) | 가상 입력과 표준 인터페이스 | PR-01 | 가상 입력 출력 |
| W-12 | D2 | C | 2 | 0.5 | [BL-02](../products/digital-tennis-ble-unity.md#bl-02) | Windows standalone BLE 후보 검증 | FW-01, A 지원 | Notify 수신 로그 또는 이슈 |
| W-13 | D3 | A | 1 | 0.5 | [FW-03](../products/digital-tennis-firmware.md#fw-03) | 좌표 변환·정지 보정 | FW-02 | 보정·변환 예제 |
| W-14 | D3 | A | 2 | 0.5 | [BL-02](../products/digital-tennis-ble-unity.md#bl-02) | BLE·P2P 위험 검토와 C 지원 | C D2 결과, C D3 spike | 채택 후보·환경 기록 |
| W-15 | D3 | B | 1 | 0.5 | [GM-02](../products/digital-tennis-game.md#gm-02) | 공 충돌·경계 판정 | GM-02 | 첫/두 번째 바운스 테스트 |
| W-16 | D3 | B | 2 | 0.5 | [GM-04](../products/digital-tennis-game.md#gm-04) | 점수·듀스 순수 함수 | 없음 | 점수 사례 출력 |
| W-17 | D3 | C | 1 | 0.5 | [PR-02](../products/digital-tennis-protocol.md#pr-02) | C# 코덱과 오류 검증 | PR-01 | 벡터 테스트 결과 |
| W-18 | D3 | C | 2 | 0.5 | [GM-07](../products/digital-tennis-game.md#gm-07) | 2PC P2P Windows 빌드 spike | GM-01, A 지원 | DataChannel 송수신 또는 차단 원인 |
| W-19 | D4 | A | 1 | 0.5 | [PR-03](../products/digital-tennis-protocol.md#pr-03) | C 코덱과 공통 벡터 검증 | PR-02, C D3 | C/C# 값 일치 |
| W-20 | D4 | A | 2 | 0.5 | [FW-04](../products/digital-tennis-firmware.md#fw-04) | 필터·스윙 상태기계 시작 | FW-03 | 녹화 입력 이벤트 |
| W-21 | D4 | B | 1 | 0.5 | [GM-03](../products/digital-tennis-game.md#gm-03) | 서비스 폴트·렛·랠리 연결 | GM-02 | 가상 입력 경기 |
| W-22 | D4 | B | 2 | 0.5 | [GM-04](../products/digital-tennis-game.md#gm-04) | 득점 중복 방지·승패 | GM-03 | D4 기본 경기 시연 |
| W-23 | D4 | C | 1 | 0.5 | [BL-02](../products/digital-tennis-ble-unity.md#bl-02) | 검색·연결·Service 구독 | D2 BLE 후보 | Windows 수신 도구 |
| W-24 | D4 | C | 2 | 0.5 | [BL-03](../products/digital-tennis-ble-unity.md#bl-03) | 메인 스레드 큐·패킷 전달 | PR-02, BL-01 | 중복 없는 RacketInput |
| W-25 | D5 | A | 1 | 0.5 | [FW-04](../products/digital-tennis-firmware.md#fw-04) | 스윙 분류·파워 조정 | FW-04 | 유형별 이벤트 |
| W-26 | D5 | A | 2 | 0.5 | [FW-05](../products/digital-tennis-firmware.md#fw-05) | GATT 알림·명령 처리 | PR-02 | Notify·ACK 로그 |
| W-27 | D5 | B | 1 | 0.5 | [GM-05](../products/digital-tennis-game.md#gm-05) | 표준 입력 타격·자동 이동 | GM-04, BL-01 | 가상 입력 랠리 |
| W-28 | D5 | B | 2 | 0.5 | [AI-01](../products/digital-tennis-ai.md#ai-01) | Unity 독립 상태·정책 API | GM-02 | 정책 단독 실행 |
| W-29 | D5 | C | 1 | 0.5 | [MS-01](../products/digital-tennis-match-server.md#ms-01) | 방 코드·생성·참가 순수 로직 | 온라인 계약 | 충돌/인원 테스트 |
| W-30 | D5 | C | 2 | 0.5 | [MS-02](../products/digital-tennis-match-server.md#ms-02) | WebSocket 요청·응답 | MS-01 | 두 모의 클라이언트 |
| W-31 | D6 | A | 1 | 0.5 | [FW-05](../products/digital-tennis-firmware.md#fw-05) | 보정 명령·반복 이벤트 통합 | FW-03, FW-05 | 명령 결과·중복 벡터 |
| W-32 | D6 | A | 2 | 0.5 | [FW-06](../products/digital-tennis-firmware.md#fw-06) | 장착·연결 종료·버튼 검증 | FW-05 | 정지/버튼/센서 오류 로그 |
| W-33 | D6 | B | 1 | 0.5 | [AI-02](../products/digital-tennis-ai.md#ai-02) | 착지 예측·쉬움 정책 | AI-01 | 예측 사례·easy 랠리 |
| W-34 | D6 | B | 2 | 0.5 | [GM-06](../products/digital-tennis-game.md#gm-06) | 메뉴·연결·모드 UI | GM-05 | 1인 플레이 화면 |
| W-35 | D6 | C | 1 | 0.5 | [MS-03](../products/digital-tennis-match-server.md#ms-03) | 같은 방 시그널링전달 | MS-02 | offer/answer/ICE 로그 |
| W-36 | D6 | C | 2 | 0.5 | [BL-04](../products/digital-tennis-ble-unity.md#bl-04) | 재연결·보정 ACK 상태 | BL-03, FW-05 | 세션 초기화 로그 |
| W-37 | D7 | A | 1 | 0.5 | [FW-04](../products/digital-tennis-firmware.md#fw-04) | 측정 데이터로 임계값 보정 | FW-06 | 인식 정확도 표 |
| W-38 | D7 | A | 2 | 0.5 | [BL-03](../products/digital-tennis-ble-unity.md#bl-03) | 실물 입력→Unity 통합 지원 | BL-03, GM-05 | 실물 타격 로그 |
| W-39 | D7 | B | 1 | 0.5 | [AI-03](../products/digital-tennis-ai.md#ai-03) | 하·중·상 설정과 오류 | AI-02 | 세 정책 사례 |
| W-40 | D7 | B | 2 | 0.5 | [GM-06](../products/digital-tennis-game.md#gm-06) | 실물 입력·AI 경기 통합 | FW-05, BL-03 | 실제 컨트롤러 1게임 |
| W-41 | D7 | C | 1 | 0.5 | [MS-04](../products/digital-tennis-match-server.md#ms-04) | 릴레이·역할·epoch 검사 | MS-03 | 릴레이 메시지 테스트 |
| W-42 | D7 | C | 2 | 0.5 | [GM-07](../products/digital-tennis-game.md#gm-07) | MatchClient 코드 참가·전송 경계 | MS-02, D3 spike | 온라인 로비 연결 |
| W-43 | D8 | A | 1 | 0.5 | [FW-06](../products/digital-tennis-firmware.md#fw-06) | 라켓 장착·센서 이상 검증 | FW-06 | 실기 실패 경로 |
| W-44 | D8 | A | 2 | 0.5 | [GM-07](../products/digital-tennis-game.md#gm-07) | P2P·릴레이 선택 계약 검토 | MS-04, GM-07 | 양쪽 mode·epoch 일치 |
| W-45 | D8 | B | 1 | 0.5 | [AI-04](../products/digital-tennis-ai.md#ai-04) | seed·반응 시간·단독 검증 | AI-03 | 재현 가능한 AI 결과 |
| W-46 | D8 | B | 2 | 0.5 | [GM-05](../products/digital-tennis-game.md#gm-05) | D8 실물·AI 플레이 검증 | BL-04, AI-03 | D8 통합 영상 |
| W-47 | D8 | C | 1 | 0.5 | [GM-07](../products/digital-tennis-game.md#gm-07) | 시그널링·직접 DataChannel 연결 | MS-03, D3 spike | 직접 경로 증거 |
| W-48 | D8 | C | 2 | 0.5 | [MS-04](../products/digital-tennis-match-server.md#ms-04) | 강제 실패·릴레이 전환 | GM-07, MS-04 | 8초 전환 로그 |
| W-49 | D9 | A | 1 | 0.5 | [FW-04](../products/digital-tennis-firmware.md#fw-04) | 정지 오검출·세 스윙 측정 | D8 실물 통합 | AT-03/04 결과 |
| W-50 | D9 | A | 2 | 0.5 | [GM-08](../products/digital-tennis-game.md#gm-08) | 호스트 권위·중복 입력 검토 | B/C 온라인 연결 | 득점 중복 0 기록 |
| W-51 | D9 | B | 1 | 0.5 | [GM-08](../products/digital-tennis-game.md#gm-08) | 호스트 snapshot·게스트 보간 | GM-07 | 상태 송수신 |
| W-52 | D9 | B | 2 | 0.5 | [GM-08](../products/digital-tennis-game.md#gm-08) | 점수·phase·결과 동기화 | GM-08 | 양 PC 같은 결과 |
| W-53 | D9 | C | 1 | 0.5 | [MS-05](../products/digital-tennis-match-server.md#ms-05) | 끊김·heartbeat·재접속 | MS-04 | pause/resume 로그 |
| W-54 | D9 | C | 2 | 0.5 | [MS-06](../products/digital-tennis-match-server.md#ms-06) | 서버 실행·배포 안내 | MS-05 | 재현 가능한 실행 환경 |
| W-55 | D10 | A | 1 | 0.5 | [FW-06](../products/digital-tennis-firmware.md#fw-06) | 센서·BLE 연속 실행 확인 | D9 인식 조정 | 30분 관측 기록 |
| W-56 | D10 | A | 2 | 0.5 | [GM-08](../products/digital-tennis-game.md#gm-08) | 2PC 회귀·P2P 경로 검증 | GM-08, MS-05 | AT-13/14 결과 |
| W-57 | D10 | B | 1 | 0.5 | [GM-08](../products/digital-tennis-game.md#gm-08) | 지연·중복·역순 상태 검증 | GM-08 | AT-15 결과 |
| W-58 | D10 | B | 2 | 0.5 | [GM-06](../products/digital-tennis-game.md#gm-06) | 재접속·중단·결과 UI | MS-05 | 오류 상태 시연 |
| W-59 | D10 | C | 1 | 0.5 | [MS-05](../products/digital-tennis-match-server.md#ms-05) | 다른 네트워크·재접속 검증 | MS-06 | AT-16/17 결과 |
| W-60 | D10 | C | 2 | 0.5 | [BL-04](../products/digital-tennis-ble-unity.md#bl-04) | 입력 지연·재연결 측정 | BL-04 | PC내 p95·누락 통계 |
| W-61 | D11 | A | 1 | 0.5 | [FW-06](../products/digital-tennis-firmware.md#fw-06) | 펌웨어 QA·결함 수정 여유 | AT-01~07 | 회귀 결과 |
| W-62 | D11 | A | 2 | 0.5 | [DC-03](../products/digital-tennis-docs.md#dc-03) | 배선·보정·펌웨어 설치 문서 | FW-06 | 따라할 수 있는 안내 |
| W-63 | D11 | B | 1 | 0.5 | [GM-09](../products/digital-tennis-game.md#gm-09) | Windows 빌드·플레이 QA | AT-08~11 | 릴리스 후보 |
| W-64 | D11 | B | 2 | 0.5 | [GM-09](../products/digital-tennis-game.md#gm-09) | 결함 수정 여유·회귀 | B D11 QA | 회귀 결과 |
| W-65 | D11 | C | 1 | 0.5 | [DC-03](../products/digital-tennis-docs.md#dc-03) | 2PC 통합·결함 수정 여유 | D10 네트워크 | AT-12~17 결과 |
| W-66 | D11 | C | 2 | 0.5 | [DC-02](../products/digital-tennis-docs.md#dc-02) | GitBook 목차·링크·동기화 | DC-01 | 사이트 검증 |
| W-67 | D12 | A | 1 | 0.5 | [DC-03](../products/digital-tennis-docs.md#dc-03) | 외장 컨트롤러 최종 시연 | D11 QA | 실기 증거 |
| W-68 | D12 | A | 2 | 0.5 | [PR-04](../products/digital-tennis-protocol.md#pr-04) | 펌웨어·공통 버전표 공개 | 전원 검증 | 릴리스·SHA표 |
| W-69 | D12 | B | 1 | 0.5 | [GM-09](../products/digital-tennis-game.md#gm-09) | 깨끗한 Windows 실행 검증 | D11 빌드 | AT-18 결과 |
| W-70 | D12 | B | 2 | 0.5 | [DC-04](../products/digital-tennis-docs.md#dc-04) | 게임·AI 시연·포트폴리오 | AI-04, GM-09 | 영상·남은 문제 |
| W-71 | D12 | C | 1 | 0.5 | [DC-03](../products/digital-tennis-docs.md#dc-03) | P2P·릴레이 최종 증거 | D11 2PC 검증 | 분리된 판정 |
| W-72 | D12 | C | 2 | 0.5 | [DC-04](../products/digital-tennis-docs.md#dc-04) | 문서·서버 릴리스·최종 체크 | 전원 검증 | GitBook·문서·버전표 |

## 상태 관리

구현을 시작하면 작업별 Todo·Doing·Review·Done·Blocked를 Issue 또는 이 표에 기록합니다. Done은 해당 과제의 완료 기준과 증거가 있을 때만 사용합니다. 한 과제는 여러 반일 작업을 포함할 수 있으므로 일부 WBS 완료와 전체 과제 완료를 구분합니다. 일정 변경 시 36인일 합계와 새 선행 조건을 다시 확인합니다.

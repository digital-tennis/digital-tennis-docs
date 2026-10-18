# DT-TR-23-10-00 · 실물 컨트롤러 본딩 검수

문서 개정 **R02**, 2026-10-19, 검토본. 실제 제품은 **NU40-DK+별도 외장 IMU**이며 이번 실기 기기는 센서 없는 NU-54다. [책임 분리와 ADR](architecture.md), [통신 계약](../contracts/controller-protocol.md)을 따른다.

## 00 현재 결과

**Mac 일반 Unity 창에서 실제 암호화·본딩, 테니스 프로토콜 왕복, 보드 재시작 후 본딩 재사용을 통과했다.** 센서가 없어 ready/calibrated는 false이고 동작 테스트·설정 저장은 계속 차단된다.

| 확인 항목 | 실제 결과 |
| --- | --- |
| 메뉴·설정 | 실제 키보드로 시작 메뉴→설정→입력 기기→무선 상세 진입 |
| 실제 검색 | clean 빌드 첫 검색은 0기기, 명시적 재검색에서 알려진 Tennis 기기 발견 |
| 연결 | 현재 상대의 보호된 보안 상태 확인 후 Connected |
| 테니스 메시지 | 현재 연결·nonce에 대응하는 LINK_PROBE/REPLY 성공 |
| 센서 없는 보정 요청 | 실패 ACK, ready/calibrated=false, 세 동작 테스트·저장 차단 |
| 연결 해제·재연결 | 이전 통신 확인을 폐기하고 새 연결에서 다시 왕복 성공 |
| 보드 일반 reset | 단절 후 저장된 본딩으로 재연결, 새 probe 성공 |
| 취소 | 기존 Keyboard 유지, 경기 타격·득점·입력 0 |

최종 일반 창은 소스 **bf86e40147d1acee1a03e1139494759054ab0317**, Unity6000.3.26f1, Built-in/Mono의 깨끗한 새 검수 빌드다. 실제 네이티브 backend와 키보드를 유지했고 관찰 옵션만 사용했다. 모의 전송·가짜 기기·UI callback 직접 호출·저장 게이트 우회는 사용하지 않았다. 세부 원본 PNG·JSON과 해시는 [기계 판독 결과](../testing/controller-bonding-validation.json)에서 추적한다. [실제 게임 화면·원본 자료](https://github.com/digital-tennis/digital-tennis-game/blob/7af42a20b42975b21a41ab3f7055c6846fb510e9/docs/controller-bonding.md)를 함께 확인한다.

## 10 보안 근거와 제한

별도 native 진단은 보호된 4바이트 상태의 **Level2/bonded/SC**와 실제 20바이트 응답을 확인했다. 해당 왕복 52.131ms는 단일 관찰값이다. macOS Bluetooth에서도 알려진 Tennis 기기가 연결됨으로 표시됐다. OS 키 데이터베이스를 직접 열람하거나 기기 UUID·주소·키·PIN을 공개하지 않았다.

현재 시험 정책은 승인된 **LE Secure Connections + Just Works**다. 암호화·본딩은 요구하지만 PIN/숫자 대조를 통한 최초 페어링 중간자 방어는 없다. 이번 성공 중 새로운 PIN/숫자 대조 팝업은 나타나지 않았으므로 팝업을 조작한 검증으로 기록하지 않는다.

보드 reset은 flash·저장영역 읽기·초기화 없이 수행했다. 이전에 승인받아 설치한 Tennis 이미지와 분리된 영속 identity1을 유지한다. 검증 종료 후 임시 교체한 게임 앱은 원래 백업으로 복원했고 본딩은 유지했다.

NU40-DK 실물 GPIO/BLE, 별도 외장 IMU의 배선·장착·보정·인식률, 물리 Windows와 두 물리 PC/WAN은 남아 있다. 본딩이 없는 새 PC의 최초 승인 팝업 조작도 별도 항목이다. 원래12일·3명 범위를 보존하며 센서 없는 성공을 모션 경기 성공으로 표시하지 않는다.

## 15 이전 시도와 소프트웨어 근거

이전 R01의 Level4 기능 불일치·ATT15·SMP timeout, 잠금 상태·일부 검색0과 독립 Mono 검색/보안 timeout은 당시 실패 이력으로 보존한다. 이번 잠금 해제 후 clean 일반 창 실행으로 실제 본딩·왕복·재시작 재사용 미검증을 해소했다. 과거 실패 객체는 기계 판독 결과의 `previousUnverifiedAttempt`에 남긴다.

기존 소프트웨어 근거는 Unity Edit189/189·Play43통과/NullGPU1제외·별도 GPU마우스1/1·패킷장면1/1, protocol 이벤트2,045/보안66,046사례, SDK44·AI25·서버28개, firmware host2모음/보드3구성이다. 실제 라디오 결과와 자동 검사·교차 빌드를 구분한다. 이번 후속 변경은 실기 자료와 지원 상태 문서이며 런타임 코드를 수정하지 않았다.

[README/라이선스 운영](open-source.md)과 [펌웨어 빌드·설치 근거](https://github.com/digital-tennis/digital-tennis-firmware/pull/2)를 함께 확인한다.

## 20 검토 PR

모두 draft이며 병합하지 않았다. protocol→firmware/SDK→game→docs 순서로 검토하고, 스쿼시 병합 후 소비 SHA를 새 병합 커밋으로 다시 고정한다. AI는 README/라이선스만 변경했다.

| 제품 | PR | 검증한 실행 코드 |
| --- | --- | --- |
| digital-tennis-protocol | [#2](https://github.com/digital-tennis/digital-tennis-protocol/pull/2) | 12dae689fd9b |
| digital-tennis-firmware | [#2](https://github.com/digital-tennis/digital-tennis-firmware/pull/2) | 4a55c57146ea |
| digital-tennis-ble-unity | [#2](https://github.com/digital-tennis/digital-tennis-ble-unity/pull/2) | a7efc76b5d53 |
| digital-tennis-game | [#25](https://github.com/digital-tennis/digital-tennis-game/pull/25) | bf86e40147d1 (clean 일반 창) |
| digital-tennis-ai | [#4](https://github.com/digital-tennis/digital-tennis-ai/pull/4) | 7053a4e74c25 |
| digital-tennis-match-server | [#6](https://github.com/digital-tennis/digital-tennis-match-server/pull/6) | d064ade0c60a |
| digital-tennis-docs | [#3](https://github.com/digital-tennis/digital-tennis-docs/pull/3) | 이 문서 PR |


## 30 최신 검토 배포판

Game5203b381의 clean 소스로 Development/AllowDebugging을 끄고 Mac·Windows 빌드를 생성했다. native staging과 결과 디렉터리는 생성물을 새로 만들어 이전 게시물의 중복 파일을 제외한다. 자체/UPM·외부 라이선스, Mac deep/strict 서명, 두 ZIP의 CRC/SHA256을 확인했다. Mac은 로컬 ad-hoc 검토용이며 Windows는 교차 빌드다. 이 배포는 main·스토어·운영 서버 배포가 아니며 실물 본딩 성공을 의미하지 않는다. 큰 ZIP은 Git 밖 작업 전달 폴더에 보관한다.

| 파일 | 바이트 | SHA256 |
| --- | --- | --- |
| DigitalTennis-release-mac-5203b381.zip | 93711515 | e8bfbbc5fe11299fac89c25e10bd3e04cb755f39237b8cdf7cedcf05f6545b6a |
| DigitalTennis-release-windows-5203b381.zip | 143390655 | 6c1bb3ead0f6b6c8ca1faa9686917d08de2589b0e092bc0624e69e13eec3271f |

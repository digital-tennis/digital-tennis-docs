# DT-TR-23-10-00 · 실물 컨트롤러 본딩 검수

문서 개정 R01, 2026-10-19, 검토본. 실제 제품은 NU40-DK+별도 외장 IMU다. 현재 연결된 NU-54는 센서 없는 BLE 검증용이다. [책임 분리와 ADR](architecture.md), [통신 계약](../contracts/controller-protocol.md)을 따른다.

## 현재 결과

사용자 승인으로 테니스 펌웨어를 NU-54에 설치했다. 이전 앱의 변경 대상 코드만 비공개 백업했고 기존 지갑 저장영역은 읽거나 지우지 않았다. Unity 무선 상세에서 Digital Tennis NU54 광고 검색과 연결 요청을 수행했다. 최초 시험은 인증된 보안 Level4 요구와 화면 없는 보드의 기능 불일치로 실패했다. 이를 본딩 성공으로 기록하지 않는다.

사용자는 LE Secure Connections + Just Works(L2) 방식 적용을 명시적으로 승인했다. PIN/숫자 대조 MITM 인증은 없지만 암호화·본딩을 요구한다. 수정 펌웨어의 코드 대조/설치를 통과했고, 기존 앱 캐시와 분리된 Tennis identity1을 사용한다. 최초 보호된 CCC 시도는 ATT 오류15(암호화 미완료)·SMP timeout으로 끝났다. SDK는 이를 성공으로 바꾸지 않으며 OS 처리 동안 연결을 조기에 끊지 않도록 제한 재시도를 추가했다. 현재 Mac 수동 잠금 해제를 기다려 일반 창의 OS 승인·재접속 검수를 이어간다. **실물 본딩과 테니스 메시지 왕복은 아직 미완료**이며 센서 실기도 계속 유예한다.

## 완료 증거에 필요한 항목

현재 peer의 보호된4바이트 보안 읽기, 같은 nonce의20바이트 LINK_REPLY, Unity 통신 성공 화면, 센서 미준비/저장 차단, 해제/재접속 및 보드 재시작 후 키 재사용을 각각 기록한다. 기기 주소/UUID·키·PIN·원시 지갑 응답·백업은 공개하지 않는다.

[README/라이선스 운영](open-source.md), [펌웨어 빌드·설치 근거](https://github.com/digital-tennis/digital-tennis-firmware/blob/codex/controller-readiness/docs/bonding-build-validation.json)를 함께 확인한다.


## 10 소프트웨어와 실제 라디오의 경계

최종 Unity 검사는 Edit189/189, Play43통과·실패0·NullGPU1제외이며 별도 GPU 마우스1/1·패킷 장면1/1을 구분한다. protocol 이벤트2,045·보안66,046사례, SDK44·AI25·서버28개 검사와 firmware host2모음/보드3구성이 통과했다. GitHub의 허가된 Unity job은 설정상 건너뛰며 이 결과는 로컬 Unity 검사다.

동일한 게임 SDK DLL을 Unity 동봉 Mono에서 실행한 독립 진단은 실제 NU54 검색1기기·한글 native 메시지 수신을 통과했다. 보안 연결은60초 뒤 Error/Bond=false로 종료돼 입력을 열지 않았다. 일반 창의 일부0기기 결과와 독립 진단의1기기 결과를 구분한다. 추가한 선택적 진단으로 Mac 잠금 해제 후 최신 일반 창 경로를 확인해야 하며, 독립 Mono 실행을 Unity UI 연결 성공으로 바꾸어 표기하지 않는다.

Tennis identity는 보드 재시작 전후 같았으나 이는 identity 저장의 근거다. 암호화/bond 성공·bond 키 재사용은 별도이며 아직 증거가 없다. Mac의 OS 키 DB·키·PIN·주소를 공개하거나 조회하지 않는다. [기계가 읽는 결과](../testing/controller-bonding-validation.json)를 확인한다.

## 20 검토 PR

모두 draft이며 병합하지 않았다. protocol→firmware/SDK→game→docs 순서로 검토하고, 스쿼시 병합 후 소비 SHA를 새 병합 커밋으로 다시 고정한다. AI는 README/라이선스만 변경했다.

| 제품 | PR | 검토 소스 |
| --- | --- | --- |
| digital-tennis-protocol | [#2](https://github.com/digital-tennis/digital-tennis-protocol/pull/2) | 12dae689fd9b |
| digital-tennis-firmware | [#2](https://github.com/digital-tennis/digital-tennis-firmware/pull/2) | 4a55c57146ea |
| digital-tennis-ble-unity | [#2](https://github.com/digital-tennis/digital-tennis-ble-unity/pull/2) | a7efc76b5d53 |
| digital-tennis-game | [#25](https://github.com/digital-tennis/digital-tennis-game/pull/25) | 5203b3813312 |
| digital-tennis-ai | [#4](https://github.com/digital-tennis/digital-tennis-ai/pull/4) | 7053a4e74c25 |
| digital-tennis-match-server | [#6](https://github.com/digital-tennis/digital-tennis-match-server/pull/6) | d064ade0c60a |
| digital-tennis-docs | [#3](https://github.com/digital-tennis/digital-tennis-docs/pull/3) | 이 문서 PR |


## 30 최신 검토 배포판

Game5203b381의 clean 소스로 Development/AllowDebugging을 끄고 Mac·Windows 빌드를 생성했다. native staging과 결과 디렉터리는 생성물을 새로 만들어 이전 게시물의 중복 파일을 제외한다. 자체/UPM·외부 라이선스, Mac deep/strict 서명, 두 ZIP의 CRC/SHA256을 확인했다. Mac은 로컬 ad-hoc 검토용이며 Windows는 교차 빌드다. 이 배포는 main·스토어·운영 서버 배포가 아니며 실물 본딩 성공을 의미하지 않는다. 큰 ZIP은 Git 밖 작업 전달 폴더에 보관한다.

| 파일 | 바이트 | SHA256 |
| --- | --- | --- |
| DigitalTennis-release-mac-5203b381.zip | 93711515 | e8bfbbc5fe11299fac89c25e10bd3e04cb755f39237b8cdf7cedcf05f6545b6a |
| DigitalTennis-release-windows-5203b381.zip | 143390655 | 6c1bb3ead0f6b6c8ca1faa9686917d08de2589b0e092bc0624e69e13eec3271f |

# DT-TR-23-10-00 · 실물 컨트롤러 본딩 검수

문서 개정 R01, 2026-10-19, 검토본. 실제 제품은 NU40-DK+별도 외장 IMU다. 현재 연결된 NU-54는 센서 없는 BLE 검증용이다. [책임 분리와 ADR](architecture.md), [통신 계약](../contracts/controller-protocol.md)을 따른다.

## 현재 결과

사용자 승인으로 테니스 펌웨어를 NU-54에 설치했다. 이전 앱의 변경 대상 코드만 비공개 백업했고 기존 지갑 저장영역은 읽거나 지우지 않았다. Unity 무선 상세에서 Digital Tennis NU54 광고 검색과 연결 요청을 수행했다. 최초 시험은 인증된 보안 Level4 요구와 화면 없는 보드의 기능 불일치로 실패했다. 이를 본딩 성공으로 기록하지 않는다.

사용자는 LE Secure Connections + Just Works(L2) 방식 적용을 명시적으로 승인했다. PIN/숫자 대조 MITM 인증은 없지만 암호화·본딩을 요구한다. 수정 펌웨어의 코드 대조/설치를 통과했고, 기존 앱 캐시와 분리된 Tennis identity1을 사용한다. 최초 보호된 CCC 시도는 ATT 오류15(암호화 미완료)·SMP timeout으로 끝났다. SDK는 이를 성공으로 바꾸지 않으며 OS 처리 동안 연결을 조기에 끊지 않도록 제한 재시도를 추가했다. 현재 Mac 수동 잠금 해제를 기다려 일반 창의 OS 승인·재접속 검수를 이어간다. **실물 본딩과 테니스 메시지 왕복은 아직 미완료**이며 센서 실기도 계속 유예한다.

## 완료 증거에 필요한 항목

현재 peer의 보호된4바이트 보안 읽기, 같은 nonce의20바이트 LINK_REPLY, Unity 통신 성공 화면, 센서 미준비/저장 차단, 해제/재접속 및 보드 재시작 후 키 재사용을 각각 기록한다. 기기 주소/UUID·키·PIN·원시 지갑 응답·백업은 공개하지 않는다.

[README/라이선스 운영](open-source.md), [펌웨어 빌드·설치 근거](https://github.com/digital-tennis/digital-tennis-firmware/blob/codex/controller-readiness/docs/bonding-build-validation.json)를 함께 확인한다.

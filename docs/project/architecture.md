# 시스템 구조와 통합 순서

> 초기 설계/과제와 현재 완료 상태는 다릅니다. [2026-10-16 구현 현황](../project/implementation-status.md)을 먼저 확인하세요. 직접 P2P·실물 BLE·Windows 실기는 별도 증거가 필요합니다.

외장 IMU 드라이버는 단위가 정규화된 샘플을 반환하고, 스윙 인식기는 샘플을 이벤트로 바꿉니다. 펌웨어는 이벤트를 공통 패킷으로 인코딩합니다. Windows BLE SDK는 수신한 패킷을 검증한 뒤 Unity 메인 스레드에서 `RacketInput`으로 전달합니다.

## 입력 경계

```text
ImuSample {deviceTimeMs, accelG[3], gyroDps[3], sensorReady}
SwingEvent {eventId, kind, power, yawDeg, pitchDeg, calibrated}
RacketInput {sessionId, eventId, kind, power01, aimX, aimZ, receivedAtMs, source}
```

`sessionId`는 PC가 연결마다 부여하는 식별자입니다. `eventId`는 같은 스윙의 재전송을 구별합니다. `receivedAtMs`는 PC 단조 시각이며 MCU 시각과 직접 비교하지 않습니다. `power01=power/100`입니다. 방향 변환은 좌표계 계약을 따른 뒤 게임에서만 샷 속도로 바꿉니다.

## 온라인의 권위

호스트 PC만 공의 이동·충돌·득점·승패를 확정합니다. 게스트는 자신의 입력을 호스트에 보내며 호스트 상태를 화면에 보간합니다. 호스트와 게스트의 Unity 물리가 같은 결과를 낼 것이라고 가정하지 않습니다. 온라인에서 게스트 AI는 동작하지 않습니다.

`IGameTransport.Send/Receive/Close` 경계 안에서 P2P DataChannel과 WebSocket 릴레이를 교체합니다. WebSocket은 방 코드와 P2P 연결 정보의 전달 경로이며 그 자체가 직접 P2P는 아닙니다. ICE/STUN/TURN 관련 설명은 [WebRTC 공식 자료](https://webrtc.org/getting-started/peer-connections)를 참고합니다.

Unity 공식 WebRTC 저장소는 확인 시점에 deprecated로 표시되어 있습니다. D3까지 **Editor가 아닌 Windows 실행 파일**로 패키지·백엔드 호환성을 확인하고 버전 고정 여부를 결정합니다. [공식 저장소](https://github.com/Unity-Technologies/com.unity.webrtc)

## 통합 순서

1. protocol 테스트 벡터를 C/C# 양쪽에서 해석합니다.
2. 가상 컨트롤러로 게임의 서브·득점을 만듭니다.
3. 외장 IMU 샘플→이벤트를 시리얼 로그로 확인합니다.
4. Windows BLE 도구로 Notify→표준 입력을 확인합니다.
5. 실물 입력을 게임에 넣고 AI를 연결합니다.
6. 릴레이로 호스트 권위의 2PC 상태를 먼저 검증합니다.
7. 동일 메시지를 P2P로 전달하고 강제 실패 시 릴레이 전환을 검증합니다.

P2P 검증이 늦어져도 다른 기능은 계속 진행합니다. 직접 연결을 달성하지 못했다면 요구사항 미충족으로 보고하고, 릴레이 데모와 구분합니다.

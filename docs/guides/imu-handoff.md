# 외장 IMU를 가진 개발자에게 인수하기

2026-10-20 기준. 제품은 **NU40-DK + 별도 부착 외장 IMU**이며, 최초12일·3명·36PD 계획을 유지합니다. 현재 사용자는 IMU를 보유하지 않으므로 실제 센서 검증은 후속 담당자가 수행합니다. NU54의 BLE/버튼 검증은 센서 인식 증거가 아닙니다.

[펌웨어의 상세 개발 인수 가이드](https://github.com/digital-tennis/digital-tennis-firmware/blob/46881a8e0610b9439d77785f06186e1f77e3535b/docs/imu-developer-handoff.md)에 배선 확인표, 함수별 수정 위치, 과제 입력/출력과 완료 기준을 정리했습니다. [Air Band 참고 적용과 기록·재생 안내](imu-air-band.md)는 새 가속도 피크 처리 경로를 설명합니다. 실물 센서를 연결한 결과와 합성 입력 결과를 구분합니다.

## 책임과 수정 순서

| 계층 | 담당 코드 | 바꿀 내용 |
| --- | --- | --- |
| firmware | external_imu.c, dt_controller.h/c, main.c, 검토한 overlay | 단위/ODR·축·보정·스윙 구간·제스처 분류 |
| protocol | controller-v2.md, ControllerPacket.cs의 PacketCodec, dt_protocol.h/c, test-vectors.json | 새 액션/필드가 생길 때만 공통 C/C#·버전·벡터 함께 변경 |
| ble-unity | BleControllerClient.cs | 현재 본딩 연결·보정 ACK·flags·중복/시각 검사, 단위 정규화 |
| game | NativeControllerBackend, ControllerDevices의 InputDeviceManager, ControllerSetupSession, PlayerInputAdapter | 사용 기기 선택·테스트·저장, 의도→일반 입력 변환 |
| game rules | TennisMatchController.SubmitInput, RacketInput/RacketShot | 타격 거리/높이/phase·물리·스킬·점수 |

현재 raw6축을PC로 모아 분류하는 구조가 아닙니다. 펌웨어가 액션을 판정하고20바이트 이벤트를 보냅니다. 새 IMU가 같은 샘플 단위와 이벤트 계약을 만족하면 SDK/게임을 바꿀 필요가 없습니다. raw 분류를PC로 옮기려면 별도 샘플 계약·순번/손실·프레이밍·버전부터 설계해야 하며 현행 기능으로 안내하지 않습니다.

## 후속 담당자의 작업 순서

1. 보드/센서 모델·전압·버스·실제 헤더·주소·장착 방향을 기록합니다. 합성 MPU6050 fixture를 실제 배선으로 사용하지 않습니다.
2. Zephyr 드라이버의 유효6축과 시각을 확인하고, 실패할 때 false가 전달되는지 검증합니다.
3. 정지 보정, 축 행렬, 필터와 gyro+accel 피크/재무장 임계값을 실측 데이터로 조절합니다. 기본 임계값은 상품 정확도 근거가 아닙니다.
4. 실제FH/BH/서브와 오동작 데이터를 분리해 평가합니다. 특수샷의 모드 선택과 자동 제스처 인식을 구분합니다.
5. 호스트 재생·오류 검사 후 실제 NU40 빌드와 설치를 담당자가 수행합니다. 현재 연결된 NU54에는 추가 쓰기/버튼 시험을 하지 않습니다.
6. 실제 Unity의 무선 연결→보정→서브/스윙/스킬 테스트→저장→일반 경기 순서로 확인합니다. 수신 성공과 공 적중은 다른 결과입니다.

## 인수 결과물

실제 배선·장착표, 소스/도구/이미지 해시, 진단 CSV 설명, 호스트 검사, 분리된 평가 데이터의 혼동 행렬·오검출/누락/중복·지연 분포, Unity 일반 창 결과와 미검증 목록을PR에 포함합니다. 센서 정확도 합격 목표는 실물 담당자가 정한 값과 함께 기록합니다. 본딩 키·장치 주소·비공개 코드 백업은 공개하지 않습니다.

[통신 규격](../contracts/controller-protocol.md) · [기존 실물 본딩/버튼 범위](../project/controller-bonding.md)

## 2026-10-20 가상 모션 검증 추가

장비가 없는 상태에서의 다음 단계는 [가상 IMU 실험실](imu-tennis-simulator.md)입니다. 7종 C 분류와 물리 궤적을 비교하고 같은 overhead의 상황별 판정·약한 발리 누락을 재현할 수 있습니다. 실물 적용 전 수정 위치와 미구현 상태 전달 경계도 함께 확인합니다.

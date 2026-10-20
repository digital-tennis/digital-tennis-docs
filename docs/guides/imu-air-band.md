# NU40 외장 IMU: Air Band 참고 적용

> 현재 계약은 [물리 이벤트 v3](../project/physical-controller-events.md)입니다. 아래의 피크 기본·7종 샷·보드 경기context 설명은 이전 커밋의 기록입니다. 새 보드 기본은 물리6종이고 게임이 테니스 의미를 결정합니다.

DT-HW-31-21-00 / R01 / 2026-10-20. 제품은 **NU40-DK + 별도 부착 외장6축 IMU**이며 원래 12일·3명·36PD 계획을 유지합니다. NU54는 기존 센서 없는 BLE/버튼 시험 대상입니다. 이번 개선에서는 실물 IMU·추가 버튼 시험·flash를 하지 않았습니다. ATA iSpec 2200을 참고한 자체 문서 관리 형식이며 공식 적합성을 주장하지 않습니다.

## 참고 프로젝트에서 확인한 것

[Air Band 고정 소스](https://github.com/hex-aragon/air-band/tree/d89ce32a460b34c0cc740235dc9a76e74396a094)는 Arduino/Bluefruit에서 가속도를 주기적으로 읽고 피크와 세기를 판정해 BLE 이벤트를 보내는 구조입니다. [영상](https://www.youtube.com/watch?v=T8Lj7S-T7LY)에서 스틱 동작과 화면 타격 반응을 확인했으며 [제작자 설명](https://next-ai-agent.tistory.com/m/8)은 외장 센서로 입력과 화면을 연결한 개념 검증을 설명합니다. 분석 커밋의 `classifyHit()`은 고정0이며 TinyML 학습 모델은 없습니다.

라이선스가 없어 원본 소스·주석·자산을 복사하지 않았습니다. 피크 검출 원리를 참고하여 기존 Zephyr/C 펌웨어에 독립 구현했습니다. 자체 코드·문서는 Apache-2.0, 기존 외부 코드의 원래 조건은 유지합니다.

## 이번에 달라진 동작

| 단계 | 구현과 책임 |
| --- | --- |
| 취득 | 10ms 절대 deadline, 늦은 주기 건너뛰기. 최근20개 raw6축을 보관 |
| 보정 | 현재 연결의 실제 CALIBRATE 명령, 정지64샘플. 센서 실패·긴 공백은 보정 무효 |
| 스윙 | 자이로 회전 구간의 가속도 국소 피크를 다음 유효 샘플로 확인. 종류/상대각은 기존 자이로 분류 |
| 세기 | 중력 포함2.5..12g를1..100으로 변환. 실측 전 시작값이며 config로 조정 |
| 중복 방지 | 한 스윙 한 이벤트. gyro+accel 해제와 cooldown 후 재무장 |
| 송신 | 기존 v2 20바이트 SWING·비동기 큐. NUS8바이트 드럼 규격은 사용하지 않음 |
| PC/게임 | 기존 본딩·보정 ACK·중복 검사와 정규화 입력, 일반 타격/서브/스킬 게이트 유지 |

피크 확인 한 샘플은100Hz 목표에서 약10ms지만 필터·드라이버·BLE·Unity를 포함한 전체 지연은 실측해야 합니다. 상대 yaw/pitch를 위치·절대 heading으로 해석하지 않습니다. 특수샷/스킬의 명시 모드와 자동 제스처 인식도 구분합니다. 새로운 패킷 필드가 없어 protocol·SDK·game의 패키지 참조 변경은 필요하지 않습니다.

## 센서가 있는 담당자의 다음 작업

1. [인수 표](imu-handoff.md)를 작성합니다. 센서 모델·전압·주소·실제 헤더·장착 축을 확정합니다.
2. MPU6050 또는 LSM6DSO 예제를 **검토 후 선택**합니다. 기본 빌드는 센서 alias가 없어 모션 입력을 만들지 않습니다. LSM6DS3/DSL은 LSM6DSO로 선언하면 안 됩니다.
3. 현재 Zephyr DTS는 SDA=P0.22/SCL=P0.21입니다. Air Band Arduino의 SDA=P0.26/SCL=P0.27은 이 저장소의 SPI1과 겹치므로 배선을 그대로 옮기지 않습니다.
4. 선택한 overlay로 빌드합니다. `--trace`는 개발 UART에 bounded 원본 값을 기록하는 선택 사항이며 BLE raw 스트리밍이 아닙니다. 일반 빌드에서는 꺼져 있습니다.
5. 첫65개 이상 정지 샘플부터 UART 로그를 수집하고 CSV로 변환합니다. 부팅 세션은 나누고 누락 시각을 보간하지 않습니다.
6. 같은 C 판정 코드로 재생하고 실제 FH/BH/서브·정지·걷기·반동 데이터의 별도 평가 결과로 임계값을 조절합니다. 정밀도/재현율·누락/중복·오검출/분·지연 분포를 남깁니다.
7. Unity 무선 설정에서 본딩→보정→서브/스윙/스킬 테스트→저장→일반 경기 순서로 확인합니다. 설정 입력을 경기에 누출하거나 입력 게이트를 우회하지 않습니다.

펌웨어 root에서 실행하는 기록 재생 명령:

```sh
cmake -S . -B .work/host -DDT_PROTOCOL_ROOT=/absolute/path/digital-tennis-protocol
cmake --build .work/host
ctest --test-dir .work/host --output-on-failure
python3 tools/imu-trace-to-csv.py uart.log samples.csv
.work/host/imu_replay samples.csv > events.csv
```

[상세 코드·모델별 ODR/범위·빌드 명령](https://github.com/digital-tennis/digital-tennis-firmware/blob/46881a8e0610b9439d77785f06186e1f77e3535b/docs/air-band-imu-adaptation.md)에서 정확한 수정 위치를 확인합니다. 임계값은 펌웨어 config에 빌드 시 주입하며 runtime CSV/원격 설정을 제공하는 것은 아닙니다. 게임 CSV는 그 이후의 경기 효과를 설정합니다.

## 검증과 남은 한계

[검증 기록](../testing/imu-peak-validation.json)은 합성 센서값을 동일 C 코드에 재생한 결과, 실제 센서 드라이버를 포함한 보드 컴파일과 기존 Unity 수신 경로 회귀를 구분합니다. 실제 NU40 센서 장착·배선·인식률·전파 지연은 미검증입니다. 센서 없는 NU54 버튼 시험을 더 요청하지 않습니다.

## 후속: 테니스 동작별 가상 검증

[가상 IMU 실험실](imu-tennis-simulator.md)은 3D 라켓 궤적에서 만든 센서값을 실제 C 판정기로 재생합니다. 실험용7종 프로필과 실패/상황 모호함을 검토하며 기본 보드 앱의 빠른 피크 설정을 교체하지 않습니다. 경기 상황 BLE 전달과 실물 정확도·전체 지연은 후속 과제입니다.

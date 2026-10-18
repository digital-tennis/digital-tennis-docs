# Digital Tennis 개발 문서

Digital Tennis는 키보드와 BLE 모션 라켓으로 즐기는 Unity PC 테니스 프로젝트입니다. 이 문서는 게임·펌웨어·통신·AI·온라인 서비스가 어떻게 연결되는지, 무엇을 구현하고 어떻게 확인할지 안내합니다.

## 먼저 무엇을 보고 싶나요?

| 목적 | 읽는 순서 |
| --- | --- |
| 게임을 플레이하고 싶어요 | [게임 실행·조작 안내](https://github.com/digital-tennis/digital-tennis-game) |
| 시스템을 이해하고 싶어요 | [제품별 책임](project/repositories.md) → [아키텍처와 판정 위치](project/architecture.md) |
| 개발이 처음이에요 | [작업 방법](guides/contributing.md) → [용어](guides/glossary.md) → [제품별 과제](products/README.md) |
| 컨트롤러를 연결하고 싶어요 | [통신 계약](contracts/controller-protocol.md) → [현재 본딩 검수](project/controller-bonding.md) |
| 온라인 기능을 개발해요 | [온라인 계약](contracts/online-protocol.md) → [통합 수용 기준](testing/acceptance.md) |
| 문서를 수정·공개하고 싶어요 | [공개 문서 정책](project/open-source.md) → [GitBook 연결](guides/gitbook.md) |

## 제품 구조

**펌웨어**가 외장 IMU와 버튼을 읽어 물리 동작을 판정합니다. **프로토콜**은 전달할 필드·단위·버전을 정의하고, **BLE SDK**는 OS 연결·본딩·수신 검증을 맡습니다. **게임**은 정규화 입력을 받아 실제 타격·규칙·점수를 처리합니다. **AI**는 같은 입력 경계로 행동을 제안하며, **서버**는 두 플레이어의 방과 통신을 연결합니다.

전체 저장소와 담당 영역은 [제품별 저장소](project/repositories.md), 설계 선택의 이유는 [시스템 구조](project/architecture.md)에서 확인합니다.

## 하드웨어와 검증 범위

제품 타깃은 **NU40-DK + 별도로 부착하는 외장 IMU**입니다. 내장 센서를 전제하지 않으며 모델·전압·배선·장착 축은 실제 부품과 보드 리비전으로 확인합니다. NU-54는 센서 없는 BLE 연결 시험용이며 Mac 일반 Unity 창의 실제 본딩·테니스 왕복·보드 재시작 후 재연결을 확인했습니다.

키보드 게임, 모의 패킷, 보드 컴파일, 실제 BLE 본딩, 실물 IMU와 서로 다른 두 PC의 온라인 검수는 각각 다른 확인 항목입니다. 최근 본딩·배포 결과와 남은 실기는 [현재 검수](project/controller-bonding.md)에 기록합니다. 과거 시점의 완료 수치나 계획을 현재의 전체 성공으로 읽지 않습니다.

## 구현 과제와 원래 일정

[제품별 37개 과제](products/README.md)는 코딩 테스트 문제처럼 배경, 선행 조건, 입력·출력, 동작 규칙, 예외, 예제와 완료 기준을 제공합니다. 새로 참여한다면 담당 제품의 과제부터 읽고 관련 계약을 확인하세요.

초기 목표는 **12일·3명·36인일**이며 [WBS](planning/wbs.md)에 72개 반일 작업으로 보존합니다. 초기 목표와 당시 가정은 [프로젝트 범위](project/overview.md), 현재 변경·확장은 [구현 현황](project/implementation-status.md)과 개별 검수 기록에서 구분합니다.

## 문서 읽기 기준

- 규격의 필드·단위·절차는 해당 계약 문서를 따릅니다. 컨트롤러 바이트 형식의 정본은 [protocol 규격](https://github.com/digital-tennis/digital-tennis-protocol/blob/main/spec/controller-v2.md)입니다.
- 날짜·커밋을 명시한 검증 문서는 그 실행 시점의 근거입니다. 실제 성공, 모의 검사, 교차 빌드, 미검증을 구분합니다.
- 최초 계획·과제·이력은 보존합니다. 현재 실행 방법은 각 제품의 루트 README를 우선합니다.

전체 탐색은 [목차](SUMMARY.md)를 사용하세요.

## 후속 개발 인수

[외장 IMU를 가진 개발자의 수정·검증 순서](guides/imu-handoff.md)와 [강화학습 AI의 실제 학습/실행 범위](project/learned-ai.md)를 확인하세요.

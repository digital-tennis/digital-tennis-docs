# Digital Tennis Docs

현재 상태와 남은 작업은 [현재 작업 목록](docs/project/current-backlog.md)과 [최신 소프트웨어 검증·배포](docs/project/software-followup.md)에서 확인하세요.
**게임·컨트롤러·온라인 서비스를 함께 만드는 개발 문서.** 제품 구조부터 구현 과제, 인터페이스 계약과 검증 기준까지 한곳에서 찾을 수 있습니다.

[문서 시작](docs/README.md) · [시스템 구조](docs/project/architecture.md) · [제품별 과제](docs/products/README.md) · [전체 목차](docs/SUMMARY.md) · [물리 컨트롤러 v3](docs/project/physical-controller-events.md)

## Digital Tennis란?

키보드 또는 모션 라켓으로 타격 타이밍을 조작하는 Unity PC 테니스 프로젝트입니다. 15개 국가의 오리지널 선수, 난이도별 AI, 테니스 점수·세트 진행과 방 코드 기반 온라인 2인 대전을 개발합니다. 하드웨어 목표는 **NU40-DK + 별도로 부착하는 외장 IMU**입니다.

이 저장소는 제품 간 책임과 계약을 연결하는 **문서의 진입점**입니다. 실제 코드와 실행 방법은 각 제품 저장소에서 관리합니다.

## 목적에 따라 읽기

| 하고 싶은 일 | 시작할 문서 |
| --- | --- |
| 게임을 실행하고 플레이하기 | [게임 README](https://github.com/digital-tennis/digital-tennis-game) |
| 전체 데이터 흐름과 책임 이해하기 | [시스템 아키텍처](docs/project/architecture.md) |
| 처음 개발에 참여하기 | [작업 방법](docs/guides/contributing.md) → [제품별 과제](docs/products/README.md) |
| 펌웨어·PC 통신 구현하기 | [컨트롤러 계약](docs/contracts/controller-protocol.md) |
| 온라인 방·시그널링 구현하기 | [온라인 계약](docs/contracts/online-protocol.md) |
| 확인한 것과 남은 검증 구분하기 | [현재 본딩·배포 검수](docs/project/controller-bonding.md) · [통합 수용 기준](docs/testing/acceptance.md) |
| 초기 일정과 팀 분담 보기 | [12일·3인 WBS](docs/planning/wbs.md) |

## 제품별 저장소

| 저장소 | 담당 영역 |
| --- | --- |
| [digital-tennis-game](https://github.com/digital-tennis/digital-tennis-game) | Unity 게임·입력 어댑터·규칙·화면·음향 |
| [digital-tennis-firmware](https://github.com/digital-tennis/digital-tennis-firmware) | 외장 IMU·버튼·보정·물리 동작 판정·BLE 송신 |
| [digital-tennis-protocol](https://github.com/digital-tennis/digital-tennis-protocol) | GATT·패킷·단위·버전·공통 코덱 |
| [digital-tennis-ble-unity](https://github.com/digital-tennis/digital-tennis-ble-unity) | PC Bluetooth·OS 본딩·수신 검증·정규화 입력 |
| [digital-tennis-ai](https://github.com/digital-tennis/digital-tennis-ai) | 게임과 독립된 난이도별 이동·타격 정책 |
| [digital-tennis-match-server](https://github.com/digital-tennis/digital-tennis-match-server) | 방 코드·시그널링·릴레이·재접속 |
| **digital-tennis-docs** | 통합 설계·계약·과제·일정·검증 안내 |

## 문서의 구성

```text
docs/
  README.md       문서 첫 화면
  SUMMARY.md      GitBook 전체 탐색
  project/        목표·책임·구조·현황
  products/       제품별 초보자용 구현 과제
  contracts/      컨트롤러·온라인 인터페이스
  guides/         참여·GitBook·브랜드·제출 안내
  planning/       초기 WBS와 위험 관리
  testing/        수용 기준·벡터·검증 근거
```

**37개 구현 과제**는 상황, 선행 조건, 입력·출력, 동작 규칙, 예제, 예외와 완료 기준을 갖춥니다. 초기 계획은 **12일·3명·36인일**이며, 72개 반일 작업으로 보존합니다. 초기 계획과 현재 구현·실기 상태는 구분해 읽습니다.

통신·구조 문서는 문서 ID·개정·적용 범위·요구사항·절차·검증 근거를 사용합니다. ATA iSpec 2200의 문서 통제 방식을 참고한 자체 형식이며 공식 적합성 인증을 의미하지 않습니다. [문서·공개 정책](docs/project/open-source.md)

## 로컬에서 읽고 검사하기

**Git과 Python 3**만 있으면 됩니다. Markdown 파일을 GitHub나 편집기에서 바로 읽을 수 있습니다.

```sh
git clone https://github.com/digital-tennis/digital-tennis-docs.git
cd digital-tennis-docs
python3 tools/check-docs.py
python3 tools/check_docs.py
```

검사는 내부 링크·목차 누락·과제 구성·원래 WBS 공수·패킷 벡터·로고 규격을 확인합니다. 제품 동작이나 실물 연결의 성공을 판정하는 검사는 아닙니다.

## GitBook에서 사용하기

저장소 루트의 `.gitbook.yaml`은 `docs/`를 콘텐츠 루트로 지정합니다. 첫 페이지는 `docs/README.md`, 탐색은 `docs/SUMMARY.md`입니다. GitBook Git Sync에서 이 공개 저장소를 연결하고, 콘텐츠 경로에 맞는 설정을 사용하세요. 계정·Space 연결과 게시 절차는 [GitBook 연결 안내](docs/guides/gitbook.md)에 정리했습니다.

## 도움말·기여

[Digital Tennis](https://github.com/digital-tennis)가 관리합니다. 잘못된 설명이나 빠진 절차는 [Issues](https://github.com/digital-tennis/digital-tennis-docs/issues)에 해당 문서와 기대하는 설명을 남겨 주세요. [기여 안내](CONTRIBUTING.md)에 따라 관련 계약·과제·검증 근거를 함께 수정하고, 새 페이지는 목차에 등록합니다.

## 라이선스

직접 작성한 코드·문서는 [Apache-2.0](LICENSE)입니다. [NOTICE](NOTICE)를 포함하며, 외부 자료·자산의 원래 조건은 [외부 고지](THIRD_PARTY_NOTICES.md)를 따릅니다.

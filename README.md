# Digital Tennis 개발 문서

NU40-DK와 **별도 부착형 외장 IMU**를 라켓 컨트롤러로 사용하고, Unity PC 테니스 게임에서 1인 AI 플레이와 온라인 2인 플레이를 제공하는 프로젝트입니다. 개발 기간은 **12일**, 개발자는 **3명**, 총 공수는 **36인일**입니다.

게임 main은 실제 P2P·릴레이 복구, 네이티브 BLE SDK와 입력 설정, 일반 Mac 창 키보드·마우스 검증을 포함합니다. 이번 후속 PR은 펌웨어 송신·버튼·모션과 센서 없는 BLE 통신 확인을 보완합니다. 외장 IMU 정확도와 Windows·두 PC 실기는 별도입니다. [현재 구현과 검증 범위](docs/project/implementation-status.md)를 먼저 확인하세요.

- [컨트롤러 후속 검수·최신 배포판](docs/project/controller-readiness.md)
- [처음 읽는 문서](docs/README.md)
- [제품과 저장소 책임](docs/project/repositories.md)
- [12일 일정과 72개 반일 작업 슬롯](docs/planning/wbs.md)
- [제품별 상세 개발 과제](docs/products/README.md)
- [GitBook 무료 플랜 연결](docs/guides/gitbook.md)
- [컨트롤러 통신 규격](docs/contracts/controller-protocol.md)
- [온라인 통신 규격](docs/contracts/online-protocol.md)

GitBook에서는 하나의 Space에 `docs/`를 연결합니다. 저장소 루트의 `.gitbook.yaml`은 루트에서 연결하는 방식, `docs/.gitbook.yaml`은 `docs/`를 Space 디렉터리로 매핑하는 방식을 지원합니다. 문서 내용과 목차는 `docs/README.md`, `docs/SUMMARY.md`에 있습니다.

로고는 [500×500 업로드 파일](docs/assets/digital-tennis-github-avatar-500.png)과 [원본](docs/assets/digital-tennis-logo-original.png)으로 제공됩니다.

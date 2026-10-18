# Digital Tennis · 개발 문서와 통합 규격

전체 제품의 책임·초보자 과제·12일 WBS·계약·검수 근거를 GitBook에 연결 가능한 문서로 관리한다.

전체 제품은 NU40-DK에 **별도 외장 IMU**를 부착하는 라켓 컨트롤러와 Unity PC 테니스 게임으로 구성한다. 최초 계획은 **12일·3명**이다.

## 주요 기능

- 7개 제품의 상황/입력/출력/예외/완료 기준
- 컨트롤러·온라인 계약과 실제 검증/미검증 구분
- GitBook 구조·로컬 링크·원래 일정 자동 검사

## 빠른 시작

Python3. GitBook 계정 게시/권한은 저장소 검사와 별도다.

```sh
python3 tools/check-docs.py
python3 tools/check_docs.py
```

## 책임과 현재 범위

원래12일·3인·36인일,37개 과제와72개 반일 슬롯을 보존한다. 루트 .gitbook.yaml은 docs/를 가리키며 docs/.gitbook.yaml은 Space를 docs/에 매핑할 때 쓴다. 실제 게시·실물 검증을 문서 검사 성공으로 대신하지 않는다.

## 구조와 문서

`docs/project/`: 현황/아키텍처 · `docs/products/`: 과제 · `docs/contracts/`: 계약 · `docs/planning/`: WBS · `docs/testing/`: 근거

[처음 읽기](docs/README.md), [목차](docs/SUMMARY.md), [GitBook 연결](docs/guides/gitbook.md), [컨트롤러 검수](docs/project/controller-readiness.md)

## 도움말과 기여

재현 가능한 문제는 [이슈](https://github.com/digital-tennis/digital-tennis-docs/issues)로 남긴다. 관리 주체는 [Digital Tennis](https://github.com/digital-tennis)이며 [기여 안내](CONTRIBUTING.md)를 따른다. 검증 커밋을 고정하고 실제 장치 성공·모의 검사·교차 빌드를 구분한다.

## 라이선스

프로젝트 자체 코드·문서는 **[Apache-2.0](LICENSE)**이다. [NOTICE](NOTICE)와 [외부 코드·자산 고지](THIRD_PARTY_NOTICES.md)를 함께 확인한다. 외부 자산에 Apache-2.0을 덮어쓰지 않는다.

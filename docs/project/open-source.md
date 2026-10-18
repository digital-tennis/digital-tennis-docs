# DT-DM-00-20-00 · 공개 문서와 라이선스

문서 개정 R01, 2026-10-19, PR 검토본. 최초12일·3명·36인일과 NU40-DK+별도 외장 IMU 조건을 유지한다.

## 00 적용 범위

사용자 결정에 따라 7개 제품의 직접 작성한 코드·문서는 Apache-2.0을 적용한다. 각 루트에 LICENSE(원문), NOTICE, THIRD_PARTY_NOTICES.md, CONTRIBUTING.md를 둔다. 다른 저작권자의 코드·폰트·모델·음원에 프로젝트 라이선스를 덮어쓰지 않는다. [Apache 원문](https://www.apache.org/licenses/LICENSE-2.0.txt).

| 제품 | README가 안내하는 시작점 | 고유 책임 |
| --- | --- | --- |
| firmware | 호스트 검사·보드 빌드·GPIO/센서 조건 | 모션 취득·보정·판정·GATT |
| protocol | C/C# 교차 검사·관리된 ICD | wire/단위/버전/벡터 |
| ble-unity | SDK 검사·native 빌드 | OS 연결·보안·수신 검증 |
| game | 실제 게임 캡처3개·Unity 시작·키·CSV | 입력 adapter·테니스·표현 |
| ai | 순수 패키지 검사·난이도 | 공통 경계를 통과하는 입력 의도 |
| match-server | npm 시작·실소켓 검사·운영 예제 | 방/역할·시그널링·릴레이 |
| docs | GitBook 설정·과제/WBS·링크 검사 | 계약·작업·근거 추적 |

README는 프로젝트가 하는 일·주요 기능·전제 환경/시작 방법·책임/제약·구조/상세 문서·도움말/관리 주체·기여·라이선스 순서로 구성한다. 구현/실기 상태는 상세 검수 문서로 연결한다. [GitHub README 안내](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes).

## 10 외부 원문 보존

NU40/NU54 보드 정의는 원래 MIT와 고정 출처를 유지한다. game의 Quaternius·Kenney는 취득한 pack의 CC0 고지, Nanum은 SIL OFL, flag-icons는 MIT, Natural Earth는 원래 공개 조건, Flite는 원래 COPYING을 보존한다. Unity/WebRTC·Windows .NET은 공급자 고지와 라이선스를 유지한다. 실제 세부 파일과 취득/변환 근거는 각 저장소 THIRD_PARTY_NOTICES.md가 기준이다.

native helper와 game 빌드 도구는 Apache LICENSE/NOTICE, 사용한 Digital Tennis 패키지의 고지, 외부 자산·WebRTC/.NET 고지를 결과물 Licenses에 복사한다. 배포 포장은 빠진 필수 고지가 있으면 실패한다. 루트 라이선스를 추가했다는 이유로 외부 자산을 새 라이선스로 표시하지 않는다.

## 20 변경·배포 추적

문서/코드·소비 패키지는 검토한 Git SHA를 고정한다. PR 스쿼시 병합 후 소비 SHA를 병합 커밋으로 다시 갱신하고 빌드/검수를 반복한다. sourceCommit·dirty 상태·Development/AllowDebugging·체크섬을 배포 명세에 기록한다. clean 소스 없는 release 포장은 거부한다.

키·PIN·OS 본딩 데이터·실물 기기 식별자·이전 앱 코드 백업은 공개 저장소에 넣지 않는다. 코드 섹터 백업은 로컬 비공개 폴더에만 보관한다. 실물 성공/모의 라디오/교차 빌드/미검증을 분리한다.

## 30 규격 문서 형식

컨트롤러 DT-ICD-23-10-00, 온라인 DT-ICD-23-20-00과 아키텍처 DT-SDD-00-10-00은 문서 ID·개정·적용성·유효 절·요구/절차·검증 근거를 사용한다. ATA iSpec2200에서 영감을 받은 자체 형식이며 항공기 ATA 챕터·유료 원문/SGML DTD·공식 적합성 인증을 포함하지 않는다. [ATA 공식 범위](https://ataebiz.org/standards/).

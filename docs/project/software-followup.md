# DT-VAL-00-00-01 · 소프트웨어 후속 완료 기록

R01 / 2026-10-20. 제품은 **NU40-DK + 별도 외장 IMU**다. NU54는 센서 없는 임시 BLE/버튼 시험 타깃이다. 최초 12일·3명·36PD 계획을 보존한다. 이번 기록은 실물 센서 성공이나 공식 ATA iSpec2200 적합성 선언이 아니다.

## 10 완료한 작업과 검토 PR

| 저장소 | 변경과 완료 기준 | PR |
| --- | --- | --- |
| firmware | 과거 v2 샷 모드 설명을 현재 v3 물리 6종·번호별 Down/Up·전체 구간 종료 분류와 게임 판정 책임으로 현행화 | [PR #8](https://github.com/digital-tennis/digital-tennis-firmware/pull/8) |
| game | 센서 입력에 15명 CSV 모션 스킬 연결, 실제 IMU와 버튼 바인딩 구분, 중복/시간/메뉴/단절 격리, 실제 경기 평가와 비개발 배포물 | [PR #29](https://github.com/digital-tennis/digital-tennis-game/pull/29) |
| ai | 실제 Unity 경기 보고서의 점수·시도·서비스·액션 합 검증과 CSV/JSON 집계, 실제 실행 결과 | [초안 PR #6](https://github.com/digital-tennis/digital-tennis-ai/pull/6) |
| docs | 현재 작업의 시작점, 과거 기록과 현재 계약 분리, 검증·배포·외부 유예 목록 연결 | 이 문서 PR |

기능은 PR 검토 중이다. 최신 main 배포물과 개선 후보 배포물을 구분하며, 사용자 승인 없이 새 기능을 main에 반영하지 않았다. AI PR은 도구/문서/증거 변경으로 Runtime과 모델을 바꾸지 않으므로 게임의 AI 패키지는 기존 병합된 `b00d33a`를 유지한다. protocol `2bb3f0e`, SDK `a0e705e`도 병합된 커밋에 고정돼 있다. 서버 wire는 바꾸지 않았다.

## 20 모션 스킬을 수정하는 방법

보드와 SDK는 캐릭터·스킬을 알지 않는다. 게임의 `SensorPlayerInputSource → GestureSkillInputSource → PlayerInputRouter/Adapter`가 로컬 선수의 패턴을 선택한다. 게임의 `Balance/gestures.csv`는 15명의 서로 다른 패턴과 최대 간격·총시간·cooldown을 정의한다.

- 한국: `HorizontalNegative | ObliqueUp | HorizontalPositive`.
- 일본: `OverheadDown | ObliqueUp | ShortRotation`.
- 사용하는 토큰은 v3의 물리 6종이다. 장치가 보내지 않는 Hold/Push 등을 추정하지 않는다.
- 부분 동작은 일반 타격 후보로 전달하고, 완성하는 마지막 입력만 기존 Skill 요청으로 바꾼다. 버튼4/K는 유지한다.
- 버튼2/3이 중립 타격으로 바인딩되어도 실제 IMU 출처 표시가 없으므로 패턴에 섞이지 않는다.
- 메뉴·설정·타이핑·정지·득점 후·선수/소스 변경·단절에서는 부분 패턴을 지운다. 재고/공/점수는 입력원이 수정하지 않는다.

정상 앱의 `Application.persistentDataPath/Balance/gestures.csv`를 원자적으로 교체한 뒤, 효과가 끝난 서브 대기의 F5 또는 앱 재시작으로 반영한다. 잘못된 재로드는 직전 값을 유지한다. 검증은 `-dt-gestures-file /absolute/isolated.csv`로 사용자 파일과 분리한다. 펌웨어의 물리 분류 CSV는 빌드 입력이고 게임 패턴 CSV는 실행 설정이다. 실제 손동작의 간격·인식률·편의성은 [실물 IMU 인수](../guides/imu-handoff.md)에서 후속 담당자가 측정한다.

## 30 Unity와 AI 검증

| 검사 | 실제 결과 |
| --- | --- |
| Unity EditMode | 207개 통과 |
| Unity PlayMode | 46개 통과. 기본 실행에서 제외한 아래 두 검사는 별도로 수행 |
| GPU 포인터 | 1개 통과 |
| 전용 실제 AI 경기 | 3난이도 × 3시드 = 9사례, 사례마다 두 서비스 게임, 총106포인트 |
| AI 독립 C# | 28개 통과 |
| AI 보고서 집계 | 정상 집계와 부분/중복/불일치/미동작/대진·해시 오류 거부 통과 |

v3 패킷→실제 SDK→설정 보정/테스트/저장→센서 입력→한국 패턴→일반 Skill에서 재고 소비와 재전송 중복 방지를 확인했다. 해당 패킷 검사의 재고는 명시적인 사전조건이고, 별도 랠리 검사는 실제 공격으로 획득한 재고를 소비한다. 두 증거를 혼동하지 않는다.

| 난이도 | 포인트 | AI 득점 | 고정 입력 상대 점유율 | 실제 AI 리턴 | 타격 거부 |
| --- | --- | --- | --- | --- | --- |
| 하 | 40 | 13 | 32.5% | 31 | 0 |
| 중 | 41 | 29 | 70.7% | 72 | 0 |
| 상 | 25 | 24 | 96.0% | 54 | 0 |

학습 판단과 액션 집계는 각각157회다. KOR/JPN 고정 대진의 가상 사람 입력 결과이며 사람 승률이 아니다. 이 코호트는 짧은 좌/우 코너3/5만 선택했다. 다른 대진·전체6행동·장기전술 일반화를 입증하지 않는다. 이 수치에 맞춰 CSV 계수나 모델 가중치를 임의 조절하지 않았다.

최초9사례 묶음은7사례 후 Unity 기본180초 제한에서 중단됐다. 전용 제한1200초와 사례별 중간 저장을 추가한 재실행에서9사례가 모두 통과했다. 각 서비스 게임의100초 제한과 점수/타격 검사는 유지했다. 실제 Unity 프레임 시각 때문에 시드가 같아도 포인트 수의 비트 단위 일치는 보장하지 않는다.

런타임 구현은 `e4d5e7807437641f6ec603db9cadb67c53df8061`, 보완한 평가 코드는 `0393f1d396ca5278414b87c056056714672c3ed7`이다. 이후 문서 커밋은 게임 코드/CSV/패키지를 바꾸지 않는다. 모델·CSV·XML·원시 결과 해시는 [기계 판독 검증](../testing/software-followup-validation.json)에 있다. 원시9사례와 집계는 AI 저장소의 `Models/match-scenes.json`, `Models/match-evaluation.json`에 공개했다.

## 40 배포물과 일반 Mac 창

| 구분 | 실제 빌드 소스 | 생성물 |
| --- | --- | --- |
| 최신 main | `b28a668e4b7c86ff5d0709c44311ef68a0d983b4` | Mac/Windows 비개발 ZIP·JSON·SHA256 |
| 개선 후보 | `fa6736e25506a4bd1800605e313217e3b4a7c930` | Mac/Windows 비개발 ZIP·JSON·SHA256 |

각 빌드는 깨끗한 커밋에서 수행했고 Development/AllowDebugging=false, 네이티브 helper·런타임/자산 고지·ZIP·체크섬을 검증했다. Mac은 ad-hoc 서명 검증을 통과했으며 Developer ID 공증은 별도다. Windows는 교차 빌드이며 실제 PC 검수가 필요하다. 파일은 이번 작업의 로컬 `outputs/software-followup/releases/{main,candidate}/`에 보관하며 Git에 대용량 ZIP을 넣지 않는다. 기록 JSON의 파일명·SHA256으로 식별한다.

두 버전을 각각 일반 Mac 창에서 실행하고 실제 네이티브 키보드로 시작·선수/상대/코트 선택·서브2회·AI리턴2회·2포인트·다음서브를 확인했다. 최신 main에서는 일시정지·키보드 상세·미연결 무선 상세도 열었다. 키보드에는 연결 기능이 없고 무선은 찾기→연결→통신/동작 테스트→저장 순서이며, 미연결 저장은 차단됐다. 설정 변경을 저장하거나 보드를 추가 조작하지 않았다. 기록한 런타임 예외는0이다.

[실제 화면과 게임별 검증 문서](https://github.com/digital-tennis/digital-tennis-game/blob/7d3212bbbe24f29037c1d8064e2b6271ebf4f09b/docs/software-followup.md)에서 일반 창 이미지를 확인할 수 있다. 화면은 게임 자체의 캡처이고 OS 화면이나 연출용 가짜 점수가 아니다.

## 50 남은 외부 작업과 확장

[현재 작업 목록](current-backlog.md)의 외부 조건을 유지한다. NU40+외장IMU 배선·장착·사람 데이터/지연, 실제 Windows, 서로 다른PC/WAN, 공용WSS 호스팅·도메인, GitBook 계정 게시, 음악/음성 채택과 사람 플레이 밸런스가 남아 있다. NU54 버튼 반복 시험은 요구하지 않는다.

전체 경기 학습 환경·자기대전·이동/서브/스킬 학습과 학습 재개는 후속 AI 확장이다. 경기 중 BGM 음소거와 득점 함성1회·다음서브 정지 정책, Apache-2.0 및 외부 자산의 원래 고지를 유지한다.

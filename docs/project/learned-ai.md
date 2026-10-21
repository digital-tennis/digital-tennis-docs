# 강화학습 AI 연결과 현재 범위

2026-10-19 기준. [AI PR #5](https://github.com/digital-tennis/digital-tennis-ai/pull/5)는 Stable-Baselines3 PPO로 실제 학습한 actor와 독립 C# 추론을 추가합니다. [학습·교체 가이드](https://github.com/digital-tennis/digital-tennis-ai/blob/d2e1f004041cd35773fc423c5be65b071d7e9cd8/Training/README.md)에서 재현 절차와 소스 계약을 확인합니다.

## 게임을 제어하는 경로

관측12개→PPO actor→6개 코스/깊이 후보→AiPolicy의 이동/접촉 실행→TennisAiOpponent→일반 RacketInput/SubmitInput입니다. 기존 반응 지연·위치 오차·확률과 CSV 샷 계수를 유지합니다. 모델이 공/점수/스킬 재고를 직접 바꾸지 않습니다. 게임에는 Python 서버·API키가 필요하지 않습니다.

학습 대상은 샷 배치입니다. 자동 이동·서브 시작·타격 타이밍과 스킬 시점은 기존 정책이며 전체 경기를 end-to-end로 학습한 모델은 아닙니다. Unity ML-Agents는 후속으로 전체 경기 환경을 구축할 때 선택할 수 있습니다.

## 학습 근거와 한계

65,536단계 학습 후 분리한2,048상황의 배치 보상은0.568433, 무작위는0.214257입니다. 이 값은 실제 경기 승률이 아닙니다.64개 별도 관측에서 SB3와 C# 액션 일치를 검사했고, AI 라이브러리28검사를 통과했습니다. 실제 Unity 결과는 게임 검수 기록에 따로 기재합니다.

환경은 탄도·정적 네트/경계와 상대 이동 거리로 배치를 평가하는1단계 MDP입니다. 네트 두께·전체 회복·장기 전술·상대의 실제 정책을 완전히 재현하지 않습니다. 모델은 네 코너 배치를 주로 선택하며 중앙 액션이 선택되지 않은 평가 결과도 보존합니다. 과적합/실전 성능은 추가 경기 데이터로 판단해야 합니다.

## 실행 중 멈춘 것처럼 보일 때

- 상대 HUD의 **학습 AI / 내 서브를 기다리는 중**이면 사람 차례의 서브 대기입니다.
- **서브 준비 중**이면 상대 서브가 지연 후 시작돼야 합니다.
- 무선 기기가 끊겨 일시정지됐거나 메뉴가 열린 상태에서는 AI도 멈추는 것이 정상입니다.
- 모델이 잘못됐으면 번들 학습 모델 또는 표시된 기본 AI로 대체합니다. 모델 오류를 숨기고 무기한 대기하지 않습니다.

교체 모델은 게임의 persistentDataPath/AI/placement-ppo.json에 완성된 파일을 원자적으로 저장한 뒤 다음 경기를 시작하면 적용합니다. 학습 가중치 변경에 게임 재빌드는 필요하지 않습니다. actor 형상/스키마/크기/유한값을 검사하고, 모델과CSV/환경 해시를 기록합니다.

## Unity 재검수 결과

독립 AI28검사, Unity Edit191개·AI 장면4개를 통과했습니다. 세 난이도 모두 이동/모델 판단/반환 타격과 서비스 교대·코트 교대 후2게임 진행을 확인했습니다. pause와온라인에서 AI 입력이 진행되지 않는 것도 검사했습니다. 장면 자동 검수는 사람 쪽 입력 fixture를 사용했습니다.

별도로 깨끗한 Mac 빌드bd8037a의 일반 창에서 실제 키보드 서브3회 뒤 모델 판단3회·AI 반환3회를 확인했습니다. 이 일반 창에는 가상 사람 source·물리/점수/재고 주입을 사용하지 않았습니다. 추가 보드 버튼이나 IMU 시험은 하지 않았고 게임은 키보드 설정으로 일시정지해 두었습니다.

[게임 화면·빌드 소스·해시 기록](https://github.com/digital-tennis/digital-tennis-game/blob/b4c4bb5a82d7a94c23152597ac58a944861c4dfa/docs/learned-ai.md) · [기계 판독 결과](../testing/learned-ai-validation.json)

최종 HUD 가독성 보완 소스5098f4ad3796도 일반 창에서 키보드 서브·모델 판단1회·반환1회와 상태 패널을 확인했습니다. 기능 검수의bd8037a 소스/3회 결과는 보존하며, 최종 UI 검수는 별도 해시로 추적합니다.

## main 병합과 소비 참조

2026-10-19에 AI → game 순서로 스쿼시 병합했으며 firmware의 IMU 인수 가이드도 병합했다. 게임 manifest와 Unity 생성 잠금 파일은 아래 AI main 커밋을 참조한다. 기존 일반 창·장면 검수 소스/모델 해시는 당시 증거로 보존한다.

| 저장소 | PR | main 병합 커밋 |
| --- | --- | --- |
| digital-tennis-ai | [#5](https://github.com/digital-tennis/digital-tennis-ai/pull/5) | [b00d33aa500c](https://github.com/digital-tennis/digital-tennis-ai/commit/b00d33aa500cc9ae4f94994f8ea0f530f9ec43ba) |
| digital-tennis-firmware | [#4](https://github.com/digital-tennis/digital-tennis-firmware/pull/4) | [97efb9a45fc7](https://github.com/digital-tennis/digital-tennis-firmware/commit/97efb9a45fc70040fb20041255321ca6c0f77652) |
| digital-tennis-game | [#27](https://github.com/digital-tennis/digital-tennis-game/pull/27) | [9c4767a5c7f6](https://github.com/digital-tennis/digital-tennis-game/commit/9c4767a5c7f69d2df7302bd9c2f948d84cc664ff) |

새 소비 참조로 AI main28검사와 Unity 프로젝트 검사·Edit191검사를 다시 통과했다. AI Runtime과 번들 actor는 기존 실기 검수 소스와 동일하다. 이번 병합 작업에서 IMU나 추가 보드 버튼 검증을 수행하지 않았다.

2026-10-21 확장의 현재 상태는 [전체 경기 AI 결과·계약·남은 검수](ai-full-match.md)를 확인하세요. 실제 self-play/재개를 실행했으며 새 모델의 Mac 일반 창 검수는 미완료입니다.

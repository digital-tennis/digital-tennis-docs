# 전체 경기 AI·학습 브리지 계약

2026-10-21 / 관측 v2, action v1, reward v1. [실제 결과와 제한](../project/ai-full-match.md)을 함께 읽는다.

- 관측32개와 6개 코스/깊이 행동은 AI `Runtime/FullMatchActor.cs`의 Fields/Normalize와 `Training/full_match.py`가 정본이다. shape/version/finite/크기 검사를 통과해야 한다. 고정 clip normalization이며 running statistics는 없다.
- game `FullMatchObservation`이 안정적인 Near/Far identity를 실제 end에서 canonical 좌표로 변환한다. 외부 AI에 UnityEngine/transport/game 의존성을 추가하지 않는다.
- 일반 서브·타격·스킬 gate, 실제 재고·reach·duplicate/stale input·pause/online/비권한 격리는 game 책임이다. 학습자가 ball/score/stock을 바꾸지 않는다.
- 실제 best-of-3 매치 Winner만 done이다. 중간 reset을 거절하며 Python은 점수/물리를 근사하지 않는다. 브리지는 테스트 opt-in loopback 전용이고 정상 C# inference와 분리한다.
- CSV는 PPO/보상/학습량/seed·상대 snapshot 주기를 검증한다. 보상은 실제 본인−상대 points/games/sets/match와 거절 변화다. 업데이트·finish-only·partial match를 구분한다.
- self-play 상대의 bytes/hash를 경기 내내 동결하고 선수별 RNG와 schedule을 분리한다. held-out seed/대진에서 update0·평가 전후 weights 동일을 검증한다.
- complete checkpoint에는 optimizer/RNG/counter/관측/normalization/환경 lease·상대 풀/schedule·설정/코드 hash를 보존한다. immutable generation 후 원자 pointer, deserialize 전 검증이다. 같은 살아 있는 Unity world만 재개하며 Unity 종료 복원은 실패한다.
- 잘못된 교체 actor는 검증된 번들, 번들도 잘못되면 명시된 기본 AI로 대체한다. 온라인 상대에 AI를 실행하지 않는다.

훈련 명령과 고정 Python 의존성은 AI `Training/README.md`, Unity 실행/원시 감사는 game `docs/ai-full-match-results.md`와 `tools/verify-ai-delivery.py`를 참조한다. 자체 Apache-2.0와 기존 외부 라이선스, NU40-DK+별도 외장 IMU, 원래12일·3명 계획을 유지한다.

새 모델의 Mac 일반 창 검수는 시스템 잠금으로 미완료이며 GPU batch와 구분한다.

# 장비 없이 진행하는 소프트웨어 확장

2026-10-18. 실물 장비가 필요한 작업은 유예하고 소프트웨어 구현·실행 가능한 검증을 진행한다. **NU40-DK+별도 부착 외장 IMU, 최초12일·3명·36인일 계획**은 원안으로 유지한다. 원안은37개 제품 과제를72개 반일 슬롯에 배정한 계획이며 실제 소요 시간이나 완료 상태를 소급해서 덮어쓰지 않는다.

## 구현 제품과 의존 관계

| 제품 | 이번 구현 | 병합 PR |
|---|---|---|
| protocol | C99/C# 코덱·공통 벡터·호환 v2 | [PR1](https://github.com/digital-tennis/digital-tennis-protocol/pull/1) |
| firmware | 참고 보드·외장 IMU 포트·보정/필터/모션·BLE Peripheral 구조·호스트/보드 대상 컴파일 | [PR1](https://github.com/digital-tennis/digital-tennis-firmware/pull/1) |
| ble-unity | Mac CoreBluetooth/Windows GATT·SDK·보정ACK·취소/재연결·입력 검증 | [PR1](https://github.com/digital-tennis/digital-tennis-ble-unity/pull/1) |
| match-server | epoch 시그널·직접 채널 준비/실패 협의·WSS 배포 구성·부하 검사 | [PR5](https://github.com/digital-tennis/digital-tennis-match-server/pull/5) |
| game | 실제 패킷 SDK·보정/테스트/저장·직접 DataChannel·품질/배포 회귀 | [PR23](https://github.com/digital-tennis/digital-tennis-game/pull/23) |
| docs | 현재 상태·재현·증거·계정/실물/사람 선택의 구분 | 이 문서 PR |

후속 병합 요청에 따라 protocol→firmware→BLE SDK→server→game 순서로 스쿼시 병합했다. 펌웨어와 SDK의 프로토콜 참조, 게임의 manifest/lock을 아래 main 커밋으로 갱신하고 검증했다. AI 패키지는 기존 병합된 main 커밋을 유지한다. 서버의 새 제어 메시지는 이 게임 버전과 함께 적용한다. 문서 PR은 제품 병합 결과를 기록한 뒤 마지막으로 병합한다.

| 제품 | 스쿼시 병합된 main 커밋 |
|---|---|
| digital-tennis-protocol | [`5163cd3073be696c0f8da9ab21f2d85f7e160575`](https://github.com/digital-tennis/digital-tennis-protocol/commit/5163cd3073be696c0f8da9ab21f2d85f7e160575) |
| digital-tennis-firmware | [`d720fca8f699d951fe68b8c413865ee233989fa6`](https://github.com/digital-tennis/digital-tennis-firmware/commit/d720fca8f699d951fe68b8c413865ee233989fa6) |
| digital-tennis-ble-unity | [`a4885be6e65b8aba6bfe20cdd2b0e241653aae84`](https://github.com/digital-tennis/digital-tennis-ble-unity/commit/a4885be6e65b8aba6bfe20cdd2b0e241653aae84) |
| digital-tennis-match-server | [`305fb82dd65de5cd109255a7d3a862b1e79225ba`](https://github.com/digital-tennis/digital-tennis-match-server/commit/305fb82dd65de5cd109255a7d3a862b1e79225ba) |
| digital-tennis-game | [`9fec849c9bb29f6df6180e8bd71a549d8ac5e7e7`](https://github.com/digital-tennis/digital-tennis-game/commit/9fec849c9bb29f6df6180e8bd71a549d8ac5e7e7) |

새 참조로 펌웨어 프로토콜 실제 다운로드·호스트 sanitizer 검사, SDK31개 검사(표준 인접 저장소 경로 포함), 서버 main28개 검사, Unity 프로젝트·패킷 컨트롤러 PlayMode·소스 검사를 통과했다. 원격 병합 브랜치와 로컬 main/브랜치를 정리한다. 아래 전체 경기·품질·배포 수치와 체크섬은 원래 검증한 커밋의 기록이며 새 main 빌드의 증거와 구분한다.

## NU40-DK 구조와 센서 경계

참고: [chcbaram/nu40dk-kit](https://github.com/chcbaram/nu40dk-kit), 확인 커밋`df4367ed03d35c8599dc6007f049b2f4df9812b3`. 앱/하드웨어 드라이버/보드 정의를 분리하는 방식을 참고하고 보드 정의의 MIT 고지를 보존했다. Xbox 예제는Central로 다른 컨트롤러를 수신한다. 테니스 라켓은Peripheral/GATT Server로 PC에 데이터를 보낸다.

외장 센서는 확인한 overlay의`external-imu`alias와 Zephyr 센서 드라이버 포트로 지정한다. 모델·전압·주소·헤더 핀·장착 행렬이 미확정이면 그대로 미확정으로 남긴다. 내장 IMU 대체나 임의 핀맵을 넣지 않는다. 센서 부재/실패 시 ready/calibrated=false이고 정상 스윙을 만들지 않는다. 호스트 가짜 센서로 소프트웨어 상태를 검증한다. 설치된 NCS3.4.1/Zephyr4.4.2에서 외장 alias가 없는 기본 구성과 컴파일 전용 합성 센서 fixture 구성 모두 보드 대상 ELF/HEX를 생성했다. 이는 실제 부팅·flash·전파·센서 정확도 성공을 의미하지 않는다. 테스트 모델/주소는 실제 제품 선택이 아니며 fixture를 플래시하지 않는다.

## 컨트롤러 계약

20바이트 v1의 FH1/BH2/서브3을 보존하며 v2에서만 스매시4/발리5/슬라이스6/로브7/스킬8을 추가한다. CRC·길이·범위·순번 순환·중복 이벤트·연결 세대를 검사한다. 각도·세기는 정규화된 입력이고 플레이어 권한/Near·Far는 보드가 결정하지 않는다. v2 의도 지원은 실물8제스처 인식 성공을 의미하지 않는다.

무선 연결과 센서 보정, 동작 테스트, 저장은 독립 단계다. 현재 연결의 보정 성공ACK와 서브/스윙/스킬 테스트가 필요하다. 재보정·끊김·기기 변경은 테스트를 무효화한다. 저장만 실제 설정과 입력 소스를 바꾸고 취소는 기존 값을 유지한다. 키보드 상세에는 무선 연결 기능을 넣지 않는다.

## 검증 상태의 의미

| 구분 | 완료 증거 |
|---|---|
| 코덱 | 같은 벡터를 C/C#으로 해석하고 값·오류·왕복 바이트 일치 |
| 펌웨어 호스트 | 외장 IMU 포트·보정·타임아웃·중복·모션 상태 테스트 |
| BLE 소프트웨어 | SDK 검사·네이티브 컴파일·게임 패킷 E2E |
| 실제 BLE/IMU | 실물 센서·전파·OS 동의·인식률 기록이 있어야 완료 |
| 직접 P2P | 실제 DataChannel 게임 송수신과 서버 게임 중계0을 함께 확인 |
| 릴레이 전환 | 실제 채널 실패/제한 시간 뒤 양측 합의·새 epoch·동일 점수 |
| Windows | 교차 빌드와 실제 Windows 실행을 별도 표기 |
| 시각/음향 | 실제 게임 캡처·파형 검사와 사람의 채택을 별도 표기 |

기존15명·15코트·CSV·AI·정식 단식 규칙·최대3스킬·반대편 시점·호스트 권위를 유지한다. 경기/서브/랠리/스킬 BGM은0이고 득점 함성은1회·다음 서브 정지다. 메뉴/인트로/결과곡 A/B는 **사람의 최종 선택 미정**이다.

## 유예 목록

- 실제 외장 IMU 모델/배선·장착 축과 보드 리비전 확인, 실제 부팅/flash·전파·OS 페어링·인식 정확도
- 실물Windows·서로 다른 두PC/WAN·실물 두 컨트롤러
- 사람 플레이 기반 밸런스·음성/음악 채택과 추가 아트 방향 승인
- 공용 도메인/호스팅·GitBook 계정 연결과 실제 게시 확인
- 팀 코드 라이선스 선택(제3자 MIT/CC0/도구 고지는 별도 보존)

유예 항목을 모의 입력·자동 검사·교차 빌드로 완료 처리하지 않는다. 새 버전별 수치·실제 실행·PR과 배포 파일은 최종 검증 후 이 문서에 연결한다.

## 새 개발자의 실행 순서

1. protocol에서 `python3 tools/check.py`를 실행한다. C 컴파일러·CMake·.NET10 SDK가 필요하다. 오류/정상/호환 벡터를 먼저 통과시킨다.
2. firmware는 README의 호스트 CMake 경로로 가짜 센서·BLE sink 검사를 실행한다. 실제 보드 빌드와 구분한다. `src/common`의 포트, `src/ap`의 보정/모션, `src/driver`의 센서, `boards`의 하드웨어를 순서대로 읽는다.
3. ble-unity에서 `dotnet run --project tests/Checks.csproj -c Release`를 실행한다. `IBleTransport`는 전파, `BleControllerClient`는 연결/보정/입력 규칙, game의 `NativeControllerBackend`는 게임 변환이다. 한 계층에 서로의 책임을 합치지 않는다.
4. 서버에서 `npm ci`, `npm run check`, `npm test`를 실행한다. Docker/Caddy 배포 절차는 서버의 `docs/deployment.md`를 따른다. 계정이 없으면 로컬 검증까지만 기록한다.
5. game은 Unity6000.3.26f1로 `bash tools/unity.sh check`, `test-edit`, `test-play`, `build-verification-mac`을 순서대로 실행한다. 같은 프로젝트의 Editor를 먼저 닫는다. Mac native helper에는 Xcode Command Line Tools, Windows helper 교차 빌드에는 .NET10 SDK가 필요하다.
6. game의 `docs/software-integration.md`와 도구의 `--help`를 따라 패킷·실제 온라인 두 프로세스·품질을 검증한다. 검사 CSV/오디오는 `.work/`의 복사본으로 격리한다. 일반 사용자 파일을 테스트로 덮어쓰지 않는다.
7. 배포는 커밋이 깨끗한 상태에서 `release-mac`/`release-windows` 후 `tools/package-release.py`로 진행한다. 개발/디버깅 옵션, helper·런타임 고지, plist·앱 서명·ZIP·SHA256·소스 커밋을 확인한다.

## 무료 자산과 라이선스 추적

| 항목 | 보존하는 근거 | 범위 |
|---|---|---|
| NU40-DK 참고 보드 | 참고 커밋·MIT 원문·출처 | firmware의 third-party 고지, 자체 코드 전체를 자동 MIT로 선언하지 않음 |
| Quaternius 전신·헤어·이동 | CC0 원본·취득/변환 해시 | game의 기존 캐릭터 출처·비교 자료 |
| Kenney 타격·이동 음원 | CC0 두 팩 원문·factory provenance | 기존 이동/타격 변형을 유지 |
| Flite 음성·폰트·국기/지도 | 각 도구/폰트 고지·flag-icons MIT·Natural Earth Public Domain | 국가별 억양/성우 녹음이라고 주장하지 않음 |
| Unity WebRTC | 패키지 LICENSE·Third Party Notices | desktop 배포의 ControllerNative/Licenses |
| Windows .NET runtime | 실제 restore/download한 런타임 팩 LICENSE/NOTICE·버전 목록 | self-contained helper 배포에 동봉 |

청음 페이지는 현재 `audio.csv`의160개 cue를 사용하며, 기본/대체 cue가 같은 파일이면 그 사실을 명시한다. 자동 재생하지 않고 한 음원을 재생할 때 다른 음원은 멈춘다. 게임의 실제 혼합 녹음과 파일 원음 청음을 구별한다.

## 보드 대상 컴파일 결과

실물을 사용하지 않고 NCS3.4.1(LTS)/Zephyr4.4.2, 설치된 GNU14.3.0/Zephyr SDK1.0.1로 두 구성을 컴파일·링크했다. 기본 구성은 Flash175,696B/RAM33,932B, 합성 외장 드라이버 구성은 Flash179,796B/RAM33,996B다. 보드 스키마의 full_name, BLE 광고 API·데이터 수명과 공통 라이브러리 ARM 플래그 문제를 보완했다. 구독 상태는 atomic으로 공유한다. 모든 플래시/장치 탐색 명령은 실행하지 않았다. 재현은 firmware의 `tools/build-board.py`와 `docs/board-build-validation.json`을 따른다.

## 최종 통합 결과

- Unity Edit189/189·Play43/43, 프로젝트/소스 검사 통과.
- 명시적 MOCK 전파+실제20바이트 코덱/SDK/설정/게임adapter:14장 캡처,1포인트·양쪽 타격·다음 서브·끊김 후 일시정지, 오류0.
- 실제 P2P 전체86포인트:2–0세트(7–6/6–0), 서버 게임 중계0. 양측 실제 직접 송수신 확인.
- 별도 장애 경기: 실제 P2P 채널 차단→relay2→WebSocket 재접속relay3→동일 전체 경기→같은 방 양측 재경기1회·첫 포인트[1,0]. 런타임/프로토콜/종료 후 예외0.
- 15인·15코트30시점,6종 타격74접촉,15인×AI3난이도45사례 모두 실제 다음 서브. 고정 조건12150사례/48600포인트는 타임아웃0·재현성 통과이며 사람 승률이 아니다. 이번에 기존 CSV 밸런스를 임의로 바꾸지 않았다.
- Mac 배포 실행 파일의 인트로·득점·다음 서브 및 경기 BGM0·함성 정책을 별도 재검사했다. Mac 일반 창 실행은 확인했지만 UI 도구가 screenshot timeout/elementHasNoFrame을 반환해 실제 키보드·마우스 조작은 미검증이다. 잠금 우회나 물리 입력 성공을 주장하지 않는다.
- Mac·Windows 비개발 패키지는 clean 소스, Development/AllowDebugging=false, helper/라이선스·ZIP CRC·SHA256을 검사한다. Mac은 로컬adhoc서명이고 Windows는 교차 빌드다.

[기계가 읽을 수 있는 수치·소스 커밋·체크섬](../testing/software-validation.json)에 실제 결과를 보존한다. 원본 PNG/WAV·실행 로그·배포ZIP은 Git에 넣지 않고 이번 작업의 로컬 전달 폴더에 둔다. 초기 검토 뒤 후속 요청에 따라 위 제품 PR들을 스쿼시 병합했다. 실물 장비/두PC·계정 게시·음악/음성/밸런스 채택 항목을 소프트웨어 검사로 완료 처리하지 않는다.

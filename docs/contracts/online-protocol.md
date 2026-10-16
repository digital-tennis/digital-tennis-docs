# 온라인 통신 규격 v1

> 초기 설계/과제와 현재 완료 상태는 다릅니다. [2026-10-16 구현 현황](../project/implementation-status.md)을 먼저 확인하세요. 직접 P2P·실물 BLE·Windows 실기는 별도 증거가 필요합니다.

BLE 컨트롤러 패킷은 PC 내부에서 RacketInput으로 변환합니다. PC 사이와 서버에는 다음 JSON 메시지를 사용합니다. 이 초기 계약은 C/B가 구현하고 A가 검토합니다.

## 공통 봉투

```json
{"v":1,"type":"room.create","requestId":"r1","payload":{}}
```

`v`는 1, `type`은 정의된 문자열, 요청의 `requestId`는 1~64자입니다. 응답에는 같은 requestId를 넣습니다. 서버 알림은 requestId가 null입니다. 전체 UTF-8 메시지는 최대 16KiB이며, 유한한 숫자만 허용합니다. 오류 응답은 `type:error`, payload의 `code`·`message`를 제공합니다. 부적절한 메시지 때문에 다른 연결까지 종료하지 않습니다.

## 방 코드와 생명주기

코드는 `ABCDEFGHJKLMNPQRSTUVWXYZ23456789`의 32문자에서 암호학적 난수로 선택한 6자리입니다. 입력은 공백 제거·대문자화 후 검사합니다. 활성 방과 충돌하면 최대 10번 다시 뽑고 실패하면 CODE_EXHAUSTED를 반환합니다. 방 인원은 호스트·게스트 2명입니다. 대기 방은 생성 10분 뒤 만료하고, 경기 중 방은 대기 TTL로 삭제하지 않습니다.

```text
WAITING → READY → CONNECTING → PLAYING → FINISHED → CLOSED
                         ↘ 연결 실패 → RELAY 합의 → PLAYING
PLAYING → PAUSED → 15초 내 재접속 → PLAYING
                 ↘ 만료 → CLOSED
```

서버는 최초 참가에 playerId(`host`/`guest`)와 예측 불가능한 reconnectToken을 제공합니다. 토큰은 URL·일반 로그·저장소에 남기지 않습니다. 5초마다 heartbeat를 보내고 15초 동안 응답이 없으면 끊김으로 판단합니다. 토큰에 의한 재접속 유예는 끊김 판정 시점부터 15초입니다. 호스트가 돌아오지 않으면 경기는 무효 종료하며 호스트 이전은 구현하지 않습니다.

## 서버 요청과 응답

| 요청 type | payload | 정상 응답/알림 | 주요 오류 |
| --- | --- | --- | --- |
| room.create | {} | room.created: code, playerId, reconnectToken, state | ALREADY_IN_ROOM, CODE_EXHAUSTED |
| room.join | code | room.joined; 두 참가자에게 room.ready | INVALID_CODE, ROOM_NOT_FOUND, ROOM_FULL |
| room.leave | {} | room.left; 상대에게 peer.left | NOT_IN_ROOM |
| session.resume | code, reconnectToken | session.resumed; 상태 스냅샷 재동기화 | INVALID_TOKEN, RESUME_EXPIRED |
| peer.signal | kind=offer/answer/ice, data | 같은 방 상대에게 peer.signal | NOT_IN_ROOM, INVALID_SIGNAL |
| transport.propose | mode=p2p/relay, epoch | 상대에게 동일 제안 | NOT_HOST, INVALID_EPOCH |
| transport.ack | mode, epoch | 호스트에게 ack | INVALID_EPOCH |
| transport.commit | mode, epoch | 양쪽에 transport.committed | NOT_HOST, PEER_NOT_ACKED |
| game.relay | epoch, message | 상대에게 relay.message | NOT_IN_ROOM, INVALID_ROLE, INVALID_EPOCH |
| heartbeat | clientTimeMs | heartbeat.ack | INVALID_PAYLOAD |

방 membership은 서버가 현재 소켓에 연결하여 관리합니다. payload에 다른 방의 code나 playerId를 넣어 권한을 얻을 수 없습니다. offer는 호스트, answer는 게스트만 보냅니다. ICE는 양쪽이 보낼 수 있습니다. signal 데이터는 SDP 문자열 또는 선택한 P2P 후보의 직렬화 가능한 연결 객체로 제한하고 길이를 검사합니다. 이 형식은 D3 후보 확정 후 구체화합니다.

한 소켓당 메시지는 초기값 초당 60개, burst 120개로 제한하고 create/join은 30초당 5회로 제한합니다. 초과는 RATE_LIMITED입니다. 이 값은 30Hz 스냅샷·입력 통합 실험 후 조정할 수 있습니다. 서버 메모리에 방을 보관하며 서버 재시작 후 방 복구는 범위 밖입니다.

## PC 간 게임 메시지

```json
{"v":1,"type":"input","epoch":1,"inputSeq":42,"playerId":"guest","payload":{"eventId":7,"kind":"forehand","power01":0.8,"aimX":-0.2,"aimZ":0.1}}
```

```json
{"v":1,"type":"snapshot","epoch":1,"tick":120,"payload":{"ball":{"pos":[0,1.2,3],"vel":[0,-2,8]},"players":[{"id":"host","pos":[0,0,-9]},{"id":"guest","pos":[0,0,9]}],"points":[2,1],"phase":"RALLY","serverId":"host","serveSide":"left","faultCount":0,"lastHitter":"host","bounceCount":0,"rallyId":4,"lastProcessedInputSeq":42}}
```

고정 물리 tick은 60Hz, 상태 송신은 30Hz의 초기값입니다. points는 표시 문자열이 아닌 누적 포인트 정수입니다. `lastProcessedInputSeq`는 호스트가 처리한 게스트 입력 순번입니다. `result` 메시지는 matchId와 결과·승자를, `pause`는 reason을 포함합니다. 점수·공·result는 호스트만 발행합니다. 서버 릴레이에서도 발신 소켓 역할을 검사합니다. 게스트는 스냅샷 tick이 감소하면 무시합니다.

inputSeq와 tick은 uint32이며 wrap 비교는 `delta=(new-old) mod 2^32`, `0<delta<2^31`입니다. 동일 inputSeq는 한 번만 처리합니다. 입력은 받는 호스트의 현재 타격 구간에서만 검증하고, 게스트의 MCU 시각을 호스트 tick과 직접 비교하지 않습니다. MVP는 rollback이나 완전한 부정행위 방지를 구현하지 않습니다.

## P2P와 릴레이 선택

1. room.ready 이후 호스트가 offer, 게스트가 answer, 양쪽이 ICE 정보를 서버로 교환합니다.
2. 두 PC의 DataChannel 준비가 8초 안에 끝나면 호스트가 mode=p2p, epoch=1을 제안합니다.
3. 실패하면 호스트가 mode=relay로 제안합니다. 게스트 ack 후 host commit이 양쪽에 도착해야 경기 입력을 시작합니다.
4. mode 또는 연결 변경 시 경기 일시정지, epoch 증가, 마지막 호스트 스냅샷 적용, 양쪽 확인 후 재개합니다. 오래된 epoch 메시지는 버립니다.
5. P2P 중에도 WebSocket은 방·heartbeat·전환 제어용으로 유지합니다.

P2P 초기 어댑터는 reliable ordered DataChannel 하나를 사용합니다. 경기 메시지의 바이트·역할·중복 검사는 릴레이와 동일합니다. 제한된 네트워크에서 TURN을 선택하더라도 해당 경로는 `turn-relay`로 기록하여 직접 P2P와 구별합니다.

## 직접 연결을 입증할 증거

두 Windows 실행 파일의 연결 상태, 선택된 ICE 후보 종류, 메시지 송수신 카운터를 기록합니다. direct P2P는 선택 경로에 relay 후보가 없음을 확인합니다. IP·토큰은 공개 로그에서 지웁니다. 릴레이를 강제로 선택한 테스트에는 mode=relay 표시와 서버 중계 카운터를 남깁니다. [연결 정보와 시그널링의 공식 설명](https://webrtc.org/getting-started/peer-connections)

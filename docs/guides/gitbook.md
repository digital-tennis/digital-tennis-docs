# GitBook 무료 플랜 연결

GitBook Free는 확인 시점에 Git Sync와 편집자 1명을 제공합니다. 세 명이 무료로 협업하려면 GitHub 브랜치·PR로 문서를 수정하고, 한 명이 GitBook 연결과 공개 사이트를 관리합니다. 팀원이 GitBook 웹 편집자로 모두 참여하는 기능은 이 무료 구성의 전제가 아닙니다. [현재 가격과 기능](https://www.gitbook.com/pricing)

## 연결할 값

| 항목 | 값 |
| --- | --- |
| GitHub 조직 | digital-tennis |
| 저장소 | digital-tennis-docs |
| 브랜치 | main |
| 문서 디렉터리 | docs/ |
| 첫 페이지 | docs/README.md |
| 목차 | docs/SUMMARY.md |
| 최초 동기화 방향 | GitHub → GitBook |
| Space 수 | 1 |

## 연결 단계

1. GitBook 계정에서 무료 플랜으로 문서 사이트와 한 개 Space를 준비합니다.
2. 해당 콘텐츠의 Git Sync 설정을 열고 GitHub를 선택합니다.
3. GitBook GitHub 앱에 `digital-tennis-docs` 저장소 접근을 승인합니다. 조직 승인 단계가 표시되면 조직 소유자가 승인합니다.
4. `digital-tennis/digital-tennis-docs`와 `main`을 선택합니다.
5. Space와 디렉터리를 매핑하는 화면에서는 `./docs`를 선택합니다. 이때 `docs/.gitbook.yaml`이 적용됩니다. 저장소 전체를 한 Space로 연결하는 화면에서는 루트의 `.gitbook.yaml`이 `root: ./docs/`로 같은 콘텐츠를 가리킵니다.
6. 첫 연결은 **GitHub → GitBook**으로 가져옵니다. 기존 GitHub 문서가 기준이므로 빈 GitBook 문서로 저장소를 덮어쓰지 않습니다.
7. 첫 페이지, 7개 제품 과제, 이미지와 목차가 보이는지 확인합니다.
8. GitHub에서 문장 하나를 수정해 PR을 병합하고 GitBook 반영을 확인합니다. 반대로 GitBook 편집을 사용할 경우 동기화 커밋 후 최신 내용을 pull합니다.

최근 GitBook은 사이트 매핑 파일 `gitbook-docs.yaml`을 생성할 수 있습니다. 연결 과정에서 생성한 Space의 `key`는 유지합니다. 하나의 Space로 운영하므로 여러 Space·유료 섹션·사용자 지정 도메인·유료 테마가 필요하지 않습니다. 파일 역할은 [공식 설정 문서](https://gitbook.com/docs/docs-as-code/git-sync/content-configuration.md)를 참고합니다.

## 연결이 안 될 때

저장소가 목록에 없으면 GitBook 앱의 조직·저장소 접근을 확인합니다. 목차가 비면 실제 매핑 디렉터리와 `.gitbook.yaml` 기준 상대 경로를 확인합니다. 중복 페이지가 생기면 SUMMARY에서 같은 Markdown 파일이 두 번 등장하는지 확인합니다. GitBook의 계정 연결·사이트 공개는 실제 GitBook 계정에서 수행해야 하며 저장소 생성만으로 자동 연결되지 않습니다.

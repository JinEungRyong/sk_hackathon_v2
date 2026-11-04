# git 명령어

원칙: 세션마다 **자기 경로만** 커밋한다. **커밋하지 않은 파일은 제출에서 빠질 수 있다.** `git push`는 하지 않는다.
`git add -A`, `git add .`, `git commit -a`는 쓰지 않는다. 다른 세션이 작업 중인 파일이 섞인다.
터미널 붙여넣기는 Ctrl+Shift+V.

## 시작할 때 (하네스 복사)
과제 저장소 최상위에서 실행한다. clone은 반드시 저장소 **밖**(`/tmp`)에 한다. 저장소 안에 clone하면 git 안에 git이 생겨 커밋이 꼬인다.
```
git clone https://github.com/JinEungRyong/sk_hackathon.git /tmp/hk
[ -e AGENTS.md ] && echo "AGENTS.md 이미 있음: 직접 합치기" || cp /tmp/hk/AGENTS.md .
mkdir -p work_wiki/human && cp -r /tmp/hk/harness/. work_wiki/human/
mkdir -p ~/.agents/skills && cp -r /tmp/hk/harness/skill/* ~/.agents/skills/   # web-page-templates, ux-ui-audit-hackathon
git add AGENTS.md work_wiki/human && git commit -m "add: 하네스 구축"
```
- 과제 저장소에 AGENTS.md가 이미 있으면 덮어쓰지 않고 메시지만 나온다. 그때는 내용을 직접 합친다
- 스킬은 Codex를 다시 시작해야 보인다 (09_add_skill.md)
- 커밋이 "Please tell me who you are"로 실패하면:
  ```
  git config user.name "이름" && git config user.email "you@example.com"
  ```

## 세션별 커밋 (경로를 `--` 뒤에도 적는다)
`--` 뒤에 적은 경로만 커밋된다. 다른 세션이 add만 해 둔 파일은 그대로 남는다.
| 세션 | 명령 |
|---|---|
| 인터뷰 | `git add work_wiki/interview_log.md work_wiki/facts.md work_wiki/assumptions.md work_wiki/questions.md work_wiki/screen_briefs.md work_wiki/sessions/interview.md && git commit -m "[interview] 손실 질문 결과" -- work_wiki/interview_log.md work_wiki/facts.md work_wiki/assumptions.md work_wiki/questions.md work_wiki/screen_briefs.md work_wiki/sessions/interview.md` |
| 계획 | `git add PLAN.md work_plan work_src/run .gitignore work_wiki/sessions/plan.md && git commit -m "[plan] 데이터 살펴보기와 샘플 추출" -- PLAN.md work_plan work_src/run .gitignore work_wiki/sessions/plan.md` |
| 구현 | `git add work_src/clean work_wiki/sessions/clean.md && git commit -m "[clean] 휴무 코드 정리와 테스트" -- work_src/clean work_wiki/sessions/clean.md` |
| 검증 | `git add work_wiki/sessions/verify.md && git commit -m "[verify] clean 지적 3건" -- work_wiki/sessions/verify.md` (통합 검증 때는 `work_wiki/scenarios.md`도 함께) |
| UX 검증 | `git add work_wiki/ux_audit.md work_wiki/sessions/ux.md && git commit -m "[ux] 시나리오 6개, Issue 5건" -- work_wiki/ux_audit.md work_wiki/sessions/ux.md` |
- 아직 없는 파일(예: 처음엔 assumptions.md가 없음)은 명령에서 뺀다. 없는 경로가 있으면 add가 실패한다
- `index.lock` 오류: 다른 세션이 커밋 중. 몇 초 뒤 다시
- 커밋은 Codex 세션이 하게 시키면 된다 (AGENTS.md에 같은 규칙이 있음)
- 세션은 기록 파일(`work_wiki/sessions/<세션>.md`)의 '커밋' 블록에 실행할 `git add`·`git commit` 명령을 먼저 적고 그대로 실행한다. 기록 파일도 같은 커밋에 들어간다
- 세션이 무엇을 커밋했는지 보기: `grep -A4 "커밋:" work_wiki/sessions/clean.md`
- `커밋: 대기`가 남아 있으면 그 세션에 "대기 중인 커밋 처리해"라고 시킨다

## 매번 쓰는 것
| 상황 | 명령 |
|---|---|
| 지금 무엇이 바뀌었나 | `git status` |
| 바뀐 내용 보기 | `git diff` (파일 이름만: `git diff --stat`) |
| 지금까지의 기록 | `git log --oneline` |
| 한 세션의 커밋만 | `git log --oneline --grep "\[clean\]"` |
| 특정 커밋 내용 | `git show <커밋번호>` (파일 이름만: `git show --stat <커밋번호>`) |

## 커밋 메시지 규칙
- `[세션 이름] 무엇을 했나`: `[interview]`, `[plan]`, `[<부분>]`, `[verify]`
- 진행상황 정리 세션은 커밋하지 않는다. progress.md, progress_summary.md는 `.git/info/exclude`에 들어가 `git status`에도 나오지 않는다
- 검증 반영: `[clean] verify 지적 1 반영`
- 준비: `chore: …`

## 검증 세션 뒤 확인
```
git status            # verify.md(통합 검증 때는 scenarios.md도)만 바뀌었는지
git diff --stat       # 다른 파일이 바뀌었으면 원인 확인
```
검증 세션이 다른 파일을 고쳤다면 그 변경을 되돌린다 (그 파일을 다른 세션이 작업 중이 아닌지 먼저 확인):
```
git restore <파일>
```

## 실수했을 때
| 상황 | 명령 | 주의 |
|---|---|---|
| 커밋 전 특정 파일 변경을 버리고 싶다 | `git restore <파일>` | 버린 내용은 되돌릴 수 없음 |
| add 했는데 빼고 싶다 | `git restore --staged <파일>` | 파일 내용은 그대로 |
| 방금 커밋 메시지를 고치고 싶다 | `git commit --amend -m "새 메시지"` | 바로 직전 커밋만. 병렬 작업 중에는 다른 세션이 그사이 커밋했을 수 있으니 `git log -1`로 내 커밋인지 확인 |
| 지난 커밋을 취소하고 싶다 | `git revert <커밋번호>` | 기록을 지우지 않고 '취소 커밋'을 새로 만듦 |
| 다른 세션 파일이 내 커밋에 섞였다 | `git revert` 하지 말고 그대로 두고 기록에 적는다 | 되돌리면 다른 세션 작업이 사라질 수 있음 |
- `git reset --hard`, 강제 덮어쓰기 계열은 쓰지 않는다. 다른 세션의 작업과 이력이 사라진다.

## 제출 직전
```
git status                    # "nothing to commit" 이어야 함 (work_out/은 .gitignore)
git ls-files | head -50       # 제출될(추적 중인) 파일 목록
git log --oneline | head -30  # 세션별 작업 흐름이 보이는지
```
- 결과물 파일이 `git ls-files`에 없으면 해당 세션에서 add 후 커밋
- 남은 변경이 여러 세션 것이면 세션마다 자기 경로로 나눠 커밋 (계획 세션이 마지막에 정리해도 됨)
- 올리면 안 되는 파일(키, 대용량 임시 파일)은 `.gitignore`에 추가 후 `git rm --cached <파일>`

## 후속 서술형 대비
- `git log --oneline`에서 세션 이름별로 무엇을 어떤 순서로 했는지 훑어 둔다

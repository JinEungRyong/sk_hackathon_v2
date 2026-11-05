Codex에 설치하는 방법

압축을 풀어 web-page-templates 폴더를 다음 위치 중 하나에 넣습니다.
나만 쓸 때: ~/.agents/skills/
특정 저장소에서 팀과 함께 쓸 때: 그 저장소의 .agents/skills/
Codex를 다시 시작합니다.
$web-page-templates로 직접 부르거나, "쇼핑몰 홈 화면 만들어 줘"처럼 요청합니다. 두 번째 방식은 스킬 설명과 맞는 요청이면 Codex가 스킬을 자동으로 고릅니다.


UX 검증 세션이다. ux-ui-audit-hackathon 스킬로 검수해. 시험용 계정은 SOLUTION.md에 있어.


1. Codex가 직접 알려주도록 설정하기 (가장 간단한 방법)

~/.codex/config.toml에 TUI 알림을 켜 두면, 세션이 작업을 마치거나 승인을 기다릴 때 터미널 알림이 옵니다.

toml


[tui]
notifications = ["agent-turn-complete", "approval-requested"]
notification_method = "osc9"   # iTerm2, VS Code 터미널 등에서 사용

chmod +x codex-status.sh
./codex-status.sh              # 한 번만 출력합니다
watch -n 2 ./codex-status.sh   # 2초마다 갱신합니다



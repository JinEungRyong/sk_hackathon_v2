# F. 내비게이션·선택 상태 (Navigation & Selected State)

탭, 필터, 메뉴, Segmented Control처럼 "지금 어디에 있는지 / 무엇이 선택됐는지"를 알려주는 UI는 **색상만으로 선택 상태를 구분하지 않는다.**

## 선택형 UI
- Segmented Control / Tab: 선택 항목에 배경, 밑줄, 굵기 중 색 외 단서가 하나 이상 있는가?
- Filter Chip: 선택 시 체크 아이콘이나 채워진 배경처럼 형태 변화가 있는가?
- 코드에 선택 상태가 반영되어 있는가? (`aria-selected`, `aria-pressed`, `aria-checked`, `aria-current="page"`)
- 클래스명만 `.active`이고 aria 속성이 없으면 스크린리더는 선택 상태를 알 수 없다.

## 사용자 선호 우선
선택 상태 표현 방식(배경, 밑줄, 굵기, 아이콘 등)은 팀/사용자가 정한 방식이 있으면 그것을 따른다. 정한 방식이 생기면 이 파일에 기록해 다음 검수부터 같은 기준을 쓴다.

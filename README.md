# 🎯 나만의 퀴즈 게임

## 목차
1. [프로젝트 개요](#프로젝트-개요) · [퀴즈 주제 선정 이유](#퀴즈-주제-선정-이유) · [개발 환경](#개발-환경) · [실행 방법](#실행-방법)
2. [기능 목록](#기능-목록) · [실행 증거 (텍스트 로그)](#실행-증거-텍스트-로그) · [실행 화면](#실행-화면)
3. [설계: 클래스를 나눈 이유](#설계-클래스를-나눈-이유) · [파일 구조](#파일-구조) · [데이터 파일 설명](#데이터-파일-설명-statejson)
4. [백업 및 복구 정책](#백업-및-복구-정책) · [대량 데이터 확장성 분석](#대량-데이터-확장성-분석-1000개-이상) · [요구사항 변경 시 수정 가이드](#요구사항-변경-시-수정-가이드)
5. [Git 작업 규칙](#git-작업-규칙) · [Git 실습 기록](#git-실습-기록)

## 프로젝트 개요
터미널에서 실행하는 **파이썬 기초 개념 퀴즈 게임**입니다.
메뉴에서 번호를 선택해 퀴즈 풀기, 퀴즈 추가, 퀴즈 목록 보기, 점수 확인, 퀴즈 삭제를 할 수 있으며,
추가한 퀴즈와 최고 점수, 게임 기록은 `state.json` 파일에 저장되어 프로그램을 다시 실행해도 유지됩니다.

- 언어: Python 3.10 이상 (표준 라이브러리 `json`, `os`, `shutil`, `random`, `datetime`만 사용)
- 구조: `Quiz`(퀴즈 한 문제), `QuizGame`(게임 전체 관리) 2개의 클래스로 역할 분리
- 보너스 과제 5개(랜덤 출제, 문제 수 선택, 힌트, 퀴즈 삭제, 점수 기록 히스토리) 구현
- 저장 파일 자동 백업(`state.json.bak`)과 손상 시 자동 복구

## 퀴즈 주제 선정 이유
2주차 시험에 대비하기 위해 파이썬 기본 개념 문제로 퀴즈를 구성했습니다.
변수, 자료형, 조건문, 반복문, 함수, 클래스, 파일 입출력(JSON), 예외 처리 등
입학 연수에서 배운 핵심 개념을 퀴즈로 반복해서 풀어 보며 복습할 수 있도록 했습니다.

## 개발 환경
| 항목 | 내용 |
|---|---|
| OS | Windows + WSL (Ubuntu) |
| 에디터 | Visual Studio Code (Python 확장) |
| Python | 3.14.4 |
| Git | 2.53.0 |

```
hyejin@localhost:~/codyssey/quiz-game$ python3 --version
Python 3.14.4
hyejin@localhost:~/codyssey/quiz-game$ git --version
git version 2.53.0
hyejin@localhost:~/codyssey/quiz-game$ git config user.name
haegirl23-max
```

![개발 환경 설정 화면](docs/screenshots/dev_env.png)

## 실행 방법
```bash
# 1. 저장소 복제
git clone https://github.com/haegirl23-max/quiz-test.git
cd quiz-test

# 2. 실행 (Python 3.10 이상)
python3 main.py
```

## 기능 목록
| 메뉴 | 기능 | 설명 |
|---|---|---|
| 1 | 퀴즈 풀기 | 풀 문제 수를 고르면 퀴즈를 **무작위 순서**로 출제하고, 정답/오답과 최종 점수(100점 만점)를 보여줍니다. 최고 점수를 넘으면 갱신하고, 게임 기록을 저장합니다. |
| 2 | 퀴즈 추가 | 문제, 선택지 4개, 정답 번호, 힌트(선택)를 입력받아 새 퀴즈를 등록합니다. |
| 3 | 퀴즈 목록 | 등록된 퀴즈의 문제 목록을 번호와 함께 보여줍니다. |
| 4 | 점수 확인 | 최고 점수와 최근 게임 기록(최대 5개, 최신순)을 보여줍니다. |
| 5 | 퀴즈 삭제 | 번호를 골라 퀴즈를 삭제하고 파일에 반영합니다. (0: 취소, 삭제 전 y/n 확인) |
| 6 | 종료 | 데이터를 저장하고 프로그램을 종료합니다. |

### 보너스 과제 구현 내용
| 보너스 과제 | 구현 방법 |
|---|---|
| 1. 랜덤 출제 | `random.sample()`로 퀴즈 목록에서 겹치지 않게 무작위로 뽑아 출제 순서를 섞습니다. |
| 2. 문제 수 선택 | 퀴즈 풀기 시작 시 `1 ~ 등록된 퀴즈 수` 범위에서 풀 문제 수를 입력받습니다. |
| 3. 힌트 기능 | `Quiz` 클래스에 `hint` 속성을 추가했습니다. 정답 입력에서 `0`을 누르면 힌트를 보여주며, 힌트를 본 뒤 맞히면 **0.5문제**로만 인정해 점수가 차감됩니다. |
| 4. 퀴즈 삭제 | 메뉴 5번에서 번호로 퀴즈를 골라 확인 후 삭제하고, 즉시 `state.json`에 저장합니다. |
| 5. 점수 기록 히스토리 | 게임을 마칠 때마다 날짜/시간, 푼 문제 수, 맞힌 수, 힌트 사용 수, 점수를 기록해 `state.json`에 저장합니다. |

**점수 계산**: `점수 = (힌트 없이 맞힌 문제 × 1 + 힌트 보고 맞힌 문제 × 0.5) ÷ 푼 문제 수 × 100` (소수점 버림)

### 입력 및 예외 처리
- 입력값 앞뒤 공백 제거 (예: `"  1  "` → `"1"`)
- 숫자가 아닌 입력(예: `abc`), 범위 밖 숫자(예: `9`), 빈 입력 → 안내 메시지 후 다시 입력
- `Ctrl+C` / 입력 종료(EOF) → 비정상 종료 없이 데이터를 저장하고 종료
- 퀴즈가 없을 때 풀기·목록·삭제 선택, 퀴즈를 풀기 전 점수 확인 → 안내 메시지 출력
- 힌트가 없는 문제에서 `0` 입력 → "이 문제에는 힌트가 없습니다" 안내
- 저장 파일이 손상되면 백업으로 자동 복구, 백업도 없으면 기본 퀴즈로 초기화

## 실행 증거 (텍스트 로그)
아래는 실제 터미널 실행 결과를 그대로 옮긴 것입니다. 같은 장면의 캡처는 [실행 화면](#실행-화면)에 있습니다.

### 1) 퀴즈 풀기: 문제 수 선택 → 랜덤 출제 → 힌트 → 채점 → 최고 점수 갱신
```
hyejin@localhost:~/codyssey/quiz-game$ /usr/bin/python3 /home/hyejin/codyssey/quiz-game/main.py
📂 저장된 데이터를 불러왔습니다. (퀴즈 8개, 최고점수 기록 없음)
========================================
        🎯 나만의 퀴즈 게임 🎯
========================================
1. 퀴즈 풀기
2. 퀴즈 추가
3. 퀴즈 목록
4. 점수 확인
5. 퀴즈 삭제
6. 종료
========================================
원하는 메뉴 번호를 입력하세요 (1~6): 1
몇 문제를 풀까요? (1~8): 3
🎮 퀴즈를 시작합니다! 총 3문제
💡 정답 입력에서 0을 누르면 힌트를 볼 수 있어요. (힌트 후 정답은 0.5문제로 인정)
----------------------------------------
문제 1.
 ❓퀴즈 데이터를 JSON 파일에 저장하는 가장 큰 이유는?

  1. 프로그램 실행 속도를 높이려고
  2. 코드의 문법 오류를 찾으려고
  3. 화면에 색을 입히려고
  4. 프로그램을 종료해도 데이터를 유지하려고

정답 번호를 입력하세요 (1~4, 힌트: 0): 0
💡 힌트: '데이터 영속성'이라는 말을 떠올려 보세요.
정답 번호를 입력하세요 (1~4, 힌트: 0): 4
✅ 정답입니다! (힌트 사용으로 0.5문제 인정)

----------------------------------------
문제 2.
 ❓'종료'를 선택할 때까지 메뉴를 계속 반복하려면 가장 알맞은 것은?

  1. for i in range(5):
  2. if True:
  3. def menu():
  4. while True: 와 break

정답 번호를 입력하세요 (1~4, 힌트: 0): 4
✅ 정답입니다!

----------------------------------------
문제 3.
 ❓__init__ 메서드는 언제 실행될까?

  1. 프로그램이 끝날 때
  2. print()를 호출할 때
  3. 클래스로 객체를 만들 때 자동으로
  4. 직접 이름을 불러야만 실행된다

정답 번호를 입력하세요 (1~4, 힌트: 0): 1
❌ 오답입니다. 정답은 3번입니다.

========================================
🏆 결과: 3문제 중 2문제 정답! (50점)
💡 힌트 사용: 1회
========================================
🎉 새로운 최고 점수입니다!
```
점수 확인: (0.5 + 1 + 0) ÷ 3 × 100 = 50점

### 2) 잘못된 입력 처리 (필수 기능 단계 실행 기록)
```
정답 입력: abc
⚠️잘못된 입력입니다. 1~4 사이의 숫자를 입력해주세요.
정답 입력: 7
⚠️잘못된 입력입니다. 1~4 사이의 숫자를 입력해주세요.
정답 입력:
⚠️입력값이 없습니다. 다시 입력해주세요.
정답 입력: 2
❌ 오답입니다. 정답은 1번입니다.
```

## 실행 화면
> 메뉴·퀴즈 풀기·추가·목록·점수 화면은 필수 기능 구현 단계에서 캡처한 것이라 메뉴 구성(6번 종료)과 일부 안내 문구가 최종 버전과 다를 수 있습니다. 최종 버전 화면은 [보너스 기능 실행 화면](#보너스-기능-실행-화면)을 참고하세요.

| 화면 | 캡처 |
|---|---|
| 메뉴 | ![메뉴 화면](docs/screenshots/menu.png) |
| 퀴즈 풀기 | ![퀴즈 풀기 화면](docs/screenshots/play.png) |
| 퀴즈 추가 | ![퀴즈 추가 화면](docs/screenshots/add_quiz.png) |
| 퀴즈 목록 | ![퀴즈 목록 화면](docs/screenshots/quiz_list.png) |
| 점수 확인 | ![점수 확인 화면](docs/screenshots/score.png) |

### 보너스 기능 실행 화면
**① 문제 수 선택 + 힌트 사용**: 3문제를 선택한 뒤, 첫 문제에서 `0`을 눌러 힌트를 보고 맞혀 0.5문제로 인정된 화면입니다.

![문제 수 선택과 힌트 사용 화면](docs/screenshots/bonus_hint.png)

**② 결과와 점수 차감**: 힌트 1회 사용으로 `(0.5 + 1 + 0) ÷ 3 × 100 = 50점`이 되고 최고 점수가 갱신된 화면입니다.

![힌트 사용 결과와 최고 점수 갱신 화면](docs/screenshots/bonus_result.png)

**③ 랜덤 출제**: 같은 3문제 풀기를 다시 실행했을 때 ①과 다른 문제가 다른 순서로 출제된 화면입니다.

![랜덤 출제 화면](docs/screenshots/bonus_random.png)

## 설계: 클래스를 나눈 이유
퀴즈 한 문제와 게임 전체는 **바뀌는 이유가 다르기 때문에** 두 클래스로 나눴습니다.

| 클래스 | 맡은 일 (책임) | 가진 데이터 (속성) | 하는 일 (메서드) |
|---|---|---|---|
| `Quiz` | 퀴즈 한 문제 | `question`, `choices`, `answer`, `hint` | `display()`, `is_correct()`, `has_hint()`, `to_dict()` |
| `QuizGame` | 게임 한 판 전체 | `quizzes`, `best_score`, `history` | `run()`, `play_quiz()`, `add_quiz()`, `show_quiz_list()`, `delete_quiz()`, `show_best_score()`, `save()`, `load()` |

### 추상화: 안을 몰라도 쓸 수 있게
- `QuizGame.play_quiz()`는 `quiz.display(번호)`와 `quiz.is_correct(답)`만 부릅니다. 문제를 어떻게 그리는지, 정답을 어떻게 비교하는지는 몰라도 됩니다.
- 그래서 문제 출력 모양을 바꿀 때는 `Quiz.display()` **한 곳만** 고치면 되고, 게임 흐름 코드는 그대로입니다.
- `save()`/`load()`도 `quiz.to_dict()`에 맡기므로, 퀴즈에 항목이 늘어나도(예: 보너스의 `hint`) 저장 코드 구조는 그대로입니다.

### 재사용: 한 번 만들어 여러 곳에서
| 재사용된 코드 | 쓰이는 곳 |
|---|---|
| `Quiz` 클래스 | 기본 퀴즈 생성, 퀴즈 추가, 파일에서 불러오기 (3곳) |
| `get_number(prompt, min, max)` | 메뉴(1~6), 정답(0~4), 문제 수(1~N), 삭제 번호(0~N) (4곳) |
| `get_text(prompt)` | 문제, 선택지 4개 입력 |
| `save()` | 퀴즈 추가·삭제, 퀴즈 풀기 완료, 종료, Ctrl+C |

### 상태를 객체가 직접 보관 (캡슐화)
함수만 쓰던 단계에서는 `quizzes`와 `best_score`를 함수마다 매개변수로 넘기고 `return`으로 돌려받아야 했습니다. `QuizGame`이 `self.quizzes`, `self.best_score`를 직접 가지면서 `main()`이 20줄 넘던 것에서 2줄로 줄었고, 값 전달 실수가 생길 여지도 없어졌습니다.

`get_number()`, `get_text()`는 게임과 무관한 **범용 입력 도구**라 클래스 밖에 두었습니다. 다른 프로그램에서도 그대로 쓸 수 있습니다.

## 파일 구조
```
quiz-test/
├── main.py        # 프로그램 전체 코드 (Quiz, QuizGame 클래스 및 입력 처리 함수)
├── README.md      # 프로젝트 설명 문서
├── .gitignore     # Git에서 제외할 파일 목록 (.vscode/, state.json, 백업·임시 파일 등)
├── docs/
│   ├── benchmark.py   # 대량 데이터 성능 측정 스크립트
│   └── screenshots/   # README에 사용하는 화면 캡처
│       ├── dev_env.png
│       ├── menu.png, play.png, add_quiz.png, quiz_list.png, score.png
│       ├── bonus_hint.png, bonus_result.png, bonus_random.png
│       └── git_clone.png, git_push.png, git_pull.png, git_log.png
├── state.json     # 실행 중 자동 생성되는 데이터 파일 (Git에는 올리지 않음)
└── state.json.bak # 저장 직전 상태의 자동 백업 (Git에는 올리지 않음)
```

### main.py 구성
| 이름 | 종류 | 역할 |
|---|---|---|
| `Quiz` | 클래스 | 퀴즈 한 문제 (문제, 선택지, 정답, 힌트 / 출력, 정답 확인, 힌트 유무 확인, dict 변환) |
| `QuizGame` | 클래스 | 게임 전체 (퀴즈 목록, 최고 점수, 게임 기록 / 메뉴, 풀기, 추가, 목록, 삭제, 점수, 저장, 불러오기, 백업 복구) |
| `get_default_quizzes()` | 함수 | 힌트가 포함된 기본 퀴즈 8개 생성 |
| `get_number()` / `get_text()` | 함수 | 숫자·글자 입력을 안전하게 받는 공통 입력 함수 |

## 데이터 파일 설명 (`state.json`)
- **경로**: 프로젝트 루트의 `state.json` (`main.py`와 같은 폴더)
- **역할**: 퀴즈 목록, 최고 점수, 게임 기록을 저장하여 프로그램을 종료했다 다시 실행해도 데이터가 유지되도록 합니다.
- **인코딩**: UTF-8
- **저장 시점**: 퀴즈 추가·삭제 후, 퀴즈 풀기를 마쳤을 때, 종료(메뉴 6번 또는 `Ctrl+C`) 시
- **예외 처리**
  - 파일이 없으면(첫 실행) 기본 퀴즈 8개로 시작합니다.
  - 파일이 손상되었으면 백업(`state.json.bak`)으로 복구하고, 백업도 쓸 수 없으면 기본 퀴즈로 초기화합니다. ([백업 및 복구 정책](#백업-및-복구-정책))
  - `hint`, `history`가 없는 이전 형식의 파일도 그대로 불러올 수 있습니다. (힌트는 빈 값, 기록은 빈 목록으로 처리)

### 스키마
```json
{
  "quizzes": [
    {
      "question": "변수에 대한 설명으로 옳은 것은?",
      "choices": ["선택지1", "선택지2", "선택지3", "선택지4"],
      "answer": 1,
      "hint": "score = 0 처럼 이름을 붙여 값을 담아 두는 것을 떠올려 보세요."
    }
  ],
  "best_score": 100,
  "history": [
    {
      "date": "2026-11-10 15:30",
      "total": 5,
      "correct": 4,
      "hints": 1,
      "score": 70
    }
  ]
}
```
| 키 | 타입 | 설명 |
|---|---|---|
| `quizzes` | list | 퀴즈 목록 |
| `quizzes[].question` | str | 문제 |
| `quizzes[].choices` | list (str 4개) | 선택지 |
| `quizzes[].answer` | int (1~4) | 정답 번호 |
| `quizzes[].hint` | str | 힌트 (없으면 빈 문자열 `""`) |
| `best_score` | int 또는 null | 최고 점수 (100점 만점, 아직 풀지 않았으면 `null`) |
| `history` | list | 게임 기록 목록 (오래된 순) |
| `history[].date` | str | 게임을 마친 날짜/시간 (`YYYY-MM-DD HH:MM`) |
| `history[].total` | int | 푼 문제 수 |
| `history[].correct` | int | 맞힌 문제 수 |
| `history[].hints` | int | 힌트 사용 횟수 |
| `history[].score` | int | 점수 (100점 만점) |

## 백업 및 복구 정책
### 자동 백업 (코드에 구현)
`QuizGame.save()`는 저장할 때마다 아래 3단계를 거칩니다.

1. 현재 `state.json`을 `state.json.bak`으로 복사합니다. → **직전 저장 상태 1세대**를 항상 보관
2. 새 데이터를 `state.json.tmp`에 끝까지 씁니다.
3. 다 쓴 뒤 `os.replace()`로 `state.json`과 한 번에 바꿉니다. → 저장 도중 프로그램이 꺼져도 `state.json`이 반쯤 쓰인 상태로 깨지지 않음

### 자동 복구 (코드에 구현)
`QuizGame.load()`가 `state.json`을 읽지 못하면 다음 순서로 복구합니다.

| 상황 | 동작 | 화면 메시지 |
|---|---|---|
| `state.json` 없음 (첫 실행) | 기본 퀴즈 8개로 시작 | `📂 저장된 파일이 없어 기본 퀴즈 8개로 시작합니다.` |
| `state.json` 손상, 백업 정상 | 백업을 읽고 `state.json`에 다시 복사 | `♻️ 백업 파일(state.json.bak)로 복구했습니다.` |
| 둘 다 손상 또는 백업 없음 | 기본 퀴즈로 초기화 | `⚠️ 사용할 수 있는 백업이 없어 기본 퀴즈로 복구합니다.` |

### 수동 복구 절차
프로그램을 종료한 상태에서 프로젝트 폴더(`main.py`가 있는 곳)에서 실행합니다.

```bash
# 1. 파일이 JSON으로 정상인지 확인 (오류가 나면 손상된 것)
python3 -m json.tool state.json > /dev/null && echo "state.json 정상"
python3 -m json.tool state.json.bak > /dev/null && echo "백업 정상"

# 2. 손상된 파일은 지우지 말고 이름을 바꿔 보관
mv state.json state.json.broken

# 3. 백업으로 되돌리기
cp state.json.bak state.json

# 4. 완전히 처음 상태로 초기화하고 싶을 때 (기본 퀴즈 8개로 시작)
mv state.json state.json.old && mv state.json.bak state.json.bak.old
python3 main.py
```

### 정책 요약
| 항목 | 내용 |
|---|---|
| 백업 시점 | 매 저장 직전 (퀴즈 추가·삭제, 풀기 완료, 종료) |
| 보관 개수 | 1세대 (`state.json.bak`) |
| Git 포함 여부 | 제외 (`.gitignore`에 `state.json`, `state.json.bak`, `state.json.tmp`) |
| 장기 보관이 필요하면 | 날짜를 붙여 복사: `cp state.json backup/state_$(date +%Y%m%d).json` |

## 대량 데이터 확장성 분석 (1,000개 이상)
### 측정 결과
`docs/benchmark.py`로 퀴즈 수를 1천·1만·10만 개로 늘려 측정했습니다(Python 3.13, Linux 환경, 3회 중 가장 빠른 값). 스크립트는 임시 폴더에서 돌아가므로 실제 `state.json`을 건드리지 않으며, `python3 docs/benchmark.py`로 누구나 다시 측정할 수 있습니다.

| 퀴즈 수 | 저장(ms) | 불러오기(ms) | 파일 크기(KB) | 메모리(KB) | 랜덤 10개 뽑기(ms) | 목록 출력(ms) | 문제 검색: 리스트(ms) | 문제 검색: dict(ms) |
|---|---|---|---|---|---|---|---|---|
| 1,000 | 4.8 | 1.4 | 295 | 691 | 0.002 | 0.2 | 0.02 | 0.0001 |
| 10,000 | 49.2 | 19.5 | 3,011 | 7,042 | 0.004 | 2.6 | 0.29 | 0.0001 |
| 100,000 | 473.4 | 281.1 | 30,697 | 71,550 | 0.008 | 24.3 | 3.22 | 0.0001 |

### 분석
| 동작 | 시간 복잡도 | 결과 해석 |
|---|---|---|
| 저장 `save()` | O(N) | 퀴즈 하나만 추가해도 **파일 전체를 다시 씀**. 10만 개에서 저장 1회 약 0.5초, 파일 30MB |
| 불러오기 `load()` | O(N) | 시작할 때 1회라 1만 개(0.02초)까지는 체감 없음 |
| 메모리 | O(N) | 퀴즈 1개당 약 0.7KB. 10만 개도 약 70MB로 실행 가능 |
| 랜덤 출제 `random.sample` | O(k) | 뽑는 개수에만 비례. 10만 개에서도 차이 없음 |
| 목록 출력 | O(N) | 계산은 빠르지만 1천 줄 이상은 **사람이 읽을 수 없음** |
| 문제로 검색(리스트 순회) | O(N) | 10만 개에서 3ms. 중복 확인을 매번 하면 누적됨 |
| 문제로 검색(dict 인덱스) | O(1) | 개수와 무관하게 일정 |
| 삭제 `list.pop(i)` | O(N) | 뒤 요소를 한 칸씩 당김. 10만 개에서도 1ms 미만 |

**결론**: 현재 구조로 **1만 개까지는 문제없이** 동작합니다. 10만 개 수준에서는 "추가·삭제할 때마다 30MB 파일 전체를 다시 쓰는 것"과 "목록 전체 출력"이 병목입니다.

### 개선 방안 (규모별)
| 규모 | 개선 방법 | 바꿀 곳 |
|---|---|---|
| 1,000개 이상 | 목록을 **페이지 단위(예: 20개씩)** 로 출력 | `show_quiz_list()` |
| 1,000개 이상 | `history`를 최근 100개만 보관 | `play_quiz()`의 기록 추가 부분 |
| 1만 개 이상 | 문제 문장 → 퀴즈 **dict 인덱스**로 중복 추가 방지·검색 | `QuizGame.__init__`, `add_quiz()` |
| 1만 개 이상 | 저장 파일의 `indent=2` 제거로 크기 약 24% 축소 (1만 개 기준 3.0MB → 2.3MB 측정) | `save()`의 `json.dump` |
| 10만 개 이상 | 매번 전체 저장 대신 **종료 시 한 번 저장** 또는 변경분만 저장 | `save()` 호출 위치 |
| 10만 개 이상 | 표준 라이브러리 `sqlite3`로 저장소 교체 (한 줄씩 추가·삭제) | `save()`, `load()`, `read_state()` |

## 요구사항 변경 시 수정 가이드
자주 생길 만한 변경과 고쳐야 할 위치를 정리했습니다. 대부분 **한두 곳만** 고치면 되도록 나눠 두었습니다.

| 바꾸고 싶은 것 | 수정할 파일 · 위치 | 함께 확인할 것 |
|---|---|---|
| 점수 계산 방식 (예: 힌트 차감 비율) | `main.py` 상수 `HINT_PENALTY`, `QuizGame.play_quiz()`의 `score = ...` 줄 | README 점수 계산식 |
| 선택지 개수 (4개 → 5개) | `QuizGame.add_quiz()`의 `range(4)`, `play_quiz()`의 `get_number(..., 0, 4)`, `get_default_quizzes()`의 선택지 | 기존 `state.json` 퀴즈는 4개라 그대로 둘지 결정 |
| 퀴즈에 새 항목 추가 (예: 난이도) | `Quiz.__init__()`, `Quiz.to_dict()`, `QuizGame.read_state()`의 `item.get("난이도", 기본값)`, `add_quiz()` 입력 | README 스키마 표 |
| 문제 출력 모양 | `Quiz.display()` | 없음 (다른 코드는 그대로) |
| 메뉴 추가 | `QuizGame.show_menu()`, `QuizGame.run()`의 `elif`와 `get_number` 범위 | README 기능 목록 |
| 기본 퀴즈 내용 | `get_default_quizzes()` | 이미 `state.json`이 있으면 반영 안 됨 → 파일 초기화 필요 |
| 저장 파일 이름·위치 | 상수 `STATE_FILE` (백업·임시 파일 이름도 자동으로 따라감) | `.gitignore`, README |
| 저장 형식 (JSON → DB 등) | `QuizGame.save()`, `QuizGame.read_state()`, `restore_from_backup()` | 다른 메서드는 `self.quizzes`만 쓰므로 수정 불필요 |
| 입력 검증 규칙 | `get_number()`, `get_text()` | 모든 메뉴에 동시에 적용됨 |
| 기록 표시 개수 | `QuizGame.show_best_score()`의 `self.history[-5:]` | 없음 |

## Git 작업 규칙
### 커밋 단위
- **기능 하나 = 커밋 하나**: 메뉴, Quiz 클래스, 퀴즈 풀기, 추가, 목록, 점수, 저장, README처럼 과제 단계별로 커밋합니다.
- 실행해서 동작을 확인한 뒤에만 커밋합니다. (작성 → 저장 → Problems 0 확인 → 실행 테스트 → 커밋 → push)
- 기능 추가와 단순 정리(파일 제외, 오타)는 섞지 않고 따로 커밋합니다.

### 커밋 메시지 템플릿
```
<타입>: <무엇을 했는지 한 줄 요약>

예) Feat: 퀴즈 추가 기능 구현
```
| 타입 | 언제 쓰나 | 실제 커밋 예 |
|---|---|---|
| `Feat` | 새 기능 추가 | `Feat: 최고 점수 확인 및 갱신 기능 구현` |
| `Fix` | 버그·오류 수정 | `Fix: 함수 이름 및 예외 처리 문법 오류 수정` |
| `Refactor` | 동작은 같고 구조만 개선 | `Refactor: QuizGame 클래스로 게임 로직 구조화` |
| `Docs` | README 등 문서 | `Docs: README 작성 및 실행 화면 스크린샷 추가` |
| `Chore` | 설정·정리 (gitignore 등) | `Chore: .gitignore 공백 오류 수정 및 README 실행 화면 반영` |
| `Merge` | 브랜치 병합 | `Merge: 보너스 과제 병합` |

### 브랜치 규칙
- `main`: 항상 실행 가능한 상태만 유지
- `feature/<기능이름>`: 새 기능 작업용 (예: `feature/play-quiz`, `feature/bonus`)
- 병합은 `git merge --no-ff`로 해서 병합 기록을 남깁니다.

## Git 실습 기록
### 커밋 기록 (`git --no-pager log --oneline --graph`)
의미 있는 커밋 22개와 두 번의 브랜치 병합 기록입니다. (보너스 병합 시점 기준)
```
*   ffa0a63 (HEAD -> main, origin/main, origin/HEAD) Merge: 보너스 과제 병합
|\
| * 41639c2 (origin/feature/bonus, feature/bonus) Feat: 보너스 과제 구현 및 실행 화면 추가
| * 592df59 Feat: 보너스 과제 구현 (랜덤 출제, 문제 수 선택, 힌트, 퀴즈 삭제, 점수 기록)
|/
* ff254b9 Chore: .gitignore 공백 오류 수정 및 README 실행 화면 반영
* 23a5d2f Docs: clone/push/pull 실습 화면 추가
* 01f9f6e Chore: .vscode 폴더 추적 제외 및 .gitignore 정리
* 5ecf9b2 Docs: clone/pull 실습 기록 추가
* 0072e37 Chore: .vscode 폴더 추적 제외 및 .gitignore 정리
* 701a092 Docs: README 작성 및 실행 화면 스크린샷 추가
* 8806f14 Feat: state.json 파일 저장 및 불러오기 기능 구현
* 3a09c59 Refactor: QuizGame 클래스로 게임 로직 구조화
* 6434c45 Feat: 최고 점수 확인 및 갱신 기능 구현
* ca60cfc Feat:퀴즈 목록 기능 구현
* e49bd2b Feat: 퀴즈 추가 기능 구현
*   3779cba Merge: 퀴즈풀기 병합
|\
| * 34dec62 (origin/feature/play-quiz, feature/play-quiz) Feat: 퀴즈 풀기 기능 구현 및 종료 버그 수정
|/
* d1f6043 Feat : 파이썬 기초 주제의 기본 퀴즈 8개 작성
* 5394ed8 Fix: 함수 이름 및 예외 처리 문법 오류 수정
* 4b0bcb7 Feat: 메뉴 출력 및 입력 검증 기능 구현
* 065ff5b Chore: .vscode 폴더 추적 제외
* 9e2bb6e Fix: README 파일명 수정 및 .vscode 제외
* 38eb257 chore: 프로젝트 초기 설정
```

![git log --oneline --graph 실행 화면](docs/screenshots/git_log.png)

### 브랜치 생성 및 병합
| 브랜치 | 작업 내용 | 병합 커밋 |
|---|---|---|
| `feature/play-quiz` | 퀴즈 풀기 기능 (`34dec62`) | `3779cba Merge: 퀴즈풀기 병합` |
| `feature/bonus` | 보너스 과제 5개 (`592df59`, `41639c2`) | `ffa0a63 Merge: 보너스 과제 병합` |

```
hyejin@localhost:~/codyssey/quiz-game$ git checkout -b feature/play-quiz
Switched to a new branch 'feature/play-quiz'
hyejin@localhost:~/codyssey/quiz-game$ git branch
* feature/play-quiz
  main
...
hyejin@localhost:~/codyssey/quiz-game$ git checkout main
Switched to branch 'main'
Your branch is up to date with 'origin/main'.
hyejin@localhost:~/codyssey/quiz-game$ git merge --no-ff feature/play-quiz -m "Merge: 퀴즈풀기 병합"
Merge made by the 'ort' strategy.
 main.py | 42 +++++++++++++++++++++++++++++++++++-------
 1 file changed, 35 insertions(+), 7 deletions(-)
```

### clone / pull 실습
GitHub 저장소를 별도 폴더(`quiz-clone`)에 복제한 뒤, 복제한 저장소에서 README를 수정해 `push`하고,
원래 작업 폴더(`quiz-game`)에서 `pull`로 변경사항을 받아왔습니다.

**1. `git clone`: 별도 폴더(`quiz-clone`)에 저장소 복제**
```
hyejin@localhost:~/codyssey/quiz-game$ cd ~/codyssey
hyejin@localhost:~/codyssey$ git clone https://github.com/haegirl23-max/quiz-test.git quiz-clone
Cloning into 'quiz-clone'...
remote: Enumerating objects: 54, done.
remote: Counting objects: 100% (54/54), done.
remote: Compressing objects: 100% (37/37), done.
remote: Total 54 (delta 20), reused 45 (delta 11), pack-reused 0 (from 0)
Receiving objects: 100% (54/54), 141.55 KiB | 889.00 KiB/s, done.
Resolving deltas: 100% (20/20), done.
hyejin@localhost:~/codyssey$ cd quiz-clone
hyejin@localhost:~/codyssey/quiz-clone$ ls
README.md  docs  main.py
```
![git clone 실행 화면](docs/screenshots/git_clone.png)

**2. 복제한 저장소에서 README 수정 후 `commit`, `push`**
```
hyejin@localhost:~/codyssey/quiz-clone$ printf "\n## Git 실습 기록\n- clone한 저장소에서 README를 수정하고 push한 뒤, 원래 작업 폴더에서 pull로 받아왔습니다.\n" >> README.md
hyejin@localhost:~/codyssey/quiz-clone$ git add .
hyejin@localhost:~/codyssey/quiz-clone$ git commit -m "Docs: clone/pull 실습 기록 추가"
[main 5ecf9b2] Docs: clone/pull 실습 기록 추가
 1 file changed, 3 insertions(+)
hyejin@localhost:~/codyssey/quiz-clone$ git push
Enumerating objects: 5, done.
Counting objects: 100% (5/5), done.
Delta compression using up to 12 threads
Compressing objects: 100% (3/3), done.
Writing objects: 100% (3/3), 485 bytes | 485.00 KiB/s, done.
Total 3 (delta 2), reused 0 (delta 0), pack-reused 0 (from 0)
remote: Resolving deltas: 100% (2/2), completed with 2 local objects.
To https://github.com/haegirl23-max/quiz-test.git
   0072e37..5ecf9b2  main -> main
```
![quiz-clone에서 commit, push 실행 화면](docs/screenshots/git_push.png)

**3. `git pull`: 원래 작업 폴더(`quiz-game`)에서 변경사항 받아오기**
```
hyejin@localhost:~/codyssey/quiz-clone$ cd ~/codyssey/quiz-game
hyejin@localhost:~/codyssey/quiz-game$ git pull
remote: Enumerating objects: 5, done.
remote: Counting objects: 100% (5/5), done.
remote: Compressing objects: 100% (1/1), done.
remote: Total 3 (delta 2), reused 3 (delta 2), pack-reused 0 (from 0)
Unpacking objects: 100% (3/3), 465 bytes | 465.00 KiB/s, done.
From https://github.com/haegirl23-max/quiz-test
   0072e37..5ecf9b2  main       -> origin/main
Updating 0072e37..5ecf9b2
Fast-forward
 README.md | 3 +++
 1 file changed, 3 insertions(+)
hyejin@localhost:~/codyssey/quiz-game$ tail -3 README.md

## Git 실습 기록
- clone한 저장소에서 README를 수정하고 push한 뒤, 원래 작업 폴더에서 pull로 받아왔습니다.
```
![git pull 실행 화면](docs/screenshots/git_pull.png)

clone 쪽에서 만든 커밋 `5ecf9b2`가 pull 후 `quiz-game`의 기록에도 그대로 나타납니다(위 커밋 기록 참고).

### 사용한 Git 명령어
`init`, `add`, `commit`, `push`, `checkout`, `merge`, `clone`, `pull`, `status`, `log`, `rm --cached`, `restore`

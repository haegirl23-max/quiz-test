import json
import os
import random
import shutil
from datetime import datetime

STATE_FILE = "state.json"            # 데이터를 저장할 파일 이름 (프로젝트 루트)
BACKUP_FILE = STATE_FILE + ".bak"    # 저장 직전 상태를 보관하는 백업 파일
TEMP_FILE = STATE_FILE + ".tmp"      # 저장 도중 끊겨도 원본이 깨지지 않게 먼저 쓰는 임시 파일
HINT_PENALTY = 0.5          # 힌트를 보고 맞히면 1문제의 절반(0.5)만 인정


class Quiz:
    """퀴즈 한 문제를 표현하는 클래스"""

    def __init__(self, question, choices, answer, hint=""):
        self.question = question    # 문제 (str)
        self.choices = choices      # 선택지 4개 (list)
        self.answer = answer        # 정답 번호 1~4 (int)
        self.hint = hint            # 힌트 (str, 없으면 빈 문자열) ← 보너스 3

    def display(self, number):
        """퀴즈 문제와 선택지를 화면에 출력한다."""
        print("-" * 40)
        print(f"문제 {number}.")
        print(f" ❓{self.question}")
        print()
        for i, choice in enumerate(self.choices, start=1):
            print(f"  {i}. {choice}")
        print()

    def is_correct(self, user_answer):
        """사용자가 입력한 답이 정답이면 True, 아니면 False를 반환한다."""
        return user_answer == self.answer

    def has_hint(self):
        """힌트가 있으면 True를 돌려준다."""
        return self.hint != ""

    def to_dict(self):
        """JSON으로 저장할 수 있도록 dict 형태로 바꿔서 돌려준다."""
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
            "hint": self.hint,
        }


def get_default_quizzes():
    """처음 실행할 때 사용할 기본 퀴즈 목록을 만든다."""
    quizzes = [
        Quiz(
            "변수에 대한 설명으로 옳은 것은?",
            ["값을 저장해 두고 이름으로 다시 꺼내 쓰는 상자",
             "한 번 저장하면 절대 바꿀 수 없는 값",
             "숫자만 저장할 수 있는 공간",
             "프로그램을 종료하는 명령"],
            1,
            "score = 0 처럼 이름을 붙여 값을 담아 두는 것을 떠올려 보세요.",
        ),
        Quiz(
            "다음 중 dict(딕셔너리) 자료형은?",
            ["[1, 2, 3]", "'hello'", "{'answer': 1}", "True"],
            3,
            "dict는 중괄호 { } 안에 '이름: 값' 쌍으로 적습니다.",
        ),
        Quiz(
            "score = 75일 때 결과는? (if 90 이상 A / elif 70 이상 B / else C)",
            ["A", "B", "C", "아무것도 출력되지 않는다"],
            2,
            "위에서부터 차례로 조건을 확인하고, 처음 참이 되는 곳에서 멈춥니다.",
        ),
        Quiz(
            "'종료'를 선택할 때까지 메뉴를 계속 반복하려면 가장 알맞은 것은?",
            ["for i in range(5):", "if True:", "def menu():", "while True: 와 break"],
            4,
            "언제 끝날지 모를 때 쓰는 반복문과, 반복문을 빠져나가는 명령을 떠올려 보세요.",
        ),
        Quiz(
            "def add(a, b): return a + b 일 때, add(2, 3)의 결과는?",
            ["23", "None", "5", "에러 발생"],
            3,
            "2와 3은 따옴표가 없는 숫자(int)입니다.",
        ),
        Quiz(
            "클래스와 인스턴스의 관계를 가장 잘 설명한 것은?",
            ["클래스와 인스턴스는 같은 말이다",
             "인스턴스가 클래스를 만든다",
             "클래스는 반복문의 한 종류다",
             "클래스는 설계도, 인스턴스는 그 설계도로 만든 실제 객체다"],
            4,
            "도면 한 장으로 여러 제품을 만드는 관계를 떠올려 보세요.",
        ),
        Quiz(
            "__init__ 메서드는 언제 실행될까?",
            ["프로그램이 끝날 때",
             "print()를 호출할 때",
             "클래스로 객체를 만들 때 자동으로",
             "직접 이름을 불러야만 실행된다"],
            3,
            "game = QuizGame() 한 줄만으로 퀴즈 목록이 준비되는 이유입니다.",
        ),
        Quiz(
            "퀴즈 데이터를 JSON 파일에 저장하는 가장 큰 이유는?",
            ["프로그램 실행 속도를 높이려고",
             "코드의 문법 오류를 찾으려고",
             "화면에 색을 입히려고",
             "프로그램을 종료해도 데이터를 유지하려고"],
            4,
            "'데이터 영속성'이라는 말을 떠올려 보세요.",
        ),
    ]
    return quizzes


def get_number(prompt, min_value, max_value):
    """min_value~max_value 사이의 숫자를 받을 때까지 계속 물어본다."""
    while True:
        text = input(prompt).strip()

        if text == "":
            print("⚠️입력값이 없습니다. 다시 입력해주세요.")
            continue

        try:
            number = int(text)
        except ValueError:
            print(f"⚠️잘못된 입력입니다. {min_value}~{max_value} 사이의 숫자를 입력해주세요.")
            continue

        if number < min_value or number > max_value:
            print(f"⚠️잘못된 입력입니다. {min_value}~{max_value} 사이의 숫자를 입력해주세요.")
            continue

        return number


def get_text(prompt):
    """빈 값이 아닌 글자를 받을 때까지 계속 물어본다."""
    while True:
        text = input(prompt).strip()

        if text == "":
            print("⚠️입력값이 없습니다. 다시 입력해주세요.")
            continue

        return text


class QuizGame:
    """ 퀴즈 게임 전체(퀴즈 목록, 최고 점수, 기록, 메뉴 흐름)를 관리하는 클래스 """

    def __init__(self):
        self.quizzes = get_default_quizzes()   # 퀴즈 목록
        self.best_score = None                 # 최고 점수
        self.history = []                      # 게임 기록 목록 ← 보너스 5
        self.load()                            # 저장된 데이터가 있으면 불러오기

    def show_menu(self):
        print("=" * 40)
        print("        🎯 나만의 퀴즈 게임 🎯")
        print("=" * 40)
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 퀴즈 삭제")
        print("6. 종료")
        print("=" * 40)

    def play_quiz(self):
        """문제 수를 고르고, 랜덤 순서로 퀴즈를 풀어 점수를 계산한다."""
        if len(self.quizzes) == 0:
            print("⚠️ 퀴즈가 없습니다. 먼저 퀴즈를 추가해주세요.")
            return

        # 보너스 2: 몇 문제를 풀지 선택
        total = get_number(f"몇 문제를 풀까요? (1~{len(self.quizzes)}): ", 1, len(self.quizzes))

        # 보너스 1: 랜덤 출제 (전체에서 total개를 겹치지 않게 무작위로 뽑음)
        selected = random.sample(self.quizzes, total)

        print(f"🎮 퀴즈를 시작합니다! 총 {total}문제")
        print("💡 정답 입력에서 0을 누르면 힌트를 볼 수 있어요. (힌트 후 정답은 0.5문제로 인정)")
        earned = 0          # 획득 점수 (정답 1, 힌트 사용 후 정답 0.5)
        correct_count = 0   # 맞힌 문제 수
        hint_count = 0      # 힌트를 사용한 횟수

        for number, quiz in enumerate(selected, start=1):
            quiz.display(number)
            used_hint = False

            # 보너스 3: 0을 입력하면 힌트 보기
            while True:
                user_answer = get_number("정답 번호를 입력하세요 (1~4, 힌트: 0): ", 0, 4)
                if user_answer != 0:
                    break

                if used_hint:
                    print(f"💡 힌트(다시 보기): {quiz.hint}")
                elif quiz.has_hint():
                    used_hint = True
                    hint_count += 1
                    print(f"💡 힌트: {quiz.hint}")
                else:
                    print("⚠️ 이 문제에는 힌트가 없습니다.")

            if quiz.is_correct(user_answer):
                correct_count += 1
                if used_hint:
                    earned += HINT_PENALTY
                    print("✅ 정답입니다! (힌트 사용으로 0.5문제 인정)\n")
                else:
                    earned += 1
                    print("✅ 정답입니다!\n")
            else:
                print(f"❌ 오답입니다. 정답은 {quiz.answer}번입니다.\n")

        score = int(earned / total * 100)
        print("=" * 40)
        print(f"🏆 결과: {total}문제 중 {correct_count}문제 정답! ({score}점)")
        if hint_count > 0:
            print(f"💡 힌트 사용: {hint_count}회")
        print("=" * 40)

        # 보너스 5: 게임 기록 저장
        self.history.append({
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "total": total,
            "correct": correct_count,
            "hints": hint_count,
            "score": score,
        })

        if self.best_score is None or score > self.best_score:
            self.best_score = score
            print("🎉 새로운 최고 점수입니다!")

        self.save()

    def add_quiz(self):
        """문제, 선택지 4개, 정답, 힌트(선택)를 입력받아 새 퀴즈를 추가한다."""
        print("📝 새 퀴즈를 추가합니다.")
        question = get_text("문제를 입력하세요: ")

        choices = []
        for i in range(4):
            choice = get_text(f"선택지 {i + 1}: ")
            choices.append(choice)

        answer = get_number("정답 번호 (1~4): ", 1, 4)
        hint = input("힌트 (없으면 Enter): ").strip()

        new_quiz = Quiz(question, choices, answer, hint)
        self.quizzes.append(new_quiz)
        print("✅ 새 퀴즈가 추가되었습니다!")
        self.save()

    def show_quiz_list(self):
        """등록된 퀴즈 목록을 출력한다."""
        if len(self.quizzes) == 0:
            print("⚠️ 퀴즈가 없습니다. 먼저 퀴즈를 추가해주세요.")
            return

        print(f"\n📚 등록된 퀴즈 목록:(총 {len(self.quizzes)}개):")
        print("-" * 40)
        for number, quiz in enumerate(self.quizzes, start=1):
            print(f"{number}. {quiz.question}")
        print("-" * 40)

        print()

    def delete_quiz(self):
        """보너스 4: 번호를 골라 퀴즈를 삭제하고 파일에 반영한다."""
        if len(self.quizzes) == 0:
            print("⚠️ 삭제할 퀴즈가 없습니다.")
            return

        self.show_quiz_list()
        number = get_number(f"삭제할 퀴즈 번호 (1~{len(self.quizzes)}, 취소: 0): ", 0, len(self.quizzes))
        if number == 0:
            print("↩️ 삭제를 취소했습니다.")
            return

        target = self.quizzes[number - 1]
        confirm = input(f"'{target.question}' 퀴즈를 삭제할까요? (y/n): ").strip().lower()
        if confirm != "y":
            print("↩️ 삭제를 취소했습니다.")
            return

        self.quizzes.pop(number - 1)
        print(f"🗑️ 퀴즈가 삭제되었습니다. (남은 퀴즈 {len(self.quizzes)}개)")
        self.save()

    def show_best_score(self):
        """최고 점수와 최근 게임 기록을 출력한다."""
        if self.best_score is None:
            print("⚠️ 아직 퀴즈를 풀지 않았습니다. 먼저 퀴즈를 풀어주세요.")
            return

        print(f"\n🏆 최고 점수: {self.best_score}점")

        # 보너스 5: 최근 기록 최대 5개를 최신순으로 보여주기
        if len(self.history) > 0:
            print("\n📜 최근 게임 기록 (최신순)")
            print("-" * 40)
            recent = self.history[-5:]
            recent.reverse()
            for record in recent:
                line = f"{record['date']} | {record['total']}문제 중 {record['correct']}개 정답 | {record['score']}점"
                if record["hints"] > 0:
                    line += f" | 힌트 {record['hints']}회"
                print(line)
            print("-" * 40)
            print(f"총 {len(self.history)}번 플레이했습니다.")

    def run(self):
        """메뉴를 반복해서 보여주고 사용자의 선택에 따라 기능을 실행한다."""
        while True:
            self.show_menu()
            choice = get_number("원하는 메뉴 번호를 입력하세요 (1~6): ", 1, 6)

            if choice == 1:
                self.play_quiz()
            elif choice == 2:
                self.add_quiz()
            elif choice == 3:
                self.show_quiz_list()
            elif choice == 4:
                self.show_best_score()
            elif choice == 5:
                self.delete_quiz()
            elif choice == 6:
                self.save()
                print("👋 게임을 종료합니다. 다음에 또 만나요!")
                break

    def save(self):
        """퀴즈 목록, 최고 점수, 게임 기록을 state.json에 저장한다."""
        quiz_list = []
        for quiz in self.quizzes:
            quiz_list.append(quiz.to_dict())

        data = {
            "quizzes": quiz_list,
            "best_score": self.best_score,
            "history": self.history,
        }

        try:
            # ① 지금 파일을 백업으로 복사 (한 단계 이전 상태 보관)
            if os.path.exists(STATE_FILE):
                shutil.copyfile(STATE_FILE, BACKUP_FILE)
            # ② 임시 파일에 먼저 끝까지 쓰고
            with open(TEMP_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            # ③ 다 쓴 뒤에 한 번에 바꿔치기 (중간에 끊겨도 state.json은 온전함)
            os.replace(TEMP_FILE, STATE_FILE)
        except OSError:
            print("⚠️ 데이터를 파일에 저장하지 못했습니다.")

    def read_state(self, path):
        """path의 JSON 파일을 읽어 (퀴즈 목록, 최고 점수, 기록)을 돌려준다. 문제가 있으면 예외가 그대로 올라간다."""
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        quizzes = []
        for item in data["quizzes"]:
            # 힌트가 없던 예전 파일도 읽을 수 있도록 get()으로 기본값 "" 사용
            quizzes.append(Quiz(item["question"], item["choices"], item["answer"], item.get("hint", "")))

        return quizzes, data["best_score"], data.get("history", [])

    def load(self):
        """state.json을 불러온다. 손상됐으면 백업(state.json.bak)으로, 백업도 없으면 기본 퀴즈로 복구한다."""
        try:
            self.quizzes, self.best_score, self.history = self.read_state(STATE_FILE)

            if self.best_score is None:
                score_text = "기록 없음"
            else:
                score_text = f"{self.best_score}점"
            print(f"📂 저장된 데이터를 불러왔습니다. (퀴즈 {len(self.quizzes)}개, 최고점수 {score_text})")

        except FileNotFoundError:
            print(f"📂 저장된 파일이 없어 기본 퀴즈 {len(self.quizzes)}개로 시작합니다.")

        except (ValueError, KeyError, TypeError, OSError):
            print("⚠️ 데이터 파일이 손상되었거나 읽을 수 없습니다.")
            self.restore_from_backup()

    def restore_from_backup(self):
        """백업 파일로 복구를 시도하고, 실패하면 기본 퀴즈로 초기화한다."""
        try:
            self.quizzes, self.best_score, self.history = self.read_state(BACKUP_FILE)
            shutil.copyfile(BACKUP_FILE, STATE_FILE)
            print(f"♻️ 백업 파일(state.json.bak)로 복구했습니다. (퀴즈 {len(self.quizzes)}개)")
        except (FileNotFoundError, ValueError, KeyError, TypeError, OSError):
            self.quizzes = get_default_quizzes()
            self.best_score = None
            self.history = []
            print("⚠️ 사용할 수 있는 백업이 없어 기본 퀴즈로 복구합니다.")

def main():
    """게임 객체를 만들고 실행한다. 중간에 강제 종료되면 저장 후 종료한다."""
    game = QuizGame()
    try:
        game.run()
    except (KeyboardInterrupt, EOFError):
        print("\n⚠️ 입력이 중단되었습니다. 데이터를 저장하고 종료합니다.")
        game.save()


if __name__ == "__main__":
    main()

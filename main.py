class Quiz:
    """퀴즈 한 문제를 표현하는 클래스"""

    def __init__(self, question, choices, answer):
        self.question = question    # 문제 (str)
        self.choices = choices      # 선택지 4개 (list)
        self.answer = answer        # 정답 번호 1~4 ()

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
        ),
        Quiz(
            "다음 중 dict(딕셔너리) 자료형은?",
            ["[1, 2, 3]", "'hello'", "{'answer': 1}", "True"],
            3,
        ),
        Quiz(
            "score = 75일 때 결과는? (if 90 이상 A / elif 70 이상 B / else C)",
            ["A", "B", "C", "아무것도 출력되지 않는다"],
            2,
        ),
        Quiz(
            "'종료'를 선택할 때까지 메뉴를 계속 반복하려면 가장 알맞은 것은?",
            ["for i in range(5):", "if True:", "def menu():", "while True: 와 break"],
            4,
        ),
        Quiz(
            "def add(a, b): return a + b 일 때, add(2, 3)의 결과는?",
            ["23", "None", "5", "에러 발생"],
            3,
        ),
        Quiz(
            "클래스와 인스턴스의 관계를 가장 잘 설명한 것은?",
            ["클래스와 인스턴스는 같은 말이다",
             "인스턴스가 클래스를 만든다",
             "클래스는 반복문의 한 종류다",
             "클래스는 설계도, 인스턴스는 그 설계도로 만든 실제 객체다"],
            4,
        ),
        Quiz(
            "__init__ 메서드는 언제 실행될까?",
            ["프로그램이 끝날 때",
             "print()를 호출할 때",
             "클래스로 객체를 만들 때 자동으로",
             "직접 이름을 불러야만 실행된다"],
            3,
        ),
        Quiz(
            "퀴즈 데이터를 JSON 파일에 저장하는 가장 큰 이유는?",
            ["프로그램 실행 속도를 높이려고",
             "코드의 문법 오류를 찾으려고",
             "화면에 색을 입히려고",
             "프로그램을 종료해도 데이터를 유지하려고"],
            4,
        ),
 ]
    return quizzes


def show_menu():
    """메뉴 화면을 출력한다."""
    print("=" * 40)
    print("        🎯 나만의 퀴즈 게임 🎯")
    print("=" * 40)
    print("1. 퀴즈 풀기")
    print("2. 퀴즈 추가")
    print("3. 퀴즈 목록")
    print("4. 점수 확인")
    print("5. 종료")
    print("=" * 40)



def get_number(prompt, min_value, max_value):
    """min_value~max_value 사이의 숫자를 받을 때까지 계속 물어본다."""
    while True:
        text=input(prompt).strip()

        if text == "":
            print("⚠️입력값이 없습니다. 다시 입력해주세요.")
            continue
        
        try:
            number=int(text)
        except ValueError:
            print(f"⚠️잘못된 입력입니다. {min_value}~{max_value} 사이의 숫자를 입력해주세요.")
            continue           

        if number < min_value or number > max_value:
            print(f"⚠️잘못된 입력입니다. {min_value}~{max_value} 사이의 숫자를 입력해주세요.")
            continue

        return number

def main():
    """프로그램 전체 흐름: 메뉴 → 선택 → 실행을 반복한다."""
    while True:
        show_menu()
        choice = get_number("선택: ", 1, 5)

        if choice == 1:
            print("📝 퀴즈 풀기 (준비 중)")
            # 여기에 퀴즈 풀기 기능을 구현
        elif choice == 2:
            print("📌 퀴즈 추가 (준비 중)")
            # 여기에 퀴즈 추가 기능을 구현
        elif choice == 3:
            print("📋 퀴즈 목록 (준비 중)")
            # 여기에 퀴즈 목록 기능을 구현
        elif choice == 4:
            print("🏆 점수 확인 (준비 중)")
            # 여기에 점수 확인 기능을 구현
        elif choice == 5:
           print("👋 게임을 종료합니다. 다음에 또 만나요!")

if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n👋 게임을 종료합니다. 다음에 또 만나요!")
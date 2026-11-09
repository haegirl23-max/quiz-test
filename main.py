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
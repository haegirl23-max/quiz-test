"""퀴즈 수가 늘어날 때 저장·불러오기·검색 성능을 측정하는 스크립트.

실행: 프로젝트 루트에서 `python3 docs/benchmark.py`
- 임시 폴더에서 실행하므로 내 state.json은 건드리지 않습니다.
- 표준 라이브러리만 사용합니다.
"""
import contextlib
import io
import os
import platform
import random
import sys
import tempfile
import time
import tracemalloc

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)
import main as m  # noqa: E402


def make_quizzes(n):
    """측정용 퀴즈 n개를 만든다."""
    return [
        m.Quiz(f"문제 {i}: 파이썬 기초 개념 확인 문장입니다?",
               [f"선택지 {i}-{j} 내용" for j in range(1, 5)],
               (i % 4) + 1,
               f"힌트 {i}")
        for i in range(n)
    ]


def best_ms(fn, repeat=3):
    """fn을 repeat번 실행해 가장 빠른 시간을 밀리초로 돌려준다."""
    best = float("inf")
    for _ in range(repeat):
        start = time.perf_counter()
        fn()
        best = min(best, time.perf_counter() - start)
    return best * 1000


def main():
    os.chdir(tempfile.mkdtemp())   # 내 state.json을 덮어쓰지 않도록 임시 폴더에서 실행
    print(f"Python {platform.python_version()} / {platform.system()}")
    print("| 퀴즈 수 | 저장(ms) | 불러오기(ms) | 파일 크기(KB) | 메모리(KB) | 랜덤 10개(ms) | 목록 출력(ms) | 문제 검색: 리스트(ms) | 문제 검색: dict(ms) |")
    print("|---|---|---|---|---|---|---|---|---|")
    for n in (1000, 10000, 100000):
        with contextlib.redirect_stdout(io.StringIO()):
            game = m.QuizGame()

        tracemalloc.start()
        quizzes = make_quizzes(n)
        memory, _ = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        game.quizzes, game.best_score, game.history = quizzes, 80, []
        with contextlib.redirect_stdout(io.StringIO()):
            save_ms = best_ms(game.save)
            load_ms = best_ms(lambda: game.read_state(m.STATE_FILE))
            list_ms = best_ms(game.show_quiz_list)
        size_kb = os.path.getsize(m.STATE_FILE) / 1024

        sample_ms = best_ms(lambda: random.sample(game.quizzes, 10), 5)
        target = quizzes[-1].question
        list_search_ms = best_ms(lambda: next(q for q in game.quizzes if q.question == target), 5)
        index = {q.question: q for q in game.quizzes}
        dict_search_ms = best_ms(lambda: index[target], 5)

        print(f"| {n:,} | {save_ms:.1f} | {load_ms:.1f} | {size_kb:,.0f} | {memory / 1024:,.0f} | "
              f"{sample_ms:.3f} | {list_ms:.1f} | {list_search_ms:.2f} | {dict_search_ms:.4f} |")


if __name__ == "__main__":
    main()

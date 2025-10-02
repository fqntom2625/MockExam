#Project by : Brian Lee
#2025.10.01
#Project Purpose : 학원의 월별 테스트 채점을 편하게 하기 위한 툴
# ==== 모의고사 영어 채점기 (LC 1~17, RC 18~45) ====

N_TOTAL = 45
N_LC = 17           # 1~17
N_RC = N_TOTAL - N_LC  # 28 (18~45)
DEFAULT_POINT = 2.0 # 기본 배점

# ====== 정답 키 & 3점 문항 설정 ======
ANSWER_KEY = [
    "4","1","5","5","2","4","2","4","4","2",
    "1","5","1","1","1","2","4",   # 1~17 LC
    "3","3","2","1","3","2","2","5","3","3",
    "5","2","5","1","3","1","2","4","2","3",
    "5","5","3","3","3","5","4","4"          # 18~45 RC
]

THREE_POINT = {6, 13, 14, 29, 32, 33, 34, 35, 39, 42}  # 3점 문항 번호

# =====================================

def _validate_key():
    if len(ANSWER_KEY) != N_TOTAL:
        raise ValueError(f"정답 개수 {len(ANSWER_KEY)}개 → 45개 필요")
    for i, v in enumerate(ANSWER_KEY, start=1):
        if v not in {"1","2","3","4","5"}:
            raise ValueError(f"{i}번 정답 '{v}' → '1'~'5'만 허용")

def _build_weights():
    return [3.0 if (i+1) in THREE_POINT else DEFAULT_POINT for i in range(N_TOTAL)]

def _parse_answers_group(raw, need_len):
    """
    그룹 입력 파싱:
    - 허용: "1"~"5" (선택지), "6"(무효 처리용)
    - 공백/쉼표/붙여쓰기 모두 가능
    """
    s = raw.strip()
    if "," in s or " " in s:
        tokens = [t for t in s.replace(",", " ").split() if t]
    else:
        tokens = list(s)

    cleaned = []
    for t in tokens:
        if t not in {"1","2","3","4","5","6"}:
            return None
        cleaned.append(t)

    if len(cleaned) != need_len:
        return None
    return cleaned

def _score_section(ans_key, stu_ans, weights, start_idx, end_idx):
    score = 0.0
    got = 0
    wrong_nums = []
    for i in range(start_idx, end_idx):
        qnum = i + 1
        if stu_ans[i] == "6":   # 무효 답안
            wrong_nums.append(qnum)
        elif stu_ans[i] == ans_key[i]:
            got += 1
            score += weights[i]
        else:
            wrong_nums.append(qnum)
    total_q = end_idx - start_idx
    return score, got, total_q, wrong_nums

def _fmt(x):
    return int(x) if abs(x - int(x)) < 1e-9 else round(x, 1)

def _max_scores(weights):
    lc_max = sum(weights[:N_LC])
    rc_max = sum(weights[N_LC:])
    return lc_max, rc_max, lc_max + rc_max

def main():
    print("=== 모의고사 영어 채점기 === (종료: q)")
    print("- 총 45문항 (LC 1~17, RC 18~45)")
    print("- 입력 방법: 5문제씩 끊어서 9번 입력")
    print("  예시) 1~5번 → 4 1 5 5 2")
    print("- 허용 값: 1~5 (정답 선택), 6 = 무효 답안(빈칸/두개 답)")

    try:
        _validate_key()
    except ValueError as e:
        print("⚠️ 정답/배점 오류:", e)
        return

    weights = _build_weights()
    lc_max, rc_max, total_max = _max_scores(weights)

    while True:
        print("\n학생 답안 입력 시작 (종료: q)")
        all_answers = []
        valid = True
        for group in range(9):  # 45문항 / 5문항씩 = 9회 입력
            start_q = group * 5 + 1
            end_q = start_q + 4
            raw = input(f"{start_q}~{end_q}번 답안 입력(5개): ").strip()
            if raw.lower() in {"q", "quit", "exit"}:
                print("채점 종료")
                return
            parsed = _parse_answers_group(raw, 5)
            if parsed is None:
                print("❗ 형식 오류: 1~6만 사용, 정확히 5개 입력 필요")
                valid = False
                break
            all_answers.extend(parsed)

        if not valid:
            continue  # 다시 입력 받음

        stu = all_answers

        # 채점
        lc_score, lc_got, lc_total, lc_wrong = _score_section(ANSWER_KEY, stu, weights, 0, N_LC)
        rc_score, rc_got, rc_total, rc_wrong = _score_section(ANSWER_KEY, stu, weights, N_LC, N_TOTAL)
        total = lc_score + rc_score

        print("\n[결과]")
        print(f"LC: {_fmt(lc_score)}/{_fmt(lc_max)} (맞힌 개수: {lc_got}/{lc_total})")
        print(f"RC: {_fmt(rc_score)}/{_fmt(rc_max)} (맞힌 개수: {rc_got}/{rc_total})")
        print(f"총점: {_fmt(total)}/{_fmt(total_max)}")

        if lc_wrong or rc_wrong:
            print("- 오답/무효 번호")
            if lc_wrong:
                print(f"  LC(1~17): {', '.join(map(str, lc_wrong))}")
            if rc_wrong:
                print(f"  RC(18~45): {', '.join(map(str, rc_wrong))}")

if __name__ == "__main__":
    main()

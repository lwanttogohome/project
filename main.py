import streamlit as st
import re


# ============================================================
# 1. 페이지 설정
# ============================================================

st.set_page_config(
    page_title="비밀번호 안전도 검사기",
    page_icon="🔐",
    layout="centered"
)


# ============================================================
# 2. 무채색 기반 디자인
# ============================================================

st.markdown(
    """
    <style>

    /* 전체 배경 */
    .stApp {
        background-color: #101010;
        color: #eeeeee;
    }

    /* 전체 기본 글자 */
    html, body, [class*="css"] {
        color: #eeeeee;
    }

    /* 제목 */
    h1 {
        color: #f5f5f5 !important;
        font-weight: 700 !important;
        letter-spacing: -1px;
    }

    h2, h3 {
        color: #dddddd !important;
        font-weight: 600 !important;
    }

    /* 일반 텍스트 */
    p {
        color: #bdbdbd;
    }

    /* 구분선 */
    hr {
        border-color: #303030 !important;
    }

    /* 입력창 */
    div[data-baseweb="input"] {
        background-color: #181818 !important;
        border: 1px solid #383838 !important;
        border-radius: 8px !important;
    }

    div[data-baseweb="input"]:focus-within {
        border-color: #777777 !important;
        box-shadow: none !important;
    }

    input {
        color: #eeeeee !important;
        background-color: #181818 !important;
    }

    /* 입력창 placeholder */
    input::placeholder {
        color: #666666 !important;
    }

    /* 일반적인 카드 느낌 */
    .result-card {
        background-color: #181818;
        border: 1px solid #303030;
        border-radius: 10px;
        padding: 22px;
        margin-top: 15px;
        margin-bottom: 15px;
    }

    /* 안전도 결과 */
    .security-result {
        background-color: #181818;
        border: 1px solid #303030;
        border-radius: 10px;
        padding: 30px;
        text-align: center;
        margin-top: 20px;
        margin-bottom: 20px;
    }

    .security-title {
        color: #888888;
        font-size: 14px;
        margin-bottom: 8px;
    }

    .security-score {
        color: #eeeeee;
        font-size: 16px;
        margin-top: 10px;
    }

    /* 검사 항목 */
    .check-item {
        background-color: #181818;
        border: 1px solid #2d2d2d;
        border-radius: 8px;
        padding: 13px 16px;
        margin-bottom: 8px;
        color: #cccccc;
    }

    /* 장점 */
    .good-item {
        color: #bdbdbd;
        padding: 6px 0;
    }

    /* 경고 */
    .warning-item {
        color: #bdbdbd;
        padding: 6px 0;
    }

    /* 하단 안내 */
    .footer-text {
        color: #666666;
        font-size: 12px;
        text-align: center;
        margin-top: 25px;
    }

    /* Streamlit 기본 alert */
    div[data-testid="stAlert"] {
        background-color: #181818 !important;
        border: 1px solid #333333 !important;
        color: #cccccc !important;
    }

    /* 버튼 */
    .stButton > button {
        background-color: #202020 !important;
        color: #dddddd !important;
        border: 1px solid #3a3a3a !important;
        border-radius: 8px !important;
    }

    .stButton > button:hover {
        background-color: #292929 !important;
        border-color: #555555 !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# 3. 제목
# ============================================================

st.title("🔐 비밀번호 안전도 검사기")

st.write(
    "비밀번호의 길이와 문자 종류 등을 확인하여 "
    "기본적인 안전도를 검사합니다."
)

st.caption(
    "실제로 사용하는 비밀번호 대신 테스트용 비밀번호를 입력하세요."
)


# ============================================================
# 4. 비밀번호 입력
# ============================================================

password = st.text_input(
    "비밀번호",
    type="password",
    placeholder="테스트용 비밀번호를 입력하세요"
)


# ============================================================
# 5. 비밀번호 검사 함수
# ============================================================

def check_password(password):
    """
    비밀번호의 여러 가지 특징을 검사합니다.

    검사하는 항목:
    - 길이
    - 대문자
    - 소문자
    - 숫자
    - 특수문자
    - 반복 문자
    - 흔한 비밀번호
    """

    result = {}

    # 비밀번호 길이
    result["length"] = len(password)

    # 대문자 포함 여부
    result["uppercase"] = bool(
        re.search(r"[A-Z]", password)
    )

    # 소문자 포함 여부
    result["lowercase"] = bool(
        re.search(r"[a-z]", password)
    )

    # 숫자 포함 여부
    result["number"] = bool(
        re.search(r"[0-9]", password)
    )

    # 특수문자 포함 여부
    result["special"] = bool(
        re.search(r"[^A-Za-z0-9]", password)
    )

    # 같은 문자가 3번 이상 연속되는지 검사
    result["repeated"] = bool(
        re.search(r"(.)\1\1", password)
    )

    # 매우 흔한 비밀번호 목록
    common_passwords = [
        "123456",
        "12345678",
        "123456789",
        "password",
        "qwerty",
        "abc123",
        "111111",
        "000000",
        "admin",
        "letmein"
    ]

    result["common"] = (
        password.lower() in common_passwords
    )

    return result


# ============================================================
# 6. 비밀번호가 입력되었을 때
# ============================================================

if password:

    result = check_password(password)

    score = 0

    warnings = []

    advantages = []


    # ========================================================
    # 7. 길이 검사
    # ========================================================

    if result["length"] >= 12:

        score += 2

        advantages.append(
            "12자 이상입니다."
        )

    elif result["length"] >= 8:

        score += 1

        advantages.append(
            "8자 이상입니다."
        )

    else:

        warnings.append(
            "비밀번호가 너무 짧습니다. 8자 이상을 권장합니다."
        )


    # ========================================================
    # 8. 대문자 검사
    # ========================================================

    if result["uppercase"]:

        score += 1

        advantages.append(
            "대문자가 포함되어 있습니다."
        )

    else:

        warnings.append(
            "대문자를 추가해 보세요."
        )


    # ========================================================
    # 9. 소문자 검사
    # ========================================================

    if result["lowercase"]:

        score += 1

        advantages.append(
            "소문자가 포함되어 있습니다."
        )

    else:

        warnings.append(
            "소문자를 추가해 보세요."
        )


    # ========================================================
    # 10. 숫자 검사
    # ========================================================

    if result["number"]:

        score += 1

        advantages.append(
            "숫자가 포함되어 있습니다."
        )

    else:

        warnings.append(
            "숫자를 추가해 보세요."
        )


    # ========================================================
    # 11. 특수문자 검사
    # ========================================================

    if result["special"]:

        score += 1

        advantages.append(
            "특수문자가 포함되어 있습니다."
        )

    else:

        warnings.append(
            "!, @, #, $ 등의 특수문자를 추가해 보세요."
        )


    # ========================================================
    # 12. 반복 문자 검사
    # ========================================================

    if result["repeated"]:

        score -= 1

        warnings.append(
            "같은 문자가 3번 이상 연속으로 사용되었습니다."
        )


    # ========================================================
    # 13. 흔한 비밀번호 검사
    # ========================================================

    if result["common"]:

        score -= 3

        warnings.append(
            "너무 흔하게 사용되는 비밀번호입니다."
        )


    # ========================================================
    # 14. 점수 범위 조정
    # ========================================================

    score = max(0, min(score, 6))


    # ========================================================
    # 15. 안전도 결정
    # ========================================================

    if result["common"]:

        level = "매우 위험"
        icon = "🚨"
        level_color = "#ff4b4b"

    elif score <= 2:

        level = "약함"
        icon = "●"
        level_color = "#ff4b4b"

    elif score <= 4:

        level = "보통"
        icon = "●"
        level_color = "#d9a441"

    else:

        level = "강함"
        icon = "●"
        level_color = "#54b86b"


    # ========================================================
    # 16. 결과 영역
    # ========================================================

    st.divider()

    st.subheader("검사 결과")


    st.markdown(
        f"""
        <div class="security-result">

            <div class="security-title">
                PASSWORD SECURITY
            </div>

            <div style="
                color:{level_color};
                font-size:34px;
                font-weight:700;
                margin-top:8px;
            ">
                {icon} {level}
            </div>

            <div class="security-score">
                안전도 점수&nbsp;&nbsp;
                <strong>{score} / 6</strong>
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # 17. 점수 막대
    # ========================================================

    st.progress(score / 6)


    # ========================================================
    # 18. 검사 항목
    # ========================================================

    st.subheader("검사 항목")

    col1, col2 = st.columns(2)


    # 왼쪽
    with col1:

        if result["length"] >= 8:

            st.markdown(
                f"""
                <div class="check-item">
                    <span style="color:#777777;">✓</span>
                    &nbsp;길이 {result["length"]}자
                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                f"""
                <div class="check-item">
                    <span style="color:#ff4b4b;">✕</span>
                    &nbsp;길이 {result["length"]}자
                </div>
                """,
                unsafe_allow_html=True
            )


        if result["uppercase"]:

            st.markdown(
                """
                <div class="check-item">
                    <span style="color:#777777;">✓</span>
                    &nbsp;대문자 포함
                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                """
                <div class="check-item">
                    <span style="color:#ff4b4b;">✕</span>
                    &nbsp;대문자 없음
                </div>
                """,
                unsafe_allow_html=True
            )


        if result["lowercase"]:

            st.markdown(
                """
                <div class="check-item">
                    <span style="color:#777777;">✓</span>
                    &nbsp;소문자 포함
                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                """
                <div class="check-item">
                    <span style="color:#ff4b4b;">✕</span>
                    &nbsp;소문자 없음
                </div>
                """,
                unsafe_allow_html=True
            )


    # 오른쪽
    with col2:

        if result["number"]:

            st.markdown(
                """
                <div class="check-item">
                    <span style="color:#777777;">✓</span>
                    &nbsp;숫자 포함
                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                """
                <div class="check-item">
                    <span style="color:#ff4b4b;">✕</span>
                    &nbsp;숫자 없음
                </div>
                """,
                unsafe_allow_html=True
            )


        if result["special"]:

            st.markdown(
                """
                <div class="check-item">
                    <span style="color:#777777;">✓</span>
                    &nbsp;특수문자 포함
                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                """
                <div class="check-item">
                    <span style="color:#ff4b4b;">✕</span>
                    &nbsp;특수문자 없음
                </div>
                """,
                unsafe_allow_html=True
            )


        if result["repeated"]:

            st.markdown(
                """
                <div class="check-item">
                    <span style="color:#ff4b4b;">✕</span>
                    &nbsp;반복 문자 발견
                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                """
                <div class="check-item">
                    <span style="color:#777777;">✓</span>
                    &nbsp;반복 문자 없음
                </div>
                """,
                unsafe_allow_html=True
            )


    # ========================================================
    # 19. 잘한 점
    # ========================================================

    if advantages:

        st.subheader("좋은 점")

        for item in advantages:

            st.markdown(
                f"""
                <div class="good-item">
                    ✓ &nbsp;{item}
                </div>
                """,
                unsafe_allow_html=True
            )


    # ========================================================
    # 20. 개선할 점
    # ========================================================

    if warnings:

        st.subheader("개선할 점")

        for item in warnings:

            st.markdown(
                f"""
                <div class="warning-item">
                    <span style="color:#d9a441;">!</span>
                    &nbsp;{item}
                </div>
                """,
                unsafe_allow_html=True
            )

    else:

        st.success(
            "기본적인 안전도 검사 기준을 모두 만족했습니다."
        )


# ============================================================
# 21. 비밀번호가 입력되지 않았을 때
# ============================================================

else:

    st.markdown(
        """
        <div class="result-card">

            <div style="
                color:#777777;
                font-size:14px;
                margin-bottom:8px;
            ">
                PASSWORD CHECKER
            </div>

            <div style="
                color:#aaaaaa;
                font-size:15px;
            ">
                테스트용 비밀번호를 입력하면
                안전도를 확인할 수 있습니다.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# 22. 하단 안내
# ============================================================

st.markdown(
    """
    <div class="footer-text">
        입력된 비밀번호는 이 앱에서 별도로 저장하지 않습니다.<br>
        실제 비밀번호 대신 테스트용 비밀번호를 사용하세요.
    </div>
    """,
    unsafe_allow_html=True
)

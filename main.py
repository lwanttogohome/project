import streamlit as st
import re

st.set_page_config(
    page_title="비밀번호 안전도 검사기",
    page_icon="🔐",
    layout="centered"
)

st.markdown(
    """
    <style>
    .stApp {
        background-color: #101010;
        color: #eeeeee;
    }

    h1, h2, h3 {
        color: #eeeeee !important;
    }

    p {
        color: #bbbbbb;
    }

    hr {
        border-color: #303030 !important;
    }

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

    input::placeholder {
        color: #666666 !important;
    }

    div[data-testid="stAlert"] {
        background-color: #181818 !important;
        border: 1px solid #333333 !important;
    }

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

st.title("🔐 비밀번호 안전도 검사기")

st.write(
    "비밀번호를 여러 가지 기준으로 분석하여 안전도를 확인합니다."
)

st.caption(
    "실제 사용하는 비밀번호 대신 테스트용 비밀번호를 입력하세요."
)

password = st.text_input(
    "비밀번호",
    type="password",
    placeholder="테스트용 비밀번호를 입력하세요"
)


def check_password(password):
    checks = []

    length = len(password)

    has_upper = bool(re.search(r"[A-Z]", password))
    has_lower = bool(re.search(r"[a-z]", password))
    has_number = bool(re.search(r"[0-9]", password))
    has_special = bool(re.search(r"[^A-Za-z0-9]", password))

    checks.append({
        "name": "8자 이상",
        "ok": length >= 8,
        "help": "비밀번호는 최소 8자 이상을 권장합니다."
    })

    checks.append({
        "name": "12자 이상",
        "ok": length >= 12,
        "help": "12자 이상이면 더 긴 비밀번호가 됩니다."
    })

    checks.append({
        "name": "16자 이상",
        "ok": length >= 16,
        "help": "16자 이상이면 충분히 긴 비밀번호입니다."
    })

    checks.append({
        "name": "대문자 포함",
        "ok": has_upper,
        "help": "A~Z 중 하나 이상을 포함하세요."
    })

    checks.append({
        "name": "소문자 포함",
        "ok": has_lower,
        "help": "a~z 중 하나 이상을 포함하세요."
    })

    checks.append({
        "name": "숫자 포함",
        "ok": has_number,
        "help": "0~9 중 하나 이상을 포함하세요."
    })

    checks.append({
        "name": "특수문자 포함",
        "ok": has_special,
        "help": "!, @, #, $, % 등의 특수문자를 사용하세요."
    })

    checks.append({
        "name": "대문자와 소문자 혼합",
        "ok": has_upper and has_lower,
        "help": "대문자와 소문자를 함께 사용하는 것이 좋습니다."
    })

    checks.append({
        "name": "문자와 숫자 혼합",
        "ok": (has_upper or has_lower) and has_number,
        "help": "문자와 숫자를 함께 사용하세요."
    })

    checks.append({
        "name": "문자·숫자·특수문자 혼합",
        "ok": (
            (has_upper or has_lower)
            and has_number
            and has_special
        ),
        "help": "문자, 숫자, 특수문자를 함께 사용하세요."
    })

    repeated = bool(re.search(r"(.)\1\1", password))

    checks.append({
        "name": "같은 문자 3번 연속 사용 안 함",
        "ok": not repeated,
        "help": "aaa, 111, !!!처럼 같은 문자를 반복하지 마세요."
    })

    repeated_number = bool(re.search(r"([0-9])\1\1", password))

    checks.append({
        "name": "같은 숫자 3번 연속 사용 안 함",
        "ok": not repeated_number,
        "help": "111, 222, 333 같은 패턴을 피하세요."
    })

    sequential_numbers = [
        "0123", "1234", "2345", "3456",
        "4567", "5678", "6789",
        "9876", "8765", "7654",
        "6543", "5432", "4321", "3210"
    ]

    has_sequential_number = any(
        pattern in password
        for pattern in sequential_numbers
    )

    checks.append({
        "name": "연속된 숫자 패턴 없음",
        "ok": not has_sequential_number,
        "help": "1234, 4567 같은 연속 숫자를 피하세요."
    })

    sequential_letters = [
        "abcd", "bcde", "cdef", "defg",
        "efgh", "fghi", "ghij", "hijk",
        "ijkl", "jklm", "klmn", "lmno",
        "mnop", "nopq", "opqr", "pqrs",
        "qrst", "rstu", "stuv", "tuvw",
        "uvwx", "vwxy", "wxyz"
    ]

    password_lower = password.lower()

    has_sequential_letter = any(
        pattern in password_lower
        for pattern in sequential_letters
    )

    checks.append({
        "name": "연속된 문자 패턴 없음",
        "ok": not has_sequential_letter,
        "help": "abcd, efgh 같은 연속 문자를 피하세요."
    })

    keyboard_patterns = [
        "qwerty",
        "asdfgh",
        "zxcvbn",
        "qwert",
        "asdf",
        "zxcv"
    ]

    has_keyboard_pattern = any(
        pattern in password_lower
        for pattern in keyboard_patterns
    )

    checks.append({
        "name": "키보드 패턴 없음",
        "ok": not has_keyboard_pattern,
        "help": "qwerty, asdfgh 같은 키보드 배열을 피하세요."
    })

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
        "letmein",
        "welcome",
        "iloveyou"
    ]

    is_common = password_lower in common_passwords

    checks.append({
        "name": "흔한 비밀번호가 아님",
        "ok": not is_common,
        "help": "인터넷에서 흔하게 사용되는 비밀번호는 피하세요."
    })

    has_password_word = "password" in password_lower

    checks.append({
        "name": "'password' 단어 사용 안 함",
        "ok": not has_password_word,
        "help": "password 같은 매우 흔한 단어를 피하세요."
    })

    has_admin_word = "admin" in password_lower

    checks.append({
        "name": "'admin' 단어 사용 안 함",
        "ok": not has_admin_word,
        "help": "admin 같은 관리자 관련 단어를 피하세요."
    })

    has_space = " " in password

    checks.append({
        "name": "불필요한 공백 없음",
        "ok": not has_space,
        "help": "실수로 들어간 공백을 확인하세요."
    })

    only_numbers = password.isdigit()

    checks.append({
        "name": "숫자만으로 구성되지 않음",
        "ok": not only_numbers,
        "help": "123456 같은 숫자만으로 된 비밀번호는 피하세요."
    })

    return checks


if password:

    checks = check_password(password)

    passed = sum(
        1 for check in checks
        if check["ok"]
    )

    total = len(checks)

    if passed <= 7:
        level = "매우 위험"
    elif passed <= 11:
        level = "약함"
    elif passed <= 15:
        level = "보통"
    elif passed <= 18:
        level = "강함"
    else:
        level = "매우 강함"

    st.divider()
    st.subheader("검사 결과")

    if level == "매우 위험":
        st.error("🚨 매우 위험")
    elif level == "약함":
        st.error("🔴 약함")
    elif level == "보통":
        st.warning("🟡 보통")
    elif level == "강함":
        st.success("🟢 강함")
    else:
        st.success("🟢 매우 강함")

    st.write(f"검사 통과: **{passed} / {total}개**")

    st.progress(passed / total)

    st.subheader("🔎 세부 검사 항목")

    col1, col2 = st.columns(2)

    for index, check in enumerate(checks):

        if index % 2 == 0:
            with col1:
                if check["ok"]:
                    st.success(
                        f"✓ {index + 1}. {check['name']}"
                    )
                else:
                    st.error(
                        f"✕ {index + 1}. {check['name']}"
                    )
        else:
            with col2:
                if check["ok"]:
                    st.success(
                        f"✓ {index + 1}. {check['name']}"
                    )
                else:
                    st.error(
                        f"✕ {index + 1}. {check['name']}"
                    )

    passed_checks = [
        check for check in checks
        if check["ok"]
    ]

    if passed_checks:
        st.subheader("✓ 잘한 점")

        for check in passed_checks:
            st.write(f"✓ {check['name']}")

    failed_checks = [
        check for check in checks
        if not check["ok"]
    ]

    if failed_checks:
        st.subheader("⚠️ 개선할 점")

        for check in failed_checks:
            st.write(
                f"⚠️ {check['name']} — {check['help']}"
            )
    else:
        st.success(
            "🎉 20개 검사 항목을 모두 통과했습니다!"
        )

else:

    st.info(
        "👆 위에 테스트용 비밀번호를 입력하면 "
        "20가지 기준으로 안전도를 검사합니다."
    )

    st.subheader("검사하는 항목")

    items = [
        "① 길이 8자 이상",
        "② 길이 12자 이상",
        "③ 길이 16자 이상",
        "④ 대문자 포함",
        "⑤ 소문자 포함",
        "⑥ 숫자 포함",
        "⑦ 특수문자 포함",
        "⑧ 대문자와 소문자 혼합",
        "⑨ 문자와 숫자 혼합",
        "⑩ 문자·숫자·특수문자 혼합",
        "⑪ 같은 문자 3번 연속 사용 안 함",
        "⑫ 같은 숫자 3번 연속 사용 안 함",
        "⑬ 연속된 숫자 패턴 없음",
        "⑭ 연속된 문자 패턴 없음",
        "⑮ 키보드 패턴 없음",
        "⑯ 흔한 비밀번호가 아님",
        "⑰ password 단어 사용 안 함",
        "⑱ admin 단어 사용 안 함",
        "⑲ 불필요한 공백 없음",
        "⑳ 숫자만으로 구성되지 않음"
    ]

    for item in items:
        st.write(item)

st.divider()

st.caption(
    "🔒 입력한 비밀번호는 이 앱에서 별도로 저장하지 않습니다."
)

st.caption(
    "※ 이 검사는 기본적인 규칙을 이용한 간단한 검사입니다."
)

st.caption(
    "※ 실제 비밀번호 대신 테스트용 비밀번호를 사용하세요."
)

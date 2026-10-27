import streamlit as st
import re


# --------------------------------------------------
# 1. 페이지 설정
# --------------------------------------------------

st.set_page_config(
    page_title="비밀번호 안전도 검사기",
    page_icon="🔐",
    layout="centered"
)


# --------------------------------------------------
# 2. 제목
# --------------------------------------------------

st.title("🔐 비밀번호 안전도 검사기")

st.write(
    "비밀번호를 입력하면 길이와 문자 종류 등을 확인하여 "
    "안전도를 간단하게 검사해 줍니다."
)

st.warning(
    "⚠️ 실제로 사용하는 비밀번호는 입력하지 마세요. "
    "테스트용 비밀번호를 사용하세요."
)


# --------------------------------------------------
# 3. 비밀번호 입력
# --------------------------------------------------

password = st.text_input(
    "비밀번호를 입력하세요.",
    type="password",
    placeholder="테스트용 비밀번호를 입력하세요"
)


# --------------------------------------------------
# 4. 비밀번호 검사 함수
# --------------------------------------------------

def check_password(password):
    """
    입력한 비밀번호의 여러 조건을 검사합니다.

    검사 항목
    1. 길이
    2. 대문자
    3. 소문자
    4. 숫자
    5. 특수문자
    6. 반복되는 문자
    7. 흔히 사용하는 단순한 비밀번호
    """

    result = {}

    # 비밀번호 길이
    result["length"] = len(password)

    # 대문자가 포함되어 있는지
    result["uppercase"] = bool(re.search(r"[A-Z]", password))

    # 소문자가 포함되어 있는지
    result["lowercase"] = bool(re.search(r"[a-z]", password))

    # 숫자가 포함되어 있는지
    result["number"] = bool(re.search(r"[0-9]", password))

    # 특수문자가 포함되어 있는지
    result["special"] = bool(
        re.search(r"[^A-Za-z0-9]", password)
    )

    # 같은 문자가 3번 이상 연속되는지 확인
    result["repeated"] = bool(
        re.search(r"(.)\1\1", password)
    )

    # 매우 흔하게 사용하는 단순한 비밀번호
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

    result["common"] = password.lower() in common_passwords

    return result


# --------------------------------------------------
# 5. 비밀번호가 입력되었을 때 검사
# --------------------------------------------------

if password:

    result = check_password(password)

    score = 0
    warnings = []
    advantages = []


    # --------------------------------------------------
    # 길이 점수
    # --------------------------------------------------

    if result["length"] >= 12:
        score += 2
        advantages.append("12자 이상입니다.")

    elif result["length"] >= 8:
        score += 1
        advantages.append("8자 이상입니다.")

    else:
        warnings.append("비밀번호가 너무 짧습니다. 8자 이상을 권장합니다.")


    # --------------------------------------------------
    # 대문자
    # --------------------------------------------------

    if result["uppercase"]:
        score += 1
        advantages.append("대문자가 포함되어 있습니다.")

    else:
        warnings.append("대문자를 추가해 보세요.")


    # --------------------------------------------------
    # 소문자
    # --------------------------------------------------

    if result["lowercase"]:
        score += 1
        advantages.append("소문자가 포함되어 있습니다.")

    else:
        warnings.append("소문자를 추가해 보세요.")


    # --------------------------------------------------
    # 숫자
    # --------------------------------------------------

    if result["number"]:
        score += 1
        advantages.append("숫자가 포함되어 있습니다.")

    else:
        warnings.append("숫자를 추가해 보세요.")


    # --------------------------------------------------
    # 특수문자
    # --------------------------------------------------

    if result["special"]:
        score += 1
        advantages.append("특수문자가 포함되어 있습니다.")

    else:
        warnings.append("!, @, #, $ 같은 특수문자를 추가해 보세요.")


    # --------------------------------------------------
    # 반복 문자
    # --------------------------------------------------

    if result["repeated"]:
        score -= 1
        warnings.append(
            "같은 문자가 3번 이상 연속해서 사용되었습니다."
        )


    # --------------------------------------------------
    # 흔한 비밀번호
    # --------------------------------------------------

    if result["common"]:
        score -= 3
        warnings.append(
            "너무 흔하게 사용되는 비밀번호입니다."
        )


    # --------------------------------------------------
    # 점수를 0~6 범위로 제한
    # --------------------------------------------------

    score = max(0, min(score, 6))


    # --------------------------------------------------
    # 안전도 결정
    # --------------------------------------------------

    if result["common"]:
        level = "매우 위험"
        level_icon = "🚨"

    elif score <= 2:
        level = "약함"
        level_icon = "🔴"

    elif score <= 4:
        level = "보통"
        level_icon = "🟡"

    else:
        level = "강함"
        level_icon = "🟢"


    # --------------------------------------------------
    # 결과 표시
    # --------------------------------------------------

    st.divider()

    st.subheader("📊 검사 결과")


    # 안전도 크게 표시
    st.markdown(
        f"# {level_icon} {level}"
    )


    # 점수 표시
    st.progress(
        score / 6
    )

    st.write(
        f"안전도 점수: **{score} / 6**"
    )


    # --------------------------------------------------
    # 검사 항목 표시
    # --------------------------------------------------

    st.subheader("🔎 검사 항목")

    col1, col2 = st.columns(2)


    with col1:

        if result["length"] >= 8:
            st.success(
                f"✅ 길이: {result['length']}자"
            )
        else:
            st.error(
                f"❌ 길이: {result['length']}자"
            )


        if result["uppercase"]:
            st.success("✅ 대문자 포함")
        else:
            st.error("❌ 대문자 없음")


        if result["lowercase"]:
            st.success("✅ 소문자 포함")
        else:
            st.error("❌ 소문자 없음")


    with col2:

        if result["number"]:
            st.success("✅ 숫자 포함")
        else:
            st.error("❌ 숫자 없음")


        if result["special"]:
            st.success("✅ 특수문자 포함")
        else:
            st.error("❌ 특수문자 없음")


        if result["repeated"]:
            st.error("❌ 같은 문자 반복")
        else:
            st.success("✅ 반복 문자 없음")


    # --------------------------------------------------
    # 잘한 점
    # --------------------------------------------------

    if advantages:

        st.subheader("👍 잘한 점")

        for item in advantages:
            st.write(f"• {item}")


    # --------------------------------------------------
    # 개선할 점
    # --------------------------------------------------

    if warnings:

        st.subheader("💡 개선하면 좋은 점")

        for item in warnings:
            st.write(f"• {item}")

    else:

        st.success(
            "🎉 기본적인 안전도 검사 기준을 모두 만족했습니다!"
        )


# --------------------------------------------------
# 6. 입력하지 않았을 때
# --------------------------------------------------

else:

    st.info(
        "👆 위에 테스트용 비밀번호를 입력하면 안전도를 검사합니다."
    )


# --------------------------------------------------
# 7. 안내
# --------------------------------------------------

st.divider()

st.caption(
    "🔒 이 앱은 입력된 비밀번호를 저장하거나 공개하지 않습니다."
)

st.caption(
    "※ 실제 비밀번호의 안전성을 완벽하게 판단하는 프로그램은 아닙니다."
)

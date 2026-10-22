
import streamlit as st

st.set_page_config(
    page_title="Anna | SOC Mentor AI",
    page_icon="🛡️",
    layout="centered",
)

st.title("🛡️ Anna — SOC Mentor AI")
st.caption("Your personal cybersecurity investigation trainer")

st.write(
    "Welcome! Investigate fictional security incidents, "
    "examine evidence, and develop your SOC analyst skills."
)

language = st.selectbox(
    "Explanation language",
    ["English", "Русский", "한국어"],
)

st.divider()

st.header("SOC Lab — Case 001")
st.subheader("Alert: Multiple failed logins")

st.info(
    """
    **Target account:** admin

    **Source IP:** 203.0.113.45

    **Failed attempts:** 18

    **Time window:** 2 minutes

    **Environment:** Simulated training data
    """
)

st.write(
    "Question 1: What would you investigate first?"
)

answer = st.radio(
    "Choose your first action:",
    [
        "A. Ignore the alert.",
        "B. Review authentication logs and check for successful logins.",
        "C. Declare the account compromised immediately.",
        "D. Delete the authentication logs.",
    ],
    index=None,
)

reason = st.text_area(
    "Explain your reasoning (optional):",
    placeholder="I would investigate this because...",
)

if st.button("Submit investigation", type="primary"):
    if answer is None:
        st.warning("Please select an answer first.")
    else:
        st.subheader("Anna's evaluation")

        if answer.startswith("B."):
            st.success("Good decision! Score: 9/10")
            feedback = {
                "English": (
                    "Authentication logs can show whether any "
                    "login succeeded, which account was targeted, "
                    "and when the events occurred. Next, investigate "
                    "the source context and whether the activity "
                    "was legitimate. A failed-login alert alone "
                    "does not prove a compromise."
                ),
                "Русский": (
                    "Журналы аутентификации помогут выяснить, "
                    "был ли успешный вход, какая учётная запись "
                    "подверглась атаке и когда произошли события. "
                    "Затем проверьте источник входа и его "
                    "легитимность. Одни неудачные попытки "
                    "не доказывают компрометацию."
                ),
                "한국어": (
                    "인증 로그를 통해 로그인 성공 여부, 공격 대상 "
                    "계정 및 발생 시간을 확인할 수 있습니다. "
                    "다음으로 접속 출처와 활동의 정상 여부를 "
                    "조사하세요. 로그인 실패 경보만으로 계정 "
                    "침해를 확정할 수는 없습니다."
                ),
            }
        else:
            st.warning("Not the best first step. Score: 3/10")
            feedback = {
                "English": (
                    "Start by collecting and reviewing evidence. "
                    "Check authentication logs and determine whether "
                    "any login succeeded. Do not ignore the alert, "
                    "declare a compromise without evidence, or "
                    "delete logs."
                ),
                "Русский": (
                    "Начните со сбора и анализа доказательств. "
                    "Проверьте журналы аутентификации и выясните, "
                    "был ли успешный вход. Не игнорируйте тревогу, "
                    "не объявляйте компрометацию без доказательств "
                    "и не удаляйте журналы."
                ),
                "한국어": (
                    "먼저 증거를 수집하고 분석하세요. 인증 로그를 "
                    "확인하여 로그인 성공 여부를 파악해야 합니다. "
                    "경보를 무시하거나 증거 없이 계정 침해를 "
                    "단정하거나 로그를 삭제해서는 안 됩니다."
                ),
            }

        st.write(feedback[language])

        if reason.strip():
            st.caption(
                "Your reasoning: " + reason.strip()
            )

        st.info(
            "Next learning goal: determine whether the activity "
            "was legitimate and assess the risk before recommending "
            "a response."
        )

st.divider()
st.caption(
    "Anna v0.1 | Educational simulation | "
    "No real systems are accessed."
)

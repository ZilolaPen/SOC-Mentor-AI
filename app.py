
import streamlit as st

st.set_page_config(
    page_title="Anna | SOC Mentor AI",
    page_icon="🛡️",
    layout="centered",
)

# ---------- Session state ----------
if "stage" not in st.session_state:
    st.session_state.stage = 1

if "score" not in st.session_state:
    st.session_state.score = 0

if "completed" not in st.session_state:
    st.session_state.completed = []

# ---------- App header ----------
st.title("🛡️ Anna — SOC Mentor AI")
st.caption("Your personal cybersecurity investigation trainer")

language = st.selectbox(
    "Explanation language",
    ["English", "Русский", "한국어"],
)

st.divider()

st.caption(
    f"Investigation stage: {st.session_state.stage} / 3"
)
st.progress(st.session_state.stage / 3)

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

# ---------- Evidence for each stage ----------
if st.session_state.stage == 1:
    st.markdown("### Stage 1 — Initial triage")
    st.write(
        "What should you investigate first after "
        "receiving this alert?"
    )

    options = [
        "A. Ignore the alert.",
        "B. Review authentication logs and check for successful logins.",
        "C. Declare the account compromised immediately.",
        "D. Delete the authentication logs.",
    ]

elif st.session_state.stage == 2:
    st.markdown("### Stage 2 — New evidence")
    st.warning(
        """
        **Authentication log results**

        - 03:12:04 — Failed login
        - 03:12:09 — Failed login
        - 03:13:21 — Successful login
        - Source IP: 203.0.113.45
        - Account: admin

        The same source IP had multiple failed attempts,
        followed by a successful login.
        """
    )
    st.write(
        "What should you investigate next?"
    )

    options = [
        "A. Close the alert because a login succeeded.",
        "B. Check whether the login was legitimate and review account activity.",
        "C. Delete the successful-login event.",
        "D. Assume the activity is harmless.",
    ]

else:
    st.markdown("### Stage 3 — Assess the risk")
    st.warning(
        """
        **Additional evidence**

        - The source is unfamiliar for this account.
        - The successful login occurred after repeated failures.
        - Multi-factor authentication (MFA) status is not yet verified.
        """
    )
    st.write(
        "What is the best next investigative action?"
    )

    options = [
        "A. Verify MFA status, review session activity, and contact the account owner through a trusted channel.",
        "B. Block the source and close the case without further investigation.",
        "C. Assume the account is compromised without checking more evidence.",
        "D. Ignore the unfamiliar source.",
    ]

# ---------- Answer form ----------
with st.form(
    key=f"investigation_form_{st.session_state.stage}"
):
    answer = st.radio(
        "Choose your next action:",
        options,
        index=None,
    )

    reason = st.text_area(
        "Explain your reasoning (optional):",
        placeholder="I would investigate this because...",
    )

    submitted = st.form_submit_button(
        "Submit investigation",
        type="primary",
    )

# ---------- Evaluate the answer ----------
if submitted:
    if answer is None:
        st.warning("Please select an answer first.")
    elif st.session_state.stage in st.session_state.completed:
        st.warning(
            "This stage has already been completed. "
            "Continue to the next stage or restart the case."
        )
    else:
        current_stage = st.session_state.stage

        correct_answers = {
            1: "B.",
            2: "B.",
            3: "A.",
        }

        is_correct = answer.startswith(
            correct_answers[current_stage]
        )

        if is_correct:
            st.session_state.score += 1

        st.session_state.completed.append(current_stage)

        st.subheader("Anna's evaluation")

        if current_stage == 1:
            feedback = {
                "English": (
                    "Authentication logs help establish whether "
                    "a login succeeded, which account was targeted, "
                    "and when events occurred. A failed-login alert "
                    "alone does not prove a compromise."
                ),
                "Русский": (
                    "Журналы аутентификации помогают выяснить, "
                    "был ли успешный вход, какая учётная запись "
                    "подверглась атаке и когда произошли события. "
                    "Одни неудачные попытки входа не доказывают взлом."
                ),
                "한국어": (
                    "인증 로그를 통해 로그인 성공 여부, 대상 계정 "
                    "및 발생 시간을 확인할 수 있습니다. 로그인 실패 "
                    "경보만으로 계정 침해를 확정할 수는 없습니다."
                ),
            }
        elif current_stage == 2:
            feedback = {
                "English": (
                    "A successful login after repeated failures "
                    "increases concern, but it does not by itself "
                    "prove compromise. Review account activity, "
                    "login context, and whether the owner recognizes it."
                ),
                "Русский": (
                    "Успешный вход после серии неудачных попыток "
                    "повышает риск, но сам по себе не доказывает взлом. "
                    "Проверьте активность аккаунта, контекст входа "
                    "и подтвердите его у владельца."
                ),
                "한국어": (
                    "반복된 로그인 실패 후 성공한 기록은 위험도를 "
                    "높이지만, 이것만으로 침해를 확정할 수는 없습니다. "
                    "계정 활동과 로그인 맥락을 확인하고 사용자에게 "
                    "정상적인 활동인지 확인하세요."
                ),
            }
        else:
            feedback = {
                "English": (
                    "Verify MFA, review the session and related activity, "
                    "and contact the account owner using a trusted "
                    "channel. Follow your organization's incident "
                    "response procedure if compromise is suspected."
                ),
                "Русский": (
                    "Проверьте MFA, изучите сессию и связанную активность, "
                    "затем свяжитесь с владельцем через доверенный канал. "
                    "При подозрении на компрометацию следуйте процедуре "
                    "реагирования на инциденты вашей организации."
                ),
                "한국어": (
                    "MFA 상태와 세션 및 관련 활동을 확인하고, "
                    "신뢰할 수 있는 채널로 계정 소유자에게 문의하세요. "
                    "침해가 의심되면 조직의 사고 대응 절차를 따르세요."
                ),
            }

        if is_correct:
            st.success("Good decision! +1 point")
        else:
            st.warning(
                "Not the strongest next step. "
                "Review Anna's explanation and try to understand why."
            )

        st.write(feedback[language])

        if reason.strip():
            st.markdown("**Your reasoning**")
            st.write(reason)

        st.metric(
            "Investigation score",
            f"{st.session_state.score} / 3",
        )

        if current_stage < 3:
            st.session_state.stage += 1
            st.info(
                f"Stage {current_stage} completed. "
                f"New evidence is ready for Stage "
                f"{st.session_state.stage}."
            )
            st.rerun()
        else:
            st.success(
                "Case completed! You have finished all "
                "three investigation stages."
            )

# ---------- Controls ----------
st.divider()

left, right = st.columns(2)

with left:
    if st.button("Restart case"):
        st.session_state.stage = 1
        st.session_state.score = 0
        st.session_state.completed = []
        st.rerun()

with right:
    st.caption(
        f"Stages completed: {len(st.session_state.completed)} / 3"
    )

st.divider()
st.caption(
    "Anna v0.2 | Fictional training data | "
    "No real systems are accessed."
)

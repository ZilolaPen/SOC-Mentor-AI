import streamlit as st

from translations import TRANSLATIONS

# Answer IDs stay the same in every language.
CORRECT_ANSWERS = {1: "B", 2: "B", 3: "A"}

# ---------- Session state ----------
for key, default in (("stage", 1), ("score", 0), ("completed", [])):
    if key not in st.session_state:
        st.session_state[key] = default

if "language" not in st.session_state:
    st.session_state.language = "English"

text = TRANSLATIONS[st.session_state.language]
st.set_page_config(page_title=text["title"], page_icon="🛡️", layout="centered")

# The callback runs before the app reruns, so even this selector's label
# and the page title use the newly selected language immediately.
def update_language():
    st.session_state.language = st.session_state.language_picker


st.title(text["title"])
st.caption(text["tagline"])
st.selectbox(
    text["language"],
    list(TRANSLATIONS),
    index=list(TRANSLATIONS).index(st.session_state.language),
    key="language_picker",
    on_change=update_language,
)

st.divider()
st.caption(text["stage_progress"].format(stage=st.session_state.stage))
st.progress(st.session_state.stage / 3)
st.header(text["case_title"])
st.subheader(text["alert_title"])
st.info(text["alert"])

# ---------- Evidence for the current stage ----------
current_stage = st.session_state.stage
stage_text = text["stages"][current_stage]
st.markdown(f"### {stage_text['title']}")
if stage_text["evidence"]:
    st.warning(stage_text["evidence"])
st.write(stage_text["question"])

# ---------- Answer form ----------
# Explicit keys preserve the selected answer and reasoning when the
# displayed labels change after choosing another language.
with st.form(key=f"investigation_form_{current_stage}"):
    answer = st.radio(
        text["choose_action"],
        list(stage_text["options"]),
        format_func=lambda answer_id: f"{answer_id}. {stage_text['options'][answer_id]}",
        index=None,
        key=f"answer_{current_stage}",
    )
    reason = st.text_area(
        text["reason_label"],
        placeholder=text["reason_placeholder"],
        key=f"reason_{current_stage}",
    )
    submitted = st.form_submit_button(text["submit"], type="primary")

# ---------- Evaluate the answer ----------
if submitted:
    if answer is None:
        st.warning(text["select_answer"])
    elif current_stage in st.session_state.completed:
        st.warning(text["already_completed"])
    else:
        is_correct = answer == CORRECT_ANSWERS[current_stage]
        if is_correct:
            st.session_state.score += 1
        st.session_state.completed.append(current_stage)
        st.subheader(text["evaluation"])
        if is_correct:
            st.success(text["correct"])
        else:
            st.warning(text["incorrect"])
        st.write(stage_text["feedback"])
        if reason.strip():
            st.markdown(f"**{text['your_reasoning']}**")
            st.write(reason)
        st.metric(text["score"], f"{st.session_state.score} / 3")
        if current_stage < 3:
            st.session_state.stage += 1
            st.info(text["next_stage"].format(current=current_stage, next=st.session_state.stage))
            st.rerun()
        else:
            st.success(text["case_completed"])

# ---------- Controls ----------
def restart_case():
    st.session_state.stage = 1
    st.session_state.score = 0
    st.session_state.completed = []
    for stage in CORRECT_ANSWERS:
        st.session_state.pop(f"answer_{stage}", None)
        st.session_state.pop(f"reason_{stage}", None)


st.divider()
left, right = st.columns(2)
with left:
    st.button(text["restart"], on_click=restart_case)
with right:
    st.caption(text["completed_count"].format(count=len(st.session_state.completed)))
st.divider()
st.caption(text["footer"])

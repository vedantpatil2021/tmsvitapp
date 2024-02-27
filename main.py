import streamlit as st
st.set_page_config(layout = "wide")

import pandas as pd
from datetime import datetime
from processJSON import processJSON

JSON_PATH = "./data.json"
data = processJSON(JSON_PATH)

st.title("TT Manager")

st.markdown("# ")
st.header("Time Table")
st.dataframe(data.drop("weekday", 1), use_container_width = True)

questions = [
    "What is my next lecture?",
    "What's my schedule for today?",
    "What's my schedule on specific day?",
    "Give me a list of lectures taught by specific professor.",
    "Which rooms are assigned to a particular professor?"
]

question = st.selectbox("Ask a Question", questions)
index = questions.index(question)

if index <= 1:
    _, _, day = datetime.today().isocalendar()

if 3 <= index <= 4:
    profs = list(set(data["instructor_name"]))
    profs.sort()
    prof = st.selectbox("Select a Professor", profs)
    ans = data[data["instructor_name"] == prof]

if index == 0:
    current_time = datetime.now().time()
    st.write(f"Current Time: {current_time}")
    st.markdown("## ")
    ans = data[(data["weekday"] == day) & (data["start_time"] >= current_time)]

elif index == 1:
    ans = data[data["weekday"] == day]

elif index == 2:
    date = st.date_input("Select a date")
    ans = data[data["weekday"] == (date.weekday())]

elif index == 3:
    ans = ans.sort_values(by = ["course_name"])
    ans = ans[["course_name"]].drop_duplicates().reset_index(drop = True)
    
elif index == 4:
    ans = ans.sort_values(by = ["room"])
    ans = ans[["room"]].drop_duplicates().reset_index(drop = True)


if st.button("GET"):
    try:
        st.dataframe(ans.drop("weekday", 1), use_container_width = True)
    except Exception as e:
        print(e)
        st.dataframe(ans)
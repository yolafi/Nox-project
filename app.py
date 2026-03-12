import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="NOX", page_icon="🌑", layout="centered")

# 2. Initialize Session State (Local memory for the user)
if 'votes' not in st.session_state:
    st.session_state.votes = {}

# 3. Google Sheets Connection
SHEET_ID = "16bSqmFKnS-Fex_-BP2pr7GaGqnd-gdZ2Q6rtqstddSc"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

@st.cache_data(ttl=60) # Refreshes data every minute
def load_data():
    return pd.read_csv(CSV_URL).dropna(subset=["Nom de l'objet"])

# 4. Main Application Interface
try:
    df = load_data()

    st.title("🌑 NOX")
    st.markdown("### The ultimate hype barometer.")
    st.divider()

    for index, row in df.iterrows():
        # Mapping Google Sheet columns
        name = row["Nom de l'objet"]
        image_url = row["Lien vidéo (ou photo)"]
        description = row["Description courte"]
        global_nox_score = row["Nox-score"]

        with st.container():
            # Image Display
            try:
                st.image(image_url, use_container_width=True)
            except:
                st.warning("Image not found")

            # Title & Description
            st.subheader(name)
            st.info(description)

            # Global Score Display
            st.metric(label="Global NOX-SCORE", value=f"{global_nox_score}/10")

            # Vote Logic
            if index in st.session_state.votes:
                # Personal result display
                user_score = st.session_state.votes[index]
                st.success(f"Your Score: {user_score}/10 ✅")
                
                # Reset Vote Button
                if st.button("Reset my vote", key=f"reset_{index}"):
                    del st.session_state.votes[index]
                    st.rerun()
            else:
                # Voting Interface
                note = st.slider("Rate this item", 0, 10, 5, key=f"s_{index}")
                if st.button(f"Submit {note}/10", key=f"btn_{index}"):
                    st.session_state.votes[index] = note
                    st.rerun()
            
            st.divider()

except Exception as e:
    st.error("Data connection error.")
    st.write("Ensure your Google Sheet is shared with 'Anyone with the link' as a Viewer.")
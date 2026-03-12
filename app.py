import streamlit as st
import pandas as pd

# 1. Configuration de la page (onglet nettoyé, juste "NOX" sans émoji nul)
st.set_page_config(page_title="NOX", layout="centered")

# 2. Mémoire des votes
if 'votes' not in st.session_state:
    st.session_state.votes = {}

# 3. Récupération des données
SHEET_ID = "16bSqmFKnS-Fex_-BP2pr7GaGqnd-gdZ2Q6rtqstddSc"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

@st.cache_data(ttl=60)
def load_data():
    return pd.read_csv(CSV_URL).dropna(subset=["Nom de l'objet"])

# 4. Interface principale
try:
    df = load_data()

    # --- TON LOGO (Uniquement l'image, pas de texte ni d'émoji) ---
    st.image("https://i.ibb.co/cK88yMMn/16780.png", use_container_width=True)
    
    st.divider()

    for index, row in df.iterrows():
        name = row["Nom de l'objet"]
        image_url = row["Lien vidéo (ou photo)"]
        global_score = row["Nox-score"]

        with st.container():
            try:
                st.image(image_url, use_container_width=True)
            except:
                st.write(f"🖼️ {name}")

            st.subheader(name)
            st.metric(label="Global NOX-SCORE", value=f"{global_score}/10")

            if index in st.session_state.votes:
                st.success(f"Your Score: {st.session_state.votes[index]}/10 ✅")
                if st.button(f"Reset vote", key=f"reset_{index}"):
                    del st.session_state.votes[index]
                    st.rerun()
            else:
                note = st.slider(f"Rate", 0, 10, 5, key=f"s_{index}")
                if st.button(f"Submit {note}/10", key=f"b_{index}"):
                    st.session_state.votes[index] = note
                    st.rerun()
            
            st.divider()

except Exception as e:
    st.error("Connection error.")

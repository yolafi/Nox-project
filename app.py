import streamlit as st
import pandas as pd

st.set_page_config(page_title="NOX", page_icon="🌑")

# --- CONNEXION AU GOOGLE SHEET ---
# Ton lien actuel avec la correction pour l'export CSV
sheet_id = "16bSqmFKnS-Fex_-BP2pr7GaGqnd-gdZ2Q6rtqstddSc"
csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

# Fonction pour charger les données
def load_data():
    # On ajoute on-error pour éviter que l'app plante si une ligne est vide
    return pd.read_csv(csv_url).dropna(subset=['Nom', 'Image'])

try:
    df = load_data()

    st.title("🌑 NOX")
    st.write("Donne ton avis sur les dernières tendances.")

    for index, row in df.iterrows():
        # Affiche l'image avec une gestion d'erreur si le lien est mort
        try:
            st.image(row['Image'], use_container_width=True)
        except:
            st.warning(f"Image introuvable pour {row['Nom']}")
            
        st.subheader(row['Nom'])
        
        note = st.slider(f"Nox-Score", 0, 10, 5, key=f"slider_{index}")
        
        if st.button(f"Voter pour {row['Nom']}", key=f"btn_{index}"):
            st.balloons()
            st.success(f"Tu as mis {note}/10 !")
        st.divider()

except Exception as e:
    st.error("⚠️ Erreur de lecture")
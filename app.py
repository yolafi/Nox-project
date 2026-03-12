import streamlit as st

st.set_page_config(page_title="NOX", page_icon="🌑")

st.title("🌑 NOX")
st.write("Le baromètre de la hype. Note les tendances !")

# Tes premiers objets
objets = [
    {"nom": "GTA VI", "image": "https://media.rockstargames.com/rockstargames-newsite/img/global/games/fob/640/GTAVI.jpg"},
    {"nom": "Avatar: Fire and Ash", "image": "https://img.vgc.co/media/2024/08/avatar-fire-and-ash.jpg"}
]

for obj in objets:
    with st.container():
        st.image(obj["image"], use_container_width=True)
        st.subheader(obj["nom"])
        # Le slider (curseur) comme sur ta photo !
        note = st.slider(f"Nox-Score pour {obj['nom']}", 0, 10, 5, key=obj['nom'])
        if st.button(f"Valider la note : {note}/10", key="btn_"+obj['nom']):
            st.balloons() # Petit effet de fête
            st.success(f"Note enregistrée pour {obj['nom']} !")
        st.divider()
      

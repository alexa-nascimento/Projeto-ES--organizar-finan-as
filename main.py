import streamlit as st
from database import criar_tabelas
from auth import login_page

st.set_page_config(page_title="Financeiro",page_icon="") #titulo da aba

criar_tabelas() # garante banco criado


if "logged" not in st.session_state: #usuario sem estado salvo, cria estado not logged
    st.session_state["logged"] = False
    
if not st.session_state["logged"]: #não logado mostra login, estando logado se redireciona para tela inicial
    login_page()
else:
    st.switch_page("pages/dashboard.py")
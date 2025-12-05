import streamlit as st 
from database import criar_usuario, validar_login

def login_page():
    st.title("Organização Financeira - Login") #titulo da  pagina

    tab_login,tab_cadastro = st.tabs(["Login","Cadastro"]) #duas abas criadas
    
    with tab_login: #caixa de texto para usuario e senha
        username = st.text_input("Usuário")
        password = st.text_input("Senha", type="password") #oculta caracteres
        if st.button("Entrar"):
            user = validar_login(username, password)
            if user:
                st.session_state["logged"] = True
                st.session_state["user_id"] = user[0]
                st.switch_page("pages/dashboard.py")
            else:
                st.error("Usuario ou senha incorretos.") #verifica login existente,salva sessão se sim,mostra erro se não.
    
    with tab_cadastro: # input pra criar nova conta
        new_user = st.text_input("Novo usuário")
        new_pass = st.text_input("Nova senha", type="password")
        if st.button("Cadastrar"): #tenta criar usuario e retorna
            if criar_usuario(new_user, new_pass):
                st.success("Usuário criado! Agora faça login.")
            else:
                st.error("Usuário ja existente.")


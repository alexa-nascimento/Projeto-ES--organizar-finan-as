import streamlit as st
import datetime
from database import (
    inserir_transacao, listar_transacoes, deletar_transacao, criar_metas,listar_metas,adicionar_progresso,deletar_meta, conectar
)


# CSS 
st.markdown("""
<style>

.container {
    padding: 20px;
    margin-top: 20px;
    border-radius: 15px;
    background-color: #1a1a1a;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.3);
}

.titulo {
    font-size: 24px;
    font-weight: 700;
    margin-bottom: 15px;
}

.gasto { border-left: 8px solid #ff4b4b; }
.ganho { border-left: 8px solid #4caf50; }
.meta  { border-left: 8px solid #0ea5e9; }

.item {
    padding: 12px;
    background-color: #2a2a2a;
    border-radius: 10px;
    margin-bottom: 8px;
}

</style>
""", unsafe_allow_html=True)


def nome_perfil_usuario(user_id):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT username FROM users WHERE id = ?", (user_id,))
    user = cur.fetchone()
    conn.close()
    if user:
        return user[0]
    return "Usuario"


# -------------------------
# Proteção de login
# -------------------------
if "logged" not in st.session_state or not st.session_state["logged"]:
    st.switch_page("main.py")

st.title("Painel Financeiro")
user_id = st.session_state["user_id"]

with st.sidebar:
    username =  nome_perfil_usuario(st.session_state["user_id"])
    st.markdown(f"""
        <div style="
                background-color: #1f1f1f;
                padding: 15px;
                border-radius: 15px;
                text-align:center;
                margin-bottom:10px;
                ">
                <div style="
                width: 70px;
                height:70px;
                background-color: #4caf50;
                border-radius:50%;
                margin: 0 auto 10px auto;
                display: flex;
                align-items:center;
                justify-content:center;
                font-size:24px;
                color:white
                font-weight:bold;
                ">
                {username[0].upper()}
        </div>
        <div style='color=white;font-size=18px;font-weight:bold;'>{username}</div>
        </div>
        """,unsafe_allow_html=True)
    if st.button(" Sair"):
        st.session_state.clear()
        st.switch_page("main.py")


# -------------------------
# FORMULÁRIO PARA ADICIONAR
# -------------------------
st.subheader("Transações")

if st.button("➕ Adicionar item"):
    st.session_state["abrir_dialog"] = True

# ---------------------------
# POP-UP DE ADICIONAR ITEM
# ---------------------------

@st.dialog("Adcionar item")
def dialog_adcionar_item():
    st.subheader("Novo transação")

    col1,col2, col3 = st.columns(3)

    with col1:
        tipo = st.selectbox("Tipo:", ["gasto", "ganho"])
    with col2:
        descricao = st.text_input("Descrição")
    with col3:
        valor = st.number_input("Valor", min_value=0.0, step=0.01)

    data_transacao = st.date_input("Data da transação")

    if st.button("Salvar"):
        inserir_transacao(
            st.session_state["user_id"],
            tipo,
            descricao,
            valor,
            str(data_transacao)
            )
        st.success("item adicionado!")
        st.session_state["abir_dialog"] = False
        st.rerun()
    if st.button("Cancelar"):
        st.session_state["abrir_dialog"] = False
        st.rerun()
    
if st.session_state.get("abrir_dialog", False):
    dialog_adcionar_item()


# ---------------------------------------------------------
#  CARDS LADO A LADO — GASTOS E GANHOS
# ---------------------------------------------------------

colA, colB = st.columns(2)
with colA:
    st.markdown("<div class='container gasto'><div class='titulo'> Gastos</div>", unsafe_allow_html=True)

    gastos = listar_transacoes(user_id, tipo="gasto")

    if len(gastos) == 0:
        st.info("Nenhum gasto registrado.")
    else:
        for id_, uid, tipo_, desc, val, data in gastos:
            st.markdown(f"<div class='item'><b>{desc}</b> — R$ {val:.2f}<br><small>{data}</small></div>", unsafe_allow_html=True)
            if st.button("Excluir", key=f"del_gasto_{id_}"):
                deletar_transacao(id_)
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

with colB:
    st.markdown("<div class='container ganho'><div class='titulo'>💰 Ganhos</div>", unsafe_allow_html=True)

    ganhos = listar_transacoes(user_id, tipo="ganho")

    if len(ganhos) == 0:
        st.info("Nenhum ganho registrado.")
    else:
        for id_, uid, tipo_, desc, val, data in ganhos:
            st.markdown(f"<div class='item'> <b>{desc}</b> — R$ {val:.2f}<br><small>{data}</small></div>", unsafe_allow_html=True)
            if st.button("Excluir", key=f"del_ganho_{id_}"):
                deletar_transacao(id_)
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)



# -------------------------------------------------------
# FORMULÁRIO DE METAS
# -------------------------------------------------------
st.subheader("Adicionar nova meta")

col1, col2 = st.columns(2)
with col1:
    meta_desc =st.text_input("Descrição da meta")
with col2:
    meta_valor = st.number_input("Valor objetivo (R$)" , min_value=0.0)

if st.button("Criar meta"):
    criar_metas(user_id, meta_desc, meta_valor)
    st.success("Meta criada")
    st.rerun()



# ---------------------------------------------------------
#  METAS – CONTAINER 3
# ---------------------------------------------------------
st.markdown("<div class='container meta'>", unsafe_allow_html=True)
st.markdown("<div class='titulo'>🎯 Metas</div>", unsafe_allow_html=True)

metas = listar_metas(user_id)

if len(metas) == 0:
    st.info("Nenhuma meta registrada.")
else:
    for id_, uid,  desc, objetivo, progresso, data in metas:

        st.markdown(f"<div class='item'><b>{desc}</b><br>Objetivo: R$ {objetivo:.2f}</div>", 
                    unsafe_allow_html=True)

        
        percentual = progresso / objetivo if objetivo > 0 else 0
        st.progress(percentual)

        add_val = st.number_input(f"Adicionar à meta \"{desc}\"", min_value= 0.0, step=1.0,key=f"add_(id_)")
        if st.button("Adicionar valor", key=f"add_btn_{id_}"):
            adicionar_progresso(id_, add_val)
            st.success("Progresso atualizado!")
            st.rerun()
        
        if st.button("Excluir meta", key=f"del_meta_{id_}"):
            deletar_meta(id_)
            st.rerun()


st.markdown("</div>", unsafe_allow_html=True)
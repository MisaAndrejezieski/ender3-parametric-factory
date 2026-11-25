from pathlib import Path

import plotly.graph_objects as go
import streamlit as st
import trimesh

from cad.industrial_case import gerar_case_eletronico
from cad.mechanical_gears import gerar_engrenagem_tecnica

st.set_page_config(page_title="Parametric CAD Studio", layout="wide")
st.title("Studio CAD Paramétrico — Engenharia & Peças Sob Medida")

with st.sidebar:
    st.header("1. Escolha o Gerador")
    modelo = st.selectbox(
        "Tipo de Peça",
        ["Engrenagem Mecânica Involuta", "Case Industrial Eletrônico"],
    )

    st.header("2. Parâmetros em Tempo Real")
    if modelo == "Engrenagem Mecânica Involuta":
        modulo = st.slider("Módulo do Dente (mm)", 1.0, 5.0, 2.0, 0.25)
        num_dentes = st.slider("Número de Dentes (Z)", 10, 60, 24, 1)
        espessura = st.slider("Espessura (mm)", 4.0, 40.0, 12.0, 1.0)
        diametro_eixo = st.slider("Diâmetro do Eixo (mm)", 3.0, 25.0, 8.0, 0.5)
        rasgo_chaveta = st.checkbox("Incluir Rasgo de Chaveta", value=True)
        arquivo_stl = gerar_engrenagem_tecnica(
            modulo=modulo,
            num_dentes=num_dentes,
            espessura=espessura,
            diametro_eixo=diametro_eixo,
            rasgo_chaveta=rasgo_chaveta,
            nome_arquivo="preview_engrenagem.stl",
        )
    else:
        comp = st.slider("Comprimento (mm)", 40.0, 200.0, 110.0, 2.0)
        larg = st.slider("Largura (mm)", 30.0, 160.0, 75.0, 2.0)
        alt = st.slider("Altura (mm)", 15.0, 100.0, 40.0, 2.0)
        parede = st.slider("Espessura da Parede (mm)", 1.6, 4.0, 2.4, 0.2)
        arquivo_stl = gerar_case_eletronico(
            comprimento=comp,
            largura=larg,
            altura=alt,
            parede=parede,
            nome_arquivo="preview_case.stl",
        )

# Renderização 3D interativa no navegador
malha = trimesh.load_mesh(str(arquivo_stl))
vertices = malha.vertices
faces = malha.faces

fig = go.Figure(
    data=[
        go.Mesh3d(
            x=vertices[:, 0],
            y=vertices[:, 1],
            z=vertices[:, 2],
            i=faces[:, 0],
            j=faces[:, 1],
            k=faces[:, 2],
            color="#00CC96",
            opacity=1.0,
            flatshading=True,
        )
    ]
)
fig.update_layout(
    scene=dict(aspectmode="data"),
    margin=dict(l=0, r=0, t=0, b=0),
    height=600,
)

col1, col2 = st.columns([3, 1])
with col1:
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Métricas da Peça")
    volume_cm3 = malha.volume / 1000.0
    peso_petg_g = volume_cm3 * 1.27  # Densidade média PETG
    custo_filamento = (peso_petg_g / 1000.0) * 110.0  # R$ 110/kg PETG

    st.metric("Volume Sólido", f"{volume_cm3:.2f} cm³")
    st.metric("Peso Estimado (PETG)", f"{peso_petg_g:.1f} g")
    st.metric("Custo Material", f"R$ {custo_filamento:.2f}")

    with open(arquivo_stl, "rb") as f:
        st.download_button(
            label="Baixar STL Pronto para Fatiar",
            data=f,
            file_name=Path(arquivo_stl).name,
            mime="application/octet-stream",
            type="primary",
        )

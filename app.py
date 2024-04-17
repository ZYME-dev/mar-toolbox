import streamlit as st
import pandas as pd
import numpy as np
from typing import List, Optional
from pydantic import BaseModel, Field
from fillpdf import fillpdfs
from datetime import datetime

# streamlit run app.py


class MPRA_AttestationTravaux(BaseModel):

    first_name  : str = Field(default='', alias="Prénom")
    last_name   : str = Field(default='', alias="Nom")
    full_name   : str = Field(default='', alias="Nom Prénom")

    address_street_number : str = Field(default='', alias="n°")
    address_street_name   : str = Field(default='', alias="Voie")
    address_city_code     : str = Field(default='', alias="Code postal")
    address_city_name     : str = Field(default='', alias="Ville")

    total_amounts_ht  : int = Field(default=0, alias="cout euro HT")
    total_amounts_ttc : int = Field(default=0, alias="cout TTC")
    

data = MPRA_AttestationTravaux()

def export_pdf():

    path = 'mpra_attestation_travaux.pdf'
    path_out = 'out.pdf'
    model = data.model_dump(by_alias=True)
    print(model)

    fillpdfs.write_fillable_pdf(path, path_out, model)


st.title('Dossier MPRA')



with st.container():
    st.header("1. Identité du demandeur", divider=True)
    col1, col2 = st.columns(2)
    last_name = col1.text_input("Nom")
    first_name = col2.text_input("Prénom(s)")
    full_name = f"{last_name.upper()}, {first_name}"
    if first_name != "" and last_name != "" : st.text(full_name)

    data.last_name = last_name
    data.first_name = first_name
    data.full_name = full_name

st.button("export", on_click=export_pdf)

with st.container():
    st.header("2. Adresse du chantier", divider=True)
    col1, col2 = st.columns([1, 3])
    address_street_number = col1.text_input("N°")
    address_street_name = col2.text_input("Voie")
    col1, col2 = st.columns([1, 3])
    address_city_code = col1.text_input("Code Postal")
    address_city_name = col2.text_input("Ville")

    data.address_street_number = address_street_number
    data.address_street_name = address_street_name
    data.address_city_code = address_city_code
    data.address_city_name = address_city_name

with st.container():
    st.header("3. Synthèse des travaux éligibles", divider=True)
    col1, col2 = st.columns(2)
    total_amounts_ht = col1.number_input('Coût total des travaux éligibles (€ HT)', value=0, min_value=0)
    total_amounts_ttc = col2.number_input('Coût total des travaux éligible (€ TTC)', value=0, min_value=0)
    data.total_amounts_ht = total_amounts_ht
    data.total_amounts_ttc = total_amounts_ttc

with st.container():
    st.header("4. Synthèse de l’audit énergétique", divider=True)
    col1, col2 = st.columns(2)
    audit_date = col1.date_input("Date de réalisation de l'audit énergétique", datetime.now(), format="DD/MM/YYYY") 
    audit_id = col2.text_input("Identifiant de l’audit énergétique (n°)")
    col1, col2 = st.columns(2)
    audit_company_name = col1.text_input("Raison Sociale")
    audit_company_siret = col2.text_input("Siret (14 chiffres)", max_chars=14)

    
    def situation(key_id):
        st.write("Consommation conventionnelle (chauffage, refroidissement, production d'eau chaude sanitaire, éclairage, auxiliaires)")
        with st.expander("Calculette EP > EF"):
            cols = st.columns(7)
            cols[0].write("Energie Primaire")
            ep = [0,0,0,0,0]
            ep[0] = cols[1].number_input("Chauffage", key=key_id+"ep_chauffage", value=0, min_value=0)
            ep[1] = cols[2].number_input("ECS", key=key_id+"ep_ecs", value=0, min_value=0)
            ep[2] = cols[3].number_input("Climatisation", key=key_id+"ep_climatisation", value=0, min_value=0)
            ep[3] = cols[4].number_input("Auxiliaires", key=key_id+"ep_auxiliaires", value=0, min_value=0)
            ep[4] = cols[5].number_input("Eclairage", key=key_id+"ep_eclairage", value=0, min_value=0)
            ep_calc = sum(ep)
            ep_sum = cols[6].number_input("Total EP", key=key_id+"ep_sum", value=ep_calc, min_value=0)

            cols = st.columns(7)
            cols[0].write("Elec ?")
            is_elec = [False, False, False, False, False]
            is_elec[0] = cols[1].checkbox("", key=key_id+"is_elec_chauffage", value=False)
            is_elec[1] = cols[2].checkbox("", key=key_id+"is_elec_ecs", value=True)
            is_elec[2] = cols[3].checkbox("", key=key_id+"is_elec_climatisation", value=True)
            is_elec[3] = cols[4].checkbox("", key=key_id+"is_elec_auxiliaires", value=True)
            is_elec[4] = cols[5].checkbox("", key=key_id+"is_elec_eclairage", value=True)

            cols = st.columns(7)
            cols[0].write("Energie Finale")
            ef_calc = [0,0,0,0,0]
            for i in range(0,5):
                if is_elec[i] : ef_calc[i] = int(ep[i] / 2.3)
                else :  ef_calc[i] = int(ep[i])
            ef = [0,0,0,0,0]
            ef[0] = cols[1].number_input("", key=key_id+"ef_chauffage", value=ef_calc[0], min_value=0, disabled=True)
            ef[1] = cols[2].number_input("", key=key_id+"ef_ecs", value=ef_calc[1], min_value=0, disabled=True)
            ef[2] = cols[3].number_input("", key=key_id+"ef_climatisation", value=ef_calc[2], min_value=0, disabled=True)
            ef[3] = cols[4].number_input("", key=key_id+"ef_auxiliaires", value=ef_calc[3], min_value=0, disabled=True)
            ef[4] = cols[5].number_input("", key=key_id+"ef_eclairage", value=ef_calc[4], min_value=0, disabled=True)
            ef_sum = cols[6].number_input("Total EF", key=key_id+"ef_sum", value=sum(ef), min_value=0)
        
        col1, col2, col3 = st.columns(3)
        ep_total = col1.number_input("Energie Primaire (kWh/m²/an)", key=key_id+"ep_total", value=ep_sum, min_value=0)
        ef_total = col2.number_input("Energie Finale (kWh/m²/an)", key=key_id+"ef_total", value=ef_sum, min_value=0)
        ges_total = col3.number_input("Émissions GES (kgCO2eq/m²/an)", key=key_id+"ges_total", value=0, min_value=0)

        col1, col2, col3 = st.columns(3)
        dpe = col2.selectbox("Etiquette", key=key_id+"dpe", options=['A', 'B', 'C', 'D', 'E', 'F', 'G'], index=6)
        shab = col3.number_input("Surface de référence du logement (m²)", key=key_id+"shab", value=100, min_value=0)
        
        return (ep_total, ef_total, ges_total, dpe, shab)
    
    st.subheader("Situation initiale du logement (« avant travaux »)")
    si = situation("SI_")

    st.subheader("Situation du logement projetée dans le scénario de travaux retenu (« après travaux »)")
    sf = situation("SF_")

    st.subheader("Gain de classes de performance énergétique associé au projet de travaux :")

    dpe_jump = ord(si[3])-ord(sf[3])
    if dpe_jump < 2 : st.error(f"Le nombre de sauts de classe est seulement de : {dpe_jump} < 2")
    else: st.success(f"Le nombre de sauts de classe est de : {dpe_jump}")

with st.container():
    st.header("5. Description des travaux éligibles", divider=True)

    col_size = [1,1,1,1]
    for row in range(1, 8):
        with st.expander(f"Poste de Travaux N° {row}"):
            # if row > 1 : st.divider()
            cols = st.columns(col_size)
            cols[0].text_input("Quantité", key=f"A{row}", placeholder="100 m²")
            cols[1].text_input("Résistance", key=f"B{row}", placeholder="3.5 W/m².K")
            cols[2].number_input("Montant HT", key=f"C{row}", placeholder=1000, min_value=0)
            cols[3].number_input("Montant TTC",key=f"D{row}", placeholder=1200, min_value=0)
            st.text_input("", key=f"E{row}", placeholder="Isolation thermique par l’extérieur des murs avec de la laine de bois")
        

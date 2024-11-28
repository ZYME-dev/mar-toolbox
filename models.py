from typing import List, Optional
from pydantic import BaseModel, Field
from PyPDFForm import PdfWrapper, FormWrapper


def flatten(data, key=None, *, parent_key=False, seperator="."):
    if isinstance(data, list):
        for item in data:
            yield from flatten(item, key)
    elif isinstance(data, dict):
        for k, v in data.items():
            if key:
                if parent_key : new_key = key + seperator + k
                else: new_key = k
                yield from flatten(v, new_key)
            else:
                yield from flatten(v, k) 
    else:
        yield key, data

class Form_AttestationTravauxMPRA(BaseModel):

    # Fait à
    # date jour
    # Date mois
    # Date année
    # Nom Prénom P5
    # Signature17
    # Fait à \(accompagnateur\)
    # date jour \(accompagnateur\)
    # Date mois \(accompagnateur\)
    # Date année \(accompagnateur\)
    # Nom Prénom Accompagnateur
    # Signature19
    # Raison sociale p5
    # N SIRET P5

    demandeur_nom_prenom: Optional[str] = Field(default=None, serialization_alias="Nom Prénom")
    adresse_chantier_num : str | int | None = Field(default=None, serialization_alias="n°")
    adresse_chantier_voie   : Optional[str] = Field(default=None, serialization_alias="Voie")
    adresse_chantier_codepostal     : Optional[str] = Field(default=None, serialization_alias="Code postal")
    adresse_chantier_ville     : Optional[str] = Field(default=None, serialization_alias="Ville")
    cout_total_travaux_elligibles_ht : Optional[int] = Field(default=None, serialization_alias="cout euro HT")
    cout_total_travaux_elligibles_ttc : Optional[int] = Field(default=None, serialization_alias="cout TTC")
    audit_date_jour : Optional[str] = Field(default=None, serialization_alias="Date de réalisation de laudit énergétique Jour")
    audit_date_mois : Optional[str] = Field(default=None, serialization_alias="Date de réalisation de laudit énergétique Mois")
    audit_date_annee : Optional[str] = Field(default=None, serialization_alias="Date de réalisation de laudit énergétique Année")

    audit_id: Optional[str] = Field(default=None, serialization_alias="Identifiant")
    audit_professionnel_raison: Optional[str] = Field(default=None, serialization_alias="Raison sociale")
    audit_professionnel_siret: Optional[str] = Field(default=None, serialization_alias="N SIRET")

    etat_initial_ep: Optional[int] = Field(default=None, serialization_alias="Energie primaire")
    etat_initial_ef: Optional[int] = Field(default=None, serialization_alias="Energie finale")
    etat_initial_ges: Optional[int] = Field(default=None, serialization_alias="Emissions annuelles")
    etat_initial_dpe: Optional[str] = Field(default=None, serialization_alias="Classe énergétique")
    etat_initial_shab: Optional[int] = Field(default=None, serialization_alias="Surface")

    etat_final_ref_scenario: Optional[int] = Field(default=None, serialization_alias="référence")
    etat_final_ep: Optional[int] = Field(default=None, serialization_alias="Energie primaire p2")
    etat_final_ef: Optional[int] = Field(default=None, serialization_alias="Energie finale p2")
    etat_final_ges: Optional[int] = Field(default=None, serialization_alias="Emissions annuelles p2")
    etat_final_dpe: Optional[str] = Field(default=None, serialization_alias="Classe énergétique P2")
    etat_final_shab: Optional[int] = Field(default=None, serialization_alias="surface p2")

    gain_classe_2: bool = Field(default=False, serialization_alias="Gain de classes 1")
    gain_classe_3: bool = Field(default=False, serialization_alias="Gain de classes 2")
    gain_classe_4: bool = Field(default=False, serialization_alias="Gain de classes 3")

    poste_1_description: Optional[str] = Field(default=None, serialization_alias="Description des postes de travaux éligibles Row 2")
    poste_1_cout_ht_ttc: Optional[str] = Field(default=None, serialization_alias="Coût des travaux en HT TTC Row1") 

    poste_2_description: Optional[str] = Field(default=None, serialization_alias="Description des postes de travaux éligibles Row 3")
    poste_2_cout_ht_ttc: Optional[str] = Field(default=None, serialization_alias="Coût des travaux en HT TTC Row 2") 

    poste_3_description: Optional[str] = Field(default=None, serialization_alias="Description des postes de travaux éligibles Row 4")
    poste_3_cout_ht_ttc: Optional[str] = Field(default=None, serialization_alias="Coût des travaux en HT TTC Row 3") 

    poste_4_description: Optional[str] = Field(default=None, serialization_alias="Description des postes de travaux éligibles Row 5")
    poste_4_cout_ht_ttc: Optional[str] = Field(default=None, serialization_alias="Coût des travaux en HT TTC Row 4") 

    poste_5_description: Optional[str] = Field(default=None, serialization_alias="Description des postes de travaux éligibles Row 6")
    poste_5_cout_ht_ttc: Optional[str] = Field(default=None, serialization_alias="Coût des travaux en HT TTC Row 5") 

    poste_6_description: Optional[str] = Field(default=None, serialization_alias="Description des postes de travaux éligibles Row 7")
    poste_6_cout_ht_ttc: Optional[str] = Field(default=None, serialization_alias="Coût des travaux en HT TTC Row 6") 

    poste_7_description: Optional[str] = Field(default=None, serialization_alias="Description des postes de travaux éligibles Row 8")
    poste_7_cout_ht_ttc: Optional[str] = Field(default=None, serialization_alias="Coût des travaux en HT TTC Row 7") 

    derogation_1_designation: Optional[str] = Field(default=None, serialization_alias="Paroi opaque ou vitrée concernée Row 1")
    derogation_1_motif: Optional[str] = Field(default=None, serialization_alias="Motifs Row 1")

    derogation_2_designation: Optional[str] = Field(default=None, serialization_alias="Paroi opaque ou vitrée concernée Row 2")
    derogation_2_motif: Optional[str] = Field(default=None, serialization_alias="Motifs Row 2")

    derogation_3_designation: Optional[str] = Field(default=None, serialization_alias="Paroi opaque ou vitrée concernée Row 3")
    derogation_3_motif: Optional[str] = Field(default=None, serialization_alias="Motifs Row 3")


    def get_filling_dict(self):
        model = self.model_dump(by_alias=True)
        data = dict(flatten(model))
        return data

if __name__ == "__main__" :
    # 
    # 

    # D
    # Date de réalisation de laudit énergétique Année
    f = Form_AttestationTravauxMPRA()

    f.demandeur_nom_prenom = "DU PELOUX, Lionel"
    f.etat_final_shab = 101
    f.etat_final_dpe = "B"
    f.gain_classe_3 = True
    model = f.model_dump(by_alias=True)
    data = dict(flatten(model))

    for k in data: print(f"{k}:{data[k]}")

    path = 'anah_mpra_attestation_factures.pdf'
    path_out = 'out.pdf'

    data_dict = {
        "Nom Prénom" : "Lionel du Peloux",
        "Coût des travaux en HT TTC Row1": '1200.00 € HT \n 1220,00 € TTC', 
    }

    # fillpdfs.write_fillable_pdf(path, path_out, data_dict)

    filled = FormWrapper(path).fill(f.get_filling_dict(),flatten=False)

    with open(path_out, "wb+") as output:
        output.write(filled.read())
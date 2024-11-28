import json
from pathlib import Path
from typing import Dict
from PyPDFForm import PdfWrapper, FormWrapper
import encodings
from datetime import datetime
import python_calamine

path = "anah_mpra_attestation_factures.pdf"
path_out = "out.pdf"
# fields = fillpdfs.get_form_fields(path)
# for f in fields: print(f)

data_dict = {
    "Nom Prénom": "Lionel du Peloux",
    "Coût des travaux en HT TTC Row1": "1200.00 € HT \n 1220,00 € TTC",
}


def fill_pdf_template(data:dict, template_filepath:Path):
    
    if template_filepath.suffix == ".pdf":
        # pdf_form_schema = PdfWrapper(str(template_filepath)).schema
        # print(json.dumps(pdf_form_schema, indent=4, sort_keys=True))
        filled = FormWrapper(str(template_filepath)).fill(data)
        with open(f"tmp/{template_filepath.name.replace("template","output")}", "wb+") as output:
            output.write(filled.read())
    

def read(form_path="assets/form.xlsx"):
    
    
    templates = []
    templates_dir = Path("assets/templates/")
    for f in templates_dir.iterdir():
        print(f)
    
    workbook = python_calamine.CalamineWorkbook.from_path(form_path)
    
    generators = []
    for sheet_name in workbook.sheet_names:
        print(sheet_name)
        sheet = workbook.get_sheet_by_name(sheet_name)
        data = sheet.to_python()
        if "template" in data[0][0]:
            template_filename = data[0][0]
            template_filename_parts = template_filename.split(".")
            extension = template_filename_parts[-1]
            
            
            d = {}
            for row in data[1:]:
                k = row[1]
                if k != "":
                    try:
                        if isinstance(row[2], datetime):
                            v = row[2].strftime("%d/%m/%Y")
                        else:
                            v = int(row[2])
                            if "plan_financement" in template_filename:
                                v = "" if v == 0 else str(v).rjust(5)
                            else:
                                v = "" if v == 0 else str(v)
                    except ValueError:
                        v = row[2] 
                    d[k] = v      
        
            template_filepath = templates_dir.joinpath(template_filename)
            fill_pdf_template(data=d, template_filepath=template_filepath)
            pass
        


def print_widgets(path):
    pdf_form_schema = PdfWrapper(path).schema
    print(json.dumps(pdf_form_schema, indent=4, sort_keys=True))
    print("")
    for k, v in pdf_form_schema["properties"].items():
        # print(f"{k} : {v['type']}")
        print(f"{k}")
        pass

    # filled = FormWrapper(path).fill(
    #     {
    #         "demandeur_nom_prenom": "DU PELOXU, Lionel",
    #         "type_demandeur": 1,
    #         "demandeur_fait_le": datetime.now().strftime("%d/%m/%Y")
    #     },
    #     flatten=False,  # optional
    # )


    # with open("output.pdf", "wb+") as output:
    #     output.write(filled.read())
read()
# print_widgets("assets/anah_mpra_plan_financement.template.pdf")

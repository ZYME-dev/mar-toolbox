import fillpdf
from fillpdf import fillpdfs
from PyPDFForm import PdfWrapper
import json
from PyPDFForm import PdfWrapper, FormWrapper
import encodings

path = 'anah_mpra_attestation_travaux.pdf'
path_out = 'out.pdf'
fields = fillpdfs.get_form_fields(path)
# for f in fields: print(f)

data_dict = {
    "Nom Prénom" : "Lionel du Peloux",
    "Coût des travaux en HT TTC Row1": '1200.00 € HT \n 1220,00 € TTC', 
}

pdf_form_schema = PdfWrapper(path).schema
for k,v in pdf_form_schema["properties"].items():
    print(f"{k} : {v['type']}")
    # print(f"{k}")


# filled = FormWrapper(path).fill(
#     {
#         "Nom Prénom": "DU PELOUX, Lionel",
#     },
#     flatten=False,
# )

# with open(path_out, "wb+") as output:
#     output.write(filled.read())

# mydict = {k: str(v).encode("utf-8") for k,v in pdf_form_schema.items()}
# print(json.dumps(pdf_form_schema["properties"], indent=4, sort_keys=True, ensure_ascii=False))

# fillpdfs.write_fillable_pdf(path, path_out, data_dict)
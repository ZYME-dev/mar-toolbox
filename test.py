import fillpdf
from fillpdf import fillpdfs

path = 'mpra_attestation_travaux.pdf'
path_out = 'out.pdf'
fields = fillpdfs.get_form_fields(path)
for f in fields: print(f)

data_dict = {
    "Nom Prénom" : "Lionel du Peloux",
    "Coût des travaux en HT TTC Row1": '1200.00 € HT \n 1220,00 € TTC', 
}

fillpdfs.write_fillable_pdf(path, path_out, data_dict)
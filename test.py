
from PyPDFForm import PdfWrapper
import json
from PyPDFForm import PdfWrapper, FormWrapper
import encodings
from datetime import datetime


path = 'anah_mpra_attestation_factures.pdf'
path_out = 'out.pdf'
# fields = fillpdfs.get_form_fields(path)
# for f in fields: print(f)

data_dict = {
    "Nom Prénom" : "Lionel du Peloux",
    "Coût des travaux en HT TTC Row1": '1200.00 € HT \n 1220,00 € TTC', 
}

def print_widgets(path):

    pdf_form_schema = PdfWrapper(path).schema
    for k,v in pdf_form_schema["properties"].items():
        print(f"{k} : {v['type']}")
    # print(f"{k}")



def create_grid():

    grid_view_pdf = PdfWrapper("anah_mprs_plan_financement.pdf").generate_coordinate_grid(
        color=(1, 0, 0), 
        margin=20)

    with open("anah_mprs_plan_financement_grid.pdf", "wb+") as output:
        output.write(grid_view_pdf.read())

def create_form():

    font_size = 10
    font="Courier"
    font_color=(0, 0, 0)
    bg_color=(1, 1, 1)
    border_width=0

    new_form = PdfWrapper("anah_mprs_plan_financement.pdf")
    new_form = new_form.create_widget(
        widget_type="text",
        name="nom",
        page_number=1,
        x=150,
        y=580,
        width=140,
        height=12,
        font=font, 
        font_size=font_size,
        font_color=font_color,
        bg_color=bg_color,
        border_width=border_width,
    )
    new_form = new_form.create_widget(
        widget_type="text",
        name="prenom",
        page_number=1,
        x=352,
        y=580,
        width=190,
        height=12,
        font=font, 
        font_size=font_size,
        font_color=font_color,
        bg_color=bg_color,
        border_width=border_width,
    )
    new_form = new_form.create_widget(
        widget_type="text",
        name="adress",
        page_number=1,
        x=162,
        y=567,
        width=400,
        height=12,
        font=font, 
        font_size=font_size,
        font_color=font_color,
        bg_color=bg_color,
        border_width=border_width,
    )

    with open("anah_mprs_plan_financementç_form.pdf", "wb+") as output:
        output.write(new_form.read())


if __name__ == "__main__" :

    create_grid()
    create_form()

    print_widgets("anah_mpra_attestation_factures.pdf")
    print("---")
    print_widgets("anah_mprs_plan_financement.pdf")


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
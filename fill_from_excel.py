import json
from pathlib import Path
from typing import IO, Any, Dict, Iterator, List, OrderedDict
from PyPDFForm import PdfWrapper, FormWrapper
import encodings
from datetime import datetime
import python_calamine
from pypdf import PdfReader, PdfWriter
import tablib
from openpyxl import load_workbook
from pydantic import BaseModel
from itertools import islice
from docxtpl import DocxTemplate
path = "anah_mpra_attestation_factures.pdf"
path_out = "out.pdf"
# fields = fillpdfs.get_form_fields(path)
# for f in fields: print(f)

data_dict = {
    "Nom Prénom": "Lionel du Peloux",
    "Coût des travaux en HT TTC Row1": "1200.00 € HT \n 1220,00 € TTC",
}


class FormFiller(BaseModel):
    template_filename: str
    output_filename: str
    fields: OrderedDict


def iter_excel_tablib(file: IO[bytes]) -> Iterator[dict[str, object]]:
    yield from tablib.Dataset().load(file).dict


def fill_pdf_template(data: dict, template_filepath: Path, editable=False):
    if template_filepath.suffix == ".pdf":
        # pdf_form_schema = PdfWrapper(str(template_filepath)).schema
        # print(json.dumps(pdf_form_schema, indent=4, sort_keys=True))
        if editable:
            filled = FormWrapper(str(template_filepath)).fill(data, flatten=False)
        else:
            filled = PdfWrapper(str(template_filepath)).fill(data)
        with open(
            f"tmp/{template_filepath.name.replace("template","output")}", "wb+"
        ) as output:
            output.write(filled.read())


def fill_pdf_template_pydpf(data: dict, template_filepath: Path):
    if template_filepath.suffix == ".pdf":
        # pdf_form_schema = PdfWrapper(str(template_filepath)).schema
        # print(json.dumps(pdf_form_schema, indent=4, sort_keys=True))
        reader = PdfReader(str(template_filepath))
        writer = PdfWriter()

        writer.append(reader)
        data["auditeur_siret"] = 12354654654689
        for page in writer.pages:
            writer.update_page_form_field_values(
                page,
                data,
                auto_regenerate=True,
            )

        with open(
            f"tmp/{template_filepath.name.replace("template","output")}", "wb+"
        ) as output_stream:
            writer.write(output_stream)


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
            # fill_pdf_template_pydpf(data=d, template_filepath=template_filepath)
            pass


def print_pdf_widgets(path):
    pdf_form_schema = PdfWrapper(path).schema
    print(json.dumps(pdf_form_schema, indent=4, sort_keys=True))
    print("")
    for k, v in pdf_form_schema["properties"].items():
        print(f"{k} : {v['type']}")
        # print(f"{k}")
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


def get_form_fillers(form_path="assets/form.xlsx") -> List[FormFiller]:
    wb = load_workbook(filename=form_path, data_only=True)
    form_fillers: List[FormFiller] = []
    for sheetname in wb.sheetnames:
        ws = wb[sheetname]

        if (
            ws["A1"].value == "TEMPLATE FILENAME"
            and ws["A2"].value == "OUTPUT FILENAME"
        ):
            # the sheet represent a form filler
            template_filename = ws["B1"].value
            output_filename = ws["B2"].value
            
            fields = OrderedDict()
            for i in range(4, ws.max_row + 1):
                k = ws[f"B{i}"].value
                v = ws[f"C{i}"].value
                if k != None and k != "":
                    # if isinstance(v, int) or isinstance(v, float):
                    #     v = str(v)
                    fields[k] = v

            form_filler = FormFiller(
                template_filename=template_filename,
                output_filename=output_filename,
                fields=fields,
            )

            form_fillers.append(form_filler)

    return form_fillers


def fill_forms(
    form_fillers: List[FormFiller],
    editable=False,
    template_base_dir: str = "assets/templates/",
    output_base_dir: str = "tmp/",
):
    for form_filler in form_fillers:
        
        template_filepath = str(
            Path(template_base_dir).joinpath(form_filler.template_filename)
        )

        output_filepath = str(
            Path(output_base_dir).joinpath(form_filler.output_filename)
        )
        
        fields = dict(form_filler.fields.items())
        
        if Path(form_filler.template_filename).suffix == ".pdf":
            if editable:
                filled = FormWrapper(template_filepath).fill(fields, flatten=False)
            else:
                filled = PdfWrapper(template_filepath).fill(fields, flatten=False)
            with open(output_filepath, "wb+") as output:
                output.write(filled.read())
        elif Path(form_filler.template_filename).suffix == ".docx":
            template = DocxTemplate(template_filepath)
            template.render(fields)
            template.save(output_filepath)

        pass


if __name__ == "__main__":
    # read()
    print_pdf_widgets("assets/templates/anah_mpra_attestation_cee.template.pdf")
    form_fillers = get_form_fillers("assets/form.xlsx")
    form_fillers = get_form_fillers("cccps/payan.xlsx")
    fill_forms(form_fillers)
    pass
    # print_widgets("assets/anah_mpra_plan_financement.template.pdf")

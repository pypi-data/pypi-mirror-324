import typer 
import ase.io   
import os
import json
import re
import pymatgen
from pymatgen.core import  Structure
app = typer.Typer()

@app.command()
def cif2midb():
    # read the cif and mcif files and find out the Formula, Reference and ICSDid(if available)
    # we use ase to find out needed information and fill the template_json

    template_json = {
    "Formula": "",
    "Method": "LKAG formula, total energies fitting, or spin spirals",
    "Basis set": "FP-LMTO, RS-LMTO-ASA, LMTO-ASA, KKR, LAPW, PW, CPA or PAW",
    "XC functional": "",
    "DFT code":"",
    "Reference": "",
    "Description": "",
    "MPid": "",
    "ICSDid": "",
    "Description": ""
    }


    #first of all we need to find out how many cif files are there in the current directory and process them one by one use the path
    # find out the cif files
    cif_file = []
    mcif_file = []
    # get the current running directory
    path = os.getcwd()
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".cif"):
                cif_file.append(os.path.join(root, file))
            if file.endswith(".mcif"):
                mcif_file.append(os.path.join(root, file))
    


    if len(cif_file) == 0:
        print("No cif file found in the current directory, try the mcif file")
    else:
        print("Processing cif files")
        # find out the formula, reference and ICSDid
        for cif in cif_file:
            atoms = ase.io.read(cif)
            formula = atoms.get_chemical_formula()
            template_json["Formula"] = formula
            # find out the reference
            with open(cif, 'r') as f:
                for line in f:
                    if "_citation_DOI" in line:
                        template_json["Reference"] = line.split()[1]
                        break
            # find out the ICSDid
            with open(cif, 'r') as f:
                for line in f:
                    if "_database_code_ICSD" in line:
                        template_json["ICSDid"] = line.split()[1]
                        break

            #if the template.json file already exists, we will delete it and create a new one
            if os.path.exists("template.json"):
                os.remove("template.json")
            # write the template_json to a json file
            with open("template.json", "w") as f:
                json.dump(template_json, f, indent=4)
            print("The template.json file has been created")
            print("Please fill in the rest of the information in the template.json file")
    
    if len(mcif_file) == 0:
        print("No mcif file found in the current directory, stop processing")
        return
    else:
        # find out the formula, reference and ICSDid
        # here we using the mcif file so we take pymatgen to process
        print("Processing mcif files")
        for mcif in mcif_file:
            structure = Structure.from_file(mcif)
            formula = structure.formula
            template_json["Formula"] = formula
            # find out the reference
            with open(mcif, 'r') as f:
                for line in f:
                    if "_citation_DOI" in line:
                        template_json["Reference"] = line.split()[1]
                        break
            # find out the ICSDid
            with open(mcif, 'r') as f:
                for line in f:
                    if "_database_code_ICSD" in line:
                        template_json["ICSDid"] = line.split()[1]
                        break

            if os.path.exists("template.json"):
                os.remove("template.json")
            # write the template_json to a json file
            with open("template.json", "w") as f:
                json.dump(template_json, f, indent=4)
            print("The template.json file has been created")
            print("Please fill in the rest of the information in the template.json file")

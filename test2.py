import pytesseract
import pdfplumber
import os
from PIL import Image
import time
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django
django.setup()
from Arch_App.models import Departement, Dossier, Fichier,Log

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

def extract_header_from_pdf(pdf_file, num_lines=10):
    header = ""
    try:
        with pdfplumber.open(pdf_file) as pdf:
            first_page = pdf.pages[0]
            for line in first_page.extract_text().split('\n')[:num_lines]:
                header += line + '\n'
    except Exception as e:
        print(f"Erreur lors de l'extraction de l'en-tête du fichier {pdf_file}: {e}")
    return header.strip()


def move_pdf_to_subfolder(pdf_file, target_subfolder):
    os.makedirs(target_subfolder, exist_ok=True)
    new_file_path = os.path.join(target_subfolder, os.path.basename(pdf_file))

    os.rename(pdf_file, new_file_path)

    element = target_subfolder.split("\\")
    id = Fichier.objects.order_by('-id').first()

    departement_id = Departement.objects.filter(nom=element[-2]).first().id
    print(departement_id)
    dossier = Dossier.objects.filter(nom=element[-1]).filter(departement_id=departement_id).first()

    pdf_file = open(new_file_path, "rb")
    pdf_file.seek(0,os.SEEK_END)
    size = pdf_file.tell()

    if dossier is not None:
        dossier_id = dossier.id
        dossier.size = dossier.size + size
    else:
        dbId = Dossier.objects.order_by('-id').first().id+1
        dossier = Dossier(dbId,element[-1],size,departement_id=departement_id)
    dossier.save()
    dossier_id = dossier.id
    
    file = Fichier(id,os.path.basename(new_file_path),new_file_path,size,dossier_id=dossier_id)
    file.save()
    log = Log()
    log.nature = "creation"
    log.size = size
    log.save()
    print(f"Fichier déplacé vers : {target_subfolder}")


def process_pdf_file(file_path, folder_keywords):
    # Extraction de l'en-tête à partir du PDF
    header = extract_header_from_pdf(file_path, num_lines=10)
    header_lower = header.lower()  # Convertir en minuscules pour recherche insensible à la casse

    for main_folder, keywords in folder_keywords.items():
        for key, value in keywords.items():
            for keyword in value:
                keyword_lower = keyword.lower()  # Convertir en minuscules pour recherche insensible à la casse
                if keyword_lower in header_lower:
                    target_subfolder = os.path.join(scan_directory, main_folder, key)
                    move_pdf_to_subfolder(file_path, target_subfolder)
                    return

def process_folders(scan_directory, main_folders, folder_keywords):
    for main_folder in main_folders:
        folder_path = os.path.join(scan_directory, main_folder)
        if not os.path.isdir(folder_path):
            continue

        for item in os.listdir(folder_path):
            file_path = os.path.join(folder_path, item)
            filename = os.path.basename(file_path)
            if os.path.isfile(file_path) and filename.endswith('.pdf'):
                process_pdf_file(file_path, folder_keywords)
            

if __name__ == "__main__":
    scan_directory = 'C:\\Users\\FAROUQ\\Desktop\\scan'

    main_folders = ['Informatique', 'Achats', 'Import', 'Back-Office', 'Ressources Humaines', 'Marketing', 'Finance']

    folder_keywords = {
        'Informatique': {
            'CV': ['stage']
        },
        'Achats': {
            'Liste': ['réseaux locaux'],
        },
        'Import': {
            'gestion': ['video games']
        },
        'Back-Office': {
            'sous-dossier7': ['mot_cle10'],
            'sous-dossier8': ['mot_cle11', 'mot_cle12']
        },
        'Ressources Humaines': {
            '00 - Demande de congé ': ['demande de depart en conge ']
        },
        'Marketing': {
            'sous-dossier10': ['mot_cle15']
        },
        'Finance': {
            'sous-dossier11': ['mot_cle16', 'mot_cle17']
        }
    }

    try:
        success_message = False
        while True:
            file_moved = False
            process_folders(scan_directory, main_folders, folder_keywords)
            if file_moved and not success_message:
                print("Fichier déplacé avec succès.")
                success_message = True
            elif not file_moved:
                success_message = False

            time.sleep(10)
            print("go")
    except KeyboardInterrupt:
        pass

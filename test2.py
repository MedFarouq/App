import pytesseract
import pdfplumber
import os
import csv
from PIL import Image
import time
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django
django.setup()
from Arch_App.models import Departement, Dossier, Fichier

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
    print ("123", pdf_file)
    target_path = os.path.join(target_subfolder)
    os.makedirs(target_path, exist_ok=True)
    new_file_path = os.path.join(target_path, os.path.basename(pdf_file))
    
    os.rename(pdf_file, new_file_path)

    element = target_subfolder.split("\\")
    id = Fichier.objects.order_by('-id').first().id+1

    departement_id = Departement.objects.filter(nom=element[1]).first().id
    dossier = Dossier.objects.filter(nom=element[2]).filter(departement_id=departement_id).first()
    
    pdf_file_name = pdf_file 
    pdf_file = open(pdf_file,"rb")
    pdf_file.seek(0,os.SEEK_END)
    size = pdf_file.tell()

    if dossier is not None:
        dossier_id = dossier.id
        dossier.size = dossier.size + size
    else: 
        dbId = Dossier.objects.order_by('-id').first().id+1
        dossier = Dossier(dbId,element[2],size,departement_id=departement_id)
    dossier.save()
    dossier_id = dossier.id

    
    file = Fichier(id,os.path.basename(pdf_file_name),new_file_path,size,dossier_id=dossier_id)
    file.save()
    print(f"Fichier déplacé vers : {target_subfolder}")

def update_csv(file_name, remove=False):
    csv_file = 'processed_files.csv'
    if os.path.exists(csv_file):
        with open(csv_file, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            processed_files = [row[0] for row in reader]
        
        if remove:
            processed_files = [f for f in processed_files if f != file_name]
        else:
            processed_files.append(file_name)

        with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            for file_name in processed_files:
                writer.writerow([file_name])

def process_pdf_file(file_path, folder_keywords):
    # Vérifier si le fichier PDF existe toujours
    if not os.path.exists(file_path):
        # Si le fichier n'existe plus, le supprimer du fichier CSV
        filename = os.path.basename(file_path)
        update_csv(filename, remove=True)
        return

    # Extraction de l'en-tête à partir du PDF
    header = extract_header_from_pdf(file_path, num_lines=10)
    header_lower = header.lower()  # Convertir en minuscules pour recherche insensible à la casse

    for main_folder, keywords in folder_keywords.items():
        folder_path = os.path.join(scan_directory, main_folder)
        for sub_folder in os.listdir(folder_path):
            target_subfolder = os.path.join(folder_path, sub_folder)
            for keyword in keywords:
                keyword_lower = keyword.lower()  # Convertir en minuscules pour recherche insensible à la casse
                if keyword_lower in header_lower:
                    move_pdf_to_subfolder(file_path, target_subfolder)
                    return

    # Ajouter le fichier à la liste des fichiers traités
    filename = os.path.basename(file_path)
    update_csv(filename)

def process_folders(scan_directory, main_folders, folder_keywords):
    csv_file = 'processed_files.csv'
    if os.path.exists(csv_file):
        with open(csv_file, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            processed_files = [row[0] for row in reader]
    else:
        processed_files = []
        
    for main_folder in main_folders:
        folder_path = os.path.join(scan_directory, main_folder)
        if not os.path.isdir(folder_path):
            continue

        for root, _, files in os.walk(folder_path):
            for filename in files:
                file_path = os.path.join(root, filename)
                if filename.endswith('.pdf') and filename not in processed_files:
                    process_pdf_file(file_path, folder_keywords)

if __name__ == "__main__":
    # Chemin du répertoire de scan
    scan_directory = 'C:/Users/FAROUQ/Desktop/scan'

    # Liste des noms de dossiers principaux
    main_folders = ['Informatique', 'Achats', 'import', 'back-office', 'ressources humaines', 'marketing', 'finance']

    # Dictionnaire des noms de dossiers principaux et de leurs sous-dossiers correspondants avec les mots-clés
    folder_keywords = {
        'Informatique': {
            'CV': ['stage'],
        },
        'Achats': {
            'Liste': ['réseaux locaux'],
        },
        'import': {
            'sous-dossier6': ['mot_cle9']
        },
        'back-office': {
            'sous-dossier7': ['mot_cle10'],
            'sous-dossier8': ['mot_cle11', 'mot_cle12']
        },
        'ressources humaines': {
            'sous-dossier9': ['mot_cle13', 'mot_cle14']
        },
        'marketing': {
            'sous-dossier10': ['mot_cle15']
        },
        'finance': {
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
    except KeyboardInterrupt:
        pass






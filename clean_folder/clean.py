import re
import sys
from pathlib import Path
import shutil

CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

TRANS = dict()

for cyrillic, latin in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(cyrillic)] = latin
    TRANS[ord(cyrillic.upper())] = latin.upper()

def normalize(name: str) -> str:
    translate_name = re.sub(r'[^A-Za-z0-9.]', '_', name.translate(TRANS))
    return translate_name

JPEG_IMAGES = []
JPG_IMAGES = []
PNG_IMAGES = []
SVG_IMAGES = []
AVI_VIDEO = []
MP4_VIDEO = []
MOV_VIDEO = []
MKV_VIDEO = []
DOC_DOC = []
DOCX_DOC = []
TXT_DOC = []
PDF_DOC = []
XLXS_DOC = []
PPTX_DOC = []
MP3_AUDIO = []
OGG_AUDIO = []
WAV_AUDIO = []
AMR_AUDIO = []
ZIP_ARCHIVES = []
GZ_ARCHIVES = []
TAR_ARCHIVES = []
MY_OTHER = []

REGISTER_EXTENSION = {
    'JPEG': JPEG_IMAGES,
    'JPG': JPG_IMAGES,
    'PNG': PNG_IMAGES,
    'SVG': SVG_IMAGES,
    "AVI": AVI_VIDEO,
    "MP4": MP4_VIDEO,
    "MOV": MOV_VIDEO,
    "MKV": MKV_VIDEO,
    "DOC": DOC_DOC,
    "DOCX": DOCX_DOC,
    "TXT": TXT_DOC,
    "PDF": PDF_DOC,
    "XLXS": XLXS_DOC,
    "PPTX": PPTX_DOC,
    "MP3": MP3_AUDIO,
    "OGG": OGG_AUDIO,
    "WAV": WAV_AUDIO,
    "AMR": AMR_AUDIO,
    "ZIP": ZIP_ARCHIVES,
    "GZ": GZ_ARCHIVES,
    "TAR": TAR_ARCHIVES,
}

FOLDERS = []
EXTENSIONS = set()
UNKNOWN = set()


def get_extension(name: str) -> str:
    return Path(name).suffix[1:].upper()

def scan(folder: Path):
    for item in folder.iterdir():
        if item.is_dir():
            if item.name not in ('archives', 'video', 'audio', 'documents', 'images', 'MY_OTHER'):
                FOLDERS.append(item)
                scan(item)
            continue

        extension = get_extension(item.name)  
        full_name = folder / item.name
        if not extension:
            MY_OTHER.append(full_name)
        else:
            try:
                ext_reg = REGISTER_EXTENSION[extension]
                ext_reg.append(full_name)
                EXTENSIONS.add(extension)
            except KeyError:
                UNKNOWN.add(extension) 
                MY_OTHER.append(full_name)
                
def handle_media(file_name: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    file_name.replace(target_folder / normalize(file_name.name))
    
def handle_docs(file_name: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    file_name.replace(target_folder / normalize(file_name.name))

def handle_archive(file_name: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    folder_for_file = target_folder / normalize(file_name.name.replace(file_name.suffix, ''))
    folder_for_file.mkdir(exist_ok=True, parents=True)
    try:
        shutil.unpack_archive(str(file_name.absolute()), str(folder_for_file.absolute()))
    except shutil.ReadError:
        folder_for_file.rmdir()
        return
    file_name.unlink()
    
def main(folder: Path):
    scan(folder)
    for file in JPEG_IMAGES:
       handle_media(file, folder / 'images' / 'JPEG')
    for file in JPG_IMAGES:
       handle_media(file, folder / 'images' / 'JPG')
    for file in PNG_IMAGES:
       handle_media(file, folder / 'images' / 'PNG')
    for file in SVG_IMAGES:
       handle_media(file, folder / 'images' / 'SVG')
    for file in AVI_VIDEO:
       handle_media(file, folder / 'video' / 'AVI')
    for file in MP4_VIDEO:
       handle_media(file, folder / 'video' / 'MP4')
    for file in MOV_VIDEO:
       handle_media(file, folder / 'video' / 'MOV')
    for file in MKV_VIDEO:
       handle_media(file, folder / 'video' / 'MKV')
    for file in DOC_DOC:
       handle_docs(file, folder / 'documents' / 'DOC')
    for file in DOCX_DOC:
       handle_docs(file, folder / 'documents' / 'DOCX')
    for file in TXT_DOC:
       handle_docs(file, folder / 'documents' / 'TXT')
    for file in PDF_DOC:
       handle_docs(file, folder / 'documents' / 'PDF')
    for file in XLXS_DOC:
       handle_docs(file, folder / 'documents' / 'XLXS')
    for file in PPTX_DOC:
       handle_docs(file, folder / 'documents' / 'PPTX')   
    for file in MP3_AUDIO:
       handle_media(file, folder / 'audio' / 'MP3_AUDIO')
    for file in OGG_AUDIO:
       handle_media(file, folder / 'audio' / 'OGG_AUDIO')
    for file in WAV_AUDIO:
       handle_media(file, folder / 'audio' / 'WAV_AUDIO')
    for file in AMR_AUDIO:
       handle_media(file, folder / 'audio' / 'AMR_AUDIO')
    for file in ZIP_ARCHIVES:
       handle_archive(file, folder / 'archives' / 'ZIP_ARCHIVES')
    for file in GZ_ARCHIVES:
       handle_archive(file, folder / 'archives' / 'GZ_ARCHIVES')
    for file in TAR_ARCHIVES:
       handle_archive(file, folder / 'archives' / 'TAR_ARCHIVES')
    for file in MY_OTHER:
       handle_media(file, folder / 'MY_OTHER')
  
   

    for folder in FOLDERS[::-1]:
        try:
            folder.rmdir()
        except OSError:
            print(f'Error during remove folder {folder}')

def start():
    if sys.argv[1]:
        folder_process = Path(sys.argv[1])
        main(folder_process)


if __name__ == "__main__":
    folder_process = Path(sys.argv[1])
    main(folder_process.resolve())
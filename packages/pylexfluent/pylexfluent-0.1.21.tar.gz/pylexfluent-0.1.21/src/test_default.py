
import logging
from typing import List 
import lxf.settings as settings
settings.set_logging_level(logging.DEBUG)
settings.enable_tqdm=False
logger = logging.getLogger('test_default')
fh = logging.FileHandler('./logs/test_default.log')
fh.setLevel(settings.get_logging_level())
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.setLevel(settings.get_logging_level())
logger.addHandler(fh)
#####################################################
from lxf.services.measure_time import measure_time_async
from lxf.services.try_safe import try_safe_execute_async
from lxf.extractors.default.default_extractor import  default_chunks_extractor
import asyncio
from lxf.ai.classification.classifier import extract_text_from_file
from lxf.ai.text_analysis.default_text_analysis import  extract_titles, summarize_chunks
from lxf.domain.extracted_data import ExtractedData

import os

# System call
os.system("")

# Class of different styles
class print_color():
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'
    


async def process_pdf_with_default_extractor(file_path: str)->None:
    """
    
    """
    extracted_text = await extract_text_from_file(file_path)
    
    if extracted_text:
       # print(f"\n\nExtrtacted Text:\n {extracted_text} \n\n")
        extracted_data = default_chunks_extractor(extracted_text)
        for chunk in extracted_data.chunks:
            print(print_color.BLUE+f"\nChunk {chunk.metadata.chunk}/{chunk.metadata.chunks}")
            print(print_color.YELLOW+f"{chunk.metadata.title}\n{chunk.metadata.description}\n{chunk.metadata.hierarchie}\n")
            print(print_color.CYAN+f"Content : \n{chunk.page_content}")
    else:
        print(print_color.RED+"Aucun texte n'a pu être extrait du PDF.")


async def test_extract_title(file_path:str)->List[str]:
    extracted_text=await extract_text_from_file(file_path)
    titles=extract_titles(extracted_text)
    for i , title  in enumerate(titles) :
        print(f"\nTitre {i} : {title}")


async def do_summarize(file_path):
    """
    """
    extracted_text = await extract_text_from_file(file_path)
    
    chunk_summaries = summarize_chunks(extracted_text) 

    print("\n Résumés des chunks :")
    for i, chunk_summary in enumerate(chunk_summaries):
        print(chunk_summary) 

    logger.info("Résumé terminé avec succès.")

if __name__ == "__main__":
    import asyncio
    file_path = "data/acte_vte.pdf"
    asyncio.run(process_pdf_with_default_extractor(file_path))
    #asyncio.run(do_summarize(file_path=file_path))
    #asyncio.run(test_extract_title(file_path))
    

    

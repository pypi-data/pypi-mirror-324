#######################################
import os
import logging
from lxf.settings import get_logging_level

logger = logging.getLogger('default extractor')
fh = logging.FileHandler('./logs/default_extractor.log')
fh.setLevel(get_logging_level())
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.setLevel(get_logging_level())
logger.addHandler(fh)
########################################


from lxf.ai.ocr.default_ocr import  lemmatize_and_extract_entities, segment_text_into_chunks
from lxf.services.try_safe import try_safe_execute_async
from lxf.domain.extracted_data import Chunk, ChunkMetadata, ExtractedData, ExtractedMetadata





# def default_chunks_extractor(full_file_path:str,**kwargs)->tuple[str,dict] :
#     logger.debug("Aucune donnee extraite depuis l'extracteur par defaut!")
#     return f'Defaut Extractor',None


def default_chunks_extractor(text: str) -> ExtractedData:
    """
    Effectue la segmentation, la lemmatisation, et la reconnaissance d'entités nommées sur un texte donné.
    """
    if text == None :
        logging.error("Le texte fourni est vide")
        return None
    chunks = segment_text_into_chunks(text)

    if chunks == None: 
        logging.error("Aucun chunk généré après la segmentation.")
        return  ExtractedData(metadata=ExtractedMetadata(), chunks=[])
    extracted_data = ExtractedData()
    extracted_data.metadata=ExtractedMetadata()
    extracted_data.chunks=[]
    for i, chunk_text in enumerate(chunks):
        lemmatized_text, entities = lemmatize_and_extract_entities(chunk_text)
        chunk = Chunk()
        chunk.metadata = ChunkMetadata()
        chunk.metadata.chunk=i + 1
        chunk.metadata.chunks=len(chunks),
        chunk.metadata.title=f"Chunk {i + 1}",
        chunk.metadata.source=""
        chunk.page_content = lemmatized_text  
        if entities:
            logging.debug(f"Entités détectées pour le chunk {i + 1}")
            entity_descriptions = []
            for e in entities:
                entity_descriptions.append(f"{e['text']} ({e['label']})")
            chunk.metadata.description += f"Entités détectées : {', '.join(entity_descriptions)}"
        else:
            chunk.metadata.description = "Aucune entité détectée."
            logging.debug(f"Aucune entité détectée pour le chunk {i + 1}.")
        extracted_data.chunks.append(chunk)

    return extracted_data





##### Sementic splitting 
    #         volume_name = extract_volume_name(object_key) or bucket
    #         name_collection = volume_name

    #         store = get_vectors_store(collection_name=name_collection, url=url, port=port, apikey=api_key, embeddings=embeddings)

    #         ext = full_file_path.rpartition(".")[-1].strip().upper()
    #         loader = None

    #         if ext == PDF:
    #             loader = PyPDFLoader(full_file_path)
    #         elif ext in [DOC, DOCX]:
    #             loader = Docx2txtLoader(full_file_path)
    #         else:
    #             loader = UnstructuredFileLoader(full_file_path)

    #         documents: List[Document] = loader.load()
    #         text = "".join([sanitize_text(doc.page_content) for doc in documents])

    #         segments = segment_text_into_chunks(text)
    #         nbr_segments = len(segments)
    #         document_name = os.path.basename(object_key)
    #         new_docs: List[Document] = []
    #         for segment in segments:
    #             metadata = {
    #                 'source': object_key,
    #                 'ext': ext,
    #                 'bucket': bucket,
    #                 'nombre de chunks': nbr_segments,
    #                 'tags': {'volume_name': volume_name, 'document_name': document_name}
    #             }
    #             new_doc = Document(page_content=segment, metadata=metadata)
    #             new_docs.append(new_doc)

    #         store.add_documents(new_docs)
    #         logger.debug(f"Documents ajoutés avec succès dans la collection {name_collection}.")

    #     result = update_job_status(unit_of_work.indexation_repository(), job_to_update.id, "completed")
    #     if result:
    #         check_and_delete_file_if_jobs_completed(unit_of_work.job_repository(), parent_id, full_file_path)
    #     else:
    #         logger.warning(f"Premier essai de mise à jour du statut pour Id {job_id} a échoué.")
    #         time.sleep(0.3)
    #         result = update_job_status(unit_of_work.indexation_repository(), job_to_update.id, "completed")
    #         if result:
    #             check_and_delete_file_if_jobs_completed(unit_of_work.job_repository(), parent_id, full_file_path)
    #         else:
    #             logger.error(f"Second essai de mise à jour du statut pour Id {job_id} a échoué.")

    # except Exception as ex:
    #     logger.exception(f"Une erreur s'est produite lors de l'ajout du fichier à la collection : {ex}")
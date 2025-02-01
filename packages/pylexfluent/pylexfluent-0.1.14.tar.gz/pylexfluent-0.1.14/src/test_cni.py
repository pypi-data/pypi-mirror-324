import logging
import asyncio
import os
import sys
from typing import List


from lxf.services.measure_time import measure_time_async
import lxf.settings as settings
settings.set_logging_level(logging.DEBUG)
settings.enable_tqdm=False
###################################################################

logger = logging.getLogger('test_cni')
fh = logging.FileHandler('./logs/test_cni.log')
fh.setLevel(settings.get_logging_level())
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.setLevel(settings.get_logging_level())
logger.addHandler(fh)
#################################################################

from lxf.domain.cni import Cni
from lxf.services.try_safe import try_safe_execute_async
from lxf.extractors.administratif.cni_extractor import extract_data

@measure_time_async
async def do_test_cni(filename:str):
    """
    """
    return await try_safe_execute_async(logger,extract_data,file_path=filename)


if __name__ == "__main__":

    file_path = "data/cni.pdf"
    cni_candidates:List[Cni] = asyncio.run(do_test_cni(filename=file_path))

    if cni_candidates:
        for cni in cni_candidates:
            print(cni)
    else:
        print("Aucune CNI trouvée.")

import logging
import sys


from lxf.settings import set_logging_level, get_logging_level  
set_logging_level(logging.DEBUG)

from lxf.services.measure_time import measure_time_async
from lxf.services.try_safe import try_safe_execute_asyncio



from lxf.ai.classification.classifier import get_classification
from lxf.domain.predictions import  Predictions

import lxf.settings as settings 

###################################################################

logger = logging.getLogger('test classifier')
fh = logging.FileHandler('./logs/test_classifier.log')
fh.setLevel(get_logging_level())
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.setLevel(get_logging_level())
logger.addHandler(fh)
#################################################################

@measure_time_async
async def do_test(file_name) -> Predictions :
    """
    """
    return await get_classification(file_name=file_name,max_pages=10)


if __name__ == "__main__":
    sys.stdout.reconfigure(line_buffering=True) 
    pdf_path = "data/ODP.pdf"
    iban_pdf="data/RIBB.pdf"
    result = try_safe_execute_asyncio(logger=logger,func=do_test,file_name=iban_pdf) #asyncio.run(do_test(iban_pdf))
    print(result)    
    result = try_safe_execute_asyncio(logger=logger,func=do_test,file_name=pdf_path) #asyncio.run(do_test(pdf_path))
    print(result)

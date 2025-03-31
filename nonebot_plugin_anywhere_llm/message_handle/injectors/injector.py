from collections import OrderedDict, defaultdict
import datetime
from ...utils import logger
from typing import Callable, Dict, List, Tuple


class InformationInjector:
    def __init__(self):

        self.injectors: Dict[str, Tuple[int, Callable[[str], str]]] = OrderedDict()
    
    def register_injector(self, name: str, 
                         injector: Callable[[str], str],
                         priority: int = 0,) -> None:
        self.injectors[name] = (priority, injector)
        
    
    def inject(self, system_prompt: Dict[str, str]) -> None:
        
     
        context = system_prompt['content']
        for name, (_, injector) in sorted(self.injectors.items(), 
                                       key=lambda x: x[1][0]):
            
            try:
                context += injector(context)
            except Exception as e:
                logger.warning(repr(e))
                continue
            
        system_prompt['content'] = context
            

                    
    
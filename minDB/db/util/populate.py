import datetime
import sys
from typing import Dict, Any, Optional
import torch


def generate_field(content: str, vector: Optional[torch.Tensor] = None) -> Dict[str, Any]:
  """Generates a field for a database""" 
  content = {
    "metadata": {
      "time": datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
      "size": sys.getsizeof(content)
    }, 
    "content": content,
    "vector": vector,
    "md5": None # TODO: implement MD5 algorithm
  }

  return content
from pydantic import create_model
from typing import ClassVar



model_2 = create_model('LoginModel',username = str,password=str)


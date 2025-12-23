from pwdlib import PasswordHash
from fastapi import HTTPException

hash = PasswordHash.recommended()

async def v_hash(hash_t:str,password:str):
    if hash_t == None:
        raise HTTPException(status_code=401,detail='Неверный логин или пароль')
    p_h = hash.verify(password,hash_t)
    return  p_h

async def create_hash(password:str):
    return hash.hash(password)

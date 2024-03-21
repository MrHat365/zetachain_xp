"""
  @ Author:   Mr.Hat
  @ Date:     2024/3/21 01:59
  @ Description: 
  @ History:
"""
import random


async def random_line(filepath: str, delete: bool = True):
    with open(filepath, 'r') as file:
        keys = file.readlines()

    if not keys:
        return False
    random_key = random.choice(keys)
    if delete:
        keys.remove(random_key)

        with open(filepath, 'w') as file:
            file.writelines(keys)

    return random_key.strip()
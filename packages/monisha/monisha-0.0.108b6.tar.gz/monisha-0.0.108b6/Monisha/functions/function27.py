import asyncio
from .function09 import Storage
#=================================================================================

class Queue:

    async def queue(cid, wait=1, maximum=1):
        while cid in Storage.USER_TID:
            if Storage.USER_TID.index(cid) + 1 > maximum:
                await asyncio.sleep(wait)
            else:
                break

#=================================================================================

    async def message(imog, text, button=None, maximum=1):
        if maximum < len(Storage.USER_TID):
            try: await imog.edit(text=text, reply_markup=button)
            except Exception: pass

#=================================================================================

    async def delete(tid):
        Storage.USER_TID.remove(tid) if tid in Storage.USER_TID else 0

    async def position(tid):
        return Storage.USER_TID.index(tid) if tid in Storage.USER_TID else 0

    async def add(tid):
        Storage.USER_TID.append(tid) if tid not in Storage.USER_TID else None

#=================================================================================

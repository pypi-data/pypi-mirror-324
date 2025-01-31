import pytz
from datetime import datetime
#===============================================================================

class SchedulER:

    async def get20():
        nowaes = datetime.now(tz=pytz.timezone("Asia/Kolkata"))
        mineed = nowaes.replace(hour=0, minute=0, second=0, microsecond=0)
        return (mineed - nowaes).seconds

#===============================================================================

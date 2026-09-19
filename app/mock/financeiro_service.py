import random
import asyncio
from app.models.err_msg import CustomError
from app.models.service_interface import ServiceInterface

class MockFinancialInterface(ServiceInterface):
    def __init__(self, rate_of_failure:float=0.2):
        self.failure_rate=rate_of_failure
        self.name = "Financial Service"

    async def mock_wait_time(self):
        wait_time = random.randint(1,10)
        await asyncio.sleep(wait_time)

    async def mock_call_endpoint(self):
        is_failed_call = random.random() <= self.failure_rate
        await self.mock_wait_time()
        if not is_failed_call:
            return "OK"
        raise CustomError("Unknown Error calling Financial service")
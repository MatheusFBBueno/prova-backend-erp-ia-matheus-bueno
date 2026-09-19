from app.mock.cliente_service import MockClientInterface
from app.mock.estoque_service import MockStockInterface
from app.mock.financeiro_service import MockFinancialInterface
from app.models.err_msg import CustomError
from app.models.status_msg import StatusMessage
import asyncio


class ServiceCaller:
    def __init__(self):
        self.max_retries = 5
        pass

    async def call_service_with_retry(self,service, timeout):
        tries = 0
        return_val = StatusMessage("Empty","")
        while tries < self.max_retries:
            try:
                return_msg:str = await asyncio.wait_for(service.mock_call_endpoint(), timeout=timeout)
            except asyncio.TimeoutError:
                print(f"Timeout chamando {service.name}, tentando novamente")
                return_val = StatusMessage("Timeout", f"Requisição para {service.name} teve timeout")
                tries += 1
                continue
            except CustomError as e:
                print(f"Erro chamando {service.name}, tentando novamente")
                return_val = StatusMessage("Fail", e.error)
                tries += 1
                continue

            return_val = StatusMessage("Success", return_msg)
            break
        return return_val

    async def make_request_service(self, mockinterface):
        mockinterface.mock_call_endpoint()
    

    async def call_and_wait_services(self):
        # chamando serviços com timeouts arbitrarios
        client, stock, fin = await asyncio.gather(self.call_service_with_retry(MockClientInterface(),5),
                                                  self.call_service_with_retry(MockStockInterface(),2),
                                                  self.call_service_with_retry(MockFinancialInterface(),7))
        
        
        print(f"Client returned status {client.get_status()} and message {client.get_message()}")
        print(f"Stock returned status {stock.get_status()} and message {stock.get_message()}")
        print(f"Financial returned status {fin.get_status()} and message {fin.get_message()}")
        return {"Client service":f"Client returned status {client.get_status()} and message {client.get_message()}",
                "Stock service":f"Stock returned status {stock.get_status()} and message {stock.get_message()}",
                "Financial service": f"Financial returned status {fin.get_status()} and message {fin.get_message()}"}
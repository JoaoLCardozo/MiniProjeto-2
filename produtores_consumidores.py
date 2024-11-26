import threading
import time
from buffer import Buffer

class Trabalhador(threading.Thread):
    """
    Classe base para produtores e consumidores.
    """
    def __init__(self, buffer, id_trabalhador, timesteps, delay):
        threading.Thread.__init__(self)
        self.buffer = buffer
        self.id_trabalhador = id_trabalhador
        self.timesteps = timesteps
        self.delay = delay

class Produtor(Trabalhador):
    """
    Produtor que adiciona itens ao buffer.
    """
    def run(self):
        for t in range(self.timesteps):
            item = f"Peça_{self.id_trabalhador}_{t}"
            self.buffer.adicionar_item(item)
            time.sleep(self.delay)  # Simula o tempo de produção

class Consumidor(Trabalhador):
    """
    Consumidor que remove itens do buffer.
    """
    def run(self):
        for t in range(self.timesteps):
            self.buffer.remover_item()
            time.sleep(self.delay)  # Simula o tempo de consumo

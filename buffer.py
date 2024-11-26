import threading

class Buffer:
    """
    Implementa um buffer com capacidade limitada para controle de concorrência usando semáforos e mutex.
    """
    def __init__(self, capacidade):
        self.capacidade = capacidade
        self.buffer = []
        self.mutex = threading.Lock()  # Garante acesso único ao buffer
        self.espaco_disponivel = threading.Semaphore(capacidade)  # Espaços disponíveis no buffer
        self.itens_disponiveis = threading.Semaphore(0)  # Itens disponíveis para consumo

    def adicionar_item(self, item):
        """
        Adiciona um item ao buffer, bloqueando caso o buffer esteja cheio.
        """
        self.espaco_disponivel.acquire()  # Aguarda por espaço disponível
        with self.mutex:
            self.buffer.append(item)
            print(f"[PRODUTOR] Item {item} adicionado. Buffer: {len(self.buffer)}/{self.capacidade}.")
        self.itens_disponiveis.release()  # Notifica que há um item disponível

    def remover_item(self):
        """
        Remove um item do buffer, bloqueando caso o buffer esteja vazio.
        """
        self.itens_disponiveis.acquire()  # Aguarda por um item disponível
        with self.mutex:
            item = self.buffer.pop(0)
            print(f"[CONSUMIDOR] Item {item} removido. Buffer: {len(self.buffer)}/{self.capacidade}.")
        self.espaco_disponivel.release()  # Notifica que há espaço disponível
        return item

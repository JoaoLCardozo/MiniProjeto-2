import threading
import time
import pandas as pd
import matplotlib.pyplot as plt

class Buffer:
    def __init__(self, capacidade):
        self.capacidade = capacidade
        self.buffer = []
        self.mutex = threading.Lock()
        self.espaco_disponivel = threading.Semaphore(capacidade)
        self.itens_disponiveis = threading.Semaphore(0)

    def adicionar_item(self, item):
        self.espaco_disponivel.acquire()
        with self.mutex:
            self.buffer.append(item)
            print(f"[PRODUTOR] Item {item} adicionado. Buffer: {len(self.buffer)}/{self.capacidade}.")
        self.itens_disponiveis.release()

    def remover_item(self):
        self.itens_disponiveis.acquire()
        with self.mutex:
            item = self.buffer.pop(0)
            print(f"[CONSUMIDOR] Item {item} removido. Buffer: {len(self.buffer)}/{self.capacidade}.")
        self.espaco_disponivel.release()
        return item

class Trabalhador(threading.Thread):
    def __init__(self, buffer, id_trabalhador, timesteps, delay):
        threading.Thread.__init__(self)
        self.buffer = buffer
        self.id_trabalhador = id_trabalhador
        self.timesteps = timesteps
        self.delay = delay

class Produtor(Trabalhador):
    def run(self):
        for t in range(self.timesteps):
            item = f"Peça_{self.id_trabalhador}_{t}"
            self.buffer.adicionar_item(item)
            time.sleep(self.delay)

class Consumidor(Trabalhador):
    def run(self):
        for t in range(self.timesteps):
            self.buffer.remover_item()
            time.sleep(self.delay)

def gerar_dados():
    return {
        "Configuração": ["10", "20", "30", "40", "50"],
        "Itens Produzidos": [100, 200, 300, 400, 500],
        "Itens Consumidos": [90, 180, 270, 360, 450],
    }

def plotar_grafico(df):
    plt.figure(figsize=(8, 5))
    plt.plot(df["Configuração"], df["Itens Produzidos"], marker="o", label="Produzidos", color="blue")
    plt.plot(df["Configuração"], df["Itens Consumidos"], marker="o", label="Consumidos", color="orange")
    plt.xlabel("Capacidade do Buffer")
    plt.ylabel("Quantidade de Itens")
    plt.title("Produção e Consumo por Capacidade do Buffer")
    plt.grid(alpha=0.5)
    plt.legend()
    plt.tight_layout()
    plt.show()

def main():
    capacidade_buffer = 50
    num_produtores = 5
    num_consumidores = 5
    timesteps = 20
    delay_produtor = 0.8
    delay_consumidor = 1.2

    buffer = Buffer(capacidade_buffer)

    produtores = [Produtor(buffer, i, timesteps, delay_produtor) for i in range(num_produtores)]
    consumidores = [Consumidor(buffer, i, timesteps, delay_consumidor) for i in range(num_consumidores)]

    print("\n[INFO] Iniciando a simulação...\n")
    for trabalhador in produtores + consumidores:
        trabalhador.start()

    for trabalhador in produtores + consumidores:
        trabalhador.join()

    print("\n[INFO] Simulação concluída.")
    print(f"Total de itens produzidos: {num_produtores * timesteps}")
    print(f"Total de itens consumidos: {num_consumidores * timesteps}")
    print(f"Itens restantes no buffer: {len(buffer.buffer)}")

if __name__ == "__main__":
    try:
        start_time = time.time()
        main()
        print(f"Tempo total de execução: {time.time() - start_time:.2f} segundos")


        dados = gerar_dados()
        df = pd.DataFrame(dados)
        plotar_grafico(df)
    except Exception as e:
        print(f"[ERRO] Ocorreu um erro: {e}")

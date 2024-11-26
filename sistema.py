from buffer import Buffer
from produtores_consumidores import Produtor, Consumidor
import time

def main():
    """
    Simula a interação de produtores e consumidores com um buffer compartilhado.
    """
    # Configurações do sistema
    capacidade_buffer = 50
    num_produtores = 5
    num_consumidores = 5
    timesteps = 20
    delay_produtor = 0.8
    delay_consumidor = 1.2

    # Inicializa o buffer
    buffer = Buffer(capacidade_buffer)

    # Cria produtores e consumidores
    produtores = [Produtor(buffer, i, timesteps, delay_produtor) for i in range(num_produtores)]
    consumidores = [Consumidor(buffer, i, timesteps, delay_consumidor) for i in range(num_consumidores)]

    # Inicia threads
    print("\n[INFO] Iniciando a simulação...\n")
    for trabalhador in produtores + consumidores:
        trabalhador.start()

    # Aguarda threads finalizarem
    for trabalhador in produtores + consumidores:
        trabalhador.join()

    # Relatório final
    print("\n[INFO] Simulação concluída.")
    print(f"Total de itens produzidos: {num_produtores * timesteps}")
    print(f"Total de itens consumidos: {num_consumidores * timesteps}")
    print(f"Itens restantes no buffer: {len(buffer.buffer)}")

if __name__ == "__main__":
    try:
        start_time = time.time()
        main()
        print(f"Tempo total de execução: {time.time() - start_time:.2f} segundos")
    except Exception as e:
        print(f"[ERRO] Ocorreu um erro: {e}")

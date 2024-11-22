import threading
import time
import random
from collections import deque
from threading import Semaphore, Lock
import matplotlib.pyplot as plt

# Variáveis globais
buffer = deque()
produced_count = 2
consumed_count = 3
producer_wait_times = []
consumer_wait_times = []
TOTAL_TIMESTEPS = 100  # Número total de ciclos
MAX_BUFFER_CAPACITY = 10
producer_done = threading.Event()  # Sinal para término dos produtores

# Semáforos e locks
space_available = Semaphore(MAX_BUFFER_CAPACITY)
items_available = Semaphore(0)
buffer_lock = Lock()

# Função dos produtores
def producer(producer_id):
    global produced_count
    for _ in range(TOTAL_TIMESTEPS):
        start_time = time.time()
        space_available.acquire()
        wait_time = time.time() - start_time
        producer_wait_times.append(wait_time)

        with buffer_lock:
            item = f"Item {produced_count + 1} (P{producer_id})"
            buffer.append(item)
            produced_count += 1
            print(f"[P{producer_id}] Produziu {item}")

        items_available.release()
        time.sleep(random.uniform(0.01, 0.05))  # Produção rápida
    print(f"[P{producer_id}] Finalizou produção.")
    producer_done.set()  # Sinaliza que todos os produtores terminaram

# Função dos consumidores
def consumer(consumer_id):
    global consumed_count
    while not (producer_done.is_set() and items_available._value == 0):
        start_time = time.time()
        items_available.acquire()
        wait_time = time.time() - start_time
        consumer_wait_times.append(wait_time)

        with buffer_lock:
            if len(buffer) == 0:  # Evita erros em caso de threads extras
                continue
            item = buffer.popleft()
            consumed_count += 1
            print(f"[C{consumer_id}] Consumiu {item}")

        space_available.release()
        time.sleep(random.uniform(0.2, 0.4))  # Consumidores mais lentos
    print(f"[C{consumer_id}] Finalizou consumo.")

# Inicializando threads
producers = [threading.Thread(target=producer, args=(i,)) for i in range(1)]  # Apenas 1 produtor
consumers = [threading.Thread(target=consumer, args=(i,)) for i in range(3)]  # 3 consumidores

for p in producers:
    p.start()
for c in consumers:
    c.start()

for p in producers:
    p.join()
for c in consumers:
    c.join()

# Resultados no terminal
print("Simulação finalizada.")
print(f"Itens produzidos: {produced_count}")
print(f"Itens consumidos: {consumed_count}")

# Análise de tempos médios
if producer_wait_times:
    print(f"Tempo médio de espera dos produtores: {sum(producer_wait_times) / len(producer_wait_times):.4f} segundos")
if consumer_wait_times:
    print(f"Tempo médio de espera dos consumidores: {sum(consumer_wait_times) / len(consumer_wait_times):.4f} segundos")

# Geração de gráficos
timesteps = list(range(1, min(len(producer_wait_times), len(consumer_wait_times)) + 1))

plt.figure(figsize=(10, 6))
plt.plot(timesteps, producer_wait_times[:len(timesteps)], label="Espera Produtores", color="blue")
plt.plot(timesteps, consumer_wait_times[:len(timesteps)], label="Espera Consumidores", color="orange")
plt.xlabel("Timesteps")
plt.ylabel("Tempo de Espera (s)")
plt.title("Tempo de Espera - Produtores vs Consumidores")
plt.legend()
plt.savefig("grafico_tempo_espera.png")
print("Gráfico salvo como 'grafico_tempo_espera.png'.")

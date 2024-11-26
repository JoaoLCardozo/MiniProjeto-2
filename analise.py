import pandas as pd
import matplotlib.pyplot as plt

def gerar_dados():
    """
    Gera dados simulados para análise.
    """
    return {
        "Configuração": ["10", "20", "30", "40", "50"],
        "Itens Produzidos": [100, 200, 300, 400, 500],
        "Itens Consumidos": [90, 180, 270, 360, 450],
    }

def plotar_grafico(df):
    """
    Plota um gráfico comparativo de produção e consumo com base nos dados fornecidos.
    """
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

if __name__ == "__main__":
    dados = gerar_dados()
    df = pd.DataFrame(dados)
    plotar_grafico(df)

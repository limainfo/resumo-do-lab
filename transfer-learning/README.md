# Transfer Learning — Guia Prático (baseado no ml4a-guides)

Este projeto demonstra **transfer learning** para classificação de imagens em um conjunto de dados relativamente pequeno, reaproveitando uma CNN pré-treinada (ex.: VGG, ResNet, MobileNet) e **afinando** (fine-tuning) as últimas camadas para a sua tarefa. O material é baseado no notebook *Transfer Learning* do repositório **ml4a-guides**. ([GitHub][1])

> **O que você vai ver**
>
> * Carregar um dataset de imagens e dividir em *train/val/test*;
> * Extrair features de uma rede pré-treinada e treinar um *head* classificatório;
> * *Freeze/unfreeze* de camadas para fine-tuning;
> * Avaliação (accuracy, matriz de confusão) e inferência.

---

## Links

* **Abrir no Colab:**
  `https://colab.research.google.com/github/kylemath/ml4a-guides/blob/master/notebooks/transfer-learning.ipynb`  ([Google Colab][2])

* **Repo base (ml4a-guides):**
  `https://github.com/kylemath/ml4a-guides`  — contém notebooks e instruções (inclui script para baixar datasets em `data/download.sh`). ([GitHub][3])

* **Leitura complementar (TensorFlow):** Tutorial oficial de transfer learning e fine-tuning. ([TensorFlow][4])

---

## Requisitos

Você pode executar **direto no Google Colab** (recomendado) — não é necessário preparar ambiente local.

Para executar **localmente**, instale:

* Python 3.8+
* TensorFlow/Keras
* NumPy, Matplotlib, etc.

O repositório *ml4a-guides* também oferece um **container Docker** e scripts de execução (`run.sh`) para rodar Jupyter localmente. Veja a seção “Running the container” no README do repositório. ([GitHub][3])

---

## Como executar

### Opção A — Google Colab (mais simples)

1. Abra o link do Colab (acima). ([Google Colab][2])
2. No Colab, vá em **Runtime → Run all** para executar todas as células.
3. Ajuste caminhos/hiperparâmetros conforme seu dataset.

### Opção B — Local com Docker (do repo base)

1. Clone o repositório base:

   ```bash
   git clone https://github.com/kylemath/ml4a-guides.git
   cd ml4a-guides
   ```
2. (Opcional) Baixe datasets padrão:

   ```bash
   cd data
   ./download.sh
   ```

   > Observação: em macOS/Windows pode ser necessário instalar **unrar**. ([GitHub][3])
3. Volte à raiz do repo e construa/rode o container:

   ```bash
   docker build . -t ml4a
   ./run.sh
   ```

   O Jupyter Notebook abrirá em `http://localhost:8888`. ([GitHub][3])

---

## Dataset

O notebook utiliza um **dataset de imagens públicas** (ex.: Caltech-101 ou Cats vs Dogs). Você pode:

* Usar o **script `data/download.sh`** do repo base para baixar datasets de exemplo; ou
* Substituir por **seu próprio conjunto de imagens**, mantendo a mesma estrutura de pastas (uma pasta por classe). ([GitHub][3], [TensorFlow][4])

> Dica: caso use Caltech-101, organize as classes em pastas e garanta número mínimo de imagens por classe para evitar overfitting extremo.

---

## Estrutura típica do notebook

1. **Importações & Configuração**
   Carrega TensorFlow/Keras e define hiperparâmetros (tamanho de imagem, batch size, learning rate).

2. **Carregamento/Preparação dos dados**

   * Leitura das imagens;
   * *Split* em treino/validação/teste;
   * *Data augmentation* opcional.

3. **Modelo pré-treinado**

   * Carrega a **base convolucional** com pesos pré-treinados (ex.: ImageNet);
   * **Congela** camadas (feature extractor) e adiciona *head* denso para classificação.

4. **Treino do *head***

   * Treina somente o topo (camadas novas) até convergir.

5. **Fine-tuning**

   * Descongela parte das últimas camadas da base;
   * Re-treina com **taxa de aprendizado menor**.

6. **Avaliação & Inferência**

   * Métricas em validação/teste;
   * Predição em novas imagens.

Para uma referência conceitual e exemplos em Keras, veja o guia de Transfer Learning da TensorFlow. ([TensorFlow][4])

---

## Problemas comuns

* **Caminho de dataset inválido:** verifique a raiz do dataset e os nomes das pastas por classe.
* **Memória insuficiente:** reduza `image_size`, `batch_size` ou congele mais camadas.
* **Baixa acurácia:** adote *augmentation*, equalize número de amostras por classe, ajuste LR/épocas.

---

## Licença & Créditos

Este README foi elaborado com base no notebook **transfer-learning.ipynb** e nas instruções do repositório **ml4a-guides** (licença **GPL-2.0**). Consulte o repositório original para detalhes de licença, dados e scripts auxiliares. ([GitHub][3])

---

[1]: https://github.com/kylemath/ml4a-guides?utm_source=chatgpt.com "practical guides, tutorials, and code samples for ml4a"
[2]: https://colab.research.google.com/github/kylemath/ml4a-guides/blob/master/notebooks/transfer-learning.ipynb?utm_source=chatgpt.com "transfer-learning.ipynb"
[3]: https://github.com/kylemath/ml4a-guides "GitHub - kylemath/ml4a-guides: practical guides, tutorials, and code samples for ml4a"
[4]: https://www.tensorflow.org/tutorials/images/transfer_learning?utm_source=chatgpt.com "Transfer learning and fine-tuning | TensorFlow Core"

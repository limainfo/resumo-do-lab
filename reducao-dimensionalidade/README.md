# Conversor de Imagens “na raça” (RGB → Cinza → PB)

Script em Python que:

1. Lê **qualquer** formato de imagem suportado pelo OpenCV (JPG, PNG, BMP, TIFF, WebP, etc.);
2. Converte para **matriz RGB** (lista de listas, sem `cvtColor`);
3. Converte **RGB → tons de cinza** usando a luminância **BT.601** (cálculo manual);
4. Converte **cinza → preto e branco** por **limiar** (Otsu automático ou manual);
5. Exibe as imagens em janelas e, opcionalmente, **salva** os resultados.

> **Observação didática:** Todas as transformações de pixels (RGB→cinza e cinza→PB) são feitas “na raça”, com loops e fórmulas, **sem** usar funções prontas de conversão do OpenCV.

---

## Requisitos

* Python 3.8+
* [opencv-python](https://pypi.org/project/opencv-python/)
* numpy

Instalação:

```bash
pip install --upgrade opencv-python numpy
```

> Se você acidentalmente instalou o pacote `cv` (que não é o OpenCV), remova-o:

```bash
pip uninstall -y cv
```

---

## Arquivo principal

* `machine-converte-images.py`

---

## Uso

```bash
python .\machine-converte-images.py .\caminho\para\imagem.jpg [--save] [--manual-threshold N]
```

Exemplos:

```bash
# Abrir imagem, calcular Otsu automaticamente e exibir janelas
python .\machine-converte-images.py ".\teste.jpeg"

# Idem, mas também salvar as saídas (saida_gray.png e saida_bw.png)
python .\machine-converte-images.py ".\teste.jpeg" --save

# Usar limiar manual (ex.: 128) em vez de Otsu
python .\machine-converte-images.py ".\teste.jpeg" --manual-threshold 128 --save
```

**Tecla para sair:** com as janelas focadas, pressione qualquer tecla (o script usa `cv.waitKey(0)`).

---

## Opções

* `--save`
  Salva as imagens geradas como `saida_gray.png` e `saida_bw.png`.

* `--manual-threshold N` (0..255)
  Usa limiar fixo para binarização. Se omitido, o limiar é escolhido automaticamente pelo método de **Otsu** (implementado manualmente).

---

## Como funciona (resumo)

* **Leitura universal:** `cv.imread` carrega a imagem (BGR). O código **não** usa `cv.cvtColor` para converter: ele monta manualmente uma **matriz RGB** `List[List[Tuple[int,int,int]]]`.

* **RGB → Cinza (manual):**
  $Y = 0.299R + 0.587G + 0.114B$ (ITU-R BT.601), com *clamp* para 0..255.

* **Cinza → PB (manual):**

  * **Otsu:** constrói histograma 0..255, calcula variância entre classes e escolhe o melhor limiar.
  * **Binarização:** pixels `<= limiar` viram **preto (255)** e `> limiar` viram **branco (0)** (pode inverter facilmente no código).

* **Exibição/salvamento:** apenas para **I/O** e **janelas**; as matrizes são convertidas de volta para `numpy.uint8` para `cv.imshow` / `cv.imwrite`.

---

## Estrutura do código (principais funções)

* `read_image_to_rgb_matrix(path) -> (rgb_matrix, h, w)`
  Lê a imagem e retorna uma matriz RGB (lista de listas), altura e largura.

* `rgb_to_gray(rgb, h, w) -> gray_matrix`
  Converte cada `(R,G,B)` em um valor de cinza 0..255 (BT.601).

* `otsu_threshold(gray, h, w) -> int`
  Calcula limiar ótimo (0..255) pelo método de Otsu (implementação própria).

* `gray_to_bw(gray, h, w, threshold) -> bw_matrix`
  Binariza a matriz de cinza (0/255).

* `*_matrix_to_numpy(...)`
  Converte as matrizes de listas para `numpy` (necessário para `imshow`/`imwrite`).

---

## Solução de problemas

* **`AttributeError: module 'cv' has no attribute 'imread'`**
  Você importou o módulo errado. Use:

  ```python
  import cv2 as cv
  ```

  E garanta que instalou `opencv-python`, **não** `cv`.

* **“Não foi possível abrir a imagem”**
  Verifique o caminho/arquivo e use aspas no Windows:

  ```bash
  python .\machine-converte-images.py ".\minha imagem.jpg"
  ```

* **Sem janelas/erro de GUI (servidor/WSL/headless):**
  Remova as chamadas `cv.imshow/ waitKey/ destroyAllWindows` e use `--save` para gerar os arquivos.
  Ex.:

  ```bash
  python .\machine-converte-images.py ".\teste.jpeg" --save
  ```

---

## Desempenho

O código usa **loops Python** para fins didáticos. Em imagens grandes, pode ficar lento. Para acelerar **sem** usar funções prontas de conversão, é possível **vetorizar** (usar operações `numpy` para as mesmas fórmulas).

---

## Licença

Livre para uso acadêmico/educacional. Ajuste conforme a necessidade do seu curso/projeto.

---

Se quiser, posso adicionar uma seção de **testes automatizados** (com imagens pequenas) e/ou uma versão **vetorizada com numpy** mantendo a lógica didática.

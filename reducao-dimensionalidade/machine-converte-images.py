#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lê uma imagem de QUALQUER formato suportado pelo OpenCV, converte para uma
matriz RGB, depois:
  1) RGB -> GRAY (tons de cinza) com luminância BT.601 (na raça)
  2) GRAY -> PB (preto e branco) por limiar (Otsu automático ou manual)

Exibe as três versões (original, cinza e PB) em janelas.

Uso:
    python .\machine-converte-images.py .\teste.jpeg --save

- --save: grava 'saida_gray.png' e 'saida_bw.png'
- --manual-threshold N: usa limiar fixo (0..255) em vez de Otsu
"""

import argparse
from typing import List, Tuple
import cv2 as cv
import numpy as np

RGB = Tuple[int, int, int]                 # tupla (R,G,B) 0..255
RGBMatrix = List[List[RGB]]                # matriz [linhas][colunas] de RGB
GrayMatrix = List[List[int]]               # matriz 0..255
BWMatrix = List[List[int]]                 # matriz 0 ou 255

# ---------------------------------------------------------------------
# 1) Ler imagem e transformar em MATRIZ RGB (sem usar conversores prontos)
# ---------------------------------------------------------------------
def read_image_to_rgb_matrix(path: str) -> Tuple[RGBMatrix, int, int]:
    """
    Lê arquivo com OpenCV (BGR) e converte para matriz RGB (lista de listas).
    Não usa cvtColor; fazemos a troca de canais manualmente.
    Retorna (matriz_rgb, altura, largura).
    """
    img_bgr = cv.imread(path, cv.IMREAD_UNCHANGED)
    if img_bgr is None:
        raise ValueError(f"Não foi possível abrir a imagem: {path}")

    # Se tiver alfa (4 canais), descartamos o alfa só para simplificar
    if img_bgr.ndim == 3 and img_bgr.shape[2] == 4:
        img_bgr = img_bgr[:, :, :3]

    # Se for grayscale já (1 canal), expandimos para RGB duplicando
    if img_bgr.ndim == 2:
        img_bgr = np.stack([img_bgr, img_bgr, img_bgr], axis=2)

    h, w, _ = img_bgr.shape

    # Constrói a matriz RGB como lista de listas de tuplas (R,G,B)
    rgb_matrix: RGBMatrix = []
    for y in range(h):
        row: List[RGB] = []
        for x in range(w):
            b, g, r = img_bgr[y, x]          # OpenCV entrega BGR
            row.append((int(r), int(g), int(b)))
        rgb_matrix.append(row)
    return rgb_matrix, h, w

# ---------------------------------------------------------------------
# 2) RGB -> GRAY (na raça)
#    Fórmula de luminância (ITU-R BT.601): Y = 0.299 R + 0.587 G + 0.114 B
# ---------------------------------------------------------------------
def rgb_to_gray(rgb: RGBMatrix, h: int, w: int) -> GrayMatrix:
    gray: GrayMatrix = [[0]*w for _ in range(h)]
    for y in range(h):
        row_rgb = rgb[y]
        row_g = gray[y]
        for x in range(w):
            r, g, b = row_rgb[x]
            yv = int(round(0.299*r + 0.587*g + 0.114*b))
            # clamp por segurança
            if yv < 0: yv = 0
            if yv > 255: yv = 255
            row_g[x] = yv
    return gray

# ---------------------------------------------------------------------
# 3) Limite por Otsu (na raça)
#    Calcula histograma [0..255] e escolhe o threshold que maximiza a
#    variância entre classes.
# ---------------------------------------------------------------------
def otsu_threshold(gray: GrayMatrix, h: int, w: int) -> int:
    hist = [0]*256
    for y in range(h):
        for x in range(w):
            hist[gray[y][x]] += 1

    total = h * w
    sum_total = sum(i * hist[i] for i in range(256))
    sum_b = 0
    w_b = 0
    max_between = -1.0
    t_best = 0

    for t in range(256):
        w_b += hist[t]
        if w_b == 0:
            continue
        w_f = total - w_b
        if w_f == 0:
            break
        sum_b += t * hist[t]
        m_b = sum_b / w_b
        m_f = (sum_total - sum_b) / w_f
        between = w_b * w_f * (m_b - m_f) ** 2
        if between > max_between:
            max_between = between
            t_best = t
    return t_best

# ---------------------------------------------------------------------
# 4) GRAY -> PB (na raça): saída 0 ou 255
# ---------------------------------------------------------------------
def gray_to_bw(gray: GrayMatrix, h: int, w: int, threshold: int) -> BWMatrix:
    bw: BWMatrix = [[0]*w for _ in range(h)]
    for y in range(h):
        row_g = gray[y]
        row_b = bw[y]
        for x in range(w):
            row_b[x] = 0 if row_g[x] > threshold else 255
            # (convencionei: > limiar => branco (0), <= limiar => preto (255))
            # Se preferir ao contrário, troque a ordem acima.
    return bw

# ---------------------------------------------------------------------
# 5) Helpers para exibir/salvar com OpenCV (somente I/O/janela)
# ---------------------------------------------------------------------
def rgb_matrix_to_numpy(rgb: RGBMatrix, h: int, w: int) -> np.ndarray:
    """Converte a matriz RGB (listas) para np.ndarray uint8 (H,W,3) em BGR p/ OpenCV."""
    # Monta array RGB:
    arr = np.zeros((h, w, 3), dtype=np.uint8)
    for y in range(h):
        for x in range(w):
            r, g, b = rgb[y][x]
            arr[y, x, 0] = b
            arr[y, x, 1] = g
            arr[y, x, 2] = r
    return arr  # BGR para OpenCV

def gray_matrix_to_numpy(gray: GrayMatrix, h: int, w: int) -> np.ndarray:
    arr = np.zeros((h, w), dtype=np.uint8)
    for y in range(h):
        for x in range(w):
            arr[y, x] = gray[y][x]
    return arr

def bw_matrix_to_numpy(bw: BWMatrix, h: int, w: int) -> np.ndarray:
    arr = np.zeros((h, w), dtype=np.uint8)
    for y in range(h):
        for x in range(w):
            arr[y, x] = bw[y][x]
    return arr

# ---------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("image", help="caminho da imagem de entrada (jpg, png, bmp, tiff, webp...)")
    ap.add_argument("--save", action="store_true", help="salva saida_gray.png e saida_bw.png")
    ap.add_argument("--manual-threshold", type=int, default=None,
                    help="limiar manual 0..255 (se omitido, usa Otsu)")
    args = ap.parse_args()

    # 1) Lê e vira matriz RGB
    rgb, h, w = read_image_to_rgb_matrix(args.image)
    print(f"Imagem carregada: {w}x{h}")

    # 2) RGB -> cinza (na raça)
    gray = rgb_to_gray(rgb, h, w)

    # 3) Threshold
    if args.manual_threshold is None:
        thr = otsu_threshold(gray, h, w)
        print(f"Limiar por Otsu: {thr}")
    else:
        thr = args.manual_threshold
        if thr < 0 or thr > 255:
            raise ValueError("manual-threshold deve estar entre 0 e 255.")
        print(f"Limiar manual: {thr}")

    # 4) Cinza -> PB (na raça)
    bw = gray_to_bw(gray, h, w, thr)

    # 5) Exibição (somente janela/I-O via OpenCV)
    img_bgr = rgb_matrix_to_numpy(rgb, h, w)
    img_gray = gray_matrix_to_numpy(gray, h, w)
    img_bw = bw_matrix_to_numpy(bw, h, w)

    cv.imshow("Original (RGB)", img_bgr)
    cv.imshow("Tons de Cinza (manual)", img_gray)
    cv.imshow("Preto e Branco (manual)", img_bw)
    print("Pressione qualquer tecla na janela para fechar...")
    cv.waitKey(0)
    cv.destroyAllWindows()

    # 6) Salvar (opcional)
    if args.save:
        cv.imwrite("saida_gray.png", img_gray)
        cv.imwrite("saida_bw.png", img_bw)
        print("Arquivos salvos: saida_gray.png, saida_bw.png")

if __name__ == "__main__":
    main()

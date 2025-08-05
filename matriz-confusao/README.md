Abaixo vai um guia + código **puro Python** para calcular as principais métricas de classificação a partir de uma **matriz de confusão** (VP, VN, FP, FN). Incluí fórmulas, tratamento de bordas (evitar divisão por zero), uma função opcional para **montar a matriz de confusão** a partir de rótulos `y_true` e `y_pred`, e um exemplo com valores **arbitrários** (como o desafio pede).

---

## Métricas (fórmulas)

Considere:

* **VP** (TP) = verdadeiros positivos
* **VN** (TN) = verdadeiros negativos
* **FP** = falsos positivos
* **FN** = falsos negativos
* **N** = VP + VN + FP + FN

Principais métricas:

* **Acurácia**: $\displaystyle \frac{VP + VN}{N}$
* **Sensibilidade / Recall / TPR**: $\displaystyle \frac{VP}{VP + FN}$
* **Especificidade / TNR**: $\displaystyle \frac{VN}{VN + FP}$
* **Precisão / PPV**: $\displaystyle \frac{VP}{VP + FP}$
* **F1-score**: $\displaystyle \frac{2 \cdot \text{Precisão} \cdot \text{Recall}}{\text{Precisão} + \text{Recall}}$

> (Opcional) **F$_\beta$**: $\displaystyle (1+\beta^2)\frac{P \cdot R}{\beta^2 P + R}$

---

## Saída esperada (para o exemplo VP=50, VN=40, FP=5, FN=10)

```
Matriz de confusão (arbitrária):
VP=50  FP=5
FN=10  VN=40
N=105

              acuracia: 0.8571
  sensibilidade_recall: 0.8333
         especificidade: 0.8889
              precisao: 0.9091
              f1_score: 0.8696
```

> Observação: Os valores podem variar conforme a sua matriz arbitrária ou seus dados reais.

---

## Dicas

* **Divisão por zero**: pode ocorrer se não houver positivos previstos/verdadeiros em algum cenário extremo. O código retorna `NaN` nesses casos.
* **F$_\beta$**: use `fbeta(cm, beta=2)` para dar mais peso ao *recall*, ou `beta<1` para dar mais peso à *precisão*.
* **A partir de rótulos**: use `confusion_from_labels(y_true, y_pred, positive=<classe_positiva>)` para montar a CM e depois chame `compute_all`.


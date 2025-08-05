from dataclasses import dataclass
from typing import Iterable, Any, Dict, Optional
import math

@dataclass
class ConfusionMatrix:
    vp: int  # verdadeiros positivos (TP)
    vn: int  # verdadeiros negativos (TN)
    fp: int  # falsos positivos (FP)
    fn: int  # falsos negativos (FN)

    @property
    def n(self) -> int:
        return self.vp + self.vn + self.fp + self.fn

def _safe_div(num: float, den: float) -> float:
    """Divisão segura: retorna NaN se den==0."""
    return num / den if den != 0 else float('nan')

def accuracy(cm: ConfusionMatrix) -> float:
    return _safe_div(cm.vp + cm.vn, cm.n)

def recall(cm: ConfusionMatrix) -> float:
    # sensibilidade / TPR
    return _safe_div(cm.vp, cm.vp + cm.fn)

def specificity(cm: ConfusionMatrix) -> float:
    # TNR
    return _safe_div(cm.vn, cm.vn + cm.fp)

def precision(cm: ConfusionMatrix) -> float:
    # PPV
    return _safe_div(cm.vp, cm.vp + cm.fp)

def fbeta(cm: ConfusionMatrix, beta: float = 1.0) -> float:
    p = precision(cm)
    r = recall(cm)
    if math.isnan(p) or math.isnan(r) or (p == 0 and r == 0):
        return float('nan')
    b2 = beta * beta
    return (1 + b2) * _safe_div(p * r, (b2 * p + r))

def f1(cm: ConfusionMatrix) -> float:
    return fbeta(cm, beta=1.0)

def compute_all(cm: ConfusionMatrix) -> Dict[str, float]:
    return {
        "acuracia": accuracy(cm),
        "sensibilidade_recall": recall(cm),
        "especificidade": specificity(cm),
        "precisao": precision(cm),
        "f1_score": f1(cm),
    }

# ----- (Opcional) construir CM a partir de rótulos -----
def confusion_from_labels(y_true: Iterable[Any], y_pred: Iterable[Any], positive: Any) -> ConfusionMatrix:
    """
    Constrói VP, VN, FP, FN a partir de y_true e y_pred.
    'positive' indica a classe considerada positiva.
    """
    vp = vn = fp = fn = 0
    for t, p in zip(y_true, y_pred):
        if p == positive and t == positive:
            vp += 1
        elif p == positive and t != positive:
            fp += 1
        elif p != positive and t == positive:
            fn += 1
        else:
            vn += 1
    return ConfusionMatrix(vp, vn, fp, fn)

# ----- Exemplo de uso com CM arbitrária -----
if __name__ == "__main__":
    # Escolha arbitrária (como proposto no desafio):
    # Suponha VP=50, VN=40, FP=5, FN=10
    cm = ConfusionMatrix(vp=50, vn=40, fp=5, fn=10)

    print("Matriz de confusão (arbitrária):")
    print(f"VP={cm.vp}  FP={cm.fp}")
    print(f"FN={cm.fn}  VN={cm.vn}")
    print(f"N={cm.n}\n")

    metrics = compute_all(cm)

    # Impressão formatada
    for k, v in metrics.items():
        print(f"{k:>22}: {v:.4f}")

    # Exemplo opcional a partir de rótulos:
    # y_true = [1,1,0,1,0,0,1,0,1,0]
    # y_pred = [1,0,0,1,0,0,1,1,1,0]
    # cm2 = confusion_from_labels(y_true, y_pred, positive=1)
    # print("\nCM de rótulos:", cm2)
    # print(compute_all(cm2))

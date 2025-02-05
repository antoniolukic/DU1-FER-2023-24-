import torch
import torch.nn.functional as F


# definiranje operacije
def f(x, a, b):
    return a * x + b

# definiranje varijabli i izgradnja dinamičnog
# računskog grafa s unaprijednim prolazom
a = torch.tensor(5., requires_grad=True)
b = torch.tensor(8., requires_grad=True)
x = torch.tensor(2.)
y = f(x, a, b)
s = a ** 2

# unatražni prolaz koji računa gradijent
# po svim tenzorima zadanim s requires_grad=True
y.backward()
s.backward()               # gradijent se akumulira
assert x.grad is None      # pytorch ne računa gradijente po x
assert a.grad == x + 2 * a # dy/da + ds/da
assert b.grad == 1         # dy/db + ds/db

# ispis rezultata
print(f"y={y}, g_a={a.grad}, g_b={b.grad}")


def multiclass_confusion_matrix(y_true, y_pred, class_count):
    with torch.no_grad():
        y_pred = F.one_hot(y_pred, class_count)
        cm = torch.zeros([class_count] * 2, dtype=torch.int64, device=y_true.device)
        for c in range(class_count):
            cm[c, :] = y_pred[y_true == c, :].sum(0)
    return cm

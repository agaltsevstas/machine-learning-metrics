# Метрики для обнаружения объектов
class Metrics:
    def __init__(self):
        self.tp = 0  # true positive - правильное обнаружение
        self.fp = 0  # false positive - неправильное обнаружение
        self.fn = 0  # false negative - неправильное обнаружение
        self.tn = 0  # true negative - не применяется

    def number(self):
        return self.tp + self.fn

    # Правильность
    def accuracy(self):
        sum = self.tp + self.fp + self.tn + self.fn
        if sum == 0:
            return 0
        return (self.tp + self.tn) / sum

    # Точность
    def precision(self):
        sum = self.tp + self.fp
        if sum == 0:
            return 0
        return self.tp / sum

    # Полнота
    def recall(self):
        sum = self.tp + self.fn
        if sum == 0:
            return 0
        return self.tp / sum

    # Гармоническое среднее между точностью и полнотой
    def f1_score(self):
        return 2 / ((1 / self.precision()) + (1 / self.recall()))

    # Вывод значений
    def values(self):
        num = 1
        if self.number() > 0:
            num = self.number()
        return 1.0*self.fn/num, 1.0*self.fp/num, self.accuracy(), self.precision(), self.recall(), self.f1_score()

    # Название метрик
    @staticmethod
    def str_header():
        return ["fn", "fp", "acc", "prec", "rec", "f1"]

def union(a,b):
    x = min(a[0], b[0])
    y = min(a[1], b[1])
    w = max(a[0]+a[2], b[0]+b[2]) - x
    h = max(a[1]+a[3], b[1]+b[3]) - y
    return (x, y, w, h)

def intersection(a,b):
    x = max(a[0], b[0])
    y = max(a[1], b[1])
    w = min(a[0]+a[2], b[0]+b[2]) - x
    h = min(a[1]+a[3], b[1]+b[3]) - y
    if w < 0 or h < 0: return (0, 0, 0, 0)
    return (x, y, w, h)

def intersection_over_union(o1, o2, T=0.7):
    if o1[4] != o2[4]:
        return False
    I = intersection(o1, o2)
    U = union(o1, o2)
    Ai = I[2] * I[3]
    Au = U[2] * U[3]
    if Au * Ai == 0:
        return False
    if 1.0 * Ai / Au < T:
        return False
    return True

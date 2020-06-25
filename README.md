# Аннотация
GUI приложение показывающее метрики для обнаружения объектов на основе xml файлов.

## Поддерживаемые платформы
* Linux 

## Требования:
* python3, библиотеки:
  * sys
  * os
  * numpy
  * numpy
  * tkinter
  * matplotlib
  * xml

# Описание
Приложение предоставляет простые в использовании функции, реализующие те же метрики, которые используются в самых популярных источниках по обнаружению объектов . Реализация была тщательно сравнена с официальной реализацией, и полученные результаты совпадают с официальными результатами.

## Определения 

### Метрика степени пересечения между двумя ограничивающими рамками (IOU)

Для того, чтобы определить пересечения между двумя регионами изображения будет использоваться метрика Intersection over Union (IOU). Она считается довольно просто: площадь пересечения двух областей (area of overlap) делится на общую площадь объединения регионов (area of union). Изображение ниже иллюстрирует IOU, где исходный объект отмечен зеленым прямоугольником и обнаруженный объект красным прямоугольником.

<p align="center">
<img src="images/iou.png"/>
</p>

### Оценка качества в задачах классификации
* TP — истино-положительное решение. Обнаружение при условии IOU ≥ _порог_  
* TN — истино-отрицательное решение. Обнаружение при условии IOU < _порог_ 
* FP — ложно-положительное решение
* FN — ложно-отрицательное решение

_порог_: в зависимости от метрики, он обычно устанавливается на 50%, 75% или 95%.

### Accuracy (правильность)

Правильность - доля правильных ответов алгоритма.

<p align="center">
<img src="images/precision.jpg" align="center"/>
</p>

### Precision (точность)
Точность системы в пределах класса – это процентов объектов действительно принадлежащих данному классу относительно всех документов которые система отнесла к этому классу. 
<p align="center">
<img src="images/precision.jpg"/>
</p>

### Recall (полнота)
Полнота системы – это процент найденных классификатором объектов принадлежащих классу относительно всех объектов этого класса в тестовой выборке.

<p align="center">
<img src="images/recall.jpg"/>
</p>

### F1-socre
Гармоническое среднее между точностью и полнотой.

<p align="center">
<img src="images/f1-score.jpg"/>
</p>

# Загрузка
```
git clone https://gitlab.com/agaltsev.stas/machine-learning-metrics-from-xml.git
cd machine-learning-metrics-from-xml
```

# Запуск
```
python3 gui.py
```

<p align="center">
<img src="images/1.png"/>
</p>

Пользователю предлагается загрузить 2 xml файла: исходный файл source local (load xml labled), а также размеченный нейросетью (load xml nerounet). Результаты работы представлены ниже на рисунках для классов: car, sign, truck, person, trafficlight, bus.
<p align="center">
<img src="images/2.png"/>
</p>
<p align="center">
<img src="images/3.png"/>
</p>

## Ссылки

* Метрики в задачах машинного обучения 
https://habr.com/ru/company/ods/blog/328372/

* Object Detection. Распознавай и властвуй. Часть 1 
https://habr.com/ru/company/jetinfosystems/blog/498294/

* Decoding the Confusion Matrix 
https://keytodatascience.com/confusion-matrix/

* Object Detection Metrics
https://github.com/rafaelpadilla/Object-Detection-Metrics#recall


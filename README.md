# Модуль Python для проверки точности определения размеров дефектов газопровода
[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/63b6127420a04315913e8aee4fbf9914)](https://www.codacy.com/gh/vb64/oeg.feature.class/dashboard?utm_source=github.com&utm_medium=referral&utm_content=vb64/oeg.feature.class&utm_campaign=Badge_Coverage)
[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/vb64/oeg.feature.class/oeg.feature.class%20tests?label=Python%202.7%203.6%203.7%203.8&style=plastic)](https://github.com/vb64/oeg.feature.class/actions?query=workflow%3A%22oeg.feature.class+tests%22)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/63b6127420a04315913e8aee4fbf9914)](https://www.codacy.com/gh/vb64/oeg.feature.class/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=vb64/oeg.feature.class&amp;utm_campaign=Badge_Grade)

Этот модуль Python реализует определение "класса размера дефекта" трубопровода согласно [Specifications and requirements for intelligent pig inspection of pipelines](http://www.iliassociation.org/documents/industry/POF%20specs%20V3_2%20January%202005.pdf) 

![Anomaly dimension classification](img/class_table.PNG)

![Graphical presentation of metal loss anomalies per dimension class](img/class_chart.PNG)

А также проверку точности определения размеров дефектов и порога обнаружения при продольном и поперечном намагничивании согласно "Р Газпром2-2.3-919-2015 ОСНОВНОЕ И ВСПОМОГАТЕЛЬНОЕ ОБОРУДОВАНИЕ ДЛЯ ВНУТРИТРУБНОГО ДИАГНОСТИРОВАНИЯ Технические требования".

![Таблица Е.1 – Пороги  обнаружения и точностьопределения геометрических параметров дефектов потери металла стенки трубы припродольном намагничивании](img/mfl.PNG)

![Таблица Е.2 – Пороги обнаружения и точностьопределения геометрических параметров дефектов потери металластенки трубыпри поперечном намагничивании](img/tfi.PNG)

## Установка

```
$ pip install oeg_feature_class
```

## Использование

```python
# функция size_class определяет "класс размера" дефекта при заданных длине, ширине дефекта и толщине стенки трубы.
from oeg_feature_class import size_class, FeatureClass

# дефект размером 100x100 мм на стенке трубы толщиной 10 мм является дефектом класса "обширный"
assert size_class(100, 100, 10) == FeatureClass.GENE

# дефекты с нулевыми размерами не допускаются
size_class(0, 100, 10)
oeg_feature_class.Error: Wrong FeatureClass params. l=0 w=100 t=10

# функция is_detectable определяет, должен ли выявляться дефект заданных размеров на заданной толщине стенки трубы
# при указанном типе намагничивания
from oeg_feature_class import is_detectable, MagnetType

# дефект размером 10x10 мм глубиной 5 мм на стенке трубы толщиной 11 мм должен определяться снарядами с продольным намагничиванием
assert is_detectable((10, 10, 5), 11, magnet_type=MagnetType.MFL)

# функция is_in_limits проверяет, укладываются ли в допустимую погрешность вычисленные размеры дефекта по сравнению с его реальными размерами
# при заданных толщине стенки трубы и типе намагничивания
from oeg_feature_class import is_in_limits

# реальные размеры дефекта: длина 90 мм, ширина 12 мм, глубина 4 мм
real = (90, 12, 4)
# вычисленные размеры дефекта: длина 72 мм, ширина 11 мм, глубина 1 мм
calcked = (72, 11, 1)

# проверяем, соответствуют ли вычисленные размеры дефекта допускам, если толщина стенки трубы равна 16.6 мм и тип намагничивания поперечный
length_ok, width_ok, depth_ok = is_in_limits(calcked, real, 16.6, magnet_type=MagnetType.TFI)

# вычисленная длина укладывается в допустимую погрешность
assert length_ok
# вычисленная ширина укладывается в допустимую погрешность
assert width_ok
# вычисленная глубина НЕ укладывается в допустимую погрешность
assert not depth_ok
```

## Разработка

```
$ git clone git@github.com:vb64/oeg.feature.class.git
$ cd oeg.feature.class
```
При использовании Python
```
$ make setup2 PYTHON_BIN=/path/to/python27/executable
```
При использовании Python 3
```
$ make setup PYTHON_BIN=/path/to/python37/executable
```
Затем
```
$ make tests
```

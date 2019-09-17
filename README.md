# oeg_feature_class

Этот модуль Python реализует определение "класса размера дефекта" трубопровода согласно [Specifications and requirements for intelligent pig inspection  of pipelines](http://www.iliassociation.org/documents/industry/POF%20specs%20V3_2%20January%202005.pdf) 

![Anomaly dimension classification](img/class_table.PNG)

![Graphical presentation of metal loss anomalies per dimension class](img/class_chart.PNG)

А также проверку точности определения размеров дефектов и порога обнаружения при продольном и поперечном намагничивании согласно "Р Газпром2-2.3-919-2015 ОСНОВНОЕ И ВСПОМОГАТЕЛЬНОЕ ОБОРУДОВАНИЕ ДЛЯ ВНУТРИТРУБНОГО ДИАГНОСТИРОВАНИЯ Технические требования".

![Таблица Е.1 – Пороги  обнаружения и точностьопределения геометрических параметров дефектов потери металла стенки трубы припродольном намагничивании](img/mfl.PNG)

![Таблица Е.2 – Пороги обнаружения и точностьопределения геометрических параметров дефектов потери металластенки трубыпри поперечном намагничивании](img/tfi.PNG)

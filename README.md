# sql-tree-perfomance
Benchmark tree structure for Django

### Задача

Сравинить производительность храниния древовидной структуры данных в PostgreSQL приминительно к Django приложению.

### Тестируемы инструментарий

Для работы с рекурсивными структурами в Django будут использованы следующие инстументы

1. Штатная рекурсия Django на основе ForeignKey
2. Модуль django-mptt
3. Модуль для реализации Ltree

### Методика тестирования

Тестирование будет проводится на наборе данных из 150 тыс компаний. Время будет замеряться для следующих запросов:

1. Чтение всего дерева
2. Чтение произвольного узла
3. Перемещение узла с нижнего на верхний уровень
4. Перемещение узла внутри уровня
5. Вставка узла на второй уровень

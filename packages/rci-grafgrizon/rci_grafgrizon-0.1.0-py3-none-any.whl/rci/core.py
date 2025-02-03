import importlib.resources

class RCI:
    def __init__(self):
        self.text = self._load_data()
    
    def _load_data(self):
        with importlib.resources.open_text("rci.data", "all_DL.txt") as file:
            return file.read()
    
    def get_imports(self):
        """
        print(get_imports()) - получить общий импорт для всех заданий
        """
        return self.text.split("###")[0]
    
    def get_cell(self, topic, task, cell):
        """
        topic:
        1 - regression
        2 - classification
        3 - images
        
        task:
        1.
        1 - 2. Набор данных: regression/gold.csv. Оптимизаторы
        2 - 2. Набор данных: regression/gold.csv. Гиперпараметры
        3 - 2. Набор данных: regression/bike_cnt.csv. BatchNorm1d
        4 - 2. Набор данных: regression/bike_cnt.csv. Dropout
        
        2.
        1 - 2. Набор данных: classification/bank.csv. Оптимизаторы
        2 - 2. Набор данных: classification/bank.csv. Dropout
        3 - 2. Набор данных: classification/bank.csv. Несбалансированность
        
        3.
        1 - 3. Набор данных: images/sign_language.zip. Скрытые представления
        2 - 3. Набор данных: images/sign_language.zip. PCA
        3 - 3. Набор данных: images/sign_language.zip. Число сверточных блоков
        4 - 3. Набор данных: images/eng_handwritten.zip. val, ранняя остановка
        5 - 3. Набор данных: images/eng_handwritten.zip. 3 модификации изображения
        6 - 3. Набор данных: images/chars.zip. Обычный и расширенный датасеты
        7 - 3. Набор данных: images/chars.zip. Неопределенные классы
        8 - 3. Набор данных: images/clothes_multi.zip. Задача множественной классификации
        
        cell:
        Номер нужной ячейки
        
        Вывод: print(get_cell(topic, task, cell))
        """
        if len(self.text.split('###')[topic].split('##')[task].split('---')) <= cell:
            return 'end'
        else:
            return self.text.split('###')[topic].split('##')[task].split('---')[cell]

# Импортируем необходимые константы и классы из PyQt5
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QWidget,  # Импорт базовых виджетов
                            QPushButton, QLabel, QListWidget,  # Импорт элементов интерфейса
                            QLineEdit, QTextEdit, QInputDialog,  # Импорт полей ввода и диалогов
                            QHBoxLayout, QVBoxLayout)  # Импорт компоновщиков

app = QApplication([]) # Создаем экземпляр приложения
notes = [] # Инициализируем список для хранения заметок

'''Интерфейс приложения'''

notes_win = QWidget() # Создаем главное окно приложения
notes_win.setWindowTitle('Умные заметки') # Устанавливаем заголовок окна
notes_win.resize(900, 600) # Задаем размеры окна (ширина: 900, высота: 600)

list_notes = QListWidget() # Создаем виджет списка для отображения заметок
list_notes_label = QLabel('Список заметок') # Создаем метку для списка заметок
button_note_create = QPushButton('Создать заметку') # Создаем кнопку для создания новой заметки
button_note_del = QPushButton('Удалить заметку') # Создаем кнопку для удаления заметки
button_note_save = QPushButton('Сохранить заметку') # Создаем кнопку для сохранения заметки

field_tag = QLineEdit('') # Создаем поле ввода для тегов
field_tag.setPlaceholderText('Введите тег...') # Устанавливаем placeholder текст для поля тега
field_text = QTextEdit() # Создаем поле для ввода текста заметки
button_tag_add = QPushButton('Добавить к заметке') # Создаем кнопку для добавления тега к заметке
button_tag_del = QPushButton('Открепить от заметки') # Создаем кнопку для удаления тега из заметки
button_tag_search = QPushButton('Искать заметки по тегу') # Создаем кнопку для поиска заметок по тегу
list_tags = QListWidget() # Создаем виджет списка для отображения тегов
list_tags_label = QLabel('Список тегов') # Создаем метку для списка тегов
layout_notes = QHBoxLayout() # Создаем горизонтальный компоновщик для основного layout
col_1 = QVBoxLayout() # Создаем первую колонку (вертикальный компоновщик)
col_1.addWidget(field_text) # Добавляем поле текста в первую колонку

col_2 = QVBoxLayout() # Создаем вторую колонку
col_2.addWidget(list_notes_label) # Добавляем метку во вторую колонку
col_2.addWidget(list_notes) # Добавляем список заметок во вторую колонку
# Создаем первый ряд кнопок
row_1 = QHBoxLayout()
row_1.addWidget(button_note_create)
row_1.addWidget(button_note_del)

# Создаем второй ряд кнопок
row_2 = QHBoxLayout()
row_2.addWidget(button_note_save)
# Добавляем ряды кнопок во вторую колонку
col_2.addLayout(row_1)
col_2.addLayout(row_2)
# Добавляем элементы для работы с тегами во вторую колонку
col_2.addWidget(list_tags_label)
col_2.addWidget(list_tags)
col_2.addWidget(field_tag)
# Создаем третий ряд кнопок для работы с тегами
row_3 = QHBoxLayout()
row_3.addWidget(button_tag_add)
row_3.addWidget(button_tag_del)
# Создаем четвертый ряд для кнопки поиска
row_4 = QHBoxLayout()
row_4.addWidget(button_tag_search)
# Добавляем ряды кнопок для тегов во вторую колонку
col_2.addLayout(row_3)
col_2.addLayout(row_4)
# Добавляем колонки в основной layout с указанием пропорций
layout_notes.addLayout(col_1, stretch = 2)  # Первая колонка занимает 2/3 ширины
layout_notes.addLayout(col_2, stretch = 1)  # Вторая колонка занимает 1/3 ширины
# Устанавливаем layout для главного окна
notes_win.setLayout(layout_notes)

'''Функционал приложения'''
# Функция для отображения выбранной заметки
def show_note():
    # Получаем текст выбранного элемента (заголовок заметки)
    key = list_notes.selectedItems()[0].text()
    print(key)
    # Ищем заметку в списке и отображаем её содержимое
    for note in notes:
        if note[0] == key:
            field_text.setText(note[1])  # Устанавливаем текст заметки
            list_tags.clear()  # Очищаем список тегов
            list_tags.addItems(note[2])  # Добавляем теги заметки

# Функция для добавления новой заметки
def add_note():
    # Открываем диалог для ввода названия заметки
    note_name, ok = QInputDialog.getText(notes_win, "Добавить заметку", "Название заметки: ")
    if ok and note_name != "":
        # Создаем новую заметку [название, текст, теги]
        note = [note_name, '', []]
        notes.append(note)  # Добавляем заметку в список
        list_notes.addItem(note[0])  # Добавляем название в список заметок
        list_tags.addItems(note[2])  # Добавляем теги (пока пустые)
        print(notes)
        # Сохраняем заметку в файл
        with open(str(len(notes)-1)+".txt", "w", encoding='utf-8') as file:
            file.write(note[0]+'\n')

# Функция для сохранения заметки
def save_note():
    if list_notes.selectedItems():        
        key = list_notes.selectedItems()[0].text() # Получаем название выбранной заметки
        index = 0
        # Ищем заметку в списке
        for note in notes:
            if note[0] == key:                
                note[1] = field_text.toPlainText() # Обновляем текст заметки
                # Сохраняем в файл
                with open(str(index)+".txt", "w", encoding='utf-8') as file:
                    file.write(note[0]+'\n')  # Записываем название
                    file.write(note[1]+'\n')  # Записываем текст
                    # Записываем теги через пробел
                    for tag in note[2]:
                        file.write(tag + ' ')
                    file.write('\n')
            index += 1
        print(notes)
    else:
        print("Заметка для сохранения не выбрана!")

# Функция для поиска заметок по тегу
def search_tag():    
    tag = field_tag.text() # Получаем текст из поля тега    
    if button_tag_search.text() == "Искать заметки по тегу..." and tag: # Если кнопка в режиме поиска и тег указан
        notes_filtered = {}  # Словарь для отфильтрованных заметок
        # Ищем заметки с указанным тегом
        for note in notes:
            if tag in notes[note]['теги']:
                notes_filtered[note] = notes[note]        
        button_tag_search.setText("Сбросить поиск") # Меняем текст кнопки на "Сбросить поиск"        
        list_notes.clear() # Очищаем список заметок
        list_tags.clear()  # Очищаем список тегов      
        list_notes.addItems(notes_filtered) # Показываем только отфильтрованные заметки    
    elif button_tag_search.text() == "Сбросить поиск": # Если кнопка в режиме сброса        
        field_tag.clear()  # Очищаем поле тега
        list_notes.clear() # Очищаем список заметок
        list_tags.clear()  # Очищаем список тегов     
        list_notes.addItems(notes) # Показываем все заметки        
        button_tag_search.setText("Искать заметки по тегу") # Возвращаем текст кнопки

# Привязка обработчиков событий к виджетам
list_notes.itemClicked.connect(show_note)  # Клик по заметке
button_note_create.clicked.connect(add_note)  # Клик по кнопке создания
button_note_save.clicked.connect(save_note)  # Клик по кнопке сохранения
button_tag_search.clicked.connect(search_tag)  # Клик по кнопке поиска

# Загрузка заметок из файлов при запуске
name = 0  # Счетчик для имен файлов
note = []  # Временный список для хранения данных заметки
# Читаем файлы, пока они существуют
while True:
    filename = str(name)+".txt"
    try:
        # Открываем файл для чтения
        with open(filename, "r", encoding='utf-8') as file:
            # Читаем строки файла
            for line in file:
                line = line.replace('\n', '')  # Убираем символ переноса строки
                note.append(line)  # Добавляем строку в временный список
        # Разбиваем строку с тегами на список
        tags = note[2].split()
        note[2] = tags

        # Добавляем заметку в общий список
        notes.append(note)
        note = []  # Очищаем временный список
        name += 1  # Увеличиваем счетчик

    except IOError:  # Если файл не найден, прерываем цикл
        break

# Выводим список заметок в консоль
print(notes)

# Добавляем названия заметок в список
for note in notes:
    list_notes.addItem(note[0])

notes_win.show()# Показываем главное окно
app.exec_()# Запускаем главный цикл приложения

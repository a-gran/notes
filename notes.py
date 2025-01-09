# Импортируем необходимые константы и классы из PyQt5
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QWidget,  # Импорт базовых виджетов
                            QPushButton, QLabel, QListWidget,  # Импорт элементов интерфейса
                            QLineEdit, QTextEdit, QInputDialog,  # Импорт полей ввода и диалогов
                            QHBoxLayout, QVBoxLayout)  # Импорт компоновщиков

import os

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

# Функция для удаления заметки из списка и файловой системы
def del_note():
    # Проверяем, выбрана ли какая-либо заметка в списке
    if list_notes.selectedItems():
        # Получаем текст (название) выбранной заметки
        key = list_notes.selectedItems()[0].text()
        # Инициализируем индекс для отслеживания позиции заметки в списке
        index = 0
        
        # Перебираем все заметки в поиске нужной
        for note in notes:
            # Если нашли заметку с нужным названием
            if note[0] == key:
                # Пытаемся удалить файл заметки и перенумеровать оставшиеся
                try:
                    # Удаляем файл текущей заметки
                    os.remove(str(index) + ".txt")
                    
                    # Перенумеровываем все последующие файлы
                    for i in range(index + 1, len(notes)):
                        if os.path.exists(str(i) + ".txt"):
                            os.rename(str(i) + ".txt", str(i - 1) + ".txt")
                            
                except Exception as e:
                    print("Ошибка при работе с файлами:", e)
                
                # Удаляем заметку из списка заметок по индексу
                notes.pop(index)
                # Очищаем поле текста заметки
                field_text.clear()
                # Очищаем список тегов
                list_tags.clear()
                # Очищаем список заметок в интерфейсе
                list_notes.clear()
                # Обновляем список заметок, добавляя только названия
                list_notes.addItems([note[0] for note in notes])
                
                # Пересохраняем все заметки с новыми индексами
                for i, note in enumerate(notes):
                    with open(str(i) + ".txt", "w", encoding='utf-8') as file:
                        file.write(note[0] + '\n')  # Записываем название
                        file.write(note[1] + '\n')  # Записываем текст
                        # Записываем теги через пробел
                        for tag in note[2]:
                            file.write(tag + ' ')
                        file.write('\n')
                
                # Прерываем цикл, так как заметка уже найдена и удалена
                break
            # Увеличиваем индекс для следующей итерации
            index += 1
    else:
        # Если заметка не выбрана, выводим сообщение об ошибке
        print("Заметка для удаления не выбрана!")

# Функция для добавления нового тега к заметке
def add_tag():
    # Проверяем, выбрана ли какая-либо заметка
    if list_notes.selectedItems():
        # Получаем название выбранной заметки
        key = list_notes.selectedItems()[0].text()
        # Получаем текст тега из поля ввода
        tag = field_tag.text()
        
        # Проверяем, что тег не пустой
        if tag:
            # Ищем нужную заметку в списке
            for note in notes:
                if note[0] == key:
                    # Проверяем, что такого тега еще нет у заметки
                    if tag not in note[2]:
                        # Добавляем новый тег в список тегов заметки
                        note[2].append(tag)
                        # Добавляем тег в интерфейс списка тегов
                        list_tags.addItem(tag)
                        # Очищаем поле ввода тега
                        field_tag.clear()
                        # Сохраняем изменения в файл
                        save_note()
    else:
        # Если заметка не выбрана, выводим сообщение об ошибке
        print("Заметка для добавления тега не выбрана!")

# Функция для удаления тега из заметки
def del_tag():
    # Проверяем, выбраны ли заметка и тег
    if list_notes.selectedItems() and list_tags.selectedItems():
        # Получаем название выбранной заметки
        key = list_notes.selectedItems()[0].text()
        # Получаем текст выбранного тега
        tag = list_tags.selectedItems()[0].text()
        
        # Ищем нужную заметку в списке
        for note in notes:
            if note[0] == key:
                # Удаляем тег из списка тегов заметки
                note[2].remove(tag)
                # Очищаем список тегов в интерфейсе
                list_tags.clear()
                # Обновляем список тегов в интерфейсе
                list_tags.addItems(note[2])
                # Сохраняем изменения в файл
                save_note()
    else:
        # Если тег или заметка не выбраны, выводим сообщение об ошибке
        print("Тег для удаления не выбран!")

# Функция для поиска заметок по тегу
def search_tag():
    # Получаем текст тега из поля ввода
    tag = field_tag.text()
    
    # Если кнопка в режиме поиска и тег указан
    if button_tag_search.text() == "Искать заметки по тегу" and tag:
        # Создаем список для хранения найденных заметок
        matching_notes = []
        # Перебираем все заметки
        for note in notes:
            # Если искомый тег есть в списке тегов заметки
            if tag in note[2]:
                # Добавляем название заметки в список найденных
                matching_notes.append(note[0])
        
        # Меняем текст кнопки на "Сбросить поиск"
        button_tag_search.setText("Сбросить поиск")
        # Очищаем список заметок в интерфейсе
        list_notes.clear()
        # Очищаем список тегов в интерфейсе
        list_tags.clear()
        # Очищаем поле текста заметки
        field_text.clear()
        # Показываем только найденные заметки
        list_notes.addItems(matching_notes)
    
    # Если кнопка в режиме сброса поиска
    elif button_tag_search.text() == "Сбросить поиск":
        # Очищаем поле ввода тега
        field_tag.clear()
        # Очищаем список заметок в интерфейсе
        list_notes.clear()
        # Очищаем список тегов в интерфейсе
        list_tags.clear()
        # Очищаем поле текста заметки
        field_text.clear()
        # Показываем все заметки
        # Создаем временный список для хранения названий заметок
        note_names = []
        # Проходим по всем заметкам и добавляем их названия в список
        for note in notes:
            note_names.append(note[0])
        # Добавляем все названия в интерфейс списка заметок
        list_notes.addItems(note_names)
        # Возвращаем исходный текст кнопки
        button_tag_search.setText("Искать заметки по тегу")

# Привязка обработчиков событий к виджетам
list_notes.itemClicked.connect(show_note)  # Клик по заметке
button_note_create.clicked.connect(add_note)  # Клик по кнопке создания
button_note_save.clicked.connect(save_note)  # Клик по кнопке сохранения
button_note_del.clicked.connect(del_note)  # Клик по кнопке удаления заметки

button_tag_search.clicked.connect(search_tag)  # Клик по кнопке поиска
button_tag_add.clicked.connect(add_tag)  # Клик по кнопке добавления тега
button_tag_del.clicked.connect(del_tag)  # Клик по кнопке удаления тега

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

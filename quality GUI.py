#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Adds the second PMXML to the first one, saves to output

@author: Maxim Mukhortov and Stas Agaltsev
"""

import os
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
import pm_utils as pm
from sklearn.metrics import precision_recall_fscore_support, accuracy_score

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

# Вычисление метрик
def metrics_calculation(xml_paths):
    metrics = {}
    # Считывание xml файлов
    files_objects = [pm.readXml(xml_path, "basename") for xml_path in xml_paths]
    # Параллельный цикл для 2 xml файлов
    for labeled_file, neuronet_file in zip(files_objects[0], files_objects[1]):
        # Проверка на совпадение изображений
        if neuronet_file != labeled_file:
            continue
        # Получение объекта и его координат
        labeled_objects = files_objects[0][labeled_file]
        neuronet_objects = files_objects[1][neuronet_file]
        # Если объекты не найдены в одном из xml файлов
        if any(len(v) == 0 for v in (labeled_objects, neuronet_objects)):
            continue
        labeled_pairs = np.zeros(len(labeled_objects), np.int32)
        neuronet_pairs = np.zeros(len(neuronet_objects), np.int32)
        # Проверка на совпадение объектов в xml файлах
        for i in range(len(labeled_objects)):
            labeled_class = labeled_objects[i][4]
            if labeled_class not in metrics:
                metrics[labeled_class] = Metrics()
            for j in range(len(neuronet_objects)):
                neuronet_class = neuronet_objects[j][4]
                # True positive
                if labeled_class == neuronet_class and pm.intersection_over_union(labeled_objects[i],
                                                                                  neuronet_objects[j],
                                                                                  0.5):
                    labeled_pairs[i] = 1
                    neuronet_pairs[j] = 1
                    metrics[labeled_class].tp += 1
        # False positive
        for j in range(len(neuronet_objects)):
            if neuronet_pairs[j] == 0:
                neuronet_class = neuronet_objects[j][4]
                if neuronet_class not in metrics:
                    metrics[neuronet_class] = Metrics()
                metrics[neuronet_class].fp += 1
        # False negative
        for j in range(len(labeled_objects)):
            if labeled_pairs[j] == 0:
                labeled_class = labeled_objects[j][4]
                metrics[labeled_class].fn += 1
    return Metrics.str_header(), metrics

# GUI приложение
class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.filepath_first = None
        self.filepath_second = None
        self.file_first = "1"
        self.file_second = "2"
        self.label_first = tk.Label(text="missing file", fg="red")
        self.label_first.grid(row=0, column=1, sticky="nsew")
        self.label_second = tk.Label(text="missing file", fg="red")
        self.label_second.grid(row=1, column=1, sticky="nsew")
        self.list_box = tk.Listbox(selectmode=tk.EXTENDED, height=2)
        self.list_box.grid(row=2, columnspan=3, sticky="nsew")
        self.button_file_first = tk.Button(text="Load XML labeled",   activeforeground="blue", bg="#4e9a06",
                                           command=lambda: self.open_xml(self.file_first))
        self.button_file_first.grid(row=0, column=0, sticky="nsew")
        self.button_file_second = tk.Button(text="Load XML neuronet data",  activeforeground="blue", bg="#ffff00",
                                            command=lambda: self.open_xml(self.file_second))
        self.button_file_second.grid(row=1, column=0, sticky="nsew")
        self.button_histogram = tk.Button(text="histogram",  activeforeground="blue", bg="#ffb841",
                                          command=lambda: self.histogram())
        self.button_histogram.grid(row=3, column=0, sticky="nsew")
        self.button_delete = tk.Button(text="Delete", activeforeground="blue", bg="#ff496c",
                                       command=lambda: self.delete_file())
        self.button_delete.grid(row=3, column=1, sticky="nsew")
        self.button_exit = tk.Button(text="Exit", activeforeground="blue", bg="#42aaff",
                                     command=lambda: self.question_exit())
        self.button_exit.grid(row=3, column=2, sticky="nsew")
        self.update_clock()

    # Загрузка xml файла
    def open_xml(self, file_selection):
        filepath = tk.filedialog.askopenfilename(initialdir=dir, title="Select XML First",
                                                 filetypes=[("XML files", "*.xml")])
        # Проверка пути к xml файла на пустоту и на совпадение ранее загруженного xml файла с таким же именем
        if len(filepath) and not filepath == self.filepath_first and not filepath == self.filepath_second:
            """
            Если загружается xml labeled файл, то он добавляется в начало списка и удаляется ранее добавленный
            файл.
            Если загружается xml neuronet файл, то он добавляется в конец списка и удаляется ранее добавленный
            файл.
            """
            if file_selection == self.file_first:
                if self.filepath_first:
                    self.list_box.delete(0)
                self.list_box.insert(0, filepath)
                self.filepath_first = filepath
            elif file_selection == self.file_second:
                if self.filepath_second:
                    self.list_box.delete(tk.END)
                self.list_box.insert(tk.END, filepath)
                self.filepath_second = filepath
            print(filepath + " LOADED")

    # Выход из программы
    def question_exit(self):
        ask = messagebox.askquestion("Exit", "Are you sure to quit?")
        if ask == "yes":
            self.tk.quit()

    # Открытие гистограммы
    def histogram(self):
        xml_files = self.list_box.get(0, tk.END)
        metrics_names, metrics = metrics_calculation(xml_files)
        print("CLASSNAME\t" + '\t'.join(metrics_names))
        # Построение гистограммы на основе данных из xml файлов
        fig, ax = plt.subplots(nrows=1, ncols=len(metrics), figsize=(18, 10))
        fig.suptitle("Metrics:\nfn — false negative\n"
                     "fp — false positive\n"
                     "acc — accuracy\n"
                     "prec — precision\n"
                     "rec — recall\n"
                     "f1 — score",
                     x=0.95, y=0.5)
        # Вывод вычисленных метрик по данным из xml файлов в консоль и на гистограмму
        for i, classname in enumerate(metrics):
            print("%10s\t" % classname + "\t".join("{:0.2f}".format(value) for value in metrics[classname].values()))
            values = metrics[classname].values()
            # Заголовок гистограммы
            ax[i].set_title(classname)
            # Спрятать метки внизу гистограммы
            ax[i].tick_params(bottom=False)
            # Спрятать метки и диапазон значений по оси y на всех гистограммах кроме первой
            ax[i].axes.get_yaxis().set_visible(False)
            ax[0].axes.get_yaxis().set_visible(True)
            ax[i].bar(metrics_names, values)
            for j, value in enumerate(values):
                ax[i].text(j, value, round(value, 2), horizontalalignment="center", verticalalignment="bottom")
        print("----------------------------------------------------------\n")
        # Спрятать интервал между гистограммами
        plt.subplots_adjust(wspace=0, hspace=0)
        plt.show()
        self.quit()

    # Удаление файла(ов) при нажатии или выделении через shift
    def delete_file(self):
        select = list(self.list_box.curselection())
        select.reverse()
        for i in select:
            filepath = self.list_box.get(i)
            if filepath == self.filepath_first:
                self.filepath_first = None
            elif filepath == self.filepath_second:
                self.filepath_second = None
            self.list_box.delete(i)
            print(filepath + " DELETED")

    def update_clock(self):
        """
        Таймер, который проверяет через каждые (несколько) миллисекунд на наличие двух загруженных xml файлов.
        Если оба xml файла не загружены, то кнопка button_histogram недоступна.
        """
        if self.filepath_first:
            self.label_first.config(text=os.path.basename(self.filepath_first) + " LOADED", fg="blue")
        else:
            self.label_first.config(text="missing file", fg="red")

        if self.filepath_second:
            self.label_second.config(text=os.path.basename(self.filepath_second) + " LOADED", fg="blue")
        else:
            self.label_second.config(text="missing file", fg="red")

        if self.list_box.size() == 2:
            self.button_histogram.config(state=tk.ACTIVE, bg="#ffb841")
        else:
            self.button_histogram.config(state=tk.DISABLED, bg="white")
        self.after(100, self.update_clock)

def main():
    root = tk.Tk()
    # Ширина экрана
    width = root.winfo_screenwidth()
    # Высота экрана
    height = root.winfo_screenheight()
    # Середина экрана
    width = width//2
    height = height//2
    # Смещение от середины
    width = width - 200
    height = height - 200
    root.title("Choose FILES")
    # Размеры GUI приложения
    root.geometry("400x200+{}+{}".format(width, height))
    # Масштабирование
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    root.grid_columnconfigure(2, weight=1)
    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=1)
    root.grid_rowconfigure(2, weight=1)
    root.grid_rowconfigure(3, weight=1)
    Application(master=root)
    root.mainloop()

if __name__ == "__main__":
    main()





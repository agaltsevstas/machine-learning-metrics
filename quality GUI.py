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

class Metrics:
    def __init__(self):
        self.tp = 0
        self.fp = 0
        self.tn = 0
        self.fn = 0

    def number(self):
        return self.tp + self.fn

    def accuracy(self):
        sum = self.tp + self.fp + self.tn + self.fn
        if sum == 0:
            return 0
        return (self.tp + self.tn) / sum

    def precision(self):
        sum = self.tp + self.fp
        if sum == 0:
            return 0
        return self.tp / sum

    def recall(self):
        sum = self.tp + self.fn
        if sum == 0:
            return 0
        return self.tp / sum

    def values(self):
        num = 1
        if self.number() > 0:
            num = self.number()
        return 1.0*self.fn/num, self.fp/num, self.accuracy(), self.precision(), self.recall()

    @staticmethod
    def str_header():
        return ["fn", "fp", "acc", "prec", "rec"]

def quality_calculation(xml_paths):
    qualities = {}
    files_objects = [pm.readXml(xml_path, "basename") for xml_path in xml_paths]
    for src_file in files_objects[0]:
        src_objects = files_objects[0][src_file]
        proc_objects = []
        for proc_file in files_objects[1]:
            if proc_file == src_file:
                proc_objects = files_objects[1][proc_file]
                break
        if proc_file != src_file:
            continue
        # Image not found in processed list
        if len(proc_objects) == 0:
            continue
        # Objects loops
        src_pairs = np.zeros(len(src_objects), np.int32)
        proc_pairs = np.zeros(len(proc_objects), np.int32)
        for i in range(len(src_objects)):
            src_class = src_objects[i][4]
            if src_class not in qualities:
                qualities[src_class] = Metrics()
            for j in range(len(proc_objects)):
                proc_class = proc_objects[j][4]
                # True positive
                if src_class == proc_class and pm.same(src_objects[i], proc_objects[j], 0.3):
                    src_pairs[i] = 1
                    proc_pairs[j] = 1
                    qualities[src_class].tp += 1
        # False positive
        for j in range(len(proc_objects)):
            if proc_pairs[j] == 0:
                proc_class = proc_objects[j][4]
                if proc_class not in qualities:
                    qualities[proc_class] = Metrics()
                qualities[proc_class].fp += 1
        # False negative
        for j in range(len(src_objects)):
            if src_pairs[j] == 0:
                src_class = src_objects[j][4]
                qualities[src_class].fn += 1

    metrics_names = Metrics.str_header()
    return metrics_names, qualities

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
        self.button_file_first = tk.Button(text="Load XML",   activeforeground="blue", bg="#4e9a06",
                                           command=lambda: self.open_xml(self.file_first))
        self.button_file_first.grid(row=0, column=0, sticky="nsew")
        self.button_file_second = tk.Button(text="Load XML",  activeforeground="blue", bg="#ffff00",
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

    def open_xml(self, file_selection):
        filepath = tk.filedialog.askopenfilename(initialdir=dir, title="Select XML First",
                                                 filetypes=[("XML files", "*.xml")])
        if len(filepath) and not filepath == self.filepath_first and not filepath == self.filepath_second:
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

    def question_exit(self):
        ask = messagebox.askquestion("Exit", "Are you sure to quit?")
        if ask == "yes":
            self.tk.quit()

    def histogram(self):
        xml_files = self.list_box.get(0, tk.END)
        # values = np.array(["", ""])
        # description = "Compares two lists to measure quality"
        # values = pm.parseArguments(sys.argv, xml_files, values, __file__, description)
        metrics_names, qualities = quality_calculation(xml_files)
        print("CLASSNAME\t" + '\t'.join(metrics_names))
        fig, ax = plt.subplots(nrows=1, ncols=len(qualities), figsize=(18, 10))
        fig.suptitle("Metrics:\nfn — false negative\n"
                     "fp — false positive\n"
                     "acc — accuracy\n"
                     "prec — precision\n"
                     "rec — recall", x=0.95, y=0.5)
        for i, classname in enumerate(qualities):
            print("%10s\t" % classname + "\t".join("{:0.2f}".format(value) for value in qualities[classname].values()))
            values = qualities[classname].values()
            x = range(len(values))
            ax[i].set_title(classname)
            # ax[i].axis('off')
            # ax[i].yaxis.set_ticklabels([])
            ax[i].tick_params(labelleft="off", left=False)
            fig.set
            # ax[i].set_Xticklabels([])
            ax[i].axes.get_yaxis().set_visible(False)
            ax[0].axes.get_yaxis().set_visible(True)
            ax[i].bar(metrics_names, values)
            for j, value in enumerate(values):
                ax[i].text(j, value, round(value, 2), horizontalalignment="center", verticalalignment="bottom")
        print("----------------------------------------------------------\n")
        plt.subplots_adjust(wspace=0, hspace=0)
        plt.show()
        self.tk.quit()

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
    root.geometry("400x200+{}+{}".format(width, height))
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





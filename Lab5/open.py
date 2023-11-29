import pandas as pd


def open_new_csv(csv_path: str) -> pd.DataFrame:
    '''Function for opening the original annotation as a dataframe,
    naming columns of the dataframe and removing unnecessary'''
    dframe = pd.read_csv(
        csv_path, delimiter=",", names=["Absolute path", "Relative path", "Class"]
    )
    dframe = dframe.drop("Relative path", axis=1)
    return dframe

def open_csv(csv_path: str) -> pd.DataFrame:
    '''Function for opening the csv-annotation as a dataframe'''
    dframe = pd.read_csv(csv_path)
    return dframe

def save_csv(dframe: pd.DataFrame, file_path: str) -> None:
    '''Function of saving a dataframe to a csv file'''
    dframe.to_csv(file_path, index=False)




import cv2
import os
import logging
import pandas as pd
import matplotlib.pyplot as plt


logging.basicConfig(level=logging.INFO)


def generate_frame(frame: pd.DataFrame, label_class: str) -> pd.DataFrame:
    '''сформировать DataFrame из названия класса и абсолютного пути к файлу; 
    добавление столбца с меткой и трех столбцов, содержащих информацию об изображении'''
    try:
        height_image = []
        width_image = []
        depth_image = []
        number_label = []
        count = 0
        for path in frame["Absolute path"]:
            image = cv2.imread(path)
            # количество строк, количество столбцов, глубина [количество каналов]
            cv_image = image.shape
            height_image.append(cv_image[0])
            width_image.append(cv_image[1])
            depth_image.append(cv_image[2])
            if frame.loc[count, "Class"] == label_class:  # перебираем каждую строку
                label = 0
            else:
                label = 1
            number_label.append(label)
            count += 1
        frame["Height"] = height_image
        frame["Width"] = width_image
        frame["Depth"] = depth_image
        frame["Label"] = number_label
        return frame
    except:
        logging.error("Error in generate_frame \n")


def balance_test(frame: pd.DataFrame) -> pd.DataFrame:
    '''вычислить статистическую информацию для столбцов; определить, является ли набор сбалансированным'''
    try:
        label_info = frame["Label"].value_counts()
        balanced = label_info.values[0] / label_info.values[1]
        if balanced >= 0.9 and balanced <= 1.1:
            logging.info(f"Набор сбалансирован")
        else:
            logging.info("Набор не сбалансирован")
        return frame[["Height", "Width", "Depth"]].describe()
    except:
        logging.error("Errot in balance_test")


def filter(frame: pd.DataFrame, label: int) -> pd.DataFrame:
    '''возвращает отфильтрованный по метке DataFrame'''
    filter_frame = frame[frame["Label"] == label]
    return filter_frame


def max_filter(frame: pd.DataFrame, width_max: int, height_max: int, label: int) -> pd.DataFrame:
    '''фильтрация по максимальному значению'''
    filter_frame = frame[(frame["Height"] <= height_max) & (
        frame["Width"] <= width_max) & (frame["Label"] == label)]
    return filter_frame


def grouping(frame: pd.DataFrame) -> pd.DataFrame:
    '''группировка по количеству пикселей'''
    frame["Pixels"] = frame["Height"] * frame["Width"]
    frame_groupy = frame.groupby(["Label"]).agg(
        {"Pixels": ["max", "min", "mean"]})
    return frame_groupy


def histogram(frame: pd.DataFrame, label: int) -> list:
    '''строит гистограмму с использованием средств библиотеки OpenCV'''
    try:
        image = filter(frame, label)["Absolute path"].sample().values[0]
        image_bgr = cv2.imread(image)
        height, width, depth = image_bgr.shape
        b, g, r = cv2.split(image_bgr)
        hist_b = cv2.calcHist([b], [0], None, [256], [0, 256])
        hist_g = cv2.calcHist([g], [0], None, [256], [0, 256])
        hist_r = cv2.calcHist([r], [0], None, [256], [0, 256])
        hists = [hist_b, hist_g, hist_r]
        print(hists)
        return hists
    except:
        logging.error(f"File for histogram was not found: \n")


def draw_histogram(hists: list) -> None:
    '''отрисовка гистограмм'''
    colors = ["blue", "green", "red"]
    for i in range(len(hists)):
        plt.plot(hists[i], color=colors[i], label=f"Histogram_{i}")
        plt.xlim([0, 256])
    plt.ylabel("strenght")
    plt.title("Histograms")
    plt.xlabel("range")
    plt.legend()
    plt.show()


def open_new_csv(csv_path: str) -> pd.DataFrame:
    '''открытие файла для именования столбцов и удаления Relative path'''
    frame = pd.read_csv(
        csv_path, delimiter=",", names=["Absolute path", "Relative path", "Class"]
    )
    frame_copy = frame.drop("Relative path", axis=1)
    return frame_copy


def save_csv(frame: pd.DataFrame, file_path: str) -> None:
    '''сохранение DataFrame в файл'''
    frame.to_csv(file_path, index=False)  # экспорт данных без индексов


if __name__ == "__main__":
    frame = generate_frame(open_new_csv('lab4/set/dataset.csv'), "cat")
    print(frame)
    save_csv(frame, 'lab4/set/frame.csv')
    save_csv(balance_test(frame), 'lab4/set/balance_test.csv')
    save_csv(filter(frame, 1), 'lab4/set/filter.csv')
    max_width = frame['Width'].max()
    max_height = frame['Height'].max()
    save_csv(max_filter(frame, max_width, max_height,  1), 'lab4/set/max_filter.csv')
    save_csv(grouping(frame), 'lab4/set/grouping.csv')
    print(grouping(frame))
    print(frame[["Height", "Width", "Depth"]].describe())
    draw_histogram(histogram(frame, 1))
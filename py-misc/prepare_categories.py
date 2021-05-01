import sys
import json
import pprint
import random
import argparse
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import Qt as qt

from data_record import DataRecord

def fix_by_newline(s, threshold=110):
    s_new = ''

    for line in s.split('\n'):
        for i in range(len(line) // threshold + 1):
            s_new += line[i * threshold: (i + 1) * threshold] + '\n'

    return s_new

class TgChannelManager:
    def __init__(self, start_index, category_dict, tg_channels, log_name):
        self.__category_dict = category_dict
        self.__tg_channels = tg_channels
        self.__is_main_category_used = True
        self.__index = start_index
        self.__category_indices = []
        self.__log_name = log_name
        self.__last_category_name = ''

        self.__loaded_indices = set()

        # Create the file if it doesn't exist
        with open(log_name, 'a') as f:
            pass

        with open(log_name, 'r') as f:
            for line in f.readlines():
                idx = int(line.split(' ')[0])
                self.__loaded_indices.add(idx)

    def forward(self, category_index):
        if not self.__is_main_category_used:
            meta_category_name = list(self.__category_dict.keys())[self.__category_indices[0]]

            if category_index >= len(self.__category_dict[meta_category_name]):
                return False

        elif category_index >= len(self.__category_dict):
            return False

        self.__category_indices.append(category_index)

        if not self.__is_main_category_used:
            self.__is_main_category_used = True
            self.__log()

            if self.__index < len(self.__tg_channels) - 1:
                self.__index += 1
                return True
            else:
                return False
        else:
            self.__is_main_category_used = False
            return True

    def back(self):
        self.__is_main_category_used = True

        if self.__index > 0:
            self.__index -= 1
            return True
        else:
            return False

    def reset(self):
        self.__is_main_category_used = True
        self.__category_indices.clear()

    def skip(self):
        self.reset()

        if self.__index < len(self.__tg_channels) - 1:
            self.__index += 1
            return True
        else:
            return False

    def get_index(self):
        return self.__index

    def get_channel(self):
        return self.__tg_channels[self.__index]

    def is_main_category_used(self):
        return self.__is_main_category_used

    def get_last_category_name(self):
        return self.__last_category_name

    def get_all_index_count(self):
        return len(self.__loaded_indices)

    def __log(self):
        meta_category_name = list(self.__category_dict.keys())[self.__category_indices[0]]
        category_name = self.__category_dict[meta_category_name][self.__category_indices[1]]
        self.__last_category_name = category_name

        with open(self.__log_name, 'a') as f:
            f.write(f'{self.__index} {category_name}\n')

        self.__loaded_indices.add(self.__index)
        self.__category_indices.clear()

    def __len__(self):
        return len(self.__tg_channels)

class MyWidget(QtWidgets.QWidget):
    digit_keys = [qt.Key_1, qt.Key_2, qt.Key_3, qt.Key_4, qt.Key_5, qt.Key_6, qt.Key_7, qt.Key_8, qt.Key_9, qt.Key_0]
    category_indices = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]

    def __init__(self, categoryDict, tgChannelManager):
        super().__init__()

        self.channelTitle = QtWidgets.QLabel('', alignment=QtCore.Qt.AlignLeft)

        self.channelDescription = QtWidgets.QLabel('', alignment=QtCore.Qt.AlignLeft)
        self.channelRecentPosts = QtWidgets.QListWidget()
        self.channelRecentPosts.setFocusPolicy(qt.NoFocus)
        self.channelRecentPosts.setHorizontalScrollBarPolicy(qt.ScrollBarAlwaysOff);

        self.leftDescriptionLayout = QtWidgets.QVBoxLayout()
        self.leftDescriptionLayout.addWidget(self.channelTitle)
        self.leftDescriptionLayout.addWidget(self.channelDescription)
        self.leftDescriptionLayout.addStretch()

        self.leftChannelLayout = QtWidgets.QVBoxLayout()
        self.leftChannelLayout.addLayout(self.leftDescriptionLayout, 1)
        self.leftChannelLayout.addWidget(self.channelRecentPosts, 12)

        self.leftLayout = QtWidgets.QVBoxLayout()
        self.leftLayout.addLayout(self.leftChannelLayout, 3)

        self.rightStackedLayout = QtWidgets.QStackedLayout()
        self.rightStackedLayout.addWidget(self.get_category_layout(categoryDict.keys()))

        for categoryKey in categoryDict.keys():
            self.rightStackedLayout.addWidget(self.get_category_layout(categoryDict[categoryKey]))

        self.rightLayout = QtWidgets.QVBoxLayout()
        self.rightLayout.addLayout(self.rightStackedLayout)
        self.rightLayout.addStretch()

        self.contentLayout = QtWidgets.QHBoxLayout()
        self.contentLayout.addLayout(self.leftLayout, 1)
        self.contentLayout.addLayout(self.rightLayout, 1)

        self.statusBar = QtWidgets.QStatusBar()

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addLayout(self.contentLayout)
        self.layout.addWidget(self.statusBar)
        self.setLayout(self.layout)

        self.tgChannelManager = tgChannelManager
        self.update_channel()

    def keyPressEvent(self, event):
        keyPressed = event.key()

        if keyPressed in self.digit_keys:
            keyIndex = self.digit_keys.index(keyPressed)
            status = self.tgChannelManager.forward(keyIndex)

            if status:
                if not self.tgChannelManager.is_main_category_used():
                    self.rightStackedLayout.setCurrentIndex(keyIndex + 1)
                else:
                    self.rightStackedLayout.setCurrentIndex(0)
                    self.update_channel()

        elif keyPressed == qt.Key_Backspace:
            self.tgChannelManager.back()
            self.rightStackedLayout.setCurrentIndex(0)
            self.update_channel()

        elif keyPressed == qt.Key_Space:
            self.tgChannelManager.skip()
            self.rightStackedLayout.setCurrentIndex(0)
            self.update_channel()

        elif keyPressed == qt.Key_Escape:
            self.tgChannelManager.reset()
            self.rightStackedLayout.setCurrentIndex(0)

    def get_category_layout(self, categories):
        container = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(container)

        for i, category in enumerate(categories):
            category_index = self.category_indices[i]
            label = QtWidgets.QLabel(f'[{category_index}] {category}', alignment=QtCore.Qt.AlignLeft)
            layout.addWidget(label)

        return container

    def update_channel(self):
        index = self.tgChannelManager.get_index()
        statusBarText = f'{index} / {len(self.tgChannelManager)}'

        all_index_count = self.tgChannelManager.get_all_index_count()
        statusBarText += f' ({all_index_count})'

        if len(self.tgChannelManager.get_last_category_name()) > 0:
            statusBarText += f' {self.tgChannelManager.get_last_category_name()}'

        self.statusBar.showMessage(statusBarText)

        channel = self.tgChannelManager.get_channel()
        self.channelTitle.setText(channel.title)
        self.channelDescription.setText(fix_by_newline(channel.description))
        self.channelRecentPosts.clear()

        for i in range(len(channel.recent_posts)):
            recentPost = fix_by_newline(channel.recent_posts[i])
            self.channelRecentPosts.addItem(QtWidgets.QListWidgetItem(recentPost))

if __name__ == '__main__':
    with open('categories.json', 'r') as f:
        categoryDict = json.load(f)

    parser = argparse.ArgumentParser()
    parser.add_argument('--start_index', type=int, default=0)
    parser.add_argument('--dataset_name', default='../../preprocessed/dc-concat-ar-1k-translated.txt')
    parser.add_argument('--out_log_name', default='../../outputs/dc-concat-ar-1k-ground-truth.txt')
    args = parser.parse_args()

    pp = pprint.PrettyPrinter(indent=4)
    tgChannels = []

    with open(args.dataset_name, 'r') as f:
        for line in f.readlines():
            tgChannel = DataRecord(line, pp)
            tgChannels.append(tgChannel)

    tgChannelManager = TgChannelManager(args.start_index, categoryDict, tgChannels, args.out_log_name)

    app = QtWidgets.QApplication([])
    widget = MyWidget(categoryDict, tgChannelManager)
    widget.setWindowTitle('Data Clustering Contest 2021 - Markup')
    widget.show()

    with open('style.qss', 'r') as f:
        _style = f.read()
        app.setStyleSheet(_style)

    sys.exit(app.exec_())

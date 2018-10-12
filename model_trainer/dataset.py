import numpy as np
from PIL import Image
import os
import random


class DishDataset:

    def __init__(self, data_dir):
        
        self.cursor = 0
        self.test_cursor = 0
        self.data = []
        self.train_data = []
        self.test_data = []
        
        with open('labels.txt') as labels_text:
            data_labels = labels_text.readlines()
            # remove whitespace characters like `\n` at the end of each line
        data_labels = [label.strip() for label in data_labels]
        
        for index in range(10):
            images = os.listdir(os.path.join(data_dir, data_labels[index]))
            images = [os.path.join(data_dir, data_labels[index], image) for image in images]
            count = 0
            for image in images:
                if count < 1500:
                    if '._' not in image:
                        if DishDataset.is_RGB(image):
                            self.data.append({'image': image, 'label': index})
                            count += 1
        random.shuffle(self.data)
        training_size = int(len(self.data)*0.7)
        self.train_data = self.data[:training_size]
        self.test_data = self.data[training_size:]
        print(len(self.train_data))
        print(len(self.test_data))

    def sample(self, batch_size):
        batch = self.train_data[self.cursor:self.cursor+batch_size]
        if len(batch) < batch_size:     # Corner case f we need to wrap around the data
            batch += self.train_data[0:(self.cursor+batch_size) % len(self.train_data)]
        self.cursor = (self.cursor + batch_size) % len(self.train_data)

        images = [sample['image'] for sample in batch]
        new_images = []
        for image in images:
            image = DishDataset.read_image(image)
            if image is not None:
                new_images.append(image)
        images = new_images
        images = np.stack(images)

        labels = [sample['label'] for sample in batch]
        labels = [DishDataset.one_hot(label) for label in labels]
        labels = np.stack(labels)

        return images, labels

    def test_sample(self, batch_size):
        batch = self.test_data[self.test_cursor:self.test_cursor+batch_size]
        if len(batch) < batch_size:     # Corner case f we need to wrap around the data
            batch += self.test_data[0:(self.test_cursor+batch_size) % len(self.test_data)]
        self.test_cursor = (self.test_cursor + batch_size) % len(self.test_data)

        images = [sample['image'] for sample in batch]
        new_images = []
        for image in images:
            image = DishDataset.read_image(image)
            if image is not None:
                new_images.append(image)
        images = new_images
        images = np.stack(images)

        labels = [sample['label'] for sample in batch]
        labels = [DishDataset.one_hot(label) for label in labels]
        labels = np.stack(labels)

        return images, labels

    # def __len__(self):
    #     return len(self.train_data)

    def __len__(self):
        return len(self.test_data)
    
    @staticmethod
    def is_RGB(image_path):
        if '.DS_Store' in image_path:
            # print("Skipping .DS_Store file")
            return False

        """
        image = Image.open(image_path)
        if image.mode == 'RGB':
            return True
        
        else:
            print("Image File: {} is Gray Scale".format(image_path))
            return False
        """
        return True

    @staticmethod
    def read_image(image_path):
        try:
            image = Image.open(image_path)              # Image object
        except OSError:
            print(image_path)
            return None
        if image.mode != 'RGB':
            # print(image_path)
            image = image.convert('RGB')
        image = image.resize((128, 128))
        image = np.array(image)                     # Multi-dimentional array
        image = image.astype(np.float32)            # uint to float
        image = image / 255                         # 0-255 -> 0-1
        return image

    @staticmethod
    def one_hot(label):
        encoded_label = np.zeros(10)
        encoded_label[label] = 1
        return encoded_label

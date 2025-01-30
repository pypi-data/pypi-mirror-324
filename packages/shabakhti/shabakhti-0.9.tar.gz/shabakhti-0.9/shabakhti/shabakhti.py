import numpy as np
from PIL import Image, ImageDraw
from tensorflow.keras.models import load_model
from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import to_categorical
from tensorflow.keras import layers, models
import cv2
import tkinter as tk

class Hoshe:
    def __init__(self):
        self.model = self.load_or_train_model()

    def train_model(self):
        # بارگذاری داده‌های MNIST
        (x_train, y_train), (x_test, y_test) = mnist.load_data()

        # نرمال‌سازی داده‌ها
        x_train = x_train.astype('float32') / 255.0
        x_test = x_test.astype('float32') / 255.0

        # تغییر شکل داده‌ها برای ورودی شبکه CNN
        x_train = x_train.reshape(-1, 28, 28, 1)
        x_test = x_test.reshape(-1, 28, 28, 1)

        # تبدیل برچسب‌ها به دسته‌بندی یک-داغ (One-Hot Encoding)
        y_train = to_categorical(y_train, 10)
        y_test = to_categorical(y_test, 10)

        # ساخت مدل CNN
        model = models.Sequential()
        model.add(layers.Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(28, 28, 1)))
        model.add(layers.MaxPooling2D(pool_size=(2, 2)))
        model.add(layers.Conv2D(64, kernel_size=(3, 3), activation='relu'))
        model.add(layers.MaxPooling2D(pool_size=(2, 2)))
        model.add(layers.Flatten())
        model.add(layers.Dense(128, activation='relu'))
        model.add(layers.Dense(10, activation='softmax'))

        # کامپایل مدل
        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

        # آموزش مدل
        model.fit(x_train, y_train, epochs=5, batch_size=128, validation_data=(x_test, y_test))

        # ذخیره مدل آموزش دیده
        model.save('digit_recognizer_model.h5')
        return model

    def load_or_train_model(self):
        try:
            model = load_model('digit_recognizer_model.h5')
        except:
            model = self.train_model()
        return model

    def preprocess_image(self, img):
        # تغییر اندازه تصویر به 28x28
        img = img.resize((28, 28))

        # تبدیل به آرایه numpy
        img_array = np.array(img)

        # معکوس کردن رنگ‌ها
        img_array = 255 - img_array

        # اعمال آستانه برای باینری کردن تصویر
        img_array = cv2.threshold(img_array, 30, 255, cv2.THRESH_BINARY)[1]

        # نرمال‌سازی
        img_array = img_array / 255.0

        # تغییر شکل آرایه برای ورودی مدل
        img_array = img_array.reshape(1, 28, 28, 1)

        return img_array

class DigitRecognizerApp:
    def __init__(self, master):
        self.master = master
        master.title("تشخیص زنده‌ی عدد دست‌نویس با دقت بالا")

        # ایجاد کانواس برای نقاشی
        self.canvas = tk.Canvas(master, width=300, height=300, bg="white")
        self.canvas.pack()

        # دکمه پاک‌کردن
        self.clear_button = tk.Button(master, text="پاک‌کردن", command=self.clear)
        self.clear_button.pack()

        # نمایش نتیجه
        self.label = tk.Label(master, text="عدد پیش‌بینی شده: ", font=("Arial", 20))
        self.label.pack()

        # تنظیمات نقاشی
        self.image = Image.new("L", (300, 300), color=255)
        self.draw = ImageDraw.Draw(self.image)
        self.canvas.bind("<B1-Motion>", self.paint)
        
        # بهبود ترسیم با ذخیره موقعیت قبلی ماوس
        self.last_x, self.last_y = None, None

        # به‌روزرسانی پیش‌بینی در زمان واقعی
        self.update_prediction()

        # بارگذاری مدل
        self.hoshe = Hoshe()

    def paint(self, event):
        x, y = event.x, event.y
        r = 8  # شعاع قلم
        if self.last_x and self.last_y:
            self.canvas.create_line(self.last_x, self.last_y, x, y, fill="black", width=r*2)
            self.draw.line([self.last_x, self.last_y, x, y], fill=0, width=r*2)
        self.last_x, self.last_y = x, y

    def clear(self):
        self.canvas.delete("all")
        self.image = Image.new("L", (300, 300), color=255)
        self.draw = ImageDraw.Draw(self.image)
        self.label.config(text="عدد پیش‌بینی شده: ")
        self.last_x, self.last_y = None, None

    def update_prediction(self):
        # پیش‌پردازش تصویر
        img = self.image.copy()
        img_array_full = np.array(img)

        # بررسی اینکه آیا تصویری کشیده شده است یا نه
        if np.count_nonzero(img_array_full) < img_array_full.size - 50:
            img_array = self.hoshe.preprocess_image(img)
            # پیش‌بینی
            prediction = self.hoshe.model.predict(img_array)
            result = np.argmax(prediction)
            confidence = np.max(prediction) * 100
            self.label.config(text=f"عدد پیش‌بینی شده: {result} (اعتماد: {confidence:.2f}%)")
        else:
            self.label.config(text="عدد پیش‌بینی شده: ")

        # به‌روزرنیی مجدد پس از 200 میلی‌ثانیه
        self.master.after(200, self.update_prediction)

def shabakhti():
    root = tk.Tk()
    app = DigitRecognizerApp(root)
    root.mainloop()



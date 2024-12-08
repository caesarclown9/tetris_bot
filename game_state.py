
import pyautogui
import numpy as np
import cv2

DEBUG = True  

def preprocess_image(image):
    """
    Обрабатывает изображение для улучшения контраста и удаления фона.
    :param image: Исходное изображение (numpy array).
    :return: Обработанное бинарное изображение.
    """

    image = cv2.equalizeHist(image)
    

    binary_image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                        cv2.THRESH_BINARY, 11, 2)
    

    kernel = np.ones((2,2), np.uint8)
    binary_image = cv2.morphologyEx(binary_image, cv2.MORPH_OPEN, kernel)
    binary_image = cv2.morphologyEx(binary_image, cv2.MORPH_CLOSE, kernel)
    
    return binary_image

def find_game_area_using_template(template_path, threshold=0.8):
    """
    Ищет игровую область на экране с использованием шаблона.
    :param template_path: Путь к файлу с изображением шаблона игрового поля.
    :param threshold: Порог совпадения (0.0 - 1.0).
    :return: Координаты области игры (x, y, w, h) или None, если не найдено.
    """

    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    if template is None:
        raise ValueError(f"Шаблон {template_path} не найден или поврежден.")
    template_height, template_width = template.shape


    screenshot = pyautogui.screenshot()
    full_image = cv2.cvtColor(np.array(screenshot), cv2.COLOR_BGR2GRAY)

    if DEBUG:
        cv2.imwrite("debug_screenshot.png", full_image)
        cv2.imwrite("debug_template.png", template)


    result = cv2.matchTemplate(full_image, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)


    print(f"Уровень совпадения: {max_val:.2f}")


    if max_val >= threshold:
        print(f"Игровая область найдена с уверенностью {max_val * 100:.2f}%")
        return max_loc[0], max_loc[1], template_width, template_height
    else:
        print("Игровая область не найдена! Попробуйте уменьшить порог или уточнить шаблон.")
        return None

def get_game_state(template_path):
    """
    Определяет состояние игры, используя найденную игровую область.
    :param template_path: Путь к файлу с шаблоном игрового поля.
    :return: Изображение игрового поля или ошибка, если область не найдена.
    """
    game_area = find_game_area_using_template(template_path)
    if game_area is not None:
        x, y, w, h = game_area

        screenshot = pyautogui.screenshot(region=(x, y, w, h))
        game_image = cv2.cvtColor(np.array(screenshot), cv2.COLOR_BGR2GRAY)


        game_image = preprocess_image(game_image)

        if DEBUG:
            cv2.imwrite("debug_processed_game_image.png", game_image)

        resized_image = cv2.resize(game_image, (10, 20))
        return resized_image
    else:
        raise ValueError("Игровая область не найдена! Попробуйте проверить шаблон или снизить порог.")

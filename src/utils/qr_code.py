import cv2
from pyzbar.pyzbar import decode


def read_qr_from_image(image_path):
    """
    Считывает QR-код с изображения и возвращает зашифрованный текст.

    :param image_path: Путь к изображению с QR-кодом
    :return: Расшифрованный текст из QR-кода или сообщение об ошибке
    """
    try:
        # Загрузка изображения
        image = cv2.imread(image_path)
        if image is None:
            return "Ошибка: Не удалось загрузить изображение."

        # Декодирование QR-кода
        decoded_objects = decode(image)

        # Проверка наличия QR-кодов
        if not decoded_objects:
            return "QR-код не найден на изображении."

        # Получение текста из QR-кода
        qr_texts = [obj.data.decode("utf-8") for obj in decoded_objects]
        return qr_texts if len(qr_texts) > 1 else qr_texts[0]

    except Exception as e:
        return f"Ошибка: {e}"


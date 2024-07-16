import os
from PIL import Image


def images_from_folder(folder):
    images = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.tif')):
                file_path = os.path.join(root, file)
                img = Image.open(file_path)
                images.append(img)
    return images


def concatenate_images(images):
    num_images = len(images)
    num_columns = 2
    num_rows = (num_images + 1) // num_columns

    # нахождение максимальной ширины и высоты для каждой строки и столбца
    max_widths = [0] * num_columns
    max_heights = [0] * num_rows
    for i, image in enumerate(images):
        col = i % num_columns
        row = i // num_columns
        max_widths[col] = max(max_widths[col], image.width)
        max_heights[row] = max(max_heights[row], image.height)

    # расчет общей ширины и высоты итогового изображения
    total_width = sum(max_widths)
    total_height = sum(max_heights)

    # создание нового пустого изображения с расчетными размерами и вставка всех изображений
    concatenated_image = Image.new('RGB', (total_width, total_height))

    y_offset = 0
    for row in range(num_rows):
        x_offset = 0
        for col in range(num_columns):
            index = row * num_columns + col
            if index < num_images:
                image = images[index]
                concatenated_image.paste(image, (x_offset, y_offset))
                x_offset += max_widths[col]
        y_offset += max_heights[row]

    return concatenated_image


def main():
    base_folder = 'Для тестового'
    for folder_name in os.listdir(base_folder):
        folder_path = os.path.join(base_folder, folder_name)
        if os.path.isdir(folder_path):
            images = images_from_folder(folder_path)
            if images:
                concatenated_image = concatenate_images(images)
                output_file = f'{folder_name}.tif'
                concatenated_image.save(output_file)


if __name__ == "__main__":
    main()

import cv2

class PencilArt:
    def __init__(self, input_image_path, output_image_path):
        self.input_image_path = input_image_path
        self.output_image_path = output_image_path

    def convert_to_sketch(self):
        image = cv2.imread(self.input_image_path)

        if image is None:
            raise ValueError(f"Could not read the image: {self.input_image_path}")

        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred_image = cv2.GaussianBlur(gray_image, (21, 21), sigmaX=0, sigmaY=0)
        inverted_blur = cv2.bitwise_not(blurred_image)
        sketch = cv2.divide(gray_image, 255 - inverted_blur, scale=256)

        cv2.imwrite(self.output_image_path, sketch)
        print(f"Sketch saved at: {self.output_image_path}")

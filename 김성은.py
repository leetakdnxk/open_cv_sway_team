# Denoises a color image using grayscale conversion, Gaussian blur, and morphological opening
def remove_noise(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ksize = (5, 5)
    blurred_image = cv2.GaussianBlur(gray_image, ksize, 0)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    opened_image = cv2.morphologyEx(blurred_image, cv2.MORPH_OPEN, kernel)
    return opened_image

img1_denoised = remove_noise(img1)
img2_denoised = remove_noise(img2)
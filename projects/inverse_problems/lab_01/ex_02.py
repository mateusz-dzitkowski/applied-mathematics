import numpy as np
import cv2
import matplotlib.pyplot as plt
from scipy.signal import convolve2d
from skimage.restoration import wiener

# Step 1: Load an Example Image (Grayscale)
image = cv2.imread("lenna.png", cv2.IMREAD_GRAYSCALE)
# image = cv2.resize(image, (256, 256))  # Resize for simplicity
image = (image - image.min()) / (image.max() - image.min())

# Step 2: Define a Motion Blur Kernel (Point Spread Function - PSF)
def motion_blur_kernel(size=15, angle=0):
    """Generate a linear motion blur kernel."""
    kernel = np.zeros((size, size))
    kernel[size // 2, :] = 1  # Horizontal blur
    kernel = cv2.warpAffine(kernel,
                            cv2.getRotationMatrix2D((size // 2, size // 2), angle, 1),
                            (size, size))
    kernel /= np.sum(kernel)  # Normalize
    return kernel

# Create motion blur effect
kernel_size = 30
blur_kernel = motion_blur_kernel(size=kernel_size, angle=30)
blurred_image = convolve2d(image, blur_kernel, mode='same')
blurred_image += np.random.normal(scale=0.1, size=blurred_image.shape)

# Step 3: Apply Wiener Deconvolution for Deblurring
restored_image = wiener(blurred_image, blur_kernel, balance=0.1)  # Adjust balance factor

# Step 4: Plot the Images
fig, ax = plt.subplots(1, 3, figsize=(30, 10))

ax[0].imshow(image, cmap='gray')
ax[0].set_title("Original Image")
ax[0].axis("off")

ax[1].imshow(blurred_image, cmap='gray')
ax[1].set_title("Blurred Image")
ax[1].axis("off")

ax[2].imshow(restored_image, cmap='gray')
ax[2].set_title("Deblurred Image (Wiener)")
ax[2].axis("off")

plt.tight_layout()
plt.show()

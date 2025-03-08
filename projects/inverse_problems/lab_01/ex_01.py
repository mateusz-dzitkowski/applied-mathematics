import numpy as np
import matplotlib.pyplot as plt
from skimage.transform import radon, iradon
from PIL import Image


# Step 1: Create a Test Image (Phantom)
phantom = np.asarray(Image.open("brain.jpg").convert("L"))
phantom_scaled = (phantom - phantom.min()) / (phantom.max() - phantom.min())
phantom_resized = np.pad(phantom_scaled, (20, 20), "constant")

# Step 2: Compute Radon Transform (Sinogram)
theta = np.linspace(0., 180., max(phantom_resized.shape), endpoint=False)  # Define projection angles
sinogram = radon(phantom_resized, theta=theta, circle=True)
sinogram += np.random.normal(scale=50, size=sinogram.shape)

# Step 3: Perform Inverse Radon Transform (Reconstruction)
reconstructed_image = iradon(sinogram, theta=theta, filter_name='ramp')
reconstructed_image = (reconstructed_image - reconstructed_image.min()) / (reconstructed_image.max() - reconstructed_image.min())

# Step 4: Plot the Original, Sinogram, and Reconstructed Image
fig, axes = plt.subplots(1, 3, figsize=(40, 15))
axes[0].imshow(phantom_resized, cmap='gray')
axes[0].set_title("Original Phantom")
axes[0].axis("off")

axes[1].imshow(sinogram, cmap='gray', aspect='auto', extent=(0, 180, 0, sinogram.shape[0]))
axes[1].set_title("Sinogram (Radon Transform)")
axes[1].set_xlabel("Projection Angle (degrees)")
axes[1].set_ylabel("Projection Position")

axes[2].imshow(reconstructed_image, cmap='gray')
axes[2].set_title("Reconstructed Image")
axes[2].axis("off")

plt.tight_layout()
plt.show()

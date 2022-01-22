from PIL import Image
from torchvision import transforms
import numpy as np
from skimage.color import rgb2lab, lab2rgb
import torch
import fastai
import io
import base64

model = torch.load('./generator.pt')
model.eval()

def lab_to_rgb(L, ab):
    """
    Takes a batch of images
    """
    
    L = (L + 1.) * 50.
    ab = ab * 110.
    Lab = torch.cat([L, ab], dim=1).permute(0, 2, 3, 1).cpu().numpy()
    rgb_imgs = []
    for img in Lab:
        img_rgb = lab2rgb(img)
        rgb_imgs.append(img_rgb)
    return np.stack(rgb_imgs, axis=0)
    

def Colorizer(image):
    img = Image.open(image).convert("RGB")

    # Convert to np array
    img = np.array(img)

    # Converting RGB to L*a*b
    img_lab = rgb2lab(img).astype("float32") 

    # Convert to Tensor
    img_lab = transforms.ToTensor()(img_lab)

    # setting values in between -1 and 1
    L = img_lab[[0]] / 50. - 1. 
    ab = img_lab[[1, 2]] / 110.

    # predict
    predicted_ab = model(L.unsqueeze(0))

    # converting back to actual values and rgb
    fake_img = lab_to_rgb(L.unsqueeze(0), predicted_ab.detach())[0]

    bytes_img = io.BytesIO()

    im = Image.fromarray((fake_img*255).astype('uint8'))

    im.save(bytes_img, "PNG")

    bytes_img.seek(0)

    base64_img = base64.b64encode(bytes_img.read())

    return base64_img

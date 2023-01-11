import torch
import torch.nn as nn
import torchvision.transforms as transforms
import torch.utils.data as data
from CHR.models import resnet101_CHR
from CHR.util import Warp
from PIL import Image
import os

object_categories =['Gun','Knife','Wrench','Pliers','Scissors']
def load_image(path):
    img = Image.open(path).convert('RGB')
    return img

class SingleImageBatchLoader(data.Dataset):

    def __init__(self, root, transform=None):
        self.root = root
        self.path_images = os.path.join(root,  'JPEGImage')
        self.transform = transform
        self.classes = object_categories
        self.loaded = True

    def load(self, image_id):
        self.image_id = image_id
        self.loaded = False
        
    def __getitem__(self, index):
        img = load_image(os.path.join(self.path_images, '{}.jpg'.format(self.image_id)))
        if self.transform is not None:
            img = self.transform(img)
        
        self.loaded = True
        return img

    def __len__(self):
        res = int(not self.loaded)
        return res

    def get_number_classes(self):
        return len(self.classes)

def main_ray():
    num_classes = 5

    # load model
    model = resnet101_CHR(num_classes, pretrained=True)

    test_image_size = 224
    filename = os.path.join('./CHR/models-/checkpoint.pth.tar')
    checkpoint = torch.load(filename, map_location=torch.device('cpu'))
    model.load_state_dict(checkpoint['state_dict'])
    model.eval()

    image_id = 'P07122'
    
    transform = transforms.Compose([
        Warp(test_image_size),
        transforms.ToTensor(),
        transforms.Normalize(mean=model.image_normalization_mean, std=model.image_normalization_std),
    ])

    img = load_image(os.path.join('./dataset', 'JPEGImage', '{}.jpg'.format(image_id)))
    img_transformed = transform(img)
    batch_img_tensor = torch.unsqueeze(img_transformed, 0)
    target = model(batch_img_tensor)

    print('target: {}, image: {}'.format(target, image_id))

if __name__ == '__main__':
    main_ray()
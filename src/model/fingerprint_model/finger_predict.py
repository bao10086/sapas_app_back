# 导入包
import os



import torch
import torchvision.transforms as transforms
from PIL import Image
from finger_model import Finger_Model





def get_pic_files(path):
    pic = []
    for root, _, files in os.walk(path):
        for file in files:
            pic.append(os.path.join(path, file))
    return pic


def finger_predict_main(img_dir,model_dir):
    pic=get_pic_files(img_dir)
    count=0
    for file in os.listdir(img_dir): #file 表示的是文件名
        count = count+1
    for img in pic:
        im=Image.open(img).convert('RGB')
        model_path=model_dir
        #获取类别

        #获取类别
        nclass=count
        # 数据预处理
        transform = transforms.Compose(
            [transforms.Resize((224, 224)), # 首先需resize成跟训练集图像一样的大小
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])])
        im = transform(im)  # [C, H, W]
        im = torch.unsqueeze(im, dim=0)  # 对数据增加一个新维度，因为tensor的参数是[batch, channel, height, width] 

        # 实例化网络，加载训练好的模型参数
        net = Finger_Model(n_class=nclass).eval()
        net.load_state_dict(torch.load(model_path),False)
        with torch.no_grad():
    
            outputs = net(im)
            #print(outputs)
            predict = torch.max(outputs, dim=1)[1].data.numpy()
            #可以加入log
            pred_softmax = torch.softmax(outputs, dim=1)
            print(pred_softmax)
            if pred_softmax.max()<float(1.2/nclass) and nclass>1:
                return False
            if nclass ==1 and pred_softmax.max()<0.6:
                return False
    return True

    
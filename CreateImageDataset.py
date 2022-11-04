
import torchvision
import torchvision.transforms as transforms

'''
Under the project root path, create two folders `Train` and `Test`
In each folder, separate images to sub-folders with the folder names as class names. For example, Train\class1, Train\class2, Test\class1, Test\class2, etc.
Then use ImageFolder method of the visiondataset class to automatically create train or test dataset
The datasets are tuples that consist of images and their corresponding classes
'''

train_path = r'C:\Users\erwang\Documents\EricWang\U\phd\work4_openvino\dataset_GroupWorks\Train'
test_path = r'C:\Users\erwang\Documents\EricWang\U\phd\work4_openvino\dataset_GroupWorks\Test'

# train set
train_dataset = torchvision.datasets.ImageFolder(root=train_path, transform=transforms.ToTensor())
# test set
test_dataset = torchvision.datasets.ImageFolder(root=test_path, transform=transforms.ToTensor())

# display 1 image size and its label
for x,y in train_dataset:
    print(x.shape, y)
    break

# check how many labels
check_=0
for x,y in train_dataset:
    check_ += y
print(check_)
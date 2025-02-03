
# Light CNN for Deep Face Recognition, Lightweight & Accurate Face Recognition Model for Central Asian Faces.
A [PyTorch](http://pytorch.org/) implementation of [A Light CNN for Deep Face Representation with Noisy Labels](https://arxiv.org/abs/1511.02683) from the paper by Xiang Wu, Ran He, Zhenan Sun and Tieniu Tan.  The official and original Caffe code can be found [here](https://github.com/AlfredXiangWu/face_verification_experiment) and PyTorch code [here](https://github.com/AlfredXiangWu/LightCNN).  

### Table of Contents
- <a href='#updates'>Updates</a>
- <a href='#installation'>Installation</a>
- <a href='#datasets'>Datasets</a>
- <a href='#training'>Training</a>
- <a href='#evaluation'>Evaluate</a>
- <a href='#performance'>Performance</a>
- <a href='#citation'>Citation</a>
- <a href='#references'>References</a>

## Updates

- January 31, 2025
    - Initial commit
    - Upgraded to support Python 3.12+, got rid of Python 2.7 requirement.
    - Focused on LightCNN-v4 model only for better performance
    - Added preprocessing for face alignment, cropping, resizing and normalization
    - Added feature extraction and comparison
    - Simplified installation and usage process
    - Updated dependencies to latest stable versions

## Installation
- Clone this repository.

```bash
git clone https://github.com/YernarBekbolat/LightCNN-V4-PyTorch
```

- Create a virtual environment (optional).

```bash
python -m venv venv
venv\Scripts\activate
```

- Install the required dependencies.

```bash
pip install -r requirements.txt
```

## Usage
- Download LightCNN-v4 model from [here](https://drive.google.com/file/d/1zFB8RmxeS00Nbq2fM0EoME15RIHtVOqn/view?usp=sharing) and put it in the local directory.
**Note**: you don't need to unzip tar file, just download it and put it in the local directory.

- Collect your own dataset and put it in the local directory.

- Fullfll the test_list.txt file with the names of the images in your dataset. Example:
```
Face1.jpg
Face2.jpg
Face3.jpg
Face4.jpg
Face5.jpg
```

- Run the align_faces.py to align and crop the faces in your dataset. All aligned and cropped faces will be saved in the ./faces folder.
```bash
python align_faces.py
```

- Run the extract_features.py to extract the features faces folder. Features will be saved in the ./features folder.
```bash
python extract_features.py --resume LightCNN-V4_checkpoint.pth.tar --root_path ./faces/ --img_list test_list.txt --save_path ./features/ --cuda False
```

- Run the compare_features.py to compare the faces and get cosine similarity of the face pairs.
```bash
python compare_features.py --feat1 ./features/Face1.feat --feat2 ./features/Face2.feat     
```

## Datasets
Can be referred [here](https://github.com/AlfredXiangWu/LightCNN).  

## Training 
Can be referred [here](https://github.com/AlfredXiangWu/LightCNN).	 

## Evaluation

Can be referred [here](https://github.com/AlfredXiangWu/LightCNN).  

## Performance
Can be referred [here](https://github.com/AlfredXiangWu/LightCNN).   

## Citation
If you use authors models, please cite the following paper:
```
@article{wu2018light,
  title={A light CNN for deep face representation with noisy labels},
  author={Wu, Xiang and He, Ran and Sun, Zhenan and Tan, Tieniu},
  journal={IEEE Transactions on Information Forensics and Security},
  volume={13},
  number={11},
  pages={2884--2896},
  year={2018},
  publisher={IEEE}
}
```
	
## References
- [Original Light CNN implementation (caffe)](https://github.com/AlfredXiangWu/face_verification_experiment).
- [Original Light CNN implementation (pytorch)](https://github.com/AlfredXiangWu/LightCNN).



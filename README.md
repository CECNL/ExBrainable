# ExBrainable
An Open-Source GUI for CNN-based EEG Decoding and Model Interpretation.

We developed a graphic user interface (GUI), ExBrainable, which is dedicated to modeling, decoding, and visualization of electroencephalographic (EEG) data based on explainable neural network models. Available functions include model training, evaluation, and parameter visualization. Demonstration on motor-imagery EEG data exhibits the spatial and temporal representations of EEG patterns associated with prior knowledge of neuroscience. As a growing open-source platform, ExBrainable offers fast, simplified, and user-friendly analysis of EEG data using cutting-edge computational approaches for brain/neuroscience research.

## Installation
1. Install Python >= 3.7
2. Install Pytorch >= 1.0 from http://pytorch.org/ 
3. Use the package manager pip to install ExBrainable
```bash
$ pip install ExBrainable
```
4. Run ExBrainable
```bash
$ ExBrainable
```
To get the latest code using git and conda, open a terminal and type:
```bash
$ git clone https://github.com/CECNL/ExBrainable
$ cd ExBrainable
$ conda env create -f environment.yml 
$ conda activate ExBrainable 
```

## Documentation
See our preprint on ArXiv: https://arxiv.org/abs/2201.04065

## Demonstration
Here is a brief video demonstration of ExBrainable: https://youtu.be/m40z2klbmtg

## Dataset
The BCI Competition IV 2a dataset used in our paper is available on: https://www.bbci.de/competition/iv/. \
Example data used in the demo video can be downloaded here: https://drive.google.com/drive/folders/1-M-ZU1BbfwdiFP-jkPcCfu058fRzksSI?usp=sharing

## Citing
If you use this our codes in your research, please cite our paper and the related references in your publication as:
```bash
@article{huang2022exbrainable,
  title={ExBrainable: An Open-Source GUI for CNN-based EEG Decoding and Model Interpretation},
  author={Huang, Ya-Lin and Hsieh, Chia-Ying and Huang, Jian-Xue and Wei, Chun-Shu},
  journal={arXiv preprint arXiv:2201.04065},
  year={2022}
}
```
MNE-Python software:
```bash
@article{10.3389/fnins.2013.00267,
author={Gramfort, Alexandre and Luessi, Martin and Larson, Eric and Engemann, Denis and Strohmeier, Daniel and Brodbeck, Christian and Goj, Roman and Jas, Mainak and Brooks, Teon and Parkkonen, Lauri and Hämäläinen, Matti},
title={{MEG and EEG data analysis with MNE-Python}},
journal={Frontiers in Neuroscience},
volume={7},
pages={267},
year={2013},
url={https://www.frontiersin.org/article/10.3389/fnins.2013.00267},
doi={10.3389/fnins.2013.00267},
issn={1662-453X},
}
```
If you use the EEGNet model, please cite the following:
```bash
@article{Lawhern2018,
  author={Vernon J Lawhern and Amelia J Solon and Nicholas R Waytowich and Stephen M Gordon and Chou P Hung and Brent J Lance},
  title={EEGNet: a compact convolutional neural network for EEG-based brain–computer interfaces},
  journal={Journal of Neural Engineering},
  volume={15},
  number={5},
  pages={056013},
  url={http://stacks.iop.org/1741-2552/15/i=5/a=056013},
  year={2018}
}
```
If you use the ShalowConvNet model, please cite the following:
```bash
@article{hbm23730,
author = {Schirrmeister Robin Tibor and 
          Springenberg Jost Tobias and 
          Fiederer Lukas Dominique Josef and 
          Glasstetter Martin and 
          Eggensperger Katharina and 
          Tangermann Michael and 
          Hutter Frank and 
          Burgard Wolfram and 
          Ball Tonio},
title = {Deep learning with convolutional neural networks for EEG decoding and visualization},
journal = {Human Brain Mapping},
volume = {38},
number = {11},
pages = {5391-5420},
keywords = {electroencephalography, EEG analysis, machine learning, end‐to‐end learning, brain–machine interface, brain–computer interface, model interpretability, brain mapping},
doi = {10.1002/hbm.23730},
url = {https://onlinelibrary.wiley.com/doi/abs/10.1002/hbm.23730}
}
```
If you use the SCCNet model, please cite the following:
```bash
@inproceedings{wei2019spatial,
  title={Spatial component-wise convolutional network (SCCNet) for motor-imagery EEG classification},
  author={Wei, Chun-Shu and Koike-Akino, Toshiaki and Wang, Ye},
  booktitle={2019 9th International IEEE/EMBS Conference on Neural Engineering (NER)},
  pages={328--331},
  year={2019},
  organization={IEEE}
}
```

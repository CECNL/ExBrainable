# ExBrainable
An Open-Source GUI for CNN-based EEG Decoding and Model Interpretation.

We developed a graphic user interface (GUI), ExBrainable, which is dedicated to modeling, decoding, and visualization of electroencephalographic (EEG) data based on explainable neural network models. Available functions include model training, evaluation, and parameter visualization. Demonstration on motor-imagery EEG data exhibits the spatial and temporal representations of EEG patterns associated with prior knowledge of neuroscience. As a growing open-source platform, ExBrainable offers fast, simplified, and user-friendly analysis of EEG data using cutting-edge computational approaches for brain/neuroscience research.

## Installation
1. Install Python >= 3.7
2. Install Pytorch >= 1.0 from http://pytorch.org/ 
3. Use the package manager pip to install ExBrainable
```bash
pip install ExBrainable
```
4. Run GUI.py
```bash
python GUI.py
```
If you use conda, create and activate an environment for ExBrainable with:
```bash
conda env create -f environment.yml 
conda activate ExBrainable 
```

## Documentation
See our preprint on ArXiv: https://arxiv.org/abs/2201.04065

## Demonstration
Here is a brief video demonstration of ExBrainable: https://youtu.be/m40z2klbmtg

## Dataset
The BCI Competition IV 2a dataset used in our paper is available on: https://www.bbci.de/competition/iv/
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
as well as any model provided in the model base (see model.py for references).

# ExBrainable
An Open-Source GUI for CNN-based EEG Decoding and Model Interpretation
## Installation
We provides two choices to install ExBrainable GUI : 
### 1. Use ExBrainable on desktop  
1. Create and activate an environment for ExBrainable
```bash
conda env create -f environment.yml 
conda activate ExBrainable 
```
2. Run GUI.py
```bash
python GUI.py
```
### 2. In programming 
1. Install Python >= 3.7
2. Install Pytorch >= 1.0 from http://pytorch.org/ 
3. Use the package manager pip to install ExBrainable
```bash
pip install ExBrainable
```
### motor imagery data : BCICIV2a 
- data and labels are separated
- download [here](https://drive.google.com/drive/folders/1-M-ZU1BbfwdiFP-jkPcCfu058fRzksSI?usp=sharing)
## Video demonstration 
This is a brief video demonstration of ExBrainable : https://youtu.be/m40z2klbmtg
## Documentation
## Citing
1. ExBrainble on arxiv
2. mne-python 

### develop 
1. ReviseWithClass資料夾
- 放設計架構之後的code，epoching data在[這裡](https://drive.google.com/drive/folders/1oMi3sfp0MRpumd82yfguO083Fi2MIONK?usp=sharing)，
- dev資料夾獨立測試用

import setuptools
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"),"r") as fh:
    long_description = fh.read()



setuptools.setup(
     name='ExBrainable',  
     version='0.0.3',  
     author="Ya-Lin Huang", 
     author_email="yalinhuang.bt06@nycu.edu.tw",
     description="ExBrainable: An Open-Source GUI for CNN-based EEG Decoding and Model Interpretation",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/CECNL/ExBrainable",
     install_requires=['mne', 'numpy', 'scipy', 'matplotlib','torchsummary', 'sklearn'],
     packages=setuptools.find_packages(), #Use for other package dependencies.
     classifiers=[
        #'Development Status :: 3 - Alpha',  #not sure 

        # Indicate who your project is intended for
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        'Topic :: Software Development :: Build Tools',

        "Topic :: Scientific/Engineering :: Artificial Intelligence",

        # Pick your license as you wish (should match "license" above)
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.7',
    ],
    keywords='eeg deep-learning brain-state-decoding',
    include_package_data=False, # 沒有其他打包文件
    zip_safe=False, #whether the package is installed in compressed mode or regular mode.
)
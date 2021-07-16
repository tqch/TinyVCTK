# TinyVCTK

This repo contains a light-weight 8-bit encoded version of the original **V**oice **C**loning **T**ool**K**it (VCTK) dataset, which is directly adapted from an official subset, **D**evice **R**ecorded VCTK (DR-VCTK) except that:
- 16-bit data are encoded into 8-bit through mu-law transformation
- silence parts (below tenth of maximum magnitude) are trimmed from the start and the end of each track 

please check `preprocess_demo.py` for details

## Source

[[Download]](https://datashare.ed.ac.uk/download/DS_10283_3038.zip)

## Credit

Device Recorded VCTK (Small subset version)                        

RELEASE November 2017  
                                                            
National Institute of Informatics (NII)

JAPAN

Copyright (c) 2017  

The Centre for Speech Technology Research (CSTR)

University of Edinburgh

UK

Copyright (c) 2017  

Dr. Junichi Yamagishi

jyamagis@nii.ac.jp

jyamagis@inf.ed.ac.uk

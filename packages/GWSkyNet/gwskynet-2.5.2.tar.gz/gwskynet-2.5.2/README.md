# GWSkyNet

[GWSkyNet](https://iopscience.iop.org/article/10.3847/2041-8213/abc5b5), developed by Cabero et al 2020, is a machine learning classifier capable of distinguishing between astrophysical events and instrumental artifacts. Designed to facilitate potential EM follow-up observations, the classifier can be operated in low-latency and provide information complementary to what has previously been released in an Open Public Alert(OPA) seconds after an alert is published. A unique feature of the classifier is that it needs only the publicly available information from the OPA system. The classifier can also be expanded easily to intake other information such as the SNRs of a GW candidate in each detector in the network.

GWSkyNet is now being developed as a low-latency annotation pipeline for the fourth observing run of the LIGO Scientific and Virgo Collaboration (O4).

For more detail, please refer to the following document 

- [GWSkyNet design doc](https://dcc.ligo.org/LIGO-T2200100)    
- [Presentation to the low latency group](https://dcc.ligo.org/LIGO-G2200610)
- [Paper on GWSkyNet](https://iopscience.iop.org/article/10.3847/2041-8213/abc5b5)

## Getting started

The current version of GWSkyNet uses the following libaries:

- numpy       1.23.2
- astropy     5.1.1
- reproject   0.8
- ligo.skymap 1.0.2
- tensorflow  2.9.1
- scipy       1.8.0

Using GWSkyNet is easy.

To apply GWSkyNet to a graviational wave candidate to determine the origin of the gravitational wave candidate (glitch or astrophysical) , all is needed is a FITS file corresponding to the gravitational wave alert. Such a FITS file may be downloaded from [GraceDB](https://gracedb.ligo.org/superevents/public/O3/)

In the following example, we will use the FITS files corresponding to the Open Public Alert [S190421ar](https://gracedb.ligo.org/superevents/S190421ar/view/). 

To apply GWSkyNet to S190421ar, perform the following:
```
import GWSkyNet.GWSkyNet as G
model       = G.load_GWSkyNet_model()
data        = G.prepare_data('S190421ar.fits')
class_score = G.predict(model, data)
FAR, FNR    = G.get_rates(class_score[0])
```
Running the above code will output a class score equal to 0.995. A class_score closer to 1 indicates the origin is more likely to be astrophysical.
FAR and FNR stand for False Alarm Rate and False Negative Rate respectively.

### Architecture    
GWSkyNet architecture. The first two branches are convolutional neural networks with residual connections for image data. The shape of the input data is indicated in parenthesis, with N the number of examples in the training set. The numbers in the SeparableConv2D (SepConv) and MaxPool layers indicate the kernel size in pixels and the number of filters (when applicable). The number in the Dense layers indicates the number of units.    
![](figs/CNN_architecture.png)    
### Performance    
False Positive Rate (FPR) and False Negative Rate (FNR) as functions of the Real-Noise (RN) score threshold. At a score threshold RN>=0.5, GWSkyNet yields 5.3% FNR and 3.8% FPR. Lowering the threshold to RN>=0.1 reduces the FNR to 2.4%, with FPR increased to 9.3%. The intersection is at RN=0.39, with FPR=FNR=4.5%.    
![](figs/FNR-FPRvsthreshold.png)

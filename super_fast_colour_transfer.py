import cv2
import numpy as np
import argparse


# Finding necessary parameters
def img_stats(image):
    (l,a,b)=cv2.split(image)
    (lMean, lStd) = (l.mean(), l.std())
    (aMean, aStd) = (a.mean(), a.std())
    (bMean, bStd) = (b.mean(), b.std())
    return (lMean, lStd, aMean, aStd, bMean, bStd)


# applying colour-transfer algorithm
def colour_transfer(source,target):
    source=cv2.cvtColor(source,cv2.COLOR_BGR2LAB).astype("float32")
    target=cv2.cvtColor(target,cv2.COLOR_BGR2LAB).astype("float32")
    (lMeanSrc, lStdSrc, aMeanSrc, aStdSrc, bMeanSrc, bStdSrc) = img_stats(source)
    (lMeanTar, lStdTar, aMeanTar, aStdTar, bMeanTar, bStdTar) = img_stats(target)
    (l, a, b) = cv2.split(target)
    l=((l-lMeanTar)*(lStdTar / lStdSrc)) + lMeanSrc
    a=((a-aMeanTar)*(aStdTar / aStdSrc)) + aMeanSrc
    b=((b-bMeanTar)*(bStdTar / bStdSrc)) + bMeanSrc
    l = np.clip(l, 0, 255)
    a = np.clip(a, 0, 255)
    b = np.clip(b, 0, 255)
    output = cv2.merge([l, a, b])
    output = cv2.cvtColor(output.astype("uint8"), cv2.COLOR_LAB2BGR)
    return output


if __name__=='__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("source", required=True, help="path to source image whose effect has to be applied")
    ap.add_argument("target", required=True, help="path to target image upon which the effect has to be applied")
    ap.add_argument("output", required=True, help="path to output image")
    args = vars(ap.parse_args())
    source = cv2.imread(args.source)
    target = cv2.imread(args.target)
    output=colour_transfer(source,target)
    cv2.imwrite(args.output, output)
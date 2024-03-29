---
title: "Accurate Image Alignment and Registration using OpenCV"
date: 2022-03-08T21:00:00+01:00
location: "Belgium"
---

![](/image/las_meninas_input.jpg)

The image alignment and registration pipeline takes two input images that contain the same scene from slightly different viewing angles. The picture above displays both input images side by side with the common scene (object) being the painting *[Las Meninas](https://www.museodelprado.es/en/the-collection/art-work/las-meninas/9fdc7800-9ade-48b0-ab8b-edee94ea877f)* (1656) by Velázquez, currently at the [Museo del Prado](https://www.museodelprado.es/en) in Madrid (Spain).

The first step is computing the projection that establishes the mathematical relationships which maps pixel coordinates from one image to another [^1]. The most general planar 2D transformation is the eight-parameter perspective transform or homography denoted by a general $ 3×3 $ matrix $ \mathbf{H} $. It operates on 2D homogeneous coordinate vectors, $\mathbf{x'} = (x',y',1)$ and $\mathbf{x} = (x,y,1)$, as follows:

$$ \mathbf{x'} \sim \mathbf{Hx} $$

Afterwards, we take the homographic matrix and use it to warp the perspective of one of the images over the other, aligning the images together. With task clearly defined and the pipeline introduced, the next sections describe how this can be archieved using OpenCV.

## Feature Detection

To compute the perspective transform matrix $ \mathbf{H} $, we need the link both input images and assess which regions are the same. We could manually select the corners of each painting and use that to compute the homography, however this method has several problems: the corners of a painting could be occluded in one of the scenes, not all scenes are rectangular paintings so this would not be suitable for those cases, and it would require manual work per scene, which is not ideal if want to process numerous scenes in an automatic manner.

Therefore, a feature detection and matching process is used to link common regions in both images. The only limitation of this technique is that the scene must include *enough* features evenly distributed. The used method here was ORB [^2], but other feature extraction methods are also available --- the code of the class <code>FeatureExtraction</code> is presented at the end of the post for brevity.

<pre>
img0 = cv.imread("lasmeninas0.jpg", cv.COLOR_BGR2RGBA)
img1 = cv.imread("lasmeninas1.jpg", cv.COLOR_BGR2RGBA)
features0 = FeatureExtraction(img0)
features1 = FeatureExtraction(img1)
</pre>

![](/image/las_meninas_features.jpg)

## Feature Matching

The aforementioned class computed the keypoints (position of a feature) and descriptors (*description* of said feature) for both images, so now we have to pair them up and remove the outliers. Firstly, FLANN (Fast Library for Approximate Nearest Neighbors) computes the pairs of matching features whilst taking into account the nearest neighbours of each feature. Secondly, the best features are selected using the Lowe's ratio of distances test, which aims to eliminate false matches from the previous phase [^3]. The code is presented below, and the full function at the end. Right after the code, the picture presents both input images side by side with the matching pairs of features.

<pre>
matches = feature_matching(features0, features1)
matched_image = cv.drawMatches(img0, features0.kps, \
    img1, features1.kps, matches, None, flags=2)
</pre>

![](/image/las_meninas_matched.jpg)

## Homography Computation

After computing the pairs of matching features of the input images, it is possible to compute the homography matrix. It takes as input the matching points on each image and using [RANSAC](https://en.wikipedia.org/wiki/Random_sample_consensus) (random sample consensus) we are able to efficiently compute the projective matrix. Although the feature pairs were already filtered in the previous phase, they are filtered again so that only the inliers are used to compute the homography. This removes the outliers from the calculation, which leads to a minimization of the error associated with the homography computation.

<pre>
H, _ = cv.findHomography( features0.matched_pts, \
    features1.matched_pts, cv.RANSAC, 5.0)
</pre>

This function gives as output the following $ 3×3 $ matrix (for our input):

$$
\mathbf{H} =
\begin{bmatrix}
+7.85225708\text{e-}01 & -1.28373989\text{e-}02 & +4.06705815\text{e}02 \cr
-4.21741196\text{e-}03 & +7.76450089\text{e-}01 & +8.15665534\text{e}01 \cr
-1.20903215\text{e-}06 & -2.34464498\text{e-}05 & +1.00000000\text{e}00 \cr
\end{bmatrix} 
$$

## Perspective Warping & Overlay

Now that we have computed the transformation matrix that establishes the mathematical relationships which maps pixel coordinates from one image to another, we can do the image registration process. This process will do a perspective warp of one of the input images so that it overlaps on the other one. The outside of the warped image is filled with transparency, which then allows us to [overlay](https://stackoverflow.com/questions/41508458/python-opencv-overlay-an-image-with-transparency) that over the other image and verify its correct alignment.

<pre>
h, w, c = img1.shape
warped = cv.warpPerspective(img0, H, (w, h), \
    borderMode=cv.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))
output = np.zeros((h, w, 3), np.uint8)
alpha = warped[:, :, 3] / 255.0
output[:, :, 0] = (1. - alpha) * img1[:, :, 0] + alpha * warped[:, :, 0]
output[:, :, 1] = (1. - alpha) * img1[:, :, 1] + alpha * warped[:, :, 1]
output[:, :, 2] = (1. - alpha) * img1[:, :, 2] + alpha * warped[:, :, 2]
</pre>

<div id="overlay">
  <figure>
    <div id="compare"></div>
  </figure>
  <input oninput="beforeAfter()" onchange="beforeAfter()" type="range" min="0" max="1000" value="500" id="slider"/>
</div>

<details>
<summary>main.py</summary>

<pre>
import cv2 as cv
import numpy as np
from aux import FeatureExtraction, feature_matching


img0 = cv.imread("lasmeninas0.jpg", cv.COLOR_BGR2RGBA)
img1 = cv.imread("lasmeninas1.jpg", cv.COLOR_BGR2RGBA)
features0 = FeatureExtraction(img0)
features1 = FeatureExtraction(img1)

matches = feature_matching(features0, features1)
# matched_image = cv.drawMatches(img0, features0.kps, \
#     img1, features1.kps, matches, None, flags=2)

H, _ = cv.findHomography( features0.matched_pts, \
    features1.matched_pts, cv.RANSAC, 5.0)

h, w, c = img1.shape
warped = cv.warpPerspective(img0, H, (w, h), \
    borderMode=cv.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))

output = np.zeros((h, w, 3), np.uint8)
alpha = warped[:, :, 3] / 255.0
output[:, :, 0] = (1. - alpha) * img1[:, :, 0] + alpha * warped[:, :, 0]
output[:, :, 1] = (1. - alpha) * img1[:, :, 1] + alpha * warped[:, :, 1]
output[:, :, 2] = (1. - alpha) * img1[:, :, 2] + alpha * warped[:, :, 2]
</pre>
</details>

<details>
<summary>aux.py</summary>

<pre>
import cv2 as cv
import numpy as np
import copy


orb = cv.ORB_create(
    nfeatures=10000,
    scaleFactor=1.2,
    scoreType=cv.ORB_HARRIS_SCORE)

class FeatureExtraction:
    def __init__(self, img):
        self.img = copy.copy(img)
        self.gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        self.kps, self.des = orb.detectAndCompute( \
            self.gray_img, None)
        self.img_kps = cv.drawKeypoints( \
            self.img, self.kps, 0, \
            flags=cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        self.matched_pts = []


LOWES_RATIO = 0.7
MIN_MATCHES = 50
index_params = dict(
    algorithm = 6, # FLANN_INDEX_LSH
    table_number = 6,
    key_size = 10,
    multi_probe_level = 2)
search_params = dict(checks=50)
flann = cv.FlannBasedMatcher(
    index_params,
    search_params)

def feature_matching(features0, features1):
    matches = [] # good matches as per Lowe's ratio test
    if(features0.des is not None and len(features0.des) > 2):
        all_matches = flann.knnMatch( \
            features0.des, features1.des, k=2)
        try:
            for m,n in all_matches:
                if m.distance < LOWES_RATIO * n.distance:
                    matches.append(m)
        except ValueError:
            pass
        if(len(matches) > MIN_MATCHES):    
            features0.matched_pts = np.float32( \
                [ features0.kps[m.queryIdx].pt for m in matches ] \ 
                ).reshape(-1,1,2)
            features1.matched_pts = np.float32( \
                [ features1.kps[m.trainIdx].pt for m in matches ] \
                ).reshape(-1,1,2)
    return matches
</pre>
</details>

<details>
<summary>requirements.txt</summary>

<pre>
opencv-python==4.2.0.34
numpy==1.19.2
</pre>
</details>

[^1]: Szeliski R. (2006) Image Alignment and Stitching. In: Paragios N., Chen Y., Faugeras O. (eds) Handbook of Mathematical Models in Computer Vision. Springer, Boston, MA. [https://doi.org/10.1007/0-387-28831-7_17](https://doi.org/10.1007/0-387-28831-7_17).

[^2]: Rublee, E., Rabaud, V., Konolige, K., & Bradski, G. (2011, November). ORB: An efficient alternative to SIFT or SURF. In 2011 International conference on computer vision (pp. 2564-2571). Ieee. [http://doi.org/10.1109/ICCV.2011.6126544](http://doi.org/10.1109/ICCV.2011.6126544)

[^3]: Lowe, D. G. (2004). Distinctive image features from scale-invariant keypoints. International journal of computer vision, 60(2), 91-110. [https://doi.org/10.1023/B:VISI.0000029664.99615.94](https://doi.org/10.1023/B:VISI.0000029664.99615.94)


<style>
#overlay { 
    aspect-ratio: 1200 / 900; 
    overflow: hidden;
    width: 100%;
    margin-bottom: 16px;
}
#overlay figure { 
    background-image: url(/image/las_meninas_after.jpg);
    background-size: cover;
    font-size: 0;
    height: 100%;
    margin: 0; 
    position: relative;
    width: 100%; 
}
#compare {
    background-image: url(/image/las_meninas_before.jpg);
    background-size: cover;
    bottom: 0;
    border-right: 5px solid rgba(255,255,255,0.7);
    box-shadow: 10px 0 15px -13px #000;
    height: 100%;
    max-width: 98.6%;
    min-width: 0.6%;
    overflow: visible;
    position: absolute;
    width: 50%; 
}
.animate{
    animation: first 2s 1 normal ease-in-out 0.1s; 
    -webkit-animation: first 2s 1 normal ease-in-out 0.1s;
}
input#slider {
    -moz-appearance: none;
    -webkit-appearance: none;
    border: none; 
    background: transparent;
    cursor: col-resize;
    height: 100vw;
    left: 0;
    margin: 0;
    outline: none; 
    padding: 0;
    position: relative;
    top: -100vw;
    width: 100%;
}
input#slider::-moz-range-track { 
    background: transparent; 
}
input#slider::-ms-track {
    border: none; 
    background-color: transparent;
    height: 100vw; 
    left: 0; 
    outline: none; 
    position: relative;
    top: -100vw; 
    width: 100%;
    margin: 0;
    padding: 0;
    cursor: col-resize;
    color:transparent;
}
input#slider::-ms-fill-lower {
    background-color:transparent;
}
input#slider::-webkit-slider-thumb {
    -webkit-appearance:none;
    height: 100vw;
    width: 0.5%;
    opacity: 0;
}
input#slider::-moz-range-thumb {
    -moz-appearance: none;
    height: 100vw;
    width: 0.5%;
    opacity: 0;
}
input#slider::-ms-thumb {
    height: 100vw;
    width: 0.5%; 
    opacity:0;
}
input#slider::-ms-tooltip {
    display:none;
}
#compare::before {
    background: url(/image/comparison-toggle.png) no-repeat scroll 0 center transparent;
    background-size:contain;
    content: " ";
    float: right;
    height: 100%;
    margin-right: -18px;
    position: relative;
    top:0;
    width: 32px;
}
@keyframes first {
    0% {width: 50%; }
    25% {width: 20%; }
    75% {width: 80%; }
    100% {width: 50%; }
}
@-webkit-keyframes first {
    0% {width: 50%; }
    25% {width: 20%; }
    75% {width: 80%; }
    100% {width: 50%; }
}
</style>

<script>
// before-after image comparison
function beforeAfter() {
    document.getElementById("compare").style.width = document.getElementById("slider").value / 10 + "%";
}

setInterval(() => {
    if(document.getElementById("slider").value == 500) {
        document.getElementById("compare").classList.toggle("animate");
    }
}, 4000);
</script>

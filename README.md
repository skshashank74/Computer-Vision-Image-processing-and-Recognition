# Assignment 1 : Image processing and Recognition Basics

## Injecting the correct answer

To inject the correct answer in the image we created a pattern in the blank space between the instruction and the multiple choice questions. We started injecting the pattern from pixel index (row = 350, column = 5). As there are 85 question we stored the pattern along the width of image and options (‘A’, ‘B’, ‘ C’, ‘D’, ‘E’) along the columns. We created a black box of size (10,10) which darkens the pixel based on which option is correct. If option ‘A’ of first question is correct then it darken the 10,10 pixel from (350,5) to (360,15) else it goes down by 10 pixel to check if option B is correct and it keeps going down until option ‘E’ is reached. We used a spacing of 10 pixel between each options and the question so that if the image have rotation it can handle still some cases. But if the angle of rotation increases the extraction.py code will fail. The idea behind using a pixel box of (10,10 ) is to make it robust of the noise being added while scanning.

We tried other approaches to inject the correct answers. In one of the approach, we tried to  embed the Unicode code of the correct option in RGB values. We first stored the numbers of the correct answers in  R of RGB and then iterated storing the correct answer for each questions corresponding to where we marked the number of correct answer. However, we realised we don’t need to make the marking invisible and this approach would not be robust in many ways.

To run injection code we need to use below command. 'form.jpg' is the blank form, 'answers.txt' is the txt file for correct answers and injected.jpg is the output file

```
python3 inject.py form.jpg answers.txt injected.jpg
```
```
python3 inject.py test-images/a-3.jpg test-images/a-3_groundtruth.txt injected1.jpg
```

## Extracting the correct answers

After injecting we need to extract the answer from injected.jpg file. When we save the file in jpg usually there some noise added in pixel value and the pixel do not remain exactly the same. The extraction.py code is just reverse of injection.py code. Few design decision we made here, were we start with (row = 350, column = 5) pixel for the first question and iterate for each option in the similar way we did it in injection. We take the sum of (10,10) pixel, if the sum of pixel values are less than 3000 we label that option as the correct answer. We kept threshold of 3000 so that the code is robust of the noise being added in the image. 

However, if the injected.jpg image has a rotation greater than 1 degree then our code will fail to extract the correct answers. To correct the orientation we though of getting angle from hough transform and then aligning the image. Also, we thought of adding a marker so that we know were to start for pulling the answers. As of know we are hard coding it to (350,5). As our hough transform code ran fine very late we couldn't try this approach.

To run extraction code we need to use below command. 'form.jpg' is the blank form, 'answers.txt' is the txt file for correct answers and injected.jpg is the output file

```
python3 extract.py injected.jpg output.txt
```

## Extracting the answers from the OMR sheet

Extracting the answer from OMR sheet can be divided into 2 parts:
1. Getting the coordinates of intersection of vertical and horizontal line of the first question
2. Extracting the option marked


### Getting the horizontal and vertical lines (cordinates of the first question)  
Vertical lines           |  Horizontal lines
:-------------------------:|:-------------------------:
![Retrieved Vertical Lines](https://github.com/skshashank74/Computer-Vision-Image-processing-and-Recognition/blob/main/genp8.png)  |  ![Retrieved Horizontal Lines](https://github.com/skshashank74/Computer-Vision-Image-processing-and-Recognition/blob/main/genp9.png)
 


We first divided the image into three patches. (Q 1-29 first patch, Q 30-58 second patch, Q 59-85 third patch). After getting the patches, we are calculating the pixel intensity of each columns and rows. We sort the pixel intensity of both rows and columns and take first 80 highest intensity value for rows and 50 highest intensity value for columns. When we draw the lines we notice that the horizontal and vertical lines are passing through the box edges but their are lines which are passing from between the boxes too. To exclude those lines, we made a condition that any vertical lines should have a minimum distance of 25 pixel and any horizatal lines should have distance of minimum 12 pixel. We then extract the coordinates of the very first box by looking for the intersection of the very first horiziontal and vertical line within our set parameters i.e past the question number.  

### Extracting the option marked

Using the coordinates retrievd we then iterate from left to write and decide whether a particular pixel is marked based on the pixel intensity. We also check if the student had written outside the box accordingly by checking pixels on the left of the question number and mark it with an 'x' accordingly. We then perform the same operations on all questions in that patch by moving from top to bottom. We then append all the answers retrieved and save it in the form of a text file whose name is specified by the user.

To run grading code we need to use below command. 'marked.jpg' is the makrked OMR sheet, 'output.txt' would be name of the file containing the answers retrieved from the bubbled OMR.

```
python3 grade.py marked.jpg output.txt
```

a-27 accuracy           |  a-3 accuracy
:-------------------------:|:-------------------------:
![a-27 accuracy](https://github.com/skshashank74/Computer-Vision-Image-processing-and-Recognition/blob/main/a-27_accuracy.jpg)  |  ![a-3 accuracy](https://github.com/skshashank74/Computer-Vision-Image-processing-and-Recognition/blob/main/a_3_accuracy.jpg)

### Alternate approach

#### Hough Transform to detect the horizontal and vertical lines

Our initial approach was to detect the answer box's vertical and horizontal lines and in turn get the intersection points of those lines through **Hough transformation**.

With this approach, the edges detected in the input image is transformed into parameter space to find the rho (perpendicular distance from origin to the line) and theta (the angle between the rho and the X-axis). Our design approach for the line detection is as follows-

1. Split the input image into 3 patches containing the answer columns. This approach was taken to
2. Apply Gaussian filter to remove any noise. Optional filter is to apply erode and dilate filter to remove noise.
3. Apply edge detection on the image to retrieve the edges for Hough transform. Threshold the edge image to 0 (pixel value < 125) and 255 (pixel value >125). This is to reduce the Hough transform operation on less important pixels and speed up detection.
4. Since the line of interest are the horizontal and vertical lines of the boxes (with +/- 5 degree permissible), theta angles -90 degrees, 0 degrees, 90 degrees are considered. This sped up the line detection.
5. Horizontal and vertical lines with votes greater than threshold (based on experiments) are considered for the image.

With detected horizontal and vertical lines, intersection of the boxes are found.


### TODO

1. With Hough transform, the angle of rotation is for rotated image is calculated. This shall be applied on the input image to correct the rotation.

### References

1. https://docs.opencv.org/3.4/d6/d10/tutorial_py_houghlines.html
2. 
3. https://towardsdatascience.com/lines-detection-with-hough-transform-84020b3b1549
4. 
Above are the accuracies reported for OMR sheets a-27.jpg and a-3.jpg based on the given ground truths.

Discussed the approach wth: Ujwala Musku, Rupesh Deshmukh, Harshith Khandelwal

Contribution:

We all three were involved in formulating the approach of injecting the answer, extracting the answer embedded in the image and getting the marked answers of students.

Injection (code, report) – Shashank Kumar  
Extraction (code, report) - Shashank Kumar  
Getting the horizontal and vertical line (code, report) - Shashank Kumar, Sai Giridhar Rao Allada  
Extracting the marked answers of the student (code, report)- Sai Giridhar Rao Allada  
Extracting 'X' (code, report) - Sai Giridhar Rao Allada  
Hough Transform - Shashank Holla  





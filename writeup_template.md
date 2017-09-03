## Project: Search and Sample Return

---


**The goals / steps of this project are the following:**  

**Training / Calibration**  

* Download the simulator and take data in "Training Mode"
* Test out the functions in the Jupyter Notebook provided
* Add functions to detect obstacles and samples of interest (golden rocks)
* Fill in the `process_image()` function with the appropriate image processing steps (perspective transform, color threshold etc.) to get from raw images to a map.  The `output_image` you create in this step should demonstrate that your mapping pipeline works.
* Use `moviepy` to process the images in your saved dataset with the `process_image()` function.  Include the video you produce as part of your submission.

**Autonomous Navigation / Mapping**

* Fill in the `perception_step()` function within the `perception.py` script with the appropriate image processing functions to create a map and update `Rover()` data (similar to what you did with `process_image()` in the notebook). 
* Fill in the `decision_step()` function within the `decision.py` script with conditional statements that take into consideration the outputs of the `perception_step()` in deciding how to issue throttle, brake and steering commands. 
* Iterate on your perception and decision function until your rover does a reasonable (need to define metric) job of navigating and mapping.  

[//]: # (Image References)

[image1]: ./misc/rover_image.jpg
[image2]: ./calibration_images/example_grid1.jpg
[image3]: ./calibration_images/example_rock1.jpg 

## [Rubric](https://review.udacity.com/#!/rubrics/916/view) Points
### Here I will consider the rubric points individually and describe how I addressed each point in my implementation.  

---

### Notebook Analysis
#### 1. Run the functions provided in the notebook on test images. Add/modify functions to allow for color selection of obstacles and rock samples.
Here is an example image.

![alt text][image1]

#### 1. Populate the `process_image()` function with the appropriate analysis steps to map pixels identifying navigable terrain, obstacles and rock samples into a worldmap.  Run `process_image()` on your test data using the `moviepy` functions provided to create video output of your result. 
And another! 

![alt text][image2]
### Autonomous Navigation and Mapping

#### 1. Fill in the `perception_step()` (at the bottom of the `perception.py` script) and `decision_step()` (in `decision.py`) functions in the autonomous mapping scripts and an explanation is provided in the writeup of how and why these functions were modified as they were.

##### 'perception step()

At fisrt, I defined the source points and the destination points and apply perspective transform to the picture from the Mover's front camera. Second, I appilied color threshhold to identify navigable terrain/obstacles/rock samples. Also, I changed correspoding pixel color to display the area Rover found on the left side screen of simulator.
 
Next, I converted map image pixel values to rover-centric coordinates for both navigable terrain and obstacles. Then I converted it to world coordinates, and update Rover's world map.

Next, I converted rover-centric pixel positions to polar coordinates in order to manipulate Rover's steering.
Separterly I did the same conversion to the rock pixels when Rover find some rocks.    

##### 'descision_step()

Af first, I checked whether there is the navigable terrain with threshhold. If exits, Rover is set as 'forward' mmode. In 'forward' mode, throttle is on if the velocity does not reach the Max limit. Angle is decided to the minimum candidate based on the detection of obstacles (when detecting, the angle is removed from the candidate). This is because I wanted to make Rover run along with the wall counter-clockwise.

Otherwise set as 'stop' mode, and make Rover rotate to find the navigable angles. 


If the rock is close to the Rover, Rover is set as 'pick' mode, then try to stop near by the rock. if near_sample attribute is 1, Rover picks up the rock, then move to 'forward' mode again.

Also, in case that Rover cannot move by any mode, I made a check the position of Rover, and if find it is not changed, Rover try to rotate and throttle in order to move.


#### 2. Launching in autonomous mode your rover can navigate and map autonomously.  Explain your results and how you might improve them in your writeup.  

***Note: running the simulator with 1,024 x 768 with "Good" as a choices of resolution and graphics quality. FPS output is set  to 48 by (`drive_rover.py`).**

When I tried, the results was as follows.




![alt text][image3]



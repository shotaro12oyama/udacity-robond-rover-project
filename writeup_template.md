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

Next, I converted rover-centric pixel positions to polar coordinates
separterly I  when Rover see if we can find some rocks
    

##### 'descision_step()


# Check if we have vision data to make decisions with
    if Rover.nav_angles is not None:
        # Check for Rover.mode status
        if Rover.mode == 'forward': 
            # Check the extent of navigable terrain
            if len(Rover.nav_angles) >= Rover.stop_forward:  
                # If mode is forward, navigable terrain looks good 
                # and velocity is below max, then throttle 
                if Rover.vel < Rover.max_vel:
                    # Set throttle value to throttle setting
                    Rover.throttle = Rover.throttle_set
                else: # Else coast
                    Rover.throttle = 0
                Rover.brake = 0                     
                # Decision is made based on the distance and existance of obstacles
                obs_angles = np.array(Rover.obs_angles)
                obs_angles = obs_angles [ np.where(Rover.obs_dists < 40) ]
                obs_angles = obs_angles * 180/np.pi
                #separate to steer angle range candidate and check each
                steer_candidate = [0, 5, 10, 15]
                if obs_angles[(obs_angles > -2.5) & (obs_angles < 2.5)].any():
                    steer_candidate.remove(0)
                if obs_angles[(obs_angles > 2.5) & (obs_angles < 7.5)].any():
                    steer_candidate.remove(5)
                if obs_angles[(obs_angles > 7.5) & (obs_angles < 12.5)].any():
                    steer_candidate.remove(10)
                if obs_angles[(obs_angles > 12.5) & (obs_angles < 17.5)].any():
                    steer_candidate.remove(15)
                #select the minimum available steer angle
                if len(steer_candidate) > 0:
                    Rover.steer = np.min(steer_candidate)
                if not obs_angles[(obs_angles > -17.5) & (obs_angles < -2.5)].any():
                    Rover.steer = -15
                #to move 'pick' mode when finding rocks
                if Rover.rock_angles is not None:
                    rock_angles = np.array(Rover.rock_angles)
                    rock_angles = rock_angles [ np.where(Rover.rock_dist < 50) ]
                    if len(rock_angles) > 0:
                        Rover.steer = np.clip(np.mean(rock_angles *180/np.pi), -15, 15)
                        Rover.mode = 'pick'

            # If there's a lack of navigable terrain pixels then go to 'stop' mode
            elif len(Rover.nav_angles) < Rover.stop_forward:
                    # Set mode to "stop" and hit the brakes!
                    Rover.throttle = 0
                    # Set brake to stored brake value
                    Rover.brake = 0
                    Rover.steer = 15
                    Rover.mode = 'stop'
                    

        # If we're already in "stop" mode then make different decisions
        elif Rover.mode == 'stop':
            # If we're in stop mode but still moving keep braking
            if Rover.vel > 0.2:
                Rover.throttle = 0
                Rover.brake = Rover.brake_set
                Rover.steer = 0
            # If we're not moving (vel < 0.2) then do something else
            elif Rover.vel <= 0.2:
                # Now we're stopped and we have vision data to see if there's a path forward
                if len(Rover.nav_angles) < Rover.go_forward:
                    Rover.throttle = 0
                    # Release the brake to allow turning
                    Rover.brake = 0
                    # Turn range is +/- 15 degrees, when stopped the next line will induce 4-wheel turning
                    Rover.steer = 15 # Could be more clever here about which way to turn
                # If we're stopped but see sufficient navigable terrain in front then go!
                if len(Rover.nav_angles) >= Rover.go_forward:
                    # Set throttle back to stored value
                    Rover.throttle = Rover.throttle_set
                    # Release the brake
                    Rover.brake = 0
                    # Set steer to mean angle
                    Rover.steer = 15
                    Rover.mode = 'forward'


    # Just to make the rover do something 
    # even if no modifications have been made to the code
        elif Rover.mode =='pick':
            rock_angles = np.array(Rover.rock_angles)
            # to pick up when prepared
            if Rover.near_sample == 1:
                Rover.steer = 0
                Rover.brake = Rover.brake_set
                Rover.samples_collected +=1
                Rover.rock_dist = None
                Rover.rock_angles = None
            # speed down when being close to the rock
            elif Rover.rock_dist[(Rover.rock_dist < 10)].any():
                Rover.throttle = 0
                Rover.steer = np.clip(np.mean(rock_angles * 180/np.pi), -15, 15)
                Rover.brake = Rover.brake_set
            # to come down to the rock
            else: 
                Rover.throttle = Rover.throttle_set
                Rover.steer = np.clip(np.mean(rock_angles * 180/np.pi), -15, 15)
                Rover.brake = 0
            # to move back to 'forward' mode
            if Rover.rock_dist is None:
                Rover.mode ='forward'

    else:
        Rover.throttle = Rover.throttle_set
        Rover.steer = 0
        Rover.brake = 0

    # when rover cannot move by any mode
    if Rover.pos_prev is not None:
        if Rover.near_sample == 1:
            Rover.steer = 0

        elif  np.round(Rover.pos[0],3) == np.round(Rover.pos_prev[0],3) and np.round(Rover.pos[1],3) == np.round(Rover.pos_prev[1],3):
            Rover.pos_count += 1
            Rover.throttle = 0
            Rover.brake = 0
            Rover.steer = 15

            if Rover.pos_count % 3 == 0:
                Rover.throttle = Rover.throttle_set 



    # If in a state where want to pickup a rock send pickup command
    if Rover.near_sample and Rover.vel == 0 and not Rover.picking_up:
        Rover.send_pickup = True
    
    Rover.pos_prev = Rover.pos
    
    return Rover






#### 2. Launching in autonomous mode your rover can navigate and map autonomously.  Explain your results and how you might improve them in your writeup.  

***Note: running the simulator with 1,024 x 768 with "Good" as a choices of resolution and graphics quality. FPS output is set  to 48 by (`drive_rover.py`).**

Here I'll talk about the approach I took, what techniques I used, what worked and why, where the pipeline might fail and how I might improve it if I were going to pursue this project further.  



![alt text][image3]



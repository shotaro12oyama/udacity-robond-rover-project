import numpy as np
import random

# This is where you can build a decision tree for determining throttle, brake and steer 
# commands based on the output of the perception_step() function
def decision_step(Rover):

    # Implement conditionals to decide what to do given perception data
    # Here you're all set up with some basic functionality but you'll need to
    # improve on this decision tree to do a good job of navigating autonomously!

    # Example:
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
                # Set steering to average angle clipped to the range 15
                # Decision is made based on close environment
                obs_angles = np.array(Rover.obs_angles)
                obs_angles = obs_angles [ np.where(Rover.obs_dists < 40) ]
                obs_angles = obs_angles * 180/np.pi
                #print('angle_candidates=', obs_angles)
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
                                
                if len(steer_candidate) > 0:
                    Rover.steer = np.min(steer_candidate)
                if not obs_angles[(obs_angles > -17.5) & (obs_angles < -2.5)].any():
                    Rover.steer = -15
                
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

            if Rover.pos_prev is not None:
                if  np.round(Rover.pos[0],3) == np.round(Rover.pos_prev[0],3) and np.round(Rover.pos[1],3) == np.round(Rover.pos_prev[1],3):
                    Rover.pos_count += 1
                    Rover.throttle = 0
                    Rover.brake = 0
                    Rover.steer = 15

                    if Rover.pos_count % 3 == 0:
                        Rover.throttle = Rover.throttle_set 
                    

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

            if not Rover.rock_dist[(Rover.rock_dist < 50)].any():
                Rover.mode ='forward'

            if Rover.near_sample == 1:
                Rover.steer = 0
                Rover.brake = Rover.brake_set
                Rover.samples_collected +=1
                Rover.mode = 'forward'

            else: 
                Rover.throttle = Rover.throttle_set
                Rover.steer = np.clip(np.mean(rock_angles * 180/np.pi), -15, 15)
                Rover.brake = 0
                Rover.mode ='pick'
            

            if Rover.rock_dist[(Rover.rock_dist < 10)].any():
                Rover.throttle = 0
                Rover.steer = np.clip(np.mean(rock_angles * 180/np.pi), -15, 15)
                Rover.brake = Rover.brake_set
                Rover.mode = 'pick'




    else:
        Rover.throttle = Rover.throttle_set
        Rover.steer = 0
        Rover.brake = 0


    # If in a state where want to pickup a rock send pickup command
    if Rover.near_sample and Rover.vel == 0 and not Rover.picking_up:
        Rover.send_pickup = True
    
    Rover.pos_prev = Rover.pos
    
    return Rover


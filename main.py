
# AERE 361 Final Project
# Kyle Younge

"""Monitor customisable temperature and humidity ranges, with an optional audible alarm tone."""
import time
from adafruit_clue import clue
import time
import adafruit_seesaw
import board
from adafruit_neokey.neokey1x4 import NeoKey1x4

# use default I2C bus
i2c_bus = board.I2C()

# Create a NeoKey object
neokey = NeoKey1x4(i2c_bus, addr=0x31)

alarm_enable = False
border_width = 1
clue_display = clue.simple_text_display(title='Score Tracker', title_scale=5,text_scale=1,colors=(clue.WHITE,))
clue_display = clue.simple_text_display(text_scale=3, colors=(clue.WHITE,))
current_time = time.monotonic()
home_score = 0
visitor_score = 0
shotclock_reset = 0
page = "clock setup"
clock_set = 20
clock_remaining = 20 * 60
shotclock_set = 20
shotclock_remaining = 20
period = "Q1"
clock_run = False
while True:
    current_time = time.monotonic()
    
    ##################################################################### Scoreboard Setup #######################################################################################
    ### Clock Set
    while page == "clock setup":
        clue_display = clue.simple_text_display(title='   Scoring Setup', title_scale=1,text_scale=2,colors=(clue.WHITE,))

        clock_set_mapping = {20: 25, 25: 30, 30: 0.1, 0.1: 20}

        if clue.button_a:
            clock_set = clock_set_mapping.get(clock_set, clock_set)
            clock_remaining = 60 * clock_set
            time.sleep(0.1)

        if clue.button_b:
            page = "shotclock setup"
            time.sleep(0.1)

        clue_display[1].text = "Game Clock: {:.0f} min".format(clock_set)
        clue_display[3].text = "Shotclock: {:.0f} sec".format(shotclock_set)
        clue_display[5].text = "Period: " + str(period)
        clue_display[1].color = clue.GREEN
        clue_display.show()

    ### Shotclock set
    while page == "shotclock setup":
        clue_display = clue.simple_text_display(title='   Scoring Setup', title_scale=1,text_scale=2,colors=(clue.WHITE,))

        shotclock_set_mapping = {20: 25, 25: 30, 30: 35, 35: 20}

        if clue.button_a:
            shotclock_set = shotclock_set_mapping.get(shotclock_set, shotclock_set)
            shotclock_remaining = shotclock_set
            time.sleep(0.1)

        if clue.button_b:
            page = "period setup"
            time.sleep(0.1)

        clue_display[1].text = "Game Clock: {:.0f} min".format(clock_set)
        clue_display[3].text = "Shotclock: {:.0f} sec".format(shotclock_set)
        clue_display[5].text = "Period: " + str(period)
        clue_display[3].color = clue.GREEN
        clue_display.show()

    ### Period set
    while page == "period setup":
        clue_display = clue.simple_text_display(title='   Scoring Setup', title_scale=1,text_scale=2,colors=(clue.WHITE,))

        period_set_mapping = {"Q1": "Q2", "Q2": "Q3", "Q3": "Q4", "Q4": "H1", "H1": "H2", "H2": "Q1"}

        if clue.button_a:
            period = period_set_mapping.get(period, period)
            time.sleep(0.1)

        if clue.button_b:
            page = "scoreboard"
            time.sleep(0.1)

        clue_display[1].text = "Game Clock: {:.0f} min".format(clock_set)
        clue_display[3].text = "Shotclock: {:.0f} sec".format(shotclock_set)
        clue_display[5].text = "Period: " + str(period)
        clue_display[5].color = clue.GREEN
        clue_display.show()

    ### Set Paramenters for Scoreboard

    ##################################################################### Scoreboard Page #######################################################################################

    while page == "scoreboard":
        clue_display = clue.simple_text_display(text_scale=3, colors=(clue.WHITE,))

        # Clock stop state
        while clock_run == False:
            buzzer = False
            current_time = time.monotonic() 

            # Scoring
            if neokey[0]:
                home_score = home_score + 1
                time.sleep(0.1)

            if neokey[1]:
                visitor_score = visitor_score + 1
                time.sleep(0.1) 

            if neokey[2]:
                home_score = home_score - 1
                time.sleep(0.1)

            if neokey[3]:
                visitor_score = visitor_score - 1
                time.sleep(0.1)

            # Reset Shotclock
            if clue.button_a:
                shotclock_remaining = shotclock_set
                time.sleep(0.1)

            # Start Clock
            if clue.button_b:
                clock_run = True
                clock_start = current_time
                shotclock_start = current_time
                time.sleep(0.1)
            
            # Display Computations
            clock_sec = clock_remaining % 60
            clock_min = clock_remaining // 60 

            # Display Format
            clue_display[1].text = "Home     Away"   
            clue_display[2].text = " {:02d}       {:02d}".format(home_score, visitor_score)
            clue_display[3].text = "    {:02d}:{:02d}   ".format(round(clock_min), round(clock_sec))
            clue_display[5].text = "{:02d}         {}".format(round(shotclock_remaining), period)   
        
            clue_display.show()
   
        #Clock running state
        if clock_run == True:
            current_time = time.monotonic()  

            #Clock
            clock_display = clock_remaining - (time.monotonic() - clock_start)
            shotclock_display = shotclock_remaining - (time.monotonic() - shotclock_start)

            #Scoring
            if neokey[0]:
                home_score = home_score + 1
                time.sleep(0.1)

            if neokey[1]:
                visitor_score = visitor_score + 1
                time.sleep(0.1) 

            if neokey[2]:
                home_score = home_score - 1
                time.sleep(0.1)

            if neokey[3]:
                visitor_score = visitor_score - 1
                time.sleep(0.1)
                
            if clue.button_b:
                clock_remaining = clock_display
                shotclock_remaining = shotclock_display
                clock_run = False
                time.sleep(0.1)

            if clue.button_a:
                shotclock_remaining = shotclock_set
                shotclock_start = current_time
                time.sleep(0.1)

            # Shotclock runs out
            if shotclock_display <= 0:
                clock_remaining = clock_display
                shotclock_display = 0
                clue.start_tone(2000)
                time.sleep(0.5)
                clue.stop_tone()
                shotclock_remaining = shotclock_set
                clock_run = False

            #Game clock runs out
            if clock_display <= 0:
                clock_remaining = 0
                clock_display = 0
                clue.start_tone(2000)
                time.sleep(2)
                clue.stop_tone()

                clock_run = False

            # Quarter Periods Display Setup w/ Halftime Display-------------------------------------------------------------------------------- 
                if period.startswith("Q"):                      # Checks Period variable for Q
                    next_quarter = int(period[1]) + 1           # Assigns next Quarter ex: Q1 -> Q2
                    if next_quarter <= 4:                       # Continues until the NEXT quarter is Q4
                        period = "Q" + str(next_quarter)

                        # Reset clock for the next period
                        clock_remaining = clock_set * 60
                        shotclock_remaining = shotclock_set
                        clock_run = False

                        if next_quarter == 3:
                            # Halftime Display   
                            clue_display[1].text = "  HALF TIME "
                            clue_display[2].text = " **\_(^^)_/** "
                            clue_display[4].text = "Home     Away"   
                            clue_display[5].text = " {:02d}       {:02d}".format(home_score, visitor_score)   
                            clue_display.show()
                            time.sleep(5)

                        # Display Format
                        clue_display[1].text = "Home     Away"   
                        clue_display[2].text = " {:02d}       {:02d}".format(home_score, visitor_score)
                        clue_display[3].text = "    {:02d}:{:02d}   ".format(round(clock_min), round(clock_sec))
                        clue_display[5].text = "{:02d}         {}".format(round(shotclock_display), period)        
                        clue_display.show()

                    if next_quarter >= 5:
                        if home_score == visitor_score:
                            period = "OT"
                            # Reset clock for the next period
                            clock_remaining = clock_set * 60
                            shotclock_remaining = shotclock_set
                            clock_run = False

                            # Overtime Display   
                            clue_display[1].text = "  It's a Tie! "
                            clue_display[2].text = "   Overtime "
                            clue_display[4].text = "Home     Away"   
                            clue_display[5].text = " {:02d}       {:02d}".format(home_score, visitor_score)   
                            clue_display.show()
                            time.sleep(5)

                            # Display Computations
                            clock_sec = clock_display % 60
                            clock_min = clock_display // 60 
                            
                            # Display Format
                            clue_display[1].text = "Home     Away"   
                            clue_display[2].text = " {:02d}       {:02d}".format(home_score, visitor_score)
                            clue_display[3].text = "    {:02d}:{:02d}   ".format(round(clock_min), round(clock_sec))
                            clue_display[5].text = "{:02d}         {}".format(round(shotclock_display), period)        
                            clue_display.show()
                        elif home_score > visitor_score:          
                            winner = "Home"
                        else:
                            winner = "Away"


                    # #Game Display for Game Over 
                    #     clue_display[1].text = "Home     Away"   
                    #     clue_display[2].text = " {:02d}       {:02d}".format(home_score, visitor_score)
                    #     clue_display[3].text = "  GAME OVER ".format(round(clock_min), round(clock_sec))
                    #     clue_display[4].text = "  {} Wins  ".format(winner)        
                    #     clue_display.show()
                    #     time.sleep(5)
                    
            # Half Periods Display Setup w/ Halftime Display--------------------------------------------------------------------------------                                  
                elif period.startswith("H"):
                    next_half = int(period[1]) + 1
                    if next_half == 2:
                        period = "H" + str(next_half)
                        # Reset clock for the next period
                        clock_remaining = clock_set * 60
                        shotclock_remaining = shotclock_set
                        clock_run = False
  
                        # Halftime Display   
                        clue_display[1].text = "  HALF TIME "
                        clue_display[2].text = " **\_(^^)_/** "
                        clue_display[4].text = "Home     Away"   
                        clue_display[5].text = " {:02d}       {:02d}".format(home_score, visitor_score)   
                        clue_display.show()
                        time.sleep(5)

                    if next_half == 3:                       # If the game is over
                        if home_score > visitor_score:          # Assigns Winner
                            winner = "Home"
                        else:
                            winner = "Away"

                    #Game Display for Game Over 
                        clue_display[1].text = "Home     Away"   
                        clue_display[2].text = " {:02d}       {:02d}".format(home_score, visitor_score)
                        clue_display[3].text = "  GAME OVER ".format(round(clock_min), round(clock_sec))
                        clue_display[4].text = "  {} Wins  ".format(winner)        
                        clue_display.show()
                        time.sleep(5)
                                     

            
            # Display Computations
            clock_sec = clock_display % 60
            clock_min = clock_display // 60 
            
            # Display Format
            clue_display[1].text = "Home     Away"   
            clue_display[2].text = " {:02d}       {:02d}".format(home_score, visitor_score)
            clue_display[3].text = "    {:02d}:{:02d}   ".format(round(clock_min), round(clock_sec))
            clue_display[5].text = "{:02d}         {}".format(round(shotclock_display), period)        
            clue_display.show()
            

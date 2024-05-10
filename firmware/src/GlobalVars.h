#ifndef GLOBAL_VARS_H
#define GLOBAL_VARS_H

#ifdef DEBUG
#define DEBUG_PRINT(x) Serial.print(x)
#define DEBUG_PRINTLN(x) Serial.println(x)
#else
#define DEBUG_PRINT(x)
#define DEBUG_PRINTLN(x)
#endif

namespace SYSTEM_CONFIG
{
    const byte  PIN_ENABLE_MOTORS   = 2;                 // Pin number to enable motors
    const byte  PIN_DIR_MOTOR_X     = 3;                 // Pin number for Dir in motor X
    const byte  PIN_PULL_MOTOR_X    = 4;                 // Pin number for Pull in motor X
    const byte  PIN_DIR_MOTOR_Y     = 5;                 // Pin number for Dir in motor Y
    const byte  PIN_PULL_MOTOR_Y    = 6;                 // Pin number for Pull in motor Y
    const byte  PIN_X_ENDSTOP       = 9;                 // Pin number for X-axis endstop
    const byte  PIN_Y_ENDSTOP       = 10;                // Pin number for Y-axis endstop
    const byte  PIN_CAM_SHUTTER     = A5;                // Pin number to control camera shutter through optocoupler
    const byte  PIN_CAM_FOCUS       = A4;                // Pin number to control camera focus through optocoupler
    const byte  PIN_FLASH_RESET     = A3;                // Pin number to reset the FlashSequencerBoard      
    const byte  PIN_LED_AUX         = A2;                // Pin number to control the Auxiliar LED  
    const byte  PIN_STATUS_LED      = 11;                // Pin number for status leds  

    const int FOCUS_DELAY           = 750;               // Delay of the focus pulse
    const int SHUTTING_DELAY        = 300;               // Delay of the shutting pulse
    const int RESET_FLASH_DELAY     = 150;               // Delay of the reset pulse
    const int SHUTTING_INTERVAL_DELAY = 400;             // Delay between shuts in the capture loop

    const int SPEED_WHILE_COMING_BACK_TO_HOME = 3000;    // Speed of motors while moving back to home position (negative value implies reverse direction)
    const int SPEED_WHILE_MOVING_IN_SETSPEED = 1500;     // Speed of motors while moving in set speed mode
    const int LED_UPDATE_INTERVAL = 32;                  // Interval in microseconds for updating motor positions (1/4 ms approx.)

    const int MAX_DIST_X            = 950;               // Max distance in X axes
    const int MAX_DIST_Y            = 750;               // Max distance in Y axes

    const int ENDSTOP_LOGIC_MASK_X = 0;                  // 0 -> Normaly Close & 1 -> Normaly Open
    const int ENDSTOP_LOGIC_MASK_Y = 0;                  // 0 -> Normaly Close & 1 -> Normaly Open

    const int DIRECTION_TOWARD_HOME_MASK_X = -1;         // Direction speed mask for motors to go to the mechanical origin in X
    const int DIRECTION_TOWARD_HOME_MASK_Y = -1;         // Direction speed mask for motors to go to the mechanical origin in Y

    const short STATUS_LED_STRIPE_LENGTH = 2;            // Number of WS2812 in the strip



    // MOTION CONFIGURATION


    const int MAX_SPEED = 3000;                        // Max speed in mm/s
    const int ACCELERATION = 800;                      // Acceleration in mm/s^2
    const float STEPS_PER_MM = 80.0;                   // Steps per mm
}



#endif // GLOBAL_VARS_H

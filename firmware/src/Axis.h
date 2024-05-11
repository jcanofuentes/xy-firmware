
#ifndef AXIS_H
#define AXIS_H

#include "AccelStepper.h"

class Axis
{
public:
    Axis(int stepPin, int dirPin, int endStopPin, int maxSpeed, int acceleration, float stepsPerMM) : stepper(AccelStepper::DRIVER, stepPin, dirPin),
                                                                                                      endStopPin(endStopPin),
                                                                                                      stepsPerMM(stepsPerMM)
    {
        pinMode(endStopPin, INPUT_PULLUP);
        stepper.setMaxSpeed(maxSpeed);
        stepper.setAcceleration(acceleration);
        movingToOrigin = false;
    }

    void move(int millimeters)
    {
        if (!movingToOrigin)
        { // Only accept new move commands if not currently seeking origin
            long targetDistance = millimetersToSteps(millimeters);
            stepper.move(targetDistance);
        }
    }

    void goToOrigin()
    {
        movingToOrigin = true;
        stepper.moveTo(-999999); // Move stepper to a large negative position to ensure it hits the limit switch
    }

    void setMaxSpeed(int speed)
    {
        stepper.setMaxSpeed(speed);
    }

    void setAcceleration(int acceleration)
    {
        stepper.setAcceleration(acceleration);
    }

    void update()
    {
        if (movingToOrigin)
        {
            if (digitalRead(endStopPin) == LOW)
            {                                  // Assuming LOW when triggered
                stepper.stop();                // Stop the stepper
                stepper.setCurrentPosition(0); // Reset the stepper position
                movingToOrigin = false;
            }
        }
        stepper.run();
    }

    long currentPositionInMillimeters()
    {
        return stepsToMillimeters(stepper.currentPosition());
    }

    bool isAtOrigin()
    {
        return stepper.currentPosition() == 0;
    }

    void setHomePosition()
    {
        homePosition = stepper.currentPosition();
    }

    void goToHome()
    {
        stepper.moveTo(homePosition);
    }

    void stop()
    {
        stepper.stop();
    }

    void enable()
    {
        stepper.enableOutputs();
    }

private:
    AccelStepper stepper;
    int endStopPin;
    bool movingToOrigin;
    long homePosition;
    float stepsPerMM = 80.0;

    long millimetersToSteps(int mm)
    {
        return static_cast<long>(mm * stepsPerMM); // Convert millimeters to steps
    }

    long stepsToMillimeters(long steps)
    {
        return static_cast<long>(steps / stepsPerMM); // Convert steps back to millimeters
    }
};


#endif // AXIS_H

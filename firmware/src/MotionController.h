#ifndef MOTION_CONTROLLER_H
#define MOTION_CONTROLLER_H

#include <Arduino.h>
#include "IBaseComponent.h"
#include "Axis.h"
#include "GlobalVars.h"

class MotionController : public IBaseComponent
{
public:
    MotionController()
    {
        x = new Axis(PIN_PULL_MOTOR_X, PIN_DIR_MOTOR_X, PIN_X_ENDSTOP, MAX_SPEED, ACCELERATION, STEPS_PER_MM_X);
        y = new Axis(PIN_PULL_MOTOR_Y, PIN_DIR_MOTOR_Y, PIN_Y_ENDSTOP, MAX_SPEED, ACCELERATION, STEPS_PER_MM_Y);
    }
    void notify(const CommandData &data) override
    {
        switch (data.command)
        {
        case 'X':
            x->move(data.value);
            send.ack(); // Send an acknowledgement
            break;
        case 'Y':
            y->move(data.value);
            break;
        default:
            break;
        }
    }

    void moveX(int millimeters)
    {
        x->move(millimeters);
    }
    void update()
    {
        x->update();
        y->update();
    }

private:
    Axis *x;
    Axis *y;
};

#endif // MOTION_CONTROLLER_H
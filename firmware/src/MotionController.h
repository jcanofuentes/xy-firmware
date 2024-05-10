#ifndef MOTION_CONTROLLER_H
#define MOTION_CONTROLLER_H

#include <Arduino.h>
#include "IBaseComponent.h"
#include "Axis.h"
#include "GlobalVars.h"
#include "MessageBus.h"

using namespace SYSTEM_CONFIG;

class MotionController : public IBaseComponent
{
private:
    Axis* x;
    Axis* y;
    MessageBus* messageBus;

public:
    MotionController( MessageBus* bus) : messageBus(bus)
    {
        x = new Axis(PIN_PULL_MOTOR_X, PIN_DIR_MOTOR_X, PIN_X_ENDSTOP, MAX_SPEED, ACCELERATION, STEPS_PER_MM);
        y = new Axis(PIN_PULL_MOTOR_Y, PIN_DIR_MOTOR_Y, PIN_Y_ENDSTOP, MAX_SPEED, ACCELERATION, STEPS_PER_MM);
    }
    void notify(const CommandData &data) override
    {
        switch (data.command)
        {

        // Move the X axis
        case 'X':
            x->move(data.value);
            break;
        // Move the Y axis
        case 'Y':
            y->move(data.value);
            break;
        // Send the current X position
        case 'U':
            short xPosition = x->currentPositionInMillimeters();
            messageBus->sendMessage(CommandData('u', xPosition));
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
};

#endif // MOTION_CONTROLLER_H
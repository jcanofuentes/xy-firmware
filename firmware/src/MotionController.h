#ifndef MOTION_CONTROLLER_H
#define MOTION_CONTROLLER_H

#include <Arduino.h>
#include "IBaseComponent.h"
#include "Axis.h"
#include "GlobalVars.h"
#include "MessageBus.h"

using namespace SYSTEM_CONFIG;

// Enum for the current state of the motion controller
enum MotionControllerState
{
    IDLE,      // Idle state: the motion controller is not doing anything
    TO_ORIGIN, // Going to origin state: the motion controller is going to the origin
};

class MotionController : public IBaseComponent
{
private:
    Axis *x;
    Axis *y;
    MessageBus *messageBus;

    MotionControllerState state = IDLE;

public:
    MotionController(MessageBus *bus) : messageBus(bus)
    {
        x = new Axis(PIN_PULL_MOTOR_X, PIN_DIR_MOTOR_X, PIN_X_ENDSTOP, MAX_SPEED, ACCELERATION, STEPS_PER_MM);
        y = new Axis(PIN_PULL_MOTOR_Y, PIN_DIR_MOTOR_Y, PIN_Y_ENDSTOP, MAX_SPEED, ACCELERATION, STEPS_PER_MM);
    }
    void notify(const CommandData &data) override
    {
        switch (data.command)
        {
        case 'X':
            moveX(data);
            break;
        case 'Y':
            moveY(data);
            break;
        case 'O':
            goToOrigin(data);
            break;
        // Send x position
        case 'x':
            getX(data);
            long xPosition = x->currentPositionInMillimeters();
            messageBus->sendMessage(CommandData('x', (short)xPosition));
            break;
        // Send y position
        case 'y':
            long yPosition = y->currentPositionInMillimeters();
            messageBus->sendMessage(CommandData('y', (short)yPosition));
            break;
        default:
            break;
        }
    }

    void moveX(const CommandData &data)
    {
        x->move(data.value);
        sendAck(data);
    }

    void moveY(const CommandData &data)
    {
        y->move(data.value);
        sendAck(data);
    }
    void getY(const CommandData &data)
    {
        long yPosition = y->currentPositionInMillimeters();
        messageBus->sendMessage(CommandData('x', (short)yPosition));
        //sendAck(data);
    }

    void getX(const CommandData &data)
    {
        long xPosition = x->currentPositionInMillimeters();
        messageBus->sendMessage(CommandData('x', (short)xPosition));
        //sendAck(data);
    }

    void goToOrigin(const CommandData &data)
    {
        x->goToOrigin();
        y->goToOrigin();
        state = TO_ORIGIN;
        sendAck(data);
    }

    void update()
    {
        x->update();
        y->update();

        if (state == TO_ORIGIN)
        {
            if (x->isAtOrigin() && y->isAtOrigin())
            {
                state = IDLE;
                CommandData data('O', -9999);
                messageBus->sendMessage(data);
            }
        }
    }

    void sendAck(const CommandData &data)
    {
        CommandData ack(data.command, data.value);
        messageBus->sendMessage(ack);
    }
};

#endif // MOTION_CONTROLLER_H
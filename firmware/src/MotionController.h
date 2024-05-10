#ifndef MOTION_CONTROLLER_H
#define MOTION_CONTROLLER_H

#include <Arduino.h>
#include "IBaseComponent.h"
#include "Axis.h"

class MotionController : public IBaseComponent
{
public:
    MotionController();

    void notify(const CommandData &data) override;

    void moveX(int millimeters)
    {
    }
    void update()
    {
    }

private:

};

#endif // MOTION_CONTROLLER_H
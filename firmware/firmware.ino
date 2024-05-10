
#include "src/CommandData.h"
#include "src/GlobalVars.h"
#include "src/Axis.h"

#include "src/EventManager.h"

EventManager eventManager;
MotionController* motionController = nullptr;

Axis* x;

#ifdef DEBUG
#define DEBUG_PRINT(x) Serial.print(x)
#define DEBUG_PRINTLN(x) Serial.println(x)
#else
#define DEBUG_PRINT(x)
#define DEBUG_PRINTLN(x)
#endif


using namespace SYSTEM_CONFIG;
void setup()
{
    Serial.begin(115200);
    Serial.println("Hello World!");

    motionController = new MotionController();
    eventManager.addComponent(motionController);
}

void loop()
{
    if (Serial.available() >= 3)
    {
        CommandData data;
        data.command = Serial.read();
        data.value = readShort();
        eventManager.notify(data);

        DEBUG_PRINT("Command: ");
        DEBUG_PRINT(data.command);
        DEBUG_PRINT(", Value: ");
        DEBUG_PRINTLN(data.value);
    }

    // Actualiza el estado de los motores
    motionController->update();
}

short readShort()
{
    // Read a short from the serial port
    byte highByte = Serial.read();
    byte lowByte = Serial.read();
    return (short)((highByte << 8) | lowByte);
}

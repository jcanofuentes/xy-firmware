
#include "src/CommandData.h"
#include "src/EventManager.h"
#include "src/MotionController.h"

EventManager eventManager;
MotionController* motionController = nullptr;
MessageBus* messageBus = nullptr;


void setup()
{
    Serial.begin(115200);
    messageBus = new MessageBus();
    motionController = new MotionController(messageBus);
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
    }

    // Update the motion controller
    motionController->update();
    
    // Send messages
    messageBus->dispatchMessages();
}

// Read a short from the serial port
short readShort()
{
    byte highByte = Serial.read();
    byte lowByte = Serial.read();
    return (short)((highByte << 8) | lowByte);
}

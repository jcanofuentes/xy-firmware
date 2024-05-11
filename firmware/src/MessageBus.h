#ifndef MESSAGE_BUS_H
#define MESSAGE_BUS_H

#include "CommandData.h"
# include <Arduino.h>
# include <Streaming.h>

class MessageBus
{
private:
public:
    MessageBus() {}

    void sendMessage(const CommandData& data)
    {
        sendSerial(data);
    }

    void sendSerial(const CommandData& data)
    {
        Serial.write(data.command);
        Serial.write((byte)(data.value >> 8));
        Serial.write((byte)(data.value & 0xFF));
    } 
};

#endif // MESSAGE_BUS_H
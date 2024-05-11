#ifndef MESSAGE_BUS_H
#define MESSAGE_BUS_H

#include "CommandData.h"
#include <Arduino.h>
#include <Streaming.h>
#include <Vector.h>

const int ELEMENT__MAX = 5; // Maximum number of messages

class MessageBus
{
private:
    CommandData storage_array[ELEMENT__MAX];
    Vector<CommandData> messages;

public:
    MessageBus()
    {
        messages.setStorage(storage_array);
    }

    void dispatchMessages()
    {
        for (const CommandData &message : messages)
        {
            sendSerial(message);
        }
        messages.clear(); // Clear the messages

    void sendMessage(const CommandData &data)
    {
        messages.push_back(data);
    }

    void sendSerial(const CommandData &data)
    {
        Serial.write(data.command);
        Serial.write((byte)(data.value >> 8));
        Serial.write((byte)(data.value & 0xFF));
    }
};

#endif // MESSAGE_BUS_H
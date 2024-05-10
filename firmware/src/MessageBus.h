#ifndef MESSAGE_BUS_H
#define MESSAGE_BUS_H

#include "CommandData.h"
# include <Arduino.h>

class MessageBus
{
private:
public:
    MessageBus() {}

    void sendMessage(const CommandData& data)
    {
        // Serial << "MessageBus sendMessage: " << data << endl;
    }
};

#endif // MESSAGE_BUS_H
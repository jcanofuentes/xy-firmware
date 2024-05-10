#include "EventManager.h"

EventManager::EventManager()
{
    components.setStorage(storage_array);
}

void EventManager::addComponent(IBaseComponent *component)
{
    Serial << "EventManager addComponent" << endl;
    components.push_back(component);
}

void EventManager::notify(const CommandData &data)
{
    // Serial << "EventManager notify: " << data << endl;
    for (int i = 0; i < components.size(); i++)
    {
        components[i]->notify(data);
        /*         
        Serial.print("EventManager notify: Command - ");
        Serial.print(data.command);
        Serial.print(", Value - ");
        Serial.println(data.value); 
        */
    }
}

void EventManager::printComponents()
{
    Serial << "EventManager printComponents" << endl;
    for (int i = 0; i < components.size(); i++)
    {
        char buffer[50];
        sprintf(buffer, "Component %d: %p", i, components[i]);
        Serial << buffer << endl;
    }
}
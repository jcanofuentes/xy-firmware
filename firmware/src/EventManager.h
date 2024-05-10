#ifndef EVENT_MANAGER_H
#define EVENT_MANAGER_H

#include "IBaseComponent.h"
#include "CommandData.h"
#include <Arduino.h>
#include <Streaming.h>
#include <Vector.h>

const int ELEMENT_COUNT_MAX = 5; // Maximum number of components

class EventManager
{
private:
  IBaseComponent *storage_array[ELEMENT_COUNT_MAX];
  Vector<IBaseComponent *> components;

public:
  EventManager()
  {
    components.setStorage(storage_array);
  }

  void addComponent(IBaseComponent *component)
  {
    components.push_back(component);
  }

  void notify(const CommandData &data)
  {
    for (int i = 0; i < components.size(); i++)
    {
      components[i]->notify(data);
    }
  }
};

#endif // EVENT_MANAGER_H
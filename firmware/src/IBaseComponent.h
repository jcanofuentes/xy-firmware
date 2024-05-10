#ifndef I_BASE_COMPONENT_H
#define I_BASE_COMPONENT_H

#include "CommandData.h"

class IBaseComponent {
public:
    virtual void notify(const CommandData& data) = 0;
};

#endif // I_BASE_COMPONENT_H
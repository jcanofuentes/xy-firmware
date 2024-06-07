# XY Firmware

## Overview
XY Firmware is designed to control motion systems, such as CNC machines or 3D printers, using a serial interface. The firmware receives commands from a graphical user interface (GUI) and controls the motion of the system accordingly. It also provides feedback to the GUI about the system status.

## Installation
To install and set up the XY Firmware, follow these steps:

1. **Clone the repository:**
    ```sh
    git clone https://github.com/jcanofuentes/xy-firmware.git
    cd xy-firmware
    ```

2. **Install dependencies:**
    Ensure you have the Arduino IDE installed and all required libraries.

3. **Build the project:**
    Open `firmware/firmware.ino` in the Arduino IDE and upload it to your microcontroller.

## Usage
To use the XY Firmware, follow these steps:

1. **Connect the hardware:**
    Ensure the microcontroller is properly connected to the motion system and the computer running the GUI.

2. **Run the firmware:**
    The firmware will start running once uploaded to the microcontroller.

3. **Send commands via GUI:**
    Use the GUI to send commands to the firmware. The firmware will process these commands and control the motion system accordingly.

## Components Explanation

### EventManager
The `EventManager` handles the communication between different components of the system. It receives commands and notifies the relevant components to act on them.

```cpp
#include "src/EventManager.h"

EventManager eventManager;
```

### MotionController
The MotionController is responsible for controlling the motion of the system. It receives commands through the EventManager and updates the system's motion accordingly.
```cpp
#include "src/MotionController.h"

MotionController* motionController = nullptr;
motionController = new MotionController(messageBus);
eventManager.addComponent(motionController);
```
### MessageBus
The MessageBus handles the sending of messages, such as status updates, back to the GUI. This allows the GUI to receive feedback from the firmware about the current state of the system.
```cpp
#include "src/MessageBus.h"

MessageBus* messageBus = nullptr;
messageBus = new MessageBus();
```

### Firmware Code Explanation
The firmware.ino file contains the main logic for the firmware.

```cpp
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

    motionController->update();
    messageBus->dispatchMessages();
}

short readShort()
{
    byte highByte = Serial.read();
    byte lowByte = Serial.read();
    return (short)((highByte << 8) | lowByte);
}
```
### Serial Communication
The firmware uses the Serial object for communication with the GUI. The baud rate is set to 115200.

### Receiving Commands
Commands are received in the loop function. When at least 3 bytes are available in the serial buffer, the firmware reads the command and value and notifies the EventManager.

### Event Management
The EventManager notifies the relevant components to handle the commands. The MotionController is updated in each iteration of the loop.

### Sending Messages
The MessageBus sends messages back to the GUI, providing feedback about the system's status.

### Directory Structure
```bash
xy-firmware/
│-- firmware/
│   │-- firmware.ino
│   │-- src/
│       │-- CommandData.h
│       │-- EventManager.h
│       │-- MotionController.h
│       │-- MessageBus.h
│-- gui/
│   │-- src/
│-- .gitignore
│-- LICENSE
```
### License
This project is licensed under the terms of the MIT License.

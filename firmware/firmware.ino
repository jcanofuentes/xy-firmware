#include <AccelStepper.h>

#include <Arduino.h>
#include "src/EventManager.h"
#include "src/CommandData.h"
#include "src/MotionController.h"
#include "src/GlobalVars.h"

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

    //setupEventManger();
    x = new Axis(PIN_PULL_MOTOR_X, PIN_DIR_MOTOR_X, PIN_X_ENDSTOP, MAX_SPEED, ACCELERATION, STEPS_PER_MM_X);

}

void setupEventManger()
{
    motionController = new MotionController();
    eventManager.addComponent(motionController);
    eventManager.printComponents();
}

void loop()
{
    if (Serial.available() >= 3)
    {
        CommandData data;
        data.command = Serial.read();
        data.value = readShort();


        switch ( data.command )
        {
        case 'X':
            x->move(data.value);
            break;
        case 'O':
            x->goOrigin();
            break;
        default:
            break;
        }

        DEBUG_PRINT("Command: ");
        DEBUG_PRINT(data.command);
        DEBUG_PRINT(", Value: ");
        DEBUG_PRINTLN(data.value);

        eventManager.notify(data);
    }

    x->update();

/*     // Ejemplo para mover a 100 mm y regresar al origen
    static bool moved = false;
    if (!moved)
    {
        motionController->moveX(100); // Mueve el motor a 100 mm
        moved = true;
    }

    if (moved && motionController->x.currentPositionInMillimeters() == 100)
    {
        motionController->x.goOrigin(); // Regresa el motor al origen
    }

    // Actualiza el estado de los motores
    motionController->update(); */
}

short readShort()
{
    // Read a short from the serial port
    byte highByte = Serial.read();
    byte lowByte = Serial.read();
    return (short)((highByte << 8) | lowByte);
}

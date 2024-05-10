// CommandData.h
#ifndef COMMAND_DATA_H
#define COMMAND_DATA_H

struct CommandData {
    char command;
    short value;
    // Constructors
    CommandData() : command(0), value(0) {}
    CommandData(char cmd, short val) : command(cmd), value(val) {}
};

#endif // COMMAND_DATA_H
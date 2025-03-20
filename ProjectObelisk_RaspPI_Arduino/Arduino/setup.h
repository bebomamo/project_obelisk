#include <CameraOV7670.h>
#include <CameraOV7670RegisterDefinitions.h>
#include <CameraOV7670Registers.h>

//
// Created by indrek on 1.05.2016.
//

#ifndef OV7670_SETUP_H
#define OV7670_SETUP_H

/*
 *
 *  EXAMPLE = 3
 *  Reads data from LiveOV7670Library and send it over UART to computer
 *  https://github.com/indrekluuk/ArduImageCapture
 *
 *
 */
#define EXAMPLE 3



void initializeScreenAndCamera();
void processFrame();



#endif //OV7670_SETUP_H

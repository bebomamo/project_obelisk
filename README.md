# Project Overview
Project Obelisk aimed to recreate and enhance the traditional key tag unlocking systems widely used for business security. Our approach replaces the physical key tag with a "custom key" powered by image recognition via artificial intelligence. The "custom key" can be any object that can be uniquely recognized, such as the back of your phone, a rubber duck, or even an apple. The system allows users to dynamically train and store custom keys, which are then used to activate a connected device, such as a servo motor. In our prototype, this servo motor simulates a door lock mechanism, showcasing the concept's functionality.

![Demo](https://github.com/user-attachments/assets/e05cc01c-2aee-4061-800d-37bee5872383)

# About this Project
This project was developed over the course of 10 weeks for the Advanced Digital Systems Lab (ECE395) at UIUC. It involved the creation of a hardware-based system, where my partner and I individually or collaboratively explored the complexities of embedded systems, hardware design, and artificial intelligence. Our journey was marked by numerous challenges that required extensive research, documentation reading, and hands-on troubleshooting, pushing our knowledge and skills in electrical and embedded systems design to new limits.

# Project Obelisk
Project Obelisk is the main undertaking, designed as an all-in-one solution that integrates image processing, AI for object recognition, and a control loop to manage the servo motor and LED indicators. This system seamlessly ties together hardware and software components, allowing for dynamic key recognition and an output signal to trigger external devices.

# Project Obelisk Arduino / Raspberry Pi
The Arduino/Raspberry Pi subproject was designed as a testing environment for simpler systems and to verify our concept before moving to low-level C implementation. This step involved experimenting with synchronization signals, image array padding, and baud rate requirements for camera debugging. Using the Arduino/Raspberry Pi setup allowed us to handle some of the image processing off the primary microcontroller, providing valuable insights into data flow, timing, and system behavior.

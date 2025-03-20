/*
 * OV7670.h
 *  Created in: 2022
 *     Author: J. Bajic
 *
 *  Modified on: Dec 2, 2024
 *      Modified: bnigg2
 */

#ifndef OV7670_H_
#define OV7670_H_

#include <stdint.h>
#include "stm32h7xx_hal.h"

#define OV7670_RST_PORT		GPIOD
#define OV7670_RST_PIN		GPIO_PIN_12
#define OV7670_PWDN_PORT	GPIOD
#define OV7670_PWDN_PIN		GPIO_PIN_14
#define OV7670_ADDR 		0x42
#define OV7670_TIMEOUT 		1000

//-------------------------------------------------
#define F_XCLK 		24 		// 24MHz set by MCO
//-------------------------------------------------

typedef enum {CONTINUOUS=0, SNAPSHOT} Capture_mode;

typedef enum {OFF=0, ON} Camera_state;
typedef enum {YUV422=0, RGB565} Camera_format;
typedef enum {VGA=0, QVGA, QQVGA, QQQVGA, CIF, QCIF, QQCIF} Camera_resolution;

/* Only QVGA and RGB565 defined */
typedef struct{
	Camera_resolution resolution; 	// 0-VGA, 1-QVGA, 2-QQVGA, 3-CIF, 4-QCIF, 5-QQCIF
	Camera_format format;			// 0-YUV422, 1-RGB565
}Camera_settings;

extern volatile uint8_t frame_ready;

/**
 * @brief Initialize the OV7670 camera module.
 * @param p_hdcmi Pointer to the DCMI handle.
 * @param p_hdma_dcmi Pointer to the DMA handle for DCMI.
 * @param p_hi2c Pointer to the I2C handle for communication with the OV7670.
 */
void OV7670_Init(DCMI_HandleTypeDef *p_hdcmi, DMA_HandleTypeDef *p_hdma_dcmi, I2C_HandleTypeDef *p_hi2c);

/**
 * @brief Control the power state of the OV7670 camera module.
 * @param en Set to 1 to power up, 0 to power down.
 */
void OV7670_Power(uint8_t en);

/**
 * @brief Perform a hardware reset of the OV7670 camera module.
 */
void OV7670_ResetHW(void);

/**
 * @brief Write a value to a specific register in the OV7670 using SCCB (I2C).
 * @param regAddr Address of the register to write to.
 * @param val Value to write into the register.
 */
void OV7670_WriteSCCB(uint8_t regAddr, uint8_t val);

/**
 * @brief Read a value from a specific register in the OV7670 using SCCB (I2C).
 * @param regAddr Address of the register to read from.
 * @param data Pointer to store the read value.
 */
void OV7670_ReadSCCB(uint8_t regAddr, uint8_t *data);

/**
 * @brief Start image capture in snapshot or continuous mode.
 * @param mode Capture mode (SNAPSHOT or CONTINUOUS).
 * @param capture_address Address of the buffer to store captured image data.
 */
void OV7670_Start(Capture_mode mode, uint16_t *capture_address);

/**
 * @brief Stop image capture.
 */
void OV7670_Stop(void);

/**
 * @brief Perform a software reset on the OV7670 and load default configurations.
 */
void OV7670_ResetSW(void);

/**
 * @brief Configure OV7670 registers using an array of parameter pairs.
 * @param params Array of register address and value pairs. The last entry should have 0xFF as the address to indicate the end.
 */
void OV7670_Config(const uint8_t params[][2]);

/**
 * @brief Configure the horizontal and vertical frame boundaries.
 * @param hstart Horizontal start boundary.
 * @param hstop Horizontal stop boundary.
 * @param vstart Vertical start boundary.
 * @param vstop Vertical stop boundary.
 */
void OV7670_SetFrameControl(uint16_t hstart, uint16_t hstop, uint16_t vstart, uint16_t vstop);

/**
 * @brief Retrieve the current image properties.
 * @param width Pointer to store the image width.
 * @param height Pointer to store the image height.
 * @param format Pointer to store the image format.
 */
void OV7670_getImageInfo(uint16_t *width, uint16_t *height, uint8_t *format);


#endif /* OV7670_H_ */

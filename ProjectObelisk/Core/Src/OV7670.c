/*
 * OV7670.c
 *
 *  Created on: Dec 2, 2024
 *      Author: BRADE
 */

#include "OV7670.h"
#include "OV7670REG.h"


#define ENABLE_HSYNC 0
#define ENABLE_VSYNC 0

// Internal Static Variables
static DCMI_HandleTypeDef *sp_hdcmi;
static DMA_HandleTypeDef *sp_hdma_dcmi;
static I2C_HandleTypeDef *sp_hi2c;
//static LPTIM_HandleTypeDef *sp_hlptim;

static uint8_t capture_mode=0;
static uint32_t img_address=0;
static uint16_t img_width=320;
static uint16_t img_height=240;
static uint8_t img_format=RGB565;

volatile uint8_t frame_ready = 0;

/* Initialize the OV7670 camera with provided handles for DCMI, DMA, and I2C */
void OV7670_Init(DCMI_HandleTypeDef *p_hdcmi, DMA_HandleTypeDef *p_hdma_dcmi, I2C_HandleTypeDef *p_hi2c) {
    sp_hdcmi = p_hdcmi;         // Store the DCMI handle
    sp_hdma_dcmi = p_hdma_dcmi; // Store the DMA handle
    sp_hi2c = p_hi2c;           // Store the I2C handle
}

/* Control the power state of the OV7670 camera */
void OV7670_Power(uint8_t en) {
    if (en) {
        // Power ON: Set the PWDN pin to LOW
        HAL_GPIO_WritePin(OV7670_PWDN_PORT, OV7670_PWDN_PIN, GPIO_PIN_RESET);
    } else {
        // Power OFF: Set the PWDN pin to HIGH
        HAL_GPIO_WritePin(OV7670_PWDN_PORT, OV7670_PWDN_PIN, GPIO_PIN_SET);
    }
    HAL_Delay(50); // Wait for power state to stabilize
}

/* Perform a hardware reset on the OV7670 camera */
void OV7670_ResetHW(void) {
    HAL_GPIO_WritePin(OV7670_RST_PORT, OV7670_RST_PIN, GPIO_PIN_RESET); // Assert reset
    HAL_Delay(50); // Wait for reset to take effect
    HAL_GPIO_WritePin(OV7670_RST_PORT, OV7670_RST_PIN, GPIO_PIN_SET);   // Deassert reset
    HAL_Delay(50); // Wait for reset to stabilize
}

/* Write a value to a specific SCCB register on the OV7670 */
void OV7670_WriteSCCB(uint8_t regAddr, uint8_t val) {
    uint8_t txbuf[2] = {regAddr, val}; // Prepare data for transmission (register + value)
    HAL_I2C_Master_Transmit(sp_hi2c, OV7670_ADDR, txbuf, 2, OV7670_TIMEOUT); // Transmit data via I2C
}

/* Read a value from a specific SCCB register on the OV7670 */
void OV7670_ReadSCCB(uint8_t regAddr, uint8_t *data) {
    HAL_I2C_Master_Transmit(sp_hi2c, OV7670_ADDR, &regAddr, 1, OV7670_TIMEOUT); // Transmit register address
    HAL_I2C_Master_Receive(sp_hi2c, OV7670_ADDR, data, 1, OV7670_TIMEOUT);      // Receive the register value
}

/* Start capturing images in snapshot or continuous mode */
void OV7670_Start(Capture_mode mode, uint16_t *capture_address) {
    capture_mode = mode;                   // Set the capture mode
    img_address = (uint32_t)capture_address; // Set the address for captured image data

    if (capture_mode == SNAPSHOT) {
        // Start DMA for single-frame capture
        HAL_DCMI_Start_DMA(sp_hdcmi, DCMI_MODE_SNAPSHOT, img_address, img_width * img_height / 2);
    } else {
        // Start DMA for continuous capture
        HAL_DCMI_Start_DMA(sp_hdcmi, DCMI_MODE_CONTINUOUS, img_address, img_width * img_height / 2);
    }
}

/* Stop capturing images */
void OV7670_Stop() {
    HAL_DCMI_Stop(sp_hdcmi); // Stop DCMI capture
}

/* Configure OV7670 registers based on a parameter array */
void OV7670_Config(const uint8_t params[][2]) {
    for (int i = 0; params[i][0] != 0xFF; i++) { // Loop through the parameter list until the end marker (0xFF)
        uint8_t data;
        OV7670_WriteSCCB(params[i][0], params[i][1]); // Write the new value to the register
        OV7670_ReadSCCB(params[i][0], &data);    // Read back the value to confirm
        HAL_Delay(1); // Short delay between register writes
    }
}

/* Perform a software reset on the OV7670 and configure it */
void OV7670_ResetSW(void) {
    OV7670_WriteSCCB(REG_COM7, 0x80); // Issue a software reset
    HAL_Delay(30); // Wait for the reset to complete
    OV7670_Config(QVGA_RGB565_regs);  // Load default configuration for QVGA RGB565
    HAL_Delay(10); // Wait for configuration to take effect
}

/* Set frame boundaries for horizontal and vertical control */
void OV7670_SetFrameControl(uint16_t hstart, uint16_t hstop, uint16_t vstart, uint16_t vstop) {
    OV7670_WriteSCCB(REG_HSTART, (hstart >> 3) & 0xff); // Set horizontal start (upper bits)
    OV7670_WriteSCCB(REG_HSTOP, (hstop >> 3) & 0xff);   // Set horizontal stop (upper bits)
    OV7670_WriteSCCB(REG_HREF, ((hstop & 0x7) << 3) | (hstart & 0x7)); // Combine lower bits for horizontal ref

    OV7670_WriteSCCB(REG_VSTART, (vstart >> 2) & 0xff); // Set vertical start (upper bits)
    OV7670_WriteSCCB(REG_VSTOP, (vstop >> 2) & 0xff);   // Set vertical stop (upper bits)
    OV7670_WriteSCCB(REG_VREF, ((vstop & 0x3) << 2) | (vstart & 0x3)); // Combine lower bits for vertical ref
}

/* Retrieve image width, height, and format information */
void OV7670_getImageInfo(uint16_t *width, uint16_t *height, uint8_t *format) {
    *width = img_width;   // Store image width
    *height = img_height; // Store image height
    *format = img_format; // Store image format
}

/* Handle frame event callbacks for continuous capture mode */
void HAL_DCMI_FrameEventCallback(DCMI_HandleTypeDef *hdcmi) {
    if (capture_mode == CONTINUOUS) {
        frame_ready = 1; // Mark the frame as ready
        // Restart DMA transfer for continuous mode
        HAL_DMA_Start_IT(hdcmi->DMA_Handle, (uint32_t)&hdcmi->Instance->DR, img_address, img_width * img_height / 2);
    }
}

#if ENABLE_VSYNC
void HAL_DCMI_VsyncEventCallback(DCMI_HandleTypeDef *hdcmi)
{}
#endif

#if ENABLE_HSYNC
void HAL_DCMI_LineEventCallback(DCMI_HandleTypeDef *hdcmi)
{}
#endif

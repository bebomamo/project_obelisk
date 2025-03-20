/*
 * OV7670Reg.h
 *  Modified on: Nov 2, 2024
 *      Modifier: bnigg2
 *      Use: Save time define register values
 *
 */

#ifndef OV7670_REG_H_
#define OV7670_REG_H_

/*--------------------OV7670 REGISTER ADDRESSES---------------------------*/

#define REG_GAIN        		0x00    // Gain lower 8 bits (rest in vref)
#define REG_BLUE        		0x01    // blue gain
#define REG_RED         		0x02    // red gain
#define REG_VREF        		0x03    // Pieces of GAIN, VSTART, VSTOP
#define REG_COM1        		0x04    // Control 1
#define REG_BAVE        		0x05    // U/B Average level
#define REG_GbAVE       		0x06    // Y/Gb Average level
#define REG_AECHH       		0x07    // AEC MS 5 bits
#define REG_RAVE        		0x08    // V/R Average level
#define REG_COM2        		0x09    // Control 2
#define REG_PID         		0x0A    // Product ID MSB
#define REG_VER         		0x0B    // Product ID LSB
#define REG_COM3        		0x0C    // Control 3
#define REG_COM4        		0x0D    // Control 4
#define REG_COM5        		0x0E    // All "reserved"
#define REG_COM6        		0x0F    // Control 6
#define REG_AECH        		0x10    // More bits of AEC value
#define REG_CLKRC       		0x11    // Clock control
#define REG_COM7        		0x12    // Control 7
#define REG_COM8        		0x13    // Control 8
#define REG_COM9        		0x14    // Control 9  - gain ceiling
#define REG_COM10       		0x15    // Control 10
								//0x16 RSVD
#define REG_HSTART      		0x17    // Horiz start high bits
#define REG_HSTOP       		0x18    // Horiz stop high bits
#define REG_VSTART      		0x19    // Vert start high bits
#define REG_VSTOP       		0x1A    // Vert stop high bits
#define REG_PSHFT       		0x1B    // Pixel delay after HREF
#define REG_MIDH        		0x1C    // Manuf. ID high
#define REG_MIDL        		0x1D    // Manuf. ID low
#define REG_MVFP        		0x1E    // Mirror / vflip
								//0x1F-0x23
#define REG_AEW         		0x24    // AGC upper limit
#define REG_AEB         		0x25    // AGC lower limit
#define REG_VPT         		0x26    // AGC/AEC fast mode op region
								//0x27-0x29
#define REG_HSYST       		0x30    // HSYNC rising edge delay
#define REG_HSYEN       		0x31    // HSYNC falling edge delay
#define REG_HREF        		0x32    // HREF pieces
								//0x33-0x39
#define REG_TSLB        		0x3A    // lots of stuff
#define REG_COM11       		0x3B    // Control 11
#define REG_COM12       		0x3C    // Control 12
#define REG_COM13       		0x3D    // Control 13
#define REG_COM14				0x3E    // Control 14
#define REG_EDGE        		0x3F    // Edge enhancement factor
#define REG_COM15       		0x40    // Control 15
#define REG_COM16       		0x41    // Control 16
#define REG_COM17       		0x42    // Control 17
								//0x43-0x4B
#define REG_DNSTH				0x4C	// De-noise strength
								//0x4D-0x4E
#define REG_MTX1				0x4F	// Matrix coefficient 1
#define REG_MTX2				0x50	// Matrix coefficient 2
#define REG_MTX3				0x51	// Matrix coefficient 3
#define REG_MTX4				0x52	// Matrix coefficient 4
#define REG_MTX5				0x53	// Matrix coefficient 5
#define REG_MTX6				0x54	// Matrix coefficient 6
#define REG_BRIGHT      		0x55    // Brightness control
#define REG_CONTRAST     		0x56    // Contrast control
#define REG_CONTRAS_CENTER		0x57	// Contrast control
#define REG_MTX_SIGN 			0x58	// Matrix coefficient sign
								//0x59-0x66
#define REG_MANU				0x67	//Manual U Value
#define REG_MANV				0x68	//Manual V Value
#define REG_GFIX        		0x69    // Fix gain control
#define REG_GGAIN				0x6A	// G channel AWB gain
#define REG_DBLV				0x6B	// PLL and regulator control
#define REG_AWBCTR3				0x6C	// AWB Control 3
#define REG_AWBCTR2				0x6D	// AWB Control 2
#define REG_AWBCTR1				0x6E	// AWB Control 1
#define REG_AWBCTR0				0x6F	// AWB Control 0
#define REG_SCALING_XSC			0x70	// Horizontal scale factor
#define REG_SCALING_YSC			0x71	// Vertical scale factor
#define REG_SCALING_DCWCTR		0x72	// DCW Control
#define REG_SCALING_PCLK_DIV	0x73	// Clock divider control
#define REG_REG74				0x74    // Digital gain control
#define REG_REG75				0x75    // Edge enhancement lower
#define REG_REG76				0x76    // Edge enhancement upper
#define REG_REG77				0x77    // De-noise range
								//0x78-0x8B
#define REG_RGB444      		0x8C    // RGB 444 control
								//0x8D-0x9C
#define REG_BD50ST				0x9D 	// 50Hz banding filter value
#define REG_BD60ST				0x9E	// 60Hz banding filter value
#define REG_HAECC1      		0x9F    // Hist AEC/AGC control 1
#define REG_HAECC2      		0xA0    // Hist AEC/AGC control 2
								//0xA1 RSVD
#define REG_SCALING_PCLK_DELAY	0xA2	// Pixel Clock delay
								//0xA3-0xA4
#define REG_BD50MAX     		0xA5    // 50hz banding step limit
#define REG_HAECC3      		0xA6    // Hist AEC/AGC control 3
#define REG_HAECC4     			0xA7    // Hist AEC/AGC control 4
#define REG_HAECC5      		0xA8    // Hist AEC/AGC control 5
#define REG_HAECC6      		0xA9    // Hist AEC/AGC control 6
#define REG_HAECC7      		0xAA    // Hist AEC/AGC control 7
#define REG_BD60MAX     		0xAB    // 60hz banding step limit

/*--------------------END OF OV7670 REGISTER ADDRESSES--------------------*/

/*--------------------OV7670 RESOLUTION CONFIGs---------------------------*/
const uint8_t QVGA_RGB565_regs[][2]={
	//According to OV7670/7171 implementation guide v1.0 - Table 2-2
	//QVGA Specific
	{REG_COM3, 0x04},  					// DCW enable
	{REG_COM14, 0x19},					// Manual scaling
	{REG_SCALING_XSC, 0x3A},  			// Scaling_xsc
	{REG_SCALING_YSC, 0x35},  			// Scaling_ysc
	{REG_SCALING_DCWCTR, 0x11},			// Downsampling control
	{REG_SCALING_PCLK_DIV, 0xF1},
	{REG_SCALING_PCLK_DELAY,0x02},
	//Derived from OV7670/7171 implementation guide v1.0 - Table 8-2
	//RGB565 Specific and Color Calibration
	{REG_COM7, 0x04},					// Camera control register, enables DCW (digital chroma width) processing.
	{REG_RGB444, 0x00},					// Disable RGB444 settings
	{REG_COM1, 0x00},					// Camera control register, disables CCIR656 format setting
	{REG_COM15, 0xD0},					// Control for output format and compression, sets RGB output.
	{REG_COM9, 0x6A},					// Automatic gain control (AGC) settings, 128x Gain Ceiling
	{REG_COM13, 0x40},					// Control for gamma correction, set saturation
	{REG_MTX1, 0xB3},
	{REG_MTX2, 0xB3},
	{REG_MTX3, 0x00},
	{REG_MTX4, 0x3D},
	{REG_MTX5, 0xA7},
	{REG_MTX6, 0xE4},
	//Derived from OV7670/7171 implementation guide v1.0 - Table 3-2
	// Frame Rate Control
	{REG_DBLV, 0x7A},					// x4 multiplier on mclk
	{REG_CLKRC, 0x01},					// /4 divisor on mclk
	{0xFF, 0xFF}						// End
};


/*------------------END OF OV7670 RESOLUTION CONFIGs-----------------------*/
#endif /* OV7670_REG_H_ */


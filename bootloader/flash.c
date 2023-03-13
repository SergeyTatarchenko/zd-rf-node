/******************************************************************************
* File Name          : flash.c
* Author             : zlojdigger
* Version            : v 0.1
* Description        : 
*******************************************************************************/

/* Includes-------------------------------------------------------------------*/

#include "flash.h"

/* Private define  -----------------------------------------------------------*/

#ifndef TARGET_PLATFORM
#define PLATFORM_FLASH_LOCK       flash_control_dummy
#define PLATFORM_FLASH_UNLOCK     flash_control_dummy
#define PLATFORM_FLASH_INIT       flash_control_dummy
#define PLATFORM_FLASH_WRITE_WORD flash_write_word_dummy
#endif /*TARGET_PLATFORM*/

/* Private typedef -----------------------------------------------------------*/

typedef struct
{
	uint32_t  bytes_in_block;
	uint32_t  words_in_block;
	uint32_t* mem_pointer;

}FLASH_BLOCK_CONTROL_S;

typedef enum
{
	FLASH_TASK_IDLE    = 1,
	FLASH_TASK_WRITE   = 2

}FLASH_TASK_E;

/* Extern variables ----------------------------------------------------------*/

/* Private variables ---------------------------------------------------------*/

static void flash_control_dummy   (void);
static void flash_write_word_dummy(const uint32_t mem_addr, const uint32_t word);
/*----------------------------------------------------------------------------*/

static FLASH_BLOCK_CONTROL_S block_control;
static uint8_t*              data_buffer;

/*----------------------------------------------------------------------------*/

void flash_init(void)
{

}

void flash_deInit(void)
{

}

bool flash_prepareWrite()
{

}

bool flash_writeBlock(void)
{
	bool state = false;

	if(
	   (block_control.mem_pointer     == NULL) || 
	   (block_control.bytes_in_block  == 0)    ||
	   (data_buffer                   == NULL)
	   )
	{
		state = false;
	}
	else
	{
		PLATFORM_FLASH_UNLOCK();
		uint32_t* data = (uint32_t*)data_buffer;
		for(int i = 0; i < block_control.words_in_block; i++)
		{
			uint32_t addr = (uint32_t)&(block_control.mem_pointer[i]);
			PLATFORM_FLASH_WRITE_WORD(addr,data[i]);
		}
		PLATFORM_FLASH_LOCK();
		int error = memcmp(data_buffer,block_control.mem_pointer,block_control.bytes_in_block);
		if(error == 0)
		{
			state = true;
		}
		else
		{
			state = false;
		}
	}
	return state;
}

static void flash_write_word_dummy(const uint32_t mem_addr, const uint32_t word)
{
	(void)(mem_addr);
	(void)(word);
}

static void flash_control_dummy(void)
{	
}

/******************************* end of file **********************************/
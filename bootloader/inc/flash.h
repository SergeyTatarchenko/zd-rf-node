/******************************************************************************
* File Name          : flash.h
* Author             : zlojdigger
* Version            : v 0.1
* Description        : header for flash.c
*******************************************************************************/
#ifndef FLASH_H
#define FLASH_H

/* Includes-------------------------------------------------------------------*/

#include <stdint.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>

/* Public typedef -----------------------------------------------------------*/

/* Extern variables ----------------------------------------------------------*/

/* Public function prototypes ------------------------------------------------*/

extern void flash_init       (void);

extern bool flash_writeBlock(void);


#endif /*FLASH_H*/
/******************************* end of file **********************************/
cmake_minimum_required (VERSION 3.0)

set(CMAKE_SYSTEM_NAME Generic)
set(CMAKE_SYSTEM_PROCESSOR ARM)

#set(CMAKE_C_COMPILER arm-none-eabi-gcc)
#set(CMAKE_ASM_COMPILER ${CMAKE_C_COMPILER})
#set(CMAKE_C_COMPILER_WORKS 1)
#set(CMAKE_CXX_COMPILER_WORKS 1)

project (stm32f030_startup)

set ( DIR_SRCS
      system_stm32f0xx.c
      startup_stm32f0xx.s
    )

add_library (stm32f030_startup STATIC ${DIR_SRCS})

target_include_directories(stm32f030_startup PRIVATE
        include
        )        
target_compile_options(stm32f030_startup PRIVATE
        -mcpu=cortex-m0
        -mthumb
        -mlittle-endian
        -fdata-sections
        -ffunction-sections
        -O1
        -Wall
        )


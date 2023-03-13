cmake_minimum_required (VERSION 3.0)

set(CMAKE_SYSTEM_PROCESSOR ARM)
set(CMAKE_SYSTEM_NAME Generic)

set(CMAKE_C_COMPILER arm-none-eabi-gcc)
set(CMAKE_ASM_COMPILER ${CMAKE_C_COMPILER})

set(CMAKE_C_COMPILER_WORKS 1)
set(CMAKE_CXX_COMPILER_WORKS 1)

project (bootloader)
enable_language(C ASM)

set(DIR_SRCS
        main.c
        flash.c
)

set(CMAKE_SHARED_LIBRARY_LINK_C_FLAGS "")
set(CMAKE_SHARED_LIBRARY_LINK_CXX_FLAGS "")

set(EXECUTABLE ${PROJECT_NAME}.elf)

add_executable (${EXECUTABLE} ${DIR_SRCS})

#path to shared library for stm32f030
add_subdirectory(portable/STM32F030)	
target_link_directories(${EXECUTABLE} PUBLIC portable/STM32F030)
target_link_libraries (${EXECUTABLE} stm32f030_startup)
set(LINKER_SCRIPT  portable/STM32F030/STM32F030R8_FLASH.ld) 

target_include_directories(${EXECUTABLE} PRIVATE
        portable/STM32F030/include
        inc
        )        

target_compile_options(${EXECUTABLE} PRIVATE
        -mcpu=cortex-m0
        -mthumb
        -mlittle-endian
        -fdata-sections
        -ffunction-sections
        -O1
        -Wall
        )

target_link_options(${EXECUTABLE} PRIVATE
        -T${LINKER_SCRIPT}
        -mcpu=cortex-m0
        -mthumb
        -mlittle-endian
       --specs=nano.specs
        -Wl,--gc-sections
        -lc -lnosys -lm
        )

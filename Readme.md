# sdk-thirdparty-platformio

### 1. 要求：

+ RT-Thread Studio 版本>2.0.0
+ windows 10 x64 操作系统
+ 用户目录磁盘空间 > 2G

### 2. 安装

使用 RT-Thread Studio 的 SDK manager 进行安装

### 3. 钩子说明

post_install.bat 的执行方式为 cmd + rt-studio version number

示例

```powershell
./post_install.bat 2.0.0
```

###  4. 内置的 package 列表

+ cmsis-stm32f0
+ cmsis-stm32f1
+ cmsis-stm32f2
+ cmsis-stm32f4
+ cmsis-stm32f7
+ cmsis-stm32h7
+ cmsis-stm32l4
+ libopencm3
+ arduinoststm32
+ stm32cube
+ openocd
+ scons
+ gcc
+ mbed

###  5. 内置的 platform 列表

+ ststm32
[English](./README.md) | [简体中文](./README_CN.md)

# huaweicloud-iot-device-sdk-c Development Guide

- [0.Version update instructions](#0)
- [1.Preface](#1)
- [2.SDK Introduction](#2)
  - [2.1 Function Support](#2.1)
  - [2.2 SDK directory structure](#2.2)
- [3.Preparation](#3.)
  - [3.1 Environmental information](#3.1)
  - [3.2 Compile openssl library](#3.2)
  - [3.3 Compile paho library](#3.3)
  - [3.4 Compile zlib library](#3.4)
  - [3.5 Compile Huawei security function library](#3.5)
  - [3.6 Compile libssh library](#3.6)
  - [3.7 Compile libnopoll library](#3.7)
  - [3.8 Compile curl library](#3.8)
  - [3.9 Upload profile and register device](#3.9)
- [4.Quick experience](#4)
- [5.Device initialization](#5)
  - [5.1 Underlying data initialization](#5.1)
  - [5.2 Set log printing function](#5.2)
  - [5.3 Initialization connection parameters](#5.3)
  - [5.4 Callback function configuration](#5.4)
  - [5.5 Device Authentication](#5.5)
  - [5.6 Subscribe to Topic](#5.6)
  - [5.7 Compile and run the program](#5.7)
- [6.SDK function](#6)
  - [6.1 Generate SDK library files](#6.1)
  - [6.2 Device Access](#6.2)
  - [6.3 Device message reporting and delivery](#6.3)
  - [6.4 Attribute reporting and distribution](#6.4)
  - [6.5 Command issuance](#6.5)
  - [6.6 Disconnection and reconnection](#6.6)
  - [6.7 Device Shadow](#6.7)
  - [6.8 Time synchronization](#6.8)
  - [6.9 Software and firmware upgrade (OTA)](#6.9)
  - [6.10 File upload\download](#6.10)
  - [6.11 Pan-Protocol & Bridge](#6.11)
  - [6.12 National secret TLS access](#6.12)
  - [6.13 Exception storage](#6.13)
  - [6.14 MQTT5.0](#6.14)
  - [6.15 MQTT_DEBUG function](#6.15)
  - [6.16 Gateways and Subdevices](#6.16)
  - [6.17 Remote configuration](#6.17)
  - [6.18 Anomaly Detection](#6.18)
  - [6.19 Softbus function](#6.19)
  - [6.20 Log upload](#6.20)
  - [6.21 Client-side rule engine](#6.21)
  - [6.22 Remote login](#6.22)
  - [6.23 Edge M2M function](#6.23)
  - [6.24 gn compile](#6.24)
  - [6.25 Use global variables to configure connection parameters](#6.25)
  - [6.26 Equipment issuance](#6.26)
- [7.Frequently Asked Questions](#7)
- [8.Open Source Agreement](#8)

<h1 id = "0">0. Version update instructions</h1>

| Version number | Change type | Function description |
| ------ | -------- | ------------------------------------------------------------ |
| 1.2.1 | Function enhancement | Add intelligent site anomaly detection. |
| 1.2.0 | Function enhancement | Added SDK test code and demo to optimize code usage. |
| 1.1.5 | Function enhancement | New usage examples |
| 1.1.4 | Function enhancement | Update OTA upgrade transmission format |
| 1.1.3 | Function enhancement | Update conf\rootcert.pem certificate and add log upload |
| 1.1.2 | New features | Added rule engine, M2M, gn compiled files, anomaly detection, log printing timestamp, MQTT_DEBUG, national secret algorithm, remote configuration, end-cloud secure communication (soft bus) functions |
| 1.1.1 | New features | Added SSH remote operation and maintenance function |
| 1.1.0 | New features | Add MQTT5.0 function, optimize code, fix memory overflow problem |
| 1.0.1 | Function enhancement | Added scenarios where mqtts does not verify the platform public key, TLS version is V1.2, and added message storage samples |
| 0.9.0 | New features | Add gateway update sub-device status interface |
| 0.8.0 | Function enhancement | Replace the new access domain name (iot-mqtts.cn-north-4.myhuaweicloud.com) and root certificate. &lt;br/&gt;If the device uses the old domain name (iot-acc.cn-north-4.myhuaweicloud.com) to access, please use the v0.5.0 version of the SDK |
| 0.5.0 | Function enhancement | The sdk is preset with the device access address and the CA certificate supporting the Huawei IoT platform, and supports docking with the Huawei Cloud IoT platform. |

*2023/07/22*

<h1 id = "1">1 Introduction</h1>

This article uses examples to describe how huaweicloud-iot-device-sdk-c (hereinafter referred to as SDK) helps devices qu

[...截断...]

ickly connect to the Huawei IoT platform using the MQTT protocol.

<h1 id = "2">2.SDK Introduction</h1>
<h2 id = "2.1">2.1 Function support</h2>

The SDK is oriented to embedded terminal devices with strong computing and storage capabilities. Developers can achieve uplink and downlink communication between the device and the IoT platform by calling the SDK interface. The functions currently supported by the SDK are:  

| Function                                    | Description                                                  |
| ------------------------------------------- | ------------------------------------------------------------ |
| [Device Access](#6.2)                       | As a client, use the MQTT protocol to connect to the Huawei Cloud Platform. It is divided into two authentication methods: certificate authentication and key authentication. |
| [Disconnection and reconnection](#6.6)      | When the device's link is disconnected due to network instability or other reasons, the device will reconnect at intervals until the connection is successful. |
| [Message reporting](#6.3)                   | Used by devices to report customized data to the platform, and the platform forwards the messages reported by the device to the application server or other Huawei Cloud cloud services for storage and processing. |
| [Attribute Reporting](#6.4)                 | Used by the device to report attribute data to the platform in the format defined in the product model. |
| [Command delivery](#6.5)                    | Used by the platform to deliver device control commands to the device. After the platform issues a command, the device needs to return the execution result of the command to the platform in a timely manner. |
| [Device Shadow](#6.6)                       | Used to store the online status of the device, the device attribute value last reported by the device, and the configuration expected to be delivered by the application server. |
| [Software and Firmware (OTA) Upgrade](#6.9) | Used to download the OTA upgrade package in conjunction with the platform. |
| [Time Synchronization](#6.8)                | The device initiates a time synchronization request to the platform. |
| [Gateway and sub-device](#6.16)             | Gateway device: A device directly connected to the platform through the protocol supported by the platform. Sub-device: For devices that do not implement the TCP/IP protocol stack, since they cannot communicate directly with the IoT platform, they need to forward data through the gateway. Currently, only devices directly connected to the platform through the mqtt protocol are supported as gateway devices. |
| [File Upload/Download](#6.10)               | The device is supported to upload operation logs, configuration information and other files to the platform, which facilitates users to perform log analysis, fault location, device data backup, etc. |
| [Anomaly Detection](#6.18)                  | Provides security detection capabilities to continuously detect security threats to the device. Including: 1. Memory leak detection 2. Abnormal port detection 3. CPU usage detection 4. Disk space detection 5. Battery power detection |
| [Rule Engine](#6.21)                        | Through conditional triggering and based on preset rules, it triggers collaborative reactions of multiple devices to achieve device linkage and intelligent control. Currently, the IoT platform supports two types of linkage rules: cloud rules and client-side rules. |
| [MQTT5.0](#6.14)                            | The MQTT5.0 version protocol adds new MQTT5.0 features: comparison data, Clean Start and Session Expiry Interval, payload identification and content type, topic alias, user Attributes. |
| [National Secret Algorithm](#6.12)          | A TLS encryption algorithm.                                  |
| [Remote Configuration](#6.17)               | Provides remote configuration function, which allows users to remotely update 
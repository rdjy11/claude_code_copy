# Base Tech SWRS DHU 结构化需求清单

> 来源：吉利汽车研究院 Base Tech SWRS DHU 软件需求规范（Note-SWRS，Revision 005，2019-07-11，共 1572 页）

> 需求条目总数：**1999** 条

> 说明：本清单由分页文档自动切分生成，逐条保留「编号 / 标题 / 版本 / 验证方式 / 适用 AUTOSAR 版本 / 核心要求句」。


---

## 数据完整性说明

数据来源覆盖页码 1-100、101-200、201-1572，即源文档全部 1572 页，未发现内容缺失。需求编号存在正常跳跃（例如 417 与 459 之间），系文档自身编号规则所致，非内容缺失。


---

## 需求清单


### 355 — CC Subscriber ECU configuration states
- 版本：v7 ｜ 验证方式：Test ｜ 适用：通用
- a) CC legacy general principles: The ECU/system shall determine what appropriate action(s) are to be taken for a specific function/feature when utilizing a default configuration or validated CCP data.
- CC Subscriber ECUs shall implement default values for CCPs based on any required default operating condition so that the appropriate functionality can be achieved and where necessary failure mode management actions shall be active.
- The operation of the functions within the ECU strategy shall be in line with FMEA rules affecting safety of the vehicle and occupants and customer satisfaction in the absence of configuration information.

### 356 — CC Subscriber ECU in Bulk (unconfigured) state
- 版本：v6 ｜ 验证方式：Test ｜ 适用：通用
- If the CC Subscriber ECU has not received or does not contain expected CCP data after 30 seconds from its application boot-up sequence while residing within ECU delivery default/Bulk State, the CC Subscriber ECU shall use DTC "Car Configuration – Not Configured" U2300- 55, DTC test according to [CCF_2] UDS Data.

### 357 — Routines for receiving VCP signal (CC Domain Master excluded)
- 版本：v9 ｜ 验证方式：Test ｜ 适用：通用
- a) The CC Subscriber ECU shall be able to read BlockID#, in the VCP signals, arriving in any order, in accordance with table VCP signal mapping in chapter Record of tables.
- b) The CC Subscriber ECU shall be able to receive and process every arrival of a BlockID in the Vehicle configuration signals VehCfgPrm and VehCfgPrmExt.

### 358 — Invalid or unrecognized parameter values
- 版本：v7 ｜ 验证方式：Test ｜ 适用：通用
- If any CCP value(s) used for configuration (including values $00_H$ and $FF_H$ ) is received and evaluated invalid or unrecognized by the CC Subscriber ECU, the related function shall perform the following actions: a) Enter a safe mode (depending on ECU strategy in line with FMEA rules) if there is an imminent risk of serious errors.

### 359 — Configuration of ECU with updated CCP data
- 版本：v7 ｜ 验证方式：Test ｜ 适用：通用
- a) The CC Subscriber ECU shall have two separate states of configuration relating to Central Car Configuration parameters.

### 360 — Selection of CCPs in VCP signal
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- The CC Subscriber ECU shall use information in a parameter list or equivalent (released/extracted from CCdB) containing the CCP numbers that the CC Subscriber ECU has requested use for or is required to configure by.
- The BlockID# (in the VCP signal), and byte position, in which a specific CCP can be obtained, shall be according to table VCP signal mapping in chapter Record of tables.

### 361 — Car Configuration data storage
- 版本：v7 ｜ 验证方式：Test ｜ 适用：通用
- The CC Subscriber ECU must be able to maintain parameter values between normal drive cycles, ECU resets, power cycles and low voltage due to engine cranking.
- All CC Subscriber ECUs shall store their valid CCP data used for configuration in non-volatile memory (NVM).
- The format/interpretation of the parameter(s) to be stored shall be specified in the SWRS of each ECU subscribing to that parameter.

### 362 — Car Configuration parameter definition
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- A Car Configuration parameter shall have the same definition in the CC Subscriber ECU as in CCdB.

### 363 — Handling of parameter data
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- c) CCP value 00h and FFh shall not be used for any ECU SW configuration.

### 364 — ECU configuration after boot-up
- 版本：v6 ｜ 验证方式：Test ｜ 适用：通用
- After ECU application boot-up sequence the CC Subscriber ECU shall use the current set of stored CCP values (or default configuration if no previous data received/available).
- Once, as soon as a new set of parameter values is received, the CC Subscriber ECU shall evaluate the new parameter values, dependent on which configuration state the CC Subscriber ECU currently resides in (see requirement CC Subscriber ECU configuration states).

### 365 — CC Subscriber ECU DID support
- 版本：v7 ｜ 验证方式：Test ｜ 适用：通用
- a) When receiving invalid or unrecognized parameter values (according to requirement Invalid or unrecognized parameter values), the CC Subscriber ECU shall store the faulty parameter and related value.
- b) The CC Subscriber ECU shall support read out of DID "Car Configuration - Faulty Parameters Received" (0xE103 as specified in [CCF_2] UDS Data), format according to the table below.
- It shall be possible to read out up to 10 faulty CCPs identified by the CC Subscriber ECU, required only for parameter#/IDs that can be represented using 2 bytes hexadecimal code.

### 366 — A2B System Configuration responsibility
- 版本：v1 ｜ 验证方式：Inspection ｜ 适用：通用
- To define the responsibility for developing a A2B System configuration. The system owner for the specific use case is responsible to develop and define the configuration parameters for A2B.

### 367 — Define the origin of A2B configuration
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- To define the origin of A2B configuration The A2B configuration that shall be used in a particular A2B system shall be defined and stored in the node's Local Configuration.
- The configuration shall contain all transceiver register settings for the master plus all slaves that are needed for the A2B-system to work.

### 368 — Multiple A2B System configurations
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- If multiple configurations of an A2B bus depending on the Car Configuration are used, shall all possible configurations be stored in a Local Configuration and the selection of which shall be used will be by a parameter in the Car Configuration.

### 369 — Read and write to A2B chip registers
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- To define that it shall be possible to read and write to the A2B internal registers.
- [A2B-DL-10] and [A2B-DL-11] It shall be possible to read and write to the internal registers of an A2B chip via diagnostic commands.

### 370 — Response cycle calculation
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- The response time for a frame from Master to last slave and back again shall be calculated to guarantee the timing requirement.
- [A2B-DL-1] A response cycle calculation shall be performed in the Audio Channel Plan for the master and for each slave.

### 371 — SWDL the A2B configuration
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- To require that the A2B configuration parameters shall be possible to download to the ECU.
- REQPROD 432016, 432020 and 432021 The A2B configuration parameters shall be possible to download to the ECU as a Local configuration and a Car Configuration file.4.3.1.1.2 A2B Data Link Layer - General Requirements4.3.1.1.2.1 Node Discovery

### 372 — Master node PLL
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- Host initialization of A2B Master [A2B-DL-10] When the Host starts the A2B Master transceiver, the Host shall provide master clock to let the transceiver lock its PLL on this frequency.
- The master transceiver generates an interrupt when its PLL has locked and this interrupt must be detected by the Host.
- The Host shall set a DTC for absence of A2B PLL lock if no interrupt are received within 25ms.

### 373 — Response cycle parameter programming
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- [A2B-DL-1] The Host shall set the response cycle parameter values on the master and on each slave with the values calculated in the audio channel plan.

### 374 — Slave discovery and initialization
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- [A2B-DL-11] The Host shall after the Master has started carry out a node discovery and initialize all nodes present on the bus with the A2B node configuration from the Local Configuration.

### 375 — Slave discovery timeout
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- [A2B-DL-10] The slave discovery timeout for each slave shall be less than 50 ms.

### 376 — Data Rate
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- The audio channel plan may specify that an audio channel has an Increased Data Rate.

### 377 — PDM Compatibility
- 版本：v1 ｜ 验证方式：- ｜ 适用：通用
- To define the compatible TDM mode when PDM is selected as an input format. [A2B-DL-10]Verification Method: A transceiver using a PDM input port are only allowed to use TDM2 on all other ports.

### 378 — Preferred TDM modes
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- To define available TDM modes. [A2B-DL-10] and [A2B-DL-11] Preferred TDM modes are TDM2, TDM4, TDM8, TDM16 and TDM32. Note 1: A transceiver uses same TDM-mode on all ports.

### 379 — Reduced mode
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- To require that reduced mode is not allowed and the reason is that it's not fully specified. [A2B-DL-11] Reduced mode is not allowed to be used. This mode is disabled when the REDUCE bit is equal to 0.

### 380 — Stream slot size
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- [A2B-DL-10] and [A2B-DL-11] The default slot size on up- respective down-stream shall be 24 bits.

### 381 — TDM channel size
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- [A2B-DL-10] and [A2B-DL-11] The default TDM channel size shall be 32 bits.

### 382 — Critical fault reset
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- [A2B-DL-11] The host shall not try to reconnect a bus where a critical fault has occurred until restart conditions has been met.

### 383 — Critical fault shutdown
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- If a critical fault are detected, the bus shall be shut down.
- [A2B-DL-11] If a critical fault (See Note 1) occurs the bus shall be shut down, the host shall clear the master transceivers A2B_SWCTL.

### 384 — ENSW-bit clearing
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- The ENSW-bit shall be cleared in last non-affected node in case of line fault.
- [A2B-DL-11] If a line fault has opened the bias switch (power feed to next bus segment) the host software shall clear the A2B_SWCTL.

### 385 — Non critical fault restart
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- The A2B shall restart after a non-critical fault.
- [A2B-DL-11] When a non-critical fault (See [A2B-DL-1]) has occurred the host shall re-do node discovery to determine the localization of the fault (as specified in the [A2B-DL-10]).
- The host shall then initialize all discovered non-faulty nodes to create a partially working A2B system.

### 386 — Bit error counter threshold
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- REQPROD 432016, [A2B-DL-10] and [A2B-DL-11] The bit error counter threshold value shall be set to 8, unless otherwise specified.
- The bit error counter threshold shall be stored in the Local Configuration.

### 387 — Bit error detection on control data
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Define which bit error types that shall be detected.
- [A2B-DL-11] The following transmission errors shall be detected and a DTC shall be set by the host: CRC error in the interrupt response frame, header count error & missed synchronization response frame.

### 388 — Bit error detection on payload
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Define which bit error types that shall be detected [A2B-DL-11] The following transmission errors shall be detected and a DTC shall be set in each slave with the bit error count register: CRC error in a control or response frame, Data decoding errors& streaming data parity error.

### 389 — External interrupts
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- [A2B-DL-10] and [A2B-DL-11] The master node shall have the capability to catch an external interrupt (i.
- The purpose of this interrupt shall be defined for each A2B project.

### 390 — I2C access errors
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- [A2B-DL-10] and [A2B-DL-11] An I2C access error on a device outside the transceiver on a slave shall be detected by the host and a DTC shall be set.
- The action of this error shall be defined for each slave that uses I2C outside the transceiver.
- If I2C access error occurs on internal communication to an A2B slave transceiver, the host shall try again two times.

### 392 — Standards for CAN interface
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- The interface shall be specified according to CAN standard using bit rate specified in section Network Transmission Speed 500 kbps.

### 393 — The priority between standard documents and this document
- 版本：v4 ｜ 验证方式：Analysis ｜ 适用：通用
- In case of discrepancy between the standard documents and this specification, this specification has precedence.4.3.2.1.1.1 ECU LevelThe power supply voltage level at the node shall be measured continuously.
- HW and SW inaccuracy in the monitoring of the supply voltage level must be taken into account when the ECU is designed.
- The ECU must meet this operating voltage range requirement also in a worst case condition.

### 394 — Communication protocol
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- Specification of CAN protocol used N. A. Controller Area Network (CAN) in accordance with CAN V2.0 [Ext CAN DL 2] .

### 395 — Behaviour outside normal supply voltage range
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- Hysteresis shall be used to ensure stable behaviour under low and high supply voltage conditions.
- Hysteresis shall be minimum 100mV.

### 396 — CAN bus level during reset
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- Modules shall not drive the CAN bus dominant during module reset.

### 397 — Bus fault reporting
- 版本：v4 ｜ 验证方式：Analysis ｜ 适用：通用
- At least one module on each bus must be able to detect and report faults on the physical bus.

### 398 — Bit time set up for 500 kbps
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- For a maximum transmission speed tolerance of ± 0.4%, the bit time set up for nodes shall be: BIT NtQ tSJWminNum tQ tSEG2minNum tQ tSEG2maxNum tQ Sample point % SJWmin% 22 3 3 5 77 – 86 13.6 21 3 3 5 76 – 86 14.3 20 3 3 5 75 – 85 15.0 19 3 3 4 79 – 84 15.8 18 2 2 4 78 – 89 11.1 17 2 2 4 76 – 88 11.8 16 2 2 3 81 – 88 12.5 15 2 2 3 80 – 87 13.3 14 2 2 3 79 – 86 14.3 13 2 2 2 85 15.4 12 2 2 2 83 16.7 11 2 2 2 82 18.2 10 2 2 2 80 20.0 Note 1: Calculation of the Tseg1 valueNTq = Sync_Seg + Prop_Seg + Phase_Seg1 + Phase_Seg2, see [Ext CAN DL 3]Sync_Seg = 1Tseg1 = Prop_Seg + Phase_Seg1Tseg2 = Phase_Seg2Note 2: to achieve 10 or more tQ at 500kbps, the input clock to the CAN controller must have a minimum frequency of 5MHz.
- ## 4.3.2.1.1.1.4 CAN FD bit register settings for 2 Mbps Support CAN FD with 2 Mbps data rate Legacy ID: One of the following standardized bit rate settings shall be used.
- The SWRS possibly supplemented with referenced documents shall be used as the basis for design and qualification testing of the software product.

### 399 — Resynchronisation strategy
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- Increase communication robustness N. A. Resynchronisation on recessive to dominant transitions only.

### 400 — Sample mode
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- Only single sample mode shall be used.4.3.2.1.1.1.2 Speed tolerance definition

### 401 — PLL bypass
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- If a PLL is being used by, and if supported by the chosen microcontroller, the CAN physical layer shall be clocked directly from the base oscillator, i.

### 402 — PLL locking
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- Minimise the number of communication error events N. A. When a PLL is being used to clock the CAN physical layer, transmission and reception are only allowed when the PLL is locked.4.3.2.1.1.1.3 Network Transmission Speed - 500kbps

### 403 — ECU Conformance
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- ETH DL 16 The ECU shall prove conformance to 100BASE-T1 by passing all layer 2 test cases in [ETH DL 16].
- The test suites shall be performed by an external test house approved by the base technology team (PSS333).
- All test results must be provided and will be kept confidential.

### 404 — Link Establishment Time
- 版本：v5 ｜ 验证方式：Test ｜ 适用：通用
- Not available The time to establish a link shall be less than 100 msec.

### 405 — Link speed and duplex
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- In order to optimize the startup time Auto negotiation shall not be used.
- ETH DL 4 The link speed and duplex for each port that is connected to an internal or external PHY shall be set according to [ETH DL 4].

### 406 — MTU
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The default MTU size of Ethernet packets shall be set to 1500 bytes.
- MTU size shall be configurable.

### 407 — Multicast support
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- ETH DL 4 Multicast addresses shall be supported on the data link layer.
- The multicast addresses that shall be supported are found in [ETH DL 4].

### 408 — Register read out using Diagnostics
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- ETH DL 1 It shall be possible to read all registers using diagnostics according to [ETH DL 1].
- It shall be possible to read one register at a time.

### 409 — Register write using Diagnostics
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- ETH DL 1 All registers that can be modified in a chip set, shall be possible to set using diagnostics according to [ETH DL 1].

### 410 — Internal MAC Addresses
- 版本：v11 ｜ 验证方式：Test ｜ 适用：通用
- ETH DL 4 The internal MAC address shall be configurable.

### 411 — External MAC Addresses
- 版本：v5 ｜ 验证方式：Analysis ｜ 适用：通用
- N/A MAC addresses of interfaces reachable from external networks shall be universally administered.

### 412 — VLAN (IEEE 802.1Q)
- 版本：v5 ｜ 验证方式：Analysis ｜ 适用：通用
- ETH DL 12, REQPROD 359596 Virtual Local Area Network, VLAN shall be implemented according to [IEEE 802.1Q-2012] and REQPROD 359596.

### 413 — VLAN Identifier (VID)
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- ETH DL 12 ECUs shall support configuration with the full range of possible VLAN identifiers, except for the reserved VIDs stated in [Table 9-2—Reserved VID values, ETH DL 12].

### 414 — VLAN Priority
- 版本：v7 ｜ 验证方式：Test ｜ 适用：通用
- ETH DL 11, ETH DL 12 The VLAN priority bits (PCP) in the VLAN tag [ETH DL 12], shall be set according to traffic types and prioritization in [ETH DL 11].
- The priority bits shall be configurable.

### 415 — Drop Eligible Indicator, DEI
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- ETH DL 11 The Drop Eligible Indicator, DEI-flag shall be supported and configurable per VID.

### 416 — VLAN configuration
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- LC: Diagnostics and ECU Platform REQPROD 359541, REQPROD 54977,REQPROD 359419 For VLANs, the following parameters shall be configurable per VLAN interface: VLAN ID, VIDPriority, PCPDrop Eligible Indicator, DEI

### 417 — Discard Untagged Frames
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- N/A The ECU shall support per-interface discarding of Ethernet frames, which are not VLAN-tagged.
- Rules shall be configurable.4.3.4 FlexRay Data Link Layer4.3.4.1 FlexRay Data Link Layer4.3.4.1.1 Data Link Layer RequirementsThis chapter defines the values of the FlexRay parameters.

### 452 — NetworkStatus Parameter
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- - The NetworkStatus parameter shall be two bytes long and shall be sent by the FlexRay Schedule Coordinator in the first slot of the static segment in all cycles and for all schedules.
- The byte order on the bus is: the most significant shall be transmitted first and then the least significant byte.

### 453 — Definition of the NetworkStatus Parameter
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- - The values of the NetworkStatus parameter shall be implemented as defined in the table NetworkStatus parameter values and the figure Location of the Network Status Parameter.

### 454 — Transmit the NetworkStatus Parameter
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- To define which node is responsible to transmit the NetworkStatus parameter. - The FlexRay Schedule Coordinator is responsible to transmit the NetworkStatus parameter in every cycle. To define which node is the FlexRay Schedule Coordinator is project specific 

### 455 — FlexRay NetworkStatus is not received
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- To define the behaviour when a FlexRay ECU doesn't receive the NetworkStatus from the FlexRay Schedule Coordinator - If a node doesn't receive the FlexRay NetworkStatus shall the node start or continue to run the application software.
- The application signals shall be received and the transmitted frames shall contain valid data.

### 456 — NetworkStatus parameter - Fault conditions
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- A node shall always listen on the NetworkStatus parameter (signal FRNetworkStatus) to be able to recover from a fault condition and start communicate again when the status is changed to Normal, Boot or Undefined.
- The frame containing the NetworkStatus must be a valid non-null frame received without errors for any further evaluation of NetworkStatus.
- To make this possible must the schedules have common slots in the static segment and the payload must be the same.

### 458 — Sync frames in the Common Static Segment
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- To define where the sync frames shall be allocated.
- - All sync nodes must be placed in the common static segment.
- FlexRay Schedule Coordinator A FlexRay node that is responsible for coordinating the schedule that shall be present on its network.

### 459 — FlexRay Protocol Version
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- All requirements defined in specification FlexRay Communication System Protocol Specification, FlexRay Data Link Layer – External publications, must be fulfilled.

### 460 — Document precedence
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- To require precedence for this specification. - In case of discrepancy between the standard documents and this specification, this specification has precedence.

### 461 — Bit Rate
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- The Bit Rate of the FlexRay network or networks shall be 10 Mbit/s.

### 462 — Protocol related global cluster parameters
- 版本：v6 ｜ 验证方式：Test ｜ 适用：通用
- The protocol related global cluster parameters shall be implemented as defined in the table below.
- 1 - 6 us gdMaxInitializationError 1,7 μs Maximum timing error that a node may have following integration.

### 463 — Protocol relevant global cluster parameters
- 版本：v5 ｜ 验证方式：Test ｜ 适用：通用
- The protocol relevant global cluster parameters shall be implemented as defined in the table below.
- c gSyncNodeMax 8 Maximum number of nodes that may send frames with the sync frame indicator bit set to one.

### 464 — Application Schedule 1
- 版本：v6 ｜ 验证方式：Test ｜ 适用：通用
- All other parameters values shall be set according to the tables found in sections Protocol relevant global cluster parameters, Protocol related global cluster parameters, Protocol relevant node parameters and Protocol related node parameters.
- The unique global cluster parameters for Application Schedule 1 shall be implemented as defined in the table below.
- pSingleSlotEnabled False Boolean Flag indicating whether or not the node shall enter single slot mode following startup.

### 465 — Bootloader Schedule 1
- 版本：v7 ｜ 验证方式：Analysis ｜ 适用：通用
- All other parameters values shall be set according to the tables found in sectionsProtocol relevant global cluster parameters, Protocol related global cluster parameters, Protocol relevant node parameters and Protocol related node parameters.
- The unique global cluster parameters for bootloader schedule 1 shall be implemented as defined in the table below.
- pSingleSlotEnabled True Boolean Flag indicating whether or not the node shall enter single slot mode following startup.

### 466 — Protocol related node parameters
- 版本：v5 ｜ 验证方式：Analysis ｜ 适用：通用
- The protocol related node parameters shall be implemented as defined in the table below.
- Number of microticks per nominal (Default value 40) macrotick that all implementations must support.

### 467 — Protocol relevant node parameters
- 版本：v8 ｜ 验证方式：Analysis ｜ 适用：通用
- The protocol relevant node parameters shall be implemented as defined in the table below.
- pAllowPassiveToActive 2 Even/odd Cycle pairs Number of consecutive even/odd cycle pairs that must have valid clock correction terms before the CC will be allowed to transition from the POC: normal passive state to POC: normal active state.
- If pKeySlotUsedForStartup is set to true then pKeySlotUsedForSync must also be set to true.

### 468 — The priority between standard documents and this specification
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- In case of discrepancy between the standard documents and this specification, this specification has precedence.

### 469 — Node conformance test
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- The node must demonstrate conformance to the applicable tests defined in one of the comformance tests in table below.

### 470 — Bus speed
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- All modules shall be capable of operating at the nominal bus speeds of 9.6kbps or 19.2kbps.
- The operating speed shall be defined on a bus by bus basis.

### 471 — Application timing requirements
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- The node application must be designed according to functional timing requirements, not according to the timing properties of a specific LIN bus implementation (i.

### 472 — LIN signal frames may appear arbitrarily
- 版本：v4 ｜ 验证方式：Analysis ｜ 适用：通用
- The node must not assume that headers in the range 0x00 to 0x3B appear in a specific relative order.

### 473 — Format of the part number data record
- 版本：v5 ｜ 验证方式：Test ｜ 适用：通用
- When a part number for a LIN slave is to be transmitted from the slave to the master node, the format of the data shall be as follows: Part number data records used by Volvo Cars shall have 8 digits for part number + 3 characters (version suffix).
- Part number data records used by Geely shall have 10 digits for part number + 3 characters (version suffix).
- The part number digits shall be coded in BCD and the 3 characters (version suffix) shall be coded in ASCII, right justified, with any unused digit filled with 0H.

### 474 — Format of the serial number
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- When a serial number for a LIN slave is to be transmitted from the slave to the master node, the format of the data shall be as follows (see [LIN_DL_2] LIN Specification Package Revision 2.1):8 digits for serial number.

### 475 — PLL used as clock
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- When a PLL is being used to clock the LIN interface, transmission and reception are only allowed when the PLL is locked.4.3.6.1.1.1 Wake-Up timing

### 476 — Wakeup strategy
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- All nodes shall follow the strategy specified in [LIN_DL_2] LIN Specification Package Revision 2.1.
- LIN slaves designed according to LIN 1.3 Standard may follow the wake up strategy specified in [LIN_DL_1] LIN Specification Revision 1.3.

### 477 — Communication persistency
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- A short or open in any single wiring circuit of an ECU, except for power, ground, or serial data, shall not preclude the ability to communicate with that ECU for diagnostic purposes.

### 478 — ECU Power Loss
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- ECUs shall not interfere with normal communication among the remaining bus ECUs during a loss of power (or low voltage) condition.
- Upon return of power, normal operation shall resume without any operator intervention within a time determined by the vehicle manufacturer.

### 479 — Recovery from Bus short to battery
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- Upon removal of a bus short to battery voltage, normal operation shall resume without any operator intervention within 1 second.

### 480 — Recovery from Bus short to ground
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- Upon removal of a bus short to ground, normal operation shall resume without any operator intervention within 1 second.

### 481 — Recovery from reset
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- Following a reset the node must enter into a predefined state, defined in a ECU specific design document.4.3.6.1.1.3 Operating Battery Power Voltage RangeThe power supply voltage level at the node shall be measured continuously.
- HW and SW inaccuracy in the monitoring of the supply voltage level must be taken into account when the ECU is designed.
- The ECU must meet this operating voltage range requirement also in a worst case condition.

### 482 — Normal battery voltage power operation
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- The node shall communicate on the network when the node voltage supply is 8,0 – 16,0 Volt.

### 483 — Low Battery Voltage Operation
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- For 0 < Vbatt ECU < 8.0 volts the bus may operate in either the normal or the passive mode.
- In the Passive Mode the bus shall be recessive (not be pulled or driven to ground) and TxD shall be in the high state.
- Fault codes shall be suppressed below 10 volts.

### 484 — Operating voltage range hysteresis
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- Hysteresis shall be minimum 100mV.
- Hysteresis shall be used to ensure stable behaviour in low and high supply voltage conditions,see figure in section "Operating Battery Power Voltage Range".
- Reference Dokument [LIN_DL_1] LIN Specification Revision 1.3 [LIN_DL_2] LIN Specification Package Revision 2.1 [LIN_DL_3] LIN 1.3 Conformance test [LIN_DL_4] LIN 2.1 Conformance test 4.3.6.1.3 Definitions and Abbreviations For multiplex terminology, SAE J1213/1 JUN91 "Glossary of Vehicle Networks for Multiplexing and Data Communications" shall be used in applicable cases for documentation.

### 485 — LIN standard used in master node
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- The master for each network shall support the required LIN standards for each slave connected to the network in accordance with [ LIN_DL_1] LIN Specification Revision 1.3 or [ LIN_DL_2] LIN Specification Package Revision 2.1.486 v3 Header jitter The transmission of headers must follow the time schedule given by the schedule table.
- The worst case jitter and the T Header Maximum must be calculated by the supplier of the master ECU and reported to the OEM design team responsible for the ECU.
- The worst case jitter must not exceed 1 ms.

### 487 — Suppressed DTCs
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- Above 16 volts the master node shall not set DTCs due to slave nodes not responding.4.3.6.2.2 Master Wake-Up Timing

### 488 — Timeout and sleep commands
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The master shall always issue a sleep command when power down of the bus is required,[LIN_DL_2] LIN Specification Package Revision 2.1.

### 489 — Local event - master sends the first header
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- A master node shall transmit the first header within 100 ms after a local event.

### 490 — Network event - wake up request to first header
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The LIN master shall detect and begin transmission of the first header of the appropriate schedule table no longer than 130ms after the wake up request.

### 491 — Power on - master sends the first header
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- A master node shall be able to transmit the first header within 250 ms after power is applied or after a hardware reset.

### 492 — Network event - wake up request to slave ready to communicate
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The LIN slave node shall detect the wake up request and be able to transmit valid data within 100ms.
- Slaves shall not respond until their data is valid.
- Diagnostic supervision in the master shall take this delay into account.

### 493 — Power on - slave sends the first response
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- A slave node shall be able to transmit valid data within 100 ms after power is applied or after a hardware reset.
- Slaves shall not respond until their data is valid.
- Diagnostic supervision in the master shall take this delay into account.

### 1025 — Bidirectional Control Channel on four-wire LVDS with Ethernet
- 版本：v2 ｜ 验证方式：- ｜ 适用：通用
- DPR-LVDS-NETWORK-005: Req5v1Verification Method: Demonstration The control channel shall support bidirectional transfer of data.
- The type and speed of transfer shall be software configurable, and can be either I2C (400 kbps) or SPI (400 kbps - 1 Mbps).
- The SPI mode for external access on the remote side shall only be active if the Ethernet MII mode is disabled.

### 1026 — Bidirectional Control Channel on one-wire LVDS
- 版本：v1 ｜ 验证方式：- ｜ 适用：通用
- DPR-LVDS-NETWORK-005: Req4v1, [LVDS_Netw:6]Verification Method: Demonstration The control channel shall support bidirectional transfer of data.
- The type and speed of transfer shall be I2C High speed mode (400 kbps).
- The types of data to be exchanged shall include event-driven application data, diagnostics data validation of link quality, remote-side configuration data and software download.

### 1027 — Bidirectional Control Channel on two-wire LVDS
- 版本：v3 ｜ 验证方式：- ｜ 适用：通用
- DPR-LVDS-NETWORK-005: Req4v1, [LVDS_Netw:6]Verification Method: Demonstration The control channel shall support bidirectional transfer of data.
- The type and speed of transfer shall be software configurable, and can be either I2C (400 kbps) or UART (400 kbps - 1 Mbps).
- The types of data to be exchanged shall include event-driven application data, diagnostics data validation of link quality, remote-side configuration data and software download.

### 1028 — Bidirectional High-Speed Control Channel on four-wire LVDS with Ethernet
- 版本：v2 ｜ 验证方式：- ｜ 适用：通用
- DPR-LVDS-NETWORK-005Req6v1Verification Method: Demonstration The high-speed control channel shall support bidirectional transfer of data.
- The type and speed of transfer shall be software configurable.
- The Ethernet MII mode will need to disable the external SPI interface on the remote side, but the I2C master shall still be allowed to use.

### 1029 — Bit error rate
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- The selection of 32 bits shall be used if 32 bits (40 bits 8b10b encoded) link format is used.

### 1030 — Deserializer Robustness against Bit Errors Four-Wire LVDS with Ethernet
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- DPR-LVDS-NETWORK-005: Req3v1 + Analysis The deserializer shall be able to handle a length of a burst due to bit errors of up to three pixelswithin each video source.
- The burst must not cause any column displacements of the pixelscomprising a line;
- it must not corrupt the video timing generator on the receiving side;

### 1031 — Deserializer Robustness against Bit Errors Two-Wire LVDS
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- DPR-LVDS-NETWORK-005: Req2v1 + Analysis The deserializer shall be able to handle a length of a burst due to bit errors of up to three pixels.
- The burst must not cause any column displacements of the pixels comprising a line.
- Implementation: Deserializer side, two-wire LVDSQualification method: Analysis, documentation of test results.4.3.7.4.3.2 Power Supply and ResetThe power supply voltage level at the node shall be measured continuously.

### 1032 — Battery voltage above normal operating range
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- To guarantee deterministic behavior of the LVDS Link, it is desired that: above normal operating range, the Serializer shall determine the state of the link, i.
- + Analysis The LVDS network shall only be fully functional over an operating range of 8 to 16 volts, above normal range the ECU shall detect and can possible disrupt the transmission.
- The same disruption shall be during partial or complete ECU startup, shutdown, reset, brownout or comparable events.

### 1033 — Communication voltage range
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- To require the ECU to not disturb the LVDS link, neither video nor control channel, shall operate outside the operating voltage range.
- + Analysis The LVDS network shall be fully functional over an operating range of 8 to 16 volts.
- ECUs shall not interfere with the LVDS link, or disrupt the transmission of the other ECU outside of its specified voltage operating range, during partial or complete ECU startup, shutdown, reset, brownout or comparable events.

### 1034 — ECU Power Loss
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- LVDS link ECUs shall not interfere with normal communication during a loss of power (or low voltage) condition.
- + Analysis LVDS link ECUs shall not interfere with normal communication during a loss of power (or low voltage) condition.
- Upon return of power, normal operation shall resume without any operator intervention within a time determined by the vehicle manufacturer.

### 1035 — Low Battery Voltage Operation
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- For 0 < Vbatt ECU < 8.0 volts the LVDS link may operate in either the normal or be disabled.
- + Analysis For 0 < Vbatt ECU < 8.0 volts the LVDS link may operate in either the normal or be disabled.
- LVDS Control channel fault codes shall be suppressed below 8 volts.

### 1036 — Recovery from reset
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The LVDS link ECUs shall following a reset of the node enter, into a predefined state.
- + Analysis LVDS link ECUs shall following a reset of the node enter, into a predefined state, defined in a design document for the node.
- Upon return of Reset mode, normal operation shall resume without any operator intervention within a time determined by the vehicle manufacturer.

### 1037 — ECU Internal Data Propagation Delay (1wire)
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- + Analysis The internal propagation delay, measured between controller input/output and ECU connector, shall not exceed measures below: For I 2C control channel modes, the latency shall be less than 250 us.

### 1038 — ECU Internal Data Propagation Delay (2wire)
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- For data traffic the gateway delay shall be measured by the serialization time of 10 bytes + Analysis The internal propagation delay, measured between controller input/output and ECU connector, shall not exceed measures below: For SPI/I2C and UART control channel modes, the latency shall be less than the serialization time for 10 bytes messages.

### 1039 — ECU Internal Data Propagation Delay (4wire)
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- For data traffic the gateway delay shall be measured by the serialization time of 10 bytes, for fast ethernet maximum of the serialization time of 256 bytes + Analysis The internal propagation delay, measured between controller input/output and ECU connector, shall not exceed measures below: For full duplex 100Mbps Ethernet data traffic the gateway latency shall be less than 25 microseconds.
- (100Mbps Ethernet and max 1000 bytes/packets)To enable full duplex 100Mbps Ethernet two way traffic response, when ECU act as ethernet repeater, the Round-Trip Propagation Delay shall be less than 140 (in Bit Times).
- If ECU act as a transparent cable, the Round-Trip delay shall be less that 11.1 (Bit Times), 1/10th of maximum cable segment length (111.2 (Bit Times) = 100 Meters cable), and shall allow upto 5 units and 50 meters of cable in series in the Ethernet network.

### 1040 — ECU Internal Video Propagation Delay
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- DPR-LVDS-NETWORK-005: Req9v1 + Analysis The internal propagation delay, measured between controller input/output and ECU connector, shall not exceed measures below: If LVDS links transfer video traffic, maximum three (3) video frames (corresponding to 100 ms at 30 fps) are allowed, when rescale, rotate, resample, coding/decoding of video frame are performed otherwise maximum two video frames.

### 1041 — LVDS Single Chipset
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- To secure compatibility of LVDS communication, both Serilizer and Deserializer must belong to compatible chipset family.
- REQPROD 344966, REQPROD 344559 All LVDS serializers and deserializers in the LVDS network shall belong to the same chipset family of compatible chips.
- If compatible chipset is used, Tier1 must make sure that all SW access to physical level functionality, as well as the SW accessibility of the companion side is supported.

### 1042 — Node to node start up time
- 版本：v2 ｜ 验证方式：- ｜ 适用：通用
- To enable full video streaming, no more than another thirteen (13) video frames (corresponding to 433 ms at 30 fps) shall be allowed.
- Implementation: AllQualification method: Demonstration.4.3.7.4.4 Qualifications MethodsEvery requirement in this document shall be verified according to at least one established qualification method.
- Tests shall be performed to verify the compliance, and the tests shall be included in a test plan.

### 1043 — By-Pass Latency
- 版本：v3 ｜ 验证方式：- ｜ 适用：通用
- Verification Method: Demonstration The gateway shall allow a live video image on the sinks display after maximum three (3) video frames latency.

### 1044 — By-Pass Mode
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- Traffic through the gateway shall be able to transfer video direct after startup, according to startup requirements.
- If not possible to fulfill normal video within six (6) video frames latency, a By-Pass mode shall be provided, until the ECU is completely booted.
- The by-pass mode shall be able to produce a video stream that follows the VESA video timing definition of all the supported sinks.

### 1045 — By-Pass Start Up Time
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- + Analysis If an By-Pass mode is needed at the gateway, the video traffic shall be up and running within six (6) video frames latency.

### 1046 — Pixel Queue
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- + Analysis If a link has more than one source, then the pixels of each source shall be placed in a queue.
- For four-wire LVDS the selected transceiver and receiver can have HW supported video streams interleaving, in that case the preferred solution shall use the multiple HW implementations of the line- or frame-sync bits.
- However at any time, the transceiver/ receiver manufacture requirements for the line- or frame-sync must be fulfilled.

### 1047 — Pixel Queue Delay
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- + Analysis If a link has more than one source, then the pixels of each source shall be placed in a queue.
- For four-wire LVDS the selected transceiver and receiver can achieve HW supported video streams interleaving, in that case the preferred solution shall use the multiple HW implementations of the line- or frame-sync bits.
- However at any time, the transceiver/ receiver manufacture requirements for the line- or frame-sync must be fulfilled.

### 1048 — The priority between standard documents and this specification
- 版本：v1 ｜ 验证方式：- ｜ 适用：通用
- LIN signal frames may appear arbitrarily Ref requirement tag: REQPROD 53562/-;1 REQPROD 390940/0;

### 1049 — LVDS support of LIN Go to Sleep HANDLING
- 版本：v1 ｜ 验证方式：- ｜ 适用：通用
- The slave node application may still be active after the go to sleep command has been received.
- The slave nodes shall ignore the data fields 2 to 8 and interpret only the first data field.

### 1050 — Ability to disregard other headers and frames
- 版本：v1 ｜ 验证方式：- ｜ 适用：通用
- Verification Method: The node shall respond to each header that is issued by the master, header that it is not programmed to handle and incorrect headers or frames on the bus, shall be acknowledge with an error response, to avoid blockage or starvation of the message buffers in the Master.
- The node shall only respond with non error acknowledge to each header that it is programmed to handle.

### 1051 — Number of nodes in a network
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The maximum node count for any given network shall consist of 1 Master and 1 Slave.

### 1052 — Startup, Establish Normal LVDS communication
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- 2 Enables configuration link, may be set automatic.

### 1053 — Timeout and sleep commands
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- All slaves must implement both the timeout and sleep command,(LVDS deviations applies of LIN Specification Package Revision 2.1, LIN Datalink Layer - Requisite documents.)4.3.7.4.1.4.1.3 Requirement of UART or I2C communication via LVDS

### 1054 — Communication Speed
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Define the setting of communication speed between Master ECU and Slave ECU via LVDS. Communication Speed: 416kbps (±5%)The communication speed is set through configuration of the Serializer. Remark: The Serializer can both be the Master ECU or the Slave ECU. E

### 1055 — Communications protocol
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Define interface protocol which communicates between Master ECU and Slave ECU via LVDS. The Master ECU is normally the originator of the communication to Slave ECU by UART/I2C Protocol. Once handed over, the Slave ECU communicate by UART/I2C Protocol towards M

### 1056 — Device address
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Define device addresses on UART/I2C communication between Master ECU and Slave ECU via LVDS. I2C register addresses Ref [LVDS_GMSL:2] Device Serializer Read Serializer Write Deserializer Read Deserializer Write Maxim9259(Serializer) 0x81 (local address) 0x80 (

### 1057 — Master and slave configuration
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Master ECU shall be Master and Slave ECU shall be Slave.

### 1058 — Mode setting of transceiver device
- 版本：v1 ｜ 验证方式：- ｜ 适用：通用
- Define control mode in interface device(s). Verification Method: Deserializer and Serializer are set with Base Mode of control mode in each device.

### 1059 — Node address of Slave ECU for SWDL
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Master ECU converts Functional Address and Node Address to Device address on LVDS communication if needed – the Master shall route regardless of Node Address, as the Slave ECU is the only device that shall be connected to the Master ECU, per LVDS network.

### 1060 — UART characteristics
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- 1060 v1UART characteristics UART characteristics shall be according to LIN Specification Package Revision 2.1, LIN Physical Layer – Requisite documents, with nominal bus speeds of 9.6kbps or 19.2kbps.
- As a deviation from LIN standard above, the UART shall also support a high speed mode at 400 Kbps.

### 1061 — Ability to read every frame instance
- 版本：v1 ｜ 验证方式：- ｜ 适用：通用
- 1061 v1Ability to read every frame instance Verification Method: When the node is active on the bus it must not fail to read frames and to identify and respond to headers on the bus, regardless of any competing internal processes.

### 1062 — Application timing requirements
- 版本：v1 ｜ 验证方式：- ｜ 适用：通用
- Verification Method: The node application must be designed according to functional timing requirements, not according to the timing properties of a specific LIN bus implementation (i.
- The high speed mode, at the full Bus speed, needs to be taken into account – virtual bus speed shall be retimed.
- ldf-file or similar) the timing properties shall be recalculated to meet functional timing.

### 1063 — Bus speed
- 版本：v1 ｜ 验证方式：- ｜ 适用：通用
- Verification Method: All modules shall be capable of operating at the nominal bus speeds of 9.6kbps or 19.2kbps, forbackward compatibility.
- The operating speed shall be defined on a bus by bus basis.
- The bus speed shall be less than 416 kbps in high speed mode, but the virtual bus speed shall be possible to limit to 19.2kbps.

### 1064 — Format of the part number data record
- 版本：v1 ｜ 验证方式：- ｜ 适用：通用
- Verification Method: When a part number for a LIN slave is to be transmitted from the slave to the master node, the format of the data shall be as follows: Part number data records used by VCC shall have 8 digits for part number + 3 characters (version suffix).
- Part number data records used by Geely shall have 10 digits for part number + 3 characters (version suffix).
- The part number digits shall be coded in BCD and the 3 characters (version suffix) shall be coded in ASCII, right justified, with any unused digit filled with 0H.

### 1065 — Format of the serial number
- 版本：v1 ｜ 验证方式：- ｜ 适用：通用
- Verification Method: When a serial number for a LIN slave is to be transmitted from the slave to the master node, the format of the data shall be as follows (see LIN Specification Package Revision 2.1, LIN Datalink Layer - Requisite documents):8 digits for serial number.

### 1066 — LIN signal frames may appear arbitrarily
- 版本：v1 ｜ 验证方式：- ｜ 适用：通用
- Verification Method: The node must not assume that headers in the range 0x00 to 0x3B appear in a specific relative order.

### 1067 — Wakeup strategy
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- All nodes shall follow the strategy specified in LIN Specification Package Revision 2.1, LIN Datalink Layer – Requisite documents.

### 1068 — Header jitter
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The transmission of headers must follow the time schedule given by the schedule table.
- The worst case jitter and the THader_Maximum must be calculated by the supplier of the master ECU and reported to the OEM design team responsible for the ECU.
- The worst case jitter must not exceed 1 ms.

### 1069 — Local event - master sends the first header
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- A master node shall transmit the first header within 100 ms after a local event.

### 1070 — Network event - wake up request to slave ready to communicate
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The LIN slave node shall detect the wake up request and be able to transmit valid data within 100ms.
- Slaves shall not respond until their data is valid.
- Diagnostic supervision in the master shall take this delay into account.

### 1071 — Power on - master sends the first header
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- A master node shall be able to transmit the first header within 250 ms after power is applied or after a hardware reset.
- The LVDS link PLL shall be locked within 100 ms under conditions above, otherwise the master node shall be able to transmit the first header within 150 ms after LVDS link PLL is locked.

### 1072 — Power on - slave sends the first response
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- A slave node shall be able to transmit valid data within 100 ms after power is applied or after a hardware reset.
- Slaves shall not respond until their data is valid.
- The LVDS link PLL shall be locked within 100 ms under conditions above, otherwise the master node shall be able to able to transmit the first header within 150 ms after LVDS link PLL is locked.

### 1073 — Timeout and sleep commands
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The master shall always issue a sleep command when power down of the bus is required, LIN Specification Package Revision 2.1, LIN Datalink Layer - Requisite documents.4.3.7.4.1.4.4 LIN Datalink Layer compatibility - SW Slave reqs

### 1074 — Timeout and sleep commands
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- All slaves must implement both the timeout and sleep command, LIN Specification Package Revision 2.1, LIN Datalink Layer - Requisite documents.

### 1075 — Transmission time
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The true T Response Maximum value, in which a node can complete its response, shall be stated in the free text section of the Node Capability File.
- ldf-file or equivalent) shall presume a value of T Response Maximum as defined in LIN Specification Package Revision 2.1, LIN Datalink Layer - Requisite documents.
- The high speed mode, at the full Bus speed, needs to be taken into account – virtual bus speed shall be retimed.

### 1076 — Node conformance test
- 版本：v1 ｜ 验证方式：- ｜ 适用：通用
- Verification Method: The node must demonstrate conformance to the applicable tests defined in one of the conformance tests in table below.
- Conformance test shall be replaced with LVDS Master/Slave Reference model, for incompatible subset and superset of the LIN 2.1 Standard.

### 1078 — Calculation of check-sum for communication message
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Define calculation object and method Page No344(1572) Object parameters: REG ADDR and all BYTE (). Calculation method: CRC32TYPE1SYNCDEV ADDR+WREG ADDRMSG ID)NUMBEROF BYTESBYTE1BYTE2... BYTEN-4CheckSum 1CheckSum 2CheckSum 3CheckSum 4ACK0x790x6C0x01N0x000x000x0

### 1079 — Communication format
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- 1079 v1Communication format Define message format on UART/I2C communication between Master ECUand Slave ECU via LVDS. SYNC:1 byte and fixed value as 0x79. DEV ADDR:1 byte and the value specified in Device address requirement. REG ADDR:1 byte and the value spec

### 1080 — Data restrictions of endianness
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Define data restrictions of endianness. Define to be used Big-endian for more than 2 bytes data in message. When Slave ECU receives request message data width out of range, Slave ECU send Ack but Slave ECU ignores the request message and Slave ECU keeps curren

### 1081 — Detail of message Diag Command Request Diag Command Response
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- 1081 v1Detail of message Diag Command Request Diag Command Response Define detail of the message on UART/I2C communication between MasterECU and Slave ECU via LVDS. Diag Command RequestMSG ID0x3CMSG NAMEDiag Command RequestMSG TYPEType1 Diag Command ResponseMS

### 1082 — Detail of message Interrupt Status Information
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Define detail of the message on UART/I2C communication between Master ECU and Slave ECU via LVDS. MSG ID 0x20 MSG NAME Interrupt Status Information MSG TYPE Type1 Message parameters Byte Bit Data Name Value Range Value Value Name Note 1 MsgDataType 0x00-0x03 0

### 1083 — Detail of message VehCfgPrm
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Define detail of the message on UART/I2C communication between Master ECU and Slave ECU via LVDS. MSG ID 0x09 MSG NAME VehCfgPcm MSG TYPE Type1 Message parameters Byte Bit Data Name Value Range Value Value Name Note 1 BlkIDBytePosn1 0-255 - - Block ID for spec

### 1084 — Event triggered signals heartbeat
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- To be able to detect lost signals All event triggered signals shall have a heartbeat, meaning that the signal shall be re-sent with 1 second intervals even if an event has not occurred (i.

### 1085 — Message flow of diagnostics between Diagnostic tester and Slave ECU
- 版本：v1 ｜ 验证方式：- ｜ 适用：通用
- TBD Page No352(1572) 3 Shall be cyclic only during first 30 seconds at the beginning of every driving cycle, and then not sent anymore.
- Period time shall be the same as incoming CC signal to Master ECU .

### 1087 — Remote Register access LVDS Slave ECU LVDS command
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- + Analysis Slave ECU LVDS Chipset registers shall access via Master ECU via the control channel over LVDS link.
- Access from Master ECU to remote Slave ECU register addresses shall only handle by Master ECU as local error management.
- Gateway accesses to Remote Slave ECU registers write access shall handle CRC error management, offloading the CRC from the message before perform the remote Slave ECU LVDS register access.

### 1088 — Sequence diagram Diagnostic
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- 1088 v1Sequence diagram Diagnostic Define Diagnostic message sequence of Master ECU and Slave ECU. The following shows P4Server setting and clear timing: Set: When Ack is returned to Diag CommandRequest((with SPRMIB parameter & SPRMIB = False) OR (without SPRM

### 1089 — Sequence diagram Startup and Normal communication
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- 1089 v1Sequence diagram Startup and Normal communication Define normal sequence of Master ECU and Slave ECU. In later revision of this document, there will be a sequence diagram showing behaviour of start-up, normal message communication, detection of user ope

### 1090 — Sequence diagram SWDL
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Define SWDL message sequence of Master ECU and Slave ECU. This sequence shows behaviour of SWDL message communication. TesterECU EAT program modePhysical/Functional RoutineControl(SPRMI=B=FALSE,start Routine, check programming pre-condition) Functional Diagnos

### 1091 — Time restrictions of message
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Define time restrictions of message. Define interval time between in each data byte. Less than 13.75 usec (1 byte/2) Message type1SYNCDEVADDR+WREGADDR(MSGID)NUMBEROFBYTESNBYTE1N... BYTEN-1CheckSumACKQLess than 13.75usec (1byte/2) Message type2SYNCDEVADDR+WREGA

### 1092 — HDCP Keep alive
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- In order to support secured transmissions over LVDS, HDCP shall be used.
- + Analysis In order to remain the HDCP communication, HDCP authentication and keep alive calls shall be used when DCP videos are possible to be transmitted over the LVDS link.
- However at any time, the transceiver/receiver supplier requirements for the HDCP format must be fulfilled.

### 1093 — HDCP setup HDCP Authentication Flowchart
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- In order to support secured transmissions over LVDS, HDCP Authentication flowchart shall be used.
- + Analysis In case of HDCP usage, the following setup shall be used : HDCP Authentication Flowchart HDCP Authentication Flow diagram: System pC Serializer Deserializer Time (μs) Comment Read Des Ri' 82 1 byte read.
- However at any time, the transceiver/receiver supplier requirements for the HDCP format must be fulfilled.

### 1094 — HDCP support
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- Blu-ray, then both the serializer and deserializer of the link shall have built-in HDCP-support.

### 1095 — State management of LVDS link(1wire)
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The Serializer shall be responsible to set up the control channel.
- The change of the selected method for utilize the control channel over the LVDS link shall be compliant to the below implementation.
- However at any time, the transceiver/receiver manufacturer requirements for the control channel implementation must be fulfilled.

### 1096 — State management of LVDS link(2wire)
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The Serializer shall be responsible to set up the control channel.
- The Control channel State management shall follow the scheme below.
- The change of the selected method for utilize the control channel over the LVDS link shall be compliant to the below implementation.

### 1097 — State management of LVDS link(4wire)
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The Serializer shall be responsible to set up the control channel.
- The Control channel State management shall follow the scheme below.
- The change of the selected method for utilize the control channel over the LVDS link shall be compliant to the below implementation.

### 1098 — Link Package Format
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- + Analysis Each package shall contain 30-bits: Bit position Field name Description 0-7 R Color data RGB, red 8-15 G Color data RGB, green 16-23 B Color data RGB, blue 24 V Toggling bit for line 25 H Toggling bit for frame 26 E Image enable 27*-28* ID* Source ID* 29* F* Function bit* Page No319(1572) Figure: Line formatR[0:7] G[8:15] B[16:23] V[24] H[25] E[26] ID[27:28]* F[29]** For non-interleaved links, these bits are not used.
- (RGB 888, YCbCr 4:4:4, YCbCr 4:2:2, YCbCr 4:2:0, etc.)However at any time, the transceiver/receiver supplier requirements for the packet format must be fulfilled.

### 1099 — Pixel Overhead Reduction
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- + Analysis All source information that does not need to be pixel synchronized may be sent through the control channel.
- The timing and the reduction of blanking may be compatible with the VESA-CVT-R standard for reduced blanking.

### 1100 — Toggle on Sync Bits
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- + Analysis In case of a bit error the line- or frame- sync shall be delayed by only one pixel.
- Sync information shall generate a toggle on the line- and frame-bits.
- For four-wire LVDS the selected transceiver and receiver can have HW supported video streams interleaving, in that case the preferred solution shall use the multiple HW implementations of the line- or frame-sync bits.

### 1101 — Video stream multiplex
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- Some links may require multiple video streams to be transmitted simultaneously.
- + Analysis If multiple video streams need to be transmitted over a single LVDS-link then they shall be multiplexed at the pixel level.
- The demultiplexer shall regenerate the original pixel clock for each demultiplexed video stream, in accordance with the pixel clock of the respective source.

### 1102 — Compatible generic requirements
- 版本：v1 ｜ 验证方式：- ｜ 适用：通用
- Specify which generic LVDS requirements are applicable for 1-wire Verification Method: An LVDS node using a 1-wire solution shall be applicable towards the section LVDS Datalink Layer - Generic reqs requirements specified in the table below: Req ID Requirement Reference Req ID 1094 : HDCP support Req ID 1092 : HDCP Keep Alive Req ID 1093 : HDCP setup HDCP Authentication flowchart Req ID 1098 : Link Package Format Req ID 1101 : Video stream multiplex Req ID 1100 : Toggle on Sync Bits Req ID 1095 : State management of LVDS link(1wire) Req ID 1095 : Node conformance test Req ID 1061 : Ability to read every frame instance Req ID 1067 : Wakeup strategy Req ID 1062 : Application timing requirements Req ID 1066 : LIN signal frames may appear arbitrarily Req ID 1073 : Timeout and sleep commands Req ID 1069 : Local event - master sends the first header Req ID 1071 : Power on - master sends the first header Req ID 1070 : Network event - wake up request to slave ready to communicate Req ID 1072 : Power on - slave sends the first response Req ID 1068 : Header jitter Req ID 1075 : Transmission time Req ID 1074 : Timeout and sleep commands Req ID 1051 : Number of nodes in a network Req ID 1050 : Ability to disregard other headers and frames Req ID 1053 : Timeout and sleep commands Req ID 1049 : LVDS support of LIN Go to Sleep HANDLING Req ID 1059 : Node address of Slave ECU for SWDL Req ID 1080 : Data restrictions of endianness Req ID 1086 : Message list Req ID 1084 : Event triggered signals heartbeat Req ID 1085 : Message flow of diagnostics between Diagnostic tester and Slave ECU Req ID 1089 : Sequence diagram Startup and Normal communication Req ID 1090 : Sequence diagram SWDL Req ID 1088 : Sequence diagram Diagnostic Req ID 1033 : Communication voltage range Req ID 1035 : Low Battery Voltage Operation Req ID 1032 : Battery voltage above normal operating range Req ID 1034 : ECU Power Loss Req ID 1036 : Recovery from reset Req ID 1041 : LVDS Single Chipset Req ID 1040 : ECU Internal Video Propagation Delay Req ID 1037 : ECU Internal Data Propagation Delay (1wire) Req ID 1042 : Node to node start up time Req ID 1029 : Bit error rate Req ID 1026 : Bidirectional Control Channel on one-wire LVDS Req ID 1044 : By-Pass Mode Req ID 1045 : By-Pass Start Up Time Page No270(1572) Req ID 1043 : By-Pass Latency Req ID 1046 : Pixel Queue Req ID 1047 : Pixel Queue Delay 4.3.7.2.2 Generic Control Channel (1wire)(LVDS Control Channel UDS compatible)The logic layer for the control channel link protocol is based on LIN Rev.
- de/)The physical layer for the Control channel on LVDS FPD-Link III coaxial shall use an I 2C link.

### 1103 — The priority between standard documents and this specification
- 版本：v1 ｜ 验证方式：- ｜ 适用：通用
- Verification Method: In case of discrepancy between the standard documents and this specification, this specification has precedence.4.3.7.2.2.1 Control channel protocol

### 1104 — I2C start and stop conditions
- 版本：v1 ｜ 验证方式：- ｜ 适用：通用
- Define the I2C start and stop conditions Verification Method: When the master shall initiate communication, the start condition shall be SDA transitions low when SCL is high.
- When the master shall stop communication, the stop condition shall be SDA transitions high when SCL is high.

### 1105 — Node I2C compliance
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Define the I2C compliance The nodes connected to the control channel shall be compliant to [LVDS_FPD:0],[LVDS_COAX:0] and [LVDS_I2C:0].

### 1106 — Startup, Establish Normal LVDS communication
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- 2 Enables configuration link, may be set automatic.

### 1107 — Communications protocol
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Define interface protocol which communicates between Master ECU and Slave ECU via LVDS. The Master ECU is normally the originator of the communication to Slave ECU by I2C Protocol. Once handed data is requested over, the Slave ECU communicate by I2C Protocol t

### 1108 — Master and slave configuration
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Master ECU shall be Master and Slave ECU shall be Slave in the I2C communication.

### 1109 — Slave address
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Define device addresses on I2C communication between Master ECU and Slave ECU via LVDS. + Analysis I2C register addresses: Device Serializer Read Serializer Write Deserializer Read Deserializer Write LVDS 1-wireSerializer 0xB0 (local address) 0xB1 (local addre

### 1110 — Bus speed
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- ldf files, according to LIN standard AND Test All modules shall be capable of operating at the nominal bus speeds of 9.6kbps or 19.2kbps, forbackward compatibility.
- The operating speed shall be defined on a bus by bus basis.
- The bus speed shall be 400 kbps (I2C fast-mode) in high speed mode, but the virtual bus speed shall be possible to limit to 19.2kbps.

### 1111 — Net bit rate of the LVDS chipset
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- The requirement specifies the minimum efficient net bit rate over LVDS Control channel AND Test The effective bit rate of the link shall be at least 150kbit/s.

### 1112 — Clock stretching in node
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- All master nodes shall implement support for clock stretching.

### 1113 — Local Register access Master ECU LVDS command
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- + Analysis Master ECU LVDS Chipset registers shall be accessible by diagnostic commands.
- Local access from Master ECU to its own addresses shall handle local error management.
- Gateway accesses to local Master ECU registers write access shall handle CRC or parity error management, offloading the CRC or parity from the message before perform the local register access.

### 1116 — Communication format
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- It shall be sent when the received frame has been validated, before the processing of the data.
- If the frame is incorrect, only the stop condition shall be sent.1115 v1 Calculation of check-sum for communication message Define calculation object and method + Analysis Object parameters: REG ADDRMsg ID and all BYTE Data ().

### 1117 — Detail of message Diag Command Request Diag Command Response
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- de/)The physical layer for the Control channel on LVDS GMSL shall use a virtual UART link.
- (4wire)The APIX2 chip shall provide an AShell which allows protocol handling with a framing of 8 bytes and additional CRC12 and optionally automatic retransmission of faulty data package, which is independent from the Control channel data package frame format defined in this section.
- UART/SPI), but this is not the main target for this specification, as the control channel in that case must implement an IP protocol package SW stack to emulate the needed Ethernet MAC layer.

### 1120 — Time restrictions of message
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Define time restrictions of message. Message type 1: ![](images/dea870555a20655157084fa7fd464e4af3d71add31e333ad3751b618ead75606. jpg) ![](images/299232fcc5fc32976558fa8dd3ed14fc91302ff97207a8e41e75f6517dfd261a. jpg) Note: The data bits marked as green (Ack/Na

### 1121 — LVDS Link LIN Error management of protocol
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- 1121 v1LVDS Link LIN Error management of protocol The Serializer shall be responsible to detect error on the Control channel.
- The Control channel Error format shall follow LIN format.
- + Analysis The master shall be responsible to detect error on the Control channel, if communication is unstable, the master needs to reinitialize the communication and check the link quality.

### 1122 — LVDS Link LIN Event and status
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- 1122 v1LVDS Link LIN Event and status The Serializer shall be responsible to handle Event and Status PID over the Control channel.
- The Control channel Event and Status format shall follow LIN format.
- + Analysis The Control channel shall have the PID mapping for Event and Status given below.

### 1123 — LVDS Link LIN Frame format
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The Serializer shall be responsible to set up the control channel.
- The Control channel frame format shall follow LIN format.
- + Analysis The LVDS control channel frame format, over the LVDS link shall be compliant to the below implementation.

### 1124 — LVDS Link LIN Mode control
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The Serializer shall be responsible to change mode over the Control channel.
- The Control channel mode format shall follow LIN format.
- The LVDS control channel Mode management format, over the LVDS link shall be compliant to the below implementation.

### 1125 — LVDS Link LIN SWDL Proprietary solution
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The Serializer shall be responsible to set up the SWDL over the control channel.
- The Control channel frame format shall follow LIN format.
- + Analysis The LVDS control channel SWDL format, over the LVDS link shall be compliant to the below implementation.

### 1126 — Built-in monitoring of link quality
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- DPR-LVDS-NETWORK-005: Req23v1 + Analysis It shall be possible to monitor the quality of the forward video channel on the deserializer side through a dedicated error counter.
- It shall also be possible to clear the error counter.
- The deserializer shall indicate the link status in terms of the existence, or absence, of a successful synchronization to the clock of the transmitted stream.

### 1127 — Error Management of MII MAC layer
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- DPR-LVDS-NETWORK-005: Req25v1, [ LVDS_APIx_Eth:1] + Analysis The MAC layer shall indicate a loss of data packages to the Network layer for further error management.

### 1128 — Generation of source-specific diagnostic test pattern
- 版本：v3 ｜ 验证方式：- ｜ 适用：通用
- To be able to verify source identity and image quality for diagnostics DPR-LVDS-NETWORK-005: Req24v1Verification Method: Demonstration ECU's equipped with a serializer shall be able to generate a video test pattern for each video channel separately.
- Valid test patterns: Test pattern White 24 bits, 0xFF, 0xFF, 0xFFTest pattern Red 24 bits, 0xFF, 0x00, 0x00Test pattern Green 24 bits, 0x00, 0xFF, 0x00Test pattern Blue 24 Bits, 0x00, 0x00, 0xFFImplementation: In Serializer side, shall be verified in Deserializer side.

### 1129 — LVDS Link Fault Detection, Receiver (4wire)
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- + Analysis It shall be possible to read out the link status and associated registers with diagnostic commands,to be used for quality measurements of the LVDS link.
- The Diagnostics shall detect and set DTCs for at least the following faults related to the LVDS link: Failure to lock PLLUnsuccessful synchronization to the clock of the received stream.

### 1130 — LVDS Link Fault Detection, Transceiver (4wire)
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- + Analysis It shall be possible to read out the link status and associated registers with diagnostic commands,to be used for quality measurements of the LVDS link.
- The Diagnostics shall detect and set DTCs for at least the following faults related to the LVDS link: Any internal error in the LVDS chipset, causing the stream not to be sent correctly.

### 1131 — ReceiverTest mode Management State chart(4wire)
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The PRBS Error counter, the PRBS test mode and the Link reset state shall be used.
- + Analysis It shall be possible to set the Receiver in PRBS test mode and associated registers with diagnostic commands,to be used for quality measurements of the LVDS link.
- The test mode shall make use of the LVDS chipset's built in PRBS mode and shall be controlled through a diagnostic control routine.

### 1132 — TransceiverTest mode Management State chart (4wire)
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- + Analysis It shall be possible to set the Transceiver in PRBS test mode with diagnostic commands, t o be used for quality measurements of the LVDS link.
- The test mode shall make use of the LVDS chipset's built in PRBS mode and shall be controlled through a diagnostic control routine.
- The following states on local side and remote (Receiver side) shall be implemented.

### 1133 — Local Config File LVDS Receiver
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- There shall be a way to modify the configuration of the Deserializer registers, test modes and link settings.
- The configuration data shall be possible to download to the ECU nonvolatile storage using a local config file.
- + Analysis It shall be possible to download a local config file that contains the configuration of the ECU to the nonvolatile storage via a microcontroller.

### 1134 — Local Config File LVDS Transceiver
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- There shall be a way to modify the configuration of the Serializer registers, test modes and link settings.
- The configuration data shall be possible to download to the ECU nonvolatile storage using a local config file.
- + Analysis It shall be possible to download a local config file that contains the configuration of the ECU, to the nonvolatile storage.

### 1135 — Local Register access LVDS Receiver
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Due to that the Tier 1 needs to define the format of the register data, the total size of the registers, how the data shall be structured, etc in order to configure the ECU using a local config file.
- + Analysis The Tier 1 shall define how all registers that are possible to modify in the ECU shall be contained in the local config file.

### 1136 — Local Register access LVDS Transceiver
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Due to that the Tier 1 needs to define the format of the register data, the total size of the registers, how the data shall be structured, etc in order to configure the ECU using a local config file.
- + Analysis The Tier 1 shall define how all registers that are possible to modify in the ECU shall be contained in the local config file.

### 1137 — Setting registers using Diagnostics LVDS Receiver
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- In order to be able to change the register settings, all registers that are possible to modify shall be possible to set using diagnostics.
- + Analysis All registers that can be modified shall be possible to set using diagnostics, ISO14229.

### 1138 — Setting registers using Diagnostics LVDS Transceiver
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- In order to be able to change the register settings, all registers that are possible to modify shall be possible to set using diagnostics.
- + Analysis All registers that can be modified shall be possible to set using diagnostics, ISO14229.

### 1139 — Status registers and Counters LVDS Receiver
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- It shall be possible to read the status of the Receiver with help of diagnostic commands.
- + Analysis It shall be possible to read status and counters in the Receiver with diagnostic commands.

### 1140 — Status registers and Counters LVDS Transceiver
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- It shall be possible to read the status of the Transceiver with help of diagnostic commands.
- + Analysis It shall be possible to read status and counters in the Transceiver with diagnostic commands.

### 1141 — LVDS Link Fault Detection, Receiver (2wire)
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- + Analysis It shall be possible to read out the link status and associated registers with diagnostic commands,to be used for quality measurements of the LVDS link.
- The Diagnostics shall detect and set DTCs for at least the following faults related to the LVDS link: Failure to lock PLLUnsuccessful synchronization to the clock of the received stream.

### 1142 — LVDS Link Fault Detection, Transceiver (2wire)
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- + Analysis It shall be possible to read out the link status and associated registers with diagnostic commands,to be used for quality measurements of the LVDS link.
- The Diagnostics shall detect and set DTCs for at least the following faults related to the LVDS link: Any internal error in the LVDS chipset, causing the stream not to be sent correctly.

### 1143 — Receiver Test mode Management State chart(2wire)
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The PRBS Error counter, the PRBS test mode and the Link reset state shall be used + Analysis Page No301(1572) It shall be possible to set the Receiver in PRBS test mode and associated registers with diagnostic commands, to be used for quality measurements of the LVDS link.
- The test mode shall make use of the LVDS chipset's built in PRBS mode and shall be controlled through a diagnostic control routine.
- The following states on local side (Receiver side) or remote via the Control channel shall be implemented.

### 1144 — Transceiver Test mode Management State chart (2wire)
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- + Analysis It shall be possible to set the Transceiver in PRBS test mode with diagnostic commands, t o be used for quality measurements of the LVDS link.
- The test mode shall make use of the LVDS chipset's built in PRBS mode and shall be controlled through a diagnostic control routine.
- The following states on local side and remote (Receiver side) shall be implemented.

### 1145 — LVDS Built-in Self-Test
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- REQPROD 344967, REQPROD 344560 + Analysis The circuit implementing the LVDS-link shall be able to test the quality of the forward channel by means of a built-in test, accessed via LVDS SW application.

### 1146 — LVDS Channel equalizing
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- REQPROD 344972, REQPROD 344565 + Analysis The LVDS link SW shall be able to support channel equalization compensation settings in physical layer.
- The amount of compensation shall be programmable in at least 10 steps.

### 1147 — LVDS Integrated Bidirectional Control Channel
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- REQPROD 344951 , REQPROD 344516 + Analysis The LVDS-link shall support SW access to a bidirectional channel for control data.
- Latency shall be less than 1 ms and data throughput at least 400 kbps, including SW frame overhead.

### 1148 — LVDS Integrated high-speed data link
- 版本：v1 ｜ 验证方式：- ｜ 适用：通用
- REQPROD 344517Verification Method: The four-wire LVDS-link shall support SW access to high-speed bidirectional transfer over a full-duplex 100 Mbps (including SW frame overhead) Ethernet channel.

### 1149 — LVDS Line diagnostics
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- REQPROD 344975 + Analysis The LVDS link SW layer shall be able to identify and indicate the LVDS link failure modes in physical layer.

### 1150 — LVDS Pre-Emphasis
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- REQPROD 344971 , REQPROD 344563 + Analysis The LVDS link SW shall be able to support pre-emphasis compensation settings in physical layer.
- The amount of compensation shall be programmable in at least 10 steps.

### 1151 — LVDS Signal Quality Evaluation
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- REQPROD 344969, REQPROD 344562 + Analysis The LVDS link SW shall be able from the software layer on the serializer side of the link to allow temporary setting of pre-emphasis and equalization, as well as to carry out PRBS tests, including reading out the test result from the deserilizer with application layer SW.

### 1152 — LVDS Video throughput
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- REQPROD 344968, REQPROD 344561 + Analysis The LVDS-link SW shall support video throughput analysis via LVDS physical layer features.
- Qualification method: Analysis, documentation of test results.4.3.7.3.1.3 LVDS Link - LIN - Communication diagnosticsThe LVDS control channel must be able to perform diagnostics over the LVDS link, The methods for diagnostics must be compliant to the to the [LVDS_Generic:11] UDS Services and [LVDS_GENERIC:15] UDSonLVDS.

### 1153 — Deserializer communication diagnostics (2wire)
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The Deserializer shall be responsible to set up the diagnostics over the control channel.
- The Control channel diagnostics format shall follow LIN format.
- + Analysis The LVDS control channel Receiver diagnostics format, over the LVDS link shall be compliant to the below implementation.

### 1154 — Deserializer communication diagnostics (4wire)
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The Deserializer shall be responsible to set up the diagnostics over the control channel.
- The Control channel diagnostics format shall follow LIN format.
- + Analysis The LVDS control channel Receiver diagnostics format, over the LVDS link shall be compliant to the below implementation.

### 1155 — Serializer communication diagnostics (2wire)
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The Serializer shall be responsible to set up the diagnostics over the control channel.
- The Control channel diagnostics format shall follow LIN format.
- + Analysis The LVDS control channel Transceiver diagnostics format, over the LVDS link shall be compliant to the below implementation.

### 1156 — Serializer communication diagnostics (4wire)
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The Serializer shall be responsible to set up the diagnostics over the control channel.
- The Control channel diagnostics format shall follow LIN format.
- + Analysis The LVDS control channel Transceiver diagnostics format, over the LVDS link shall be compliant to the below implementation.

### 1157 — LVDS Control channel over Ethernet
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- When the Control Channel is implemented over Ethernet protocol - the IP Command Protocol shall be used.
- When Ethernet protocol is used it shall also handle diagnostics and SWDL functionality.
- + Analysis The Ethernet protocol over LVDS link shall be implemented according to the IP Command Protocol.

### 1158 — Transport and Network layer
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The transport/network layer required by this document shall be compliant to [CoFR_4] Road vehicles - Communication on FlexRay - Part 2: Communication layer services, ISO 10681-2, CoFlexRay — Part 2: Communication layer services, with the restrictions/additions as defined by this document.4.3.8.1.1.1 Communication Layer Protocol4.3.8.1.1.1.1 Protocol functionsAll messages shall be transmitted as unacknowledged messages.
- Acknowledged messages shall be supported but not used.
- the sender shall not use and the receiver shall accept the acknowledged messages.

### 1159 — Unacknowledge messages - used
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- All messages shall be transmitted as unacknowledged messages.

### 1160 — Known (ML) Message Length - used
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- All messages shall be transmitted with a known message length.

### 1161 — Unknown (ML) Message Length - not supported
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Unknown message length shall not be supported, i.
- any message received with unknown message length shall be ignored.4.3.8.1.1.1.2 Unsegmented and Segmented TransmissionAn unsegmented message is transmitted if the message length is lower than or equal to MFDS for STF C_PDU.
- This means that these C_PDUs shall be filled with message data equaling MFDS.

### 1162 — Message length break point for unsegmented_segmented messages
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- An unsegmented message shall be transmitted if the message length is lower than or equal to MFDS for STF C_PDU.
- A segmented transmission shall be performed when the message length is greater than the MFDS for STF C_PDU.

### 1163 — Dynamic frame length for segmented message
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Dynamic frame length for a segmented message (or dynamic data transfer) is not allowed, see Road vehicles - Communication on FlexRay - Part 2: Communication layer services, ISO 10681-2, CoFlexRay — Part 2: Communication layer services - External publications section 7.3.4.3.8.1.1.1.3 Protocol control information (C_PCI)The following sub-sections detail the valid usage of the FlowControl (FC) parameters.4.3.8.1.1.1.3.1 FlowStatus (FS) parametersAll defined FlowStatus (FS) parameters in [CoFR_4] Road vehicles - Communication on FlexRay - Part 2: Communication layer services, ISO 10681-2 shall be supported but only following shall be used: ContinueToSend, Wait, Abort and Overflow.
- In programming session, the server may use FC.

### 1164 — FlowControl Wait usage
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- Non-gateway server: In programming session, the server may use FC.
- Gateway ECU: The gateway ECU shall use FC.

### 1165 — FlowStatus (FS) parameter
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- For robustness reasons and future needs all defined FS shall be supported.
- All defined FlowStatus (FS) parameters in Road vehicles - Communication on FlexRay - Part 2: Communication layer services, ISO 10681-2, CoFlexRay — Part 2: Communication layer services - External publications shall be supported but only following shall be used: ContinueToSend, Wait, Abort and Overflow.
- Wait frame transmissions (C_WFTmax)The C_WFTmax counter shall be set to 255.

### 1166 — C_WFTmax
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The WAIT mechanism will aid the following dimensioning use cases:- Down stream: Two queued messages are sent to an ECU and the time from the first request received until the final response sent of the first request.- Up stream: Functional address request with unsuppressed response result in a many responses which may need to wait.
- The C_WFTmax counter shall be set to 255 4.3.8.1.1.1.3.3 Bandwidth Control (BC) parameterThe bandwidth control mechanism shall not be used.
- Consequently, BC parameter shall be set to zero (0).

### 1167 — Bandwidth Control (BC) parameter
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- BC shall be supported for robustness reasons and for future needs.
- The bandwidth control mechanism shall be supported but not used.
- Consequently, BC parameter shall be set to zero (0).

### 1168 — Buffersize (BfS) parameter - sender influence
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The sender shall not influence the BufferSize so that a lower amount of data is transmitted than the given BufferSize, except for when the end of the message is reached.

### 1169 — Minimum Buffersize (BfS) in programming session server side
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- For servers and gateway ECUs: In programming session the receiver of a downstream message must respond with a BfS value such that there are never more than one FC C_PDUs per 4095 bytes of data (including the first FC C_PDU) when buffer resources makes 4095 bytes available.
- Additional for gateway ECU: In programming session, if available RAM buffer is less than the length of the message, then BfS value must be so large that all available RAM buffer is used to receive as much as possible of the message, per each FC C_PDU.
- If the server can receive a complete message of 65535 bytes with only one FC C_PDUs, then BfS parameter shall be set to 0x0000.

### 1170 — Minimum BufferSize (BfS) in programming session client side
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- For ECU gatewaying responses from FlexRay to another network: In programming session the receiver of an upstream message must respond with a BfS value such that there are never more than one FC C_PDUs per 1024 bytes of data (including the first FC C_PDU) when buffer resources makes 1024 bytes available.
- In programming session, if available RAM buffer is less than the length of the message, then BfS value must be so large that all available RAM buffer is used to receive as much as possible of the message, per each FC C_PDU.
- If the server can receive a complete message of 65535 bytes with only one FC C_PDUs, then BfS parameter shall be set to 0x0000.

### 1171 — Minimum BufferSize (BfS) in non-programming sessions server side
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- For servers and gateway ECUs: In non-programming session the receiver of a downstream message must respond with a BfS value such that there are never more than one FC C_PDUs per 200 bytes of data (including the first FC C_PDU) when buffer resources makes 200 bytes available.
- Additional for gateway ECU: In non-programming session, if available RAM buffer is less than the length of the message, then BfS value must be so large that all available RAM buffer is used to receive as much as possible of the message, per each FC C_PDU.
- If the server can receive a complete message of 65535 bytes with only one FC C_PDUs, then BfS parameter shall be set to 0x0000.

### 1172 — Minimum BufferSize (BfS) in non-programming sessions client side
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- For ECU gatewaying responses from FlexRay to another network: In non-programming session the receiver of a upstream message must respond with a BfS value such that there are never more than one FC C_PDUs per 4095 bytes of data (including the first FC C_PDU) when buffer resources makes 4095 bytes available.
- In non-programming session, if available RAM buffer is less than the length of the message, then BfS value must be so large that all available RAM buffer is used to receive as much as possible of the message, per each FC C_PDU.
- If the server can receive a complete message of 65535 bytes with only one FC C_PDUs, then BfS parameter shall be set to 0x0000.

### 1173 — C_As timeout in programming session
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- The timeout value shall be high enough to not be affected by situations like occasional high busloads and low enough to get a user friendly system if for example an ECU is not connected.
- C_As timeout value shall be CycleTime * 200 in programming session, (e.

### 1174 — C_Ar timeout in programming session
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- The timeout value shall be high enough to not be affected by situations like occasional high busloads and low enough to get a user friendly system if for example an ECU is not connected.
- C_Ar timeout value shall be CycleTime * 200) in programming session, (e.

### 1175 — C_Bs timeout in programming session
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- The timeout value shall be high enough to not be affected by situations like occasional high busloads and low enough to get a user friendly system if for example an ECU is not connected.
- C_Bs timeout value shall be CycleTime * 200) in programming session, (e.

### 1176 — C_Br in programming session for FC. CTS,ABT and OVFLW
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- When in programming session the ECU will not be burdened by simultaneously running an application and hence the ECU shall be able to respond faster than in non-programming session.
- C_Br shall maximum be CycleTime * 3 for FC.
- CTS C_PDU within C_Br.3) For high performance, the timing parameter values for C_Br shall be as low as possible.

### 1177 — C_Br in programming session for FC. WAIT
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- The time that an ECU may wait before sending a FC.
- Wait frame must be lower than the specified timeout to ensure the sending ECU does not time out the message.
- Wait frame shall be as high as possible.

### 1178 — C_Cs in programming session between FC and CF frames
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- When in programming session the ECU will not be burdened by simultaneously running an application and hence the ECU shall be able to respond faster than in non-programming session.
- C_Cs shall maximum be CycleTime * 3 in programming session between reception a FlowControl C_PDU until transmission of the next ConsecutiveFrame C_PDU/LastFrame C_PDU, (e.
- Note:1) The CycleTime value is specified in [CoFR_2] FlexRay Data Link Layer.2) For high performance, the timing parameter values for C_Cs shall be as low as possible.

### 1179 — C_Cs in program session between CF frames (Down stream)
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- In programming session the consecutive frames shall be sent with maximum use of the client side ECU slots.
- C_Cs for down stream transmitted messages shall maximum be CycleTime * 1 in programming session between a ConsecutiveFrame C_PDU until transmission of the next ConsecutiveFrame C_PDU/LastFrame C_PDU, (e.
- Note:1) The CycleTime value is specified in [CoFR_2] FlexRay Data Link Layer.2) For high performance, the timing parameter values for C_Cs shall be as low as possible.

### 1180 — C_Cs in program session between CF frames (Up stream-ECU)
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- In programming session the consecutive frames shall be sent with maximum use of the server side ECUs slots.
- C_Cs for up stream transmitted messages from a ECU shall maximum be CycleTime * 2 in programming session between a ConsecutiveFrame C_PDU until transmission of the next ConsecutiveFrame C_PDU/LastFrame C_PDU, (e.

### 1181 — C_Cs in program session between CF frames (Up stream-Gateway
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- In programming session the consecutive frames shall be sent with maximum use of the server side ECUs slots.
- C_Cs for up stream transmitted messages from a gateway ECU shall maximum be CycleTime * 2 in programming session between a ConsecutiveFrame C_PDU until transmission of the next ConsecutiveFrame C_PDU/LastFrame C_PDU, (e.

### 1182 — C_Cr timeout in programming session
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- The timeout value shall be high enough tonot be affected by situations like occasional high busloads and low enough toget a user friendly system if for example an ECU is not connected.
- C_Cr timeout value shall be CycleTime * 200) in programming session (e.
- when in non-programming session) then the table below shall apply.

### 1183 — C_As timeout in non-programming session
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- The timeout value shall be high enough tonot be affected by situations like occasional high busloads and low enough toget a user friendly system if for example an ECU is not connected.
- C_As timeout value shall be CycleTime * 200 in non-programming session, (e.

### 1184 — C_Ar timeout in non-programming session
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- The timeout value shall be high enough tonot be affected by situations like occasional high busloads and low enough toget a user friendly system if for example an ECU is not connected.
- C_Ar timeout value shall be CycleTime * 200) in non-programming session, (e.

### 1185 — C_Bs timeout in non-programming session
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- The timeout value shall be high enough to not be affected by situations like occasional high busloads and low enough to get a user friendly system if for example an ECU is not connected.
- C_Bs timeout value shall be CycleTime * 200) in non-programming session, (e.

### 1186 — C_Br in non-programming session for FC. CTS,ABT and OVFLW
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- The time spent waiting shall be minimized.
- Although C_Br time does not affect the transmission time as much as C_Cs time, the diagnostic kernel scheduling shall still be done with the same frequency.
- C_Br shall maximum be CycleTime * 4 for FC.

### 1187 — C_Br in non-programming session for FC. WAIT
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- The time that an ECU may wait before sending a FC.
- Wait frame must be lower than the specified timeout to ensure the sending ECU does not time out the message.
- Wait frame shall be as high as possible.

### 1188 — C_Cs in non-programming session between FC and CF frames
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- When in non-programming session the ECU will be burdened by simultaneously running an application and hence the C_Cs requirement shall be relaxed compared to programming session.
- C_Cs shall maximum be CycleTime * 4 in non-programming session between reception of a FlowControl C_PDU until transmission of the next ConsecutiveFrame C_PDU/LastFrame C_PDU, (e.
- 5ms cycle time P ≤20ms)Note:1) The CycleTime value is specified in [CoFR_2] FlexRay Data Link Layer.2) For high performance, the timing parameter values for C_Cs shall be as low as possible.

### 1189 — C_Cs in non-programming session between CF frames (Down stream)
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- When in non-programming session the ECU will be burdened by simultaneously running an application and hence the C_Cs requirement shall be relaxed compared to programming session.
- In non-programming session the consecutive frames shall be sent with maximum use of the client side ECU slots.
- Down stream and up stream messages are judged to have equal importance for C_Cs between consecutive CF C_PDUs C_Cs for down stream transmitted messages shall maximum be CycleTime * 2 in non-programming session between a ConsecutiveFrame C_PDU until transmission of the next ConsecutiveFrame C_PDU/LastFrame C_PDU, (e.

### 1190 — C_Cs in non-program session between CF frames (Up stream-ECU)
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- When in non-programming session the ECU will be burdened by simultaneously running an application and hence the C_Cs requirement shall be relaxed compared to programming session.
- In non-programming session the consecutive frames shall be sent with maximum use of the server side ECUs slots.
- C_Cs for up stream transmitted messages from a ECU shall maximum be CycleTime * 2 in non-programming session between a ConsecutiveFrame C_PDU until transmission of the next ConsecutiveFrame C_PDU/LastFrame C_PDU, (e.

### 1191 — C_Cs in non-program session between CF frames (Up stream-Gateway)
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- When in non-programming session the ECU will be burdened by simultaneously running an application and hence the C_Cs requirement shall be relaxed compared to programming session.
- In non-programming session the consecutive frames shall be sent with maximum use of the server side ECUs slots.
- C_Cs for up stream transmitted messages from a gateway ECU shall maximum be CycleTime * 8 in non-programming session between a ConsecutiveFrame C_PDU until transmission of the next ConsecutiveFrame C_PDU/LastFrame C_PDU, (e.

### 1192 — C_Cr timeout in non-programming session
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- The timeout value shall be high enough to not be affected by situations like occasional high busloads and low enough to get a user friendly system if for example an ECU is not connected.
- C_Cr timeout value shall be 4000 ms.4.3.8.1.1.3 Interleaving of messages4.3.8.1.1.3.1 DuplexIn programming session, all ECUs of a FlexRay network, both FlexRay ECUs and FlexRay Schedule Coordinator, shall comply with full-duplex behaviour, which specifies the concurrency of transmission and reception of the channel and the behaviour of unexpected arrival of C_PDUs.
- In all other sessions half duplex shall be supported.

### 1193 — Duplex communication
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- In programming session, full duplex shall be supported .
- In all other sessions half duplex shall be supported .4.3.8.1.1.4 Data link layer usage4.3.8.1.1.4.1 Hardware Address filtering within dynamic segmentTo utilize hardware filtering all physically addressed request/response frames shall have the Payload Preamble Indicator (PPI) set.
- Functionally addressed requests shall not have the PPI set.

### 1194 — Payload Preamble Indicator (PPI) - Physically addressing
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- To utilize hardware filtering all physically addressed request/response messages shall have thePayload Preamble Indicator (PPI) set (set to one).

### 1195 — Payload Preamble Indicator (PPI) - Function addressing
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- All functionally addressed request messages shall have the Payload Preamble Indicator (PPI)cleared (set to zero).4.3.8.1.1.4.2 Multiple C_PDU to single frame (L_PDU) mappingOnly one C_PDU shall be mapped into a single L-PDU.

### 1196 — One (1) C_PDU per frame
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Only one C_PDU shall be mapped into a single L_PDU.
- Only one C_PDU shall be mapped into a single frame (L_PDU).4.3.8.1.1.4.3 Use data frame by frameWhile receiving a segmented request for TransferData 0x36 the transport protocol shall send allN_Data from each N_PDU immediately to upper layers that contain the flash programmingfunctions (optional for all other services).
- The ECU must not start flashing the TransferDatablock after the complete TransferData block has been received.

### 1197 — Forward C_Data from each C_PDU to upper layer
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- While a diagnostic server is receiving a segmented request for TransferData 0x36 the transport protocol layer shall send all C_Data from each C_PDU to upper layers that contain the flash programming functions (optional for all other services).
- If the C_Data is compressed, all C_Data from each C_PDU shall be sent to the layer where decompression is performed, and that layer shall in turn send data as soon as it is decompressed to upper layers that contain the flash programming functions.
- Note: this contradicts and shall override ISO specified transport layer behaviour which states that the transport layer shall only send complete diagnostic messages to upper layers.

### 1198 — Transport and Network layer
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- ISO standard shall be followed as far as possible unless otherwise specified to reduce cost and make implementation easier.
- The transport/network layer shall be compliant to [DoCAN_2] Road vehicles – Diagnostic communication over Controller Area Network (DoCAN) - Part 2: Transport protocol and network layer services with the restrictions/additions as defined by this document.
- If there are contradictions between this specification and [DoCAN_2] Road vehicles – Diagnostic communication over Controller Area Network (DoCAN) - Part 2: Transport protocol and network layer services, then this specification shall override [DoCAN_2] Road vehicles – Diagnostic communication over Controller Area Network (DoCAN) - Part 2: Transport protocol and network layer services.

### 1199 — Precedence of requirements
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- If there are other kinds or requirements like legislative requirements (for example OBD requirements), these requirements may have higher priority than the requirements in this specification.
- However if the other requirements have performance requirements lower than the performance requirements specified in this document, the performance requirements in this document shall be followed.
- 4.3.9.1.2.1 Protocol control information specification 4.3.9.1.2.1.1 BlockSize (BS) parameter definitionWhen in a non-programming session, both the server and client side shall be able to receive a complete diagnostic message without sending any intermediate flow control frames, to ensure as swift communication as possible.

### 1200 — BlockSize parameter non-programming session server side
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- For more information see section BlockSize (BS) parameter definition Section "BlockSize (BS) parameter definition" BlockSize shall be 15 (0x0F) or higher for server side.
- If the server can receive 4095 bytes without intermediate FlowControl frames, the BlockSize parameter shall be set to 0x00.
- 22281 v1CAN FD BlockSize parameter non-programming session server side Define BlockSize for non-programming session server side Legacy ID: BlockSize shall be 5 (0x05) or higher for server side.

### 1201 — BlockSize parameter non-programming session client side
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- For ECU gatewaying responses from CAN to another network: In non-programming session the receiver of an upstream message must respond with BS=0 so that there are never more than one FlowControl N_PDUs per 4095 bytes of data (including the first FlowControl N_PDU) when buffer resources makes 4095 bytes available.
- In non-programming session, if the largest available RAM buffer is less than the length of the message, that buffer must be used, and BS set so that all of that buffer is used.

### 1202 — BlockSize parameter programming session server side
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- BlockSize (BS) shall always be 0x00 in programming session for server side.

### 1203 — BlockSize parameter programming session client side
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- BlockSize (BS) shall always be 0x00 in programming session for client side4.3.9.1.2.1.2 Separation (STmin) parameter definitionThe STmin parameter shall reflect the maximum processing time the ECU needs to have in between each CAN frame, regardless of ECU state or activity.
- For example if an ECU sets a STmin time of 1ms, the supplier must guarantee that the ECU is always able to process consecutive frames at this rate.
- Preferably the STmin time shall be as low as possible, but the server is allowed to set a maximum of 15ms.

### 1204 — Separation time (STmin) non-programming session server side
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Section "Separation (STmin) parameter definition" Separation time (STmin) for server side when in non-programming session shall be maximum 15ms.

### 1205 — Separation time (STmin) non-programming session client side
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- When in non-programming session the ECU shall be able to receive CF N_PDU with minimum 5ms separation time (i.

### 1206 — Separation time (STmin) programming session server side
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Separation time (STmin) for programming session shall be maximum 0ms for server side.

### 1207 — Separation time (STmin) programming session client side
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- When in programming session the ECU shall be able to receive CF N_PDU with minimum 5ms separation time (i.
- Note: It is allowed to support shorter separation time than this requirement specifies.4.3.9.1.2.1.3 Separation time between single framesIn programming session the ECU shall be able to handle receiving single frames (SF) with no separation time.
- In these examples and if using 500kbps bit rate up to four single frames shall be received within one millisecond.

### 1208 — Separation time between single frames - programming session
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- In programming session the ECU shall handle receiving single frames (SF N_PDU) with as short time apart as the CAN protocol allows.
- Wait frame transmission (N_WFTmax)The N_WFTmax counter shall be set to 255 (0xFF).
- In programming session, the server may use FC.

### 1209 — N_WFTmax value for server side
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- N_WFTmax counter shall be set to 255 (FF hex) for server side.

### 1210 — N_WFTmax value for client side
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- N_WFTmax counter shall be set to 255 (FF hex) for client side.

### 1211 — Flowcontrol Wait usage
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- Non-gateway server: In programming session, the server may use FC.
- Gateway ECU: The gateway ECU shall use FC.
- Wait the periodicity shall be N_Bs * 0.9 = 900ms ± 50ms.

### 1212 — N_As timeout in non-programming session
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The timeout value shall be high enough to not be affected by situations like occasional high busloads and low enough to get a user friendly system if for example an ECU is not connected.
- N_As timeout value shall be 1000ms in non-programming session.

### 1213 — N_Ar timeout in non-programming session
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The timeout value shall be high enough to not be affected by situations like occasional high busloads and low enough to get a user friendly system if for example an ECU is not connected.
- N_Ar timeout value shall be 1000ms in non-programming session.

### 1214 — N_Bs timeout in non-programming session
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The timeout value shall be high enough to not be affected by situations like occasional high busloads and low enough to get a user friendly system if for example an ECU is not connected.
- N_Bs timeout value shall be 1000ms in non-programming session.

### 1215 — N_Br Performance requirement in non-programming session for FC. CTS andFC. OVFLW
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- The time spent waiting shall be minimized.
- Although N_Br time does not affect the transmission time as much as N_Cs time, the diagnostic kernel scheduling shall still be done with the same frequency Table - Timing parameters non-programming session, item 4 N_Br shall be N_Br < 20 ms for FC.
- If other CAN frames with higher priority exist on CAN, then a FC N_PDU may be delayed due to CAN protocol arbitration.

### 1216 — N_Br Performance requirement in non-programming session for FC. Wait
- 版本：v5 ｜ 验证方式：Test ｜ 适用：通用
- The time that an ECU may wait before sending a FC.
- Wait frame must be lower than the specified timeout to ensure the sending ECU does not time out the message.
- Wait frame shall be as high as possible.

### 1217 — N_Cs Performance requirement in non-programming session
- 版本：v5 ｜ 验证方式：Test ｜ 适用：通用
- The time spent waiting shall be minimized and especially for N_Cs since N_Cs wait time is the factor that affects the transfer rates the most.
- When in non-programming session, the ECU shall be able to send Consecutive Frames with N_Cs less than 20ms.
- If other CAN frames with higher priority exist on CAN, then a FC N_PDU may be delayed due to CAN protocol arbitration.

### 1218 — N_Cr timeout in non-programming session
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The timeout value shall be high enough to not be affected by situations like occasional high busloads and low enough to get a user friendly system if for example an ECU is not connected.
- N_Cr timeout value shall be 1000ms in non-programming session.

### 1219 — N_As timeout in programming session
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The timeout value shall be high enough to not be affected by situations like occasional high busloads and low enough to get a user friendly system if for example an ECU is not connected.
- N_As timeout value shall be 1000ms in programming session.

### 1220 — N_Ar timeout in programming session
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- The timeout value shall be high enough to not be affected by situations like occasional high busloads and low enough to get a user friendly system if for example an ECU is not connected.
- N_Ar timeout value shall be 1000ms in programming session.

### 1221 — N_Bs timeout in programming session
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The timeout value shall be high enough to not be affected by situations like occasional high busloads and low enough to get a user friendly system if for example an ECU is not connected.
- N_Bs timeout value shall be 1000ms in programming session.

### 1222 — N_Br performance requirement in programming session for FC. CTS andFC. OVFLW
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- When in programming session the ECU will not be burdened by simultaneously running an application and hence the ECU shall be able to respond faster than in non-programming session.
- Table - Timing parameters programming session, item 4 N_Br shall be N_Br < 2000 microseconds for FC.
- If other CAN frames with higher priority exist on CAN, then a FC N_PDU may be delayed due to CAN protocol arbitration.

### 1223 — N_Br Performance requirement in programming session for FC. Wait
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- The time that an ECU may wait before sending a FC.
- Wait frame must be lower than the specified timeout to ensure the sending ECU does not time out the message.
- Wait frame shall be as high as possible.

### 1224 — N_Cs Performance requirement in programming session
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- In programming session the consecutive frames shall be sent as close to back to back as possible for maximum speed.
- Table - Timing parameters programming session, item 5 In programming session N_Cs shall be N_Cs < 100 microseconds.
- If other CAN frames with higher priority exist on CAN, then a FC N_PDU may be delayed due to CAN protocol arbitration.

### 1225 — N_Cr timeout in programming session
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The timeout value shall be high enough to not be affected by situations like occasional high busloads and low enough to get a user friendly system if for example an ECU is not connected.
- N_Cr timeout value shall be 1000ms in programming session.4.3.9.1.2.3.2 Unexpected arrival of N_PDUIn programming session, full duplex shall be supported.
- In all other sessions half duplex shall be supported.

### 1226 — Duplex communication
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- Full duplex shall be supported to make it possible to queue requests on both the gateways and the servers in programming session.
- In programming session, full duplex shall be supported.
- In all other sessions half duplex shall be supported.

### 1227 — Addressing format
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- "Normal addressing" as specified in [DoCAN_2] Road vehicles – Diagnostic communication over Controller Area Network (DoCAN) - Part 2: Transport protocol and network layer services shall be used.

### 1228 — CAN frame identifier length
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- -bit CAN frame identifiers shall be used.

### 1229 — Supporting functional requests
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Functional requests shall be supported.4.3.9.1.1.2 CAN frame data paddingFor Classic CAN the DLC (Data Length Code) contained in every CAN frame shall always be set to eight.
- Any CAN frame with a DLC different from eight shall be considered invalidly formatted and ignored by the recipient.
- For CAN FD the DLC (Data Length Code) contained in every CAN frame shall always be set to a value within the range 8 to 15.

### 1230 — Length of Classic CAN frames
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- The DLC (DataLengthCode) of USDT frames on Classic CAN format shall always be set to eight.
- 22292 v2 Length of CAN FD frames Define the length of USDT frames Legacy ID: The DLC (DataLengthCode) of USDT frames on CAN FD format shall be in the range 8 to 15.

### 1231 — Handling of CAN requests in regards of DLC
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- USDT request frames with a DLC not equal to eight (8) for Classic CAN, or outside the range 8-15 for CAN FD, shall be considered invalidly formatted and be ignored by the recipient.

### 1232 — Unused data in the CAN frame
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Unused data shall be padded with 0x00 and the receiver of the frame shall ignore padding.4.3.9.1.1.3 Use data frame by frameWhile receiving a segmented request for TransferData 0x36 the transport protocol shall send all N_Data from each N_PDU immediately to upper layers that contain the flash programming functions (optional for all other services).
- The ECU must not start flashing the TransferData block after the complete TrasferData block has been received.
- If the N_Data (transferRequestParameterRecord) is compressed, all N_Data from each N_PDU shall be sent to the layer where decompression is performed, and that layer shall in turn send data as soon as it is decompressed to upper layers that contain the flash programming functions.

### 1233 — Forward N_Data from each N_PDU to upper layer
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- While a diagnosotic server is receiving a segmented request for TransferData 0x36 the transport protocol layer shall send all N_Data from each N_PDU to upper layers that contain the flash programming functions (optional for all other services).
- If the N_Data is compressed, all N_Data from each N_PDU shall be sent to the layer where decompression is performed, and that layer shall in turn send data as soon as it is decompressed to upper layers that contain the flash programming functions.
- Note: this contradicts and shall override ISO specified transport layer behaviour which states that the transport layer shall only send complete diagnostic messages to upper layers.

### 1234 — Client Behaviour During DoIP Session
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- The client ECU shall remain connected during the complete DoIP Session.
- If the Edge Node disconnects then the client shall try to reestablish the connection.

### 1262 — DoIP header
- 版本：v5 ｜ 验证方式：Test ｜ 适用：通用
- To define the header used for in-vehicle DoIP communication DoIP-036, DoIP-064 [ISO13400-2] The DoIP header shall follow DoIP-036 and DoIP-064 in [ISO13400-2] during its transportation through the internal vehicle network.

### 1263 — DoIP Ports for Internal Communication
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- DoIP-001 [ISO 13400-2] All in-vehicle DoIP communication shall use the target/destination TCP port 13400 when connecting to and communicating with the Edge Node.

### 1264 — Source Port for Internal Communication
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- To define which source(local) port the in-vehicle IP ECUs shall use for DoIP communication.
- The source port number shall be randomized by the IP ECU.

### 1265 — DoIP Support in Internal ECUs
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- To define which DoIP types that shall be supported for in vehicle DoIP communication.
- DoIP-064 [ISO 13400-2] All internal ECUs in the vehicle network shall only support diagnostic message, payload type 0x8001, according to DoIP-064 [ISO13400-2]

### 1266 — Lost TCP connection for DoIP Messages
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- If the IP ECU detects that a DoIP connection is not available to the Edge Node then it shall establish a DoIP connection to the Edge Node.

### 1267 — Open TCP Connection for DoIP Messages
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- At startup, all TCP based target ECUs within the vehicle shall initiate and open TCP Connections for DoIP communication to/from the Edge Node.
- The TCP Connection shall remain until the Edge node sends a reset or shut down request.

### 1268 — Reconnect With Same IP and Port Number
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- The IP ECU shall try to connect again after 5 ms using IP address and port number after a connection attempt has been refused.
- The source port number shall be the same as when the ECU started.
- e the port number shall not be randomized when a connection attempt is refused.

### 1269 — Close TCP port on connection reset
- 版本：v2 ｜ 验证方式：Test ｜ 适用：4.0.x
- To ensure that the TCP port is closed when the Edge node is resetting The IP ECU shall close the TCP port when the Edge node resets4.3.11 Guideline for Safety Related Communication4.3.11.1 Guideline for Safety Related Communication4.3.11.1.1 Appendix B - Examples of CAN Signals ReceptionThe principle to receive a signal in an asynchronous system is shown in Figure: Reception of a signal in an asynchronous system.
- The specific mechanism is also application dependant, but shall ensure that a faulty application SW should not be able to cause a hazardous situation.
- In order to fulfill the requirements (A) and (M) must perform mutual monitoring of the other's error detection capabilities, i.

### 1270 — ARP Implementation
- 版本：v4 ｜ 验证方式：Analysis ｜ 适用：通用
- RFC 826 The Address Resolution Protocol, ARP shall be implemented as specified by [RFC 826].

### 1271 — ARP Cache
- 版本：v5 ｜ 验证方式：Analysis ｜ 适用：通用
- IP-ECUs shall implement one dynamic ARP cache for each logical interface and the size shall be 30 entries.

### 1272 — ARP Announcements
- 版本：v4 ｜ 验证方式：Analysis ｜ 适用：通用
- RFC 826, RFC 2002 ARP announcements shall be supported as defined by [RFC 826] and [RFC 2002].

### 1273 — ARP Cache timeout
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- ARP entries shall be removed after a certain amount of time if not used.
- The timeout shall be configurable and default to 30 minutes.

### 1274 — Local Configurations
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- Configurability of these parameters shall be implemented according to [REQPROD 436145].

### 1275 — ICMP
- 版本：v4 ｜ 验证方式：Analysis ｜ 适用：通用
- RFC 792, RFC 1122 ICMP shall be implemented as specified by [RFC 792] and [RFC 1122].
- The implementation shall include support for ICMP messages of the type stated in the table below.

### 1276 — Internet Protocol Version
- 版本：v5 ｜ 验证方式：Analysis ｜ 适用：通用
- RFC 791 IP-ECUs shall implement IPv4 as specified by [RFC 791].

### 1277 — IP fragmentation
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- To support IP fragmentation RFC 791 IP fragmentation shall be supported according to [RFC 791].

### 1278 — Reassembling fragmented packets
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- To ensure support for reassembling datagrams that are fragmented RFC 815 IP-ECUs shall support reassembling of incoming datagrams that are fragmented according to[RFC 815].

### 1279 — Network identification using network mask
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- To enable identification of the network an IP address belongs to by using thenetwork mask RFC 4632 The network that a specific IP address belongs to shall be identified by the network mask inaddition to the IP address according to [RFC 4632].

### 1280 — Time-to-Live
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- For internal communication, the Time-to-Live, TTL field shall be set to 20 by the sender.
- Forcommunication with external networks the default TTL, 64 shall be used which isrecommended by IANA.
- For these types of datagrams, TTL 10 (TBD) shall be used.

### 1281 — Internal IP Addresses
- 版本：v8 ｜ 验证方式：Test ｜ 适用：通用
- To define that the IP address shall be configurable via a SWDL process.
- RFC 1918, RFC 5735, LC: Diagnostics and ECU Platform, REQPROD 436145 Internal IP addresses shall be configurable.

### 1282 — IP Aliasing
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- IP aliasing shall be supported to enable association of multiple IP addresses for each physical interface.
- The number of IP addresses per interface shall not be limited by software.
- The IP addresses shall be configurable.

### 1283 — IP Network Prioritization
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- RFC 2474, IEEE 802.1p IP-ECUs shall be able to use the prioritize tag (DSCP - DiffServ) of IP packets.
- It shall be possible to configure prioritization for different traffic classes.

### 1284 — TCP Implementation
- 版本：v4 ｜ 验证方式：Analysis ｜ 适用：通用
- RFC 793 Transmission Control Protocol, TCP shall be implemented as specified by [RFC 793].

### 1285 — TCP Keep-ALives
- 版本：v5 ｜ 验证方式：Test ｜ 适用：通用
- RFC 1122 IP-ECUs shall implement and enable TCP Keep-Alive according to [RFC 1122].
- The implementation shall include the parametersKeepaliveTimer,KeepaliveRetriesandKeepaliveFrequency.
- KeepaliveTimeris the time an established connection may be idle before sending the first Keep-Alive probe.

### 1286 — Congestion control
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- To ensure the presence of a congestion control mechanism RFC 896 IP-ECUs shall implement Nagle Algorithm as a mechanism for congestion control as defined in [RFC 896].
- It shall be configurable and be disabled as default.

### 1287 — Congestion control strategies
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- RFC 5681 IP-ECUs shall implemented congestion control mechanisms slow-start, congestion avoidance, fast retransmit and fast recovery as defined in [RFC 5681].
- It shall be possible to enable and disable the features through configuration and the default state shall be disabled.

### 1288 — Graceful TCP Connection Shutdown on ECU Reset
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- - During a reset procedure, an IP-ECU shall close all open sockets and ensure that TCP's connection termination procedure runs to completion before doing the actual reset.

### 1289 — Initial TCP Window Size
- 版本：v6 ｜ 验证方式：Analysis ｜ 适用：通用
- RFC 793, RFC 3390 The initial size of TCP's window shall be set to a value no lesser than the upper bound specified in RFC 3390---around 4K bytes---, and implemented in conformance with [RFC 793].

### 1290 — Internal TCP Connection Establishment
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- From the time a client initiates a TCP connection until the connection is established shall take maximum 2 seconds.

### 1291 — UDP Implementation
- 版本：v4 ｜ 验证方式：Analysis ｜ 适用：通用
- RFC 768 The User Datagram Protocol shall be implemented as specified by [RFC 768].

### 1292 — UDP Checksum
- 版本：v4 ｜ 验证方式：Analysis ｜ 适用：通用
- RFC 768 UDP checksums shall be generated and validated as specified by [RFC 768].

### 1293 — Broadcasts
- 版本：v6 ｜ 验证方式：Analysis ｜ 适用：通用
- RFC 919, RFC 922 IP-ECUs shall support broadcasting as specified in [RFC 919] and [RFC 922].4.3.13 IP Command Protocol4.3.13.1 IP Command Protocol4.3.13.1.1 Appendix4.3.13.1.1.1 Traditional DatatypesTraditional datatypes are supported and may be used: Type Description Size [bit] Remark Boolean TRUE/FALSE 8 FALSE (0x00), TRUE (0x01) Uint8 Unsigned integer 8 0 to 255 Uint16 Unsigned integer 16 0 to 65,535 Uint32 Unsigned integer 32 0 to 4,294,967,295 Sint8 Signed integer 8 -128 to 127 Sint16 Signed integer 16 -32,768 to 32,767 Sint32 Signed integer 32 -2,147,483,648 to2,147,483,647 Float32 Floating point number 32 IEEE 754 binary32(Single Precision) Float64 Floating point number 64 IEEE 754 binary64(Double Precision) String UTF-8 Table: List of supported data types Range/Sign to Data Type Range/Sign Data Type Description 0x00 ...
- Unicode encoding shall UTF-8.
- The interface definition must also define the maximum number of bytes the string (including termination with "\0") can occupy.

### 1294 — Allowed port numbers
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- org/assignments/port-numbers The allowed communication port numbers shall be chosen according the IANA organization and clearly defined which ports shall be used within specification which defines the signal content (IP Command Bus).

### 1295 — IP Protocol Header - TCP usage
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- The IP Command Protocol header shall be used when transporting TCP packets for control and command between ECU's.
- The usage of TCP as transport layer shall be clearly specified in the IP Command Bus.

### 1296 — TCP size usage
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- TCP shall be used for control messages larger than 1400 bytes.

### 1297 — TCP connection establishment
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- The IP based ECU's which shall use TCP as transport layer, shall establish a TCP connection from client to server at startup.
- If the client detects that the TCP connection is not available, it shall re-establish the TCP connection to the server.

### 1298 — TCP server initialization
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- The server shall at startup initialize, open server port and listen on connection attempts.

### 1299 — TCP client startup behaviour
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- The client shall at startup create a socket and try to connect to the server

### 1300 — TCP client re-establishment
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- The client TCP connections re-establish attempts shall be performed every 100ms after a connection attempt has been refused.

### 1301 — IP Protocol Header - UDP usage
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- The IP Protocol header shall be used when transporting UDP packets for control and command between ECU's.
- The usage of UDP as transport layer shall be specified in the IP Command Bus.

### 1302 — UDP checksum
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- The protocol shall be used according to Internetwork specification [Internetworks General Specification], where it's also stated that the usage of UDP checksum is mandatory.4.3.13.1.2.2 Application LayerThe functionalities of the services are offered as a set of operations For example, a service "A" or service "B" offers a set of operations as seen in the figure below.
- Each service shall have a unique identifier and each service operation shall be assigned its unique identifier to distinguish them from one another.
- Figure: Showing relations between services and operationsThis specification does not intend to specify any details on how to protect sensitive data that GEELY Page No513(1572) shall be used.

### 1303 — Protocol header format
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- 1303 v3Protocol header format To define when the IP Command Protocol header shall be used.
- The IP Command Protocol application header format must be used for control and command communication within the vehicle IP-based network and all headers must be encoded with network byte order (big endian) [RFC 791].

### 1304 — DataType
- 版本：v4 ｜ 验证方式：Analysis ｜ 适用：通用
- To define the usage of the DataType-field The DataType is 8 bits long and defines how the sender/receiver shall handle the payload (data field) of the message.
- The data is packed in byte orderoras defined in corresponding SWRS which defines how the data shall be packed.

### 1305 — Length
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- To define that length field is always mandatory The Length parameter is mandatory and shall be included in the IP application messages.

### 1306 — OperationID
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- To define where the unique OperationID identifiers shall be listed.
- The OperationID is allocated by document owner and shall be listed into the signal specifications (IP Command Bus).

### 1307 — OperationTypes
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- To define the operation types that shall be supported by the IP Command Protocol.
- The following table defines the OperationTypes that shall be supported.
- The receiver of a message of this notification type shall respond with an ACK message.

### 1308 — Payload-field packing
- 版本：v4 ｜ 验证方式：Analysis ｜ 适用：通用
- The Payload-field shall be ordered in network byte order (Big-endian) [RFC 791].
- The data shall be defined in the IP Command Bus specification.

### 1309 — Encoded payload - ASN.1
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- Appendix - ASN.1 EXAMPLES If the message shall be encoded according to the DataType 0x00 [REQPROD 346798], the Abstract Syntax Notation One (ASN.1) with PER-unaligned shall be used.
- The default character encoding shall be UTF-8, used by all ASN.1 strings.
- Details of how ASN.1 shall be used is explained in Appendix.

### 1310 — Process-flag, proc
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- 1310 v1Process-flag, proc To define the usage of the process flag The proc -flag is 1 bit and shall have the default value 0x0.
- Messages (with operationIDs) that initiate a time consuming process at the server shall have this flag set to 1 to make the server keep track of the message.
- The proc -flag applies only for messages with operation types Request and SetRequest, since the message flows includes a Response that may take more or less time for the server to send back to the client.

### 1311 — ProtocolVersion
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- 1311 v3ProtocolVersion To define the current version number of the IP Command Protocol. The currently used IP Command Protocol number: 0x03

### 1312 — ServiceID
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- To define where the unique service identifiers shall be listed.
- The ServiceID is allocated by document owner and shall be listed into the signal specifications (IP Command Bus).

### 1313 — SenderHandleID
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- To define how the SenderHandleID shall be used.
- With UDP there is a lack of flow control, to be able to identify messages SenderHandleID shall be used.
- SenderHandleID [32 bits] ServiceID8[8 bits] OperationID8[8 bits] OpType[8 bits] SeqNr[8 bits] The picture above illustrates the way the SenderHandleID shall be constructed to fulfill the required behavior.

### 1314 — SenderHandleID response usage
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- 1314 v4SenderHandleID response usage To define how the SenderHandleID shall be used.
- When generating a response message, after a request message the server shall copy the SenderHandleID from the request message to the response message.
- The SenderHandleID may be reused as soon as the response arrived or is not expected to arrive anymore (timeout).

### 1315 — SenderHandleID usage
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- 1315 v3SenderHandleID usage To define how the applications shall use SenderHandleID to distinguish between different application messages.
- The applications shall use the SenderHandleID and the IP-source address to distinguish between different messages.4.3.13.1.2.2.2 Application Message Format SequencesThis chapter defines the client/server communication within a service, using different OperationTypes.
- Another type of notification is the cyclic notifications, where specified information shall be transmitted to the client in a fixed interval.

### 1316 — Notification types
- 版本：v4 ｜ 验证方式：Analysis ｜ 适用：通用
- [REQPROD 346797] There shall be two types of notifications namely NOTIFICATION and NOTIFICATION_CYCLIC.

### 1317 — Notification message content
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- To define what shall be included in notification messages.
- Any notification message (NOTIFICATION/ NOTIFICATION_CYCLIC) shall contain the latest parameter data.

### 1318 — Dynamic notification request
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- To define how NOTIFICATION_REQUEST shall be implemented.
- If the request is sent as a UDP packet, the application shall wait for the ACK before expecting to receive any notification messages from the service, containing the latest property value.

### 1319 — Cyclic Notification message handling
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- To define how notifications shall be implemented.
- Cyclic Notification messages (operation type 0x06) shall never be followed up with an ERROR message.

### 1320 — UDP Acknowledgment
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- To define when the acknowledgment messages shall be used, using the IP Command Protocol using UDP.
- OperationTypeID OperationTypeName Acknowledge(Yes/No) 0x00 REQUEST Yes 0x01 SETREQUEST_NORETURN Yes 0x02 SETREQUEST Yes 0x03 NOTIFICATION_REQUEST Yes 0x04 RESPONSE Yes 0x05 NOTIFICATION Yes 0x06 NOTIFICATION_CYCLIC No 0x70 ACK No 0xE0 ERROR No ACK messages shall NOT be used for multicast or broadcast messages.

### 1321 — UDP acknowledgment handling
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- [Figure: Message Sequence Format - OperationType Request/Response using UDP] When either the server or the client receives a control message that is expected to be acknowledged, it shall sent the ACK message after a validation check, before processing the message.
- Note: If the client receives the response to a request prior to the expected ACK message, it shall consider the response message as an ACK message, thus continue and acknowledge the response by sending an ACK to the server.

### 1322 — Notifications upon link establishment
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- To define how notifications shall be implemented using UDP or TCP.
- Notification messages shall be setup/started immediately after the link is established, to the subscribers.
- For type NOTIFICATION, the latest/current value shall be sentFor type NOTIFICATION_CYCLIC, transmission shall be done according to the chosen timer-intervals.

### 1323 — Dynamic notification startup behaviour
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- To define how notifications shall be implemented using UDP or TCP in relation to operation type NOTIFICATION_REQUEST.
- When an application is subscribing for notifications dynamically (no matter for which notification type) an initial notification message shall not be sent when “link up” as described for static notifications (as in requirement [REQPROD 346859]).
- In case the application still wishes to receive notifications, it shall send a new NOTIFICATION_REQUEST.

### 1324 — OperationType Notification using UDP
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- To define how static notifications (using OperationType: NOTIFICATION) shall be implemented using UDP.
- The application shall always send at least one successful NOTIFICATION message (ACKmessage must have been received) after the link is established.
- OperationID) on the subscriber side (client) todecide if there shall be a delay before the notification's acknowledge message is sent.

### 1325 — OperationType Notification_Cyclic using UDP
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- 1325 v3OperationType Notification_Cyclic using UDP To define how static notifications (using OperationType: NOTIFICATION_CYCLIC) shall be implemented using UDP.
- The application shall always send at least one NOTIFICATION_CYCLIC message after the linkis established.
- NOTIFICATION_CYCLIC messages shall not be responded to will ACK messages.

### 1328 — OperationType Notification_Request
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- 1328 v3OperationType Notification_Request To define how notifications request (dynamic subscription) shall be implemented.
- [REQPROD 346857], [REQPROD 346859], [REQPROD 346860], [REQPROD 346861], [REQPROD 346862] NOTIFICATION_REQUEST messages shall be followed up with notification messages, which are either using OperationType NOTIFICATION or NOTIFICATION_CYCLIC on a specific service.
- The payload of the message using OperationType NOTIFICATION_REQUEST shall use the following structure: TYPE VALUE8bit 16 bit TYPE defines what kind of subscription action is needed on the server.

### 1329 — Dynamic notification handling
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- To define how notifications request (dynamic subscription) shall be implemented.
- [REQPROD 346857], [IP Prot: 346858] Applications subscribing to notifications dynamically shall consider subscription terminated if the requested service becomesUnavailable(according to requirement [REQPROD 347882]).
- This means that the application must send a new NOTIFICATION_REQUEST message to resume the information flow when the service becomesAvailable.

### 1330 — OperationType Notification_Request using UDP
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- To define how notifications request shall be implemented using UDP.
- If the server receives a faulty/erroneous NOTIFICATION_REQUEST message, the server shall send an ERROR message instead of ACK and send no additional NOTIFICATION messages.

### 1331 — OperationType Notification_Request using TCP
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- To define how notifications request shall be implemented using TCP.

### 1332 — 
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- The message exchange between a client and a server using TCP, the IP Command Protocol and the REQEUST and RESPONSE message shall be implemented according to figure [ Message Sequence Format – OperationType Request/Response using TCP].
- jpg) Page No531(1572) Figure: Message Sequence Format – OperationType Request/Response using UDP Figure: Message Sequence Format – Alternative Request sequence with an Error using UDPA message of type REQUEST may in some cases, depending on underlying function, take enough time before responded to that the client retransmits the message (due to WFR time out).
- In such cases the message shall be constructed with the proc -flag set to 0x1 indicating to the server that the Response may not be available for some time.

### 1334 — UDP SETREQUEST
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- The SETREQUEST shall be implemented according to figure [Message Sequence Format – OperationType SetRequest using UDP].
- Note: If the client sends a SETREQUEST and receives a correct (expected) RESPONSE prior the expected ACK message, the RESPONSE message shall be handled as correct ACK message.
- The client shall then respond with an ACK message on the RESPONSE message.

### 1337 — TCP SETREQUEST_NORETURN
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- When using TCP and sending a SETREQUEST_NORETURN, figure [Message SequenceFormat – OperationType SetRequestNoReturn using TCP] shall be used.
- If the server detects an error in the received message, it shall generate and send back anERROR message which explains the reason for the error.
- jpg) Figure: Message Sequence Format – OperationType SetRequestNoReturn using TCP When using UDP or TCP, a sanity check must be done upon reception to detect errors in the message header.

### 1341 — Concurrent message handling
- 版本：v4 ｜ 验证方式：Analysis ｜ 适用：通用
- An application shall be able to handle multiple incoming and outgoing messages in parallel(concurrently).
- This means that if a application sends a message with OperationType: REQUEST, theapplication shall not only be able to wait for the ACK_, RESPONSE or ERROR message, buthandle multiple incoming/outgoing messages at the same time.

### 1342 — Minimum concurrent message sequences
- 版本：v4 ｜ 验证方式：Analysis ｜ 适用：通用
- To define the minimum concurrent sequences The server shall be able to handle at minimum 10 (TBD) messages (opearationIDs)concurrently.

### 1343 — Concurrent message sequences, busy
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- To define the behaviour if all slots are busy If the server is concurrently handling the maximum number of messages required in[REQPROD 347045], it shall respond with an ERROR message using the ErrorCode busy (see table in [REQPROD 347068]), to any new incoming messages.

### 1344 — Error message, Processing
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- [REQPROD 381652] If the server is busy processing an operationID requested with the proc -flag (decribed in [REQPROD 381652]) set to 0x1 and the same operationID is requested within a new message, it shall drop the newly received message and respond with an ERROR message using the ErrorCode processing (see table in [REQPROD 347068]).4.3.13.1.2.3.1 Retransmission of messagesIf the network is congested and many messages are dropped, retransmissions might create even more load into the system (so more messages will be dropped or delayed).

### 1345 — Retransmission formula
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- To define the retransmission formula which shall be used for WFA and WFR The following retransmission formula shall be used.
- increaseTimerValueWFA = 1,5increaseTimerValueWFR = 2· If the client has performed maximum allowed retries and failed due to WFA timeouts, both the WFA timer/counter and the WFR timer/counter shall be restored to default values.· Upon a reset of the devices or reception of appropriate acknowledgment (ACK) or response (RESPONSE), the application shall load the default defaultTimeoutWFA and defaultTimeoutWFR timer values.·usedTimeoutWFx = defaultTimeoutWFxIt's then up to the application to decide if it should restart the transmission trials or not.

### 1346 — WFA retransmission using UDP
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- If UDP is used, there shall be a retry counters which counts the maximum number of WFA-retransmissions.
- The retry counter shall be set to:· numberOfRetriesWFA = 7 Retransmissions of event based messages (operation type 0x05) shall be done a maximum of numberOfRetriesWFA times but only until an event triggers a new transmission, in which case the retransmission mechanism is canceled and reset to default values.

### 1347 — WFR - Signal specific
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- It shall be possible to specify the defaultTimeoutWFR and numberOfRetriesWFR values uniquely per IP Command Bus signal, in which the default values are replaced with values specified in the corresponding SWRS and SRD only for the specific signal.

### 1348 — WFR retransmissions using UDP and TCP
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- There shall be a retry counters which counts the maximum number of WFR-retransmissions.
- The retry counter shall be set to: numberOfRetriesWFR = 2More information about retransmission formula is stated in [REQPROD 347050].

### 1349 — WFx - configurable parameters
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- To define parameters that must be configurable.
- The following parameters shall be configurable in the Local Configuration File: defaultTimeoutWFAdefaultTimeoutWFRnumberOfRetriesWFAnumberOfRetriesWFRincreaseTimerValueWFA Figure: Timers allocation on the OSI-model ACKNOWLEDGEMENT TIMER (WFA) The "Wait-For-Acknowledgement" (WFA) timer is used whenever a sender sends a message as UDP packets.
- The WFA timer shall be used to regulate the amount of time that the application shall wait on an acknowledgment message before resending (more info about retransmission can be found in chapter [Retransmission of messages]).

### 1352 — WFA timer handling
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- A client/server sending a control message (UDP) shall start a WFA timer which counts down until an ACK message is received or the timer value has expired.
- If the sender application does not receive an ACK message within the defined WFA time, the application shall retransmit the control message.

### 1353 — Default WFA value
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- The default acknowledgment timeout value shall be named, defaultTimeoutWFA.
- This timer shall be set to 500 milliseconds as default value.
- Note: The defaultTimeoutWFA value shall be adjustable via a local configuration file within each ECU that uses the IP command bus.

### 1354 — Default WFR value
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- The default response timeout value shall be named defaultTimeoutWFR.
- This timer shall be set to 1 second as default value.
- Note: The defaultTimeoutWFR value shall be adjustable via a local configuration file within each ECU that uses the IP command bus.

### 1355 — WFR reset to default value
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- To define how a retransmission shall be implemented using the WFR timers, when either UDP or TCP is used.
- If the application is restarted or the transmission has been a success (response-received), the default response timeout value (defaultTimeoutWFA) shall be used.

### 1356 — WFR timers using TCP
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- To define how the applications shall handle the WFR timer, when TCP is used as transport protocol.
- When TCP is used, the WFR timers shall be implemented as the following: On the client side, before sending a REQUEST (or SETREQUEST) message, the application shall start the WFR-timer.
- When the RESPONSE message is received, the WFR-timer shall be terminated.

### 1357 — WFR implementation using UDP
- 版本：v4 ｜ 验证方式：Analysis ｜ 适用：通用
- To define how the applications shall handle the WFR timer, when UDP is used as transport protocol.
- When UDP is used, the WFR timers shall be implemented as the following: On the client side, when a REQUEST (or SETREQUEST ) message have been sent, the application shallafter receivingthe ACK message start a WFR-timer.
- If a RESPONSE message is received, the WFR-timer shall be terminated.

### 1358 — WFR timeout handling
- 版本：v4 ｜ 验证方式：Analysis ｜ 适用：通用
- To define how a retransmission shall be implemented using the WFR timers, when UDP is used.
- This following sequence shall be implemented for the an WFR-timeout;1.
- An error message containing Error Code 0x01 shall be used in this example.

### 1359 — Error message error codes
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- An ERROR message shall use the following ErrorCodes and ErrorInformation.
- Table: List of general Error Codes In cases when there are more than one error in the message only one ERROR message shall be send back to the transmitter with the most prioritized error code, according to the following list.

### 1360 — Error message payload
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- To define the structure of a error message An ERROR message payload shall be designed as the following: ErrorCode[8 bits] ErrorInformation[16 bits]

### 1361 — Error message structure
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- To define the structure of an error message An ERROR message shall always use the IP Command Protocol header including ServiceID,OperationID, SenderHandleID and the Length.
- Instead, this document defines the rules on how to the control communication shall be handled between the applications.
- This document shall be used together with the corresponding signal document (for a specific project) which defines the signal content (the actual application data).4.3.13.1.3.1 Abbreviations & Definitions Abbr.

### 1365 — ECU wakeup detection
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- To define how to handle the vehicle bus ECU wakeup signal When the property ResourceGroup = RG_X is detected on the vehicle bus ECU wakeup signal in [REQPROD 347897]), and the X in RG_X refers to the Resource Group number which the LM module is a member of according to [REQPROD 347895], the following shall happen: Initialize the vehicle internal IP bus according to chapter [Link Manager - Initialization], once the ECU has started.

### 1366 — Wakeup of internal IP Bus
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- To define how to wake up the vehicle internal IP bus via the vehicle bus The IP Wakeup VFC shall be implemented according to the following description.
- VFCTimeOutDelay = 3 sec Time out after 3 seconds Note: (Timers)Deactivation criteria consisting of a VFCTimeOutDelay indicate that each VFC activation shall reset a timer called VFCTimeOutDelay.
- The VFC shall be deactivated when the entire expression is true.

### 1367 — Vehicle bus signal
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- To define the content of the vehicle bus signaling A Vehicle_bus_ECU_wakeup signal with content "" shall be used as wakeup signal when the vehicle internal IP bus is not available.
- During multiple simultaneous requests,parameter shall always be set to PRIO_HIGH if any request has= PRIO_HIGH.

### 1368 — VFC IP wakeup
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- VFC "IP Wakeup" shall be activated, see [REQPROD 347896]2.
- ResourceGroup = RG_X, Prio = shall be set in the Vehicle_bus_ECU_wakeup signal as long as VFC "IP Wakeup" is activated, and then return to default values as specified in [REQPROD 347897].

### 1369 — IP Bus release
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- If no RG is requested the parameters shall assume the default values ACTION = AVAILABLE, PRIO = PRIO_NORM([REQPROD 347120]).
- Figure: Example showing the scenario when one LM instance requests to keep alive the IP Bus while the other only broadcasts availability.1370 v5 IP Bus request To define how to request the vehicle internal IP bus When the vehicle internal IP bus (by RG) is requested by an LSC withand the ECU is ready to send IP_activity messages, the LM module shall: Check if the vehicle internal IP bus already is up, if it is go to step 3.
- The LM module shall start broadcasting the IP_activity message periodically once every second after it has been initialized according to [REQPROD 347878].

### 1372 — LM initialization
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- To define the order in which services and the LM module shall be initialized at ECU startup.
- At ECU startup, the LM module shall be initialized afterall preconfigured services have been started and ready to process received messages.
- All previous data shall be flushed during initialization.

### 1373 — LCS IP Bus release
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- To state that an LSC shall be able to request to release the vehicle internal IP bus.
- LSCs shall be able to inform the local LM instance that the vehicle internal IP bus is not needed by the LSC anymore.
- If LM sees that the IP bus is no longer requested by any LSC it shall exit the OR state.

### 1374 — LSC IP bus request
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- To state that an LSC shall be able to request the vehicle internal IP bus.
- LSCs shall be able to request the local LM instance to start the complete vehicle internal IP bus or the part required for a given RG.
- Such request shall make the LM enter the OR state.

### 1375 — LSC notifying
- 版本：v4 ｜ 验证方式：Analysis ｜ 适用：通用
- To define which information the LM module shall provide to LSCs.
- It shall be possible for an LSC to be notified if the requested RG is Available, Partly available or Unavailable.
- Note: An LSC may choose to try using the IP network even if the requested RG only is partly available.

### 1376 — Software interface
- 版本：v4 ｜ 验证方式：Analysis ｜ 适用：通用
- The LM module shall offer Local Software Components, LSCs an interface (visualized in figure [Showing ECU local interface between an LSC and the LM module]) for determining whether there exists any ARSs or ORs and if any of them has the property PRIO_HIGH (explained in [REQPROD 347120]).
- The LM module shall also offer information about the currently requested Resource Groups .

### 1377 — Active Request Session
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- Active Request Session, ARS shall be implemented according to the following definition.
- Whenever an IP_activity message is received, with ACTION-field = AVAILABLE | REQUEST_RG_X an ARS shall be set for the IP link.
- A new ARS must include priority information about the request.

### 1378 — ARS timers
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- The LM module shall implement one timer for each Active Request Session, ARS.
- This timer shall assume the value given by Request_monitoring_timeout.
- The timer shall start when the LM module has registered an ARS upon reception of the IP_activity message.

### 1379 — Number of Nodes in RG
- 版本：v5 ｜ 验证方式：Analysis ｜ 适用：通用
- The constants Number_of_Nodes_in_RG_X, where X is a number 1 – 7, shall be implemented and specified in the Local Configuration File.

### 1380 — Ongoing Request
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- During the OR state, if the request has high priority, normal power management shall be ignored.

### 1381 — Request Monitoring Timeout
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- The LM Module shall implement the configurable variable Request_monitoring_timeout, RMT.
- The parameter shall be configurable (with range 1.5 to 8 seconds and precision of 100ms) via the Local Configuration File.
- Default value shall be 3 seconds.

### 1382 — Resource Groups
- 版本：v4 ｜ 验证方式：Analysis ｜ 适用：通用
- ResourceGroup shall be implemented as a bit field of 1 byte, thus being able to represent an ECU as member of multiple Resource Groups.
- It shall be configurable in a Local Configuration File.
- Decoding of ResourceGroup shall be performed according to the following table.

### 1383 — LM broadcast
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- To define how the LM messages shall be sent among the ECUs.
- IP_activity messages shall use the subnet-directed broadcast.

### 1384 — LM IP_activity message
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- To define that LM messages shall use the IP Command Protocol All LM IP_activity messages shall use the IP Command Protocol and shall have the following properties: ServiceID (16 Bits): 0xFFFF.

### 1385 — LM IP_activity message structure
- 版本：v5 ｜ 验证方式：Test ｜ 适用：通用
- To define the LM (IP_activity) message structure The following structure shall be used when constructing the LM IP_activity message, and shall be followed directly after the IP Command Protocol Header as shown below in below figure [IP Link Manager Header].
- Note: The ACTION-field shall be implemented as a bit-field, which can take on values representing all combinations of the bits addressed.
- The AVAILABLE-bit indicates the availability of the services and shall be set when all services are available.0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31IP Command Protocol HeaderACTION [8 bit] PRIO [8 bit] Reserved [16 bit]Header fields: ACTION: Values Name Description0x01 AVAILABLE Services on local ECU are available to use.0x02 REQUEST_RG_1 Request at least one service on Resource Group 1.0x04 REQUEST_RG_2 Request at least one service on Resource Group 2.0x08 REQUEST_RG_3 Request at least one service on Resource Group 3.0x10 REQUEST_RG_4 Request at least one service on Resource Group 4.0x20 REQUEST_RG_5 Request at least one service on Resource Group 5.0x40 REQUEST_RG_6 Request at least one service on Resource Group 6.0x80 REQUEST_RG_7 Request at least one service on Resource Group 7.

### 1386 — Port
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- IP_activity messages shall be sent using software port number 50001.

### 1387 — Transport Protocol
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- To define the LM protocol IP_activity messages shall be based on IP Command Protocol over UDP.

### 1388 — Local Configuration file
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- To define the locally configurable parameters for this specification, [LC : IP Link Manager] The parameters stated in the following table shall be implemented and configurable on each ECU that deploys a LM.
- A Page No575(1572) reason for this may be limiting the time for software download during car assembly in factory and in workshop.
- External equipment which may connect to the vehicle network in a controlled way.

### 1389 — Local configuration data file content
- 版本：v5 ｜ 验证方式：Analysis ｜ 适用：通用
- Configurations shall be done according to [REQPROD 436145].
- The parameters stated in the following table shall be implemented and configurable on each router ECU.
- Parameter DataType DescriptionIf the project has requested the usage of DHCP and reserved IP addresses, it shall be possible to map MAC address with a IP address.

### 1390 — Local Configuration Tool
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- The Local Configuration Tool shall use highest possible security when accessing the router ECU.

### 1391 — Firewalling rules
- 版本：v8 ｜ 验证方式：Analysis ｜ 适用：通用
- The ECU shall implement a firewall with a firewall rules ensuring that only desired IP traffic is allowed to the ECU itself and between different ip interfaces connected to the ECU.
- It shall be possible to configure firewall rules based on information such as transport protocol, source address, destination address, source port and destination port to control ingress and egress traffic.
- The default state of the firewall shall be to block all traffic not explicitly allowed by firewall rules.

### 1392 — Interface Traffic limitation
- 版本：v6 ｜ 验证方式：Test ｜ 适用：通用
- Router ECUs shall support bandwidth limitation for all interfaces according to table [Traffic rate classification].
- All parameters shall be configurable.

### 1393 — IP Broadcast Address Limitation
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- RFC 1812 Broadcast addresses of the form (,, 0) including 0.0.0.0 are obsolete, thus shall be discarded.

### 1394 — IP NAT
- 版本：v6 ｜ 验证方式：Analysis ｜ 适用：通用
- RFC 3022 Router ECUs with a WAN connection shall implement a Traditional IP Network Address Translator, Traditional NAT according to [RFC 3022].
- Note: The NAT shall be able to handle IPv6 from external networks.

### 1395 — IP Traffic handling
- 版本：v5 ｜ 验证方式：Analysis ｜ 适用：通用
- All ingress IP traffic must pass a firewall, which performs a validation check and the router ECU is responsible for the access control between the networks.

### 1396 — NAT support for SIP
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- RFC 3261 It shall be possible to configure the router ECU's firewall to allow the Session Initiation Protocol, SIP traffic from external sources.
- Default state shall be Enabled.

### 1397 — Port Forwarding
- 版本：v5 ｜ 验证方式：Test ｜ 适用：通用
- RFC 3022 Static Port forwarding shall be implemented and configurable with the following parameters.

### 1398 — DHCP - IP Reservation Table
- 版本：v7 ｜ 验证方式：Test ｜ 适用：通用
- REQPROD 264356 A DHCP server running on any router ECU shall support IP addresses reservation for Nomadic Devices based on their MAC addresses.
- It shall be possible to configure the IP Address Reservation table.

### 1399 — IP Implementation
- 版本：v5 ｜ 验证方式：Analysis ｜ 适用：通用
- LC: Internetworks General Specification IP routers shall implement the protocol stack according to [LC: Internetworks General Specification].

### 1400 — IP Multicast
- 版本：v5 ｜ 验证方式：Analysis ｜ 适用：通用
- RFC 3376 The router ECU shall support forwarding of IP Multicast messages.

### 1401 — IP Multicasting Protocol
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- RFC 3376, RFC 4606 The router ECU shall support Internet Group Management Protocol, IGMP version 3, to maintain host group membership on a local network.

### 1402 — IPv4 router implementation
- 版本：v5 ｜ 验证方式：Analysis ｜ 适用：通用
- RFC 1812, RFC 6633, RFC 2644 The design and implementation of a router ECU shall follow the requirements according to [RFC 1812], [RFC 2644] and [RFC 6633].

### 1403 — Routing Table Content
- 版本：v5 ｜ 验证方式：Analysis ｜ 适用：通用
- 1403 v5Routing Table Content To ensure that the router ECUs have the necessary data to be able to make a forwarding decision RFC 1812 A routing table shall at least contain the following: Network Destination, Netmask, Gateway, Interface.
- The routing table shall have the capacity to hold 5K routes.

### 1404 — Static Routing
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- RFC 1812 A router ECU shall support configuration of static routes.

### 1405 — Throughput
- 版本：v6 ｜ 验证方式：Test ｜ 适用：通用
- The minimum throughput of a router ECU shall be at least 90 percent of the max bandwidth (full duplex) at Layer 3.

### 1406 — Dual Stack
- 版本：v5 ｜ 验证方式：Test ｜ 适用：通用
- RFC 2893 Dual stack support shall be implemented on the router ECU that may receive an IPv4 and/or IPv6 address from e.

### 1407 — Translation
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- RFC 3142 The router ECU that implements a dual stack according to [REQPROD 55042] shall also implement a translation mechanism to translate external IPv6 traffic into IPv4 traffic.

### 1408 — Link Monitoring
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- REQPROD 352558 The router shall implement a feature to monitor the quality of each interface.
- The Link Monitoring shall set a number of counters defined in the table below: Parameter Description Example of trigger conditions Tx Packets Number of transmitted packets The router sends/forwards a packet.

### 1409 — Link Monitoring - ECU reboot
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- REQPROD 352480 The link-monitoring counters described in [REQPROD 352480] shall be reset when the router ECU is rebooting.

### 1410 — Link Monitoring - logging
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- REQPROD 352480, REQPROD 352558 When the link-monitoring feature is enabled, it shall be possible to store all link-monitoring parameters per interface into a log-file.
- The log-file shall be of the type ringbuf with a max size of 10MB.
- The size shall be configurable.

### 1411 — Link Monitoring Accessibility
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- REQPROD 352480 Link Monitoring parameters shall be accessible for analysis via an Analysis Tool, which the supplier shall deliver.

### 1412 — Link Monitoring Activation
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- REQPROD 352480, REQPROD 352558 Two triggers for writing the link-monitoring information of [REQPROD 352480] shall be implemented.
- The default state shall be disable.

### 1413 — QoS rules
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- It shall be possible to set up QoS rules to distinguish different types of IP traffic and prioritize them accordingly.
- The QoS rules shall be a combination of the parameters in the table below.
- It shall be possible to enable and disable the QoS rules via a configuration.

### 1414 — Traffic Classification
- 版本：v8 ｜ 验证方式：Analysis ｜ 适用：通用
- A router ECU shall be able to understand and handle prioritization of RX and TX traffic.
- Figure [Traffic Classification coverage] below shows the layers at which it shall be possible to create traffic classification rules.
- Traffic classification shall be configurable.

### 1415 — Traffic Shaping
- 版本：v6 ｜ 验证方式：Analysis ｜ 适用：通用
- REQPROD 54931 The router ECUs shall implement a traffic shaper that understands and handles traffic classifications stated in [REQPROD 54931].
- Legacy ID: IP Fragmentation shall be forbidden.
- Legacy ID: IP Option shall be forbidden.

### 1416 — Fragmented ICMP
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- Fragmented ICMP packets shall be blocked without further analysis.

### 1417 — General Security
- 版本：v4 ｜ 验证方式：Analysis ｜ 适用：通用
- To ensure that the network is protected against attacks which may have a significant negative impact on the performance.
- The router ECUs shall use a firewall to protect the vehicle network from attacks which may have a negative impact on performance.
- Since the library of attacks is constantly expanding, it's impossible for to define all possible attacks that may affect the network performance negatively.

### 1418 — Ingress IP source spoofing
- 版本：v6 ｜ 验证方式：Test ｜ 适用：通用
- RFC-2827, REQPROD 76545 Router ECUs shall block ingress packets with a source IP address of an internal ECU according to [REQPROD 76545].

### 1419 — IP Broadcast storms
- 版本：v5 ｜ 验证方式：Test ｜ 适用：通用
- The router ECU shall be able to identify a broadcast storm, disable the subjected interface and re-enable the interface again after 1000 ms.
- When the interface is re-enabled and if a broadcast storm is still ongoing, the interface shall be disabled and once again enabled after a time configured as a back-off timer.

### 1420 — MAC Filtering
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- Router ECU shall support MAC filtering based on both source and destination MAC addresses.
- The MAC filtering rules shall be configurable.

### 1421 — Port Scan Protection
- 版本：v6 ｜ 验证方式：Test ｜ 适用：通用
- The router ECU shall support protection from port scanning.

### 1422 — Replay Attacks
- 版本：v5 ｜ 验证方式：Analysis ｜ 适用：通用
- RFC 1812 section 4.3.3.8 The router ECU shall implement protection against replay attacks.

### 1423 — Source record routing
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- RFC-1812 Source record routing shall not be supported.

### 1424 — Stateful Packet Inspection
- 版本：v5 ｜ 验证方式：Analysis ｜ 适用：通用
- Stateful Packet Inspection shall be implemented for TCP in the router ECUs to keep track of the state of the TCP connections.
- Default session idle timeout shall be 3600 seconds for TCP.
- UDP traffic direction shall be inspected and return traffic shall only be allowed in a configurable timeframe to create a TCP session like behavior.

### 1425 — Denial of Service Protection
- 版本：v6 ｜ 验证方式：Test ｜ 适用：通用
- REQPROD 76545, REQPROD 55067 The router ECU shall support protection against common denial of service attacks using methods as RED Random Eatly Detection and SYN Cookies.
- Both IPv4 and IPv6 traffic shall be protected.
- The following command example limits ICMP responses on interfaces:!icmp {permit\deny} ip_address net_mask [icmp_type] if_name!UDP FloodsExcessive port Scanning: Protection solution is in [REQPROD 55067]All tuning parameters and tresholds shall be able to alter through a local configuration file.

### 1426 — Active Session Monitoring
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- It shall be possible to trace full details on IP traffic on the router ECU based on the parameters stated in the table below.
- If QoS Engine is activated (Local Configuration File), the given priority value of the packets shall be presented where smallest number is the highest priority.
- TCP State for sessions: SS: SYN Sent (a start of a new connection)EST: Established (the connection is passing data)FW: FIN Wait (a request that the connection shall be stopped)CW: Close Wait (a request that the connection shall be stopped)TW: Time Wait (waiting for a short time while a connection that was in FIN Wait is fully closed.

### 1427 — Transport layer
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Define the transport protocol to use Page No600(1572) LIN Transport layer specification Diagnosable and/or re-programmable LIN slaves shall support the transport protocol specified in [LIN_TP_1] LIN Specification Package with the restrictions/additions as defined in this document.
- If there are diagnosable and/or re-programmable LIN slaves on a LIN network the LIN master shall support the transport protocol specified in [LIN_TP_1] LIN Specification Package with the restrictions/additions as defined in this document.4.3.17.1.1.1 LIN Generic requirements

### 1428 — LIN master N_Cs performance in programming session
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- In programming session a LIN master shall have a performance N_Cs = 10ms and allowed jitter is defined in [LIN_TP_2] LIN Datalink Layer - Master requirements.

### 1429 — LIN master usage of N_Cr
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The LIN master shall not time out N_Cr transport protocol timer on first frames (FF).

### 1430 — Block size
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- The LIN protocol does not have a flow control which the LIN slave can use to pause a message reception so the size of the LIN slave message buffer shall not limit the size of supported diagnostic services.
- The LIN slave Rx message buffer shall be large enough to handle any diagnostic request the LIN slave is required to handle.
- Note that if possible the LIN slave may implement a strategy where earlier received data is freed to make room for new data and thus lowering the need for buffer.

### 1431 — LIN slave proceed with current message if receiving an invalid frame
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The diagnostic communication shall not be affected by invalid frames on the protocol level.
- If an segmented diagnostic reception is ongoing, the slave node shall proceed with the reception after:• Reception of an invalid frame (failure in header, checksum error, framing error).
- a frame that was intended to be an application frame but was corrupted for any reason shall not disturb diagnostic communication.

### 1432 — LIN slave receiving a new message while processing a message
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- If LIN master for some reason do not read a response for a request which has been sent to a LIN slave and for which the LIN slave has a response available, it shall be possible to make a new try to communicate with LIN slave by sending a new request.
- The LIN slave shall the discard the response not read and accept the new request and process it.
- The slave node shall abort processing of a diagnostic request (discard any response if such was already prepared) that was correctly received after: Reception of a valid master requestReception of a master request that is valid concerning the LIN protocol, but with absurd data, e.

### 1433 — Use data frame by frame
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- The transport protocol shall send frame by frame to upper layer for diagnostic service TransferData 0x36 (optional for all other services).
- Note that this contradicts normal specified transport layer behaviour since normal transport layer behaviour states that the transport layer shall only send complete messages to upper layers.4.3.17.1.2 IntroductionThis document describes OEM specific adaptations for the LVDS control transport layer specification.
- This implies that when this document refers to multiple slaves in the network it shall be interpreted as one slave.

### 1474 — Local Config Data File
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- To be able to tune and change WLAN device / application behavior without the need of recompile the source code, uses a concept of Local Config Data file which contains default values which shall be used by the WLAN device at startup.
- Figure: Startup process of ECU using Local Config Data FileThe structure of the Local Configuration Data file shall be:[WLAN][Parameter] ..

### 1475 — WLAN software requirements
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- To clarify where the WLAN requirements are stored. [WLAN 1], [WLAN 2], [WLAN 3], [WLAN 4],[WLAN 5] It's required that the supplier implementing the WLAN functionality handles all WLAN specifications, I. E. tha following chapters of the Base Technology DPR/SWRS

### 1476 — AP transits to offline
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- [WLAN Ex 6] The AP must send de-authentication packet to all connected STA(s) before the AP goes offline.

### 1477 — Apple Device Information Element (IE)
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- [WLAN Ex 6] When AppleCarplay is used, the WLAN AP must support and include the Apple Device IE according to source reference.
- The WLAN transceiver must include the Apple Device IE in Beacon, Probe response and Association response frames at all times during the operation of WLAN AP.

### 1478 — AppleCarPlay PowerSave
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- [WLAN Ex 6] When Apple nomadic device transmits a null data packet with PM Bit set (entering 802.11 power save mode), the WLAN AP must ACK the null data packet and must flush the Tx hardware queue for that wireless client (STA) therefore not transmitting any additional packets to the Apple nomadic device.

### 1479 — IEEE 802.11 Management frames
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- 1479 v1IEEE 802.11 Management frames The AppleCarplay specification requires that a set of specific data is used inthe IEEE 802.11 management frames (Probe responses and Beacon frames)when AppleCarplay is used. [WLAN Ex 6] The AppleCarPlay specification requir

### 1480 — Interworking Information Element (IE)
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- [WLAN Ex 6] For AppleCarplay functionality, the WLAN transceiver must include the IEEE 802.11 Interworking IE in Beacon, Probe response and Association response frames at all times during the operation of WLAN AP.
- The AP must set the following fields:"Access Network Options" field - must be set based on the availability of Internet Connectivity."Venue Info" field - must be set to 10 (Vehicular).
- The Venue Type code must be set to one of the values that corresponds to Venue Group code 10 (0-255) as defined in IEEE Std.

### 1481 — Power Save Operation
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- [WLAN Ex 6] When Apple Carplay is used, the WLAN AP must be configured for a power save operation using a DTIM value of one (1).

### 1482 — Track or filter Apple devices
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- [WLAN Ex 6] The WLAN application must not implement any policy that tracks or filters Apple devices based on Wi-Fi MAC addresses.

### 1483 — WFA Wireless Multimedia
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- [WLAN Ex 6],[WLAN 1], REQPROD 54722 The WLAN AP must support the WFA Wireless Multimedia (WMM) Quality of Service (QOS) mechanism.4.3.18.1.2.2 Configuration & Debug Capabilities

### 1484 — AP - SSID Length
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- REQPROD 58128, [WLAN Ex 2] The SSID shall use at minimum 6 octets and at maximum 32 octets, when the WLAN transceiver is configured as AP.

### 1485 — Minimum Debug Capabilities
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- To define a set of minimum debug capabilities At minimum, it shall be possible to monitor (online analysis): Used FrequencyUsed channelSSID (if connected)Data rate (Bitrate)MAC address of BSSIDSNRPERLink Level (RSSI)Link Noise Link Quality for a specific BSS when connectedTx-powerMissed beaconDiscarded packetsSecurity Credentials

### 1486 — Service Set ID - SSID
- 版本：v6 ｜ 验证方式：Test ｜ 适用：通用
- The default SSID shall not reveal the identity of owner by the name and shall be according to criteria specified below.
- MyCar-[xxxxxx]Dual Band support?IF the transceiver supports Dual Band, it shall be possible to set one additional default SSID, one for each frequency band if required by applications (HMI).
- In such use-cases where Local Config parameter SSID, shall be used for 2.4GHz and Infrastructure BSS is used on both bands, a second Local Config parameter shall be used for 5GHz, named: SSID_5GHz.

### 1487 — Transmit Power
- 版本：v6 ｜ 验证方式：Analysis ｜ 适用：通用
- To fine tune Maximum Transmit Power of WLAN transceiver causing least emissions outside of vehicle [WLAN Ex 2], [WLAN Ex 3] Maximum transmit power shall be adjusted to be compatible with local regulatory regulations.
- It shall be possible to set maximum transmit power for each modulation with a resolution (power step) of 1 dBm.
- This setting shall be available via Local Config File (REQPROD 97421)

### 1488 — WLAN transceiver debug mode
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- To perform RF test using Anritsu WLAN tester [WLAN Ex 2] It shall be possible to enable debug mode on WLAN transceiver to enable them to connect to WLAN testers to perform RF parameter testing.4.3.18.1.2.2.1 Configurable MIBs

### 1489 — Access to terminal
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- To provide easy way to configure and read MIB parameters On Engineering/Development software, it shall be possible to read, write and modify MIBs via a terminal application on a Console or a PC.

### 1490 — Association Response timeout limit
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- To be able to provide good usability [WLAN Ex 2] It shall be possible to get and set dot11AssociationResponseTimeout MIB attribute.
- It shall be possible to set AssociationResponseTimeout via Local Config file (REQPROD 97421).
- It shall be possible to read, modify and write dot11AssociationResponseTimeout as per REQPROD 355456.

### 1491 — Authentication Response timeout limit
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- To be able to provide good usability [WLAN Ex 2] It shall be possible to read and set, dot11AuthenticationResponseTimeout MIB attribute.
- It shall be possible tosetAuthenticationResponseTimeout via Local Config file (REQPROD 97421).
- It shall be possible toread, modify andwdot11AuthenticationResponseTimeout as per REQPROD 355456.

### 1492 — Beacon Interval
- 版本：v5 ｜ 验证方式：Analysis ｜ 适用：通用
- To control how often Beacons are sent by AP in the BSS [WLAN Ex 2] The Beacon Interval shall be adjustable.
- It shall be possible to configure Beacon interval via Local Config File (REQPROD 97421).

### 1493 — CTS-to-self
- 版本：v6 ｜ 验证方式：Analysis ｜ 适用：通用
- To avoid hidden node problems and to set NAV distribution feature [WLAN Ex 2] Transmission and Reception of CTS-to-self frames shall be supported to help against hidden node problems and for NAV distribution feature.
- It shall be possible to enable/disable CTS-to-self frame usage via Local Config file (REQPROD 97421).

### 1494 — Domain capability
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- [WLAN Ex 2] It shall be possible get and set dot11MultiDomainCapabilityActivated MIB attribute.
- Example: If dot11MultiDomainCapabilityActivated is set to true, and the WLAN transceiver configured as STA is joining an infrastructure BSS and receives a Beacon or Probe Response frame containing a Country element, the PHY shall adopt to the regulatory domain.

### 1495 — DTIM Interval
- 版本：v6 ｜ 验证方式：Analysis ｜ 适用：通用
- To fine tune balance between throughput of BSS and amount of buffering required for multicast and broadcast frames on WLAN AP [WLAN Ex 2] The DTIM Interval shall be supported and the interval shall be adjustable.
- It shall be possible to set DTIM Interval via Local Config File (REQPROD 97421).

### 1496 — Failed count
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- [WLAN Ex 2] It shall be possible to get dot11FailedCount MIB attribute It shall be possible to read dot11FailedCount as per REQPROD 355456.

### 1497 — Fragmentation Threshold
- 版本：v5 ｜ 验证方式：Analysis ｜ 适用：通用
- To be able to tune fragmentation threshold after field testing results [WLAN Ex 2] The Fragmentation Threshold shall be adjustable.
- It shall be possible to set Fragmentation threshold via Local Config File (REQPROD 97421).
- Default value: 2346It shall be possible to read, modify and write Fragmentation threshold as per REQPROD 355456.

### 1498 — Long retry limit
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- To be able to tune number of retransmission attempts [WLAN Ex 2] It shall be possible to get and set dot11LongRetryLimit MIB attribute.
- It shall be possible to set Long Retry Limit via Local Config file (REQPROD 97421)It shall be possible to read, modify and write dot11LongRetryLimit as per REQPROD 355456.

### 1499 — MAC statistics
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- To enable possibility for monitoring MAC layer performance [WLAN Ex 2] It shall be possible to read dot11MACStatistics group MIB attribute.
- It shall be possible to read dot11MACStatistics group MIB attribute as per REQPROD 355456.

### 1500 — Max transmit MSDU Lifetime
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- [WLAN Ex 2] It shall be possible to get and set dot11MaxTransmitMSDULifetime MIB attribute.
- It shall be possible to set Max transmit MSDU lifetime via Local Config file (REQPROD 97421).
- It shall be possible to read, modify and write dot11MaxTransmitMSDULifetime as per REQPROD 355456.

### 1501 — Multi domain capability
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- To require multidomain support capability [WLAN Ex 2] dot11MultiDomainCapabilityImplemented MIB shall be set to true.

### 1502 — Retry Count
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- [WLAN Ex 2] It shall be possible to read below MIB attributes:· dot11RetryCount· dot11MultipleRetryCountIt shall be possible to read dot11RetryCount and dot11MultipleRetryCount as per REQPROD 355456.

### 1503 — RTS CTS
- 版本：v6 ｜ 验证方式：Analysis ｜ 适用：通用
- [WLAN Ex 2] It shall be possible to read and set dot11RTSThreshold MIB attribute.
- It shall be possible to set RTSThreshold via Local Config file (REQPROD 97421).
- It shall be possible to read, modify and write dot11RTSThreshold as per REQPROD 355456.

### 1504 — Short retry limit
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- To be able to tune number of retransmission attempts [WLAN Ex 2] It shall be possible to get and set dot11ShortRetryLimit MIB attribute.
- It shall be possible to set Short Retry Limit via Local Config file (REQPROD 97421).
- It shall be possible to read, modify and write dot11ShortRetryLimit as per REQPROD 355456.4.3.18.1.2.2.2 Local Configuration Data

### 1505 — Local Configuration Data
- 版本：v7 ｜ 验证方式：Test ｜ 适用：通用
- 65536)This attribute specifiesREQPROD 58121the current maximumsize, in octets, of theMPDU that may bedelivered to the securityencapsulation.

### 1506 — Error Handling
- 版本：v5 ｜ 验证方式：Analysis ｜ 适用：通用
- if possible this functionality shall be used to diagnose the errors.
- [WLAN Ex 2], [WLAN Ex 3] It shall be possible to perform analysis on the WLAN transceiver (settings, registers) by usage of a Local Config Tool or a Local Analysis Tool.4.3.18.1.2.4 Functional Requirements4.3.18.1.2.4.1 Mode Requirement

### 1507 — Mode Requirement
- 版本：v6 ｜ 验证方式：Test ｜ 适用：通用
- [WLAN Ex 2] A WLAN transceiver used in a vehicle shall support operation mode AP and STA.

### 1508 — Mode Requirement on Frequency Bands
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- [WLAN 4], REQPROD 57764, REQPROD 57790 It shall be possible to configure the default mode behaviour on respective frequency band: AP, STA or WiFi Direct.
- The following Local Config Parameters (REQPROD 97421) shall be used: Wireless Mode 2.4GHzWireless Mode 5GHzRole / Frequency bandWireless Mode 2.4GHzAPAPSTAAPAPSTAAPWi-Fi DirectWi-Fi DirectSTAWi-Fi DirectWi-Fi DirectSTA 4.3.18.1.2.4.2 Network Mode

### 1509 — Dual Band
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- To ensure that the WLAN transceiver supports simultaneous operation of 2.4GHz and 5GHz REQPROD 97421 The WLAN transceiver shall support simultaneous operation in 2.4 GHz and 5 GHz.
- Note: It shall be possible to decide to either operate on only 2.4GHz, 5GHz or 2.4GHz+5GHz via the local configuration file according to REQPROD 97421, by using the local config parameter: Frequency Range.

### 1510 — WLAN Mode 2.4GHz
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- REQPROD 97421 It's required that for 2.4GHz operation to support the following combinations:802.11b only802.11g only802.11b/g mixed802.11b/g/n mixed802.11g/n mixed802.11n onlyIt shall be possible to configure default operation mode via Local Config File as per REQPROD 97421, using the parameter WirelessNetworkMode_24GHz

### 1511 — WLAN Mode 5GHz
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- REQPROD 97421 It's required that for 5GHz operation to support the following combinations:802.11a only802.11a/n mixed802.11n only802.11n/ac802.11 ac onlyIt shall be possible to configure default operation mode via Local Config File as per REQPROD 97421, using the parameter WirelessNetworkMode_5GHz4.3.18.1.2.4.3 STA specific requirements4.3.18.1.2.4.3.1 Roaming

### 1512 — Seamless Roaming
- 版本：v10 ｜ 验证方式：Test ｜ 适用：通用
- Document typeNote-SWRS Page No638(1572) The WLAN transceiver shall support roaming within ESS when connected to OEM Access Points.
- Application shall support two methods to perform roaming (default shall be configurable via Local Config File REQPROD 242995).
- Used roaming technique may make an impact on the traffic while scanning and therefore it's recommended that the WLAN transceiver only performs scanning while not actively transmitting data.

### 1513 — Active scanning
- 版本：v5 ｜ 验证方式：Test ｜ 适用：通用
- To ensure that there is a fast method which may be used to identify nearby (external) WLAN Access Points.
- WLAN Security, doc nr 31836313 A WLAN STA shall have support for active scanning.
- WLAN STA shall be able to wait for the probe responses on a specific channel for a set length of time.

### 1514 — Full Performance - Passive Scan
- 版本：v5 ｜ 验证方式：Test ｜ 适用：通用
- WLAN Security, doc [31836301] Full Performance – Passive scanning shall be used when WLAN transceiver is not associated to, or joining a network.
- Configuration parameters defined in local config file (REQPROD 242995) shall be used.
- Depending if the internal WLAN antenna or external WLAN antenna is used, there shall be different scan methods.

### 1515 — Internal Debug - Scanning
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- The supplier shall enable monitoring of the current scan mechanism (according to used scan settings REQPROD 242995), into log-files which shall be extracted via a Local Configuration Tool.
- The logging shall be enabled via the Local Configuration File parameter ScanDebug.
- The log-files shall contain information about the current used scan method settings, which channels are scanned and which SSID, BSSID, RSSI, MAC address are identified on the specific channel etc.

### 1516 — Limited Performance - Passive Scan
- 版本：v5 ｜ 验证方式：Test ｜ 适用：通用
- WLAN Security, doc [31836301] Limited Performance-Passive scanning shall be used when WLAN transceiver is configured,STA and is connected to an external AP (from a vehicle point of view) or,AP and has nomadic devices connected.
- Scanning for Wi-Fi networks shall be performed as per the parameters defined in the local config file (REQPROD 242995).
- Following parameters shall be used: IA-ScanMethodIA-PreferredFrequencyIA-PassiveMaxChannelTimeIA-PassiveIdleTimeIA-PeriodScanSettingIA-PassiveScanIterationIA-PassiveScanTotalTimeInfotainmentChannelList2.4GHz [...]InfotainmentChannelList5GHz [...]Enterprise 2.4GHz ChannelScanCombination[ ...

### 1517 — Passive Scanning
- 版本：v7 ｜ 验证方式：Test ｜ 适用：通用
- To discover available BSSs in the radio range [WLAN Ex 2] A STA shall support Passive Scanning on 2.4 GHz and 5 GHz frequency band.

### 1518 — Scan Setting - Local Config
- 版本：v7 ｜ 验证方式：Analysis ｜ 适用：通用
- To define the content of the Local Config File this shall be used to ease during early implementation/testing/tuning phases to enable a smooth identification of Wi-Fi networks.
- REQPROD 242993, REQPROD 242994, REQPROD 57802, REQPROD 244933 The following table contains parameters and values which shall be used within a Local Config File which shall be stored and used in the ECU which contains WLAN functionality.
- The supplier shall provide ways to modify the local configuration file to be able to modify/tune the behavior during the early development phases.

### 1519 — Tuned scanning
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- To define the responsibility of the tuning of scan settings The supplier is responsible to set the scan setting parameters which shall be used as default and is the "best match".

### 1520 — Valid AccessPoint
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- To define how the applications shall determine if a BSS is valid or not (active or dead).
- When the WLAN transceiver is detecting beacons it shall use a counter.
- If X (according to BeaconCounter value) number of beacons are missed, the link shall be declared as dead and removed from AP list.

### 1521 — Security
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- To ensure a high level of security. Network security for the wireless networks (with respect to authentication and encryption) is currently covered in WLAN Security Requirement Specification, Document nr: 31836313,WLAN Physical & Datalink Layer - Requisite Doc

### 1522 — Associated Wireless client devices
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- If the router ECU has a wireless interface configured as Access Point, it shall be possible to monitor and view the clients which are connected to the Access Point.
- The information listed in the table below shall be available for each connected device.
- The parameters above shall be accessible via a Local Analysis Tool.

### 1523 — AT4 Wireless Performc Tool
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- com/ The supplier shall guarantee/enable that the AT4-agents part (client and server) of the AT4-Wireless Performance tool is able to read out necessary Key Performance Indicators (KPI), AND that it's possible to read out L7 and L3 (according to AT4-wireless Performance tool).

### 1524 — Link Monitoring - Extended debug of wireless links
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- If the router ECU has a wireless interface, it shall be possible to enable extended debug functionality to monitor the control and management frames.
- The extended debug functionality shall be accessible via a Local Analysis Tool.
- It shall be possible to enable/disable extended debug functionality, via a Local Configuration File.

### 1525 — Link Monitoring - Wireless links
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- REQPROD 352558 The router ECU shall implement a feature to monitor the quality of the wireless communication links.
- The Link Monitoring for wireless links, shall set a number of parameters and counters defined in the table below: Parameter DescriptionMAC address of the external Access Point.
- Access Point If the wireless interface is connected to an access point, the MAC address of the access point shall be presented.

### 1526 — Lock of MCS
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- The supplier shall provide a way to enable set of a specific modulation scheme (MCS) to use (AP or STA).

### 1527 — Network performance measurement
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The ECU which uses WLAN functionality, shall implement a software tool to measure network performance.
- The supplier shall enable all possible configuration / settings which the performance application supports.
- This application shall only be enabled for test activities during development phase.

### 1528 — Channel Interference Avoidance - Auto Channel
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- N/A If a auto channel mechanism is chosen, t he WLAN transceiver shall before deployment (of an AP) scan the surrounding Wi-Fi channels to avoid interference.
- The channel with the least interference shall be used for setting up the AP.
- The parameter Wireless Channel Selection shall be used to define if static or auto channel mechanism shall be used.

### 1529 — Channel Interference Detection - Auto Channel
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- N/A If auto channel mechanism is chosen and the WLAN transceiver (configured as AP) is not in use (no clients connected), the WLAN transceiver shall periodically scan the surrounding Wi-Fi channels, to check if there is adjacent channel interference.

### 1530 — Selecting and advertising new channel
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- For an AP, if the channels are to congested the AP may attempt to move a BSS to a new operating channel.
- Chapter 10.9.8.2 in [WLAN Phy DL Ex 2] The WLAN transceiver configured as AP shall be able to:· to detect the surrounding channel congestion by using passive scan· if a cleaner channel (than current) has been detected for time x (configurable via Local Config Data file) and the channel satisfies applicable regulatory requirements AND if there are associated STA (supporting the new proposed clean channel)· The AP may take the decision to switch channel, but first informing the associated STAs that the AP is moving to a new channel and maintain the association by advertising the switch using Channel Switch Announcement elements in beacons frames.· The AP may force STAs in the BSS to stop transmissions until the channel switch takes place by setting the Channel Switch Mode field in the Channel Switch Announcement element to 1.
- The AP may send the Channel Switch Announcement frame in a BSS without performing a backoff, after determining the WM is idle for one PIFS period.4.3.18.1.2.7.1.2 Static

### 1531 — Channel Selection - Static Channel
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- REQPROD 97421 The WLAN transceivers, when configured as AP shall support a static (manual) channel selection.
- Example of Local Config file parameters, when static channel is to be used: Wireless Channel Selection: STATICThe parameters above shall be configurable via Local Configuration File according to REQPROD 97421.4.3.18.1.2.7.1.2.1 2.4GHz

### 1532 — Channel Deployment in 2.4GHz
- 版本：v5 ｜ 验证方式：Test ｜ 适用：通用
- Avoid channel overlap and degradation of throughput, when configured AP uses auto channels mechanism to select channel of operation [WLAN Ex 2] When configured as AP and if static channel mechanism is used (REQPROD 57741), a non-overlapping channel deployment strategy for the IEEE 802.11 network in 2.4 GHz band, shall be used.
- Either use channel 1, 6 or 11 for static channels in local config file: Wireless Channel Selection: STATICStatic Channel_2_4GHz: [ either 1, 6 or 11] The parameters above shall be configurable via Local Configuration File according to REQPROD 97421.
- NOTE: All these combinations shall be handled as recommended default channels according to reference.

### 1533 — Channel Deployment in 5GHz
- 版本：v5 ｜ 验证方式：Test ｜ 适用：通用
- [WLAN Ex 2] When configured as AP, a non-overlapping channel deployment strategy for the 5 GHz IEEE 802.11 network shall be used.
- The following rules apply: The parameter StaticChannel_5GHz shall be used to set the default AP channel when the parameter Wireless Channel Selection is set to STATIC.
- Channel bonding combinations according to reference shall be used with 40 MHz and 80 MHz channels width.

### 1534 — EIRP for devices without TPC and DFS
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- The supplier shall present a solution on how to enable usage of more channels on 5GHz.

### 1535 — Country Code
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- To define a configurable local configuration parameter which defines a country/region, that a specific vehicle is sold to and shall be used as default setting.
- [WLAN Ex 2] By using the local config parameter (REQPROD 97421), Country Code, the IEEE 802.11 WLAN transceiver shall adopt to allowed operating frequencies, that are licensed by nation regulatory bodies for the specific country.
- If such are implemented, they shall be used instead of this local config parameter: Country Code

### 1536 — Operating across regulatory domains
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Beacon frames contains information on the country code, max allowable transmit power and the channels that may be used for the regulatory domain.
- Chapter 9.18 in [WLAN Ex 2] The WLAN transceiver and application shall be able to get country information and adopt the PHY to the country/region/domain to avoid violations via either:[1] external interfaces, such as GPS information.[2] periodic scan (with minimum performance degradation if used by applications) and search for beacons containing country string information.
- If x beacons of multiple APs are using a new country string, the WLAN PHY shall adjust to the new country/region/domain.

### 1537 — IEEE 802.11 ESS
- 版本：v4 ｜ 验证方式：Analysis ｜ 适用：通用
- To ensure that STA may communicate over large coverage networks with usage of multiple APs.
- [WLAN Ex 2] It's required that a STA shall be able to communicate over a large coverage network, IEEE 802.11 ESS.4.3.18.1.2.8.2 Independent BSS

### 1538 — IEEE 802.11 IBSS (Ad hoc)
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- [WLAN Ex 2] IEEE 802.11 IBSS (Ad hoc) shall NOT be supported or used.4.3.18.1.2.8.3 Infrastructure BSS

### 1539 — IEEE 802.11 BSS
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- STA shall be able to communicate between each other with help of an AP.
- [WLAN Ex 2] IEEE 802.11 Infrastructure BSS shall be supported.4.3.18.1.2.8.4 P2P

### 1540 — Wi-Fi Direct
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- [WLAN 4] Wi-Fi Direct shall be implemented according to source reference [WLAN 4].4.3.18.2 WLAN Applications4.3.18.2.1 IntroductionThis document contains requirements for WLAN Applications that, supplier of ECU implementing WiFi Application need to fulfill.
- These requirements shall be implemented to ensure interoperability between devices.
- The developer may be an external supplier or an internal software department.

### 1541 — Local Configuration data
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- Peer-to-Peer technology contains three components: P2P DeviceSupports both P2P Group Owner and P2P Client roles and negotiates roles during Group formation phase of connection.○ May support WLAN and P2P concurrent operation○ Supports WSC and P2P discovery● P2P Group Owner (GO) role○ P2P Group Owner works like Access Point in infrastructure mode.○ Implements "registrar" role of WSC functionality○ P2P Group Owner may also support communication between associated clients● P2P Client role○ Works like STA in infrastructure network to implement non-AP features of infrastructure mode.○ Implements "enrollee" role of WSC functionality.

### 1542 — P2P Device concurrent operation
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- To enable concurrent operation between WLAN Infrastructure mode and P2P operation Wi-Fi Peer-to-Peer (P2P) technical specification v1.2 P2P Device role implemented according to WFA Wi-Fi P2P technical specification (ref: [WLAN App Ex 1]) shall support concurrent operation with WLAN Infrastructure network.
- P2P Group shall be able to operate on same or different channel as of WLAN Infrastructure network in 2.4 GHz or 5 GHz frequency band.

### 1543 — P2P Frequency band usage
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- To ensure that P2P Group can operate in both 2.4 GHz and 5 GHz band Wi-Fi Peer-to-Peer (P2P) technical specification v1.2 Implementation shall support P2P Discovery and P2P Group operation in 2.4 GHz and 5 GHz band.

### 1544 — WFA P2P
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Wi-Fi Peer-to-Peer (P2P) technical specification v1.2 WiFi Alliance Peer-to-Peer (P2P) technology shall be implemented according to reference [WLAN App Ex 1]

### 1545 — WFA P2P role
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- To enable concurrent WLAN and P2P operation Wi-Fi Peer-to-Peer (P2P) technical specification v1.2 P2P Device role as specified in WFA Wi-Fi P2P technical specification ([WLAN App Ex 1]) shall be implemented.

### 1546 — Wi-Fi Protected Setup PIN
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- To ensure that PIN is not susceptible to brute force attack Wi-Fi Simple Configuration Specification v2.0.2 For each time registration protocol is run, implementation shall generate random fresh 8 digits PIN to use for authentication.4.3.18.2.2.1.1 Certifications

### 1547 — WiFi Alliance certification
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- To ensure interoperability with on market devices implementing same technology ECU implementing Wi-Fi and Wi-Fi P2P standard shall be WiFi DIRECT certified by WiFi Alliance according to Wi-FI DIRECT certification program.

### 1548 — WiFi Protected Setup
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- To fulfill mandatory requirement of WiFi Direct certification program Wi-Fi Protected Setup Specification version 1.0, December 2006, Wi-Fi 11 Alliance ECU implementing WiFi and WiFi P2P standard, shall also implement WiFi Protected Setup as per the reference.
- ECU shall be certified under Wi-Fi Protected Setup program.4.3.18.2.2.1.2 P2P Services

### 1549 — P2P Services
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Wi-Fi Peer-to-Peer (P2P) technical specification v1.2 P2P Device shall support below P2P servicesP2P DiscoveryP2P Group operationP2P Power Management4.3.18.2.2.1.2.1 P2P Discovery

### 1550 — P2P Service Discovery
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Wi-Fi Peer-to-Peer (P2P) technical specification v1.2 Implementation shall support P2P Service Discovery as specified by WFA Wi-Fi P2P technical specification v1.2

### 1551 — P2P SSID
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- To obfuscate the P2P SSID Wi-Fi Peer-to-Peer (P2P) technical specification v1.2 The default P2P SSID shall not reveal the identity of owner by the name and shall follow criteria specified below.

### 1552 — P2P Invitation
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- To ensure that new members can be invited to group and persistent groups can be invoked Wi-Fi Peer-to-Peer (P2P) technical specification v1.2 Receiving and transmitting P2P Invitations shall be implemented.

### 1553 — P2P Persistent Groups
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- To invoke P2P Group between two devices which were members of group previously Wi-Fi Peer-to-Peer (P2P) technical specification v1.2 P2P Device shall support formation of P2P Persistent group.4.3.18.2.2.1.2.3 P2P Power savingIEEE802.11 standard defines power saving mechanisms but they are mainly intended for devices in STA role.

### 1554 — P2P Power saving
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- To ensure that P2P devices can save power Wi-Fi Peer-to-Peer (P2P) technical specification v1.2 Implementation shall support OppOS and NOA power schemes as specified by WFA P2P spec v1.2

### 1555 — Support for Legacy device
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- To ensure that legacy devices are able to connect to P2P group Wi-Fi Peer-to-Peer (P2P) technical specification v1.2 Implementation shall support operation of legacy devices (device not implementing WFA P2P technology) in P2P group, together with other P2P devices.4.3.18.3 WLAN Security4.3.18.3.1 Appendix A - Possible threatsThis appendix shall be seen as an acknowledgement that there are several threats on the WLAN link that should be handled by a WLAN system (STA, AP, AS).4.3.18.3.1.1 DoS Attack 1By utilizing a wireless transmitter an attacker could effectively launch a DoS attack by jamming the channel used by the system.
- The attacker then waits for the user to attach to the fake network and captures their credentials and it's possible that the attacker may crack the challenge/response pair to recover the password.4.3.18.3.1.5 Other AttacksSeveral other attacks are possible for pre-RSNA algorithms such as WEP or the less secure RSNA-PSK (WPA-PSK/TKIP/RC4) mode.
- Certificates must only be awarded to well trusted entities in a controlled environment.

### 1556 — Data Confidentiality RSNA-CCMP
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- IEEE Standard for Information technology - Telecommunications and information exchange between systems - Local and metropolitan area networks - Specific requirements, Part 11: Wireless LAN Medium Access Control (MAC) and Physical Layer (PHY) Specifications, Clause 8.3.3, WLAN Security Requirements - External publications Only CCMP (RSNA-CCMP) shall be used for data integrity and encryption according to the table in section Data Confidentiality .

### 1557 — Minimum AES Key Size
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- To ensure that the WLAN transceiver is designed to support key lengths of the AES algorithm, where the minimum key length shall be sufficient to protect data exchange.
- FIPS PUB 197 The WLAN transceiver shall support the following key sizes:128 bits192 bits256 bits 4.3.18.3.2.1.1 Scenario mapping - Policies Scenario WLAN Transceiver Mode WPA2 Version Authentication Encryption A AP or STA WPA2-Personal PSK AES-CCMP B STA WPA2-Enterprise IEEE 802.1X/EAP AES-CCMP Table: Policies - Wi-Fi Protected Access 2

### 1558 — Data Confidentiality - Policies
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- To ensure a high level of security (only authorized users may access the network).
- The data confidentiality shall be ensured by following the Policies according to the tablePolicies - Wi-Fi Protected Access 2 in section Scenario mapping – Policies .4.3.18.3.2.2 Probe RequestsA normal connection procedure is initiated by a periodic transmission of beacon frames from an AP.

### 1559 — Probe Requests
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Connection attempts shall only be made after receiving an appropriate network beacon.

### 1560 — WLAN Authentication and Privacy Infrastructure (WAPI)
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- For the Chinese market, WAPI shall be used.4.3.18.3.2.4 RSN ArchitectureThe RSN architecture as specified in IEEE Std 802.11-2007 consists of the following steps: Initial authentication and association between STA and APAuthentication using Pre-Shared Key (PSK) or IEEE Std 802.1X-2004A 4-way handshake between STA and APWhen a STA (Wi-Fi client) want to connect to a network it has to perform an authentication and association request with an AP that belongs to the network.
- IEEE Std 802.11-2007 Clause 8.1 RSNA algorithms shall be used exclusively.
- Weak passwords may also be subject to brute force attacks using information sent during the 4-way handshake.

### 1562 — IEEE 802.11 Default Passphrase
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- By default, the passphrase shall be unique for each vehicle by adding a random number to the passphrase and based on approved algorithms from the NIST standards.
- [WLAN Sec 8], [WLAN Sec 9] The default passphrase shall be set to a random unpredictable passphrase using t he Random Number Generator (RNG) which uses strong PRNGs based on NIST SP 800-90 standards.1.
- The Deterministic Pseudo Random Number Generator (DPRNG) used for generating any cryptographic keys (such as private keys, passwords, session keys, etc.) must comply with NIST SP 800-90 standards.2.

### 1563 — IEEE 802.11 Minimum Length Passphrase
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- The passphrase may use 64 hexadecimal digits, or passphrase of 12 to 63 ASCII characters.

### 1564 — IEEE 802.11 Pre-Shared Key (PSK) Authentication
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- IEEE Standard for Information technology - Telecommunications and information exchange between systems - Local and metropolitan area networks - Specific requirements, Part 11: Wireless LAN Medium Access Control (MAC) and Physical Layer (PHY) Specifications, Clause 5.8.2.2, WLAN Security Requirements - External publications IEEE 802.11 PSK authentication shall be used for the scenario A.

### 1565 — Authenticator-to-AS protocol
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- The advantage with using digital certificates signatures are that the certificates may have a limited valid lifetime, which is indicated in the certificate content.
- One private key, which is stored on the ECU (which must be protected).

### 1566 — Certificate
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- The usage of a digitally signed statement, Public Key Infrastructure Certificate and Certificate Revocation List shall be used.
- RFC-5280 Internet X.509 PKI Certificates shall be supported.

### 1567 — Certificate Policy
- 版本：v4 ｜ 验证方式：Analysis ｜ 适用：通用
- The handling of certificates needs a policy that explains who and how the certificates shall be handled.

### 1568 — Certificate and key encryption
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- p12") shall be used for file extensions, when stored in an ECU.1569 v5 Certificate Protection Private Key The protection of private keys is crucial and keys must be stored in a secure memory area of the ECU.
- RFC-5280, SAD Connected Car Security The private key must be protected from all kind of readout outside the application (e.
- It's required that the private key is stored in a secure area and it must be possible to write new private keys into the secure area.

### 1571 — EAP-TLS
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- RFC-5216 Only EAP-TLS shall be implemented.4.3.18.3.2.6.1.4 Roaming Authentication

### 1572 — Roaming Authentication
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- The device shall support the usage of preauthentication.

### 1573 — IEEE Std 802.1X-2004 Authentication
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- IEEE Standard for Information technology - Telecommunications and information exchange between systems - Local and metropolitan area networks - Specific requirements, Part 11: Wireless LAN Medium Access Control (MAC) and Physical Layer (PHY) Specifications, Clause 8.4, WLAN Security Requirements - External publications IEEE Std 802.1X-2004 authentication shall be used.

### 1574 — SSID Beacon
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- IEEE Standard for Information technology - Telecommunications and Page No691(1572) information exchange between systems - Local and metropolitan areanetworks - Specific requirements, Part 11: Wireless LAN Medium AccessControl (MAC) and Physical Layer (PHY) Specifications, Clause 7.2.3.1,WLAN Security Requirements - External publications SSID shall be included in network beacons.
- Applies to the WLAN Transceiver (ECU) configuredas AP and External AP.4.3.18.3.2.8 WLAN Security OverviewTwo important security standards: 802.1x and 802.11i shall be supported.
- According toWLANPhysical & DataLink Specification, WLAN Security Requirements - Requisite documents, theWLAN architectures which are listed in the table below shall be supported.

### 1575 — General Security
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- The supplier is required toinform the OEM, if/when the chosen standard security mechanism is breached or cracked andneeds to be updated.4.3.18.3.3 IntroductionThis document specifies all security related requirements that shall be implemented to get a secure connection on the link layer between an Access Point (AP) and a wireless station (STA).
- The WLAN transceiver within the vehicle may be used as either AP or STA.
- This documentspecifies security requirements both on the ECU containing the WLAN interface as well as on the access point that the vehicle shall be able to connect to.

### 1576 — Entropy for random numbers
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- The output from the entropy source shall be tested using the tool ENT (https://www.
- The entropy generated shall when tested with ent shall be:- - Entropy: At least 7.5 bits per character or higher.- - Compression: 0%-- - Chi-Square: Between 200 and 400 and randomly exceed more than 10% and less than 90% of the time.- - Mean value: Between 126 and 128-- - Monte Carlo: Max 0.5% error -- Serial correlation: 0.1 or lowerNote;

### 1577 — Random number generator algorithms
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- NIST Special Publication 800-22 Revision 1a MRandom numbers shall be generated by a deterministic random bit generator (DRBG), also known as a cryptographically safe pseudo random number generator.
- The generator shall be seeded and periodically reseeded from entropy provided by the entropy source.
- The generator used shall be one of the hash based or block cipher based generators approved by NIST, see SP 800-90A.

### 1578 — Certificate status indication
- 版本：v2 ｜ 验证方式：Inspection ｜ 适用：通用
- Certificate status shall be verifiable by means of a diagnostic routine.

### 1579 — Certificate verification
- 版本：v4 ｜ 验证方式：Analysis ｜ 适用：通用
- RFC 5280 for PKIX)including (but not limited to): Validate Certificate Chain (AKI => SKI chain) ValidityHostname verificationApplication specific verification (requires application specific rules)Extended key usage: shall be according to policy.
- Critical extension: shall be according to policy.
- Issuer: according to policyCertificate revocation lists or OCSP/OCSP stapling shall be supported.

### 1580 — ECU Certificate Installation
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- Enable maintainability through diagnostic services Certificate update shall be triggered or updated by means of a diagnostic routine and the certificate shall be verified before accepted by the ECU.
- Possible failure modes shall be indicated.1.

### 1581 — Revocation status information
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- The revocation status of certificates shall be checked with the certificate authority using online certificate status protocol (OCSP) or revocation list (CRL), resulting in a failed authentication when the certificate status is revoked.

### 1582 — Application tamper protection
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- There shall be mechanisms in place to ensure authenticity of the application using privileged functions (i.

### 1583 — Tamper resistant storage
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- Client certificate private keys and CA root certificate shall be stored in a hardware security module.

### 1584 — Client Certificate private key storage
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- Client certificate private keys and CA root certificate shall be encrypted with a password (a separate key).4.4.3 Security Access algorithm4.4.3.1 Security Access algorithm4.4.3.1.1 Configuration of the Level of ProtectionThe level of protection by using diagnostic service Security Access together with the Security Access Algorithm is configurable with respect to:1.
- ProtectionLevel Delay Timer (activated when max number of false attempts detected) Number of false security access attempts Fixed Bytes 1 N/A N/A Common 2 10 seconds 2 Common 3 N/A N/A Unique 4 5-60 seconds 2 Unique Table - Levels of ProtectionLevel 1: To prevent an unauthorized user that is having limited time and capabilities, or to avoid accidental errors, as the common key must for "Level 1" be assumed to be known by an attacker at some stage.

### 1585 — Soft Certificate installation
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- When certificates and private keys are generated outside the ECU and installed they shall use diagnostic software download with the following attributes in the VBF header: Certificate filesw_data_type = CERTSee, certificate structure and format for more details on contents of the certificate file.

### 1586 — Default values - Delay timers and counters for false attempts
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- To define default values for the parameters used to configure the level of protection The default values shall be set to:- Delay Timer activated after a number of false Security Access attempts: 10 seconds.
- A function/system designer is free to increase the delay timer activated after a number of false attempts, but decreasing that parameter or change of the other parameters must require an approved deviation.
- ECUs having the proper hardware capabilities shall store (in non-volatile memory) the information whether the delay timer after a number of false attempts has been activated or not, i.

### 1587 — SecurityAccess (27) - time delay after false securityAccess attempts
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- It shall be possible to make at least 1 false SecurityAccess attempt without being penalized by a time delay before the next attempt is accepted.4.4.3.1.2 Random Number GenerationThe generation of the random number, i.

### 1588 — Seed - Random Number Generation
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- + Analysis The Seed generated must be a cryptographically secure random number, meaning that it's generated using either a True Random Number Generator (TRNG) or Pseudo-Random Number Generator (PRNG).
- This implicit implies that the Seed outputs must not be repeated after an ECU reset.
- Hence, static Seed shall never be used.4.4.3.1.3 Security Levels (Areas)An ECU is divided into several security access levels ("areas"), where each level is protected by a dedicated security access constant.

### 1589 — Distribution of the Fixed Bytes
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- 1589 v1Distribution of the Fixed Bytes To define the source provider of the fixed bytes. - + Inspection The fixed bytes are to be supplied from CEVT. These are not to be chosen by supplier.

### 1590 — Fixed Bytes default value
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- If the fixed bytes has not yet been programmed to the ECU and unlocking by the $27 Security Access service is requested, the ECU shall use a default value where all fixed bytes are set to 0xFF.

### 1591 — Key Storage
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- + Inspection The Fixed Bytes used shall be stored in a protected area, typically in tamper resistant memory, and must not be possible to read out.
- If a key update process is required, the security of that process must be ensured.
- 4.4.4 Software Authentication 4.4.4.1 General Software Authentication 4.4.4.1.1 System DescriptionTo support legacy systems and enable future growth, the Software Authentication concept must be prepared to support several signing methods even though an ECU will only support one.

### 1592 — Security Level usage
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The ECU shall use the security access levels defined inTable - Security Access Levels.
- Security Access Level Purpose Comment 01 Used for software download A vehicle unique security access constant shall be generated in the manufacturing process.
- 03 Car mode transition A common security access constant shall be applied.

### 1594 — Signing Method SHA256_RSA2048 - Hash function
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- Define the hash function. FIPS PUB 180-4, Secure Hash Standard (SHS) FEDERAL INFORMATION PROCESSING STANDARDS PUBLICATION, March 2012. The hash function to be used is the SHA-256 (256 bits) as defined in FIPS PUB 180-4, Secure Hash Standard (SHS), March 2012.

### 1595 — Signing Method SHA256_RSA2048 - Key Size
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- PKCS #1 v2.2: RSA Cryptography Standard, RSA Laboratories, October 27, 2012 The key size shall be 2048 bits.
- 4.4.4.1.2.3 Signing Method - Key balancingThe software authentication concept must support different strategies with respect to key management and key balancing.
- After a threat and risk analysis the proper security class shall be defined and applied for ECUs in the vehicle platform(s).

### 1596 — Signing Method SHA256_RSA2048 - Public Key Algorithm
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- PKCS #1 v2.2: RSA Cryptography Standard, RSA Laboratories, October 27, 2012 The public key algorithm shall be: PKCS #1 v2.2: RSA Cryptography Standard, RSA Laboratories, October 27, 2012, where the RSASSA-PSS signature scheme shall be used.
- The salt length shall be set to the same length as the underlying hash value.

### 1597 — Software authentication security classes
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- This variability must be managed in the variant handling systems off-board.
- The software authentication security classes as defined in the Table - Software Authentication security classes must be supported with respect to key management.
- This means that it shall be possible to configure the key usage in the off-board variant management systems:1) Integrity check only, i.

### 1598 — Default Signing Method
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- The ECU shall use the default signing method, unless else is explicitly defined elsewhere, e.
- The default signing method shall be SHA256_RSA2048_sw_part_based.4.4.4.1.2.2 Signing Method - Algorithm Definitions

### 1599 — Signing Method - Variability control
- 版本：v4 ｜ 验证方式：Analysis ｜ 适用：通用
- To control the variability at the back-end systems but also to inform the ECU ofthe signing method (at design time) that shall be applied.
- To define and distribute the Signing Method, a Software Settings File (a software part) shall be used for methods where each software part is signed individually.

### 1600 — Format of the Verification Block Table
- 版本：v5 ｜ 验证方式：Test ｜ 适用：通用
- Define the format of the verification block table The verification block table, encoded with big endian, shall have the following format: Verification Block Table Format Identifier.
- it shall not be used to configure e.
- This shall be identical to the number of data blocks included in the software part.

### 1601 — Verification Block Root Hash
- 版本：v4 ｜ 验证方式：Analysis ｜ 适用：通用
- Req: The verification_block_root_hash must be calculated on the "raw" unprocessed data in the verification block table, i.
- The verification block root hash shall be calculated as Hash(startAddress||length||Verification Block Table data), where || represents the concatenation.
- The order shall be according to Figure - Verification Block Root Hash calculation.

### 1602 — Verification Block Table - Input order to Hash function per data block
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The hash value for each data block in the verification block table shall be calculated as Hash(Data), i.

### 1603 — Verification Block Table Format Identifier - Definition
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- The Verification Block Table Format Identifier shall be according to Table - Verification Block Format Identifier.
- This means that Verification Block Table Format Identifier shall be 0x0000.

### 1604 — Verification Block Table Header Identifiers
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- 1604 v4Verification Block Table Header Identifiers Define the required header identifiers required to support the applied signing method The header section of the delivered software part must contain the following identifier with respect to the verification block table, when a verification block table is constructed according to the format in "REQPROD 398360: Format of the Verification Block Table".

### 1605 — Verification Block Table on unprocessed data
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- Req: The data block definitions in the Verification Block Table shall be prior to processing methods have been applied, i.

### 1606 — Verification Block Table per Software Part
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- Each single software part must contain a verification block table, i.
- Req: If there is a must to align and pad the data blocks to some specific size, the padded data must have the value of erased memory, i.
- Figure - Data block with aligned verification block table data blockNote: The verification Block Table_block_start, verification_block_length and verification_block_root_hash shall be calculated on data (blocks)generated using the "raw" unprocessed data in the verification block table prior to some processing methods have beenany padding is applied, i.

### 1608 — Public Key Types
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- Information about the public key type must be provided by the entity managing the keys.
- That information is optionally used to control how the diagnostic client shall program the public key, e.
- what diagnostic service(s) that shall be applied.

### 1609 — Software Authentication Test and Development Key
- 版本：v5 ｜ 验证方式：Analysis ｜ 适用：通用
- To keep track of the keys used for signing and verification during test and development For test and development only, a development key provided by the OEM shall be used.
- Unless otherwise is explicitly defined by the vehicle project, the following key pair shall be used:----BEGIN PUBLIC KEY----MIIBIjANBgkqhkiG9w0BAQEFAAOCQ8AMIIBCgKCAQEAt+10S0X6piDTHDDpY4bpzV+5k97KRcnWCJT3fbnuqdB4RXaUgJ33BSTXMOLADwRuYFMjvVADVyyypu7RcxRFaHc4lfUIDT34cej4aaOiaABCNGCisJr1xrkrJuSMLm8EBZ0apAV5w8dm9f1ZL12Fk/8HZbpOrQGbVy/QC9fxTEVGpgFwHFqvLmCX+AvOJfleRemTMLHpx6IMzWQqpWSPPSmvkJBr3jKkEXWW2dIcZQknjaQPdpMl1/qc8B8GRZ1RF/l/PRXL4vUeVuoGnVFBVKZIvgYJxm0Mc6ycWyofiuoOgHoXvdeRjiC0LU3a2s9ZoGeJsK2dPCp3e/pNCQ86HrQIDAQAB----END PUBLIC KEY---- Private-Key: (2048 bit)modulus:00: b7: e9:74:4b:45: fa: a6:20: d3:1c:30: e9:63:86: e9: cd:5f: b9:93: de: ca:45: c9: d6:08:94: f7:7d: b9: ee: a9: d0:78:45:76:94:80:9d: f7:05:24: d7:30: e2: c0:0f:04:6e:60:53:23: bd:50:03: bf:2c: a9: bb: b4:5c: c5:11:5a:1d: ce:25:7d:42:03:4f:7e:1c:7a:3e:1a:68: e8:9a:00:10:8d:18:28: ac:26: bd:71: ae:4a: c9: b9:23:0b:9b: c1:01:67:46: a9:01:5e:70: f1: d9: bd:7f:56:4b:97:61:64: ff: c1: d9:6e:93: ab:40:66: d5: cb: f4:02: f5: fc:53:11:51: a9:80:5c:07:16: ab: cb:98:25: fe:02: f3:89:7e:57:91:7a:64: cc:2c:7a:71: e8:83:33:59:0a: a9:59:23: cf:4a:6b: e4:24:1a: f7:8c: a9:04:5d:65: b6:74:87:19:42:49: e3:69:03: dd: a4: c9:75: fe: a7:3c:07: c1:91:67:54:45: fe:5f: cf:45:72: f8: bd:47:95: ba:81: a7:54:50:55:29:92:2f:81:82:71:9b:43:1c: eb:27:16: ca:87: e2: ba:83: a0:1e:85: ef:75: e4:63:88:2d:0b:53:76: b6: b3: d6:68:19: e2:6c:2b:67:4f:0a:9d: de: fe:93:42:43: ce:87: adpublicExponent: 65537 (0x10001)privateExponent:67: bf: c8:3e:2a:95:12: a0: d3: d7:44:74:75:14:07: d3:36: dc:2e: e1: f1:03: db: af: e5:99:7b: e0: ae:42:48:03: f5: c5:61: f6: b6:73: e6:85:3d:5a:34:16: c6: b7: f2:0c: fe:44:08:96:64:8c:28:8d: de:96: a8:51: e9:4e:37: a3:36: c7:09:59:73:1a: a6:0f:14:9a: f2:35:1a:7a: bd: ec:98:5b: f7:9d: de:20: e2: ff: aa: eb:0f:89:08: a4:6e:06:07: a7: e1: f1:86: c0:7a:7f:16:1a: be: a8: d8:16:36:6e: dd:81:76:92: d1:79: fc:49:41: cc:3e: db:5b: e3: d4:91:62: fa:26:04:1b:1f:5e:2b: d4:7c: b2:68:5c: ec:40: f2: c6: e2:83:7d:71: e0: f9: fa:41:24:8d:36:1c: e8: c4:05:38: ab:23:37: d1: c8: c6: ad: e5: de:98: d5:0a:7e: aa: ba:54:5a:63: d5: e1:49: be:84:0d: de:66:71:78: c8: df:5c:53:88: ea:00: c1:8d: af:81:9f:0a: c4: a0:6e: b0: f7: da: a1:22:72:46:65:68:3b:24: b7:89: d0: ce: de:3a: f3: d5:07:94: d7:17:9c: c7:90:77:7b:6c:7a:21:72: e5:17:25:8a:84:20:01:1b:9b: e5:96:5c:17:0b: de:85:38: cf:95prime1:00: df: d1:18:63:6f:2c:1b:14:3b:95:3d:56: dd:5b:6f:01:6e: f9:4c:2b: cb: eb: dd:89: b0:8e: dd: f3: f0:0f: f7:71:75: d0:7e: b0: be:6b:51:3a:8c: cf:9b:81: fa:34:4f: fc:98: d6:65: b1:2f:82:55: a8: d1: b5:1a: af:7b: da:6f:02:43:14:7e:69:52:11:9e: a9:95:44: b1:19:7f:7b:7c:67:30:11:67:88:9d: b1: b5:6e:6a:69:17:64:57: dc:5e: fd:33: ae:84: dc:2a:73:54:8d: be:04: c7:6f:6e:7f:31: f1:04: b3:6b: f7:9f:62:15: b0:75:12: a8:4f:02:4a: cb: d7prime2:00: d2:5b:6c:9d: a4:9b: a9:6e:29:67:3f: d1: c2:53:1a:50:5b:0a:7c: c1:64:01: ff:20:20:8c:68:32: b1:1a: fb:8e:73:54:29:3b: e7: fc:94:0f:63:06: a2:87:56: a4: e3:48:75:21: b7:10:97: fc:3a:1d: b3: e2: ab: e6:4b:04:8d: de: fb: ac: d3: e4:3d:71:20: da:04: aa: e2:98: f4: e3:6c: f4: fa: c3: a7:1f:73:30:4f:3c: fe:8a:3e:21:06: e7:02: b4: e5:9d:4e:37:64:67:15: f3:64:73: cf:30:2d:54:19:76:22: ee:44: b5: cb:8f:94: a0: f5:15:91:68:56: cc:38:1bexponent1:7e:33: cf:06: b2:77:32:45: b4:5b:30:9d:3c:70:04:25: d0: c7:6d: b5: fc:64:61:24: f4:93:7a:7f: c4:4b:9c:81:33: a7:7e: e8:76:56: d9:14: a4: b5: a3: c0:24: af:3e: b2: f6:13:5e:80:0c:83: f7:7d:1b: d2:7c: db: Figure - Signing and verification of unprocessed (target) data Page No735(1572) ## Document Name ## Base Tech SWRS DHU 9a:80: ce: bb:7d: cb:9e:84:10: ac: b2: c4:78: d0: a4: f3: f5: b8:51: ab:75: a5:3a: b6:04:05:62:82:82:2a: 03: f0: a6: c2:32:25:9f: f0: b6:25: d7:21: f4: f9:7f: bd: fe:1e: cd:35:97:99:89: c7:0a:08:34: ad:00:01: e1: e1: c5:59: d7: b7:09:3d ## exponent2: 00:87: f8: a4:9a: b9:9e:0c: c4: b2:6a:94: ec:07:4a: 24:46:30: b2: f4: b5:24: e9: cd:79:7c: d0:85:41: cf: 0c: fb: f1: b6:46:7e:68: c4: a9:95:22: e5:05:92: e5: 1c:72:74:9f:8f:66: fd: a7: f2:36:0d:72: c9: a6:09: 2b:50: ee:5e: ad: f5: cc:5f:22: b7:3c:7a: d9: b2:0e: ab:6d: e7:4d:62:4e:70:11:2b: e3: be:57:49: c0: c9: 5f:9e:8d:46: a2: e8:32: fa:00: d6:60:23: bc:26:8a: 2f:32:54:88:75: a4:58: d8: ed: f7:49: de: a0: f7: ec: 40: a6:6b:0c:94:7f:16:7e:65 ## coefficient: 46:53:1a:19:21:2d: fe:36:73:85:3a:71: a2:84: fa: 5c:35:76: db:10: f0:34:86:14: a9:70:1c: d8:73: df: 2b: d0:43: d9:73: d2:26:1f: b2: ba:9d:82:57:9b:4c: cd:4a: bc: f2:1f: fa: f5:5b:2a:8d:6c:20:39: db: f8: 55:19:11:15: b4: a9: a1:00: dc:93:31:53: c5: c6:17: cb:36: e9:00: d8:6e: c8:75:69:6a:85:4d:42:01:2a: 86:36:59: fc: d7:0b:57:8a:76:7d: c0: bc:43:8a:4d: b1:14:07:4d:28:5a: ec:30:28:93:6e:68:14:1a: c0: 17:6c: e1:7c:39:19: e6: d8 MIIEowIBAAKCAQEAt+l0S0X6piDTHDDpY4bpzV+5k97KRcnWCJT3fbnuqdB4RXaU gJ33BSTXMOLADwRuYFMjvVADvyypu7RcxRFaHc4lfUIDT34cej4aaOiaABCNGCis Jr1xrkrJuSMLm8EBZ0apAV5w8dm9f1ZLl2Fk/8HZbpOrQGbVy/QC9fxTEVGpgFwH FqvLmCX+AvOJfleRemTMLHpx6IMzWQqpWSPPSmvkJBr3jKkEXWW2dIcZQknjaQPd pMl1/qc8B8GRZ1RF/l/PRXL4vUeVuoGnVFBVKZIvgYJxm0Mc6ycWyofiuoOgHoXv deRjiC0LU3a2s9ZoGeJsK2dPCp3e/pNCQ86HrQIDAQABAoIBAGe/yD4qlRKg09dE dHUUB9M23C7h8QPbr+WZe+CuQkgD9cVh9rZz5oU9WjQWxrfyDP5ECJZkjCiN3pao UelON6M2xwlZcxqmDxSa8jUaer3smFv3nd4g4v+q6w+JCKRuBgen4fGGwHp/Fhq+ qNgWNm7dgXaS0Xn8SUHMPttb49SRYvomBBsfXivUfLJoXOxA8sbig31x4Pn6QSSN NhzoxAU4qyM30cjGreXemNUKfqq6VFpj1eFJvoQN3mZxeMjfXFOI6gDBja+BnwrE oG6w99qhInJGZWg7JLeJ0M7eOvPVB5TXF5zHkHd7bHohcuUXJYqEIAEbm+WWXBcL 3oU4z5UCgYEA39EYY28sGxQ7lT1W3VtvAW75TCvL692JsI7d8/AP93F10H6wvmtR OozPm4H6NE/8mNZlsS+CVajRtRqve9pvAkMUfmlSEZ6plUSxGX97fGcwEWeInbG1 bmppF2RX3F79M66E3CpzVI2+BMdvbn8x8QSza/efYhWwdRKoTwJKy9cCgYEA0lts naSbqW4pZz/RwlMaUFsKfMFkAf8gIIxoMrEa+45zVCk75/yUD2MGoodWpONIdSG3 EJf8Oh2z4qvmSwSN3vus0+Q9cSDaBKrimPTjbPT6w6cfczBPPP6KPiEG5wK05Z1O N2RnFfNkc88wLVQZdiLuRLXLj5Sg9RWRaFbMOBsCgYB+M88GsncyRbRbMJ08cAQl 0MdttfxkYST0k3p/xEucgTOnfuh2VtkUpLWjwCSvPrL2E16ADIP3fRvSfNuagM67 fcuehBCsssR40KTz9bhRq3WlOrYEBWKCgioD8KbCMiWf8LYl1yH0+X+9/h7NNZeZ iccKCDStAAHh4cVZ17cJPQKBgQCH+KSauZ4MxLJqlOwHSiRGMLL0tSTpzXl80IVB zwz78bZGfmjEqZUi5QWS5RxydJ+PZv2n8jYNcsmmCStQ7l6t9cxfIrc8etmyDqtt 501iTnARK+O+V0nAyV+ejUai6DL6ANZgI7wmii8yVIh1pFjY7fdJ3qD37ECmawyU fxZ+ZQKBgEZTGhkhLf42c4U6caKE+lw1dtsQ8DSGFKlwHNhz3yvQQ9lz0iYfsrqd glebTM1KvPIf+vVbKo1sIDnb+FUZERW0qaEA3JMxU8XGF8s26QDYbsh1aWqFTUIB KoY2WfzXC1eKdn3AvEOKTbEUB00oWuwwKJNuaBQawBds4Xw5GebY ----END RSA PRIVATE KEY--- Page No736(1572)

### 1610 — Append signature to software part
- 版本：v5 ｜ 验证方式：Analysis ｜ 适用：通用
- The signing tools must support the use-case of sign and re-sign software parts, typically during development but also to enable for e.
- The digital signature when the software part is signed with the intended private key fordevelopment, sw_signature_dev, shall be appended to the software part header by the software supplier when a part is delivered..
- The signing tool must support both sign and re-sign functionality of a software part.

### 1611 — Sign Software Part - Private Key syntax
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- The Private key shall be represented in an unencrypted PKCS #8 PrivateKeyInfo format as defined in PKCS #8: Private-Key Information Syntax Standard, RSA Laboratories Technical Note Version 1.2, Revised November 1, 1993.
- The PrivateKey part of the PrivateKeyInfo shall be a represented as an ASN.1 type RSAPrivateKey as defined in PKCS #1 v2.2: RSA Cryptography Standard, RSA Laboratories, October 27, 2012.
- The Private Key shall be stored using the PEM format (base64 encoded data) as defined in RFC1421.

### 1612 — Signing function - Generate signature
- 版本：v4 ｜ 验证方式：Analysis ｜ 适用：通用
- These start address, length and data of the addressed data block shall be used as inputs when generating the hash value.

### 1613 — Signing function - Integrity Check
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The signing tool used must ensure the integrity of the software part.
- If the tool is updating some software part identifier, the file_checksum shall be checked before and after the update and the checksum shall be identical.

### 1614 — Sign a delta file
- 版本：v5 ｜ 验证方式：Analysis ｜ 适用：通用
- The programmed (installed) data shall be verified, i.
- A delta software part shall contain the same header identifiers as the corresponding full version, with respect to following Software Authentication identifiers: verification_block_start, verification_block_length, verification_block_root_hash and sw_signature_dev.4.4.4.1.1.3 Download a (signed) software partThis section describes how to download a signed software part and transfer the signature data, where the signature data is transferred aftereachsoftware part is downloaded.
- Note that ECUs implementing CheckMemory shall not respond with a checksum value at the RequestTransferExit service.

### 1615 — Sign and verify unprocessed data
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- The signing and verification shall be based on unprocessed data.
- 4.4.4.1.1.2.2 Sign a Delta Software PartWhen delta encoding is used, the delta file shall contain information (hash values, signature, ...
- Figure - Signature for a delta fileWhen a delta file, as shown in Figure - Signature for a delta file is programmed, the ECU must finally verify the final data that has been installed in the non-volatile memory.

### 1625 — Spare Capacity
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- Page No111(1572) All new ECU's shall have a spare capacity of 30% at introduction time (Job1).

### 1627 — Multiple CPU Design
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- To clarify that requirements are applicable for the complete ECU and always considered as one entity. Legacy ID: An ECU is always considered as one entity and is not allowed to create bottlenecks due to connection dependencies between multiple CPUs. Note: This

### 1628 — Domain Master Address
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- All Domain Masters shall use the address 0x1Y01 where the two last nibbles, 01 states that the ECU is a Domain Master.

### 1629 — ECU Addresses (45) => (46): Description modified. Current: ECU Address
- 版本：v46 ｜ 验证方式：- ｜ 适用：通用

### 1630 — Component Selection - CAN Physical Interfaces
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- This is necessary for maintaining the CAN signal voltage level specified in partially powered network For power-switched ECUs an “ideal passive” transceiver shall be used.
- Transceivers shall not leak more than 5μA from an active CAN bus, in power-off mode.
- For battery-powered ECUs a transceiver with sleep functionality must be used.

### 1631 — Missing frame master - CAN
- 版本：v5 ｜ 验证方式：Test ｜ 适用：通用
- UDSonCAN The ECU routing diagnostic requests to and from a CAN network shall be missing frame master for that network.

### 1632 — No priority inversion
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- The communication driver shall be designed to be free of priority inversion when frames are transmitted on the CAN bus by AUTOSAR based ECU's.
- EESE Strategic Decision The communication driver shall be designed to be free of priority inversion when frames are transmitted on the CAN bus.

### 1633 — FlexRay Backbone - FlexRay Frame ID - Bootloader Schedule (8) => (9):
- 版本：v9 ｜ 验证方式：- ｜ 适用：通用

### 1634 — 1 FlexRay Backbone - FlexRay KeySlot parameter settings for Application
- 版本：v9 ｜ 验证方式：- ｜ 适用：通用

### 1635 — FlexRay Backbone - FlexRay KeySlot parameter settings for Bootloader Sch
- 版本：v8 ｜ 验证方式：- ｜ 适用：通用

### 1636 — FlexRay Backbone - FlexRay Schedule Coordinator
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- To define which ECU is the FlexRay Schedule Coordinator (FrSC) on the network FlexRay Backbone. The FrSC have the responsibility to inform the other ECU's on the FlexRay bus which FlexRay Schedule is active for the moment. For the time being there are two sche

### 1637 — FlexRay Backbone - Missing frame master - FR
- 版本：v5 ｜ 验证方式：Analysis ｜ 适用：通用
- UDSonFR The ECU routing diagnostic requests to and from a FR network shall be missing frame master for that network.

### 1638 — FlexRay Backbone - Protocol relevant node parameters WakeupPattern
- 版本：v4 ｜ 验证方式：Analysis ｜ 适用：通用
- The FlexRay wakeup pattern (WUP) defined by parameter pWakeupPattern shall be unique in length for each FlexRay ECU and shall be implemented as described in the table below.
- If another requirement define a different value of pWakeupPattern then this requirement shall override that other requirement.
- If the ECU is not allowed to wakeup FlexRay then this value shall still be implemented, but the wakeup mechanism shall not be used.

### 1639 — 100BASE-T1 PHY Mode Matrix
- 版本：v7 ｜ 验证方式：Test ｜ 适用：通用
- N/A The mode for each PHY on each link shall be set as stated in the table below.

### 1640 — Diagnostic IP routing algorithm
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- Clarification of how the diagnostic IP routing algorithm shall work.
- A general rule for the Edge Node to be able to decide what kind of diagnostic message which shall be send over the IP-links or other vehicle network (CAN, LIN, FlexRay) is to investigate the IP address and search for the Domain ID.

### 1641 — Domain ID for IP networks
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- Clarification of which Domain ID's are dedicated for IP networks. Domain ID 0,1,2 and 3 states that this belongs to IP-based communication links. Note: This requirement is valid for all ECU communicating with IP ECU's.

### 1642 — Grandmaster Clock ECU
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- To define the Grandmaster Clock in the system N/A The Grandmaster clock shall be implemented by TBD.

### 1643 — IP Deployment Matrix (7) => (8): Description modified. Current: IP Dep
- 版本：v8 ｜ 验证方式：- ｜ 适用：通用

### 1644 — Link Speed & Duplex
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- N/A The link speed and duplex shall be 100 Mbit/s full duplex for all Ethernet links.

### 1645 — Local Configurations
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- It shall be possible to download or update Local Configuration without the involvement of the supplier.
- This type of configuration is used in single ECU and shall not be accessible to other ECUs.

### 1646 — Multicast Addresses
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- The Local Network Control Block (224.0.0.0/24) shall be used for multicast addressing, according to the table below: Multicast address Description 224.0.0.1 All ECUs on this subnet 224.0.0.2 All domain masters on this subnet 224.0.0.117-224.0.0.250 Available for project specific multicast use cases.
- Multicast addresses from this range shall be appointed after discussions the base technology team.

### 1647 — Nomadic Device IP Address Configuration
- 版本：v4 ｜ 验证方式：Analysis ｜ 适用：通用
- REQPROD 76523 The IP address range and netmask for Nomadic Devices shall be configurable via a Local Configuration Data File.

### 1648 — Nomadic Devices IP Address Range
- 版本：v12 ｜ 验证方式：Analysis ｜ 适用：通用
- ECU “IHU” and “DHU”The IHU/DHU shall use the following IP address range for Nomadic Devices: Network ID Subnet Mask IHU/DHUExternal IPaddress NomadicDeviceHost AddressRange BroadcastAddress 192.168.5.0 / 28 255.255.255.240 192.168.5.1 192.168.5.2 -192.168.5.14 192.168.5.15 Table: IHU/DHU – IP address range for Nomadic DevicesECU “TCAM”The TCAM shall use the following IP address range for Nomadic Devices: Network ID Subnet Mask TCAMExternal IPaddress NomadicDeviceHost AddressRange BroadcastAddress 192.168.15.2 - 192.168.15.15 192.168.15.0 /28 255.255.255.240 192.168.15.1 192.168.15.14Table: TCAM – IP address range for Nomadic Devices

### 1651 — VLAN Deployment Matrix (6) => (7): Description modified. Current: VLAN
- 版本：v7 ｜ 验证方式：- ｜ 适用：通用

### 1652 — VLAN Membership
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- 96902 v8 VLAN priority To achieve QoS (Quality of Service), assign VLAN priority for different usecases Legacy ID: The ECUs shall use VLAN priorities for use case specific traffic within the central network domain (switched over the internal switches in VGM, IHU and DVR) according to the assignment in the following table.
- Legacy ID: For the X-call audio stream, the SSRC shall be set to 0xFFFF0000.
- Legacy ID: For the Emergency Video Record video stream, the SSRC shall be set to 0xFFFF0031.4.2.1.7.1.1.2 Media formats4.2.1.7.1.1.2.1 Audio format 96887 v4 X-call To clarity which audio format shell be defined, and define the number of channels.

### 1653 — LIN Master
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- LIN Standard All LIN Master nodes shall follow the LIN Specification Package version 2.1 or newer so they can be moved between LIN networks.
- Only frames specified by the LDF-file shall be implemented.
- LIN Master ECUs must also support LIN Slave ECUs that uses LIN standard 1.3, to be able to handle carry-over ECUs.

### 1654 — LIN Slave
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- LIN Standard All new LIN Slave node shall follow the LIN Specification Package 2.1 or higher so they can be moved between LIN networks.
- Only frames specified by the LDF-file shall be implemented.
- LIN Frame_size/DLC shall be free length and NOT fixed in identifier.

### 1655 — NAD addresses (Network ID) for private LIN slaves
- 版本：v5 ｜ 验证方式：Analysis ｜ 适用：通用
- LIN standard Non programmable or diagnosable LIN slaves shall have a NAD address with a different Network ID address compared to programmable and diagnosable LIN slaves on the same LIN network.4.2.1.7 IP Network4.2.1.7.1 Requirements

### 1657 — Network management CAN frame identifiers
- 版本：v37 ｜ 验证方式：Analysis ｜ 适用：通用
- - An ECU using AUTOSAR CAN Network Management shall be able to receive network management frames with CAN identifiers ranging from 0x500 to 0x53F.
- The CAN frame identifiers in the table below shall be used for transmission of network management frames containing the NM-PDU.
- ECU Alias NM CAN Network NM CAN Frame ID VFCVector ID PSCM AD Redundancy CAN 0x501 0x540 IMU AD Redundancy CAN 0x502 0x541 FLC AD Redundancy CAN 0x503 0x542 BBM AD Redundancy CAN 0x504 0x543 CEM Body CAN 0x501 0x541 CCM Body CAN 0x502 0x542 DDM Body CAN 0x503 0x543 PDM Body CAN 0x504 0x544 DRM Body CAN 0x505 0x545 POT Body CAN 0x507 0x547 RLDM Body CAN 0x509 0x549 TRM Body CAN 0x50A 0x555 RRDM Body CAN 0x510 0x550 SMD Body CAN 0x512 0x552 SMP Body CAN 0x513 0x553 SMB Body CAN 0x514 0x554 ILCM Body CAN 0x515 0x555 CEM Body Exposed CAN 0x52A 0x540 HCML Body Exposed CAN 0x531 0x541 HCMR Body Exposed CAN 0x532 0x542 RCML Body Exposed CAN 0x533 0x543 RCMR Body Exposed CAN 0x534 0x544 RCMM Body Exposed CAN 0x535 0x545 ASDM CAN FD 1 0x501 0x540 FSRR CAN FD 1 0x502 0x541 FSRL CAN FD 1 0x503 0x542 ASDM CAN FD 3 0x501 0x540 SODL CAN FD 3 0x502 0x541 SODR CAN FD 3 0x503 0x542 ASDM CAN FD 4 0x501 0x540 PAS CAN FD 4 0x502 0x541 ASDM CAN FD 2 0x501 0x540 FLR CAN FD 2 0x502 0x541 FLC CAN FD 2 0x503 0x542 ECM Chassis CAN 1 0x510 0x540 VDDM Chassis CAN 1 0x521 0x545 PSCM1 Chassis CAN 1 0x523 0x541 SAS Chassis CAN 1 0x527 0x544 PAS Chassis CAN 1 0x528 0x546 ASDM Chassis CAN 1 0x529 0x547 TCM Chassis CAN 1 0x530 0x548 HVSC Chassis CAN 1 0x531 0x549 MVEM Chassis CAN 1 0x532 0x550 ECM Chassis CAN 2 0x51F 0x546 VDDM Chassis CAN 2 0x522 0x549 SUM Chassis CAN 2 0x525 0x548 SCL Chassis CAN 2 0x526 0x547 BBM Chassis CAN 2 0x527 0x550 DSRC Connectivity CAN 0x508 0x548 TCAM Connectivity CAN 0x509 0x549 VGM Connectivity CAN 0x533 0x543 AUD Infotainment CAN 0x53A 0x54A IHU Infotainment CAN 0x53B 0x54B SRS Passive Safety CAN 0x50B 0x54B RMR Passive Safety CAN 0x50D 0x54D RML Passive Safety CAN 0x50E 0x54E ASDM Passive Safety CAN 0x50F 0x54F DVR Passive Safety CAN 0x511 0x551 DMM Passive Safety CAN 0x512 0x552 RMD Passive Safety CAN 0x513 0x553 EGSM Propulsion CAN 0x516 0x545 TCM Propulsion CAN 0x517 0x555 OBC Propulsion CAN 0x518 0x552 BECM Propulsion CAN 0x519 0x541 SRS Propulsion CAN 0x51A 0x544 IGM Propulsion CAN 0x51B 0x548 IEM Propulsion CAN 0x51C 0x547 DEM Propulsion CAN 0x51E 0x542 ECM Propulsion CAN 0x520 0x543 ECS Propulsion CAN 0x521 0x544 MVBM Propulsion CAN 0x522 0x550 MVCM Propulsion CAN 0x523 0x551 ISGM Propulsion CAN 0x524 0x549 WPT Propulsion CAN 0x525 0x556 VDDM Propulsion CAN 0x526 0x554 ESM Propulsion CAN 0x528 0x546 TACM Propulsion CAN 0x52B 0x553 VGM Propulsion CAN 0x52C 0x557 MGM Propulsion CAN 0x52D 0x558 CDD Propulsion CAN 0x52F 0x559 I Note 1: NM CAN Frames use IDs in range 0x501-0x53F, all unlisted in this range shall be considered spare IDs.

### 1662 — Bootloader CAN busoff handling
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- If hardware support automatic CAN busoff recovery, that recovery mechanism shall be enabled.
- If hardware doesn't support automatic bus-off recovery the bootloader shall check all active CAN controllers for bus-off status at maximum 10 ms intervals and if bus-off is detected start the bus-off recovery sequence within 10ms.
- Note: If a permanent busoff condition is detected that can not be recovered, and a complete and compatible application exist, the S3server timer shall still run and will finally elapse, causing and exit of the programming session.

### 1663 — Bootloader routing - Spare networks
- 版本：v7 ｜ 验证方式：Analysis ｜ 适用：通用
- ```txt GEELY Note-SWRS Revision 005 Volume No 01 Page No 155(1572) EESE strategical decision The ECU shall prepare the bootloader for adding new networks according to below.

### 1664 — Deployment of the J2534 requirements
- 版本：v7 ｜ 验证方式：Analysis ｜ 适用：通用
- To define which ECU that shall implement the J2534 requirements.
- Diagnostic and Bootloader Gateway Specification The VGM shall implement the J2534 requirements according to Diagnostic and Bootloader Gateway Specification for reference see Diagnostics & ECU Platform - Requisite documents.

### 1665 — SWDL time in aftermarket
- 版本：v30 ｜ 验证方式：Test ｜ 适用：通用
- To optimize SWDL in aftermarket. REQ - 017049 in Teamcenter: The maximum total time for purchase, deliverance and flashing new software to a complete vehicle is 0.8h (48 min). This time includes: - Connection/disconnection of the communication interface, e. g.

### 1666 — SWDL time in factory
- 版本：v33 ｜ 验证方式：Test ｜ 适用：通用
- In this case the software shall be pre-loaded before delivery to the factory.

### 1667 — Separate software files
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- Legacy ID: In order to increase software flexibility and reduce the amount of non-diffable content in vbf-files, all graphics, fonts, and speech files used by an ECU must be delivered separately without any software dependencies.

### 1669 — Communication Gateway Processing
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- Communication Gateway The gateway functionality (which is a part of the communication layer) shall run every Communication SW processing period.

### 1670 — Communication Stack Processing Period
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- - The Communication stack processing period shall be 5,0 ms.

### 1671 — Communication Stack Processing Period Jitter
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- - The jitter of the Communication stack processing period shall be less than 1 ms.

### 1672 — AUTOSAR version
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- AUTOSAR version 4.2.2 shall be used.
- Note: Other revisions such as 4.0.3 may be used after agreement with the base technology team.4.2.1.11 Startup Time4.2.1.11.1 Requirements

### 1673 — Startup Time
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Legacy ID: The ECU shall startup within 2,5 seconds and have full diagnostic and software download capabilities within this time.
- The time shall be measured from a state where the power to the ECU is completely turned off until it is capable of receiving diagnostic requests from both an internal tester in the vehicle, and an external tester connected through OBD.

### 1684 — Large buffers for response
- 版本：v6 ｜ 验证方式：Test ｜ 适用：通用
- For each network behind the GW: In application mode, the Domain GW shall be able to allocate up to 4 kB large buffers for response.

### 1685 — Minimum number of buffers for requests
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- For each network behind the GW: In application mode and if the total size of all current requests are less or equal to 4 KB RAM, the Domain Network GW shall be able to allocate at least 32 buffers for requests.
- If using static sized message buffers and/or not possible to reserve buffer pool only for requests: CEVT and the ECU supplier shall come to an agreement on the number of buffers to achieve similar performance.
- Example (dynamic sized message buffers and 4 KB buffer pool): A) One network behind the gateway: Several 100 bytes messages received, 32 x 100 bytes = total size 3200 bytes < 4 KB, at least 32 buffers shall be possible to allocate.

### 1686 — Minimum number of buffers for responses
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- For each network behind the GW: In application mode and if the total size of all current responses are less or equal to 8 KB RAM, the Domain Network GW shall be able to allocate at least 32 buffers for responses.
- If using static sized message buffers and/or not possible to reserve buffer pool only for responses: CEVT and the ECU supplier shall come to an agreement on the number of buffers to achieve similar performance.
- Example (dynamic sized message buffers and 8KB buffer pool): A) One network behind the gateway: Several 200 bytes messages received, 32 x 200 bytes = total size 6400 bytes < 8 KB, at least 32 buffers shall be possible to allocate.

### 1687 — Minimum RAM for request buffers
- 版本：v5 ｜ 验证方式：Test ｜ 适用：通用
- For each network behind the GW: In application mode, the Domain Network GW shall be able to reserve at least a 4 KB RAM buffer pool only for requests where several smaller buffers can be allocated from.
- If using static sized message buffers and/or not possible to reserve buffer pool only for requests: CEVT and the ECU supplier shall come to an agreement on used buffer sizes to achieve similar performance, more memory for buffers are needed.
- For static sized message buffers it can be larger gaps in the usable memory, hence this minimum RAM requirement may need to be increased dependent on how the static sized message buffers are chosen.

### 1688 — Minimum RAM for response buffers
- 版本：v5 ｜ 验证方式：Test ｜ 适用：通用
- For each network behind the GW: In application mode, the Domain Network GW shall be able to reserve at least a 8 KB RAM buffer pool only for responses where several smaller buffers can be allocated from.
- If using static sized message buffers and/or not possible to reserve buffer pool only for responses: CEVT and the ECU supplier shall come to an agreement on used buffer sizes to achieve similar performance, more memory for buffers are needed.
- The Domain Network GW must be able to allocate 4 KB buffer for diagnostic messages.

### 1689 — Large buffers for request
- 版本：v6 ｜ 验证方式：Test ｜ 适用：通用
- For each network behind the GW: In bootloader mode, the Domain Network GW shall be able to allocate up to 4 KB large buffers for request for CAN networks and up to 16 KB large buffers for request for FlexRay networks.

### 1690 — Large buffers for response
- 版本：v5 ｜ 验证方式：Test ｜ 适用：通用
- For each network behind the GW: In bootloader mode, the Domain Network GW shall be able to allocate up to 4 kB large buffers for response.

### 1691 — Minimum number of buffers for requests
- 版本：v5 ｜ 验证方式：Test ｜ 适用：通用
- For each network behind the GW: In bootloader mode and if the total size of all current requests are less or equal to 24 KB RAM for CAN and 32 KB RAM for FlexRay, the Domain Network GW shall be able to allocate at least 32 buffers for requests.
- If using static sized message buffers and/or not possible to reserve buffer pool only for requests: the project and the ECU supplier shall come to an agreement on the number of buffers to achieve similar performance.
- Example for CAN network connected behind gateway (dynamic sized message buffers and 24 KB buffer pool): A) One network behind the gateway: Several 600 bytes messages received, 32 x 600 bytes = total size 19200 bytes < 24 KB, at least 32 buffers shall be possible to allocate.

### 1692 — Minimum number of buffers for responses
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- For each network behind the GW: In bootloader mode and if the total size of all current responses are less or equal to 4 KB RAM, the Domain Network GW shall be able to allocate at least 32 buffers for responses.
- If using static sized message buffers and/or not possible to reserve buffer pool only for responses: the project and the ECU supplier shall come to an agreement on the number of buffers to achieve similar performance.
- Example (dynamic sized message buffers and 4 KB buffer pool): A) One network behind the gateway: Several 100 bytes messages received, 32 x 100 bytes = total size 3200 bytes < 4 KB, at least 32 buffers shall be possible to allocate.

### 1693 — Minimum RAM for request buffers
- 版本：v6 ｜ 验证方式：Test ｜ 适用：通用
- For each network behind the GW: In bootloader mode, the Domain Network GW shall be able to reserve at least a 24 KB RAM buffer pool for each CAN network and at least a 32 KB RAM buffer pool for each FlexRay network, reserved only for requests where several smaller buffers can be allocated from.
- If using static sized message buffers and/or not possible to reserve buffer pool only for requests: the project and the ECU supplier shall come to an agreement on used buffer sizes to achieve similar performance, more memory for buffers are needed.
- For static sized message buffers it can be larger gaps in the usable memory, hence this minimum RAM requirement may need to be increased dependent on how the static sized message buffers are chosen.

### 1694 — Minimum RAM for response buffers
- 版本：v5 ｜ 验证方式：Test ｜ 适用：通用
- For each network behind the GW: In bootloader mode, the Domain Network GW shall be able to reserve at least a 4 KB RAM buffer pool only for responses where several smaller buffers can be allocated from.
- If using static sized message buffers and/or not possible to reserve buffer pool only for response: the project and the ECU supplier shall come to an agreement on used buffer sizes to achieve similar performance, more memory for buffers are needed.
- For static sized message buffers it can be larger gaps in the usable memory, hence this minimum RAM requirement may need to be increased dependent on how the static sized message buffers are chosen.

### 1695 — Support for queued request
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- For each network behind the GW: In bootloader mode and if the total request size is less or equal to 24kB, the Domain Network GW shall able to receive two(2) queued request on three(3) communication channels without sending flow control Wait (FC.

### 1711 — Diagnostic request format on CAN
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- All in-vehicle GW connected to CAN network shall send/receive diagnostic request asdefined in DoCAN [GW_24] ISO 15765-2 normal addressing 11 bit CAN ID with ECU logicaladdresses as defined in [GW_1] UDS Services.

### 1712 — Diagnostic response format on CAN
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- All in-vehicle GW connected to FlexRay network shall send/receive diagnostic response asdefined in DoCAN [GW_24] ISO 15765-2 normal addressing 11 bit CAN ID with ECU logicaladdresses as defined in [GW_1] UDS Services.
- maximum time between c consecutive frames, C_Cs, performance requirements.4.5.1.8.1.1.1 Diagnostic requests IP to CANThis section will describe and give grounds for the following requirements: REQPROD xxxxx Latency IP to CAN, GW_IP-CAN_L1The IP to CAN Vehicle GW shall receive and validate the complete request from IP before the request is transmitted on the Sub network (CAN), as specified in [ISO 13400-2].
- how many frames that shall be sent.

### 1716 — Diagnostic response format on FlexRay
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- All in-vehicle GW connected to FlexRay network shall send/receive diagnostic response as defined in CoFr [GW_25] ISO 10681-2 with ECU logical addresses as defined in [GW_1] UDS Services.

### 1717 — Diagnostic request format on internal IP network
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- All in-vehicle GW connected to internal IP network shall send/receive diagnostic request with a DoIP header with payload type 8001 as defined in DoIP [GW_26] ISO 13400-2 with ECU logical addresses as defined in [GW_1] UDS Services and with the three lowest nibbles in the ECU logical address in the three lowest nibbles in the IP TA and the Vehicle GW internal IP address in the IP SA.
- Diagnostic request format on FlexRay Page No825(1572) All in-vehicle GW connected to FlexRay network shall send/receive diagnostic request as defined in CoFr [GW_25] ISO 10681-2 with ECU logical addresses as defined in [GW_1] UDS Services.
- Receiving ECU shall analyse if the target address (CoFr TA) is within a valid range.

### 1720 — Internal functional request handling
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- The in-vehicle GW shall be able route a functional request to all connected networks and to the in-vehicle GW it self.

### 1721 — Prioritize functional request
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- A functional TesterPresent must be able to reach a target ECU in non-default session, to keep the ECU in non-default session, independent of other possible physical request that could be queued in the gateway.
- An in-vehicle gateway shall always prioritize a functional requests over a physical request.
- An exception of this generic requirement may be needed for the Vehicle GW connected to the external tester, which may need to work in application level to e.

### 1722 — Allocation of buffers from buffer pools
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- To be able to specify max values for latency thru a gateway, there must also be a max time for allocating buffers.
- If the total size of messages does not exceed the total size of available memory for buffers, an in-vehicle gateway shall be able to allocate a suitable buffer for the message within 1ms.
- Rationale: Fragmentation of memory for buffers must be taken in account when implementing an algorithm for allocation of buffers.

### 1723 — Static allocated buffers vs dynamic allocated buffers
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Indication to ECU supplier how much more memory that is needed if a static sized buffer algorithm is used instead of a dynamic sized buffer algorithm If static sized buffers are used instead of dynamic sized buffers, it shall be estimated that at least 50% more memory is needed.
- If using static sized message buffers and/or not possible to reserve separate buffers for request and responses: the project and the ECU supplier shall come to an agreement on used buffer structure to achieve similar performance, supplier shall count with that at least 50% more memory is needed when selecting hardware4.5.1.1.1 General allocation of buffers requirements, part 1This section will describe and give grounds for the following requirements: REQPROD 74649 Allocation of buffers from buffer poolsREQPROD 436123 Static allocated buffers vs dynamic allocated buffersThis document does not specify exactly how buffer allocation shall be implemented, this is up to the implementer.
- Hence, optimization of buffer usage may be need to be handled by project and by gateway by gateway to get a compromise between efficiency and cost.

### 1724 — Flow control mechanism for diagnostic messages
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- An in-vehicle gateway shall support flow control mechanism on the connected networks, both for request/downstream and for responses/upstream.
- Rationale: No messages or frames shall be lost, if the receiver cannot receive the complete message directly due to out of “high level” buffers, it should be negotiated between sender and receiver when the remaining part can be sent.

### 1725 — Gatewaying-on-the-fly
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- buffers less than the complete message can also be used to gateway messages) When both connected networks supports gatewaying-on-the-fly, the gateway shall use the gatewaying-on-the-fly functionality to reduce latency.
- Flexray and CAN, "gateway-on-the-fly" shall be used for these networks to reduce latency.
- Comment: The TP threshold for gatewaying-on-the-fly shall be used to for the complete transmission.

### 1726 — Generic gateway latency requirement
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- When the gateway has received enough data on the receive (Rx) communication channel to fill an L-PDU on the transmit (Tx) side and the gateway can allocate a communication channel on the Tx side, start of transfer on the Tx side shall be within 10ms.

### 1727 — Multiple CPU design in the GW ECU
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- If a multiple CPU solution is used in the GW ECU for implementing the gateway functionality, the internal interface between the CPUs shall be design to still fulfil the GW ECU requirements.
- Rationale: Latency requirement on the GW ECU shall be kept, which e.
- g implies that gateway-on-the-fly shall be used on the internal interface to keep the GW ECU latency requirement (e.

### 1728 — No re-sending of diagnostic requests
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- If a communication error occurs, an in-vehicle gateway shall not re-send a diagnostic request.
- Comment: Resending of diagnostic requests shall only be allowed for the external tester.

### 1729 — No re-sending of diagnostic responses
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- If a communication error occurs, an in-vehicle gateway shall not re-send a diagnostic response.

### 1730 — Release buffers on communication errors
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- If a communication error occurs, the in-vehicle gateway shall release corresponding buffers used for the transmit (Tx) and/or receive (Rx) communication channels.

### 1731 — Routing table
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- An in-vehicle gateway shall have routing table for all possible paths to the ECUs after the gateway in the network topology, functionally addressed request included.

### 1732 — Separate buffers for requests and responses
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Request and response buffers must be independent of each other for supporting functionality as parallel requests and queued requests An in-vehicle gateway shall have separate and independent buffers for diagnostic request/downstream and for diagnostic responses/upstream.

### 1733 — Separate CCs for request and responses
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- Request and response communication channels must be independent of each other for supporting functionality as parallel requests and queued requests An in-vehicle gateway shall have separate and independent communication channels (CCs) for diagnostic request/downstream and for diagnostic responses/upstream.

### 1734 — Session layer time-out handling
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- In-vehicle gateways shall not unpack and analyze data part of messages.
- An in-vehicle gateway shall not handle Session layer time-outs.
- Comment: Session layer time-outs handling (time-out between request and response message) shall only be handled by the external and/or internal tester.

### 1735 — Transfer all functional request before a reset of gateway
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- If an in-vehicle gateway receives a functional request that will lead to a reset of the in-vehicle gateway, the gateway shall first transmit all functional diagnostic to the connected network(s) before the gateway performs the reset.
- Comment: Implementation may differ depending on network type, e.
- A request to reset in-vehicle GW (functional or physical addressed) shall not be sent if there is pending request/responses in the vehicle.

### 1736 — Transport layer routing
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- To be able to handle different speed and messaged sizes on different networks All segmented diagnostic messages shall be routed thru a transport layer with flow control mechanism.4.5.1.1.5 OverviewThis document describes and defines requirements for in-vehicle gateways for diagnostic communication for next generation of CEVT with the electrical architecture for the SPA platform.
- Diagnostic communication Cover both 'Diagnostic' and 'Software Download' communication Domain ID Defines which domain that shall be addressed.
- internal IP Network) and Domain Network ECU ID Defines which ECU that shall be addressed.

### 1737 — Keep chronologic order of parallel physical messages
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- The in-vehicle GW shall preserve the chronological order of received parallel physical request/responses when sending out the request/response on the networks.
- Rationale: Fair arbitration shall be implemented in the gateway, i.
- one channel may not starve another channel.

### 1738 — Parallel physical requests to different ECUs
- 版本：v5 ｜ 验证方式：Test ｜ 适用：通用
- The in-vehicle GW shall support parallel requests to different ECUs (different target addresses).
- Different target addresses includes the GW ECU, and if request is SWDL request the consequence is that GW ECU must be able to re-programming itself at the same time as requests are gatewayed to other ECUs.
- For example flashing of the GW ECU shall not disturb the gateway functionality to other ECUs.

### 1739 — Wait for available communication channel
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Clarify that messages shall not be dropped if all communication channels are currently occupied.
- Message shall be kept and send as soon as a communication channel is released If no communication channel can be allocated, i.
- all communication channels are currently occupied by other messages, the in-vehicle GW must wait until a communication channel is released and then send the message on the released communication channel.

### 1740 — Protection of routing table
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- An in-vehicle gateway shall only allow reconfiguration of the routing table when the routing table is not in use (e.
- Rationale: Reconfiguration during normal operation (application running and routing table is in use) shall not be possible.

### 1741 — Static routing rules
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- An in-vehicle gateway shall only support statically defined routing rules.
- Rationale: The gateway shall not support dynamic routing rules for diagnostic messages.
- All routing paths shall be statically defined, and do not depend on the content of a diagnostic message.

### 1742 — Updateable routing table
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- Configuration routing table in gateway shall be updateable if a new ECU is added which is not included in the current routing table.
- The routing configuration table in DIAG shall be updateable at post-build time.
- 4.5.1.4 Gateway Generic SWDL4.5.1.4.1 Gateway sequence diagramsThis section contain no new requirements, but describes in some more details example of traffic on the networks as consequence of the functionality described in section 'Queued physical requests to one ECU'4.5.1.4.1.1 Queued physical requests to same ECUThe functionality described in section 'Queued physical requests to one ECU' implies that flow control mechanism must be used, i.

### 1743 — Keep chronological order for queued messages
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- If several queued diagnostic requests to one ECU, with same target address are sent thru the gateway, the chronological order of the request must be preserved.
- The in-vehicle GW for SWDL shall preserve the chronological order of queued physical request/responses to/from a target ECU.
- The queued (second) message shall never be sent out on a network before the first message.

### 1744 — Queued physical request to one ECU
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- The in-vehicle GW for SWDL shall support at least one queued physical request to a target ECU (i.
- When tester receive the response from the first request, the tester can send next request, which now will be the queued request and so on.4.5.1.4.3 Routing tableThis section will describe and give grounds for the following requirements:• REQPROD 77685 Static routing configurationFor bootloader and software download it is not possible to update the routing table burned in to the non-volatile memory, so the routing table must be able to cover all possible connections from the start, so that a ECU can be added to the network topology with out updating the bootloader.

### 1745 — Static routing configuration
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- If a new ECU is added, the Bootloader, PBL and SBL, shall be able to handle this without update of bootloader.
- Bootloader shall use Domain ID, Network ID and ECU ID ranges when forwarding messages.
- The routing configuration table in SWDL shall be able to route all possible ECU IDs in a network.

### 1804 — Calibration of agedDTCLimit
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- If not otherwise is specified by this document or is approved by CEVT Electrical Architecture, the AgedDTCLimit shall be calibrated in such a way that the following is met:· The DTC aging counter (OCC2 or OCC5) shall reach the agedDTCLimit when the fault has not been detected at such a long time that it probably will not occur and be detected again.
- Refer to [Data 12] General Diagnostic Guideline for recommendations and guidelines on how this requirement shall be met.

### 1805 — Calibration of confirmedDTCLimit
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- item 6 If not otherwise is specified by this document or is approved by the responsible authority appointed by OEM, the confirmedDTCLimit shall be calibrated in such a way that the following is met:· Calibration of DTC test sample failed is equal to the confirmedDTCLimit when it is very likely that that the most customers observe a symptom (caused by the detected fault) and is bothered by the symptom in such extent that they require repair of the vehicle.
- Note that customer symptoms may be caused by actions (e.
- telltale, text message, etc.), it shall be regarded as a customer symptom.

### 1806 — Calibration of DTC test sample failed
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- If not otherwise is specified by this document or is approved by the responsible authority appointed by OEM, the DTC test sample failed criteria shall be calibrated in such a way that the following is met:• The DTC test sample shall fail when the monitored item does not meet the design requirements specified by the implementer.

### 1807 — Calibration of DTC test sample passed
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- If not otherwise is specified by this document or is approved by the responsible authority appointed by OEM, the DTC test sample passed criteria shall be calibrated in such a way that the following is met:• The DTC test sample shall pass when the monitored item meet the design requirements specified by the implementer.

### 1808 — Calibration of DTCTestFailedLimit
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Setion Calibration of DTCs, item 4 If not otherwise is specified by this document or is approved by the responsible authority appointed by OEM, the DTCTestFailedLimit shall be calibrated, i.
- the size of the DTC fault detection counter (FDC 10) step-up (increase) value shall be adjusted, in such a way that the following is met:• The DTC fault detection counter (FDC10) shall reach a value that is equal to the DTCTestFailedLimit (i.
- Note that customer symptoms may be caused by actions (e.

### 1809 — Calibration of DTCTestPassedLimit
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Setion Calibration of DTCs, item 5 If not otherwise is specified by this document or is approved by the responsible authority appointed by OEM, the DTCTestPassedLimit shall be calibrated, i.
- the size of the DTC fault detection counter (FDC 10) step-down (decrease) value shall be adjusted, in such a way that the following is met:• The DTC fault detection counter (FDC10) shall reach a value that is equal to the DTCTestPassedLimit (i.
- Refer to [Data 12] General Diagnostic Guideline for recommendations and guidelines on how this requirement shall be met.

### 1810 — Calibration of unconfirmedDTCLimit
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Section Calibration of DTCs, item 3 If not otherwise is specified by this document or is approved by the responsible authority appointed by OEM, the unconfirmedDTCLimit shall be calibrated in such a way that the following is met:· The DTC fault detection counter (FDC10) shall reach a value that is equal to or greater than the unconfirmedDTCLimit when it is likely that at least some customers observer a symptom (caused by the detected fault) but probably only some of them is bothered by the symptom in such extent that they require repair of the vehicle.
- Note that customer symptoms may be caused by actions (e.
- telltale, text message, etc.), it shall be regarded as a customer symptom.

### 1811 — Clear DTC information by diagnostic service
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements in implementation of clear of DTC information" - item 1 All stored DTC information for all DTCs supported by the ECU, with the exceptions defined in [Data_50] Road vehicles – Diagnostics systems – Diagnostic services, UDS - Data - External publications, shall be cleared when requested by diagnostic service specified in [Data_1] UDS Services.

### 1812 — Clear DTC information when a DTC is aged
- 版本：v6 ｜ 验证方式：Analysis ｜ 适用：4.0.x 与 4.1+ 分别定义
- x: When the counter used for aging of a DTC reaches the value agedDTCLimit defined for the DTC, no DTC information shall be cleared with some exception (reset of a DTC status bit and some DTC status indicators) that is specified in the document.
- The agedDTCLimit shall be a value in the range of [1, 255].
- The counter used for aging shall either be operation cycle counter 2 or 5.

### 1813 — Clear DTC information when an aged DTC reoccurs
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：4.0.x 与 4.1+ 分别定义
- the counter used for aging of the DTC has reached the value agedDTCLimit defined for the DTC), all DTC information, except the DTC status bits and FDC10, shall be cleared for that DTC.

### 1814 — Clear DTC information when the long term memory overflows
- 版本：v6 ｜ 验证方式：Analysis ｜ 适用：通用
- To define the rules for what DTC information that shall be stored and what shall be discarded in the event that long term DTC memory is full when new DTC information needs to be stored.
- Table "Requirements in implementation of clear of DTC information" - item 2 If storage of DTC information is required but available storage for the DTC information in the long term memory is already full, all DTC information for all DTCs supported by the ECU, except the DTC status bits and FDC10, of lowest storage priority (see note 1 below) shall be cleared from the long term memory and replaced by the data that is required to be stored if the data that is required to be stored has higher storage priority according to the following priority order (1 is the highest priority):1.
- They shall have the lowest storage priority (i.

### 1815 — Detected of events associated with driver indications
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- by a service book instruction, text message, etc.) the driver to bring the car to a workshop, the workshop may need to be able to find the root cause for this indication by a DTC.
- Section "Detection of events associated with driver indications" A DTC test indicating the cause of the event that triggers an activation of a driver indication (which when activated, recommends the driver to bring the car to a workshop) shall be implemented as required by a study performed by the implementer and approved by the responsible authority appointed by OEM.4.5.2.1.2.18 Requirements from section DTC status bits

### 1816 — DTC values
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- Section "Detection of faults" Unless otherwise specified in the following sections, one unique DTC value shall be used to identify each fault that can be detected by a DTC test in an ECU.
- the fault detection counter) is also combined and no more than one instance of the DTC shall be reported in any response to the services specified in reference [Data_1] UDS Services.
- Where the implementer identifies a requirement for separate repair action or fault confirmation process for DTCs that are shown with the same DTC then the responsible authority appointed by OEM may permit the use of different DTCs.

### 1817 — Failure type value for DTCs
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- Section "Detection of faults" Unless specifically defined in this document, DTCs shall use Failure Type values which are the same as the DTCFailureTypeByte defined by [Data_51] Diagnostic trouble code definitions,UDS - Data - External publications, as appropriate depending on the type of fault.
- A failure type value of 0x00 may only be used if the Base DTC description includes the failure type and is approved in [Data_4] Global Master Reference Database.
- In such cases the Base DTC may not be combined with any other failure type values.

### 1818 — Generic Test Run Criteria - car mode transition inhibit criteria
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Changing car mode may cause transitional effects that may trigger a DTC test.
- This must be avoided in order not to set false DTCs.
- Section "Detection of faults" A II DTC tests shall be inhibited during 5 seconds from any transition from one car mode to another.

### 1819 — Generic Test Run Criteria - car modes inhibit criteria
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- In some car modes vehicle functions may be inhibited which may cause other behaviour than normally expected by the DTC tests.
- Section "Detection of faults" A II DTC tests shall be inhibited when the vehicle is set in any of the car modes Factory,Transport or Crash.

### 1820 — Generic Test Run Criteria - enable criteria
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- A general rule is that all DTC tests shall run all the time that the ECU is "in operation".
- Section "Detection of faults" DTC tests shall be enabled all the time during an operation cycle provided that no inhibited criteria are met.
- in order to mitigate the effect of the fault on customer functions or system safety), the DTC tests shall not be inhibited after the ECU has performed the action (e.

### 1821 — Generic Test Run Criteria - low power inhibit criteria
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- DTC tests shall be regarded as unreliable when electrical power availability is limited, i.
- the tests shall be inhibited.
- Section "Detection of faults" If the ECU is power supplied from the 12 V system for which the EIPowerLevel signal is applicable, all DTC tests shall be inhibited when electrical power availability is limited, as indicated by EIPowerLevel 1.

### 1822 — Generic Test Run Criteria - low voltage inhibit criteria
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- DTC tests shall be regarded as unreliable when the ECU supply voltage is low, i.
- the tests shall be inhibited.
- Section "Detection of faults" A II DTC tests shall be inhibited when voltage supplied to the ECU is lower than required for ensuring correct fault monitoring.

### 1823 — Generic Test Run Criteria - usage mode transition inhibit criteria
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- Changing usage mode may cause transitional effects that may trigger a DTC test.
- This must be avoided in order not to set false DTCs.
- Section "Detection of faults" If not otherwise is specified, all DTC tests shall be inhibited during 5 seconds from any transition from one usage mode to another.

### 1824 — Test Run Criteria - Updating the DTC Fault Detection Counter
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- If a DTC test is stopped by an inhibit criteria the actual test may not be allowed to stop due to safety or other functional requirements.
- Section "Detection of faults" If a DTC test is inhibited it shall stop updating the DTC Fault Detection Counter (FDC10).4.5.2.1.2.10 Requirements from section Detection of faults in external electrical circuits

### 1825 — Base DTC value for detection of corrupt data received from other ECU by end-to-end checksum
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults caused by signal/data content received from other ECUs" The DTC test for detection of corrupt data received from other ECU by end-to-end checksum shall use one unique base DTC value for each tested signal, in the range U2D00 to U2DFF, as defined in [Data_51] Diagnostic trouble code definitions, UDS - Data - External publications and [Data_4] Global Master Reference Database.

### 1826 — Base DTC value for detection of corrupt data received from other ECU by rolling counter
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults caused by signal/data content received from other ECUs" - item 4.1 The DTC test for detection of corrupt data received from other ECU by rolling counter shall use one unique base DTC value for each tested signal, in the range U2D00 to U2DFF, as defined in [Data_51] Diagnostic trouble code definitions , UDS - Data - External publications and [Data_4] Global Master Reference Database.

### 1827 — Base DTC value for detection of corrupt data received from other ECU by up-date-bit
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults caused by signal/data content received from other ECUs" The DTC test for detection of corrupt data received from other ECU by up-date-bit shall use one unique base DTC value for each tested signal, in the range U2F00 to U2FFF if the DTC is not emission related and U0100 to U02FF if the DTC is emission related, as defined in [Data_51] Diagnostic trouble code definitions, UDS - Data - External publications and [Data_4] Global Master Reference Database.

### 1828 — Base DTC value for detection of other ECU not operating normally
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults caused by signal/data content received from other ECUs" - item 1.1 The DTC test for detection of other ECU not operating normally shall use one unique base DTC value for each signal (indicating reduced functionality in the other ECU), in the range U2C00 to U2CFF, as defined in:[Data_51] Diagnostic trouble code definitions[Data_4] Global Master Reference Database

### 1829 — Base DTC value for detection of other ECU sending data tagged as invalid
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults caused by signal/data content received from other ECUs" - item 2.1 The DTC test for detection of other ECU sending data tagged as invalid shall use one unique base DTC value for each signal, in the range U2C00 to U2CFF, as defined in [Data_51]Diagnostic trouble code definitions and [Data_4] Global Master Reference Database

### 1830 — Base DTC value for detection of other ECU sending faulty data
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults caused by signal/data content received from other ECUs" - item 3.1 The DTC test for detection of other ECU sending faulty data shall use one unique base DTC value for each tested signal, in the range U2D00 to U2DFF, as defined in [Data_51] Diagnostic trouble code definitions and [Data_4] Global Master Reference Database.

### 1831 — Detection of corrupt data received from other ECU by end-to-end checksum
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- To handle the situation where there may be a customer complaint and a symptom associated with the ECU generating the DTC but the root cause is located on another ECU which may or may not be exhibiting any symptoms.
- Table "Requirements on detection of faults caused by signal/data content received from other ECUs" If the ECU detects, by the data protection mechanism end-to-end checksum implemented at application level in the ECU, that a data value received from other ECU is corrupted each such fault shall also be identified by an appropriate DTC.

### 1832 — Detection of corrupt data received from other ECU by rolling counter
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- To handle the situation where there may be a customer complaint and a symptom associated with the ECU generating the DTC but the root cause is located on another ECU which may or may not be exhibiting any symptoms.
- where the primary reason for the fault monitor is another than to support generation of DTC information)each such fault shall also be identified by an appropriate DTC.

### 1833 — Detection of corrupt data received from other ECU by up-date-bit
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- To handle the situation where there may be a customer complaint and asymptom associated with the ECU generating the DTC but the root cause is located on another ECU which may or may not be exhibiting any symptoms.
- set to the value 1 when expected), that a data value received from other ECU is corrupted each such fault may also be identified by an appropriate DTC.
- Note: The DTC may be mandatory if the DTC is emission related but this is not specified by this document.

### 1834 — Detection of other ECU not operating normally
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- To handle the situation where there may be a customer complaint and asymptom associated with the ECU generating the DTC but the root cause is located on another ECU which may or may not be exhibiting any symptoms.
- where the primary reason for the fault monitor is another than to support generation of DTC information) each such fault shall also be identified by an appropriate DTC.
- Otherwise, the ECU shall be able to detect that other ECU not operating normally as defined by a feasibility study performed by the implementer.

### 1835 — Detection of other ECU sending data tagged as invalid
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- To handle the situation where there may be a customer complaint and a symptom associated with the ECU generating the DTC but the root cause is located on another ECU which may or may not be exhibiting any symptoms.
- where the primary reason for the fault monitor is another than to support generation of DTC information) each such fault shall also be identified by an appropriate DTC.
- Otherwise, the ECU shall be able to detect that other ECU sends data tagged as invalid as defined by a feasibility study performed by the implementer.

### 1836 — Detection of other ECU sending faulty data
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- To handle the situation where there may be a customer complaint and a symptom associated with the ECU generating the DTC but the root cause is located on another ECU which may or may not be exhibiting any symptoms.
- where the primary reason for the fault monitor is another than to support generation of DTC information) each such fault shall also be identified by an appropriate DTC.
- Otherwise, the ECU shall be able to detect that other ECU sends faulty data as defined by a feasibility study performed by the implementer.

### 1837 — Failure type value for detection of corrupt data received from other ECU by end-to-end checksum
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults caused by signal/data content received from other ECUs" The DTCs for detection of corrupt data received from other ECU by end-to-end checksum shall use Failure Type value 0x83.

### 1838 — Failure type value for detection of corrupt data received from other ECU by rolling counter
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults caused by signal/data content received from other ECUs" - item 4.1 The DTCs for detection of corrupt data received from other ECU by rolling counter shall use Failure Type value 0x82.

### 1839 — Failure type value for detection of corrupt data received from other ECU by up-date bit
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults caused by signal/data content received from other ECUs" The DTCs for detection of corrupt data received from other ECU by up-date bit shall use Failure Type value 0x82.

### 1840 — Failure type value for detection of other ECU not operating normally
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults caused by signal/data content received from other ECUs" - item 1.1 The DTCs for detection of other ECU not operating normally shall use Failure Type value 0x92.

### 1841 — Failure type value for detection of other ECU sending data tagged as inv...
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults caused by signal/data content received from other ECUs" - item 2.1 The DTCs for detection of other ECU sending data tagged as invalid shall use Failure Type value 0x81.

### 1842 — Failure type value for detection of other ECU sending faulty data
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults caused by signal/data content received from other ECUs" - item 3.1 The DTCs for detection of other ECU sending faulty data shall use Failure Type value 0x86.

### 1843 — Root DTC for ECU not operating normally
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults caused by signal/data content received from other ECUs" - item 1.1 The ECU transmitting a signal that indicates it is not operating normally shall set an appropriate DTC for this fault (this can be either a DTC relating to the root cause of the situation if the root cause exists in the transmitting ECU, or a secondary DTC if the root cause is not in the transmitting ECU).

### 1844 — Root DTC for ECU sending data tagged as invalid
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults caused by signal/data content received from other ECUs" - item 2.1 The ECU transmitting a signal that is tagged as invalid shall set an appropriate DTC for this fault (this can be either a DTC relating to the root cause of the situation if the root cause exists in the transmitting ECU, or a secondary DTC if the root cause is not in the transmitting ECU).

### 1845 — Test Run Criteria for detection of corrupt data received from other ECU by end-to-end checksum
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults caused by signal/data content received from other ECUs" The DTC test for detection of corrupt data received from other ECU by end-to-end checksum shall run each time updated data, for which a test i simplemented, is received from another ECU.

### 1846 — Test Run Criteria for detection of corrupt data received from other ECU by rolling counter
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults caused by signal/data content received from other ECUs" - item 4.1 The DTC test for detection of corrupt data received from other ECU by rolling counter shall run each time updated data, for which a test i simplemented, is received from another ECU.

### 1847 — Test Run Criteria for detection of corrupt data received from other ECU by up-date bit
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- ble "Requirements on detection of faults caused by signal/data content received from other ECUs" The DTC test for detection of corrupt data received from other ECU by up-date bit shall run each time updated data, for which a test i simplemented, is received from another ECU.

### 1848 — Test Run Criteria for detection of other ECU not operating normally
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- The DTC test for detection of other ECU not operating normally shall run each time the updated data indicating reduced functionality in the other ECU is received.

### 1849 — Test Run Criteria for detection of other ECU sending data tagged as invalid
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults caused by signal/data content received from other ECUs" - item 2.1 The DTC test for detection of other ECU sending data tagged as invalid shall run each time updated data is received from another ECU.
- The test shall be inhibited if the received data is detected as corrupt by a data protection mechanism.

### 1850 — Test Run Criteria for detection of other ECU sending faulty data
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults caused by signal/data content received from other ECUs" - item 3.1 The DTC test for detection of other ECU sending faulty data shall run each time updated data, for which a test i simplemented, is received from another ECU.
- If plausibility check is used as fault detection logic the test shall be inhibited if a DTC test for one (or more) of the compared signals (used to evaluate the plausibility of the received signal) has detected a fault on that signal.

### 1851 — Base DTC value for detection of events caused by customer operating vehi...
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults caused by the ECU operating environment or customer actions" - item 2.1 If a DTC test for events caused by customer operating vehicle or vehicle equipment outside specification is implemented the test shall use the base DTC value U2E02.

### 1852 — Base DTC value for detection of events caused by ECU supply voltage is t...
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults caused by the ECU operating environment or customer actions" - item 3.2 If a DTC test for events caused by ECU supply voltage is too low for full operation is implemented the test shall use the base DTC value U2E04.

### 1853 — Base DTC value for detection of events caused by ECU supply voltage is t...
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults caused by the ECU operating environment or customer actions" - item 3.1 If a DTC test for events caused by ECU supply voltage is too high for full operation is implemented the test shall use the base DTC value U2E03.

### 1854 — Base DTC value for detection of events caused by other condition that is out of range for full opera
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults caused by the ECU operating environment or customer actions" - item 4.1 If DTC tests for events caused by other conditions are out of range for full operation is implemented the tests shall use a base DTC value in the range U2E05 to U2EFF.
- The tests shall use one unique base DTC value for each event.

### 1855 — Base DTC value for detection of faults caused by ambient teperature too ...
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults caused by the ECU operating environment or customer actions" - item 1.1 If a DTC test for ambient temperature too high for full and correct operation is implemented the test shall use the base DTC value U2E00.

### 1856 — Base DTC value for detection of faults caused by ambient teperature too low
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults caused by the ECU operating environment or customer actions" - item 1.2 If a DTC test for ambient temperature too low for full and correct operation is implemented the test shall use the base DTC value U2E01.

### 1857 — Base DTC value for detection of other faults inferred from system behaviour
- 版本：v1 ｜ 验证方式：Inspection ｜ 适用：通用
- Detection of other faults faults inferred from system behaviour shall use one unique base DTC value for each component, system or part of system that is monitored, to identify the fault.

### 1858 — Detection of events caused by customer operating vehicle or vehicle equi...
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- To be able to handle the situation where there may be a customer complaint and a symptom associated with the ECU but the root cause is that the ECU is operating outside of its design specification.
- where the primary reason for the fault monitor is another than to support generation of DTC information) each such event shall also be identified by an appropriate DTC.
- Otherwise, the ECU shall be able to detect that such events as defined by a feasibility study performed by the implementer.

### 1859 — Detection of events caused by ECU supply voltage is too high for full op...
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- To be able to handle the situation where there may be a customer complaint and a symptom associated with the ECU but the root cause is that the ECU is operating outside of its design specification.
- where the primary reason for the fault monitor is another than to support generation of DTC information) each such event shall also be identified by an appropriate DTC.
- Otherwise, the ECU shall be able to detect that such events as defined by a feasibility study performed by the implementer.

### 1860 — Detection of events caused by ECU supply voltage is too low for full ope...
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- To be able to handle the situation where there may be a customer complaint and a symptom associated with the ECU but the root cause is that the ECU is operating outside of its design specification.
- where the primary reason for the fault monitor is another than to support generation of DTC information) each such event shall also be identified by an appropriate DTC.
- Otherwise, the ECU shall be able to detect that such events as defined by a feasibility study performed by the implementer.

### 1861 — Detection of events caused by other condition that is out of range for f...
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- To be able to handle the situation where there may be a customer complaint and a symptom associated with the ECU but the root cause is that the ECU is operating outside of its design specification.
- where the primary reason for the fault monitor is another than to support generation of DTC information) each such event shall also be identified by an appropriate DTC.
- Otherwise, the ECU shall be able to detect that such events as defined by a feasibility study performed by the implementer.

### 1862 — Failure type value for detection of events caused by customer operating ...
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults caused by the ECU operating environment or customer actions" - item 2.1 If a DTC test for events caused by customer operating vehicle or vehicle equipment outside specification is implemented the test shall use Failure Type value 0x68.

### 1863 — Failure type value for detection of events caused by ECU supply voltage ...
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults caused by the ECU operating environment or customer actions" - item 3.1 If a DTC test for events caused by ECU supply voltage is too high for full operation is implemented the test shall use Failure Type value 0x68.

### 1864 — Failure type value for detection of events caused by ECU supply voltage ...
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults caused by the ECU operating environment or customer actions" - item 3.2 If a DTC test for events caused by ECU supply voltage is too low for full operation is implemented the test shall use Failure Type value 0x68.

### 1865 — Failure type value for detection of events caused by other condition tha...
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults caused by the ECU operating environment or customer actions" - item 4.1 If a DTC test for events caused by other condition is out of range for full operation is implemented the test shall use Failure Type value 0x68.

### 1866 — Failure type value for detection of faults caused by ambient teperature
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults caused by the ECU operating environment or customer actions" - item 1.1 and 1.2 If a DTC test for ambient temperature too high or too low for full and correct operation is implemented the test shall use Failure Type value 0x68.

### 1867 — Test period time for detection of events caused by customer operating ve...
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults caused by the ECU operating environment or customer actions" - item 2.1 If a DTC test for events caused by customer operating vehicle or vehicle equipment outside specification is implemented the test shall produce Test Samples periodically every 100 ms or faster whenever the Test Run Criteria are met.

### 1868 — Test period time for detection of events caused by ECU supply voltage is...
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults caused by the ECU operating environment or customer actions" - item 3.1 If a DTC test for events caused by ECU supply voltage is too high for full operation is implemented the test shall produce Test Samples periodically every 100 ms or faster whenever the Test Run Criteria are met.

### 1869 — Test period time for detection of events caused by ECU supply voltage is...
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults caused by the ECU operating environment or customer actions" - item 3.2 If a DTC test for events caused by ECU supply voltage is too low for full operation is implemented the test shall produce Test Samples periodically every 100 ms or faster whenever the Test Run Criteria are met.

### 1870 — Test period time for detection of events caused by other condition that is out of range for full ope
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults caused by the ECU operating environment or customer actions" - item 4.1 If a DTC test for events caused by other condition is out of range for full operation is implemented the test shall produce Test Samples periodically, while the Test Run Criteria are met, at a rate defined by the implementer and approved by the responsible authority appointed by OEM.
- If not defined by the implementer the test period time shall be 100 ms or faster.

### 1871 — Test period time for detection of faults caused by ambient teperature
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults caused by the ECU operating environment or customer actions" - item 1.1 and 1.2 If a DTC test for ambient temperature too high or too low for full and correct operation is implemented the test shall produce Test Samples periodically every 100 ms or faster whenever the Test Run Criteria are met.

### 1872 — Test Run Criteria for detection of faults caused by the ECU operating environment or customer action
- 版本：v1 ｜ 验证方式：Inspection ｜ 适用：通用
- Any fault detection test for detection of faults caused by the ECU operating environment or customer actions shall be inhibited when the fault is a secondary fault that appears as a result of another (primary) fault that is detected by another DTC test.

### 1873 — agedDTCLimit for inconsistent or incompatible vehicle configuration data
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Table "Calibration of configuration DTCs" - item 2.5 The DTC test for inconsistent or incompatible vehicle configuration data shall use Operation cycle counter #2 (OCC2) as the counter used for aging and shall have agedDTCLimit = 1 ( provided that the DTC is not emission related).

### 1874 — agedDTCLimit for invalid vehicle configuration data
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Table "Calibration of configuration DTCs" - item 2.3 The DTC test for invalid vehicle configuration data shall use Operation cycle counter #2(OCC2) as the counter used for aging and shall have agedDTCLimit = 1 ( provided that the DTC is not emission related).

### 1875 — agedDTCLimit for missing Car Configuration Logic (CCL)
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Table "Calibration of configuration DTCs" - item 4.2 The DTC test for missing Car Configuration Logic (CCL) shall use Operation cycle counter #2(OCC2) as the counter used for aging and shall have agedDTCLimit = 1 ( provided that the DTC is not emission related).

### 1876 — agedDTCLimit for missing vehicle configuration data
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- To define exact criteria for DTC aging Table "Calibration of configuration DTCs" - item 2.1 The DTC test for missing vehicle configuration data shall use Operation cycle counter #2(OCC2) as the counter used for aging and shall have agedDTCLimit = 1 ( provided that the DTC is not emission related).

### 1877 — agedDTCLimit for missing Vehicle Configuration Data (VCD)
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- To define exact criteria for DTC aging Table "Calibration of configuration DTCs" - item 5.1 The DTC test for missing Vehicle Configuration Data (VCD) shall use Operation cycle counter #2 (OCC2) as the counter used for aging and shall have agedDTCLimit = 1 ( provided that the DTC is not emission related).

### 1878 — agedDTCLimit for new configuration not learned
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Table "Calibration of configuration DTCs" - item 2.4 The DTC test for new configuration not learned shall use Operation cycle counter #2 (OCC2) as the counter used for aging and shall have agedDTCLimit = 1 ( provided that the DTC is not emission related).

### 1879 — agedDTCLimit for VCD and CCL data inconsistency
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- To define exact criteria for DTC aging Table "Calibration of configuration DTCs" - item 4.1 The DTC test for VCD and CCL data inconsistency shall use Operation cycle counter #2 (OCC2) as the counter used for aging and shall have agedDTCLimit = 1 ( provided that the DTC is not emission related).

### 1880 — Base DTC value for detection of software incompatibility with another ECU
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults caused by incompatible or missing software components" - item 8.1 The DTC test for detection of software incompatibility with another ECU shall use the base DTC value U03XX if defined in [Data_51] Diagnostic trouble code definitions, UDS - Data - External publications, otherwise base DTC value U2DXX shall be used to identify this fault.

### 1881 — Clearing of DTC for detection of supplier software installed in ECU.
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- The DTC for indicating that the ECU has supplier specific software installed shall not be possible to clear except by replacing the software.
- Table "Requirements on detection of faults caused by incompatible or missing software components" - item 8.2 The DTC U2400-57 shall always be set as long as the supplier specific software is installed in the ECU.
- It shall not be possible to delete (clear) this DTC except by erasing or replacing the supplier software.

### 1882 — ConfirmedDTCLimit for inconsistent or incompatible vehicle configuration...
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- To define exact criteria for setting confirmedDTC status Table "Calibration of configuration DTCs" - item 2.5 The DTC test for inconsistent or incompatible vehicle configuration data shall have confirmedDTCLimit = 1.

### 1883 — ConfirmedDTCLimit for invalid vehicle configuration data
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Table "Calibration of configuration DTCs" - item 2.3 The DTC test for invalid vehicle configuration data shall have confirmedDTCLimit = 1.

### 1884 — ConfirmedDTCLimit for missing Car Configuration Logic (CCL)
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Table "Calibration of configuration DTCs" - item 4.2 The DTC test for missing Car Configuration Logic (CCL) shall have confirmedDTCLimit = 1.

### 1885 — ConfirmedDTCLimit for missing vehicle configuration data
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- To define exact criteria for setting confirmedDTC status Table "Calibration of configuration DTCs" - item 2.1 The DTC test for missing vehicle configuration data shall have confirmedDTCLimit = 1.

### 1886 — ConfirmedDTCLimit for missing Vehicle Configuration Data (VCD)
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- To define exact criteria for setting confirmedDTC status Table "Calibration of configuration DTCs" - item 5.1 The DTC test for missing Vehicle Configuration Data (VCD) shall have confirmedDTCLimit = 1.

### 1887 — ConfirmedDTCLimit for new configuration not learned
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Table "Calibration of configuration DTCs" - item 2.4 The DTC test for new configuration not learned shall have confirmedDTCLimit = 1.

### 1888 — ConfirmedDTCLimit for VCD and CCL data inconsistency
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Table "Calibration of configuration DTCs" - item 4.1 The DTC test for VCD and CCL data inconsistency shall have confirmedDTCLimit = 1.

### 1889 — Detection of data integrity fault in configuration data memory
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- Central Car Configuration - SPA,UDS - Data - Requisite documents If the ECU is a Car Configuration Domain Master the ECU shall be able to detect data integrity faults in long-term memory used for storing VCD, CCL and VCP data.
- The test shall be based on the data integrity mechanism according to [Data_5] Central Car Configuration.

### 1890 — Detection of incompatible VIN
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- where the primary reason for the fault monitor is another than to support generation of DTC information) to detect if the locally stored VIN does not match the VIN transmitted from another ECU, this shall also be used as a DTC test.

### 1891 — Detection of inconsistent or incompatible vehicle configuration data
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- where the primary reason for the fault monitor is another than to support generation of DTC information) to detect if any loaded configuration parameter has a valid value but is internally inconsistent or incompatible with some other data or configuration in the ECU or an ECU hardware option, this test shall also be used as a DTC test.

### 1892 — Detection of invalid local configuration data
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults caused by local ECU Configuration (local parameters)" - item 1.1 If the ECU is required to be programmed with local configuration (or calibration) data for correct operation, the ECU shall be able to detect if it has one or more required local configuration parameters with unknown or invalid value.

### 1893 — Detection of invalid vehicle configuration data
- 版本：v4 ｜ 验证方式：Analysis ｜ 适用：通用
- Central Car Configuration - SPA,UDS - Data - Requisite documents If the ECU is a Car Configuration Subscriber the ECU shall be able to detect invalid vehicle configuration data, according to [Data_5] Central Car Configuration.

### 1894 — Detection of missing Car Configuration Logic (CCL)
- 版本：v5 ｜ 验证方式：Analysis ｜ 适用：通用
- Central Car Configuration - SPA,UDS - Data - Requisite documents If the ECU is a Car Configuration Domain Master the ECU shall be able to detect missing Car Configuration Logic data (CCL), according to [Data_5] Central Car Configuration.

### 1895 — Detection of missing vehicle configuration data (ECU never configured)
- 版本：v5 ｜ 验证方式：Analysis ｜ 适用：通用
- Central Car Configuration - SPAReq18, UDS - Data - Requisite documents If the ECU is a Car Configuration Subscriber and it is in 'Bulk state' it shall be able to detect missing vehicle configuration data, according to [Data_5] Central Car Configuration.

### 1896 — Detection of missing Vehicle Configuration Data (VCD)
- 版本：v5 ｜ 验证方式：Analysis ｜ 适用：通用
- Central Car Configuration - SPA, UDS - Data - Requisite documents If the ECU is a Car Configuration Domain Master the ECU shall be able to detect missing Vehicle Configuration Data (VCD), according to reference [Data_5] Central Car Configuration.

### 1897 — Detection of new configuration not learned
- 版本：v5 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults caused by Global ECU Configuration (global parameters)" - item 2.4 If the ECU requires an additional control routine to instruct the ECU to learn a changed configuration, the ECU shall be able to detect that a new valid configuration has been received but not learned, according to [Data_5] Central Car Configuration.

### 1898 — Detection of software incompatibility with another ECU
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- To ensure that it can be detected if an ECU has software loaded that is incompatible with another ECU. Table "Requirements on detection of faults caused by incompatible or missing software components" - item 8.1 If the ECU has a fault monitor implemented as pa

### 1899 — Detection of supplier specific software installed in ECU
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults caused by incompatible or missing software components" - item 8.2 If t he ECU is delivered to CEVT with supplier specific software that must be replaced by CEVT authorised application software as part of the manufacturing process this shall be identified by a confirmed DTC with the DTC value U2400-57.

### 1900 — Detection of VCD and CCL data inconsistency
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- Central Car Configuration - SPA, UDS - Data - Requisite documents If the ECU is a Car Configuration Domain Master the ECU shall be able to detect if incompatible VCD and CCL data are loaded, according to [Data_5] Central Car Configuration.

### 1901 — DTC value for detection of CCL part no inconsistency
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults caused by Global ECU Configuration (global parameters)" - item 4.1 Detection of CCL part no inconsistency shall use base DTC value U2302 to identify the fault.

### 1902 — DTC value for detection of data integrity fault in configuration data me...
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults caused by Global ECU Configuration (global parameters)" - item 3.1 Detection of data integrity faults in configuration data memory shall use base DTC value U2301 to identify the fault.

### 1903 — DTC value for detection of incompatible VIN
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults caused by incompatible or missing software components" - item 7.1 Detection of incompatible VIN shall use the base DTC values P0630, P0631, C0545 or C0546 to identify the fault.

### 1904 — DTC value for detection of inconsistent or incompatible vehicle configur...
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults caused by Global ECU Configuration (global parameters)" - item 2.5 The detection of inconsistent or incompatible configuration shall use base DTC value U2300 to identify the fault.

### 1905 — DTC value for detection of invalid local configuration data
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults caused by local ECU Configuration (local parameters)" - item 1.1 Detection of invalid local configuration data shall use base DTC value U2101 to identify the fault.

### 1906 — DTC value for detection of invalid vehicle configuration data
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults caused by Global ECU Configuration (global parameters)" - item 2.3 Detection of invalid configuration data shall use base DTC value U2300 to identify the fault.

### 1907 — DTC value for detection of missing Car Configuration Logic data
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults caused by Global ECUConfiguration (global parameters)" - item 4.2 Detection of missing Car Configuration Logic data shall use base DTC value U2302 to identify the fault.

### 1908 — DTC value for detection of missing vehicle configuration data
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults caused by Global ECUConfiguration (global parameters)" - item 2.1 Detection of missing vehicle configuration data shall use base DTC value U2300 to identify the fault.

### 1909 — DTC value for detection of missing Vehicle Configuration Data (VCD)
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults caused by Global ECUConfiguration (global parameters)" - item 5.1 Detection of missing vehicle configuration data (VCD) shall use base DTC value U2303 to identify the fault.

### 1910 — DTC value for detection of new configuration not learned
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults caused by Global ECUConfiguration (global parameters)" - item 2.4 Detection of new configuration not learned shall use base DTC value U2300 to identify the fault.

### 1911 — Failure type value for detection of CCL part no inconsistency
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults caused by Global ECU Configuration (global parameters)" - item 4.1 DTCs for detection of CCL part no inconsistency shall use Failure Type value 0x57.

### 1912 — Failure type value for detection of data integrity fault in configuratio...
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults caused by Global ECU Configuration (global parameters)" - item 3.1 DTCs for detection of data integrity faults in configuration data memory shall use Failure Type value 0x41.

### 1913 — Failure type value for detection of inconsistent or incompatible vehicle...
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults caused by Global ECU Configuration (global parameters)" - item 2.5 The DTCs for detection of inconsistent or incompatible configuration shall use Failure Type value 0x57.

### 1914 — Failure type value for detection of invalid local configuration data
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults caused by local ECU Configuration(local parameters)" - item 1.1 DTCs for detection of invalid local configuration data shall use Failure Type value 0x56.

### 1915 — Failure type value for detection of invalid vehicle configuration data
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults caused by Global ECUConfiguration (global parameters)" - item 2.3 The DTC for detection of invalid configuration data shall use Failure Type value 0x56.

### 1916 — Failure type value for detection of missing Car Configuration Logic data
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults caused by Global ECUConfiguration (global parameters)" - item 4.2 DTCs for detection of missing Car Configuration Logic data shall use Failure Type value 0x55.

### 1917 — Failure type value for detection of missing Vehicle Configur. Data (VCD)
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- DTCs for detection of missing vehicle configuration data (VCD) shall use Failure Type value0x55.

### 1918 — Failure type value for detection of missing vehicle configuration data
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults caused by Global ECU Configuration (global parameters)" - item 2.1 DTCs for detection of missing vehicle configuration data shall use Failure Type value 0x55.

### 1919 — Failure type value for detection of software incompatibility with another...
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults caused by incompatible or missing software components" - item 8.1 The DTCs for detection of software incompatibility with another ECU shall use Failure Type value: 0x4A if module must be replaced 0x57 If module must be reprogrammed 0x00 if cause is not known

### 1920 — Failure type value for new configuration not learned
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults caused by Global ECU Configuration (global parameters)" - item 2.4 The DTC for detection of new configuration not learned shall use Failure Type value 0x51.

### 1921 — FDC 10 max value for inconsistent or incompatible vehicle configuration ...
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- To define that the DTC test shall be able to set the Confirmed state.
- Table "Calibration of configuration DTCs" - item 2.5 The DTC test for inconsistent or incompatible vehicle configuration data shall have FDC 10 max value = 127.

### 1922 — FDC 10 max value for invalid vehicle configuration data
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- To define that the DTC test shall be able to set the Confirmed state.
- Table "Calibration of configuration DTCs" - item 2.3 The DTC test for invalid vehicle configuration data shall have FDC 10 max value = 127.

### 1923 — FDC 10 max value for missing Car Configuration Logic (CCL)
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- To define that the DTC test shall be able to set the Confirmed state.
- Table "Calibration of configuration DTCs" - item 4.2 The DTC test for missing Car Configuration Logic (CCL) shall have FDC 10 max value = 127.

### 1924 — FDC 10 max value for missing vehicle configuration data
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- To define that the DTC test shall be able to set the Confirmed state Table "Calibration of configuration DTCs" - item 2.1 The DTC test for missing vehicle configuration data shall have FDC 10 max value = 127.

### 1925 — FDC 10 max value for missing Vehicle Configuration Data (VCD)
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- To define that the DTC test shall be able to set the Confirmed state.
- Table "Calibration of configuration DTCs" - item 5.1 The DTC test for missing Vehicle Configuration Data (VCD) shall have FDC 10 max value = 127.

### 1926 — FDC 10 max value for new configuration not learned
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- To define that the DTC test shall be able to set the Confirmed state.
- Table "Calibration of configuration DTCs" - item 2.4 The DTC test for new configuration not learned shall have FDC 10 max value = 127.

### 1927 — FDC 10 max value for VCD and CCL data inconsistency
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- To define that the DTC test shall be able to set the Confirmed state.
- Table "Calibration of configuration DTCs" - item 4.1 The DTC test for VCD and CCL data inconsistency shall have FDC 10 max value = 127.

### 1928 — Test Run Criteria for detection of CCL part no inconsistency
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults caused by Global ECU Configuration (global parameters)" - item 4.1 The DTC test for detection of CCL part no inconsistency shall run whenever the VCP generation routine is executed according to [Data_5] Central Car Configuration.

### 1929 — Test Run Criteria for detection of data integrity fault in configuration...
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults caused by Global ECU Configuration (global parameters)" - item 3.1 The DTC test for detection of data integrity faults in configuration data memory shall run according to criteria specified by the implementer.

### 1930 — Test Run Criteria for detection of incompatible VIN
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults caused by incompatible or missing software components" - item 7.1 The DTC test for detection of incompatible VIN shall run at least once every operation cycle.

### 1931 — Test Run Criteria for detection of inconsistent or incompatible vehicle ...
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults caused by Global ECU Configuration (global parameters)" - item 2.5 The DTC test for detection of inconsistent or incompatible configuration shall run every time a global configuration parameter used for configuration of the ECU is received until test the test has passed.

### 1932 — Test Run Criteria for detection of invalid local configuration data
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- To enable a fault detection mechanism with maximum coverage while being robust and reliable Table "Requirements on detection of faults caused by local ECU Configuration (local parameters)" - item 1.1 If the detection of invalid local configuration data is implemented the DTC test shall run whenever a local configuration parameter is used or changed.

### 1933 — Test Run Criteria for detection of missing Car Configuration Logic data
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults caused by Global ECU Configuration (global parameters)" - item 4.2 The DTC test for detection of missing Car Configuration Logic data shall run each time new VCP data is generated according to [Data_5] Central Car Configuration.

### 1934 — Test Run Criteria for detection of missing vehicle configuration data
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- To enable a fault detection mechanism with maximum coverage while being robust and reliable Table "Requirements on detection of faults caused by Global ECU Configuration (global parameters)" - item 2.1 The DTC test for detection of missing vehicle configuration data shall be enabled while ECU is in 'Bilk state' and shall run each time a Car Configuration block is received.
- The test shall be inhibited once it has passed.

### 1935 — Test Run Criteria for detection of missing Vehicle Configuration Data (VCD)
- 版本：v4 ｜ 验证方式：Analysis ｜ 适用：通用
- To enable a fault detection mechanism with maximum coverage while being robust and reliable Table "Requirements on detection of faults caused by Global ECU Configuration (global parameters)" - item 5.1 The DTC test for detection of missing vehicle configuration data (VCD) shall run each time new VCP data is generated according to [Data_5] Central Car Configuration.

### 1936 — Test Run Criteria for invalid vehicle configuration data
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults caused by Global ECU Configuration (global parameters)" - item 2.3 The DTC test for detection of invalid configuration data shall run every time a global configuration parameter used for configuration of the ECU is received, until the test has passed.

### 1937 — Test Run Criteria for new configuration not learned
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults caused by Global ECU Configuration (global parameters)" - item 2.4 The DTC test for new configuration not learned shall run every time a global configuration parameter used for configuration of the ECU is received, until the test has passed.

### 1938 — Test sample failed criteria for inconsistent or incompatible vehicle con...
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Table "Calibration of configuration DTCs" - item 2.5 The DTC test for inconsistent or incompatible vehicle configuration data shall use the following criteria for test sample failed: O ne or more parameters used for configuration of the ECU has a valid value but is internally inconsistent or incompatible with some other data or configuration in the ECU or an ECU hardware option.
- The FDC10 shall be increased by 127 each test sample failed .

### 1939 — Test sample failed criteria for invalid vehicle configuration data
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Table "Calibration of configuration DTCs" - item 2.3 The DTC test for invalid vehicle configuration data shall use the following criteria for test sample failed: O ne or more parameters used for configuration of the ECU is received with an unrecognized or invalid value (incl.
- The FDC10 shall be increased by 127 each test sample failed .

### 1940 — Test sample failed criteria for missing Car Configuration Logic (CCL)
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Table "Calibration of configuration DTCs" - item 4.2 The DTC test for missing Car Configuration Logic (CCL) shall use the following criteria for test sample failed: No Car Configuration Logic (CCL) file is stored in the CCL memory.
- The FDC10 shall be increased by 127 each test sample failed .

### 1941 — Test sample failed criteria for missing vehicle configuration data
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- Table "Calibration of configuration DTCs" - item 2.1 The DTC test for missing vehicle configuration data shall use the following criteria for test sample failed: No valid configuration (i.
- The FDC10 shall be increased by 127 each test sample failed.

### 1942 — Test sample failed criteria for missing Vehicle Configuration Data (VCD)
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Table "Calibration of configuration DTCs" - item 5.1 The DTC test for missing Vehicle Configuration Data (VCD) shall use the following criteria for test sample failed: No Vehicle Configuration Data (VCD) file is stored in the VCD memory.
- The FDC10 shall be increased by 127 each test sample failed.

### 1943 — Test sample failed criteria for new configuration not learned
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Table "Calibration of configuration DTCs" - item 2.4 The DTC test for new configuration not learned shall use the following criteria for test sample failed: A changed configuration has been evaluated as valid and the ECU requires an additional control routine to instruct the ECU to learn a changed configuration.
- The FDC10 shall be increased by 127 each test sample failed.

### 1944 — Test sample failed criteria for VCD and CCL data inconsistency
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Table "Calibration of configuration DTCs" - item 2.1 The DTC test for VCD and CCL data inconsistency shall use the following criteria for test sample failed: The CC-Logic Part No specified in VCD (Information Data) and the CC-Logic Part No specified in CCL memory are not equal.
- The FDC10 shall be increased by 127 each test sample failed.

### 1945 — Test sample passed criteria for inconsistent or incompatible vehicle configuration data
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- Table "Calibration of configuration DTCs" - item 2.5 The DTC test for inconsistent or incompatible vehicle configuration data shall use the following criteria for test sample passed: All parameters used for configuration of the ECU have valid values and are internally consistent and compatible with all other data, configuration and hardware options in the ECU.
- The FDC10 shall be decreased by 128 each test sample passed.

### 1946 — Test sample passed criteria for invalid vehicle configuration data
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- Table "Calibration of configuration DTCs" - item 2.3 The DTC test for invalid vehicle configuration data shall use the following criteria for test sample passed: All parameter used for configuration of the ECU have been received with valid values.
- The FDC10 shall be decreased by 128 each test sample passed.

### 1947 — Test sample passed criteria for missing vehicle configuration data
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- Table "Calibration of configuration DTCs" - item 2.1 The DTC test for missing vehicle configuration data shall use the following criteria for test sample passed: A valid configuration (all required parameters have valid values) has been stored in VCP memory.
- The FDC10 shall be decreased by 128 each test sample passed.

### 1948 — Test sample passed criteria for missing Vehicle Configuration Data (VCD)
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- Table "Calibration of configuration DTCs" - item 5.1 The DTC test for missing Vehicle Configuration Data (VCD) shall use the following criteria for test sample passed: A Vehicle Configuration Data (VCD) file is stored in the VCD memory.
- The FDC10 shall be decreased by 128 each test sample passed.

### 1949 — Test sample passed criteria for new configuration not learned
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- Table "Calibration of configuration DTCs" - item 2.4 The DTC test for new configuration not learned shall use the following criteria for test sample passed: The routine required to instruct the ECU to learn a changed configuration has been successfully executed.
- The FDC10 shall be decreased by 128 each test sample passed.

### 1950 — Test sample passed criteria for No Car Configuration Logic (CCL) is present in CCL memory.
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- The FDC10 shall be decreased by 128 each test sample passed.
- Table "Calibration of configuration DTCs" - item 4.2 The DTC test No Car Configuration Logic (CCL) is present in CCL memory shall use the following criteria for test sample passed: The routine required to instruct the ECU to learn a changed configuration has been successfully executed.

### 1951 — Test sample passed criteria for VCD and CCL data inconsistency
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- Table 4-13, item 4.1 The DTC test for VCD and CCL data inconsistency shall use the following criteria for test sample passed: The CC-Logic Part No specified in VCD (Information Data) and the CC-Logic Part No specified in CCL memory are equal.
- The FDC10 shall be decreased by 128 each test sample passed.

### 1952 — UnconfirmedDTCLimit for inconsistent or incompatible vehicle configurati...
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- To define exact criteria for setting unconfirmedDTC status Table "Calibration of configuration DTCs" - item 2.5 The DTC test for inconsistent or incompatible vehicle configuration data shall have unconfirmedDTCLimit = 127.

### 1953 — UnconfirmedDTCLimit for invalid vehicle configuration data
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Table "Calibration of configuration DTCs" - item 2.3 DTC test for missing vehicle configuration data shall have unconfirmedDTCLimit = 127.

### 1954 — UnconfirmedDTCLimit for missing Car Configuration Logic (CCL)
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- To define exact criteria for setting UnconfirmedDTC status Table "Calibration of configuration DTCs" - item 4.2 The DTC test for missing Car Configuration Logic (CCL) shall have UnconfirmedDTCLimit = 127.

### 1955 — UnconfirmedDTCLimit for missing vehicle configuration data
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- To define exact criteria for setting unconfirmedDTC status Table "Calibration of configuration DTCs" - item 2.1 The DTC test for missing vehicle configuration data shall have unconfirmedDTCLimit = 127.

### 1956 — UnconfirmedDTCLimit for missing Vehicle Configuration Data (VCD)
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- To define exact criteria for setting unconfirmedDTC status Table 4.13: Table "Calibration of configuration DTCs" - item 5.1 The DTC test for missing Vehicle Configuration Data (VCD) shall have unconfirmedDTCLimit = 127.

### 1957 — UnconfirmedDTCLimit for new configuration not learned
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- To define exact criteria for setting unconfirmedDTC status Table "Calibration of configuration DTCs" - item 2.4 The DTC test for new configuration not learned shall have unconfirmedDTCLimit = 127.

### 1958 — UnconfirmedDTCLimit for VCD and CCL data inconsistency
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Table "Calibration of configuration DTCs" - item 4.1 The DTC test for VCD and CCL data inconsistency shall have unconfirmedDTCLimit = 127.4.5.2.1.2.15 Requirements from section Detection of faults caused by received signals

### 1959 — Base DTC value for detection of low supply voltage
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults in external electrical circuits connected to the ECU" - item 10.1 Detection of low supply voltage shall use base DTC value U3003 to identify the fault.

### 1960 — Base DTC value for faults in high side driver outputs
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults in external electrical circuits connected to the ECU" - items 6.1, 6.2 and 6.3 High side driver outputs circuits which has fault detection implemented shall have one unique base DTC value for each output circuit.

### 1961 — Base DTC value for low side driver outputs
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults in external electrical circuits connected to the ECU" - items 5.1, 5.2 and 5.3 Low side driver outputs circuits which has fault detection implemented shall have one unique base DTC value for each output circuit.

### 1962 — Base DTC value for short circuit and open circuit faults in FM, PCM, PWM...
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults in external electrical circuits connected to the ECU" - items 3.1, 3.2, 4.1 and 4.2 The ECU shall implement one unique base DTC value for each FM, PCM, PWM and similar input circuit for detection short circuit to ground faults, short circuit to battery and open circuit faults.

### 1963 — Base DTC value for short circuit to battery or open circuit faults in an...
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults in external electrical circuits connected to the ECU" - item 2.1 and 2.2 The ECU shall implement one unique base DTC value for each analog input circuit for detection short circuit to ground faults, short circuit to battery and open circuit faults.

### 1964 — Base DTC value for switch inputs
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults in external electrical circuits connected to the ECU" - item 1.1 and 1.2 The ECU shall implement one unique base DTC value for each switch input circuit for which fault detection is implemented.

### 1965 — Detection of CS- or CRC-error on private ECU network
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- where the primary reason for the fault monitor is another than to support generation of DTC information) this fault shall also be identified by an appropriate DTC.
- Otherwise, the ECU shall be able to detect this fault as defined by a feasibility study performed by the implementer.
- The feasibility study shall be approved by the responsible authority appointed by OEM).

### 1966 — Detection of data not updated by transmitter on private ECU network
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- where the primary reason for the fault monitor is another than to support generation of DTC information) this fault shall also be identified by an appropriate DTC.
- Otherwise, the ECU shall be able to detect this fault as defined by a feasibility study performed by the implementer.
- The feasibility study shall be approved by the responsible authority appointed by OEM).

### 1967 — Detection of faults for switch inputs
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- where the primary reason for the fault monitor is another than to support generation of DTC information) each such fault shall also be identified by an appropriate Failure Type value for a corresponding DTC.
- Otherwise, the ECU shall be able to detect faults in all switch input circuits connected to the ECU as defined by a feasibility study performed by the implementer.
- The feasibility study shall be approved by the responsible authority appointed by OEM).

### 1968 — Detection of incorrect timing and format on private ECU network
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- where the primary reason for the fault monitor is another than to support generation of DTC information) this fault shall also be identified by an appropriate DTC.
- Otherwise, the ECU shall be able to detect this fault as defined by a feasibility study performed by the implementer.
- The feasibility study shall be approved by the responsible authority appointed by OEM).

### 1969 — Detection of low supply voltage
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Low supply voltage is a root fault that may be the cause of many other fault symptoms.
- Table "Requirements on detection of faults in external electrical circuits connected to the ECU" - item 10.1 The ECU shall be able to detect if its supply voltage is lower than the vehicle battery voltage according to the requirements in section Requirements from section Requirements for detection of low supply voltage.

### 1970 — Detection of missed deadline for message on private ECU network
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- where the primary reason for the fault monitor is another than to support generation of DTC information) this fault shall also be identified by an appropriate DTC.
- Otherwise, the ECU shall be able to detect this fault as defined by a feasibility study performed by the implementer.
- The feasibility study shall be approved by the responsible authority appointed by OEM).

### 1971 — Detection of other external electrical circuit faults
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- where the primary reason for the fault monitor is another than to support generation of DTC information) each such fault shall also be identified by an appropriate Failure Type value for the corresponding DTC.
- Otherwise, the ECU shall be able to detect other faults in electrical circuits connected to the ECU as defined by a feasibility study performed by the implementer.
- The feasibility study shall be approved by the responsible authority appointed by OEM).

### 1972 — Detection of other faults for analog inputs
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- where the primary reason for the fault monitor is another than to support generation of DTC information) each such fault shall also be identified by an appropriate Failure Type value for the corresponding DTC.
- Otherwise, the ECU shall be able to detect other faults in all analog input circuits connected to the ECU as defined by a feasibility study performed by the implementer.
- The feasibility study shall be approved by the responsible authority appointed by OEM).

### 1973 — Detection of other faults for FM, PCM, PWM etc. inputs
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- where the primary reason for the fault monitor is another than to support generation of DTC information) each such fault shall also be identified by an appropriate Failure Type value for the corresponding DTC.
- Otherwise, the ECU shall be able to detect other (than short circuit and open circuit) faults in all FM, PCM, PWM and similar input circuits connected to the ECU as defined by a feasibility study performed by the implementer.
- The feasibility study shall be approved by the responsible authority appointed by OEM).

### 1974 — Detection of other faults for high side driver outputs
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- where the primary reason for the fault monitor is another than to support generation of DTC information) each such fault shall also be identified by an appropriate Failure Type value for the corresponding DTC.
- Otherwise, the ECU shall be able to detect other (than short circuit and open circuit) faults in all high side driver outputs circuits connected to the ECU as defined by a feasibility study performed by the implementer.
- The feasibility study shall be approved by the responsible authority appointed by OEM).

### 1975 — Detection of other faults for low side driver outputs
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- where the primary reason for the fault monitor is another than to support generation of DTC information) each such fault shall also be identified by an appropriate Failure Type value for the corresponding DTC.
- Otherwise, the ECU shall be able to detect other (than short circuit and open circuit) faults in all low side driver outputs circuits connected to the ECU as defined by a feasibility study performed by the implementer.
- The feasibility study shall be approved by the responsible authority appointed by OEM).

### 1976 — Detection of other faults on private ECU network
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- where the primary reason for the fault monitor is another than to support generation of DTC information) each such fault shall also be identified by an appropriate Failure Type value for the corresponding DTC.
- Otherwise, the ECU shall be able to detect other faults in the private ECU network as defined by a feasibility study performed by the implementer.
- The feasibility study shall be approved by the responsible authority appointed by OEM).

### 1977 — Detection of physical layer faults on private ECU network
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- where the primary reason for the fault monitor is another than to support generation of DTC information) this fault shall also be identified by an appropriate DTC.
- Otherwise, the ECU shall be able to detect this fault as defined by a feasibility study performed by the implementer.
- The feasibility study shall be approved by the responsible authority appointed by OEM).

### 1978 — Detection of short circuit and open circuit faults in analog inputs
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Table "Requirements on detection of faults in external electrical circuits connected to the ECU" - item 2.1 and 2.2 The ECU shall be able to detect short circuit to ground faults, and short circuit to battery or open circuit faults, for all analog input circuits connected to the ECU.

### 1979 — Detection of short circuit and open circuit faults in FM, PCM, PWM etc. ...
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Table "Requirements on detection of faults in external electrical circuits connected to the ECU" - items 3.1, 3.2, 4.1 and 4.2 The ECU shall be able to detect short circuit and open circuit faults in FM, PCM, PWM and similar input circuits connected to the ECU according to one of the following alternatives.

### 1980 — Detection of short circuit and open circuit faults in high side driver o...
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Table "Requirements on detection of faults in external electrical circuits connected to the ECU" - items 6.1 and 6.2 The ECU shall be able to detect short circuit to ground faults, and short circuit to battery or open circuit faults, for all high side driver outputs circuits connected to the ECU.

### 1981 — Detection of short circuit and open circuit faults in low side driver ou...
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Table "Requirements on detection of faults in external electrical circuits connected to the ECU" - items 5.1 and 5.2 The ECU shall be able to detect short circuit to battery faults and short circuit to ground or open circuit faults, for all low side driver outputs circuits connected to the ECU.

### 1982 — Detection of transmit error on private ECU network
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- where the primary reason for the fault monitor is another than to support generation of DTC information) this fault shall also be identified by an appropriate DTC.
- Otherwise, the ECU shall be able to detect this fault as defined by a feasibility study performed by the implementer.
- The feasibility study shall be approved by the responsible authority appointed by OEM).

### 1983 — Detection of unexpected transmissions on private ECU network
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- where the primary reason for the fault monitor is another than to support generation of DTC information) this fault shall also be identified by an appropriate DTC.
- Otherwise, the ECU shall be able to detect this fault as defined by a feasibility study performed by the implementer.
- The feasibility study shall be approved by the responsible authority appointed by OEM).

### 1984 — DTC value for other external electrical circuit faults
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults in external electrical circuits connected to the ECU" - item 11.1 There shall be one unique base DTC value for each output circuit which has a fault monitor for other faults, and for each fault detected on this circuit a unique Failure Type value shall be used

### 1985 — Failure type value for CS- or CRC-error on private ECU network
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Table "Requirements on detection of faults in external electrical circuits connected to the ECU" - item 9.3 DTCs for CS- or CRC-error on private ECU network shall have a Failure Type value 0x83.

### 1986 — Failure type value for detection of low supply voltage
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults in external electrical circuits connected to the ECU" - item 10.1 The DTC for detection of low supply voltage shall use Failure Type value 0x62.

### 1987 — Failure type value for incorrect timing and format on private ECU network
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Table "Requirements on detection of faults in external electrical circuits connected to the ECU" - item 9.4 DTCs for incorrect timing and format on private ECU network shall have a Failure Type value 0x86.

### 1988 — Failure type value for missed deadline for message on private ECU network
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Table "Requirements on detection of faults in external electrical circuits connected to the ECU" - item 9.6 DTCs for missed deadline for message on private ECU network shall have a Failure Type value 0x87.

### 1989 — Failure type value for physical layer faults on private ECU network
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Table "Requirements on detection of faults in external electrical circuits connected to the ECU" - item 9.7 DTCs for physical layer faults on private ECU network shall have a Failure Type value 0x01.

### 1990 — Failure type value for short circuit and open circuit faults in FM, PCM,...
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults in external electrical circuits connected to the ECU" - items 3.1, 3.2, 4.1 and 4.2 DTCs for faults in FM, PCM, PWM and similar input circuits shall use Failure Type value according to one of the following alternativesAlternative 1: Input circuits which have fault detection for short circuit to battery or open circuit faults implemented that can differentiate between the two faults shall use Failure Type value 0x12 and 0x13, as appropriate depending on the type of fault.
- If the fault detection can not differentiate between the two faults then Failure Type value 0x33 or 0x34, as appropriate depending on the type of fault, shall be used for both faults.
- DTCs for short circuit to ground faults shall use Failure Type value 0x11.

### 1991 — Failure type value for short circuit to battery faults in low side drive...
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults in external electrical circuits connected to the ECU" - item 5.1 DTCs for short circuit to battery faults for low side driver outputs circuits shall use Failure Type value 0x12.

### 1992 — Failure type value for short circuit to battery or open circuit faults i...
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults in external electrical circuits connected to the ECU" - item 2.1 DTCs for detection for short circuit to battery or open circuit faults in analog input circuits that can differentiate between the two faults shall use Failure Type value 0x12 and 0x13, as appropriate depending on the type of fault.
- If the fault detection can not differentiate between the two faults then Failure Type value 0x15 shall be used for both faults.

### 1993 — Failure type value for short circuit to battery or open circuit faults in high side driver outputs
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults in external electrical circuits connected to the ECU" - item 6.1 High side driver outputs circuits which have fault detection for short circuit to battery or open circuit faults implemented that can differentiate between the two faults shall use Failure Type value 0x12 and 0x13, as appropriate depending on the type of fault.
- If the fault detection can not differentiate between the two faults then Failure Type value 0x15 shall be used for both faults.

### 1994 — Failure type value for short circuit to ground faults in analog inputs
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults in external electrical circuits connected to the ECU" - item 2.2 DTCs for short circuit to ground faults for analog inputs shall use Failure Type value 0x11.

### 1995 — Failure type value for short circuit to ground faults in high side drive...
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults in external electrical circuits connected to the ECU" - item 6.2 DTCs for short circuit to ground faults for high side driver outputs circuits shall use Failure Type value 0x11.

### 1996 — Failure type value for short circuit to ground or open circuit faults in...
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults in external electrical circuits connected to the ECU" - item 5.2 Low side driver outputs circuits which have fault detection for short circuit to ground or open circuit faults implemented that can differentiate between the two faults shall use Failure Type value 0x11 and 0x13, as appropriate depending on the type of fault.
- If the fault detection can not differentiate between the two faults then Failure Type value 0x14 shall be used for both faults.

### 1997 — Failure type value for stuck at faults for switch inputs
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults in external electrical circuits connected to the ECU" - item 1.1 DTCs for 'stuck at' faults for switch inputs shall use Failure Type value 0x23 or 0x24, as appropriate depending on the type of fault.

### 1998 — Failure type value for transmit error on private ECU network
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Table "Requirements on detection of faults in external electrical circuits connected to the ECU" - item 9.1 DTCs for transmit error on private ECU network shall have a Failure Type value 0x86.

### 1999 — Failure type value for unexpected transmissions on private ECU network
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Table "Requirements on detection of faults in external electrical circuits connected to the ECU" - item 9.2 DTCs for unexpected transmissions on private ECU network shall have a Failure Type value 0x81.

### 2000 — Test period time for detection of other external electrical circuit faults
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults in external electrical circuits connected to the ECU" - item 11.1 The DTC tests for the detection of other external electrical circuit faults shall produce Test Samples periodically, while the Test Run Criteria are met, at a rate defined by the implementer and approved by the responsible authority appointed by OEM.
- If not defined by the implementer the test period time shall be 100 ms or faster.

### 2001 — Test period time for detection of other faults on private ECU network
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults in external electrical circuits connected to the ECU" - item 9.8 The DTC tests for the detection of faults in the private communication network shall produce Test Samples periodically, while the Test Run Criteria are met, at a rate defined by the implementer and approved by the responsible authority appointed by OEM.
- If not defined by the implementer the test period time shall be 100 ms or faster.

### 2002 — Test period time for detection of unexpected transmissions on private EC...
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults in external electrical circuits connected to the ECU" - item 9.2 The DTC tests for the detection of unexpected transmissions on private ECU network shall produce Test Samples periodically, while the Test Run Criteria are met, at a rate defined by the implementer and approved by the responsible authority appointed by OEM.
- If not defined by the implementer the test period time shall be 100 ms or faster.

### 2003 — Test period time for other faults for analog inputs
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults in external electrical circuits connected to the ECU" - item 2.3 The DTC tests for the detection of other (than short circuit and open circuit) faults for analog inputs shall produce Test Samples periodically, while the Test Run Criteria are met, at a rate defined by the implementer and approved by the responsible authority appointed by OEM.
- If not defined by the implementer the test period time shall be 100 ms or faster.

### 2004 — Test period time for other faults for FM, PCM, PWM etc. inputs
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults in external electrical circuits connected to the ECU" - item 3.3 and 4.3 The DTC tests for the detection of other (than short circuit and open circuit) faults for FM, PCM, PWM and similar input circuits shall produce Test Samples periodically, while the Test Run Criteria are met, at a rate defined by the implementer and approved by the responsible authority appointed by OEM.
- If not defined by the implementer the test period time shall be 100 ms or faster.

### 2005 — Test period time for other faults for high side driver outputs
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults in external electrical circuits connected to the ECU" - item 6.3 The DTC tests for the detection of other (than short circuit and open circuit) faults for high side driver outputs circuits shall produce Test Samples periodically, while the Test Run Criteria are met, at a rate defined by the implementer and approved by the responsible authority appointed by OEM.
- If not defined by the implementer the test period time shall be 100 ms or faster.

### 2006 — Test period time for other faults for low side driver outputs
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults in external electrical circuits connected to the ECU" - item 5.3 The DTC tests for the detection of other (than short circuit and open circuit) faults for low side driver outputs circuits shall produce Test Samples periodically, while the Test Run Criteria are met, at a rate defined by the implementer and approved by the responsible authority appointed by OEM.
- If not defined by the implementer the test period time shall be 100 ms or faster.

### 2007 — Test period time for other faults for switch inputs
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults in external electrical circuits connected to the ECU" - item 1.2 The DTC tests for the detection of other (than 'stuck at') faults for switch inputs shall produce Test Samples periodically, while the Test Run Criteria are met, at a rate defined by the implementer and approved by the responsible authority appointed by OEM.
- If not defined by the implementer the test period time shall be 100 ms or faster.

### 2008 — Test period time for physical layer faults on private ECU network
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults in external electrical circuits connected to the ECU" - item 9.7 The DTC tests for the detection of physical layer faults on private ECU network shall produce Test Samples periodically, while the Test Run Criteria are met, at a rate defined by the implementer and approved by the responsible authority appointed by OEM.
- If not defined by the implementer the test period time shall be 100 ms or faster.

### 2009 — Test period time for short circuit and open circuit faults in analog inputs
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults in external electrical circuits connected to the ECU" - item 2.1 and 2.2 The DTC test for the detection short circuit to ground faults, short circuit to battery and open circuit faults in analog inputs shall produce Test Samples periodically every 100 ms or faster while the Test Run Criteria are met.

### 2010 — Test period time for short circuit and open circuit faults in FM, PCM, P...
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults in external electrical circuits connected to the ECU" items 3.1, 3.2, 4.1 and 4.2 The DTC test for the detection short circuit to ground faults, short circuit to battery and open circuit faults in FM, PCM, PWM and similar input circuits shall produce Test Samples periodically every 100 ms or faster while the Test Run Criteria are met.

### 2011 — Test period time for short circuit and open circuit faults in high side ...
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults in external electrical circuits connected to the ECU" - items 6.1 and 6.2 The DTC test for the detection short circuit to battery faults, short circuit to ground and open circuit faults in high side driver outputs circuits shall produce Test Samples periodically every 100 ms or faster while the Test Run Criteria are met.

### 2012 — Test period time for short circuit and open circuit faults in low side d...
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults in external electrical circuits connected to the ECU" - items 5.1 and 5.2 The DTC test for the detection short circuit to ground faults, short circuit to battery and open circuit faults in low side driver outputs circuits shall produce Test Samples periodically every 100 ms or faster while the Test Run Criteria are met.

### 2013 — Test period time for stuck at faults for switch inputs
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults in external electrical circuits connected to the ECU" - item 1.1 The DTC test for the detection of 'stuck at' faults for switch inputs shall produce Test Samples periodically every 500 ms or faster while the Test Run Criteria are met.

### 2014 — Test Run Criteria for CS- or CRC-error on private ECU network
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults in external electrical circuits connected to the ECU" - item 9.3 The DTC test for CS- or CRC-error on private ECU network shall run each time a message is received on the network by the ECU.

### 2015 — Test Run Criteria for data not updated by transmitter on private ECU net...
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults in external electrical circuits connected to the ECU" - item 9.5 The DTC test for data not updated by transmitter on private ECU network shall run each time a message is received on the network by the ECU.

### 2016 — Test Run Criteria for detection of transmit error on private ECU network
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults in external electrical circuits connected to the ECU" - item 9.1 The DTC test for transmit error on private ECU network shall run each time a message is transmitted on the network by the ECU.

### 2017 — Test Run Criteria for fault detection in external circuits
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- Section "Detection of faults in external electrical circuits" Any fault detection test for external circuits using shall be inhibited when the fault is a secondary fault that appears as a result of another (primary) fault that is detected by another DTC test.

### 2018 — Test Run Criteria for incorrect timing and format on private ECU network
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults in external electrical circuits connected to the ECU" - item 9.4 The DTC test for incorrect timing and format on private ECU network shall run each time a message is received on the network by the ECU.

### 2019 — Test Run Criteria for missed deadline for message on private ECU network
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults in external electrical circuits connected to the ECU" - item 9.6 The DTC test for missed deadline for message on private ECU network shall run each time a message is expected to be received on the network by the ECU.

### 2020 — Test Run Criteria for short circuit to battery faults in low side driver...
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Table "Requirements on detection of faults in external electrical circuits connected to the ECU" - item 5.1 The DTC test for detection of short circuit to battery faults in a low side driver output shall run at least while the output is activated.

### 2021 — Test Run Criteria for short circuit to battery or open circuit faults in high side driver outputs
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Table 4-7, item 6.1 The DTC test for detection of short circuit to battery or open circuit faults in a high side driver output shall run at least while the output is deactivated.

### 2022 — Test Run Criteria for short circuit to ground faults in high side driver...
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Table "Requirements on detection of faults in external electrical circuits connected to the ECU" - item 6.2 The DTC test for detection of short circuit to ground faults in a high side driver output shall run at least while the output is activated.

### 2023 — Test Run Criteria for short circuit to ground or open circuit faults in ...
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Table "Requirements on detection of faults in external electrical circuits connected to the ECU" - item 5.2 The DTC test for detection of short circuit to ground or open circuit faults in a low side driver output shall run at least while the output is deactivated.

### 2024 — type value for data not updated by transmitter on private ECU network
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Table "Requirements on detection of faults in external electrical circuits connected to the ECU" - item 9.5 DTCs for data not updated by transmitter on private ECU network shall have a Failure Type value 0x82.4.5.2.1.2.11 Requirements from section Detection of low supply voltage

### 2025 — Base DTC value for detection of data integrity fault in non volatile memory
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults in internal electrical circuits" - item1.1 Detection of data integrity fault in non volatile memory shall use one unique base DTC value for all non volatile memory in the ECU.

### 2026 — Base DTC value for detection of data integrity fault in volatile memory
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults in internal electrical circuits" - item1.2 Detection of data integrity fault in volatile memory shall use one unique base DTC value for all volatile memory in the ECU.

### 2027 — Base DTC value for detection of faults in other internal parts
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults in internal electrical circuits" - item6.1 Detection of faults in other internal parts shall use one unique base DTC value for each internal part of the ECU that is monitored by a test (e.

### 2028 — Base DTC value for detection of internally connected actuator fault
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults in internal electrical circuits" - item4.1 Detection of internally connected actuator fault shall use one unique base DTC value for each actuator to identify the fault.

### 2029 — Base DTC value for detection of internally connected sensor fault
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults in internal electrical circuits" - item5.1 Detection of internally connected sensor fault shall use one unique base DTC value for each sensor to identify the fault.

### 2030 — Detection of data integrity fault in non volatile memory
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- where the primary reason for the fault monitor is another than to support generation of DTC information) each such fault shall also be identified by an appropriate DTC.
- Otherwise, the ECU shall be able to detect data integrity fault in non volatile memory as defined by a feasibility study performed by the implementer.
- The feasibility study shall be approved by the responsible authority appointed by OEM).

### 2031 — Detection of data integrity fault in volatile memory
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- where the primary reason for the fault monitor is another than to support generation of DTC information) each such fault shall also be identified by an appropriate DTC.
- Otherwise, the ECU shall be able to detect data integrity fault in volatile memory as defined by a feasibility study performed by the implementer.
- The feasibility study shall be approved by the responsible authority appointed by OEM).

### 2032 — Detection of faults in other internal parts
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- where the primary reason for the fault monitor is another than to support generation of DTC information) each such fault shall also be identified by an appropriate DTC.
- Otherwise, the ECU shall be able to detect faults in other internal parts as defined by a feasibility study performed by the implementer.
- The feasibility study shall be approved by the responsible authority appointed by OEM).

### 2033 — Detection of internal device communication error
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- where the primary reason for the fault monitor is another than to support generation of DTC information) each such fault shall also be identified by an appropriate DTC.
- Otherwise, the ECU shall be able to detect internal device communication errors as defined by a feasibility study performed by the implementer.
- The feasibility study shall be approved by the responsible authority appointed by OEM).

### 2034 — Detection of internal faults not on the main circuit board
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- Faults not on the main circuit board shall be treated as if they were external faults.
- Section "Detection of faults in internal electrical circuits" Where an ECU, or a non repairable (by the workshop) assembly unit containing the ECU, contains circuitry (actuators, sensors etc) internal to the ECU but not located on the main circuit board, the ECU shall be able to detect faults in these internal electrical circuits according to section Detection of faults in external electrical circuits as if they were external electrical circuits.

### 2035 — Detection of internally connected actuator fault
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- where the primary reason for the fault monitor is another than to support generation of DTC information) each such fault shall also be identified by an appropriate DTC.
- Otherwise, the ECU shall be able to detect internally connected actuator faults as defined by a feasibility study performed by the implementer.
- The feasibility study shall be approved by the responsible authority appointed by OEM).

### 2036 — Detection of internally connected sensor fault
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- where the primary reason for the fault monitor is another than to support generation of DTC information) each such fault shall also be identified by an appropriate DTC.
- Otherwise, the ECU shall be able to detect internally connected sensor faults as defined by a feasibility study performed by the implementer.
- The feasibility study shall be approved by the responsible authority appointed by OEM).

### 2037 — Detection of programme execution fault
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- where the primary reason for the fault monitor is another than to support generation of DTC information) each such fault shall also be identified by an appropriate DTC.
- Otherwise, the ECU shall be able to detect programme execution faults as defined by a feasibility study performed by the implementer.
- The feasibility study shall be approved by the responsible authority appointed by OEM).

### 2038 — DTC value for detection of internal device communication error
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults in internal electrical circuits" - item 2.1 Detection of internal device communication error shall use on unique base DTC value for each monitored device to identify the fault.

### 2039 — DTC value for detection of programme execution fault
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults in internal electrical circuits" - item 3.1 Detection of programme execution fault shall use one unique base DTC value for each execution unit in the ECU to identify the fault.

### 2040 — Failure type value for detection of data integrity fault in non volatile...
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults in internal electrical circuits" - item 1.1 DTCs for detection of data integrity fault in non volatile memory shall use Failure Type value 0x45 or 0x46.

### 2041 — Failure type value for detection of data integrity fault in volatile memory
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults in internal electrical circuits" - item 1.2 DTCs for detection of data integrity faults in volatile memory shall use Failure Type value 0x44.

### 2042 — Failure type value for detection of faults in other internal parts
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults in internal electrical circuits" - item 6.1 DTCs for detection of faults in other internal parts shall use a unique Failure Type value for each fault type as defined in [Data_51] Diagnostic trouble code definitions , UDS - Data - External publications .

### 2043 — Failure type value for detection of internal device communication error
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults in internal electrical circuits" - item 2.1 DTCs for detection of internal device communication error shall use Failure Type value 0x49.

### 2044 — Failure type value for detection of internally connected actuator fault
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults in internal electrical circuits" - item 5.1 DTCs for detection of internally connected actuator fault shall use a unique Failure Type value for each fault type as defined in [Data_51] Diagnostic trouble code definitions, UDS - Data - External publications.

### 2045 — Failure type value for detection of internally connected sensor fault
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults in internal electrical circuits" - item 5.1 DTCs for detection of internally connected sensor fault shall use a unique Failure Type value for each fault type as defined in [Data_51] Diagnostic trouble code definitions, UDS - Data - External publications.

### 2046 — Failure type value for detection of programme execution fault
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults in internal electrical circuits" - item 3.1 DTCs for detection of programme execution fault shall use Failure Type value 0x47.

### 2047 — Test period time for detection of faults in other internal parts
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults in internal electrical circuits" - item 6.1 The DTC tests for the detection of faults in other internal parts shall produce Test Samples periodically, while the Test Run Criteria are met, at a rate defined by the implementer and approved by the responsible authority appointed by OEM.
- If not defined by the implementer the test period time shall be 100 ms or faster.

### 2048 — Test period time for detection of internally connected actuator fault
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults in internal electrical circuits" - item 4.1 The DTC tests for the detection of internally connected actuator fault shall produce Test Samples periodically, while the Test Run Criteria are met, at a rate defined by the implementer and approved by the responsible authority appointed by OEM.
- If not defined by the implementer the test period time shall be 100 ms or faster.

### 2049 — Test period time for detection of internally connected sensor fault
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults in internal electrical circuits" - item 5.1 The DTC tests for the detection of internally connected sensor fault shall produce Test Samples periodically, while the Test Run Criteria are met, at a rate defined by the implementer and approved by the responsible authority appointed by OEM.
- If not defined by the implementer the test period time shall be 100 ms or faster.

### 2050 — Test Run Criteria and Test Period time for detection of data integrity f...
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults in internal electrical circuits" - item 1.2 The test run criteria and test period time for detection of data integrity fault in volatile memory shall be defined by the implementer.

### 2051 — Test Run Criteria and Test Period time for detection of data integrity f...
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults in internal electrical circuits" - item 1.1 The test run criteria and test period time for detection of data integrity fault in non volatile memory shall be defined by the implementer.

### 2052 — Test Run Criteria and Test period time for detection of programme execution fault
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- The test run criteria and test period time for detection of programme execution fault are specific for each implementation and must be defined by the implementer.
- Table "Requirements on detection of faults in internal electrical circuits" - item 3.1 The test run criteria and test period time for detection of programme execution fault shall be defined by the implementer.

### 2053 — Test Run Criteria for detection of internal device communication error
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults in internal electrical circuits" - item 2.1 If the detection of internal device communication error is implemented the DTC test shall run at each communication with the internal device.

### 2054 — Test Run Criteria for fault detection in internal circuitsk
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- Section "Detection of faults in internal electrical circuits" Any fault detection test for internal circuits shall be inhibited when the fault is a secondary fault that appears as a result of another (primary) fault that is detected by another DTC test.4.5.2.1.2.13 Requirements from section Detection of faults inferred from system behavior

### 2055 — Base DTC value for comparison of system behaviour with predictive model
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults inferred from system behaviour" - item 2.1 Comparison of system behaviour with predictive model shall use a unique base DTC value for each component, system or part of system that is monitored, to identify the fault.

### 2056 — Base DTC value for detection of closed loop control system out of control
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults inferred from system behaviour" - item 3.1 Detection of closed loop control system out of control shall use a unique base DTC value for each component, system or part of system that is monitored, to identify the fault.

### 2057 — Base DTC value for detection of failure to react after event
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults inferred from system behaviour" - item 1.1 Detection of failure to react after event shall use a unique base DTC value for each component, system or part of system that is monitored, to identify the fault.

### 2058 — Base DTC value for detection of other faults inferred from system behaviour
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults inferred from system behaviour" - item 5.1 Detection of other faults faults inferred from system behaviour shall use one unique base DTC value for each component, system or part of system that is monitored, to identify the fault.

### 2059 — Base DTC value for detection of system adaptation out of range
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults inferred from system behaviour" - item 4.1 Detection of system adaptation out of range shall use a unique base DTC value for each component, system or part of system that is monitored, to identify the fault.

### 2060 — Comparison of system behaviour with predictive model
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- Where no direct fault detection mechanism is available, or where it is inadequate, the ECU shall be able to indirectly detect faults in the system and components associated with the ECU.
- where the primary reason for the fault monitor is another than to support generation of DTC information) each such fault shall also be identified by an appropriate DTC.
- Otherwise, the ECU shall be able to detect if the measured behaviour of a component or system do not follow the predictions of a simulation of expected behaviour which is being run by the ECU, as defined by a feasibility study performed by the implementer.

### 2061 — Detection of closed loop control system out of control
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- Where no direct fault detection mechanism is available, or where it is inadequate, the ECU shall be able to indirectly detect faults in the system and components associated with the ECU.
- where the primary reason for the fault monitor is another than to support generation of DTC information) each such fault shall also be identified by an appropriate DTC.
- Otherwise, the ECU shall be able to detect if a closed loop control is not stable under conditions where stability would be expected, as defined by a feasibility study performed by the implementer.

### 2062 — Detection of failure to react after event
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- Where no direct fault detection mechanism is available, or where it is inadequate, the ECU shall be able to indirectly detect faults in the system and components associated with the ECU.
- where the primary reason for the fault monitor is another than to support generation of DTC information) each such fault shall also be identified by an appropriate DTC.
- Otherwise, the ECU shall be able to detect if sensor readings do not change as a result of some change actuated by the ECU, as defined by a feasibility study performed by the implementer.

### 2063 — Detection of other faults inferred from system behaviour
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- where the primary reason for the fault monitor is another than to support generation of DTC information) each such fault shall also be identified by an appropriate DTC.
- Otherwise, the ECU shall be able to detect faults inferred from system behaviour as defined by a feasibility study performed by the implementer.
- The feasibility study shall be approved by the responsible authority appointed by OEM).

### 2064 — Detection of system adaptation out of range
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- Where no direct fault detection mechanism is available, or where it is inadequate, the ECU shall be able to indirectly detect faults in the system and components associated with the ECU.
- where the primary reason for the fault monitor is another than to support generation of DTC information) each such fault shall also be identified by an appropriate DTC.
- Otherwise, the ECU shall be able to detect if a system where the ECU adapts to manufacturing tolerance, component ageing etc., has exceeded the limit of its adaptation range , as defined by a feasibility study performed by the implementer.

### 2065 — Failure type value for comparison of system behaviour with predictive model
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults inferred from system behaviour" - item 2.1 DTCs for comparison of system behaviour with predictive model shall use Failure Type value 0x61.

### 2066 — Failure type value for detection of closed loop control system out of co...
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults inferred from system behaviour" - item 3.1 DTCs for detection of closed loop control system out of control shall use Failure Type value 0x06.

### 2067 — Failure type value for detection of failure to react after event
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults inferred from system behaviour" - item 1.1 DTCs for detection of failure to react after event shall use Failure Type value 0x67.

### 2068 — Failure type value for detection of other faults inferred from system be...
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults inferred from system behaviour" - item 5.1 DTCs for detection of other faults faults inferred from system behaviour shall use a unique Failure Type value for each fault type as defined in [Data_51] Diagnostic trouble code definitions, UDS - Data - External publications.

### 2069 — Failure type value for detection of system adaptation out of range
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults inferred from system behaviour" - item 4.1 DTCs for detection of system adaptation out of range shall use Failure Type value 0x91.

### 2070 — Test period time for comparison of system behaviour with predictive model
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults inferred from system behaviour" - item 2.1 If comparison of system behaviour with predictive model is implemented the DTC test shall run periodically every 100 ms or faster whenever the Test Run Criteria are met.

### 2071 — Test period time for detection of closed loop control system out of control
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults inferred from system behaviour" - item 3.1 If the detection of closed loop control system out of control is implemented the DTC test shall run periodically every 100 ms or faster whenever the Test Run Criteria are met.

### 2072 — Test period time for detection of failure to react after event
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults inferred from system behaviour" - item 1.1 If the detection of failure to react after event is implemented the DTC test shall run periodically every 100 ms or faster whenever the Test Run Criteria are met.

### 2073 — Test period time for detection of other faults inferred from system beha...
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on detection of faults inferred from system behaviour" - item The DTC tests specified by the implementer for the detection of other faults inferred from system behaviour shall produce Test Samples periodically, while the Test Run Criteria are met, at a rate defined by the implementer and approved by the responsible authority appointed by OEM.
- If not defined by the implementer the test period time shall be 100 ms or faster.

### 2074 — Test Run Criteria for comparison of system behaviour with predictive model
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Table "Requirements on detection of faults inferred from system behaviour" - item 2.1 If comparison of system behaviour with predictive model is implemented the DTC test shall run whenever the function being simulated in the predictive model is active.

### 2075 — Test Run Criteria for detection of closed loop control system out of con...
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Table "Requirements on detection of faults inferred from system behaviour" - item 3.1 If the detection of closed loop control system out of control is implemented the DTC test shall run whenever stable closed loop control is actively expected.

### 2076 — Test Run Criteria for detection of failure to react after event
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Table "Requirements on detection of faults inferred from system behaviour" - item 1.1 If the detection of failure to react after event is implemented the DTC test shall run whenever changes from event are actively expected.

### 2077 — Test Run Criteria for detection of faults inferred from system behaviour
- 版本：v1 ｜ 验证方式：Inspection ｜ 适用：通用
- Any fault detection test for detection of faults inferred from system behaviour shall be inhibited when the fault is a secondary fault that appears as a result of another (primary) fault that is detected by another DTC test.

### 2078 — Test Run Criteria for detection of system adaptation out of range
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Table "Requirements on detection of faults inferred from system behaviour" - item 4.1 If the detection of system adaptation out of range is implemented the DTC test shall run whenever any adaptation value is updated.

### 2079 — Accuracy of vehicle battery voltage measurement
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- The vehicle battery voltage must be measured with a known minimum accuracy.
- Section "Requirements for detection of low supply voltage" The vehicle battery voltage shall be measured with a minimum accuracy of ±0.25 V .

### 2080 — AgedDTCLimit or low supply voltage fault detection
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Section "Requirements for detection of low supply voltage" The DTC shall have agedDTCLimit = 255.

### 2081 — Averaging of ECU supply voltage measurement
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- To be able to use the measured ECU supply voltage the measured value must be filtered through an averaging function.
- Section "Requirements for detection of low supply voltage" A new Uecu value shall be calculated every time a sample is taken.
- It shall be calculated as the average value of the samples taken during the last 500 ms period.

### 2082 — Averaging of vehicle battery voltage measurement
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- To be able to use the measured vehicle battery voltage the measured value must be filtered through an averaging function.
- Section "Requirements for detection of low supply voltage" A new Ubat value shall be calculated every time a sample is taken.
- It shall be calculated as the average value of the samples taken during the last 500 ms period.

### 2083 — ConfirmedDTCLimit for low supply voltage fault detection
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- To define exact criteria for setting the confirmedDTC status Section "Requirements for detection of low supply voltage" The DTC test for low supply voltage shall have confirmedDTCLimit = 10.

### 2084 — Distribution of the vehicle battery voltage value
- 版本：v4 ｜ 验证方式：Analysis ｜ 适用：通用
- To be able to use the calculated vehicle battery voltage value in for comparison with the supply voltage in all other ECUs the calculated value must be distributed on the in-vehicle networks.
- Section "Requirements for detection of low supply voltage" The calculated Ubat values shall be sent periodically and received by all Public ECUs with a maximum end-to-end time (including sensing, signaling and actuating time) of 100 ms.

### 2085 — ECU supply voltage measurement
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- The ECU supply voltage must be measured with a known minimum accuracy.
- Section "Requirements for detection of low supply voltage" The ECU shall measure its supply voltage with a minimum accuracy of ±0.25 V .

### 2086 — Sample time for ECU supply voltage measurement
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- The ECU supply voltage must be measured with a known minimum sample time.
- Section "Requirements for detection of low supply voltage" The ECU supply voltage shall be sampled every 50 ms or faster.

### 2087 — Sample time for vehicle battery voltage measurement
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- The vehicle battery voltage must be measured with a known minimum sample time.
- Section "Requirements for detection of low supply voltage" The vehicle battery voltage Ubat shall be sampled every 50 ms or faster.

### 2088 — Test Run Criteria for low supply voltage fault detection
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Section "Requirements for detection of low supply voltage" Low supply voltage fault detection shall only be done when all of following conditions are fulfilled: $U_{bat} \geq 12 V$ ANDUsageMode == Driving

### 2089 — Test sample failed criteria for low supply voltage fault detection
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Section "Requirements for detection of low supply voltage" For each new $U_{ecu}$ value being calculated the ECU shall compare the $U_{ecu}$ value with the received $U_{bat}$ value:- if $U_{ecu}

### 2090 — Test sample passed criteria for low supply voltage fault detection
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Section "Requirements for detection of low supply voltage" For each new $U_{ecu}$ value being calculated the ECU shall compare the $U_{ecu}$ value with the received $U_{bat}$ value:- if $U_{ecu} >= (U_{bat} - 3V)$ then the DTC fault detection counter (FDC10) shall be decremented by 6

### 2091 — UnconfirmedDTCLimit for low supply voltage fault detection
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- To define exact criteria for setting the UnconfirmedDTC status Section "Requirements for detection of low supply voltage" The DTC test for low supply voltage shall have unconfirmedDTCLimit = 6.

### 2092 — Vehicle battery voltage measurement
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Section "Requirements for detection of low supply voltage" The vehicle battery voltage shall be measured, by a dedicated ECU, as close to the actual battery terminals as possible (such that the measurement is unaffected by any internal energy storage in the measuring ECU).4.5.2.1.2.12 Requirements from section Detection of faults in internal electrical circuits

### 2093 — Compliance to ISO14229-1
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- Section "Diagnostic Data" All diagnostic data supported by the ECU shall be compliant to [Data_50] Road vehicles – Diagnostics systems – Diagnostic services , UDS - Data - External publications .

### 2094 — Compliance to ISO26021-1
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Diagnostics on safety systems must comply with regulations defined by relevant ISO specifications.
- The diagnostic data supported by the ECU in the safetySystemDiagnosticSession shall be defined as specified by reference [Data_53] Road vehicles - End-of-life activation of on-board pyrotechnic devices — Part 1: General information and use case definitions , UDS - Data - External publications and [Data_54] Road vehicles - End-of-life activation of on-board pyrotechnic devices - Part 2: Communication requirements , UDS - Data - External publications.

### 2095 — Compliance to ISO26262
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Implementation of diagnostics on safety related ECUs must comply with ISO 26262.
- For all ECUs implementing safety requirements with an ASIL higher than QM, it shall be ensured that the diagnostic functions required in this specification cannot violate any of those safety requirements, i.

### 2096 — Diagnostic data for private ECUs
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- Specify that also private ECUs shall support diagnostic data Section 4 - DIAGNOSTIC DATA REQUIREMENTS Private ECUs shall, from a diagnostic point of view, be regarded as if they were internally connected units (e.
- The public ECU master shall, on behalf of the private ECUs, support all the diagnostic data required by this document and that are applicable for the private ECUs.

### 2097 — Support for Fault Detection Counter #10
- 版本：v6 ｜ 验证方式：Test ｜ 适用：通用
- To provide enhanced information about the occurrence of a fault, that may be useful in the analysis of the fault, and enables detailed calibration of the corresponding DTC.
- Table "Requirements for the implementation DTC fault detection counters" For all DTCs supported by the ECU a counter identified by DTCExtendedDataRecordNumber=10 shall be implemented as defined in [Data_50] Road vehicles – Diagnostics systems – Diagnostic services ( service 19 sub-function 14 and Appendix D.5), UDS - Data - External publications and according to the following additional definitions:1.
- At the start of a new operation cycle the count value shall be 0.2.

### 2098 — Support for Fault Detection Counter #11
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- To provide enhanced information about the occurrence of a fault, that may be useful in the analysis of the fault.
- Table "Requirements for the implementation DTC fault detection counters" For all DTCs supported by the ECU a counter identified by DTCExtendedDataRecordNumber=11 may be implemented and if it is implemented then shall be according to the following definition: The count value shall be equal to the maximum value the FDC10 has reached during current operation cycle.
- The stored counter shall be reported as a 1 byte signed numeric value on request of the diagnostic services specified in reference [Data_1] UDS Services.

### 2099 — Support for Fault Detection Counter #12
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- To provide enhanced information about the occurrence of a fault, that may be useful in the analysis of the fault.
- Table "Requirements for the implementation DTC fault detection counters" For all DTCs supported by the ECU a counter identified byDTCExtendedDataRecordNumber=12 shall be implemented according to the following definition: The count value shall be equal to the maximum value, which is equal to or greater than unconfirmedDTCLimit, the FDC10 has reached since the last time DTC information was cleared.
- The stored counter shall be reported as a 1 byte signed numeric value on request of the diagnostic services specified in reference [Data_1] UDS Services.4.5.2.1.2.25 Requirements from section DTC time stamp

### 2100 — DTC Failure Type Byte
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- A unified failure type description shall be used by all DTCs since it will be displayed by the tools.
- Table "Requirements on implementation of DTCs" DTCs supported by an ECU shall use Failure Type Byte as defined in [Data_51] Diagnostic trouble code definitions , UDS - Data - External publications.

### 2101 — DTCs defined by GMRDB
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- All DTC information shall be supported by OEM specific tools and must therefore be defined in GMRDB.
- Table "Requirements on implementation of DTCs" DTCs supported by an ECU shall be implemented as defined in [Data_4] Global MasterReference Database.

### 2102 — DTCs for faults caused by the ECU operating environment or by customer
- 版本：v1 ｜ 验证方式：Inspection ｜ 适用：通用
- DTCs identifying faults caused by the ECU operating environment or by customer actions shall be defined in a separate range in order for the tools to be able to mask them out if required.
- DTCs that identifies faults caused by the ECU operating environment or by customer actions shall be defined in the base DTC range U2E00 to U2EFF and according to section Detection of faults caused by the ECU operating environment or customer actions .

### 2103 — DTCs for secondary faults caused by data from other ECU indicated as invalid
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- not root cause9 shall be defined in a separate range in order for the tools to be able to mask them out if required.
- Table "Requirements on implementation of DTCs" - item 2.3 DTCs that identifies faults caused by signal or data value received from another ECU where the signal/data is indicated as invalid by the transmitting ECU, shall be defined in the base DTC range U2C00 to U2CFF and according to section Detection of faults caused by signals and data values received from other ECUs .

### 2104 — DTCs for secondary faults caused by data from other ECU not indicated as invalid
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- not root cause9 shall be defined in a separate range in order for the tools to be able to mask them out if required.
- Table "Requirements on implementation of DTCs" - item 2.4 DTCs that identifies faults caused by signal or data value received from another ECU where the signal/data is not indicated as invalid by the transmitting ECU, shall be defined in the base DTC range U2D00 to U2DFF according to section Detection of faults caused by signals and data values received from other ECUs.

### 2105 — DTCs that are needed only during the development of the ECU
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- DTCs that are needed only during the development of the ECU shall be defined in a separate range in order for the tools to be able to mask them out if required.
- Table "Requirements on implementation of DTCs" - item 2.7 DTCs that are needed only during the development or quality tracking of the ECU shall be defined in the base DTC range U2BFF.
- The requirements on detection of the faults that shall be identified by DTCs in this range are specified in the following sections.

### 2106 — DTCs that are needed only during the development of the ECU - implementerspecified
- 版本：v5 ｜ 验证方式：Inspection ｜ 适用：通用
- DTCs that are needed only during the development of the ECU shall be defined in a separate range in order for the tools to be able to mask them out if required.
- Table "Requirements on implementation of DTCs" - item 2.6 DTCs specified by the implementer that are needed only during the development or quality tracking of the ECU shall be defined in the base DTC range U2F00 to U2FFF.
- The requirements on detection of the faults that shall be identified by DTCs in this range are specified in section Requirements on detection of faults caused by signal/data content received from other ECUs.

### 2107 — ECU operation cycle
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- Reference to requirements on an operation cycle that shall be supported by the ECU.

### 2108 — Emissions related DTCs defined by SAEJ2012
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on implementation of DTCs" - item 1.1 For all emissions related ECUs, DTCs with base DTC value in any of the ranges P0000 to P0FFF, P2000 to P2FFF or P3400 to P3FFF shall be implemented as defined in [Data_51] Diagnostic trouble code definitions , UDS - Data - External publications.

### 2109 — Non emissions related DTCs defined by SAEJ2012
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- Standardized DTCs defined in SAEJ2012 shall be used.
- Table "Requirements on implementation of DTCs" - item 2.1 DTCs with base DTC value in any of the ranges B0000 to B0FFF, B3000 to B3FFF, C0000 to C0FFF, C3000 to C3FFF, U0000 to U0FFF or U3000 to U3FFF shall be implemented as defined in [Data_51] Diagnostic trouble code definitions , UDS - Data - External publications and in the sections Detection of faults in external electrical circuits to Detection of faults due to configuration errors and software incompatibility and DTCs associated with driver indications .

### 2110 — Reporting of DTC information
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- It must be possible to extract DTC information from the ECU by standardized services.
- Table "Requirements on implementation of DTCs" DTCs supported by an ECU shall be reported on request of the diagnostic services specified in [Data_1] UDS Services, and be reported not more than once in any response.4.5.2.1.2.8 Requirements from section Calibration of DTCs

### 2111 — Support for Operation Cycle Counter #1
- 版本：v4 ｜ 验证方式：Test ｜ 适用：4.0.x 与 4.1+ 分别定义
- To provide enhanced information about the occurrence of a DTC that may be useful in the analysis of the fault.
- Table "Requirements on implementation of DTC operation cycle counters" For all DTCs supported by the ECU a counter identified by DTCExtendedDataRecordNumber=1 shall be implemented according to the following: When implementing with AUTOSAR 4.0.
- All operation cycles, including those during which the test was not passed shall be included.

### 2112 — Support for Operation Cycle Counter #2
- 版本：v5 ｜ 验证方式：Test ｜ 适用：4.0.x 与 4.1+ 分别定义
- To provide enhanced information about the occurrence of a DTC that may be useful in the analysis of the fault.
- Table "Requirements on implementation of DTC operation cycle counters" For all DTCs supported by the ECU a counter identified by DTCExtendedDataRecordNumber=2 shall be implemented according to the following: When implementing with AUTOSAR 4.0.
- The operation cycles during which the test was not passed shall be excluded.

### 2113 — Support for Operation Cycle Counter #3
- 版本：v5 ｜ 验证方式：Test ｜ 适用：4.0.x 与 4.1+ 分别定义
- To provide enhanced information about the occurrence of a DTC that may be useful in the analysis of the fault.
- Table "Requirements on implementation of DTC operation cycle counters" For all DTCs supported by the ECU a counter identified by DTCExtendedDataRecordNumber=3 shall be implemented according to the following: When implementing with AUTOSAR 4.0.
- All operation cycles, including those in which the test has not been passed or the DTC fault detection counter 10 has not reached a value that is equal to or greater than its unconfirmedDTCLimit shall be included.

### 2114 — Support for Operation Cycle Counter #4
- 版本：v4 ｜ 验证方式：Test ｜ 适用：4.0.x 与 4.1+ 分别定义
- To provide enhanced information about the occurrence of a DTC that may be useful in the analysis of the fault.
- Table "Requirements on implementation of DTC operation cycle counters" For all DTCs supported by the ECU a counter identified by DTCExtendedDataRecordNumber=4 shall be implemented according to the following: When implementing with AUTOSAR 4.0.
- Increment/clear criteria: In each operation cycle the counter shall be incremented as soon as FDC10 has reached a value that is equal to or greater than its unconfirmedDTCLimit for the first time.

### 2115 — Support for Operation Cycle Counter #5
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- To provide enhanced information about the occurrence of a DTC that may be useful in the analysis of the fault.
- Table "Requirements on implementation of DTC operation cycle counters" For all emission related DTCs supported by the ECU a counter identified by DTCExtendedDataRecordNumber=5 shall be implemented according to the following: Definition: Number of warm-up cycles since the DTC commanded the MIL to switch off (since DTC information was last cleared).
- Increment/clear criteria: The counter shall be incremented when warm-up cycle changes from false to true.

### 2116 — Support for Operation Cycle Counter #6
- 版本：v7 ｜ 验证方式：Test ｜ 适用：通用
- To provide enhanced information about the occurrence of a DTC that may be useful in the analysis of the fault.
- Table "Requirements on implementation of DTC operation cycle counters" For all DTCs supported by the ECU a counter identified by DTCExtendedDataRecordNumber=6 shall be implemented according to the following: Definition: The number of consecutive operation cycles (including the current operation cycle) during which the DTC fault detection counter 10 reached the value of +127 (since DTC information was last cleared).
- The operation cycles during which the test was not completed shall be excluded.

### 2117 — Support for Operation Cycle Counter #7
- 版本：v6 ｜ 验证方式：Test ｜ 适用：4.0.x 与 4.1+ 分别定义
- To provide enhanced information about the occurrence of a DTC that may be useful in the analysis of the fault.
- For all DTCs supported by the ECU a counter identified by DTCExtendedDataRecordNumber=7 shall be implemented according to the following: When implementing with AUTOSAR 4.0.
- The operation cycles during which the test was not passed or the DTC fault detection counter 10 did not reach a value that is equal to or greater than its unconfirmedDTCLimit shall be excluded.

### 2118 — Data records not included in local snapshot data
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Section "DTC snapshot data identification" Data records defined either as SystemSupplierSpecific or dynamically defined (as defined according to the table Requirements on implementation of data records) shall not be included in local DTC snapshot data.

### 2119 — Order of multiple samples of data records in global and local snapshot data records
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- To ensure consistent storage of data records in local DTC snapshot data records If data is sampled multiple times (record type = 'Multiple samples') before the sampling criteria is satisfied, then the sampled values shall be repeated a defined number of times in the snapshot data record.
- The order of the DTC snapshot data in the DTC snapshot record shall be such that the data which is sampled first is put at the start of the record (in bytes #1 to n) and the next data sample is appended to data from the first sample (bytes #n+1 to m), and so on.4.5.2.1.2.20 Requirements from section DTC snapshot sampling criteria

### 2120 — Sampling criteria for DTCSnapshotRecordNumber 0x20, single sample
- 版本：v5 ｜ 验证方式：Test ｜ 适用：4.0.x 与 4.1+ 分别定义
- x: For all DTCs supported by the ECU DTC snapshot data shall be sampled and stored with DTCSnapshotRecordNumber 0x20 when the following criteria is satisfied for the data associated with the DTC: Each time the FDC10 reaches a value that is equal to or greater than its unconfirmedDTCLimit until the FDC10 reaches the value +127 (since DTC information was last cleared) and each time the FDC10 reaches the value +127 until the DTC staus bit 3 – confirmedDTC is set to 1 (since DTC information was last cleared).
- If FDC10 reaches a value that is equal to or greater than its unconfirmedDTCLimit and less than +127 more than once during an operation cycle then the sampling of data shall be triggered the first time only.
- If FDC10 reaches the value +127 more than once during an operation cycle then the sampling of data shall be triggered the first time only.

### 2121 — Sampling criteria for DTCSnapshotRecordNumber 0x21, single sample
- 版本：v3 ｜ 验证方式：Test ｜ 适用：4.0.x 与 4.1+ 分别定义
- When implementing with AUTOSAR 4.0x: This requirement is Not ApplicableWhen implementing with AUTOSAR 4.1 or newer: For all DTCs supported by the ECU DTC snapshot data shall be sampled and stored with DTCSnapshotRecordNumber 0x21 when the following criteria is satisfied for the data associated with the DTC: Each time the FDC10 reaches a value that is equal to or greater than its unconfirmedDTCLimit and less than +127 (since DTC information was last cleared).
- If FDC10 reaches a value that is equal to or greater than its unconfirmedDTCLimit and less than +127 more than once during an operation cycle then the sampling of data shall be triggered the first time only.
- Only the last sampled DTC snapshot data shall kept in the memory (the previously sampled DTC snapshot data is overwritten).

### 2122 — Sampling criteria for DTCSnapshotRecordNumber 0x30 to 0x3F, multiple samples
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- For DTCs supported by the ECU DTC snapshot data may be sampled and stored with DTCSnapshotRecordNumber in the range 0x30 to 0x3F according to the following: The DTC snapshot data shall be sampled periodically.
- A number of samplers before and/or after the criteria are satisfied shall be stored (the number of samples, and the periodicity, shall be defined by the implementer).
- The DTC snapshot record shall only consist of DTC snapshot data that is needed during the development of the ECU.

### 2123 — Sampling criteria for DTCSnapshotRecordNumber 0x40 to 0x4F, single sample
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Table: Requirements on implementation DTC snapshot sampling criteria For DTCs supported by the ECU DTC snapshot data may be sampled and stored with DTCSnapshotRecordNumber in the range 0x40 to 0x4F according to the following: The DTC snapshot data shall be sampled (and stored) once when the criteria is satisfied.
- The DTC snapshot record shall only consist of DTC snapshot data that is needed during the development of the ECU.
- The implementer shall not expect that CEVT tools support the DTC snapshot record.

### 2124 — Sampling criteria for DTCSnapshotRecordNumber 0x50 to 0x5F, other samples
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Table: Requirements on implementation DTC snapshot sampling criteria For DTCs supported by the ECU DTC snapshot data may be sampled and stored with DTCSnapshotRecordNumber in the range 0x50 to 0x5F according to the following: The sampling criteria is specified by the implementer.
- The DTC snapshot record shall only consist of DTC snapshot data that is needed during the development of the ECU.
- The implementer shall not expect that CEVT tools support the DTC snapshot record.

### 2125 — Support for DTC status bit confirmedDTC
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- Table "Requirements on implementation of DTC status bits" The DTC status bit no 3, confirmedDTC, shall be supported for all DTCs supported by the ECU, as defined in [Data_50] Road vehicles – Diagnostics systems – Diagnostic services , UDS - Data - External publications, with the following addition: The bit shall be set to 1 when the OCC6 reaches the confirmedDTCLimit.
- The value of the the confirmedDTCLimit shall be in the range of [1, +15].
- The bit shall be reset to 0 when the DTC is aged.

### 2126 — Support for DTC status bit pendingDTC
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- Table "Requirements on implementation of DTC status bits" The DTC status bit no 2, pendingDTC, shall be supported for all DTCs supported by the ECU, as defined in [Data_50] Road vehicles – Diagnostics systems – Diagnostic services , UDS - Data - External publications.

### 2127 — Support for DTC status bit testFailed
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Table "Requirements on implementation of DTC status bits" The DTC status bit no 0, testFailed, shall be supported for all DTCs supported by the ECU, as defined in [Data_50] Road vehicles – Diagnostics systems – Diagnostic services , UDS - Data - External publications , with the following exception: No additional reset conditions are allowed to be defined by the implementer.

### 2128 — Support for DTC status bit testFailedSinceLastClear
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Table "Requirements on implementation of DTC status bits" The DTC status bit no 5, testFailedSinceLastClear, shall be supported for all DTCs supported by the ECU, as defined in [Data_50] Road vehicles – Diagnostics systems – Diagnostic services , UDS - Data - External publications.

### 2129 — Support for DTC status bit testFailedThisOperationCycle
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Table "Requirements on implementation of DTC status bits" The DTC status bit no 1, testFailedThisOperationCycle, shall be supported for all DTCs supported by the ECU, as defined in [Data_50] Road vehicles – Diagnostics systems – Diagnostic services , UDS - Data - External publications.

### 2130 — Support for DTC status bit testNotCompletedSinceLast-Clear
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Table "Requirements on implementation of DTC status bits" The DTC status bit no 4, testNotCompletedSinceLast-Clear, shall be supported for all DTCs supported by the ECU, as defined in [Data_50] Road vehicles – Diagnostics systems – Diagnostic services , UDS - Data - External publications.

### 2131 — Support for DTC status bit testNotCompletedThis-OperationCycle
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Table "Requirements on implementation of DTC status bits" The DTC status bit no 6, testNotCompletedThis-OperationCycle, shall be supported for all DTCs supported by the ECU, as defined in [Data_50] Road vehicles – Diagnostics systems – Diagnostic services , UDS - Data - External publications.

### 2132 — Support for DTC status bit warningIndicatorRequested
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Table "Requirements on implementation of DTC status bits" The DTC status bit no 7, warningIndicatorRequested, shall be supported for all DTCs supported by the ECU, as defined in [Data_50] Road vehicles – Diagnostics systems – Diagnostic services , UDS - Data - External publications , with the following exception: No additional reset conditions are allowed to be defined by the implementer.

### 2133 — Support for DTC status indicator #30
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- To provide enhanced information about the occurrence of a fault, that may be useful in the analysis of the fault.
- Table "Requirements on implementation of DTC status indicators" For all DTCs supported by the ECU a status indicator record identified by DTCExtendedDataRecordNumber=30 (SI30) shall be implementedThe status indicator record shall be reported as a 1 byte value.

### 2134 — Support for DTC status indicator #30, AgedDTC.
- 版本：v4 ｜ 验证方式：Test ｜ 适用：4.0.x 与 4.1+ 分别定义
- x: For all DTCs supported by the ECU, bit no 3 of SI30 shall indicate AgedDTC according to the following definition:- The bit is set to 1 when the DTC is aged.- The bit is reset to 0 when the aged DTC reoccurs.
- When implementing with AUTOSAR 4.1 or newer: For all DTCs supported by the ECU, bit no 3 of SI30 shall be set to 0.

### 2135 — Support for DTC status indicator #30, EmissionRelatedDTC
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on implementation of DTC status indicators" For all DTCs supported by the ECU, bit no 6 of SI30 shall indicate EmissionRelatedDTC according to the following definition: The bit shall be set to 1 when the DTC is emission related.

### 2136 — Support for DTC status indicator #30, SymptomSinceLastClear
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Table "Requirements on implementation of DTC status indicators" For all DTCs supported by the ECU, bit no 4 of SI30 shall be supported as defined by afeasibility study performed by the implementer.
- The feasibility study shall be approvedby the responsible authority appointed by OEM).
- If implemented bit no 4 of SI30 shall indicate SymptomSinceLastClear according to thefollowing definition: The bit shall be set to 1 when FDC10 is in the range [unconfirmedDTCLimit, +127] and specificconditions specified by the implementer, that need to be fulfilled in order to generate customersymptom, are satisfied.

### 2137 — Support for DTC status indicator #30, testFailedSinceLastClear/Aged
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Table "Requirements on implementation of DTC status indicators" For all DTCs supported by the ECU, bit no 7 of SI30 shall indicatetestFailedSinceLastClear/Aged according to the following definition: The bit is set to set to 1 wthen DTC test is falied i.

### 2138 — Support for DTC status indicator #30, UnconfirmedDTC
- 版本：v4 ｜ 验证方式：Test ｜ 适用：4.0.x 与 4.1+ 分别定义
- To provide an early indication that a fault may be currently present.
- x: For all DTCs supported by the ECU, bit no 0 of SI30 shall indicate UnconfirmedDTC according to the following definition: The bit shall be set to 1 when FDC10 reaches a value in the range [unconfirmedDTCLimit,+127]The bit shall be reset to 0 when FDC10 reaches the value -128.
- The value shall be in the range of [+1, +127].

### 2139 — Support for DTC status indicator #30, UnconfirmedDTCSinceLastClear
- 版本：v3 ｜ 验证方式：Test ｜ 适用：4.0.x 与 4.1+ 分别定义
- To provide an early indication that a fault may be present or has been present since last clear.
- x: For all DTCs supported by the ECU, bit no 2 of SI30 shall indicateUnconfirmedDTCSinceLastClear according to the following definition:- The bit is set to 1 when the FDC10 reach a value in the range [unconfirmedDTCLimit, +127].
- When implementing with AUTOSAR 4.1 or newer: For all DTCs supported by the ECU, bit no 2 of SI30 shall be set to 0.

### 2140 — Support for DTC status indicator #30, UnconfirmedDTCThisOperationCyle
- 版本：v3 ｜ 验证方式：Test ｜ 适用：4.0.x 与 4.1+ 分别定义
- To provide an early indication that a fault may be present in the current operation cycle.
- x: For all DTCs supported by the ECU, bit no 1 of SI30 shall indicateUnconfirmedDTCThisOperationCyle according to the following definition: The bit is set to 1 when the FDC10 reach a value in the range [unconfirmedDTCLimit, +127].
- The bit shall be reset to 0 at the start of an operation cycle.

### 2141 — Support for DTC status indicator #30, WarningIndicatorRequestedSinceLastClear
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- For all DTCs supported by the ECU, bit no 5 of SI30 shall indicateWarningIndicatorRequestedSinceLastClear according to the following definition: The bit shall be set to 1 when DTC status bit no 7 is set to 1.
- However, the bit may also be set to 1 even when DTC status bit not 7 – warningIndicatorRequested is not set to 1 (refer to reference [Data_50] Road vehicles – Diagnostics systems – Diagnostic services, UDS - Data - External publications regarding requirements on set of DTC status bit not 7 to 1) according to the following: The bit is set to 1 when the same criteria as required by the above mention reference on set of DTC status bit not 7 – warningIndicatorRequested to 1 is satisfied, but it may also be set to 1 and warning indicator may be requested before DTC status bit 3 – confirmed DTC is set to 1.
- Note that in all cases must FDC10 has reached the value +127, since DTC information was latest cleared, before the bit is set to 1 and warring indicator is requested (if not otherwise is specified in this document).

### 2142 — Support for DTC time stamp #20
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- To provide enhanced information about the occurrence of a fault, that may be useful in the analysis of the fault.
- Table "Requirements on implementation of DTC time stamps" For all DTCs supported by the ECU a data record identified byDTCExtendedDataRecordNumber=20 shall be implemented according to the following definition: The record value shall be equal to the global real time (data record 0xDD00) that is taken the first time FDC10 reaches a value that is equal to or greater than unconfirmedDTCLimit, since DTC information was last cleared.
- The stored data record shall be reported as a 4 byte value on request of the diagnostic services specified in reference [Data_1] UDS Services.

### 2143 — Support for DTC time stamp #21
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- To provide enhanced information about the occurrence of a fault, that may be useful in the analysis of the fault.
- Table "Requirements on implementation of DTC time stamps" For all DTCs supported by the ECU a data record identified byDTCExtendedDataRecordNumber=21 shall be implemented according to the following definition: The record value shall be equal to the global real time (data record 0xDD00) that is taken the latest time FDC10 reaches a value that is equal to or greater than unconfirmedDTCLimit, since DTC information was last cleared.
- If FDC10 is updated and reaches a value equal to or greater than unconfirmedDTCLimit more than once during an operation cycle then the time stamp shall be taken the first time only.

### 2144 — Access to external analog input signal data records
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The data records for external signals shall be available in application software but does not have to be supported in boot software.
- Table "Requirements for definition of ECU external signals in data records" - item 2.1 and 2.2 It shall be possible to access external analog input signal data records, by the relevant diagnostic services specified in [Data_1] UDS Services, in all diagnostic sessions, except programming session.

### 2145 — Access to external FM, PCM, PWM input signal data records
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The data records for external signals shall be available in application software but does not have to be supported in boot software.
- Table "Requirements for definition of ECU external signals in data records" - item 3.1 and 3.2 It shall be possible to access external FM, PCM, PWM (or similar) input signal data records, by the relevant diagnostic services specified in [Data_1] UDS Services, in all diagnostic sessions, except programming session.

### 2146 — Access to external output signal data records
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The data records for external signals shall be available in application software but does not have to be supported in boot software.
- Table "Requirements for definition of ECU external signals in data records" - item 4.1 and 4.2 It shall be possible to access external output signal data records, by the relevant diagnostic services specified in [Data_1] UDS Services, in all diagnostic sessions, except programming session.

### 2147 — Access to external switch input signal data records
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The data records for external signals shall be available in application software but does not have to be supported in boot software.
- Table "Requirements for definition of ECU external signals in data records" - item 1,1 and 1.2 It shall be possible to access external switch input signal data records, by the relevant diagnostic services specified in [Data_1] UDS Services, in all diagnostic sessions, except programming session.

### 2148 — Access to network signal data records - signals received by public ECU
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The data records for network signals shall be available in application software Table "Requirements for definition of ECU external signals in data records" - item 5.2 It shall be possible to access the data records for received network signals, by the relevant diagnostic services specified in [Data_1] UDS Services, in all diagnostic sessions, except programming session.

### 2149 — Access to network signal data records - signals transmitted by public ECU
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The data records for network signals shall be available in application software but does not have to be supported in boot software.
- Table "Requirements for definition of ECU external signals in data records" - item 5.1 It shall be possible to access the data records for transmitted network signals, by the relevant diagnostic services specified in [Data_1] UDS Services, in all diagnostic sessions, except programming session.

### 2150 — Access to other external signal data records defined by the implementer
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The data records for external signals shall be available in application software but does not have to be supported in boot software.
- Table "Requirements for definition of ECU external signals in data records" - item 8 It shall be possible to access the data records for other external signal defined by the implementer, by the relevant diagnostic services specified in [Data_1] UDS Services, in all diagnostic sessions, except programming session.

### 2151 — Access to power supply input signal data records
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The data records for external signals shall be available in application software but does not have to be supported in boot software.
- Table "Requirements for definition of ECU external signals in data records" - item 7 It shall be possible to access power supply input signal data records, by the relevant diagnostic services specified in [Data_1] UDS Services, in all diagnostic sessions, except programming session.

### 2152 — Control of network signal data records - periodic signals transmitted by...
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- The test tool must not change the periodicity of transmitted signals as this could lead to faults detected in other ECUs.
- Table "Requirements for definition of ECU external signals in data records" - item 5.1 If the network signal is normally sent periodically by the ECU then this must continue during diagnostic control of the signal.

### 2153 — External analog input signals update time
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements for definition of ECU external signals in data records" - item 2.1 and 2.2 For all external analog input signal data records, the value read by the diagnostic services specified in [Data_1] UDS Services shall be updated by the ECU each 100 ms or faster.

### 2154 — External FM, PCM, PWM input signals update time
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements for definition of ECU external signals in data records" - item 3.1 and 3.2 For all external FM, PCM, PWM (or similar) input signal data records, the value read by the diagnostic services specified in [Data_1] UDS Services shall be updated by the ECU each 100 ms or faster.

### 2155 — External output signals update time - actual output signal
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements for definition of ECU external signals in data records" - item 4.2 For all external output signal data records, for the actual output signal read back by the ECU, the value read by the diagnostic services specified in [Data_1] UDS Services, shall be updated by the ECU each 100 ms or faster.

### 2156 — External switch input signals update time
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements for definition of ECU external signals in data records" - item 1.1 and 1.2 For all external switch input signal data records, the value read by the diagnostic services specified in [Data_1] UDS Services shall be updated by the ECU each 100 ms or faster.

### 2157 — for external analog input signal data records - application signal
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements for definition of ECU external signals in data records" - item 2.2 For each external analog signal a feasibility study shall be performed by the implementer to decide if a data record shall be implemented for reading the value of the analog input signal currently available for the ECU’s application software.
- The feasibility study shall be approved by the responsible authority appointed by OEM).

### 2158 — Individual control of external output signals - application signal
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- To enhance fault tracing capabilities it shall be possible to control the output signals from the ECU from the diagnostic test tool.
- Table "Requirements for definition of ECU external signals in data records" - item 4.1 It shall be possible to control each external output signal (the desired set point normally controlled by the ECU's application software) individually and independently of each other unless there are special safety reasons not to do this.
- If any output is prohibited to be controlled due to such safety reason, this must be approved by the responsible authority appointed by OEM

### 2159 — Individual control of network signal data records - signals transmitted ...
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- To enhance fault tracing capabilities it shall be possible to individually control the network signals transmitted from the ECU from the diagnostic test tool.
- Table "Requirements for definition of ECU external signals in data records" - item 5.1 If control of the network signals is required (as defined by the feasibility study) it shall be possible to control the signals individually and independently of each other unless there are special safety reasons not to do this.
- If any network signal is prohibited to be controlled due to such safety reason, this must be approved by the responsible authority appointed by OEM.

### 2160 — Individual control of other external signal data records defined by the ...
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- To enhance fault tracing capabilities it shall be possible to individually control the signals from the ECU from the diagnostic test tool.
- Table "Requirements for definition of ECU external signals in data records" - item 8 If control of the external signal data records defined by the implementer is required (as defined by the feasibility study) it shall be possible to control the signals individually and independently of each other unless there are special safety reasons not to do this.
- If any network signal is prohibited to be controlled due to such safety reason, this must be approved by the responsible authority appointed by OEM.

### 2161 — Power supply input signals update time
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements for definition of ECU external signals in data records" - item 7 For all power supply input signal data records, the value read by the diagnostic services specified in [Data_1] UDS Services shall be updated by the ECU each 100 ms or faster.

### 2162 — Read and control of the network signal data record 0xDD02 transmitted by public ECU
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- If the ECU is responsible for maintaining and distributing the network signal that contain the data record 0xDD02 – “Vehicle battery voltage”, the value of the network signal shall be possible to read and control.

### 2163 — Reporting external analog input signal data records while the input parameter value is under tester
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- If the tester is actively controlling the input parameter the tester substituted value must be reported in the data record since this is the value that the ECu application is using Table "Requirements for definition of ECU external signals in data records" - item 2.1 If it is possible to control the value of an external analog input signal, by diagnostic services specified in [Data_1] UDS Services, the ECU shall report the tester substituted input value to a diagnostic request to read a data record for an actual external analog input signal while the input parameter value is under tester control.

### 2164 — Reporting external FM, PCM, PWM input signal data records while the input...
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- If the tester is actively controlling the input parameter the tester substituted value must be reported in the data record since this is the value that the ECU application is using.
- Table "Requirements for definition of ECU external signals in data records" item 3.1 and 3.2 If it is possible to control the value of an external FM, PCM, PWM (or similar) input signal, by diagnostic services specified in [Data_1] UDS Services, the ECU shall report the tester substituted input value to a diagnostic request to read a data record for an actual digital external FM, PCM, PWM (or similar) input signal while the input parameter value is under tester control.

### 2165 — Reporting external switch input signal data records while the input para...
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- If the tester is actively controlling the input parameter the tester substituted value must be reported in the data record since this is the value that the ECU application is using.
- Table "Requirements for definition of ECU external signals in data records" - item 1.1 If it is possible to control the value of an external switch input signal, by diagnostic services specified in [Data_1] UDS Services, the ECU shall report the tester substituted input value to a diagnostic request to read a data record for an actual digital external switch input signal while the input parameter value is under tester control.

### 2166 — Reporting other external signal data records defined by the implementer ...
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- If the tester is actively controlling a signal the tester substituted value must be reported in the data record since this is the value that the ECU application is using.
- Table "Requirements for definition of ECU external signals in data records" - item 8 If it is possible to control the value of an external signal defined by the implementer, by diagnostic services specified in [Data_1] UDS Services, the ECU shall report the tester substituted value to a diagnostic request to read a data record for the received network signal while the signal value is under tester control.

### 2167 — Reporting power supply input signal data records while the input paramet...
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- If the tester is actively controlling the input parameter the tester substituted value must be reported in the data record since this is the value that the ECU application is using.
- Table "Requirements for definition of ECU external signals in data records" - Item 7 If it is possible to control the value of power supply input signal, by diagnostic services specified in [Data_1] UDS Services, the ECU shall report the tester substituted input value to a diagnostic request to read a data record for an actual digital external switch input signal while the input parameter value is under tester control.

### 2168 — Reporting received network signal data records while the input parameter...
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- If the tester is actively controlling the network signal the tester substituted value must be reported in the data record since this is the value that the ECU application is using.
- Table "Requirements for definition of ECU external signals in data records" - item 5.2 If it is possible to control the value of a received network signal, by diagnostic services specified in [Data_1] UDS Services, the ECU shall report the tester substituted value to a diagnostic request to read a data record for the received network signal while the signal value is under tester control.

### 2169 — Support for external analog input signal data records - actual input signal
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements for definition of ECU external signals in data records" - item 2.1 For each external analog input signal a separate data record shall be defined within the ECU for reading the actual digital input signal read by the ECU.
- The record value shall be the sampled raw signal, after necessary HW and/or SW filtering of “normal” disturbances.
- By examining the raw signal it shall be possible to determine if the signal is correct or if a short to battery, short to ground or open circuit is present.

### 2170 — Support for external FM, PCM, PWM input signal data records - actual inp...
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements for definition of ECU external signals in data records" item 3.2 For each external FM, PCM, PWM (or similar) input signal a feasibility study shall be performed by the implementer to decide if a data record shall be implemented for reading the value of the input signal read by the ECU.
- The feasibility study shall be approved by the responsible authority appointed by OEM).
- The record value shall be the sampled raw signal, after necessary HW and/or SW filtering of “normal” disturbances.

### 2171 — Support for external FM, PCM, PWM input signal data records - engineering units
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements for definition of ECU external signals in data records" item 3.1 For each external FM, PCM, PWM (or similar) input signal a separate data record shall be defined within the ECU for reading the actual digital input signal read by the ECU.
- The record value shall be the actual input signal in suitable engineering units.
- By examining the value read it shall be possible to decide whether the circuit is correct or if a short to battery voltage, short to ground or open circuit fault is present.

### 2172 — Support for external output signal data records - actual output signal
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements for definition of ECU external signals in data records" - item 4.2 For each external output signal a separate data record shall be defined within the ECU for reading the actual output signal read back by the ECU.

### 2173 — Support for external output signal data records - application signal
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements for definition of ECU external signals in data records" - item 4.1 For each external output signal a separate data record shall be defined within the ECU for reading and controlling the output signal (the desired set point) controlled by the ECU's application software.

### 2174 — Support for external switch input signal data records actual input signal
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements for definition of ECU external signals in data records" - item 1.1 For each external switch input signal a separate data record shall be defined within the ECU for reading the actual digital input signal read by the ECU.
- The record value shall be the sampled raw signal, after necessary HW and/or SW filtering of "normal" disturbances.

### 2175 — Support for external switch input signal data records - application signal
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements for definition of ECU external signals in data records" - item 1.2 For each external switch input signal a feasibility study shall be performed by the implementer to decide if a data record shall be implemented for reading the value of the switch input signal currently available for the ECU's application software.
- The feasibility study shall be approved by the responsible authority appointed by OEM).

### 2176 — Support for network signal data records - signals received by public ECU
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements for definition of ECU external signals in data records" - item 5.2 If the ECU is a public ECU a feasibility study shall be performed by the implementer for each network signal received by the ECU to decide if data records shall be implemented for reading the values of the signals.
- The feasibility study shall be approved by the responsible authority appointed by OEM).

### 2177 — Support for network signal data records - signals transmitted by public ECU
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements for definition of ECU external signals in data records" - item 5.1 If the ECU is a public ECU a feasibility study shall be performed by the implementer for each network signal transmitted by the ECU to decide if data records shall be implemented for reading and/or controlling the values of the signals.
- The feasibility study shall be approved by the responsible authority appointed by OEM).

### 2178 — Support for other external signal data records defined by the implementer
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- The implementer shall identify which other signals, not covered by the the requirements in this specification, that shall be monitored.
- Table "Requirements for definition of ECU external signals in data records" - item 8 A feasibility study shall be performed by the implementer to decide if data records shall be implemented for reading and/or controlling the values of any additional external signals.
- The feasibility study shall be approved by the responsible authority appointed by OEM).

### 2179 — Support for power supply data record
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements for definition of ECU external signals in data records" - item 7 For each power supply to the ECU a separate data record shall be defined within the ECU for reading the actual voltage input to the ECU.
- The record value shall be the actual voltage read as an analog input signal by the ECU (i.

### 2180 — Access to input from internal HMI signal data records
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Data records for internal signals shall be available in application software but does not have to be supported in boot software.
- Table "Requirements for definition of ECU internal signals in data records" - item 1.1 and 1.2 It shall be possible to access input from internal HMI signal data records, by the relevant diagnostic services specified in [Data_1] UDS Services, in all diagnostic sessions, except programming session.

### 2181 — Access to other internal signal data records defined by the implementer
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The data records for ECU internal signals shall be available in application software but does not have to be supported in boot software.
- Table "Requirements for definition of ECU internal signals in data records" - item 3 It shall be possible to access the data records for other ECU internal signals defined by the implementer, by the relevant diagnostic services specified in [Data_1] UDS Services, in all diagnostic sessions, except programming session.

### 2182 — Access to output to internal HMI signal data records
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The data records for internal signals shall be available in application software but does not have to be supported in boot software.
- Table "Requirements for definition of ECU internal signals in data records" - item 2 It shall be possible to access output to internal HMI signal data records, by the relevant diagnostic services specified in [Data_1] UDS Services, in all diagnostic sessions, except programming session.

### 2183 — Individual control of other ECU internal signal data records defined by ...
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- To enhance fault tracing capabilities it shall be possible to individually control the ECU internal signals from the diagnostic test tool.
- Table "Requirements for definition of ECU internal signals in data records" - item 3 If control of the ECU internal signal data records defined by the implementer is required (as defined by the feasibility study) it shall be possible to control the signals individually and independently of each other unless there are special safety reasons not to do this.
- If any network signal is prohibited to be controlled due to such safety reason, this must be approved by the responsible authority appointed by OEM.

### 2184 — Individual control of output to internal HMI signals
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- To enhance fault tracing capabilities it shall be possible to control the output signals from the ECU from the diagnostic test tool.
- Table "Requirements for definition of ECU internal signals in data records" - item 2 It shall be possible to control each output to internal HMI signal (the desired set point normally controlled by the ECU's application software) individually and independently of each other unless there are special safety reasons not to do this.
- If any output signal is prohibited to be controlled due to such safety reason, this must be approved by the responsible authority appointed by OEM

### 2185 — Reporting input from internal HMI signal data records while the input pa...
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- If the tester is actively controlling the input parameter the tester substituted value must be reported in the data record since this is the value that the ECU application is using Table "Requirements for definition of ECU internal signals in data records" - item 1.1 If it is possible to control the value of an input from internal HMI signal, by diagnostic services specified in [Data_1] UDS Services, the ECU shall report the tester substituted input value to a diagnostic request to read a data record for an actual digital internal HMI input signal while the input parameter value is under tester control.

### 2186 — Reporting other ECU internal signal data records defined by the implement...
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- If the tester is actively controlling a signal the tester substituted value must be reported in the data record since this is the value that the ECU application is using Table "Requirements for definition of ECU internal signals in data records" - item 3 If it is possible to control the value of an ECU internal signal defined by the implementer, by diagnostic services specified in [Data_1] UDS Services, the ECU shall report the tester substituted value to a diagnostic request to read a data record for the received network signal while the signal value is under tester control.

### 2187 — Support for input from internal HMI signal data records - actual input signal
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements for definition of ECU internal signals in data records" - item 1.1 For each input from internal HMI signal a data record shall be defined within the ECU for reading the actual digital input signal read by the ECU.
- The record value shall be the sampled raw signal, after necessary HW and/or SW filtering of “normal” disturbances.

### 2188 — Support for input from internal HMI signal data records - application si...
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements for definition of ECU internal signals in data records" - item 1.2 For each input from internal HMI signal a feasibility study shall be performed by the implementer to decide if a data record shall be implemented for reading the value of the internal HMI signal currently available for the ECU's application software.
- The feasibility study shall be approved by the responsible authority appointed by OEM).

### 2189 — Support for other internal signal data records defined by the implementer
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- The implementer shall identify which other signals, not covered by the the requirements in this specification, that shall be monitored.
- Table "Requirements for definition of ECU internal signals in data records" - item 3 A feasibility study shall be performed by the implementer to decide if data records shall be implemented for reading and/or controlling the values of any additional ECU internal signals.
- The feasibility study shall be approved by the responsible authority appointed by OEM).

### 2190 — Support for output to internal HMI signal data records
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements for definition of ECU internal signals in data records" - item 2 For each output to internal HMI signal a separate data record shall be defined within the ECU for reading and controlling the output signal (the desired set point) controlled by the ECU's application software.

### 2191 — Update time for input from internal HMI signal data records
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements for definition of ECU internal signals in data records" - item 1.1 and 1.2 For all internal HMI input signal data records, the value read by the diagnostic services specified in [Data_1] UDS Services shall be updated by the ECU each 100 ms or faster.4.5.2.1.2.5 Requirements from section ECU_Vehicle status

### 2192 — Access to Application Diagnostic Database Part Number data record
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- To support diagnostic procedures it must be possible to read out the Application Diagnostic Database Part Number from the ECU, except in programming session.
- Section "ECU/Vehicle identification" It shall be possible to read the data record with the identifier 0xF120 and the data record with the identifier 0xF1A0, by diagnostic services specified in [Data_1] UDS Services, in all diagnostic sessions except programming session.

### 2193 — Access to Complete ECU PartSerial Number data record
- 版本：v5 ｜ 验证方式：Test ｜ 适用：通用
- To support diagnostic procedures it must be possible to read out the Complete ECU Part/Serial Number data record.
- Section "ECU/Vehicle identification" It shall be possible to read the data record with the identifier 0xEDA0 and the data record with the identifier 0xED20, by diagnostic services specified in [Data_1] UDS Services, including programming session running in both primary and secondary bootloader.

### 2194 — Access to Diagnostic Autosar version number
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- To support diagnostic procedures it must be possible to read out the AUTOSAR cluster(s) implemented in the ECU, except in programming session.
- Section "ECU/Vehicle identification" It shall be possible to read the data record with the identifier 0xF126, by diagnostic services specified in [Data_1] UDS Services, in all diagnostic sessions except programming session.

### 2195 — Access to ECU Core Assembly Part Number data record
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- To support diagnostic procedures it must be possible to read out the ECUCore Assembly Part Number data record.
- Section "ECU/Vehicle identification" It shall be possible to read the data record with the identifier 0xF12A and a data record withidentifier 0xF1AA, by diagnostic services specified in reference [Data_1] UDS Services, in alldiagnostic sessions, including programming session running in both primary and secondarybootloader.

### 2196 — Access to ECU Delivery Assembly Part Number data record
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- To support diagnostic procedures it must be possible to read out the ECDelivery Assembly Part Number data record, except in programming session.
- Section "ECU/Vehicle identification" It shall be possible to read the data record with the identifier 0xF12B and the data record withthe identifier 0xF1AB, by diagnostic services specified in [Data_1] UDS Services, in alldiagnostic sessions , including programming session running in both primary and secondarybootloader.

### 2197 — Access to ECU Serial Number data record
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- To support diagnostic procedures it must be possible to read out the ECUSerial Number data record.
- Section "ECU/Vehicle identification" It shall be possible to read the data record with the identifier 0xF18C, by diagnostic servicesspecified in reference [Data_1] UDS Services, in all diagnostic sessions, includingprogramming session running in both primary and secondary bootloader.

### 2198 — Access to ECU Software Extended Part Numbers data record
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- To support diagnostic procedures it must be possible to read out the ECU Software Extended Part Numbers data record, except in programming session.
- Section "ECU/Vehicle identification" It shall be possible to read the data record with the identifier 0xF12F and the data record with the identifier 0xF1AF, by diagnostic services specified in reference [Data_1] UDS Services, in all diagnostic sessions except programming session.

### 2199 — Access to ECU Software Part Numbers data record
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- To support diagnostic procedures it must be possible to read out the ECU Software Part Numbers data record, except in programming session.
- Section "ECU/Vehicle identification" It shall be possible to read the data record with the identifier 0xF12E and the data record with the identifier 0xF1AE, by diagnostic services specified in [Data_1] UDS Services, in all diagnostic sessions except programming session.

### 2200 — Access to Primary Bootloader Diagnostic Database Part Number
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- To support diagnostic procedures it must be possible to read out the database key for the diagnostic database used by the ECU's primary bootloader SW.
- Section "ECU/Vehicle identification" It shall be possible to read the data record with the identifier 0xF121 and the data record with the identifier 0xF1A1, by diagnostic services specified in reference [Data_1] UDS Services, in programming session running in both primary and secondary bootloader.
- It may be possible to read the data identifiers in other sessions.

### 2201 — Access to Primary Bootloader Software Part Number data record
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- To support diagnostic procedures it must be possible to read out the Primary Bootloader Software Part Number data record.
- Section "ECU/Vehicle identification" It shall be possible to read the data record with the identifier 0xF125 and the data record with the identifier 0xF1A5 by diagnostic services specified in reference [Data_1] UDS Services, in programming session running in both primary and secondary bootloader.
- It may be possible to read the data identifiers in other sessions.

### 2202 — Access to Private ECU(s) or component(s) Serial Number data record
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- It shall be possible to read out the data record with the identifier 0xF13F by diagnostic services specified in reference [Data_1] UDS Services, in all diagnostic sessions except programming session.

### 2203 — Access to Secondary Bootloader Diagnostic Database Part Number
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- To support diagnostic procedures it must be possible to read out the database key for the diagnostic database used by the ECU's secondary bootloader SW, when executing the secondary bootloader in programming session.
- Section "ECU/Vehicle identification" It shall be possible to read the data record with the identifier 0xF122 and the data record with the identifier 0xF1A2 by diagnostic services specified in [Data_1] UDS Services, when the ECU is executing the secondary bootloader in programming session.

### 2204 — Access to Secondary Bootloader Software Version Number data record
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- To support diagnostic procedures it must be possible to read out the Secondary Bootloader Software Version Number data record.
- Section: ECU/Vehicle identification It shall be possible to read the data record with the identifier 0xF124, by diagnostic services specified in reference [Data_1] UDS Services in programming session running in secondary bootloader.

### 2205 — Access to Vehicle Configuration Parameters data record
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- To support diagnostic procedures it must be possible to read out the Vehicle Configuration Parameters from the ECU, except in programming session.
- Section "ECU/Vehicle identification" It shall be possible to read the data record with the identifier 0xF106, by diagnostic services specified in [Data_1] UDS Services, in all diagnostic sessions in which the service is supported except programming session.

### 2206 — Access to Vehicle Identification Number data record
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- To support diagnostic procedures it must be possible to read out the Vehicle Identification Number data record, except in programming session.
- Section "ECU/Vehicle identification" If the data record with the identifier 0xF190 is implemented in the ECU, it shall be possible to read this data record by diagnostic services specified in [Data_1] UDS Services, in all diagnostic sessions except programming session.

### 2207 — Access to Vehicle Information Section data record
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- To support diagnostic procedures it must be possible to read out the Vehicle Information Section data record, except in programming session.
- Section "ECU/Vehicle identification" It shall be possible to read the data record with the identifier 0xF114, by diagnostic services specified in [Data_1] UDS Services, in all diagnostic sessions except programming session.

### 2208 — Application Diagnostic Database Part Number data record
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- Section "ECU/Vehicle identification" A data record with identifier 0xF120 shall be implemented containing Volvo Cars format Part number.
- A data record with identifier 0xF1A0 shall be implemented containing Geely format Part number.
- Both data records shall be implemented in all ECU: s independently of what car brand they shall be used in.

### 2209 — Autosar BSW cluster versions
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Section "ECU/Vehicle identification" If the ECU contains any AUTOSAR Basic Software cluster a data record with identifier 0xF126 shall be implemented exactly as defined in [Data_4] Global Master Reference Database.

### 2210 — Complete ECU PartSerial Number data record
- 版本：v8 ｜ 验证方式：Test ｜ 适用：通用
- Section "ECU/Vehicle identification" A data record with identifier 0xEDA0 shall be implemented containing Volvo Cars format Part number.
- A data record with identifier 0xED20 shall be implemented containing Geely format Part number.
- Both data records shall be implemented in all ECU: s independently of what car brand they shall be used in.

### 2211 — ECU Core Assembly Part Number data record
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- Section "ECU/Vehicle identification" A data record with identifier 0xF12A shall be implemented containing Volvo Cars format Part number.
- A data record with identifier 0xF1AA shall be implemented containing Geely format Part number.
- Both data records shall be implemented in all ECU: s independently of what car brand they shall be used in.

### 2212 — ECU Delivery Assembly Part Number data record
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- Section "ECU/Vehicle identification" A data record with identifier 0xF12B shall be implemented containing Volvo Cars format Part number.
- A data record with identifier 0xF1AB shall be implemented containing Geely format Part number.
- Both data records shall be implemented in all ECU: s independently of what car brand they shall be used in.

### 2213 — ECU Serial Number data record
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Section "ECU/Vehicle identification" A data record with identifier 0xF18C shall be implemented exactly as defined in [Data_4] Global Master Reference Database.
- Serial number data records shall have 8 digits for the serial number, all coded in BCD.
- The data record shall have a fixed length of 4 bytes, be right justified with any unused digit(s) filled with 0.

### 2214 — ECU Software Extended Part Numbers data record
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- To enable readout of the extended part numbers for the ECU softwares Section "ECU/Vehicle identification" If required by the project responsible OEM, data records shall be implemented according to the following: A data record with identifier 0xF12F shall be implemented containing Volvo Cars format Part number.
- A data record with identifier 0xF1AF shall be implemented containing Geely format Part number.
- Both data records shall be implemented in all ECU: s independently of what car brand they shall be used in.

### 2215 — ECU Software Part Number data record
- 版本：v6 ｜ 验证方式：Test ｜ 适用：通用
- Section "ECU/Vehicle identification" A data record with identifier 0xF12E shall be implemented containing Volvo Cars format Part numbers.
- A data record with identifier 0xF1AE shall be implemented containing Geely format Part numbers.
- Both data records shall be implemented in all ECU: s independently of what car brand they shall be used in.

### 2216 — ECU Software Structure Part Number data record
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- Section "ECU/Vehicle identification" If the ECU is supporting the Software Authentication concept where each data file is signed and verified individually as defined in [Data_10] General Software Authentication the ECU shall implement: A data record with identifier 0xF12C containing Volvo Cars format part number.
- The data records shall be implemented exactly as defined in [Data_4] Global Master Reference Database.
- It shall be possible to read the data records by diagnostic services specified in reference [Data_1] UDS Services, in programming session running in both primary and secondary bootloaderNote: Both data records shall be implemented in all ECU: s independently of what car brand they shall be used in.

### 2217 — No read of the Security Constant data record
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- For security reasons it must not be possible to read the value of the Security Constant in any diagnostic session.
- Section "ECU/Vehicle identification" If a data record with identifier 0xF102 is implemented in the ECU it shall not be possible to read the value of this data record by any diagnostic service in any diagnostic session or any kind of external debug interface that may be used without destroying the sealing of the ECU .

### 2218 — One time write of the Security Constant data record
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Once the value has been changed, it shall not be possible to change the value again.

### 2219 — Part number data records coding
- 版本：v6 ｜ 验证方式：Test ｜ 适用：通用
- 2219 v6Part number data records coding N/A Section "ECU/Vehicle identification" Part number data records used by VCC shall have 8 digits for part number + 3 characters (version suffix).
- Part number data records used by Geely shall have 10 digits for part number + 3 characters (version suffix).
- T he part number digits shall be coded in BCD and the 3 characters shall be coded in ASCII.

### 2220 — Primary Bootloader Diagnostic Database Part Number
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- Section "ECU/Vehicle identification" A data record with identifier 0xF121 shall be implemented containing Volvo Cars format Part number.
- A data record with identifier 0xF1A1 shall be implemented containing Geely format Part number.
- Both data records shall be implemented in all ECU: s independently of what car brand they shall be used in.

### 2221 — Primary Bootloader Software Part Number data record
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- Section "ECU/Vehicle identification" A data record with identifier 0xF125 shall be implemented containing Volvo Cars format Part number.
- A data record with identifier 0xF1A5 shall be implemented containing Geely format Part number.
- Both data records shall be implemented in all ECU: s independently of what car brand they shall be used in.

### 2222 — Private ECU(s) or component(s) Serial Number data record
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- A data record with identifier 0xF13F shall be implemented only if the following conditions are fulfilled:• The ECU is a Public ECU master for Private ECU(s) or component(s) which has additional documentation requirements.
- The content of the data record shall only consist of serial number(s) for Private ECU(s) or component(s) that are subject to additional documentation requirements.
- The content of the data record shall only consist of serial number(s) for those Private ECU(s) or component(s) that can not be directly addressed by a tester.

### 2223 — Secondary Bootloader Diagnostic Database Part Number
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- Section "ECU/Vehicle identification" A data record with identifier 0xF122 shall be implemented containing Volvo Cars format Part number.
- A data record with identifier 0xF1A2 shall be implemented containing Geely format Part number.
- Both data records shall be implemented in all ECU: s independently of what car brand they shall be used in.

### 2224 — Secondary Bootloader Software Version Number data record
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Section: ECU/Vehicle identification A data record with identifier 0xF124 shall be implemented exactly as defined in reference [Data_4] Global Master Reference Database.

### 2225 — Secondary Bootloader Software Version Number data record coding
- 版本：v2 ｜ 验证方式：Inspection ｜ 适用：通用
- Section: ECU/Vehicle identification The Secondary Bootloader Software Version Number 0xF124 shall be BCD encoded, right justified, all unused digit shall be filled with 0 in total 7 bytes.

### 2226 — Vehicle Configuration Parameters data record
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Section "ECU/Vehicle identification" A data record with identifier 0xF106 shall be implemented, exactly as defined in [Data_4] Global Master Reference Database, in the Car Configuration Domain Master, on networks with ECU configuration controlled by an on-board master configuration file.

### 2227 — Vehicle Identification Number data record
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Section "ECU/Vehicle identification" If the ECU has a requirement to store VIN, a data record with identifier 0xF190 shall be implemented exactly as defined in [Data_4] Global Master Reference Database

### 2228 — Vehicle Information Section data record
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Section "ECU/Vehicle identification" A data record with identifier 0xF114 shall be implemented exactly as defined in reference [Data_4] Global Master Reference Database, in the Car Configuration Domain Master, on networks with ECU configuration controlled by an on-board master configuration file.

### 2229 — Write of the Public Key data record
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- Section "ECU/Vehicle identification" If the ECU is supporting the Software Authentication concept where the data file is verified using a Public Key only as defined in [Data_10] General Software Authentication the ECU shall implement to: Write the Public Key data record with identifier 0xD01C, by diagnostic service defined in [Data_1] UDS Services, it is to be supported when the ECU is executing the secondary bootloader - programming session.4.5.2.1.2.7 Requirements from section DTC information - General

### 2230 — Active diagnostic session data record
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Table "Requirements for definition of ECU/Vehicle status in data records" A data record with identifier 0xF186 shall be implemented exactly as defined in [Data_4] Global Master Reference Database.

### 2231 — Build List data record
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The workshop tool must be able to read out the P-spec for the vehicle.
- Table "Requirements for definition of ECU/Vehicle status in data records" If the ECU is the Car Configuration Domain Master a data record with identifier 0xC011 shall be implemented exactly as defined in [Data_4] Global Master Reference Database.

### 2232 — Car Configuration Parameter Faults data record
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- To support a more advanced analysis of the vehicle behaviour it must be possible to understand how many incorrect configuration parameters that the ECU has received.
- A data record with identifier 0xE103 shall be implemented exactly as defined in [Data_4] Global Master Reference Database if the ECU support the DTC U230056 (0xE30056) - Invalid vehicle configuration data.

### 2233 — Car Mode data record
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Table - Requirements for definition of ECU/Vehicle status in data records If the ECU are publisher or subscriber of the car mode signal, a data record with identifier 0xD134 shall be implemented exactly as defined in reference [Data_4] Global Master Reference Database.

### 2234 — Control of Usage Mode data record
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- Table "Requirements for definition of ECU/Vehicle status in data records" It shall be possible to control the value of the data record 0xDD0A in the ECU that implements the Usage Mode Manager, by diagnostic services specified in [Data_1] UDS Services, in all diagnostic sessions in which the service used for control the data record is supported, except programming session.

### 2235 — Control or write of Car Mode data record
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- To enable control or write of the active Car mode. Table - Requirements for definition of ECU/Vehicle status in data records. Whether or not it be possible to control or write the value of the data record 0xD134, by diagnostic services specified in [Data_1] UD

### 2236 — Customer setting parameters data record
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The purpose is to support the ECU replacement process at workshop Table "Requirements for definition of ECU/Vehicle status in data records" A data record with identifier 0xDED0 shall be implemented if the ECU stores customer setting parameter.
- The data record shall only consist of record data that contain information of customer settings stored by the ECU.

### 2237 — Diagnostic Read out #1 to #4 data record
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- A data record(s) with identifier 0xEDC0 up to 0xEDC3 shall be implemented if required by the responsible authority appointed by OEM.
- The data record(s) shall only consist of other record data than the record data read by the generic standard read out sequence.

### 2238 — ECU List data record
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The workshop tool must be able to read out what ECUs are actually installed in the vehicle.
- "Requirements for definition of ECU/Vehicle status in data records" If the ECU is the Car Configuration Domain Master a data record with identifier 0xC010 shall be implemented exactly as defined in [Data_4] Global Master Reference Database.

### 2239 — Partial Network Cluster (PNC) data record
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- the ECU that supports the subsystem 'Internal-VMM implementation' (refer to [Data_3] Vehicle Mode Management - Concept SRD for details regarding VMM), a data record with identifier 0xDD0B shall be implemented exactly as defined in reference [Data_4] Global Master Reference Database.

### 2240 — Read Access to Active diagnostic session data record
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- To support diagnostic procedures it must be possible to read out the active diagnostic session from the ECU, independent of the diagnostic session.
- Table "Requirements for definition of ECU/Vehicle status in data records" It shall be possible to read the data record 0xF186, by diagnostic services specified in [Data_1] UDS Services, in all diagnostic sessions in which the service used for read the data record is supported.

### 2241 — Read Access to Build List data record
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- To support diagnostic procedures it must be possible to read out the Build List data record in all diagnostic sessions, except in programming session.
- Table "Requirements for definition of ECU/Vehicle status in data records" It shall be possible to read the data record 0xC011, by diagnostic services specified in [Data_1] UDS Services, in all diagnostic sessions in which the service used for read the data record is supported, except in programming session.

### 2242 — Read access to Car Configuration Parameter Faults data record
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- To support diagnostic procedures it must be possible to read out the Car Configuration Parameter Faults data record in all diagnostic sessions, except in programming session.
- Table "Requirements for definition of ECU/Vehicle status in data records" It shall be possible to read the data record 0xE103, by diagnostic services specified in [Data_1] UDS Services, in all diagnostic sessions in which the service used for read the data record is supported, except programming session.

### 2243 — Read access to Car Mode data record
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- To support diagnostic procedures it must be possible to read out the active Car Mode from the ECU in all diagnostic sessions, except in programming session.
- It shall be possible to read the data record 0xD134, by diagnostic services specified in reference [Data_1] UDS Services, in all diagnostic sessions in which the service used for read the data record is supported, except programming session.

### 2244 — Read access to Customer setting parameters data record
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- To support diagnostic procedures it must be possible to read out the Customer setting parameter from the ECU, independent of the diagnostic session.
- Table "Requirements for definition of ECU/Vehicle status in data records" It shall be possible to read the data record 0xDED0, by diagnostic services specified in [Data_1] UDS Services, in all diagnostic sessions in which the service used for read the data record is supported, except programming session.

### 2245 — Read Access to Diagnostic Read out #1 to #4 data record
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- To support quality tracking of the ECU It shall be possible to read the data record(s) with identifier 0xEDC0 up to 0xEDC3, by diagnostic services specified in reference [Data_1] UDS Services , in all diagnostic sessions except in programming session.

### 2246 — Read Access to ECU List data record
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- To support diagnostic procedures it must be possible to read out the ECU List data record in all diagnostic sessions, except in programming session.
- Table 4.4: Table "Requirements for definition of ECU/Vehicle status in data records" It shall be possible to read the data record 0xC010, by diagnostic services specified in [Data_1] UDS Services, in all diagnostic sessions in which the service used for read the data record is supported, except in programming session.

### 2247 — Read access to Partial Network Cluster (PNC) data record
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- To support diagnostic procedures it must be possible to read out the active Partial Network Cluster (PNC) from the ECU in all diagnostic sessions, except in programming session.
- Table "Requirements for definition of ECU/Vehicle status in data records" If the support the data identifier 0xDD0B, it shall be possible to read the data record from the ECU, by diagnostic services specified in[Data_1] UDS Services, in all diagnostic sessions in which the service used for read the data record is supported, except programming session.

### 2248 — Read access to RVDC data record
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- To support RVDC functionality in the vehicle, it must be possible to read out the RVDC data record.
- It shall be possible to read the data record 0xEA00, by diagnostic services specified in [Data_1] UDS Services and according to RVDCClient, UDS DATA, documents.

### 2249 — Read access to System adaption data record
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- To support diagnostic procedures it must be possible to read out the System adaption data from the ECU, independent of the diagnostic session.
- Table "Requirements for definition of ECU/Vehicle status in data records" It shall be possible to read the data record 0xDED1, by diagnostic services specified in [Data_1] UDS Services, in all diagnostic sessions in which the service used for read the data record is supported, except programming session.

### 2250 — Read access to Usage Mode data record
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- To support diagnostic procedures it must be possible to read out the active Usage Mode from the ECU in all diagnostic sessions, except in programming session.
- Table "Requirements for definition of ECU/Vehicle status in data records" It shall be possible to read the data record 0xDD0A, by diagnostic services specified in [Data_1] UDS Services, in all diagnostic sessions in which the service used for read the data record is supported, except programming session.

### 2251 — Read Access to Vehicle state of health data record
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- It shall be possible to read the data record(s) with identifier 0xEDC5, by diagnostic services specified in reference [Data_1] UDS Services in all diagnostic sessions except in programming session.

### 2252 — Remote Vehicle Data Collection (RVDC) data record
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- To enable readout of RVDC data record A data record with identifier 0xEA00 shall be implemented according to RVDCClient, UDS DATA, documents.
- The data record shall consist of a list of other data records that are supported by the ECU.
- The content in the data record shall be the following: Byte Description#1-2 First data record identifier supported by the ECU#3-4 Second data record identifier supported by the ECU#5-6 Third data record identifier supported by the ECU..#N-(N+1) N: th data record identifier supported by the ECUIf a data record in the list either is not supported for a specific configuration of the ECU or for some other reason does not have a correct or avaliable content, the value of the record identifier shall be replaced with 0x0000.

### 2253 — System adaption data record
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The purpose is to support the ECU replacement process at workshop Table "Requirements for definition of ECU/Vehicle status in data records" A data record with identifier 0DED1 shall be implemented if the ECU stores system adaption data.
- The data record shall only contain information of adaption data stored by the ECU.
- The data record shall be used where it is considered suitable that adaption values are transferred from an old to a new ECU in the ECU replacement process at a workshop.

### 2254 — Usage Mode data record
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Table "Requirements for definition of ECU/Vehicle status in data records" A data record with identifier 0xDD0A shall be implemented exactly as defined in reference [Data_4] Global Master Reference Database.

### 2255 — Vehicle state of health data record
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- A data record with identifier 0EDC5 shall be implemented if required by the responsible authority appointed by OEM.
- The data record shall only consist of record data that the workshop preplanning process need to supplement DTCs and DTC related data in order to identify the root cause to customer complaints.

### 2256 — Write access to Customer setting parameters data record
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- To support diagnostic procedures it must be possible to write the Customer setting parameter from the ECU, independent of the diagnostic session.
- Table: Requirements for definition of ECU/Vehicle status in data records It shall be possible to write the data record 0xDED0, by diagnostic services specified in [Data_1] UDS Services, in all diagnostic sessions in which the service used for write the data record is supported, except programming session.

### 2257 — Write access to System adaption data record
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- To support diagnostic procedures it must be possible to write the System adaption data from the ECU, independent of the diagnostic session.
- table: Requirements for definition of ECU/Vehicle status in data records It shall be possible to write the data record 0xDED1, by diagnostic services specified in [Data_1] UDS Services, in all diagnostic sessions in which the service used for write the data record is supported, except programming session.4.5.2.1.2.6 Requirements from section ECU_Vehicle identification

### 2258 — Definition of global real time data record
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on implementation of global DTC snapshot data" The ECU responsible for maintaining and distributing the real time data shall maintain a global time data record with the following range, resolution and accuracy: range 0x00000000 to 0xFFFFFFFFeresolution 1 bit = 100 msaccuracy minimum ±10 minutes/week (±0.1%)correct value not available = 0xFFFFFFFFafter the global time have reached 0xFFFFFFFFFE it shall restart from 0x00000000

### 2259 — Definition of total distance data record
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on implementation of global DTC snapshot data" The ECU responsible for maintaining and distributing the total distance data shall maintain a total distance data record with the following range, resolution and accuracy: range minimum 0x000000 to 0x0F4240.
- resolution 1 bit = 1 kmthe accuracy shall be the same as or better than the accuracy of the total distance displayed in the dash boardcorrect value not available = 0xFFFFFFFF

### 2260 — Definition of vehicle battery voltage data record
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on implementation of global DTC snapshot data" The ECU responsible for maintaining and distributing the vehicle battery voltage data shall maintain a vehicle battery voltage data record with the following range, resolution and accuracy: range minimum / 0x00 to 0x60r resolution 1 bit = 0.25 Voltthe accuracy shall be according to section Requirements for detection of low supply voltage.

### 2261 — Distribution of global DTC snapshot data
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- Section "Global DTC snapshot data" Global DTC snapshot data shall be transmitted to all public ECUs by an ECU (one or more) responsible for maintaining and distributing the data according to the following requirements:- The ECU shall transmit current values of the data periodically each second on the network except the data record 0xDD02 - "Vehicle battery voltage" which shall be sent faster according to the requirements specified in section Additional requirements for detection of low supply voltage.- The ECU shall transmit the data with a maximum age of 250 ms, except the data record 0xDD02 - "Vehicle battery voltage" which shall be sent with a lower maximim age according to the requirements specified in section Additional requirements for detection of low supply voltage.

### 2262 — Maintaining global real time after power loss
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on implementation of global DTC snapshot data" The ECU responsible for maintaining and distributing the real time data shall store the current value of global real time in long.
- If the ECU loses power supply then, following reconnection of the power supply, it shall continue to count the global real time beginning from the stored value.

### 2263 — Storage of global DTC snapshot data when not available
- 版本：v4 ｜ 验证方式：Analysis ｜ 适用：通用
- Section "Global DTC snapshot data" If global DTC snapshot data received from the vehicle network is not available when the sampling criteria is fulfilled, the latest received value shall be used and stored as DTC snapshot data.
- If no value has been received in the current operation cycle a value representing "correct value not available", according to specified in table: Requirements on implementation of global DTC snapshot data, shall be used and stored as DTC snapshot data.

### 2264 — Supported data records in global DTC snapshot data
- 版本：v10 ｜ 验证方式：Analysis ｜ 适用：通用
- To enhance fault tracing and root cause analysis specific vehicle global data shall be stored with each DTC.
- Table "Requirements on implementation of global DTC snapshot data" For all DTCs supported by the ECU the global DTC snapshot data records shall include the following data records, as defined in reference [Data_4] Global Master Reference Database and the stored data records shall be reported on request of the diagnostic services specified in reference [Data_1] UDS Services:0xDD00 Global real time.0xDD01 Total distance.0xDD02 Vehicle battery voltage.0xDD0A Usage mode.0xDD0B Partial Network Cluster (PNC).
- It shall only be included in the Global DTC snapshot data when the ECU is required to implement this DID.4.5.2.1.2.22 Requirements from section Local DTC snapshot data

### 2265 — Storage of local DTC snapshot data when not available
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- Section "Local DTC snapshot data" If local DTC snapshot data received from the vehicle network is not available when the sampling criteria is fulfilled, the latest received value shall be used and stored as DTC snapshot data.
- If no value has been received in the current operation cycle a value representing "correct value not available" shall be used and stored as DTC snapshot data.

### 2266 — Support for local DTC snapshot data
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- To enhance fault tracing and root cause analysis specific ECU local data shall be stored with each DTC.
- Table "Requirements on implementation of local DTC snapshot data" For all DTCs supported by the ECU local DTC snapshot data shall be implemented as defined by a feasibility study performed by the implementer.
- The feasibility study shall be approved by the responsible authority appointed by OEM).

### 2267 — Access development specific data records
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Table "Requirements on implementation of data records" It shall be possible to access the development specific data records (if supported by the ECU), with data identifiers in the ranges 0xE500 to 0xE5FF by diagnostic services specified in reference [Data_1] UDS Services, in all diagnostic sessions in which services used for access the data records is supported, except programming session.

### 2268 — Access Development specific data records - implementer specified
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- Table "Requirements on implementation of data records" It shall be possible to access the Development specific data records (if supported by the ECU),with data identifiers in the ranges 0xD900 to 0xDCFF, E300 to E4FF and 0xEE00 to 0xFFFF,by diagnostic services specified in reference [Data_1] UDS Services, in all diagnostic sessions except in programmingSession.

### 2269 — Access Options-System Supplier Specific data records
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- It may be possible to access the Identification Options data records, with data identifiers in the range 0xF1F0 to 0xF1FF, by diagnostic services specified in reference [Data_1] UDS Services, in all diagnostic sessions except in programmingSession.

### 2270 — Access System Supplier Specific data records
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- It may be possible to access the System Supplier Specific data records, with data identifiers in the range 0xFD00 to 0xFEFF, by diagnostic services specified in reference [Data_1] UDS Services, in all diagnostic sessions except in programmingSession.

### 2271 — Access to DTC Global Snapshot Data records
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Table "Requirements on implementation of data records" It shall be possible to access the DTC Global Snapshot Data records with data identifiers in the range 0xDD00 to 0xDD7F, by diagnostic services specified in [Data_1] UDS Services, in all diagnostic sessions in which services used for access the data records is supported, except programming session.
- external and internal signals) specified in section Global DTC snapshot data shall be defined in records with data identifiers in this range.

### 2272 — Access to ECU Identification and Configuration data records
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- Table "Requirements on implementation of data records" It shall be possible to access the ECU Identification and Configuration data records with data identifiers in the range 0xEDA0 to 0xEDFF (VCC) and 0xED20 to 0xED7F (Geely), by diagnostic services specified in [Data_1] UDS Services, in all diagnostic sessions.
- Data items specified in sections ECU/Vehicle identification shall be defined in records with data identifiers in this range.

### 2273 — Access to Identification Option - ISO specified data records
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Table "Requirements on implementation of data records" It shall be possible to access the Identification Option - ISO Specific data records, with data identifiers in the range 0xF180 to 0xF19F, by diagnostic services specified in [Data_1] UDS Services, in all diagnostic sessions.
- Data items specified in sections ECU/Vehicle status and ECU/Vehicle identification shall be defined in records with data identifiers in this range.

### 2274 — Access to Identification Option - Vehicle Manufacturer Specific data records
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Table "Requirements on implementation of data records" It shall be possible to access the Identification Option – Vehicle Manufacturer Specific data records, with data identifiers in the ranges 0xF100 to 0xF17F, and 0xF1A0 to 0xF1EF, by diagnostic services specified in [Data_1] UDS Services, in all diagnostic sessions.
- Data items specified in sections 4.1.6 shall be defined in records with data identifiers in these ranges .

### 2275 — Access to Vehicle manufacturer specific data records
- 版本：v5 ｜ 验证方式：Test ｜ 适用：通用
- Table "Requirements on implementation of data records" It shall be possible to access the vehicle manufacturer specific data records with data identifiers in the ranges 0x0100 to 0xD8FF, 0xDE00 to 0xE2FF, 0xE600 to 0xED1F, 0xED80 to0xED9F and 0xF010 to 0xF0FF, by diagnostic services specified in [Data_1] UDS Services, in all diagnostic sessions in which services used for access the data records is supported, except programming session.
- external and internal signals) specified in ECU external signals, ECU internal signals, ECU Vehicle status, Network data and Local DTC snapshot data shall be defined in records with data identifiers in this range.

### 2276 — Data types and classifications
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- To simplify implementation of data interpretation in tools all data must comply with standard definitions.
- Section "Record Data - General" All data records shall be defined according to the data types and classifications described in Appendix A.

### 2277 — Development specific data records
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- Development specific data records are not supported by OEM diagnostic tools and must be defined in a separate identifier range.
- Table "Requirements on implementation of data records" Data records needed only during the development shall be implemented with data identifiers in the range 0xE500 to 0xE5FF exactly as they are defined in [Data_4] Global Master Reference Database.

### 2278 — Development specific data records - implementer specified
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- ECU Specific data records are not supported by OEM specific tools and must be defined in a separate identifier range.
- Table "Requirements on implementation of data records" If data records that are needed only during the development of the ECU are defined by the implementer, these data records shall have data identifiers in the ranges 0xD900 to 0xDCFF, E300 to E4FF and 0xEE00 to 0xFFFF.

### 2279 — Entry conditions for diagnostic service ClearDiagnosticInformation (14)
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- 2279 v2Entry conditions for diagnostic service ClearDiagnosticInformation (14) If the ECU implement safety requirements with an ASIL higher than QM (see [Services_12] ISO 26262) it shall, in all situations when diagnostic services may violate any of those safety requirements, reject the critical diagnostic service requests.

### 2280 — Dynamically Defined Data Identifiers in ascending order
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on implementation of data records" If Dynamically defined Datalidentifier data records are implemented they shall have data identifiers in the range 0xF300 to 0xF3FF and shall use the identifiers in ascending order starting from data identifier 0xF300 (i.
- if the ECU supports only one single dynamically defined Datalidentifier then its value shall be 0xF300, if the ECU supports two dynamically defined Dataldentifiers then the values shall be 0xF300 and 0xF301, etc.).

### 2281 — Dynamically defined periodic Data Identifiers in ascending order
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- To simplify management of data identifiers in the tools Table "Requirements on implementation of data records" If Dynamically defined periodic Dataldentifier data records are implemented they shall have data identifiers in the range 0xF200 to 0xF240 and shall use the identifiers in ascending order starting from data identifier 0xF200 (i.
- if the ECU supports only one single dynamically defined periodicDataIdentifier then its value shall be 0xF200, if the ECU supports two dynamically defined periodicDataIdentifiers then the values shall be 0xF200 and 0xF201, etc.)

### 2282 — ECU Identification and Configuration data records
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on implementation of data records" ECU Identification and Configuration data records with data identifiers in the range 0xEDA0 to 0xEDFF (VCC) and 0xED20 to 0xED7F (Geely), shall be implemented exactly as they are defined in [Data_4] Global Master Reference Database.

### 2283 — Identification Option - ISO specified data records
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on implementation of data records" Identification Option – ISO specified data records with data identifiers in the range 0xF180 to 0xF19F, shall be implemented exactly as they are defined in [Data_4] Global Master Reference Database.

### 2284 — Identification Option - Vehicle Manufacturer Specific data records
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on implementation of data records" Identification Option – Vehicle Manufacturer Specific data records with data identifiers in the ranges 0xF100 to 0xF17F, and 0xF1A0 to 0xF1EF, shall be implemented exactly as they are defined in [Data_4] Global Master Reference Database.

### 2285 — Identification Options-System Supplier Specific data records
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- System supplier specific data records are not supported by OEM specific tools and must be defined in a separate identifier range.
- Table "Requirements on implementation of data records" If Identification Options data records, that are not for uesd by OEM, are defined by the system supplier, these data records shall have data identifiers in the range 0xF1F0 to 0xF1FF.

### 2286 — Specification of supported services for each data record
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- To define which services that shall be supported for each data record.
- Section "Record Data - General" Unless specified by this document, the implementer shall specify which data identifiers that the ECU supports, and for each supported data identifier, if the data record shall be possible to read, write and/or control by the services specified in [Data_1] UDS Services

### 2287 — Supported services for Dynamically Defined Data Identifiers
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on implementation of data records" If Dynamically defined Dataldentifier data records are implemented they shall be supported by services, specified by [Data_1] UDS Services, that can dynamically define a data identifier and read the dynamically defined data parameter , in all diagnostic sessions except in programmingSession .
- They shall not be supported by services that can write or control the dynamically defined data parameters.

### 2288 — Supported services for Dynamically defined periodic Data Identifiers
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on implementation of data records" If Dynamically defined periodic Dataldentifier data records are implemented they shall only be supported by services, specified by [Data_1] UDS Services, that can dynamically define a data identifier and read the dynamically defined data parameter periodically , in all diagnostic sessions except in programmingSession .
- They shall not be supported by services that can write or control the dynamically defined data parameters.

### 2289 — System Supplier Specific data records
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- System supplier specific data records are not supported by OEM specific tools and must be defined in a separate identifier range.
- Table "Requirements on implementation of data records" If data records that are not intended for use by OEM are defined by the system supplier, these data records shall have data identifiers in the range 0xFD00 to 0xFEFF.

### 2290 — Vehicle manufacturer specific data records defined in GMRDB
- 版本：v4 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on implementation of data records" Data records with data identifiers in the ranges 0x0100 to 0xD8FF, 0xDE00 to 0xE2FF,0xE600 to 0xED1F, 0xED80 to 0xED9F and 0xF010 - 0xF0FF shall be implemented exactly asthey are defined in [Data_4] Global Master Reference Database.

### 2291 — Check Complete & Compatible response time
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The Check Complete & Compatible routine must be executed quickly in order to fulfil the timing requirement of SWDL.
- Table "Requirements on P4server_max for routines" The response time P4 server_max for the Check Complete & Compatible routine shall be equal to P2 Server_max .

### 2292 — Check Memory response time
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The response time P4 server_max for the Check Memory routine shall be 2000 ms.

### 2293 — Check Programming Pre-conditions response time
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- 2293 v1Check Programming Pre-conditions response time The Check Programming Pre-conditions routine must be executed quickly in order to fulfil the timing requirement of SWDL.
- Table "Requirements on P4server_max for routines" The response time P4 server_max for the Check Programming Pre-conditions routine shall be equal to P2 Server_max .

### 2294 — Erase Memory response time
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Table "Requirements on P4server_max for routines" The response time P4 server_max for the Erase Memory routine shall be 60000 ms.

### 2295 — Extended Erase Memory response time
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- Table "Requirements on P4server_max for routines" The response time P4 server_max for the Erase Memory routine shall be increased by an additional 20s for each megabyte range of data over 1 megabyte that is requested to be erased.

### 2296 — Extended Erase Memory response time - ECU Software Structure
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Table "Requirements on P4server_max for routines" The P4 server_max for an ESS update shall be defined by the size of the total memory, e.

### 2297 — Software Installation response time
- 版本：v2 ｜ 验证方式：Test ｜ 适用：4.0.x 与 4.1+ 分别定义
- The response time for a type 2 routine shall be quickly.
- The response time P4 server_max for the Software Installation routine shall be equal to P2 Server_max.
- (The timing parameters P4 server_max and P2 Server_max are defined in reference [Data_2] UDS Session).4.5.2.1.3 Diagnostic DataDiagnostic data shall be supported by the ECU as specified by this section.

### 2298 — Access to Vehicle manufacturer specific routines
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- To support diagnostic procedures it must be possible to execute the vehicle manufacturer specific routines in all diagnostic session.
- Table "Requirements on implementation of routines" - item 1 It shall be possible to access control routines with routine identifiers in the ranges 0x0200 to 0xDBFF, and 0xFF00 to 0xFFFF, by diagnostic services specified in [Data_1] UDS Services, in the diagnostic sessions that is specified by the implementer (refer to [Data_1] UDS Services for restrictions on which diagnostic sessions the different routine types that are allowed in).

### 2299 — Development Specific routines
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Development Specific routines are not supported by OEM specific tools and must be defined in a separate identifier range.
- Table "Requirements on implementation of routines" - item 2 If routines that are needed only during the development of the ECU, or for analysis of ECUs returned to the vehicle manufacturer, are defined by the implementer, these routines shall have identifiers in the range 0xDC00 to 0xDFFF.

### 2300 — ISO specified routines
- 版本：v1 ｜ 验证方式：Inspection ｜ 适用：通用
- Routines defined by ISO that shall or may be supported Routines with routine identifiers in the ranges 0xFF00 to 0xFF02 shall be implemented as they are defined by reference IRoad vehicles – Diagnostics systems – Diagnostic services , UDS - Data - External publications .
- Routines specified in section Supported routines shall be defined with routine identifiers in these ranges.

### 2301 — System Supplier Specific routines
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- 2301 v2System Supplier Specific routines Routines needed only by the system supplier shall be defined in a separate range which may not be supported by OEM specific tools.
- Table "Requirements on implementation of routines" - item 5 If routines that are needed only by the system supplier are defined by the system supplier, these routines shall have identifiers in the range 0xF000 to 0xFEFF.
- Routines in this range shall comply with the requirements in reference [Data_50] Road vehicles – Diagnostics systems – Diagnostic services, UDS DATA External documents , but are not required to comply with requirements in reference [Data_1] UDS Services.

### 2302 — Vehicle manufacturer specific routines defined in GMRDB
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on implementation of routines" - item 1 Routines with routine identifiers in the ranges 0x0200 to 0xDBFF shall be implemented exactly as they are defined in [Data_4] Global Master Reference Database.
- Routines specified in section 4.3.2 shall be defined with routine identifiers in these ranges.

### 2303 — DTC storage time
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- The DTC information shall be stored within a maximum delay time of "DTC storage time" T1=400 ms.
- 10 or more) occur within a time period of T1 then may the "DTC storage time" be increased but only if that is approved by the responsible authority appointed by OEM.

### 2304 — Storage of DTC fault detection counters 10 and 11 in short term memory
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- I t shall be possible to store the value of the DTC fault detection counter 0x10 in short term memory for a all DTCs supported by the ECU.
- If the DTC fault detection counter 0x11 is supported by the ECU then shall it be possible to store the value of the DTC fault detection counter 0x11 in short term memory for all DTCs supported by the ECU.

### 2305 — Storage of DTC fault detection counters 12 in long term memory
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on storage of DTC information in long-term memory" I t shall be possible to store the value of the DTC fault detection counter 0x12 in long term memory for a minimum number of DTCs according to table Requirements on minimum number of DTCs for which DTC information shall be possible to store in long-term memory.

### 2306 — Storage of DTC information in short term memory
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- Section "Store DTC information" If DTC information is temporarily stored in short term memory before being stored in long term memory it shall be possible to store at least the same amount of DTC information in short term memory as in long term memory.

### 2307 — Storage of DTC operation cycle counter 5 in long term memory
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on storage of DTC information in long-term memory" If the DTC is emission related it shall be possible to store the value of the DTC operation cycle counter 5 in long term memory for a minimum number of DTCs according to table Requirements on minimum number of DTCs for which DTC information shall be possible to store in long-term memory.

### 2308 — Storage of DTC operation cycle counters 1, 2, 3, 4, 6 and 7 in long term memory
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on storage of DTC information in long-term memory" It shall be possible to store the values of the DTC operation cycle counters 1, 2, 3, 4, 6 and 7 in long term memory for a minimum number of DTCs according to table Requirements on minimum number of DTCs for which DTC information shall be possible to store in long-term memory.

### 2309 — Storage of DTC snapshot data in long term memory
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on storage of DTC information in long-term memory" It shall be possible to store the values of the DTC snapshot data defined by DTCSnapshotRecordNumber 0x20 in long term memory for a minimum number of DTCs according to table Requirements on minimum number of DTCs for which DTC information shall be possible to store in long-term memory.

### 2310 — Storage of DTC status bits no 0, 2, 3, 4 and 5 in long term memory
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on storage of DTC information in long-term memory" It shall be possible to store the values of DTC status bits no 0, 2, 3, 4, and 5 in long term memory for all DTCs supported by the ECU.

### 2311 — Storage of DTC status bits no 1, 6 and 7 in short term memory
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- It shall be possible to store the values of DTC status bits no 1, 6 and 7 in short term memory for all DTCs supported by the ECU.

### 2312 — Storage of DTC status indicator bit no 1 in short term memory
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- It shall be possible to store the value of the DTC status indicator bit no 1 defined by DTCExtendedDataRecordNumber 0x30 in short term memory for a minimum number of DTCs according to Table Requirements on minimum number of DTCs for which DTC information shall be possible to store .

### 2313 — Storage of DTC status indicator bits no 0, 2-7 in long term memory
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on storage of DTC information in long-term memory" It shall be possible to store the value of the DTC status indicator no 0, 2-7 defined by DTCExtendedDataRecordNumber 0x30 in long term memory for a minimum number of DTCs according to table Requirements on minimum number of DTCs for which DTC information shall be possible to store in long-term memory.

### 2314 — Storage of DTC time stamp in long term memory
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Requirements on storage of DTC information in long-term memory" It shall be possible to store the values of the DTC time stamp defined by DTCExtendedDataRecordNumber 0x20 and 0x21 in long term memory for a minimum number of DTCs according to table Requirements on minimum number of DTCs for which DTC information shall be possible to store in long-term memory.4.5.2.1.2.28 Requirements from section Transfer of DTC information to long term memory

### 2315 — Access to ActivateSBL routine
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- 2315 v1Access to ActivateSBL routine To support SWDL it must be possible to execute the required routine from SBL and PBL.
- Table "Requirements for implementation of routines" - item 3 It shall be possible to execute the ActivateSBL routine, by diagnostic service request specified in [Data_1] UDS Services, when the ECU is executing the primary and secondary bootloader in programming session.

### 2316 — Access to Check Complete & Compatible routine
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- To support SWDL it must be possible to execute the required routine from SBL and PBL.
- Table "Requirements for implementation of routines" - item 1 It shall be possible to execute the Check Complete & Compatible routine, by diagnostic services specified in [Data_1] UDS Services, when the ECU is executing the primary and secondary bootloader in programming session.

### 2317 — Access to Check Memory routine
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- To support SWDL it must be possible to execute the required routine from SBL and PBL.
- It shall be possible to execute the Check Memory routine, by diagnostic services specified in [Data_1] UDS Services, when the ECU is executing the primary and secondary bootloader in programming session.

### 2318 — Access to Check Programming Pre-conditions routine
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- To support SWDL it must be possible to execute the required routine before the ECU enters programme mode.
- Table "Requirements for implementation of routines" - item 2 It shall be possible to execute the Check Programming Pre-conditions routine, by diagnostic service request specified in [Data_1] UDS Services, in the default and extended diagnostic sessions.

### 2319 — Access to Erase Memory routine
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- To support SWDL it must be possible to execute the required routine from SBL.
- Table "Requirements for implementation of routines" - item 4 It shall be possible to execute the Erase Memory routine, by diagnostic service request specified in [Data_1] UDS Services, only when the ECU is executing the secondary bootloader in programming session.

### 2320 — Access to Software Installation routine
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- To support SWDL it must be possible to execute the required routine from SBL and PBL.
- It shall be possible to execute the Software installation routine, by diagnostic service request specified in reference [1], when the ECU is executing the primary and secondary bootloader in programming session.

### 2321 — Access to Software Installation routine
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The Software Installation routine shall be implemented as a type 2 routine.

### 2322 — ActivateSBL routine
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- All ECUs must support routines defined for SWDL.
- Table "Requirements for implementation of routines" - item 3 The ActivateSBL routine with routine identifier 0x0301 shall be implemented as defined in [Data_4] Global Master Reference Database.
- The routine shall be used to activate the Secondary Bootloader after it has been downloaded to volatile memory.

### 2323 — ActivateSBL routine response
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Type 1 routines shall not send a response until the routine has been completed, i.
- The final positive response message from the ActivateSBL routine shall be sent when the SBL has been activated, i.
- If the SBL is already activated at the time of the request the ECU shall respond with a positive response message with RoutineCompleted=0 (Routine is completed).

### 2324 — ActivateSBL routine type
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Table 4-30, item 3 The ActivateSBL routine shall be implemented as a type 1 routine.

### 2325 — Check Complete & Compatible routine
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- All ECUs must support routines defined for SWDL.
- Table "Requirements for implementation of routines" - item 1 The Check Complete & Compatible routine with routine identifier 0x0205 shall be implemented as defined in [Data_4] Global Master Reference Database and [Data_6] General Software Download Specification.

### 2326 — Check Complete & Compatible routine type
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Table "Requirements for implementation of routines" - item 1 The Check Complete & Compatible routine shall be implemented as a type 1 routine.

### 2327 — Check Memory routine
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- If the ECU is supporting the Software Authentication concept as defined in [Data_10] General Software Authentication, the ECU shall implement the Check Memory routine with routine identifier 0x0212 as defined in [Data_4] Global Master Reference Database and [Data_6] General Software Download specification.

### 2328 — Check Memory routine type
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The Check Memory routine shall be implemented as a type 1 routine.

### 2329 — Check Programming Pre-conditions routine
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- All ECUs must support routines defined for SWDL.
- Table "Requirements for implementation of routines" - item 2 The Check Programming Pre-conditions routine with routine identifier 0x0206 shall be implemented as defined in [Data_4] Global Master Reference Database.
- The routine shall check if the ECU, under its current operating conditions, is able to enter program mode.

### 2330 — Check Programming Pre-conditions routine type
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Table "Requirements for implementation of routines" - item 2 The Check Programming Pre-conditions routine shall be implemented as a type 1 routine.

### 2331 — Erase Memory routine
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- All ECUs must support routines defined for SWDL.
- Table "Requirements for implementation of routines" - item 4 The Erase Memory routine with routine identifier 0xFF00 shall be implemented as defined in [Data_4] Global Master Reference Database.
- The routine shall perform a non-volatile memory erase of the memory blocks defined by the memoryAddress and memorySize request parameters.

### 2332 — Erase Memory routine "already erased" detection
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Table "Requirements for implementation of routines" - item 4 If the ECU is delivered to CEVT with the complete programmable memory already erased, the routine shall include an "already erased" detection in order to reduce the overall software download time.
- SBL is downloaded and activated), the routine shall not perform any erase operation and immediately send a final positive response message with RoutineCompleted=1 (Routine is completed ).
- Once one or more bytes of the ECU programmable memory area has been programmed, the "already erased" status shall be invalidated.

### 2333 — Erase Memory routine type
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Table "Requirements for implementation of routines" - item 4 The Erase Memory routine shall be implemented as a type 1 routine.

### 2334 — Software Installation routine
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The Software Installation routine with routine identifier 0xD000 shall be implemented as defined in reference [4].
- The routine is optional and shall be used for ECUs supporting file system storage to start an installation of a downloaded data file.
- The routineContolOptionRecord has a dynamical length and shall be equal to the file system location of the ECU where the data file is stored included with the file name with extension.4.5.2.1.2.32 Requirements from section Response times

### 2335 — Transfer of DTC information to long term memory
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- Section "Transfer of DTC information to long term memory" If the ECU temporarily stores DTC information in short-term memory before storing it in long-term memory, any DTC information that has been added, deleted or changed during the operation cycle shall be transferred from short-term memory to long-term memory at the end of the operation cycle, and whenever required before it is erased from the short term memory if the erase is caused by normal vehicle operation.
- DTC information from previous operation cycle shall be retained if temporarily stores DTC information in short-term memory is lost, in the current operation cycle, due to vehicle operation that is not regarded as normal.4.5.2.1.2.29 Requirements from section Clear DTC information

### 2336 — Unique ECU address
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Of the 16 bits that is used for TA and SA bit 0-3 shall define ECU ID, bit 4-7 shall define Network ID, bit 8-11 shall define Domain ID and bit 12-15 shall define the address range and shall be set to 0x1.4.5.3.1.3.2 Physical logical address rangeEach ECU shall have one vehicle unique physical logical address assigned within the ranges ![](images/41d27ebec35e328ea8484456a0548903584072828c0b3ef8eef2936148f65608.
- The ECUs which takes the longest time to re-program shall have the lowest Domain/Network/ECU ID.
- The system architect must also make sure that a Network ID equal to 0xD is not assigned to a CAN network including emissions related ECUs (this is necessary in order to avoid possible conflicts with request messages sent from an OBD scan tool).

### 2337 — Routine result availability
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- 2337 v1Routine result availability Define how long time the route shall keep the result of the routine.
- The result of the routine shall (at least) be available, via requestRoutineResults as long as the diagnostic session is kept or until the routine is re-started.

### 2338 — Routine Type 1- Short routine, definition
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- One advantage with this routine is that it may be run in defaultSession.

### 2339 — Routine Type 1- Short routine, positive response on startRoutine
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- One advantage with this routine is that it may be run in defaultSession.
- Routine Type 1- Short routine : A positive response on startRoutine request shall be sent and only be sent in the following situations: The entry conditions have been fulfilled and the routine has been completed (and stopped).

### 2340 — RoutineInfo byte
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The positive response on the service routineControl request, regardless of sub-function, shall have the data parameter RoutineStatusRecord.
- The first byte of the data parameter RoutineStatusRecord shall be the RoutineInfo byte.
- The RoutineInfo byte shall consist of two fields where bits 7-4 defines RoutineType and bits 3-0 defines RoutineStatus.

### 2341 — RoutineStatus, RoutineAborted
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- Control routines RoutineStatus, RoutineAborted: The routine aborted before completion of all requested functionality due to any of the following reasons:1. The routine has not started due to the entry conditions are not fulfilled.2. The routine has been aborte

### 2342 — RoutineStatus, routineCompleted
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Control routines RoutineStatus, routineCompleted: The routine completed all requested functionality (successfully or not). The routine results (if any), readable via service routineControl and/or any other service, are valid.

### 2343 — RoutineStatus, RoutineExecutes
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Control routines RoutineStatus, RoutineExecutes: The routine is under execution and not yet completed (only applicable for routine type 2 and 3).4.5.3.1.2.1.8 Additional session requirements4.5.3.1.2.1.8.1 GeneralWhen the ECU transitions from any diagnostic session to another diagnostic session (including the currently active session), the ECU shall reset all active diagnostic functionality requested by diagnostic services that is not supported in the new diagnostic session or that are protected by security access.
- Note that this means that the ECU shall also reset the security level to the locked state if the ECU was previously unlocked.
- When the ECU transitions from any non-default diagnostic session to the same non-default diagnostic session, the ECU shall maintain all active diagnostic functionality requested by diagnostic services, with the exception of the functionality that are protected by security access.

### 2344 — Type 1- Short routine, sub-function requestRoutineResults
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- One advantage with this routine is that it may be run in defaultSession.
- Routine Type 1- Short routine: The sub-function requestRoutineResults may be supported.

### 2345 — Type 2- Long routine, definition
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Control routines The routine stops after a certain time when it is completed. The routine is completed before or after a positive response on startRoutine request is sent.

### 2346 — Type 2- Long routine, positive response on startRoutine
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- Type 2- Long routine : A positive response on startRoutine request shall be sent and only be sent in the following situations: The entry conditions have been fulfilled and the routine has been started or completed (and stopped).

### 2347 — Type 2- Long routine, sub-function RequestRoutineResults
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Control routines Type 2- Long routine: The sub-function RequestRoutineResults shall be supported .
- It shall be possible to read the RoutineInfo byte by RequestRoutineResults requests (after a positive response on startRoutine request has been sent) both while the routine executes and after it has been stopped (aborted or completed).

### 2348 — Type 2- Long routine, sub-function stopRoutine
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Type 2- Long routine: The sub-function stopRoutine shall be supported.
- It shall be possible to abort a routine under execution, before it is completed, by stopRoutine requests (after a positive response on startRoutine request has been sent)..

### 2349 — Type 3 - Continuous routine, definition
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Control routines Type 3 - Continuous routine: The routine is stopped by stopRoutine request. The routine don't need a certain time in order to be completed. It is completed when it is stopped by stopRoutine request.

### 2350 — Type 3 - Continuous routine, positive response on startRoutine
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Control routines Type 3 - Continuous routine: A positive response on startRoutine request shall be sent and only be sent in the following situations: The entry conditions have been fulfilled and the routine has started.

### 2351 — Type 3 - Continuous routine, sub-function RequestRoutineResults
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Control routines Type 3 - Continuous routine: The sub-function RequestRoutineResults shall be supported.
- It shall be possible to read the RoutineInfo byte by RequestRoutineResults requests both while the routine executes and after it has been stopped (aborted or completed).

### 2352 — Type 3 - Continuous routine, sub-function stopRoutine
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Control routines Type 3 - Continuous routine: The sub-function stopRoutine shall be supported.

### 2353 — Maintain active diagnostic functionality at session transitions
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- When the ECU transitions from any non-default diagnostic session to the same non-default diagnostic session, the ECU shall maintain all active diagnostic functionality requested by diagnostic services, with the exception of the functionality that are protected by security access.
- Note that written changes to non-volatile memory shall remain regardless of diagnostic session transitions.4.5.3.1.2.1.8.2 Response message data parameter sessionParameterRecordThe structure and content of the positive diagnostic response message data parameter sessionParameterRecord is defined in table SessionParameterRecord structure definition and table SessionParameterRecord content definition .
- Thus, the following specified in [Services_9] ISO 14229-1 regarding the sessionParameterRecord shall be ignored: "The content and structure of this parameter record is data-link-layer-specific and can be found in the implementation specification(s) of this part of ISO 14229".

### 2354 — Reset active diagnostic functionality at session transitions
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- When the ECU transitions from any diagnostic session to another diagnostic session (including the currently active session), the ECU shall reset all active diagnostic functionality requested by diagnostic services that is not supported in the new diagnostic session or that are protected by security access.
- The ECU shall also reset the security level to the locked state if the ECU was previously unlocked.

### 2355 — SessionParameterRecord definition
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Define SessionParameterRecord The structure and content of the positive diagnostic response message data parameter sessionParameterRecord is defined in table SessionParameterRecord structure definition and table SessionParameterRecord content definition .4.5.3.1.2.2 Response timesThe maximum response time on the diagnostic service requests supported by the ECU shall be as specified in the table below.
- For not supported diagnostic services, the ECU shall use P2 Server_max as P4 Server_max.
- If a diagnostic service is allowed to make an ECU reset the response shall be sent before performing the ECU reset.

### 2356 — Allowed diagnostic services
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Define which diagnostic services to allow. Ensures all suppliers uses the same diagnostic services as well as preventing supplier from using not allowed diagnostic services. Section "Diagnostic service requirements" The ECU is not allowed to support other diag

### 2357 — Diagnostic service specification
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- Define standardized diagnostic services, The ECU shall be compliant to [Services_9] ISO 14229-1: Road vehicles – Diagnostics systems – Diagnostic services.

### 2358 — Safety requirements
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- Implementation of diagnostics on safety related ECU must comply with ISO26262 Section "Diagnostic service requirements" If the ECU implements safety requirements with an ASIL higher than QM, it shall be ensured that the diagnostic services supported by the ECU in all sessions except in programmingSession cannot violate any of those safety requirements, i.
- Exception to this requirement is allowed only when approved by CEVT Electrical Architecture and will require that the diagnostic services are developed according to [Services_12] ISO-26262 and the allocated ASIL of those safety requirement for which independence cannot be demonstrated4.5.3.1.2.1 Supported servicesDiagnostic services shall be supported by the ECU and enabled in diagnostic sessions according to the tables in the following sub sections.
- Abbreviations in the table Requirements on diagnostic services that shall be supported by the ECU: MC1= Mandatory if the ECU is not emission related.

### 2359 — ECU ability to receive a complete message
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- The ECU shall be able to receive a complete request message, receiving a queued requestexcluded (refer to [Services_2] UDS Session for definition of queued request), without to haltthe message, while sending of it is in progress, with the help of services in lower OSI-layere.
- g network/transport layer.4.5.3.1.4 Introduction4.5.3.1.4.1 Requisite documentsThis specification shall be followed and the requirements specified in this document are notnegotiable.
- In the case of any requirement conflict between this document and any of the referenceddocuments, the proposed solution to the conflict shall be approved by CEVT ElectricalArchitecture.

### 2360 — ECU ability to receive requests
- 版本：v4 ｜ 验证方式：Analysis ｜ 适用：通用
- Define a time the ECU is allowed to be unavailable in regards of diagnostic communication when powering up and the time shall be short enough to not be a problem for manufacturing and aftersales.
- Section "ECU ability to receive requests" As long as the ECU is within an operation cycle, the ECU shall all the time be able to receive diagnostic service requests and send a response (positive or negative) on the requests.
- Refer to sectionEntry conditionsfor requirements on when the ECU shall be able to execute the received requests.

### 2361 — ECU operation cycle
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- Define a time the ECU is allowed to be unavailable in regards of diagnostic communication when powering up and the time shall be short enough to not be a problem for manufacturing and aftersales.
- Section "ECU ability to receive requests" The ECU shall start an operation cycle at the latest when the ECU has completed its start-up sequence.
- The ECU shall stop the operation cycle at the earliest when the ECU start to perform its shutdown sequence and at the latest when the ECU has completed its shutdown sequence and prior to the following ECU events:1.

### 2362 — ECU start up time
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Define a time the ECU is allowed to be unavailable in regards of diagnostic communication when powering up and the time shall be short enough to not be a problem for manufacturing and aftersales.
- Section "ECU ability to receive requests" The ECU shall complete its start-up sequence within 2500 ms after an event that initiates a start-up sequence.
- However, minimum the following events shall initiate a startup sequence:1.

### 2363 — Service clearDiagnosticInformation (14) affecting ECU functionality
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The service clearDiagnosticInformation (0x14) shall not affect the ECU's ability to execute non diagnostic tasks.

### 2366 — Service dynamicallyDefineDataIdentifier (2C) affecting ECU functionality
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The service dynamicallyDefineDataIdentifier (0x2C) shall not affect the ECU's ability to execute non diagnostic tasks.

### 2367 — Service ECUReset (11) affecting ECU functionality
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The purpose of diagnostics is to be able to monitor functionality. If the diagnostics affects the functionality, the usefulness of the diagnostics is limited. The service ECUReset (0x11) is allowed to affect the ECU's ability to execute non diagnostic tasks. T

### 2368 — Service inputOutputControlByIdentifier (2F) affecting ECU functionality
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The purpose of diagnostics is to be able to monitor functionality. If the diagnostics affects the functionality, the usefulness of the diagnostics is limited. The service inputOutputControlByIdentifier (0x2F) is allowed to affect the ECU's ability to execute n

### 2369 — Service readDataByIdentifier (22) affecting ECU functionality
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The service readDataByIdentifier (0x22) shall not affect the ECU's ability to execute non diagnostic tasks

### 2370 — Service readDataByPeriodicIdentifier (2A) affecting ECU functionality
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The service readDataByPeriodicIdentifier (0x2A) shall not affect the ECU's ability to execute non diagnostic tasks.

### 2371 — Service ReadDTCInformation (19) affecting ECU functionality
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The service ReadDTCInformation (0x19) shall not affect the ECU's ability to execute non diagnostic tasks.

### 2372 — Service readGenericInformation (AF) affecting ECU functionality
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The service readGenericInformation (0xAF) shall not affect the ECU's ability to execute non diagnostic tasks.

### 2373 — Service readMemoryByAddress (23) affecting ECU functionality
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The service readMemoryByAddress (0x23) shall not affect the ECU's ability to execute non diagnostic tasks.

### 2374 — Service routineControl (31) affecting ECU functionality
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- 4.5.3.1.2.4 Entry conditionsThe entry conditions for the diagnostic services supported by the ECU shall be kept to a minimum and are allowed or required only as specified by the table below .
- Note that this is applicable on all diagnostic service requests that the ECU receives (refer to section ECU ability to receive requests for requirements on when the ECU shall be able to receive diagnostic service requests).
- The implementer shall implement the ECU's condition for entering programmingSession based on the allocated functionality.

### 2375 — Service securityAccess (27) affecting ECU functionality
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The service securityAccess (0x27) shall not affect the ECU's ability to execute non diagnostic tasks.

### 2376 — Service testerPresent (3E) affecting ECU functionality
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The service testerPresent (0x3E) shall not affect the ECU's ability to execute non diagnostic tasks.

### 2377 — Service writeDataByIdentifier (2E) affecting ECU functionality
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The purpose of diagnostics is to be able to monitor functionality. If the diagnostics affects the functionality, the usefulness of the diagnostics is limited. The service writeDataByIdentifier (0x2E) is allowed to affect the ECU's ability to execute non diagno

### 2378 — Service writeMemoryByAddress (3D) affecting ECU functionality
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The purpose of diagnostics is to be able to monitor functionality. If the diagnostics affects the functionality, the usefulness of the diagnostics is limited. The service writeMemoryByAddress (0x3D) is allowed to affect the ECU's ability to execute non diagnos

### 2380 — Entry conditions for diagnostic service DynamicallyDefineDataIdentifier (2C)
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Entry conditions for diagnostic services shall be avoided since entry condition limits the diagnostic functionality.
- It may also be hard to both convey the information of the entry condition to the diagnostic user as well as the diagnostic user may have problems actually fulfilling the entry condition.

### 2381 — Entry conditions for diagnostic service InputOutputControlByIdentifier (2F)
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- 2381 v3Entry conditions for diagnostic service InputOutputControlByIdentifier (2F) Entry conditions for diagnostic services shall be avoided since entry condition limits the diagnostic functionality.
- It may also be hard to both convey the information of the entry condition to the diagnostic user as well as the diagnostic user may have problems actually fulfilling the entry condition.
- If the ECU implement safety requirement s with an ASIL higher than QM (see [Services_12] ISO 26262) it shall, in all situations when diagnostic services may violate any of those safety requirements, reject the critical diagnostic service requests.

### 2382 — Entry conditions for diagnostic service ReadDataByIdentifier (22)
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Entry conditions for diagnostic services shall be avoided since entry condition limits the diagnostic functionality.
- It may also be hard to both convey the information of the entry condition to the diagnostic user as well as the diagnostic user may have problems actually fulfilling the entry condition.

### 2383 — Entry conditions for diagnostic service ReadDataByPeriodicIdentifier (2A)
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Entry conditions for diagnostic services shall be avoided since entry condition limits the diagnostic functionality.
- It may also be hard to both convey the information of the entry condition to the diagnostic user as well as the diagnostic user may have problems actually fulfilling the entry condition.

### 2384 — Entry conditions for diagnostic service ReadDTCInformation (19)
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- 2384 v1Entry conditions for diagnostic service ReadDTCInformation (19) Entry conditions for diagnostic services shall be avoided since entry condition limits the diagnostic functionality.
- It may also be hard to both convey the information of the entry condition to the diagnostic user as well as the diagnostic user may have problems actually fulfilling the entry condition.

### 2385 — Entry conditions for diagnostic service ReadGenericInformation (AF)
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- 2385 v1Entry conditions for diagnostic service ReadGenericInformation (AF) Entry conditions for diagnostic services shall be avoided since entry condition limits the diagnostic functionality.
- It may also be hard to both convey the information of the entry condition to the diagnostic user as well as the diagnostic user may have problems actually fulfilling the entry condition.

### 2386 — Entry conditions for diagnostic service ReadMemoryByAddress (23)
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Entry conditions for diagnostic services shall be avoided since entry condition limits the diagnostic functionality.
- It may also be hard to both convey the information of the entry condition to the diagnostic user as well as the diagnostic user may have problems actually fulfilling the entry condition.

### 2387 — Entry conditions for diagnostic service RequestDownload (34)
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Entry conditions for diagnostic services shall be avoided since entry condition limits the diagnostic functionality.
- It may also be hard to both convey the information of the entry condition to the diagnostic user as well as the diagnostic user may have problems actually fulfilling the entry condition.

### 2388 — Entry conditions for diagnostic service RequestFileTransfer (38)
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- 2388 v1Entry conditions for diagnostic service RequestFileTransfer (38) Entry conditions for diagnostic services shall be avoided since entry condition limits the diagnostic functionality.
- It may also be hard to both convey the information of the entry condition to the diagnostic user as well as the diagnostic user may have problems actually fulfilling the entry condition.
- 4.5.3.1.2.5 Exit conditionsThe exit conditions for the diagnostic services supported by the ECU shall be kept to a minimum and are allowed only if approved by CEVT Electrical Architecture.

### 2389 — Entry conditions for diagnostic service RequestTransferExit (37)
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- 2389 v1Entry conditions for diagnostic service RequestTransferExit (37) Entry conditions for diagnostic services shall be avoided since entry condition limits the diagnostic functionality.
- It may also be hard to both convey the information of the entry condition to the diagnostic user as well as the diagnostic user may have problems actually fulfilling the entry condition.

### 2390 — Entry conditions for diagnostic service RequestUpload (35)
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Entry conditions for diagnostic services shall be avoided since entry condition limits the diagnostic functionality.
- It may also be hard to both convey the information of the entry condition to the diagnostic user as well as the diagnostic user may have problems actually fulfilling the entry condition.

### 2391 — Entry conditions for diagnostic service RoutineControl (31)
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- 2391 v3Entry conditions for diagnostic service RoutineControl (31) Entry conditions for diagnostic services shall be avoided since entry condition limits the diagnostic functionality.
- It may also be hard to both convey the information of the entry condition to the diagnostic user as well as the diagnostic user may have problems actually fulfilling the entry condition.
- If the ECU implement safety requirements with an ASIL higher than QM ([Services_12] ISO 26262) it shall, in all situations when diagnostic services may violate any of those safety requirements, reject the critical diagnostic service requests.

### 2392 — Entry conditions for diagnostic service SecurityAccess (27)
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Entry conditions for diagnostic services shall be avoided since entry condition limits the diagnostic functionality.
- It may also be hard to both convey the information of the entry condition to the diagnostic user as well as the diagnostic user may have problems actually fulfilling the entry condition.

### 2393 — Entry conditions for diagnostic service TesterPresent (3E)
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Entry conditions for diagnostic services shall be avoided since entry condition limits the diagnostic functionality.
- It may also be hard to both convey the information of the entry condition to the diagnostic user as well as the diagnostic user may have problems actually fulfilling the entry condition.

### 2394 — Entry conditions for diagnostic service TransferData (36)
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Entry conditions for diagnostic services shall be avoided since entry condition limits the diagnostic functionality.
- It may also be hard to both convey the information of the entry condition to the diagnostic user as well as the diagnostic user may have problems actually fulfilling the entry condition.

### 2395 — Entry conditions for diagnostic service WriteDataByIdentifier (2E)
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Entry conditions for diagnostic services shall be avoided since entry condition limits the diagnostic functionality.
- It may also be hard to both convey the information of the entry condition to the diagnostic user as well as the diagnostic user may have problems actually fulfilling the entry condition.
- If the ECU implement safety requirements with an ASIL higher than QM (see [Services_12] ISO 26262) it shall, in all situations when diagnostic services may violate any of those safety requirements, reject the critical diagnostic service requests.

### 2396 — Entry conditions for diagnostic service WriteMemoryByAddress (3D)
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- 2396 v2Entry conditions for diagnostic service WriteMemoryByAddress (3D) Entry conditions for diagnostic services shall be avoided since entry condition limits the diagnostic functionality.
- It may also be hard to both convey the information of the entry condition to the diagnostic user as well as the diagnostic user may have problems actually fulfilling the entry condition.
- If the ECU implement safety requirements with an ASIL higher than QM (see [Services_12] ISO 26262) it shall, in all situations when diagnostic services may violate any of those safety requirements, reject the critical diagnostic service requests.

### 2397 — Entry conditions for service ECUReset (11)
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- 2397 v2Entry conditions for service ECUReset (11) Entry conditions for diagnostic services shall be avoided since entry condition limits the diagnostic functionality.
- It may also be hard to both convey the information of the entry condition to the diagnostic user as well as the diagnostic user may have problems actually fulfilling the entry condition.
- If the ECU implement safety requirements with an ASIL higher than QM (see [Services_12] ISO 26262) it shall, in all situations when diagnostic services may violate any of those safety requirements, reject the critical diagnostic service requests.

### 2398 — Entry conditions for the service diagnosticSessionControl (10), changing to programmingSession (02)
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- Entry conditions for service diagnosticSessionControl (0x10), changing to programmingSession (0x02) (excluding programmingSession to programmingSession): The implementer shall implement the ECU's condition for entering programmingSession based on the allocated functionality.
- The condition shall ensure a defined and safe vehicle state when entering programmingSession and shall at a minimum include vehicle speed < 3km/h if not otherwise approved by CEVT Electrical Architecture.
- speed and/or "main propulsion system not active" shall the safety mechanism not prevent the ECU to change to programmingSession to allow SWDL.

### 2399 — Entry conditions for the service diagnosticSessionControl (10), other ses...
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Entry conditions for diagnostic services shall be avoided since entry condition limits the diagnostic functionality.
- It may also be hard to both convey the information of the entry condition to the diagnostic user as well as the diagnostic user may have problems actually fulfilling the entry condition.

### 2400 — Exit conditions during diagnostics services
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- 2400 v3Exit conditions during diagnostics services Exit conditions for diagnostic services shall be avoided since exit condition limits the diagnostic functionality.
- Page No1201(1572) The exit conditions for the diagnostic services supported by the ECU shall be kept to a minimum and are allowed only if approved by CEVT Electrical Architecture.4.5.3.1.2.6 Security accessThe diagnostic services supported by the ECU are allowed or required to be protected by security access only as specified in the table below.
- Note that in case of the implementer choose to protect a service that is allowed to be protected according to the table below the implementer must not protect all data that is accessible for read, write or control by the diagnostic service but just a part of it.

### 2401 — Functional addressing specific networks
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- Section "Functional logical address range" The ECU shall support the functional logical address as specified in table Functional logical address range.

### 2402 — Functional request shall be unsegmented on all networks
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- A functional request must be unsegmented on all networks.
- Section "Functional logical address range" The tester shall not send larger functional request than 6 bytes in the data field.
- The Domain ID shall represent the Domain which the ECU is logically connected to.

### 2404 — Logical address range for periodic response messages
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- The Domain ID shall represent the Domain which the ECU is logically connected to.
- The ECU shall complete its start-up sequence within 2500 ms after an event that initiates a start-up sequence.
- However, minimum the following events shall initiate a startup sequence:1.

### 2405 — Negative response code busyRepeatRequest (21)
- 版本：v4 ｜ 验证方式：Analysis ｜ 适用：通用
- Standardise the negative response codes that an ECU may send to make it easier to understand why a ECU rejects a diagnostic service request.

### 2406 — Negative response code generalReject (10)
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- Standardise the negative response codes that an ECU may send to make it easier to understand why a ECU rejects a diagnostic service request.

### 2407 — Negative response code other than generalReject (10) and busyRepeatRequest (21).
- 版本：v4 ｜ 验证方式：Analysis ｜ 适用：通用
- Standardise the negative response codes that an ECU may send to make it easier to understand why a ECU rejects a diagnostic service request.
- Document NameBase Tech SWRS DHII Figure - Typical vehicle network topologyA distributed server system shall be used where all public ECUs shall have their own server.
- All diagnostic services defined in this document shall be supported for both physical and functional addressing unless otherwise is specified in this document.

### 2408 — Allocating ECU addresses
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- The ECU address distribution method chosen shall:- make as easy gateway implementation as possible- support a method for load balancing certain types of system requests.
- The ECU shall have one vehicle unique physical logical address assigned within the ranges defined by the tablePhysical logical address range.

### 2409 — Assigning domain ID address
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- The scheduling method, for the order that SWDL shall be performed, relies on that larger (in regards of SWDL time) domains shall be programmed first.
- The method shall be vehicle platform independent.
- Domain ID's range shall be assigned based on the time it takes to make a SWDL for the specific domain.

### 2410 — Assigning ECU ID address
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- The scheduling method, for order that SWDL shall be performed, relies on that larger (in regards of SWDL time) ECU's shall be programmed first.
- The method shall be vehicle platform independent.
- ECU ID's range shall be assigned based on the time it takes to make a SWDL for the specific ECU.

### 2411 — Assigning network ID address
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- The scheduling method, for order that SWDL shall be performed, relies on that larger (in regards of SWDL time) networks shall be programmed first.
- The method shall be vehicle platform independent.
- Network ID's range shall be assigned based on the time it takes to make a SWDL for the specific network.

### 2412 — If a diagnostic service makes a reset, the response shall be sent before...
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- All ECU¿s need to follow the same sequence since failure to do so may result in different ECU¿s being in different states.
- If a diagnostic service is allowed to make a reset as specified in section Effect on the ECU operation, the response shall be sent before performing the reset.

### 2413 — Non volatile data shall be written before responding on the diagnostic request
- 版本：v4 ｜ 验证方式：Analysis ｜ 适用：通用
- Data written or cleared to an ECU shall be stored in long term memory immediately by the ECU so that it can be read out what is programmed to the ECU: s.
- If data written or cleared by a diagnostic service shall be stored in non-volatile memory, the write or clear operation to the non-volatile memory shall be completed before a positive response of the diagnostic service is sent.
- An exception to this is service clearDiagnosticInformation which shall be performed as specified by [Services_1] UDS Data.

### 2414 — P4Server_max for services not supported by the ECU
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- 2414 v1P4Server_max for services not supported by the ECU ECU shall respond swiftly even though service is not supported by the ECU since failure to do so may cause problems using functional requests with SPRMB bit set.
- For not supported diagnostic services, the ECU shall use P2 Server_max as P4 Server_max .4.5.3.1.2.3 Effect on the ECU operationThe diagnostic service's affect on the ECU operation shall be kept to a minimum and are allowed only as specified in the table below.
- The possible options are: Allowed – The service may affect the ECU's ability to execute non-diagnostic tasks.

### 2415 — P4Server_max response time for clearDiagnosticInformation (14)
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Define the time the OEM tools shall wait before assuming the diagnostic response shall be considered to have timed out.

### 2416 — P4Server_max response time for diagnosticSessionControl (10)
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Define the time the OEM tools shall wait before assuming the diagnostic response shall be considered to have timed out.

### 2417 — P4Server_max response time for dynamicallyDefineDataIdentifier (2C)
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- 2417 v1P4Server_max response time for dynamicallyDefineDataIdentifier (2C) Define the time the OEM tools shall wait before assuming the diagnostic response shall be considered to have timed out.

### 2418 — P4Server_max response time for ECURReset (11)
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Define the time the OEM tools shall wait before assuming the diagnostic response shall be considered to have timed out.

### 2419 — P4Server_max response time for inputOutputControlByIdentifier (2F)
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Define the time the OEM tools shall wait before assuming the diagnostic response shall be considered to have timed out.

### 2420 — P4Server_max response time for readDataByIdentifier (22)
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- 2420 v1P4Server_max response time for readDataByIdentifier (22) Define the time the OEM tools shall wait before assuming the diagnostic response shall be considered to have timed out.

### 2421 — P4Server_max response time for readDataByPeriodicIdentifier (2A)
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- 2421 v1P4Server_max response time for readDataByPeriodicIdentifier (2A) Define the time the OEM tools shall wait before assuming the diagnostic response shall be considered to have timed out.

### 2422 — P4Server_max response time for readDTCInformation (19)
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Define the time the OEM tools shall wait before assuming the diagnostic response shall be considered to have timed out.

### 2423 — P4Server_max response time for readGenericInformation (AF)
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Define the time the OEM tools shall wait before assuming the diagnostic response shall be considered to have timed out.

### 2424 — P4Server_max response time for readMemoryByAddress (23)
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- 2424 v1P4Server_max response time for readMemoryByAddress (23) Define the time the OEM tools shall wait before assuming the diagnostic response shall be considered to have timed out.

### 2425 — P4Server_max response time for requestDownload (34)
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Define the time the OEM tools shall wait before assuming the diagnostic response shall be considered to have timed out.

### 2426 — P4Server_max response time for requestFileTransfer (38)
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- 2426 v2P4Server_max response time for requestFileTransfer (38) Define the time the OEM tools shall wait before assuming the diagnostic response shall be considered to have timed out.

### 2427 — P4Server_max response time for requestTransferExit (37)
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- 2427 v2P4Server_max response time for requestTransferExit (37) Define the ECU performance time (P4Server) for the diagnostic response. Maximum response time for the service requestTransferExit (0x37) is 1000ms.

### 2428 — P4Server_max response time for requestUpload (35)
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Define the time the OEM tools shall wait before assuming the diagnostic response shall be considered to have timed out.

### 2429 — P4Server_max response time for routineControl (31) except for startRoutine (1), routineType = 1
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Define the time the OEM tools shall wait before assuming the diagnostic response shall be considered to have timed out.

### 2430 — P4Server_max response time for routineControl (31) startRoutine (1), rou...
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Define the time the OEM tools shall wait before assuming the diagnostic response shall be considered to have timed out.

### 2431 — P4Server_max response time for securityAccess (27)
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- 2431 v1P4Server_max response time for securityAccess (27) Define the time the OEM tools shall wait before assuming the diagnostic response shall be considered to have timed out.

### 2432 — P4Server_max response time for testerPresent (3E)
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- 2432 v1P4Server_max response time for testerPresent (3E) Define the time the OEM tools shall wait before assuming the diagnostic response shall be considered to have timed out.

### 2433 — P4Server_max response time for transferData (36)
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- 2433 v1P4Server_max response time for transferData (36) Define the time the OEM tools shall wait before assuming the diagnostic response shall be considered to have timed out.

### 2434 — P4Server_max response time for writeDataByIdentifier (2E)
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- 2434 v1P4Server_max response time for writeDataByIdentifier (2E) Define the time the OEM tools shall wait before assuming the diagnostic response shall be considered to have timed out.

### 2435 — P4Server_max response time for writeMemoryByAddress (3D)
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- 2435 v1P4Server_max response time for writeMemoryByAddress (3D) Define the time the OEM tools shall wait before assuming the diagnostic response shall be considered to have timed out.
- response shall be considered to have timed out.

### 2437 — Security access for service diagnosticSessionControl (10)
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The usage of security access to protect diagnostic services shall only be used when required and/or judged as needed.

### 2438 — Security access protection for service clearDiagnosticInformation (14)
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The usage of security access to protect diagnostic services shall only be used when required and/or judged as needed.

### 2439 — Security access protection for service dynamicallyDefineDataIdentifier (2C)
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- 2439 v2Security access protection for service dynamicallyDefineDataIdentifier (2C) The usage of security access to protect diagnostic services shall only be used when required and/or judged as needed.
- The service dynamicallyDefineDataIdentifier (0x2C) is allowed to be protected by security access only in the following situation: If data that is read by service readDataByIdentifier (0x22) or readMemoryByAddress (0x23) is protected by security access, then the service shall be protected by security access when including this same data (completely or partly) in the dynamically defined dataldentifier.

### 2440 — Security access protection for service ECUReset (11)
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The usage of security access to protect diagnostic services shall only be used when required and/or judged as needed.

### 2441 — Security access protection for service inputOutputControlByIdentifier (2F)
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- The usage of security access to protect diagnostic services shall only be used when required and/or judged as needed.

### 2442 — Security access protection for service readDataByIdentifier (22), other than system supplier specifi
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- 2442 v2Security access protection for service readDataByIdentifier (22), other than system supplier specifi The usage of security access to protect diagnostic services shall only be used when required and/or judged as needed.

### 2443 — Security access protection for service readDataByIdentifier (22), system supplier specific dataldent
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- The usage of security access to protect diagnostic services shall only be used when required and/or judged as needed.

### 2444 — Security access protection for service readDataByPeriodicIdentifier (2A)
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- 2444 v2Security access protection for service readDataByPeriodicIdentifier (2A) The usage of security access to protect diagnostic services shall only be used when required and/or judged as needed.

### 2445 — Security access protection for service readDTCInformation (19)
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The usage of security access to protect diagnostic services shall only be used when required and/or judged as needed.

### 2446 — Security access protection for service readGenericInformation (AF)
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The usage of security access to protect diagnostic services shall only be used when required and/or judged as needed.

### 2447 — Security access protection for service readMemoryByAddress (23)
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- 2447 v2Security access protection for service readMemoryByAddress (23) The usage of security access to protect diagnostic services shall only be used when required and/or judged as needed.

### 2448 — Security access protection for service requestDownload (34)
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The usage of security access to protect diagnostic services shall only be used when required and/or judged as needed.

### 2449 — Security access protection for service requestFileTransfer (38)
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The usage of security access to protect diagnostic services shall only be used when required and/or judged as needed.
- The service requestFileTransfer (0x38) is required to be protected by security access.4.5.3.1.2.7 Negative responseThe negative response codes sent by negative responses on the diagnostic services requests supported by the ECU shall be s as specified in the table below.

### 2450 — Security access protection for service requestTransferExit (37)
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The usage of security access to protect diagnostic services shall only be used when required and/or judged as needed.

### 2451 — Security access protection for service requestUpload (35)
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The usage of security access to protect diagnostic services shall only be used when required and/or judged as needed.

### 2452 — Security access protection for service routineControl (31)
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The usage of security access to protect diagnostic services shall only be used when required and/or judged as needed.

### 2453 — Security access protection for service testerPresent (3E)
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The usage of security access to protect diagnostic services shall only be used when required and/or judged as needed.

### 2454 — Security access protection for service transferData (36)
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The usage of security access to protect diagnostic services shall only be used when required and/or judged as needed.

### 2455 — Security access protection for service writeDataByIdentifier (2E)
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The usage of security access to protect diagnostic services shall only be used when required and/or judged as needed.

### 2456 — Security access protection for service writeMemoryByAddress (3D)
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The usage of security access to protect diagnostic services shall only be used when required and/or judged as needed.

### 2457 — DynamicallyDefineDataIdentifier (2C)
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The service dynamicallyDefineDataIdentifier may be supported by the ECU in defaultSession and extendedDiagnosticSession and shall not be supported in programmingSession .

### 2458 — DynamicallyDefineDataIdentifier (2C) - clear of dynamicallyDefineDataIdentifier
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The dynamically defined data records that the ECU supports shall be kept until they are cleared by the service DynamicallyDefineDataIdentifier - clearDynamicallyDefinedDataIdentifier.

### 2459 — DynamicallyDefineDataIdentifier (2C) - clearDynamicallyDefinedDataldenti...
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The service dynamicallyDefineDataIdentifier - clearDynamicallyDefinedDataIdentifier withthe data parameter dynamicallyDefinedDataIdentifier shall be supported by the ECU as specified by [Services_10] Road vehicles - End-of-life activation of on-board pyrotechnic devices - Part 1, in all sessions where the ECU supports the service dynamicallyDefineDataIdentifier.

### 2460 — DynamicallyDefineDataIdentifier (2C) - clearDynamicallyDefinedDataldenti...
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Standardised clear procedure to have compliance with OEM specific tools The service dynamicallyDefineDataIdentifier - clearDynamicallyDefinedDataIdentifier shall be supported by the ECU in all sessions where the ECU supports the service dynamicallyDefineDataIdentifier.

### 2461 — DynamicallyDefineDataIdentifier (2C) - defineByIdentifier (01, 81)
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The service dynamicallyDefineDataIdentifier - defineByIdentifier may be supported by the ECU in all sessions where the ECU supports the service dynamicallyDefineDataIdentifier.

### 2462 — DynamicallyDefineDataIdentifier (2C) - defineByIdentifier (01) - dynamic...
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The service dynamicallyDefineDataIdentifier - defineByIdentifier with the data parameter dynamicallyDefinedDataIdentifier shall be supported by the ECU in all sessions where the ECU supports the service dynamicallyDefineDataIdentifier - defineByIdentifier.

### 2463 — DynamicallyDefineDataIdentifier (2C) - defineByIdentifier (01) - memorySize
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The service dynamicallyDefineDataIdentifier - defineByIdentifier with the data parameter memorySize shall be supported by the ECU in all sessions where the ECU supports the service dynamicallyDefineDataIdentifier - defineByIdentifier.

### 2464 — DynamicallyDefineDataIdentifier (2C) - defineByIdentifier (01) - positio...
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The service dynamicallyDefineDataIdentifier - defineByIdentifier with the data parameter positionInSourceDataRecord shall be supported by the ECU in all sessions where the ECU supports the service dynamicallyDefineDataIdentifier - defineByIdentifier.

### 2465 — DynamicallyDefineDataIdentifier (2C) - defineByIdentifier (01) - sourceD...
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Compliance with OEM specific tools The service dynamicallyDefineDataIdentifier - defineByIdentifier with the data parameter sourceDataIdentifier shall be supported by the ECU in all sessions where the ECU supports the service dynamicallyDefineDataIdentifier - defineByIdentifier.

### 2466 — DynamicallyDefineDataIdentifier (2C) - defineByMemoryAddress (02) -addressAndLengthFormatIdentifier
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- DynamicThe service dynamicallyDefineDataIdentifier - defineByMemoryAddress with the data parameter addressAndLengthFormatIdentifier set to the value 0x24 may be supported by the ECU in all sessions where the ECU supports the service dynamicallyDefineDataIdentifier -defineByMemoryAddress.

### 2467 — DynamicallyDefineDataIdentifier (2C) - defineByMemoryAddress (02) -addressAndLengthFormatIdentifier
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The service dynamicallyDefineDataIdentifier - defineByMemoryAddress with the data parameter addressAndLengthFormatIdentifier set to the value 0x14 shall be supported by the ECU in all sessions where the ECU supports the service dynamicallyDefineDataIdentifier - defineByMemoryAddress.

### 2468 — DynamicallyDefineDataIdentifier (2C) - defineByMemoryAddress (02) -dynamicallyDefinedDataIdentifier
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The service dynamicallyDefineDataIdentifier - defineByMemoryAddress with the data parameter dynamicallyDefinedDataIdentifier shall be supported by the ECU in all sessions where the ECU supports the service dynamicallyDefineDataIdentifier -defineByMemoryAddress.

### 2469 — DynamicallyDefineDataIdentifier (2C) - defineByMemoryAddress (02) - memo...
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The service dynamicallyDefineDataIdentifier - defineByMemoryAddress with the data parameter memorySize shall be supported by the ECU in all sessions where the ECU supports the service dynamicallyDefineDataIdentifier - defineByMemoryAddress.
- The values of the memorySize shall be defined by the implementer.

### 2470 — DynamicallyDefineDataIdentifier (2C) - defineByMemoryAddress (02) - memo...
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Compliance with OEM specific tools The service dynamicallyDefineDataIdentifier - defineByMemoryAddress with the data parameter memoryAddress shall be supported by the ECU in all sessions where the ECU supports the service dynamicallyDefineDataIdentifier - defineByMemoryAddress.
- The values of the memoryAddress shall be defined by the implementer.

### 2471 — DynamicallyDefineDataIdentifier (2C) - defineByMemoryAddress (02, 82)
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The service dynamicallyDefineDataIdentifier - defineByMemoryAddress may be supported by the ECU in all sessions where the ECU supports the service dynamicallyDefineDataIdentifier.

### 2472 — ReadDataByIdentifier (22) - dataIdentifier(-s)
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- It shall be possible to read data from all ECUs The service readDataByIdentifier with the data parameter dataIdentifier(-s) shall be supported by the ECU in defaultSession, extendedDiagnosticSession and programmingSession, both primary and secondary bootloader.

### 2473 — ReadDataByIdentifier (22) - multiple identifiers with one request
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- Since the time for each request will be to long, the ECU shall be able to package several data record in one response message Minimum 10 dataIdentifiers, or as many dataIdentifiers as implemented, in one single ReadDataByIdentifier request shall be supported by the ECU in default and extended diagnostic session.

### 2474 — ReadDataByPeriodicIdentifier (2A)
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The service readDataByPeriodicIdentifier may be supported by the ECU in extendedDiagnosticSession and shall not be supported in defaultSession.

### 2475 — ReadDataByPeriodicIdentifier (2A) - periodicDataIdentifier
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The service readDataByPeriodicIdentifier with the data parameter periodicDataIdentifier may be supported by the ECU as specified by [Services_9] ISO 14229-1, in all sessions where the ECU supports the service readDataByPeriodicIdentifier.

### 2476 — ReadDataByPeriodicIdentifier (2A) - response message type
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Define one method to be used for all periodic identifiers Only response message type #2 is allowed. See also [Services_9] ISO 14229-1, and the implementation specification for the respective network (e. g. UDSonCAN, UDSonFR and UDSonIP) for a detailed descript

### 2477 — ReadDataByPeriodicIdentifier (2A) - transmissionMode fast (03)
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Define the transmissionMode fast The service readDataByPeriodicIdentifier with the data parameter transmissionMode set to fast may be supported by the ECU in all sessions where the ECU supports the servicereadDataByPeriodicIdentifier.
- The value of the transmission rate in the transmissionMode fast shall be defined by the implementer.
- must not be fixed, it may change over time (e.

### 2478 — ReadDataByPeriodicIdentifier (2A) - transmissionMode medium (02)
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Define the transmissionMode medium The service readDataByPeriodicIdentifier with the data parameter transmissionMode set to medium may be supported by the ECU in all sessions where the ECU supports the servicereadDataByPeriodicIdentifier.
- The value of the transmission rate in the transmissionMode medium shall be defined by the implementer.

### 2479 — ReadDataByPeriodicIdentifier (2A) - transmissionMode slow (01)
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Define the transmissionMode slow The service readDataByPeriodicIdentifier with the data parameter transmissionMode slow may be supported by the ECU in all sessions where the ECU supports the servicereadDataByPeriodicIdentifier.
- The value of the transmission rate in the transmissionMode slow shall be defined by the implementer.

### 2480 — ReadDataByPeriodicIdentifier (2A) - transmissionMode stop (04)
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Shall be possible to stop reading periodic identifiers without for example changing session since if a session change is done a lot of other functionality might reset as well.
- The service readDataByPeriodicIdentifier with the data parameter transmissionMode set to stop shall be supported by the ECU in all sessions where the ECU supports the service readDataByPeriodicIdentifier.

### 2481 — ReadMemoryByAddress (23)
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- ReadMemoryByAddress shall primarily be used during development or for validation data written by WriteMemoryByAddress.
- The readMemoryByAddress service may be supported by the ECU in defaultSession and extendedDiagnosticSession and shall not be supported in programmingSession.

### 2482 — ReadMemoryByAddress (23) - addressAndLengthFormatIdentifier (14)
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- To make it easier for tools one standardized request shall be supported by all ECUs.
- The readMemoryByAddress service with the data parameteraddressAndLengthFormatIdentifier set to a value of 0x14 shall be supported by the ECU in all sessions where the ECU supports the service readMemoryByAddress.

### 2483 — ReadMemoryByAddress (23) - addressAndLengthFormatIdentifier (24)
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Tools shall support addressAndLengthFormatIdentifier 0x24 for when there is a larger amount of data to be read (>255).
- The readMemoryByAddress service with the data parameteraddressAndLengthFormatIdentifier set to a value of 0x24 may be supported by the ECU in all sessions where the ECU supports the service readMemoryByAddress.

### 2484 — ReadMemoryByAddress (23) - memoryAddress
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The service readMemoryByAddress with the data parameter memoryAddress shall be supported by the ECU in all sessions where the ECU supports the servicereadMemoryByAddress.
- The values of the memoryAddress shall be defined by the implementer

### 2485 — ReadMemoryByAddress (23) - memorySize
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The service readMemoryByAddress with the data parameter memorySize shall be supported by the ECU in all sessions where the ECU supports the service readMemoryByAddress.
- The values of the memorySize shall be defined by the implementer.

### 2486 — WriteDataByIdentifier (2E)
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- The service WriteDataByIdentifier shall be supported if [Services_1] UDS Data specifies that the value of a data record, pointed out by a dataldentifier, shall be possible to write (by diagnostic service specified by this document).
- Otherwise, the service WriteDataByIdentifier may be supported by the ECU in one, some or all sessions.
- When in programming session WriteDataByIdentifier shall only be supported in the secondary bootloader.

### 2487 — WriteDataByIdentifier (2E) - dataldentifier
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The service WriteDataByIdentifier with the data parameter dataIdentifier(-s) shall be supported by the ECU in all sessions where the ECU supports the service WriteDataByIdentifier.

### 2488 — WriteDataByIdentifier (2E) - dataRecord
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The service WriteDataByIdentifier with the data parameter dataRecord shall be supported by the ECU in all sessions where the ECU supports the service WriteDataByIdentifier.

### 2489 — WriteMemoryByAddress (3D)
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The service WriteMemoryByAddress may be useful during the development process.
- The service WriteDataByAddress may be supported by the ECU in defaultSession and extendedDiagnosticSession but not in the programmingSession.

### 2490 — WriteMemoryByAddress (3D) - addressAndLengthFormatIdentifier (14)
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The service WriteMemoryByAddress with the data parameter addressAndLengthFormatIdentifier set to the value 0x14 shall be supported by the ECU in all sessions where the ECU supports the service WriteMemoryByAddress.

### 2491 — WriteMemoryByAddress (3D) - addressAndLengthFormatIdentifier (24)
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- OEM specific tooling shall support addressAndLengthFormatIdentifier 0x24 for when there is a larger amount of data to write (>255).
- The service WriteMemoryByAddress with the data parameteraddressAndLengthFormatIdentifier set to the value 0x24 may be supported by the ECU in all sessions where the ECU supports the service WriteMemoryByAddress.

### 2492 — WriteMemoryByAddress (3D) - dataRecord
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The service writeMemoryByAddress with the data parameter dataRecord shall be supported by the ECU in all sessions where the ECU supports the service writeMemoryByAddress.
- The values of the dataRecord shall be defined by the implementer.4.5.3.1.2.1.3 Stored Data Transmission Functional Unit Index Session Sub-function Data parameters Session Notes Name Hex Name Hex Name Hex Default Extended Diagnostic Programmings Stored Data Transmission Functional Unit 50 ClearDiagnosticIacrmation 14 M M D 51 N/A N/A groupOfDTC-Specific DTC Any 3 byte MC1 MC1 D 52 groupOfDTC-AIDTCs in emission related ECU FFF000 MC2 MC2 D 53 groupeOfDTC-AllGroups FFFFFF M M D 54 ReadDTCInformation 19 19 M M D 55 reportDTCByStatusMask 02, 82 M M D 56 DTCStatusMask See note 15 M M D 57 reportDTCSnapshotIdentification 03, 83 N/A N/A M M D 58 reportDTCSnapshotRecordBy-DTCNumber 04, 84 M M D 59 DTCMaskRecord See note 14 M M D 60 DTCSnapSnotRecordNumber FF (=all) M M D 61 Specific valueSee note 14 M M D 62 reportGenericExtendedDataRecordBy-DTCNumber 06, 86 M M D 63 DTCMaskRecord See note 14 M M D 64 DTCExtendedDataRecordNumber FF (=all) M M D 65 Specific valueSee note 14 M M D 66 reportSupportedDTC 0A,8A N/A N/A O O D 67 reportDTCWithPermanentStatus 15, 95 N/A N/A MC5 MC5 D N ReadGenencInformation AF O O D 69 reportGenericSnapshotByDTCNumber 04, 84 M M D 70 DTCMaskRecord FFFFFF (=all) M M D 71 M M D 72 DTCSnapshotRecordNumber FF (=all) M M D 73 Specific value M M D 74 reportGenericExtendedDataBy-DTCNumber 06, 86 M M D 75 DTCMaskRecord FFFFFF (=all) M M D 76 Specific valueSee note 14 M M D 17 DTCExtendedDataRecordNumber FF (=all)Specrbc value M M D 78 Specific valueSee note 14 M M D Page No1137(1572) Notes:11.
- If the ECU is emission related, the groupOfDTC set to “All Groups” or “All DTCs in emission related ECU” shall be supported by the ECU only for functional addressed diagnostic request messages.

### 2493 — WriteMemoryByAddress (3D) - memoryAddress
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The service writeMemoryByAddress with the data parameter memoryAddress shall be supported by the ECU in all sessions where the ECU supports the servicewriteMemoryByAddress.
- The values of the memoryAddress shall be defined by the implementer.

### 2494 — WriteMemoryByAddress (3D) - memorySize
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The service writeMemoryByAddress with the data parameter memorySize shall be supported by the ECU in all sessions where the ECU supports the service writeMemoryByAddress.
- The values of the memorySize shall be defined by the implementer.

### 2495 — DiagnosticSessionControl (10)
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The service diagnosticSessionControl shall be supported by the ECU in defaultSession, extendedDiagnosticSession and programmingSession, both primary and secondary bootloader.

### 2496 — DiagnosticSessionControl (10) defaultSession (01, 81)
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The ECU shall support a method in which the tester can make the ECU revert back to default session.
- The service diagnosticSessionControl – defaultSession shall be supported by the ECU in defaultSession, extendedDiagnosticSession and programmingSession, both primary and secondary bootloader.

### 2497 — DiagnosticSessionControl (10) extendedDiagnosticSession (03, 83)
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- ExtendedDiagnosticSession shall be supported since not all services used by the service tools can be performed from defaultSession.
- The service diagnosticSessionControl – extendedDiagnosticSession shall be supported by the ECU in the defaultSession and the extendedDiagnosticSession and shall not be supported in the programmingSession.

### 2498 — DiagnosticSessionControl (10) programmingSession (02, 82)
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- It shall be possible to re-program any ECU on the public network.
- The service diagnosticSessionControl – programmingSession shall be supported by the ECU in defaultSession, extendedDiagnosticSession and programmingSession, both primary and secondary bootloader.

### 2499 — DiagnosticSessionControl (10) - sessionParameterRecord
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- All ECUs shall always use a common P2 time to make timeout handling easier on the client side The ECU shall not use the service diagnosticSessionControl to alter the values of P2 Server_max and P2* Server_max from the values specified in [Services_2] UDS Session.
- The response message data parameter sessionParameterRecord shall always contain these fixed values when the defaultSession, extendedDiagnosticSession or programmingSession is requested.

### 2500 — ECUReset (11)
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- ECU reset is used in the SWDL process and may be useful when testing an ECU.
- The service ECUReset shall be supported by the ECU in the programmingSession, both primary and secondary bootloader and in the default and the extended session.

### 2501 — ECUReset (11) - hardReset (01, 81)
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The service ECUReset – hardReset shall be supported by the ECU in all sessions where theECU supports the service ECUReset.

### 2502 — SecurityAccess (27)
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The service SecurityAccess service shall be supported by the ECU in theprogrammingSession, both primary and secondary bootloader and may be supported in theextendedDiagnosticSession and shall not be supported in the defaultSession.

### 2503 — SecurityAccess (27) - requestSeed (01, 81)
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- 2503 v2SecurityAccess (27) - requestSeed (01, 81) programmingSession shall be protected by SecurityAccess The service securityAccess – requestSeed 0x01 shall be supported by the ECU in the programmingSession, both primary and secondary bootloader and shall not be supported by the other sessions.

### 2504 — SecurityAccess (27) - requestSeed (03-1F, 83-9F)
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- 2504 v1SecurityAccess (27) - requestSeed (03-1F, 83-9F) Some common diagnostic procedures (for example I/O control) shall be protected with SecurityAccess and shall be possible to unlock via OEM specific tools.
- The service securityAccess – requestSeed in the range 0x03-0x1F may be supported by the ECU in the extendedDiagnosticSession and shall not be supported in the other sessions.

### 2505 — SecurityAccess (27) - requestSeed (21-3F, A1-BF)
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- ECU specific SecurityAccess algorithms may be used but shall be placed in a separate key/seed range to prevent confusion with the general SecurityAccess algorithm.
- The service securityAccess – requestSeed in the range 0x21-0x3F may be supported by the ECU in the extendedDiagnosticSession and shall not be supported in the other sessions.

### 2506 — SecurityAccess (27) - securityAccess algorithm and constant in the lowerrequestSeed range
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- There shall be an ECU independent method in unlocking the commondiagnostic procedures.
- The requestSeed range 0x01-0x1F, 0x83-0x9F and corresponding sendKey range 0x02-0x20,0x84-0xA0 shall use the OEM standardized SecurityAccess algorithm sp ecified in reference[Services_3] Security access algorithm.

### 2507 — SecurityAccess (27) - securityAccess algorithm and constant in the higherrequestSeed range
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- The implementer shall have an ECU dependent method in unlocking thecommon diagnostic procedures The requestSeed range 0x21-0x3F, 0xA1-0xBF and corresponding sendKey range 0x22-0x40, 0xA2-0xC0 shall use a SecurityAccess algorithm that is provided by the implementer.

### 2508 — SecurityAccess (27) - sendKey (02, 82)
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- programmingSession shall be protected by SecurityAccess The service securityAccess – sendKey 02 shall be supported by the ECU in the programmingSession and shall not be supported by the other sessions.
- The data parameter securityKey shall consist of three bytes.

### 2509 — SecurityAccess (27) - sendKey (04-20, 84-A0)
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Some common diagnostic procedures (for example I/O control) shall be protected with SecurityAccess and shall be possible to unlock via OEM specific tools.
- The service securityAccess – sendKey in the range 0x04-0x20 may be supported by the ECU in the extendedDiagnosticSession and shall not be supported in the other sessions.
- The data parameter securityKey shall consist of three bytes.

### 2510 — SecurityAccess (27) - sendKey (22-40, A2-C0)
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- ECU specific SecurityAccess algorithms may be used but shall be placed in a separate key/seed range to prevent confusion with the general SecurityAccess algorithm.
- The service securityAccess – sendKey in the range 0x22-0x40 may be supported by the ECU in the extendedDiagnosticSession and shall not be supported in the other sessions.

### 2511 — SecurityAccess (27) - valid seed
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Whenever the ECU has responded with a seed on a requestSeed request, the seed shall be valid until:- Any new securityAccess request is received except when the new request has a sub-function that is not supported by the ECU and, of course, a valid request with sub-function sendKey which first unlocks the SecurityAccess level and then invalidates the seed.- ECU session transition regardless if it is to the same or another session.

### 2512 — TesterPresent (3E) - zeroSubFunction (00, 80)
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Although TesterPresent is not necessary for keeping an ECU in defaultSession, all ECUs shall support TesterPresent in default session since the response of the TesterPresent can be used as an indication of an operational ECU.
- The service testerPresent – zeroSubFunction shall be supported by the ECU in defaultSession, extendedDiagnosticSession and programmingSession, both primary and secondary bootloader.
- Minimum 10 dataIdentifiers, or as many dataIdentifiers as implemented, in one single ReadDataByIdentifier request shall be supported by the ECU in default and extended diagnostic session.

### 2513 — InputOutputControlByIdentifier (2F)
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The service InputOutputControlByIdentifier shall be supported by the ECU in extendedDiagnosticSession if [Services_1] UDS Data specifies that the value of a data record, pointed out by a dataldentifier, shall be possible to controllable by the service InputOutputControlByIdentifier.
- Otherwise the service InputOutputControlByIdentifier may be supported in extendedDiagnosticSession.
- The service InputOutputControlByIdentifier shall not be supported by the ECU in defaultSession or programmingSession.

### 2514 — InputOutputControlByIdentifier (2F) - Consecutive shortTermAdjustment re...
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Control outputs The ECU shall support several consecutive shortTermAdjustment requests without any returnControlToECU (0x00) requests in between.

### 2515 — InputOutputControlByIdentifier (2F) - controlMask
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- The service InputOutputControlByIdentifier with data parameter controlMask shall be supported by the ECU as specified in [Services_9] ISO 14229-1 if the dataRecord consists of more than one parameter (i.

### 2516 — InputOutputControlByIdentifier (2F) - ControlMask bit values of returnCo...
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Control outputs The ECU shall accept a correct returnControlToECU (0x00) request regardless of the value of the controlMask bits (0 or 1).

### 2517 — InputOutputControlByIdentifier (2F) - controlState data record
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- The service InputOutputControlByIdentifier with data parameter controlState set to dataRecord shall be supported by the ECU in all sessions where the ECU supports the service InputOutputControlByIdentifier.

### 2518 — InputOutputControlByIdentifier (2F) - controlState parameter of the posi...
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The controlState parameter (of the controlStatusRecord) of positive response messages shall always be equal to the size of the dataRecord (referenced by the dataldentifier) and shall represent the actual current value(s) for each parameter within the dataldentifier, independent of the value of the controlMask (i.
- Note that whether or not the ECU shall support a specific sub-function depends on the routine type and is specified by section Additional routine requirements.14.

### 2519 — InputOutputControlByIdentifier (2F) - dataldentifier
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The service InputOutputControlByIdentifier with data parameter dataldentifier shall be supported by the ECU in all sessions where the ECU s upports the service InputOutputControlByIdentifier.

### 2520 — InputOutputControlByIdentifier (2F) - inputOutputControlParameterfreezeCurrentState (02)
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The service InputOutputControlByIdentifier with data parameter inputOutputControlParameter set to freezeCurrentState may be supported by the ECU in all sessions where the ECU supports the service InputOutputControlByIdentifier.

### 2521 — InputOutputControlByIdentifier (2F) - inputOutputControlParameterreturnControlToECU (00)
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The service InputOutputControlByIdentifier with data parameter inputOutputControlParameter set to returnControlToECU shall be supported by the ECU in all sessions where the ECU supports the service InputOutputControlByIdentifier.

### 2522 — InputOutputControlByIdentifier (2F) - inputOutputControlParameter shortTermAdjustment (03)
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The service InputOutputControlByIdentifier with data parameter shortTermAdjustment shall be supported by the ECU in all sessions where the ECU supports the service InputOutputControlByIdentifier.

### 2523 — InputOutputControlByIdentifier (2F) - Static substituted values
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- From the time the request is received by the ECU until the ECU regains control, the substituted values of the data record (referenced by the dataIdentifier) shall remain static.

### 2524 — InputOutputControlByIdentifier (2F) - Temporarily controlling
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Unlike service writeDataByIdentifier (0x2E) and writeMemoryByAddress (0x3D), the values substituted by the service 0x2F shall always be immediately effective and revert back to the normal value (as determined by the control system) when the ECU regains control over the values.

### 2525 — RoutineControl (31)
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The service RoutineControl shall be supported by the ECU in defaultSession,extendedDiagnosticSession and programmingSession, both primary and secondary bootloader.

### 2526 — RoutineControl (31) - RoutineControlType requestRoutineResults (03)
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The service RoutineControl with the sub-function RoutineControlType set torequestRoutineResults shall be supported by the ECU as specified in section Additional routinerquirements in all sessions where the ECU supports the service RoutineControl.

### 2527 — RoutineControl (31) - RoutineControlType requestRoutineResults (03) - ro...
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The service RoutineControl with the sub-function RoutineControlType set torequestRoutineResults and with the data identifier routineldentifier shall be supported by theECU in all sessions where the ECU support the service with the sub-functionRoutineControlType set to requestRoutineResults.
- If an ECU receives a transferData request during an active download sequence with the same blockSequenceCounter as the last accepted transferData request, it shall respond with a positive response without writing the data once again to its memory.10.
- The transferResponseParameterRecord shall contain a checksum calculated on all data bytes written to the non-volatile memory defined by the diagnostic services RequestDownload, RequestUpload or RequestFileTransfer.

### 2528 — RoutineControl (31) - RoutineControlType startRoutine -routineControlOptionRecord
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The service RoutineControl with the sub-function RoutineControlType set to startRoutine and with the data identifier routineControlOptionRecord may be supported by the ECU in all sessions where the ECU support the service RoutineControl with the sub-function RoutineControlType set to startRoutine.

### 2529 — RoutineControl (31) - RoutineControlType startRoutine (01)
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The service RoutineControl with the sub-function RoutineControlType set to startRoutine shallbe supported by the ECU in all sessions where the ECU supports the service RoutineControl.

### 2530 — RoutineControl (31) - RoutineControlType startRoutine (01) - routinelden...
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The service RoutineControl with the sub-function RoutineControlType set to startRoutine andwith the data identifier routineldentifier shall be supported by the ECU in all sessions where theECU support the service with the sub-function RoutineControlType set to startRoutine.

### 2531 — RoutineControl (31) - RoutineControlType stopRoutine (02)
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The service RoutineControl with the sub-function RoutineControlType set to stopRoutine shall be supported by the ECU as specified in section Additional routine requirements in all sessions where the ECU supports the service RoutineControl.

### 2532 — RoutineControl (31) - RoutineControlType stopRoutine (02) -routineControlOptionRecord
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The service RoutineControl with the sub-function RoutineControlType set to stopRoutine and with the data identifier routineControlOptionRecord may be supported by the ECU in all sessions where the ECU support the service RoutineControl with the sub-function RoutineControlType set to stopRoutine.

### 2533 — RoutineControl (31) - RoutineControlType stopRoutine (02) - routineldent...
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The service RoutineControl with the sub-function RoutineControlType set to stopRoutine and with the data identifier routinelidentifier shall be supported by the ECU in all sessions where the ECU support the service with the sub-function RoutineControlType set to stopRoutine.

### 2534 — ClearDiagnosticInformation (14)
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Erase DTCs The service ClearDiagnosticInformation shall be supported by the ECU in defaultSession and extendedDiagnosticSession.

### 2535 — ClearDiagnosticInformation (14) - groupOfDTC All DTCs in emission related ECU
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- 2535 v1ClearDiagnosticInformation (14) - groupOfDTC All DTCs in emission related ECU To shorten the time the ECU is in the workshop or during the assembly process, it shall be possible to clear all DTCs in emission related ECUs with one diagnostic request.
- If the ECU is emission related, the service ClearDiagnosticInformation with the data parameter groupOfDTC set to the value 0xFFF000 – “All DTCs in emission related ECU” shall be supported by the ECU in all sessions where the ECU supports the service ClearDiagnosticInformation but only for functional addressed diagnostic request messages.
- Note that the requirement “The server shall support its list of diagnostic services regardless of addressing mode (physical, functional addressing type)” specified in [Services_9] ISO 14229-1, shall not apply in this case.

### 2536 — ClearDiagnosticInformation (14) - groupOfDTC All Groups
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- 2536 v2ClearDiagnosticInformation (14) - groupOfDTC All Groups To shorten the time the ECU is in the workshop or during the assembly process, it shall be possible to clear all DTCs with one diagnostic request.
- If the ECU is not emission related, the service ClearDiagnosticInformation with the data parameter groupOfDTC set to All Groups shall be supported by the ECU in all sessions where the ECU supports the service ClearDiagnosticInformation.
- If the ECU is emission related, the service ClearDiagnosticInformation with the data parameter groupOfDTC set to All Groups shall be supported by the ECU in all sessions where the ECU supports the service ClearDiagnosticInformation but only for functional addressed diagnostic request messages.

### 2537 — ClearDiagnosticInformation (14) - groupOfDTCSpecific DTC
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- It shall be possible to remove specific DTCs.
- If the ECU is not emission related, the service ClearDiagnosticInformation with the data parameter groupOfDTC set to a value of any specific DTC shall be supported by the ECU in all sessions where the ECU supports the service ClearDiagnosticInformation.
- If the ECU is emission related, the service ClearDiagnosticInformation with the data parameter groupOfDTC set to a value of a “calibration DTC” shall be supported by the ECU in all sessions where the ECU supports the service ClearDiagnosticInformation.

### 2538 — Data to be reported in ReadGenericInformation positive response
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The amount of data that can be reported in a positive response to the service ReadGenericInformation must be limited to what is relevant to report.
- A positive response to a request for the service ReadGenericInformation shall only report data from the DTCs for which DTC event data is stored in long-term memory according to [Services_1] UDS Data.

### 2539 — Definition of ReadGenericInformation positive response message data para...
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The service ReadGenericInformation uses additional response message data parameters which are not defined by ISO and must therefore be clearly defined in this specification.
- The ReadGenericInformation positive response message data parameter DTCStatusIndicators shall be a one byte parameter with the same definition as for the DTCExtendedDataRecordNumber 0x30 defined in [Services_1] UDS Data.

### 2540 — Definitions of ReadGenericInformation sub-function and data parameters
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The definitions of the request message sub-function and data parameters for the service AF are not defined by ISO and must therefore be clearly defined by this specification.
- The ECU shall accept request message sub-function and data parameters for the service ReadGenericInformation that are defined according to the same definitions as for the service ReadDTCInformation, as defined in [Services_9] ISO 14229-1, with the following addition for the data parameter DTCMaskRecord: If this data parameter equals 0xFFFFF, the request concerns all DTC's, and data shall be reported for all DTC's, for which data is available, in the positive response.

### 2541 — Format of ReadGenericInformation request message
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The request message format for the service AF is not defined by ISO and must therefore be clearly defined by this specification.
- The ECU shall accept request messages for the service ReadGenericInformation that uses the same format as for the service ReadDTCInformation, based on the corresponding sub-function parameter used, as defined in [Services_9] ISO 14229-1.

### 2542 — ReadDTCInformation (19)
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The service ReadDTCInformation shall be supported by the ECU in defaultSession and extendedDiagnosticSession.

### 2543 — ReadDTCInformation (19) - reportDTCByStatusMask (02, 82)
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- It shall be possible to read out DTCs with a specific status.
- The service ReadDTCInformation - reportDTCByStatusMask shall be supported by the ECU in defaultSession and extendedDiagnosticSession.

### 2544 — ReadDTCInformation (19) - reportDTCByStatusMask (02, 82) - DTCStatusMask
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The service ReadDTCInformation - reportDTCByStatusMask with the data parameter DTCStatusMask shall be supported by the ECU in defaultSession and extendedDiagnosticSession.

### 2545 — ReadDTCInformation (19) - reportDTCExtendedDataRecordByDTCNumber (06, 84)
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Extended data, consisting of extended status information, shall be stored along with the DTC.
- The extended data identified at the time of request shall be possible to read out.
- The service ReadDTCInformation - reportDTCExtendedDataRecordByDTCNumber shall be supported by the ECU in defaultSession and extendedDiagnosticSession.

### 2546 — ReadDTCInformation (19) - reportDTCExtendedDataRecordByDTCNumber (06, 86...
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The service ReadDTCInformation - reportDTCExtendedDataRecordByDTCNumber with the data parameter DTCMaskRecord shall be supported by the ECU in defaultSession and extendedDiagnosticSession.

### 2547 — ReadDTCInformation (19) - reportDTCExtendedDataRecordByDTCNumber (06, 86...
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The service ReadDTCInformation - reportDTCExtendedDataRecordByDTCNumber with the data parameter DTCExtendedDataRecordNumber set to 'All' shall be supported by the ECU in defaultSession and extendedDiagnosticSession.

### 2548 — ReadDTCInformation (19) - reportDTCExtendedDataRecordByDTCNumber (06, 86...
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The service ReadDTCInformation - reportDTCExtendedDataRecordByDTCNumber with the data parameter DTCExtendedDataRecordNumber set to a specific value shall be supported by the ECU in defaultSession and extendedDiagnosticSession.

### 2549 — ReadDTCInformation (19) - reportDTCSnapshotIdentification 03, 83)
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Since it's possible to have multiple DTCSnapshot records for one DTC, it must be possible to read out which DTCSnapshot records a specific DTC has.
- The service ReadDTCInformation - reportDTCSnapshotIdentification shall be supported by the ECU in defaultSession and extendedDiagnosticSession.

### 2550 — ReadDTCInformation (19) - reportDTCSnapshotRecordByDTCNumber (04, 84)
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Snapshot of data values shall be stored along with the DTC when snapshot sampling criteria is fulfilled.
- This snapshot data shall be possible to read out.
- The service ReadDTCInformation - reportDTCSnapshotRecordByDTCNumber shall be supported by the ECU in defaultSession and extendedDiagnosticSession.

### 2551 — ReadDTCInformation (19) - reportDTCSnapshotRecordByDTCNumber (04, 84) - ...
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The service ReadDTCInformation - reportDTCSnapshotRecordByDTCNumber with the data parameter DTCMaskRecord shall be supported by the ECU in defaultSession and extendedDiagnosticSession.

### 2552 — ReadDTCInformation (19) - reportDTCSnapshotRecordByDTCNumber (04, 84) - ...
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The service ReadDTCInformation - reportDTCSnapshotRecordByDTCNumber with the data parameter DTCSnapShotRecordNumber set to Specific value shall be supported by the ECU in defaultSession and extendedDiagnosticSession.

### 2553 — ReadDTCInformation (19) - reportDTCSnapshotRecordByDTCNumber (04, 84)- D...
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The service ReadDTCInformation - reportDTCSnapshotRecordByDTCNumber with the data parameter DTCSnapshotRecordNumber set to All shall be supported by the ECU in defaultSession and extendedDiagnosticSession.

### 2554 — ReadDTCInformation (19) - reportDTCWithPermanentStatus (15)
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- If the ECU is emission related and support permanent DTCs, the service ReadDTCInformation – reportDTCWithPermanentStatus shall be supported by the ECU in defaultSession and extendedDiagnosticSession.

### 2555 — ReadDTCInformation (19) - reportSupportedDTC (0A)
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Read out supported DTCs from an ECU The service ReadDTCInformation - reportSupportedDTC may be supported by the ECU in defaultSession and extendedDiagnosticSession.

### 2556 — ReadGenericInformation (AF)
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The service ReadGenericInformation may be supported by the ECU in defaultSession and/or extendedDiagnosticSession.

### 2557 — ReadGenericInformation (AF) - reportDTCSnapshotByDTCNumber (04, 84)
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Snapshot of data values shall be stored along with the DTC when snapshot sampling criteria is fulfilled.
- This snapshot data shall be possible to read out.
- If the service ReadGenericInformation is supported by the ECU, the subfunction reportGenericSnapshotByDTCNumber shall be supported by by the ECU in defaultSession and extendedDiagnosticSession.

### 2558 — ReadGenericInformation (AF) - reportDTCSnapshotByDTCNumber (04, 84) - DT...
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The data parameter DTCMaskRecord for the service/subfunction ReadGenericInformation - reportDTCSnapshotRecordByDTCNumber shall be supported by the ECU in defaultSession and extendedDiagnosticSession.

### 2559 — ReadGenericInformation (AF) - reportDTCSnapshotByDTCNumber (04, 84) - DT...
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The data parameter DTCSnapshotRecordNumber for the service/subfunction ReadGenericInformation - reportDTCSnapshotRecordByDTCNumber shall be supported by the ECU in defaultSession and extendedDiagnosticSession.

### 2560 — ReadGenericInformation (AF) - reportGenericExtendedDataByDTCNumber (06, ...
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The data parameter DTCMaskRecord for the service/subfunction ReadGenericInformation - reportGenericExtendedDataByDTCNumber shall be supported by the ECU in defaultSession and extendedDiagnosticSession.

### 2561 — ReadGenericInformation (AF) - reportGenericExtendedDataByDTCNumber (06, ...
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The data parameter DTCExtendedDataRecordNumber for the service/subfunction ReadGenericInformation - reportGenericExtendedDataByDTCNumber shall be supported by the ECU in defaultSession and extendedDiagnosticSession.

### 2562 — ReadGenericInformation (AF) - reportGenericExtendedDataByDTCNumber (06, 86)
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Extended data, consisting of extended status information, shall be stored along with the DTC.
- The extended data identified at the time of request shall be possible to read out.
- If the service ReadGenericInformation is supported by the ECU, the subfunction reportGenericExtendedDataByDTCNumber shall be supported by the ECU in defaultSession and extendedDiagnosticSession.

### 2563 — ReadGenericInformation negative response code conditionsNotCorrect
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- The negative response codes that must be supported for the service AF are not defined by ISO and must therefore be clearly defined by this specification If the ECU has received a request message for the service ReadGenericInformation where DTCMaskRecord = 0xFFFFF and no DTC event data has been stored for any DTC orDTCMaskRecord = a supported DTC number and no DTC event data has been stored for this DTC,the ECU shall send a negative response with response code 0x22 - conditionsNotCorrect

### 2564 — ReadGenericInformation negative response codeincorrectMessageLengthOrInvalidFormat
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The negative response codes that must be supported for the service AF are not defined by ISO and must therefore be clearly defined by this specification.
- If the ECU has received a request message for the service ReadGenericInformation where the length and/or format of the request message is incorrect the ECU shall send a negative response with response code 0x13 - incorrectMessageLengthOrInvalidFormat.

### 2565 — ReadGenericInformation negative response code order of priority
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The negative response codes that must be supported for the service AF are not defined by ISO and must therefore be clearly defined by this specification.
- If the criteria for sending a negative response to a request for the serviceReadGenericInformation is fulfilled for more than one negative response code the ECU shall send only one negative response with the response code with the highest priority according to the following priority order (highest priority first): 0x12, 0x13, 0x31, 0x22, 0x78.

### 2566 — ReadGenericInformation negative response code requestCorrectlyReceived-ResponsePending
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The negative response codes that must be supported for the service AF are not defined by ISO and must therefore be clearly defined by this specification.

### 2567 — ReadGenericInformation negative response code requestOutOfRange
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The negative response codes that must be supported for the service AF are not defined by ISO and must therefore be clearly defined by this specification.
- If the ECU has received a request message for the service ReadGenericInformation where DTCMaskRecord is different from 0xFFFFF and different from a supported DTC numberorthe sub-function is 0x04 and DTCSnapshotRecord is different from 0x FF and different from a supported DTCSnapshotRecordNumberorthe sub-function is 0x06 and DTCExtendedDataRecord is different from 0x FF and different from a supported DTCExtendedDataRecordNumberthe ECU shall send a negative response with response code 0x31 - requestOutOfRange

### 2568 — ReadGenericInformation negative response code subFunctionNotSupported
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The negative response codes that must be supported for the service AF are not defined by ISO and must therefore be clearly defined by this specification.
- If the ECU has received a request message for the service ReadGenericInformation with the sub-function different from 0x04 or 0x06 the ECU shall send a negative response with response code 0x12 - subFunctionNotSupported.

### 2569 — ReadGenericInformation positive response message data parameters definie...
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The service ReadGenericInformation is based on the ISO defined service ReadDTCInformation and shall therefore use the same definitions for the response message data parameters The ECU shall use ReadGenericInformation positive response message data parameters according to the same definitions as for the service ReadDTCInformation as defined in [Services_9] ISO 14229-1.

### 2570 — Response message format for ReadGenericInformation - reportGenericExtend...
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The format of the response message for the service AF is not defined by ISO and must therefore be clearly defined by this specification If the ECU has received a request message for the service ReadGenericInformation with the sub-function reportGenericExtendedDataByDTCNumber and the ECU shall send a positive response, the ECU shall send a positive response with the response message format as defined by Requirements on positive response format for service AF 06 (hex).

### 2571 — Response message format for ReadGenericInformation - reportGenericSnapsh...
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The format of the response message for the service AF is not defined by ISO and must therefore be clearly defined by this specification.
- If the ECU has received a request message for the service ReadGenericInformation with the sub-function reportGenericSnapshotByDTCNumber and the ECU shall send a positive response, the ECU shall send a positive response with the response message format as defined by Requirements on positive response format for service AF 04 (hex).

### 2572 — Values of DTCExtendedDataRecordNumber
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The values of the data parameter DTCExtendedDataRecordNumber for the service/subfunction ReadGenericInformation - reportGenericExtendedDataByDTCNumber shall be used as defined by reference [1] and the additional value of 0xFF which shall be used to identify all extended data record values supported by the ECU.

### 2573 — Values of DTCMaskRecord
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The values of the data parameter DTCMaskRecord for the service/subfunctionReadGenericInformation - reportGenericExtendedDataByDTCNumber shall be used as defined by [Services_1] UDS Data, and the additional value of 0xFFFFF which shall be used to identify all DTC values supported by the ECU.

### 2574 — Values of DTCMaskRecord
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The values of the data parameter DTCMaskRecord for the service/subfunctionReadGenericInformation - reportDTCSnapshotRecordByDTCNumber shall be used as defined by [Services_1] UDS Data, and the additional value of 0xFFFFF which shall be used to identify all DTC values supported by the ECU.

### 2575 — Values of DTCSnapShotRecordNumber
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The values of the data parameter DTCSnapshotRecordNumber for the service/subfunction ReadGenericInformation - reportDTCSnapshotRecordByDTCNumber shall be used as defined by [Services_1] UDS Data, and the additional value of 0xFF which shall be used to identify all snapshot record values supported by the ECU.4.5.3.1.2.1.4 InputOutput Control Functional Unit Index Session Sub-function Data parameters Session Notes Name Hex Name Hex Name Hex Default Extended Diagnostic Programming InputOutput Control Functional Unit 79 InputOutputControlByIdentifier 2F N M N 6 80 N/A N/A dataIdentifier See note 14 N M N 7 81 inputOutputControlParameter-returnControlToECU 00 N M N 82 InputOutputControlParameter-freezeCurrentState 02 N O N 83 InputOutputControlParameter-shortTermAdjustment 03 N M N 84 ControlState-dataRecord Spec.
- From the time the request is received by the ECU until the ECU regains control, the substituted values of the data record (referenced by the dataidentifier) shall remain static.
- If the substituted values need to change over time, for example due to safety reasons, the service routineControl (0x31) shall be used.

### 2576 — RequestDownload - addressAndLengthFormatIdentifier (44)
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- RequestDownload - addressAndLengthFormatIdentifier, with the value 0x44 (4 bytes MemoryAddress and 4 bytes memorySize), shall be supported in all sessions supporting RequestDownload (0x34).

### 2577 — RequestDownload - dataFormatIdentifier (00)
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- RequestDownload - dataFormatIdentifier 0x00 no compression and no encryption shall be supported in all sessions supporting RequestDownload (0x34).

### 2578 — RequestDownload - dataFormatIdentifier (01-0F and 11-7F and 81-FF)
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- RequestDownload - dataFormatIdentifier range 0x01-0x0F and 0x11-0x1F and 0x81-0xFF are optional in all sessions supporting RequestDownload.

### 2579 — RequestDownload - dataFormatIdentifier (10)
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- Support of compression method for downloading data to decrease the programming time RequestDownload – dataFormatIdentifier 0x10 compression method #1, as specified in [Services_5] Data Compression and Encryption and no encryption shall be supported in all sessions supporting RequestDownload (0x34).

### 2580 — RequestDownload - dataFormatIdentifier (80)
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Support of delta encoding method for downloading data to decrease the programming time RequestDownload – dataFormatIdentifier 0x80 Delta encoding, as specified in [Services_6] Delta Encoding Specification and no encryption shall be supported in all sessions supporting RequestDownload (0x34).

### 2581 — RequestDownload - memoryAdress
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- RequestDownload - memoryAdress shall be supported in all sessions supporting RequestDownload.

### 2582 — RequestDownload - memorySize
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- RequestDownload - memorySize shall be supported in all sessions supporting RequestDownload.

### 2583 — RequestDownload (34)
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The service RequestDownload shall be supported in programmingSession, both primary and secondary bootloader but shall not be used in any other session.
- If the ECU supports the RequestFileTransfer service which is an alternative method for file based data storage the RequestDownload service may not need to be supported.

### 2584 — RequestFileTransfer - dataFormatIdentifier (00)
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Support a simple standard method for downloading data RequestFileTransfer – dataFormatIdentifier 0x00 no compression and no encryption shall be supported in all sessions supporting RequestFileTransfer (0x38).

### 2585 — RequestFileTransfer - dataFormatIdentifier (01-0F and 11-7F and 81-FF)
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- RequestFileTransfer – dataFormatIdentifier range 0x01-0x0F and 0x11-0x7F and 0x81-0xFF is optional in all sessions supporting RequestFileTransfer (0x38). The presence of the parameter depends on the modeOfOperation parameter.

### 2586 — RequestFileTransfer - dataFormatIdentifier (10)
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- RequestFileTransfer – dataFormatIdentifier 0x10 compression method #1, specified in reference [Services_5] Data Compression and Encryption and no encryption shall be supported in all sessions supporting RequestFileTransfer (0x38).

### 2587 — RequestFileTransfer - dataFormatIdentifier (80)
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Support of delta encoding method for downloading data to decrease the programming time RequestFileTransfer – dataFormatIdentifier 0x80 Delta encoding, as specified in reference [Services_6] Delta encoding and no encryption shall be supported in all sessions supporting RequestFileTransfer (0x38).

### 2588 — RequestFileTransfer - filePathAndName
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- RequestFileTransfer – filePathAndName shall be supported in all sessions supporting RequestFileTransfer (0x38).

### 2589 — RequestFileTransfer - filePathAndNameLength
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- RequestFileTransfer - filePathAndNameLength shall be supported in all sessions supporting RequestFileTransfer (0x38).

### 2590 — RequestFileTransfer - fileSizeCompressed
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- RequestFileTransfer – fileSizeCompressed shall be supported in all sessions supporting RequestFileTransfer (0x38).
- The presence of the parameter depends on the modeOfOperation parameter.4.5.3.1.2.1.7 Additional routine requirementsThe positive response on the service routineControl request, regardless of sub-function, shall have the data parameter RoutineStatusRecord.
- The first byte of the data parameter RoutineStatusRecord shall be the RoutineInfo byte.

### 2591 — RequestFileTransfer - fileSizeParameterLenght
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- RequestFileTransfer – fileSizeParameterLenght shall be supported in all sessions supporting RequestFileTransfer (0x38).

### 2592 — RequestFileTransfer - fileSizeUnCompressed
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- RequestFileTransfer – fileSizeUnCompressed shall be supported in all sessions supporting RequestFileTransfer (0x38).

### 2593 — RequestFileTransfer - modeOfOperation (01-03)
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- RequestFileTransfer - modeOfOperation (0x01-0x03) shall be supported in all sessions supporting RequestFileTransfer (0x38).

### 2594 — RequestFileTransfer - modeOfOperation (03 - ReplaceFile)
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- If the modeOfOperation parameter 0x03 ReplaceFile is used and the file not is stored at the location shall the file be added.

### 2595 — RequestFileTransfer - modeOfOperation (04-05)
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- RequestFileTransfer - modeOfOperation (0x04-0x05) is optional in all sessions supporting RequestFileTransfer (0x38).

### 2596 — RequestFileTransfer (38)
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Used in the SWDL process The RequestFileTransfer service is optional in programmingSession, both primary and secondary bootloader but shall not be used in any other session.
- The RequestFileTransfer service shall be implemented as defined in ISO 14229-1:2013(Second Edition).

### 2597 — RequestTransferExit (37)
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The service RequestTransferExit shall be supported in programmingSession, both primary and secondary bootloader but shall not be used in any other session.

### 2598 — RequestTransferExit (37) transferResponseParameterRecord
- 版本：v5 ｜ 验证方式：Test ｜ 适用：通用
- If the ECU does not support Software Authentication (CheckMemory routine) as defined in [Services_8] General Software Authentication, the transferResponseParameterRecord shall contain a checksum for downloaded or uploaded data block.
- If the ECU supports Software Authentication, no transferResponseParameterRecord shall be used for downloaded block but only for upload.

### 2599 — RequestTransferExit (37) transferResponseParameterRecord - algorithm
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- If the transfer of data is initiated by RequestDownload or RequestUpload the transferResponseParameterRecord checksum calculation shall use the CRC16-CCITT algorithm (initial value 0xFFFF and normal representation).
- The checksum shall be calculated on all data bytes as defined by the diagnostic services RequestDownload or RequestUpload.

### 2600 — RequestTransferExit (37) transferResponseParameterRecord - algorithm
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- If the transfer of data is initiated by the RequestFileTransfer service the (transferResponseParameterRecord) shall consist of a four byte checksum based on the CRC32 algorithm (initial value 0xFFFFFFFF and normal representation) calculation on all data bytes as defined by the diagnostic services RequestFileTransfer.

### 2601 — RequestTransferExit (37) transferResponseParameterRecord - use non-volatile memory
- 版本：v5 ｜ 验证方式：Test ｜ 适用：通用
- The checksum (transferResponseParameterRecord) shall always be calculated on data read from the actual non-volatile memory as defined by the RequestDownload, RequestUpload or RequestFileTransfer .

### 2602 — RequestUpload - addressAndLengthFormatIdentifier (44)
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- RequestUpload - addressAndLengthFormatIdentifier, with the value 0x44 (4 bytes MemoryAddress and 4 bytes memorySize), shall be supported in all sessions supporting RequestUpload (0x35).

### 2603 — RequestUpload - dataFormatIdentifier
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- RequestUpload - dataFormatIdentifier with the value 0x00 shall be supported in all sessions supporting RequestUpload.

### 2604 — RequestUpload - memoryAdress
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- RequestUpload - memoryAdress shall be supported in all sessions supporting RequestUpload

### 2605 — RequestUpload - memorySize
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- RequestUpload - memorySize shall be supported in all sessions supporting RequestUpload.

### 2606 — RequestUpload (35)
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- The service RequestUpload may be supported in the secondary bootloader - programmingSession but shall not be used in any other session.

### 2607 — TransferData - blockSequenceCounter
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- TransferData - blockSequenceCounter shall be supported in all sessions supporting TransferData.

### 2608 — TransferData - transferRequestParameterRecord
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- TransferData - transferRequestParameterRecord shall be supported in all sessions supporting TransferData, if the data direction is from the Tester to the ECU i.

### 2609 — TransferData - transferResponseParameterRecord
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- TransferData - transferResponseParameterRecord shall be supported in all sessions supporting TransferData, if the data direction is from the ECU to the Tester i.

### 2610 — TransferData (36)
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- The service TransferData (0x36) shall be supported in programmingSession, both primary and secondary bootloader but shall not be used in any other session.

### 2611 — TransferData (36) blockSequenceCounter handling
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The use cases (a-d) for blockSequenceCounter, specified in [Services_9] ISO 14229-1, shall be handled by the tester and the ECU

### 2612 — TransferData (36) blockSequenceCounter received with the same value
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Define behaviour of how a ECU shall react when receiving the same blockSequenceCounter value twice.
- If an ECU receives a transferData request during an active download sequence with the same blockSequenceCounter as the last accepted transferData request, it shall respond with a positive response without writing the data once again to its memory.

### 2613 — Session Layer
- 版本：v4 ｜ 验证方式：Inspection ｜ 适用：通用
- ISO standard shall be followed to reduce cost and make implementation easier Road vehicles - Unified diagnostic services - Part 2: Session layer services The session layer defined in [Session_3] Road vehicles — Unified diagnostic services — Part 2: Session layer services shall be implemented with restriction/additions defined by the requirements in this specification.4.5.4.2 UDS Session ECU reqs4.5.4.2.1 Appendix4.5.4.2.1.1 Example, queuing of requests in a serverThe sequence below shows examples where multiple requests are sent to a server, a typical case is in programming session where the client will send additional request to be queued in the server.
- If gateways are located between client and server, due to delays in gateways, the second request (believed by client to be queued in vehicle) may arrive to the server slightly differently now and then in time relation to the server responses.
- The server may already have started responding to a previous request.

### 2614 — P4Server_max definition
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- In case of a request to schedule periodic responses, the initial positive or negative response that indicates the acceptance or non-acceptance of the request to schedule periodic responses shall be considered the final response.

### 2615 — P4Server_max equal to P2Server_max
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- To define the behaviour when the P4Server_max is equal to P2Server_max The server is not allowed to response with a negative response code 0x78(requestCorrectlyReceived-ResponsePending) if P4 Server_max is the same as P2 Server_max. Note: The value of P2 Serve

### 2616 — Order of responses in programming session
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The order the server responds to queued requests must be defined.
- In programming session, physical diagnostic requests addressed to a server shall be processed and responded to in the order they were received.

### 2617 — Server behavior for additional client requests in programming session
- 版本：v6 ｜ 验证方式：Test ｜ 适用：通用
- the request just received shall be ignored.
- If the server is processing a first request and queues a second request, and then a third request appears, the third request shall be ignored unless it can be queued as well.4.5.4.2.2.2 P4 definitionP4Server_max is the maximum time allowed for a server from reception of a request until start of transmission of the final response.

### 2618 — Server support of queued requests in programming session
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- In programming session the server shall be able to handle the minimum of one (1) queued physical request during processing of an already received physical request which do not lead to a server reset , meaning the server shall store the second request in a FIFO queue for later processing.
- If the server isn’t able to receive the complete second message due to lack of receive buffer space the server shall halt the message with the help of the network/transport layer e.
- Messages that can be fully received in addition to the minimum one queued request shall be stored in queue.

### 2619 — Start of P2Server for queued request in programming session
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- To reduce latency when the server shall start process the queued request.
- In programming session, the server shall start the P2 Server timer for the queued request once the final response (indicated via Server T_Data.
- the message is halted or a large queued request is received) shall the server start the P2 Server timer when the complete queued message is received (indicated via Server T_Data.

### 2620 — P2(star)Server_max
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- P2*Server_max is the maximum time for the server to start with the response message after the transmission of a negative response 0x78 (enhanced response timing). The maximum time for P2* Server in all sessions is 5000 ms.

### 2621 — P2(star)Server_min
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- For final response it shall be as short as possible to allow good timing performance.
- For pending response it must be a suitable value so that a server do not significantly increase bus load by consecutive pending responses.
- During the enhanced response timing, the minimum time between the transmission of consecutive negative messages (each with negative response code 0x78) shall be 0.3 * P2* Server_max, in order to avoid flooding the data link with unnecessary negative response messages.4.5.5 UDSonCAN4.5.5.1 UDSonCAN - Generic4.5.5.1.1 Transport_Network LayerThe transport/network layer required by this document shall be compliant to [UDSonCAN_4] DoCAN.

### 2622 — P2Server_max - non programming session
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- P2Server_max is the maximum time for the server to start with the response message after the reception of a request message. The maximum time for P2 Server in all sessions except programmingSession is 50 ms.

### 2623 — P2Server_max - ProgrammingSession
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- P2Server_max is the maximum time for the server to start with the response message after the reception of a request message The maximum time for P2 Server in programmingSession is 25 ms.

### 2624 — P2server_min
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- P2Server_min is the minimum time for the server to start with the response message after the reception of a request message. The minimum time for P2 Server in all sessions is 0ms.4.5.4.2.3.1.2 P2(star)Server

### 2650 — Addressing USDT frames
- 版本：v4 ｜ 验证方式：Analysis ｜ 适用：通用
- Define which CAN IDs an ECU shall listen on Each ECU shall support a total of three (3) USDT CAN diagnostic IDs.· Physically addressed requests (or ECU Diagnostic Reception ID).· Physically and functionally addressed responses or (ECU Diagnostic Transmission ID).

### 2651 — Application bootloader requirement
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- The application shall comply with the requirements as specified in[UDSonCAN_9] Bootloader_UDSonCAN, chapter Flow chart diagram (Application).
- 4.5.5.1.6 Session LayerThe session layer required by this document shall be compliant to [UDSonCAN_3] UDSSession with the restrictions/additions as defined by the subsequent sub-sections.

### 2653 — CAN data link layer
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- The data link layer required by this document shall be compliant to [UDSonCAN_4] CAN Data Link Layer Specification.4.5.5.1.3 Physical LayerThe physical layer required by this document shall be compliant to [UDSonCAN_8] CAN Physical Layer Specification.

### 2654 — CAN physical layer
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- The physical layer required by this document shall be compliant to [UDSonCAN_8] CAN Physical Layer Specification.4.5.5.1.4 IntroductionThis document specifies OEM specific requirements for an ECU on the CAN network.
- jpg) ## 4.5.5.1.4.1 Requisite documents Note that in the case of any requirement conflict between this document and any of the referenced documents, the proposed solution to the conflict shall be approved by CEVT Electrical Architecture.
- Information obtaining ISO documents may be found on the internet: www.

### 2655 — Diagnostic Session Layer
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- The session layer required by this document shall be compliant to [UDSonCAN_3] UDSSession.
- The ECU shall use the response ID specified in the table below - ECU Diagnostic Reception / Transmission CAN IDs as N_TA (Session layer Target Address).
- 0x71E 0x61E 0x7FF Functional request to all networks within all domains Table - ECU Diagnostic Reception / Transmission CAN IDs Note (1): The ECU reception ID from 0x700 to 0x70F is reserved due to the domain ECU always shall have network ID equal to zero(0).

### 2656 — Transport_Network layer
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- The CAN transport/network layer required by this document shall be compliant with [UDSonCAN_4] DoCAN.
- 4.5.5.1.2 Data Link LayerThe data link layer required by this document shall be compliant to [UDSonCAN_4] CAN Data Link Layer Specification.

### 2657 — Application diagnostic data
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- Define which data parameters each CAN ECU shall or may support.
- The CAN application shall support the diagnostic data as defined in [UDSonCAN_2] UDS Data.

### 2658 — Diagnostic services
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- Define which services each CAN ECU shall or may support.
- Section "Diagnostic Services" The CAN application shall support the diagnostic services as defined in [UDSonCAN_1] UDS Services.4.5.5.2.2 Diagnostic DataThe diagnostic data required are specified in [UDSonCAN_2] UDS Data, with the restrictions and additions in subsequent subsections.

### 2659 — Bus-off
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The bus-off state means there has been a fault in sending or receiving CAN frames and usually this will make customer observable symptoms and hence a DTC shall be set showing that the network has been in bus-off state.
- Table: "Summary of CAN related external circuit faults" Item 1 All ECUs on the network shall be able to detect and set bus-off DTCs when the CAN controller has gotten into the state bus-off see [UDSonCAN_7] Autosar Network Management- additional requirements for further reference.

### 2660 — Bus-off _ Decrease FDC10 steps
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- Each time the CAN controller exits the state bus-off, the ECU shall consider the DTC as set.
- Table: "Calibration of CAN DTCs" Item 1 The bus-off FDC10 shall be decrease according to specified by [UDSonCAN_7] Autosar Network Management- additional requirements.

### 2661 — Bus-off_DTC ID
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The OEM shall define which DTC ID to use to minimize differences in between different ECUs, so that administration is kept to a minimum.
- Table: "Summary of CAN related external circuit faults" Item 1 The bus-off DTC ID shall be as defined in [UDSonCAN_10] Global Master Reference Database.

### 2662 — Bus-off _ DTCAgedLimit
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Table: "Calibration of CAN DTCs" Item 1 The bus-off DTC shall use DTCAgedLimit = 255.

### 2663 — Bus-off _ DTCConfirmedLimit
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Due to the nature of the DTC, the DTC shall be considered confirmed as soon as a test failed has been run.
- Table: "Calibration of CAN DTCs" Item 1 The bus-off DTC shall use DTCConfirmedLimit = 1.

### 2664 — Bus-off_Failure type
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- The OEM shall define which failure type that shall be used to minimize the differences in between different ECUs, so that administration is kept to a minimum.
- Table: "Summary of CAN related external circuit faults" Item 1 For bus-off DTCs the failure type shall be 0x00 if the ECU is emission related and 0x88 if the ECU is not emission related.

### 2665 — Bus-off _ FDC10 max value
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- If a Bus-off occurs it is assumed it has such a big impact on the functionality of the system that it shall cause setting the confirm bit of the DTC.
- Table "Calibration of CAN DTCs" Item 1 The DTC test for Bus-off shall have FDC10 max value = 127.

### 2666 — Bus-off _ Increase FDC10 steps
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- Each time the CAN controller gets into the state bus-off, the ECU shall consider the DTC as set.
- Table: "Calibration of CAN DTCs" Item 1 The bus-off FDC10 shall be increase according to specified by [UDSonCAN_7] Autosar Network Management- additional requirements .

### 2667 — Bus-off _ Test period
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- Preferably the bus-off state shall be detected via interrupt but if not possible a minimum standardized frequency shall be used.
- Table: "Summary of CAN related external circuit faults" Item 1 The bus-off check shall be tested according to specified by [UDSonCAN_7] Autosar Network Management- additional requirements.

### 2668 — Bus-off _ Test sample failed criteria
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- Each time the CAN controller gets into the state bus-off, the ECU shall consider the DTC as set.
- Table: "Calibration of CAN DTCs" Item 1 The reported value of the bus-off DTC fault detection counter shall increase according to specified by [UDSonCAN_7] Autosar Network Management- additional requirements .

### 2669 — Bus-off _ Test sample passed criteria
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- Each time the CAN controller gets into the state bus-on, the ECU shall consider the DTC as not set.
- Table: "Calibration of CAN DTCs" Item 1 The reported value of the bus-off DTC fault detection counter shall decrease according to specified by [UDSonCAN_7] Autosar Network Management- additional requirements.

### 2670 — Bus-off_TRC
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- A standardized test run criteria shall be used to make it easier for fault tracers to know that the test has been performed.
- Table: "Summary of CAN related external circuit faults" Item 1 The TRC to perform the bus-off check shall be according to the General Test Run Criteria specified in [UDSonCAN_2] UDS Data.

### 2671 — Bus-off _ UnconfirmedDTCLimit
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Due to the nature of the DTC, the DTC shall be considered unconfirmed as soon as a test passed has been run.
- Table: "Calibration of CAN DTCs" Item 1 The bus-off DTC test shall use UnconfirmedDTCLimit = the same value as the increase value of the FDC10.

### 2672 — CANH circuit short to battery voltage
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Defining what the cause of the electrical fault may help in the fault tracing process.
- Table: "Summary of CAN related external circuit faults" Item 5 If the ECU is connected to more then one public network and the ECU is the ECU transferring diagnostic messages in between the two networks, the ECU shall support detecting CANH circuit short to battery voltage.
- Note that there shall be one unique DTC for each public network in the vehicle.

### 2673 — CANH circuit short to battery voltage _ Decrease FDC10 steps
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Generic DTC configuration shall be used for electrical faults to have as similar behaviour regarding DTC setting as possible.
- Table: "Calibration of CAN DTCs" Item 5 slave The CANH circuit short to battery voltage FDC10 shall be decreased by 2 at every test sample passed.

### 2674 — CANH circuit short to battery voltage _ DTC ID
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The OEM shall define which DTC ID to use to minimize differences in between different ECUs, so that administration is kept to a minimum.
- Table: "Summary of CAN related external circuit faults" Item 5 The CANH circuit short to battery voltage DTC ID shall be as defined in [UDSonCAN_10] Global Master Reference Database.

### 2675 — CANH circuit short to battery voltage _ DTCAgedLimit
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Generic DTC configuration shall be used for electrical faults to have as similar behaviour regarding DTC setting as possible.
- Table: "Calibration of CAN DTCs" Item 5 slave The CANH circuit short to battery voltage DTC shall use DTCAgedLimit = 255.

### 2676 — CANH circuit short to battery voltage _ DTCConfirmedLimit
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Generic DTC configuration shall be used for electrical faults to have as similar behaviour regarding DTC setting as possible.
- Table: "Calibration of CAN DTCs" Item 5 slave The CANH circuit short to battery voltage DTC shall use DTCConfirmedLimit = 3.

### 2677 — CANH circuit short to battery voltage _ Failure type
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The OEM shall define which failure type that shall be used to minimize the differences in between different ECUs, so that administration is kept to a minimum.
- Table: "Summary of CAN related external circuit faults" Item 5 For CANH circuit short to battery voltage DTCs the failure type 0x00 shall be used.

### 2678 — CANH circuit short to battery voltage _ FDC10 max value
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Generic DTC configuration shall be used for electrical faults to have as similar behaviour regarding DTC setting as possible.
- Table "Calibration of CAN DTCs" Item 5 The DTC test for CANH circuit short to battery voltage shall have FDC10 max value = 127.

### 2679 — CANH circuit short to battery voltage _ Increase FDC10 steps
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Generic DTC configuration shall be used for electrical faults to have as similar behaviour regarding DTC setting as possible.
- Table: "Calibration of CAN DTCs" Item 5 slave The CANH circuit short to battery voltage FDC10 shall be increased by 3 at every test sample failed.

### 2680 — CANH circuit short to battery voltage _ Test period
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- A standard time shall be used in detecting all physical bus faults.
- Table: "Summary of CAN related external circuit faults" Item 5 The CANH circuit short to battery voltage check shall be tested periodically at least every 100 ms.

### 2681 — CANH circuit short to battery voltage _ Test sample failed criteria
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Table: "Calibration of CAN DTCs" Item 5 slave The reported value of the DTC fault detection counter shall increase when CANH circuit short to battery voltage is detected.

### 2682 — CANH circuit short to battery voltage _ Test sample passed criteria
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Table: "Calibration of CAN DTCs" Item 5 slave The reported value of the DTC fault detection counter shall decrease when not CANH circuit short to battery voltage is detected.

### 2683 — CANH circuit short to battery voltage _ TRC
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Default test run criteria shall be used for all physical bus faults.
- Table: "Summary of CAN related external circuit faults" Item 5 The TRC to perform the CANH circuit short to battery voltage check shall be according to the general Test Run Criteria specified in [UDSonCAN_2] UDS Data.

### 2684 — CANH circuit short to battery voltage _ UnconfirmedDTCLimit
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Generic DTC configuration shall be used for electrical faults to have as similar behaviour regarding DTC setting as possible.
- Table: "Calibration of CAN DTCs" Item 5 slave The CANH circuit short to battery voltage DTC test shall use UnconfirmedDTCLimit = 5.

### 2685 — CANH circuit short to CANL circuit
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Defining what the cause of the electrical fault may help in the fault tracing process.
- Table: "Summary of CAN related external circuit faults" Item 9 If the ECU is connected to more then one public network and the ECU is the ECU transferring diagnostic messages in between the two networks, the ECU shall support detecting CANH circuit short to CANL circuit.
- Note that there shall be one unique DTC for each public network in the vehicle.

### 2686 — CANH circuit short to CANL circuit _ Decrease FDC10 steps
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Generic DTC configuration shall be used for electrical faults to have as similar behaviour regarding DTC setting as possible.
- Table: "Calibration of CAN DTCs" Item 9 The CANH circuit short to CANL circuit FDC10 shall be decreased by 2 at every test sample passed.

### 2687 — CANH circuit short to CANL circuit _ DTC ID
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The OEM shall define which DTC ID to use to minimize differences in between different ECUs, so that administration is kept to a minimum.
- Table: "Summary of CAN related external circuit faults" Item 9 The CANH circuit short to CANL circuit DTC ID shall be as defined in [UDSonCAN_10] Global Master Reference Database.

### 2688 — CANH circuit short to CANL circuit _ DTCAgedLimit
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Generic DTC configuration shall be used for electrical faults to have as similar behaviour regarding DTC setting as possible.
- Table: "Calibration of CAN DTCs" Item 9 The CANH circuit short to CANL circuit DTC shall use DTCAgedLimit = 255.

### 2689 — CANH circuit short to CANL circuit _ DTCConfirmedLimit
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Generic DTC configuration shall be used for electrical faults to have as similar behaviour regarding DTC setting as possible.
- Table: "Calibration of CAN DTCs" Item 9 The CANH circuit short to CANL circuit DTC shall use DTCConfirmedLimit = 3.

### 2690 — CANH circuit short to CANL circuit _ Failure type
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The OEM shall define which failure type that shall be used to minimize the differences in between different ECUs, so that administration is kept to a minimum.
- Table: "Summary of CAN related external circuit faults" Item 9 For CANH circuit short to CANL circuit DTCs the failure type 0x00 shall be used.

### 2691 — CANH circuit short to CANL circuit _ FDC10 max value
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Generic DTC configuration shall be used for electrical faults to have as similar behaviour regarding DTC setting as possible.
- Table "Calibration of CAN DTCs" Item 9 The DTC test for CANH circuit short to CANL circuit shall have FDC10 max value = 127.

### 2692 — CANH circuit short to CANL circuit _ Increase FDC10 steps
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Generic DTC configuration shall be used for electrical faults to have as similar behaviour regarding DTC setting as possible.
- Table: "Calibration of CAN DTCs" Item 9 The CANH circuit short to CANL circuit FDC10 shall be increased by 3 at every test sample failed.

### 2693 — CANH circuit short to CANL circuit _ Test period
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- A standard time shall be used in detecting all physical bus faults.
- Table: "Summary of CAN related external circuit faults" Item 9 The CANH circuit short to CANL circuit check shall be tested periodically at least every 100 ms.

### 2694 — CANH circuit short to CANL circuit _ Test sample failed criteria
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Table: "Calibration of CAN DTCs" Item 9 The reported value of the DTC fault detection counter shall increase when CANH circuit short to CANL circuit is detected.

### 2695 — CANH circuit short to CANL circuit _ Test sample passed criteria
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Table: "Calibration of CAN DTCs" Item 7.9 The reported value of the DTC fault detection counter shall decrease when not CANH circuit short to CANL circuit is detected.

### 2696 — CANH circuit short to CANL circuit _ TRC
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- Default test run criteria shall be used for all physical bus faults.
- Table: "Summary of CAN related external circuit faults" Item 9 The TRC to perform the CANH circuit short to CANL circuit check shall be according to the general Test Run Criteria specified in [UDSonCAN_2] UDS Data.

### 2697 — CANH circuit short to CANL circuit _ UnconfirmedDTCLimit
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Generic DTC configuration shall be used for electrical faults to have as similar behaviour regarding DTC setting as possible Table: "Calibration of CAN DTCs" Item 9 The CANH circuit short to CANL circuit DTC test shall use UnconfirmedDTCLimit = 5

### 2698 — CANH circuit short to ground
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Defining what the cause of the electrical fault may help in the fault tracing process.
- Table: "Summary of CAN related external circuit faults" Item 7 If the ECU is connected to more then one public network and the ECU is the ECU transferring diagnostic messages in between the two networks, the ECU shall support detecting CANH circuit short to ground.
- Note that there shall be one unique DTC for each public network in the vehicle.

### 2699 — CANH circuit short to ground _ Decrease FDC10 steps
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Generic DTC configuration shall be used for electrical faults to have as similar behaviour regarding DTC setting as possible.
- Table: "Calibration of CAN DTCs" Item 7 The CANH circuit short to ground FDC10 shall be decreased by 2 at every test sample passed.

### 2700 — CANH circuit short to ground _ DTC ID
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The OEM shall define which DTC ID to use to minimize differences in between different ECUs, so that administration is kept to a minimum.
- Table: "Summary of CAN related external circuit faults" Item 7 The CANH circuit short to ground DTC ID shall be as defined in [UDSonCAN_10] Global Master Reference Database.

### 2701 — CANH circuit short to ground _ DTCAgedLimit
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Generic DTC configuration shall be used for electrical faults to have as similar behaviour regarding DTC setting as possible.
- Table: "Calibration of CAN DTCs" Item 7 The CANH circuit short to ground DTC shall use DTCAgedLimit = 255.

### 2702 — CANH circuit short to ground _ DTCConfirmedLimit
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Generic DTC configuration shall be used for electrical faults to have as similar behaviour regarding DTC setting as possible.
- Table: "Calibration of CAN DTCs" Item 7 The CANH circuit short to ground DTC shall use DTCConfirmedLimit = 3.

### 2703 — CANH circuit short to ground _ Failure type
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The OEM shall define which failure type that shall be used to minimize the differences in between different ECUs, so that administration is kept to a minimum.
- Table: "Summary of CAN related external circuit faults" Item 7 For CANH circuit short to ground DTCs the failure type 0x00 shall be used.

### 2704 — CANH circuit short to ground _ FDC10 max value
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Generic DTC configuration shall be used for electrical faults to have as similar behaviour regarding DTC setting as possible.
- Table "Calibration of CAN DTCs" Item 7 The DTC test for CANH circuit short to ground shall have FDC10 max value = 127.

### 2705 — CANH circuit short to ground _ Increase FDC10 steps
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Generic DTC configuration shall be used for electrical faults to have as similar behaviour regarding DTC setting as possible.
- Table: "Calibration of CAN DTCs" Item 7 The CANH circuit short to ground FDC10 shall be increased by 3 at every test sample failed.

### 2706 — CANH circuit short to ground _ Test period
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- A standard time shall be used in detecting all physical bus faults.
- Table: "Summary of CAN related external circuit faults" Item 7 The CANH circuit short to ground check shall be tested periodically at least every 100 ms.

### 2707 — CANH circuit short to ground _ Test sample failed criteria
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Table: "Calibration of CAN DTCs" Item 7 The reported value of the DTC fault detection counter shall increase when CANH circuit short to ground is detected.

### 2708 — CANH circuit short to ground _ Test sample passed criteria
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Table: "Calibration of CAN DTCs" Item 7 The reported value of the DTC fault detection counter shall decrease when not CANH circuit short to ground is detected.

### 2709 — CANH circuit short to ground _ TRC
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Default test run criteria shall be used for all physical bus faults.
- Table: "Summary of CAN related external circuit faults" Item 7 The TRC to perform the CANH circuit short to ground check shall be according to the general Test Run Criteria specified in [UDSonCAN_2] UDS Data.

### 2710 — CANH circuit short to ground _ UnconfirmedDTCLimit
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Generic DTC configuration shall be used for electrical faults to have as similar behaviour regarding DTC setting as possible.
- Table: "Calibration of CAN DTCs" Item 7 The CANH circuit short to ground DTC test shall use UnconfirmedDTCLimit = 5.

### 2711 — CANL circuit short to battery voltage
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Defining what the cause of the electrical fault may help in the fault tracing process.
- Table: "Summary of CAN related external circuit faults" Item 8 If the ECU is connected to more then one public network and the ECU is the ECU transferring diagnostic messages in between the two networks, the ECU shall support detecting CANL circuit short to battery voltage.
- Note that there shall be one unique DTC for each public network in the vehicle.

### 2712 — CANL circuit short to battery voltage_Decrease FDC steps
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- 2712 v2CANL circuit short to battery voltage_Decrease FDC steps Generic DTC configuration shall be used for electrical faults to have as similar behaviour regarding DTC setting as possible.
- Table: "Calibration of CAN DTCs" Item 8 The CANL circuit short to battery voltage FDC10 shall be decreased by 2 at every test sample passed.

### 2713 — CANL circuit short to battery voltage _ DTC ID
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The OEM shall define which DTC ID to use to minimize differences in between different ECUs, so that administration is kept to a minimum.
- Table: "Summary of CAN related external circuit faults" Item 8 The CANL circuit short to battery voltage DTC ID shall be as defined in [UDSonCAN_10] Global Master Reference Database.

### 2714 — CANL circuit short to battery voltage _ DTCAgedLimit
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Generic DTC configuration shall be used for electrical faults to have as similar behaviour regarding DTC setting as possible.
- Table: "Calibration of CAN DTCs" Item 8 The CANL circuit short to battery voltage DTC shall use DTCAgedLimit = 255.

### 2715 — CANL circuit short to battery voltage _ DTCConfirmedLimit
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Generic DTC configuration shall be used for electrical faults to have as similar behaviour regarding DTC setting as possible Table: "Calibration of CAN DTCs" Item 8 The CANL circuit short to battery voltage DTC shall use DTCConfirmedLimit = 3.

### 2716 — CANL circuit short to battery voltage _ Failure type
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The OEM shall define which failure type that shall be used to minimize the differences in between different ECUs, so that administration is kept to a minimum.
- Table: "Summary of CAN related external circuit faults" Item 8 For CANL circuit short to battery voltage DTCc the failure type 0x00 shall be used.

### 2717 — CANL circuit short to battery voltage _ FDC10 max value
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Generic DTC configuration shall be used for electrical faults to have as similar behaviour regarding DTC setting as possible.
- Table "Calibration of CAN DTCs" Item 8 The DTC test for CANL circuit short to battery voltage shall have FDC10 max value = 127.

### 2718 — CANL circuit short to battery voltage_Increase FDC10 steps
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- 2718 v2CANL circuit short to battery voltage_Increase FDC10 steps Generic DTC configuration shall be used for electrical faults to have as similar behaviour regarding DTC setting as possible.
- Table: "Calibration of CAN DTCs" Item 8 The CANL circuit short to battery voltage FDC10 shall be increased by 3 at every test sample failed.

### 2719 — CANL circuit short to battery voltage _ Test period
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- A standard time shall be used in detecting all physical bus faults.
- Table: "Summary of CAN related external circuit faults" Item 8 The CANL circuit short to battery voltage check shall be tested periodically at least every 100 ms.

### 2720 — CANL circuit short to battery voltage _ Test sample failed criteria
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Table: "Calibration of CAN DTCs" Item 8 The reported value of the DTC fault detection counter shall increase when CANL circuit short to battery voltage is detected.

### 2721 — CANL circuit short to battery voltage_Test sample passed criteria
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Table: "Calibration of CAN DTCs" Item 8 The reported value of the DTC fault detection counter shall decrease when not CANL circuit short to battery voltage is detected.

### 2722 — CANL circuit short to battery voltage _ TRC
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Default test run criteria shall be used for all physical bus faults.
- Table: "Summary of CAN related external circuit faults" Item 8 The TRC to perform the CANL circuit short to battery voltage check shall be according to the general Test Run Criteria specified in [UDSonCAN_2] UDS Data.

### 2723 — CANL circuit short to battery voltage_UnconfirmedDTCLimit
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- 2723 v2CANL circuit short to battery voltage_UnconfirmedDTCLimit Generic DTC configuration shall be used for electrical faults to have as similar behaviour regarding DTC setting as possible.
- Table: "Calibration of CAN DTCs" Item 8 The CANL circuit short to battery voltage DTC test shall use UnconfirmedDTCLimit = 5.

### 2724 — CANL circuit short to ground
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Defining what the cause of the electrical fault may help in the fault tracing process.
- Table: "Summary of CAN related external circuit faults" Item 6 If the ECU is connected to more then one public network and the ECU is the ECU transferring diagnostic messages in between the two networks, the ECU shall support detecting CANL circuit short to ground.
- Note that there shall be one unique DTC for each public network in the vehicle.

### 2725 — CANL circuit short to ground _ Decrease FDC10 steps
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Generic DTC configuration shall be used for electrical faults to have as similar behaviour regarding DTC setting as possible.
- Table: "Calibration of CAN DTCs" Item 6 The CANL circuit short to ground FDC10 shall be decreased by 2 at every test sample passed.

### 2726 — CANL circuit short to ground _ DTC ID
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The OEM shall define which DTC ID to use to minimize differences in between different ECUs, so that administration is kept to a minimum.
- Table: "Summary of CAN related external circuit faults" Item 6 The CANL circuit short to ground DTC ID shall be as defined in [UDSonCAN_10] Global Master Reference Database.

### 2727 — CANL circuit short to ground _ DTCAgedLimit
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Generic DTC configuration shall be used for electrical faults to have as similar behaviour regarding DTC setting as possible.
- Table: "Calibration of CAN DTCs" Item 6 The CANL circuit short to ground DTC shall use DTCAgedLimit = 255.

### 2728 — CANL circuit short to ground _ DTCConfirmedLimit
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Generic DTC configuration shall be used for electrical faults to have as similar behaviour regarding DTC setting as possible.
- Table: "Calibration of CAN DTCs" Item 6 The CANL circuit short to ground DTC shall use DTCConfirmedLimit = 3.

### 2729 — CANL circuit short to ground _ Failure type
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The OEM shall define which failure type that shall be used to minimize the differences in between different ECUs, so that administration is kept to a minimum.
- Table: "Summary of CAN related external circuit faults" Item 6 For CANL circuit short to ground DTCs the failure type 0x00 shall be used.

### 2730 — CANL circuit short to ground _ FDC10 max value
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Generic DTC configuration shall be used for electrical faults to have as similar behaviour regarding DTC setting as possible.
- Table "Calibration of CAN DTCs" Item 6 The DTC test for CANL circuit short to ground shall have FDC10 max value = 127.

### 2731 — CANL circuit short to ground _ Increase FDC10 steps
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Generic DTC configuration shall be used for electrical faults to have as similar behaviour regarding DTC setting as possible.
- Table: "Calibration of CAN DTCs" Item 6 The CANL circuit short to ground FDC10 shall be increased by 3 at every test sample failed.

### 2732 — CANL circuit short to ground _ Test period
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- A standard time shall be used in detecting all physical bus faults.
- Table: "Summary of CAN related external circuit faults" Item 6 The CANL circuit short to ground check shall be tested periodically at least every 100 ms.

### 2733 — CANL circuit short to ground _ Test sample failed criteria
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Table: "Calibration of CAN DTCs" Item 6 The reported value of the DTC fault detection counter shall increase when CANL circuit short to ground is detected.

### 2734 — CANL circuit short to ground _ Test sample passed criteria
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Table: "Calibration of CAN DTCs" Item 6 The reported value of the DTC fault detection counter shall decrease when not CANL circuit short to ground is detected.

### 2735 — CANL circuit short to ground _ TRC
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Default test run criteria shall be used for all physical bus faults.
- Table: "Summary of CAN related external circuit faults" Item 6 The TRC to perform the CANL circuit short to ground check shall be according to the general Test Run Criteria specified in [UDSonCAN_2] UDS Data.

### 2736 — CANL circuit short to ground _ UnconfirmedDTCLimit
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Generic DTC configuration shall be used for electrical faults to have as similar behaviour regarding DTC setting as possible.
- Table: "Calibration of CAN DTCs" Item 6 The CANL circuit short to ground DTC test shall use UnconfirmedDTCLimit = 5.

### 2737 — Common CAN electrical fault
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Defining what the cause of the electrical fault may help in the fault tracing process.
- Table: Summary of CAN related external circuit faults If the ECU is connected to more then one public network and the ECU is the ECU transferring diagnostic messages in between the two networks, the ECU shall support detecting Common CAN electrical fault

### 2738 — Common CAN electrical fault _ Decrease FDC10 steps
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- 2738 v2Common CAN electrical fault _ Decrease FDC10 steps Generic DTC configuration shall be used for electrical faults to have as similar behaviour regarding DTC setting as possible.
- Table: Calibration of CAN DTCs, item10 The Common CAN electrical fault FDC10 shall be decreased by 2 at every test sample passed.

### 2739 — Common CAN electrical fault _ DTC ID
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The OEM shall define which DTC ID to use to minimize differences in between different ECUs, so that administration is kept to a minimum.

### 2740 — Common CAN electrical fault _ DTCAgedLimit
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- 2740 v2Common CAN electrical fault _ DTCAgedLimit Generic DTC configuration shall be used for electrical faults to have as similar behaviour regarding DTC setting as possible.
- Table: Calibration of CAN DTCs, item10 The Common CAN electrical fault DTC shall use DTCAgedLimit = 255.

### 2741 — Common CAN electrical fault _ DTCConfirmedLimit
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- 2741 v2Common CAN electrical fault _ DTCConfirmedLimit Generic DTC configuration shall be used for electrical faults to have as similar behaviour regarding DTC setting as possible.
- Table: Calibration of CAN DTCs, item10 The Common CAN electrical fault DTC shall use DTCConfirmedLimit = 3.

### 2742 — Common CAN electrical fault _Failure type
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- The OEM shall define which failure type that shall be used to minimize the differences in between different ECUs, so that administration is kept to a minimum.
- able: Summary of CAN related external circuit faults, item10 Common CAN electrical fault DTCs shall use the failure type 0x01.

### 2743 — Common CAN electrical fault _ FDC10 max value
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- 2743 v2Common CAN electrical fault _ FDC10 max value Generic DTC configuration shall be used for electrical faults to have as similar behaviour regarding DTC setting as possible.
- able: Calibration of CAN DTCs, item10 The DTC test for Common CAN electrical fault shall have FDC10 max value = 127.

### 2744 — Common CAN electrical fault _ Increase FDC10 steps
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Generic DTC configuration shall be used for electrical faults to have as similar behaviour regarding DTC setting as possible.
- Table: Calibration of CAN DTCs, item10 The Common CAN electrical fault shall be increased by 3 at every test sample failed.

### 2745 — Common CAN electrical fault _ Test sample failed criteria
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Table: Calibration of CAN DTCs, item10 The reported value of the DTC fault detection counter shall increase when the ECU detects that at least one of the physical bus error flags is set.

### 2746 — Common CAN electrical fault _ Test sample passed criteria
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Table: Calibration of CAN DTCs, item10 The reported value of the DTC fault detection counter shall decrease when the ECU detects that none of the physical bus error flags is set.

### 2747 — Common CAN electrical fault _ TRC
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Default test run criteria shall be used for all physical bus faults.
- Table: Summary of CAN related external circuit faults, item10 The TRC to perform Common CAN electrical fault check shall be according to the general Test Run Criteria specified in [UDSonCAN_2] UDS Data.

### 2748 — Common CAN electrical fault _ UnconfirmedDTCLimit
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- 2748 v2Common CAN electrical fault _ UnconfirmedDTCLimit Generic DTC configuration shall be used for electrical faults to have as similar behaviour regarding DTC setting as possible Table: Calibration of CAN DTCs, item10 The Common CAN electrical fault DTC test shall use UnconfirmedDTCLimit = 5.

### 2749 — Common CAN electrical fault _Test period
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- A standard time shall be used in detecting all physical bus faults.
- Table: Summary of CAN related external circuit faults, item10 The physical bus error status shall be read periodically at least every 100 ms.

### 2750 — DTC Generic Test Run Criteria
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- Ensure correct setting of DTCs If not otherwise stated, Generic Test Run Criteria shall apply, see [UDSonCAN_2] UDS Data.

### 2764 — Permanent missing frame _ TRC 1
- 版本：v4 ｜ 验证方式：Analysis ｜ 适用：通用
- Only one ECU shall administer missing frame TRC to be sure the same TRC are used for all ECUs in the network.
- The missing frame master, and not the missing frame slaves, shall manage all the enabling and disable conditions (i.

### 2765 — Permanent missing frame _ TRC 2
- 版本：v7 ｜ 验证方式：Analysis ｜ 适用：通用
- Missing frame DTCs shall be set in a predictable fashion (i.
- Table: "Summary of CAN related external circuit faults" Item 3 and 4 The missing frame detection shall only be based on periodic frames sent in at least the usage mode "Driving".

### 2766 — Permanent missing frame
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- 2766 v2Permanent missing frame Permanent missing frame DTCs shall be used since it may in some cases help pinpointing the location of a network problem as well as proving a rough functional test on operability of an ECU.

### 2767 — Permanent missing frame _ Test period missing frame master frame reception
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- Missing frame master shall base its permanent missing frame DTC detection on a signal frame reception timeout.
- Table: "Summary of CAN related external circuit faults" Item 3 The missing frame master shall be configured to receive the periodically transmitted frame from each missing frame slave within the supervised network.

### 2768 — Permanent missing frame _ Test period missing frame slave
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Table: "Summary of CAN related external circuit faults" Item 3 Each missing frame slave shall periodically send at least one frame with a shorter periodicity than 100 ms.
- Secondly the send frequency of an existing frame shall be increased to match the 100 ms requirement.

### 2769 — Permanent missing frame _ Decrease FDC10 steps
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Permanent missing frame DTCs shall be set with filtering to be sure the validity of the DTC.
- Table: "Calibration of CAN DTCs" Item 3 The permanent missing frame FDC10 shall be decreased by 9 at every test sample passed.

### 2770 — Permanent missing frame _ DTC ID
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The OEM shall define which DTC ID to use to minimize differences in between different ECUs, so that administration is kept to a minimum.
- Table: "Summary of CAN related external circuit faults" Item 3 The permanent missing frame DTC ID shall be as defined in [UDSonCAN_10] Global Master Reference Database.

### 2771 — Permanent missing frame _ DTCAgedLimit
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Table: "Calibration of CAN DTCs" Item 3 The permanent missing frame DTC shall use DTCAgedLimit = 255.4.5.6 UDSonFR4.5.6.1 UDSonFR - Slave Frame Miss4.5.6.1.1 Unified diagnostic services implementation4.5.6.1.1.1 Diagnostic trouble code information

### 2772 — Permanent missing frame _ DTCConfirmedLimit
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- Permanent missing frame DTCs shall be set with filtering to be sure the validity of the DTC.
- Table: "Calibration of CAN DTCs" Item 3 The permanent missing frame DTC shall use DTCCConfirmedLimit = 3.

### 2773 — Permanent missing frame _ Failure type
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The OEM shall define which failure type that shall be used to minimize the differences in between different ECUs, so that administration is kept to a minimum.
- Table: "Summary of CAN related external circuit faults" Item 3 For permanent missing frame DTCs the failure type 0x00 shall be used.

### 2774 — Permanent missing frame _ FDC10 max value
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- If a permanent missing frame occurs it is assumed it has big impact on the functionality of the system and hence it shall be able to set the confirm bit.
- Table 3 item 3 The DTC test for permanent missing frame shall have FDC10 max value = 127

### 2775 — Permanent missing frame _ Increase FDC10 steps
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Permanent missing frame DTCs shall be set with filtering to be sure the validity of the DTC.
- However the DTC must be set within 3 seconds to not have a gap in between permanent and intermittent missing frame detection.
- Table: "Calibration of CAN DTCs" Item 3 The missing frame permanent FDC shall be increased by 9 at every test sample failed.

### 2776 — Permanent missing frame _ Test period missing frame master
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Define how long time the missing frame master shall wait for each frame.
- Table: "Summary of CAN related external circuit faults" Item 3 The missing frame master shall check permanent missing frame DTCs every 150ms-170ms.

### 2777 — Permanent missing frame _ Test sample failed criteria
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The missing frame master shall be able to detect when the missing frame slaves fails to send their respective periodic frame.
- Table: "Calibration of CAN DTCs" Item 3 The reported value of the DTC fault detection counter, for a specific ECU, shall increase when the missing frame master have not received the periodic missing frame slave frame, for that specific ECU, in the test period time.

### 2778 — Permanent missing frame _ TRC 10
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- Table: "Summary of CAN related external circuit faults" Item 3 and 4 If a missing frame master does not receive the missing frame TRC no missing frame DTCs shall be set.

### 2779 — Permanent missing frame _ TRC 11
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Table: "Summary of CAN related external circuit faults" Item 3 and 4 Missing frame tests shall never be done when fault is detected on the parameters used as test run criteria (e.

### 2780 — Permanent missing frame _ TRC 3
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- Table: "Summary of CAN related external circuit faults" Item 7.3 and 7.4 All parameters used as test run criteria for missing frame tests shall be received outside the network that is being tested.

### 2781 — Permanent missing frame _ TRC 4
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- It must be possible to have different network configurations in regards of mounted ECUs on a network, without the missing frame master reporting missing slaves.
- Table: "Summary of CAN related external circuit faults" Item 3 and 4 The testing for missing frames shall only be done when the frame is expected;
- missing frame master shall be configured such that it is aware if an optional missing frame slave is present (mounted or not) on the bus or not.

### 2782 — Permanent missing frame _ TRC 5
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- The missing frame master shall be aware of different operation modes preventing the missing frame slaves to send frames.
- The missing frame master shall be aware when the missing frame slave is prevented from sending frames and shall not set any missing frame DTCs during this these modes.

### 2783 — Permanent missing frame _ TRC 6
- 版本：v5 ｜ 验证方式：Test ｜ 适用：通用
- Missing frames shall only be tested during usage modes when all ECUs are expected to be active.
- Table: "Summary of CAN related external circuit faults" Item 3 and 4 Missing frame tests shall only be done when the ECU is the usage mode "Driving"

### 2784 — Permanent missing frame _ TRC 7
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- Missing frames shall only be tested during usage modes when all ECUs are expected to be active and non-transient operation mode.
- Table: "Summary of CAN related external circuit faults" Item 3 and 4 Missing frame tests shall never be done during combustion engine crank.

### 2785 — Permanent missing frame _ TRC 8
- 版本：v5 ｜ 验证方式：Test ｜ 适用：通用
- To ensure missing frame DTCs are not falsely set due to differences in ECU power-up times, missing frames shall only be tested during non-transient conditions.
- Table: "Summary of CAN related external circuit faults" Item 3 and 4 The missing frame master shall never set TRC true until 5±2 seconds after all criteria for a DTC test, for permanent and intermittent missing frame DTCs, to run, is satisfied.

### 2786 — Permanent missing frame _ TRC 9
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- Missing frames shall only be tested within the battery voltage when communication networks shall be active.
- Table: "Summary of CAN related external circuit faults" Item 7.3 and 7.4 The voltage of the vehicle battery Ubat, shall be within: 10,0 ≤ Ubat ≤ 15,4V.
- Note: The battery voltage shall be measured as close to the battery as possible in order to minimize the measuring fault.

### 2787 — Permanent missing frame _ UnconfirmedDTCLimit
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Table: "Calibration of CAN DTCs" Item 3 The permanent missing frame DTC test shall use UnconfirmedDTCLimit = 18.

### 2788 — Permanent missing frame _ Test sample passed criteria
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The missing frame master shall be able to detect when the missing frame slaves succeeds in sending their respective periodic frame.
- Table: "Calibration of CAN DTCs" Item 3 The reported value of the DTC fault detection counter, for a specific ECU, shall decrease when the missing frame master have received the periodic missing frame slave frame, for that specific ECU, in the test period time.

### 2789 — Separating type of electrical fault
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Defining what the cause of the electrical fault may help in the fault tracing process.
- Table - Summary of CAN related external circuit faults The following faults specified in Table - Summary of CAN related external circuit faults may be identified by one common DTC, the DTC specified by item 10 of the table, instead of one single DTC for each fault if approved by CEVT Electrical Architecture: Item 5: CANH circuit short to battery voltageItem 6: CANL circuit short to groundItem 7: CANH circuit short to groundItem 8: CANL circuit short to battery voltageItem 9: CANH circuit short to CANL circuit.

### 2790 — Network management history record data
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Section "Record data" Each ECU shall implement one CAN network management state history buffer DID per CAN network the ECU is connected to.
- The network management state history buffer DID shall follow the definition specified in [UDSonCAN_7] Autosar Network Management - additional requirements.

### 2791 — Network management state history buffer _ Identifier
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- Define the record data DID Section "Record data" CAN ECUs shall implement network management state history buffer DID as defined in[UDSonCAN_10] Global Master Reference Database.4.5.5.2.2.2 Diagnostic trouble code informationThe table below specifies additional CAN requirements relative the general set of requirementsin [UDSonCAN_2] UDS Data.
- MC2 Mandatory if the ECU is not the network configuration masterNotes inthe table above: If not otherwise stated, Generic Test Run Criteria shall apply, see [UDSonCAN_2] UDSData.
- Following aspects of missing frame TRC have to be considered: The missing frame master, and not the missing frame slaves, shall manage all the enabling and disable conditions (i.

### 2908 — Dynamically resize frame length
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- To require that the dynamical resize mechanism shall be used.
- The sender of a message shall dynamically resize the frame payload length if the message is shorter that the maximum defined payload.

### 2909 — Unused data bytes
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The unused data bytes of a FlexRay frame shall be padded with zero (0x00).
- An ECU shall not reject a received FlexRay frame with non-zero pad bytes, however.4.3.8.1.1.5.1 Payload length, diagnostic responsesThe maximum frame payload length used for diagnostic responses shall be 32 bytes.
- These frame payload lengths stated in Table: Typical example network Slot ID configuration for application operation, shall be regarded as a recommendation.4.3.8.1.2 IntroductionThis specification is applicable for diagnostic messages in both software download (i.

### 2944 — DTC Generic Test Run Criteria
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- If not otherwise stated, Generic Test Run Criteria shall apply, see [UDSonFR_3] UDS Data.

### 2945 — Permanent missing frame _ Test period missing frame slave
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Table: Summary of FlexRay related faults, item8 Each missing frame slave shall periodically send at least one frame with a shorter periodicity than 100 ms.
- Secondly the send frequency of an existing frame shall be increased to match the 100 ms requirement.

### 2987 — Application layer
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- The application layer shall be compliant with [UDSonIP_14] ISO 14229-5: Road vehicles —Unified diagnostic services (UDS) — Part 5: Unified diagnostic services on Internet Protocol implementation (UDSonIP).4.5.7.1.2 Unified diagnostic service implementationThis section specifies the diagnostic services and data required for an IP ECU.4.5.7.1.2.1 Diagnostic servicesThe required diagnostic service are defined in [UDSonIP_1] UDS Services with the restrictions and additions in subsequent subsections.
- The Response Message Type for this service shall be of type#2 format.

### 2989 — Diagnostic routing or switching
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- Section "Overview", IP Routing Specification ECUs that shall route or switch diagnostic messages shall support applicable parts of routing or switching in accordance to IP Routing Specification, UDSonIP, Requisite documents.4.5.7.2 UDSonIP - IP Router Switch ECU reqs4.5.7.2.1 Detection of no Ethernet link to ECUThe IP Router/switch ECU shall discover when there is no Ethernet link to the IP ECU.
- The polling shall be performed periodically when the IP ECU's conditions for communicating as well as the conditions for performing diagnostics are met.

### 2990 — ReadDataByPeriodicIdentifiers Response Message Type
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Section "ReadDataByPeriodicIdentifier", UDS Services The Response Message Type for ReadDataByPeriodicIdentifier(0x2A) shall be a type #2 format.
- TRC1 TRC1 shall include the Generic Test Run Criteria from [UDSonIP_2] UDS Data and shall also include voltage for communication in accordance to [UDSonIP_6] Ethernet Physical Layer.
- Test sample failed criteria Increase FDC (# of steps) Test sample passed criteria Decrease FDC (# of steps) Unconfirmed DTC Limit FDC 10 max value DTC Confirmed Limit DTC Aged Limit 1 The reported value of the DTC fault detection counter shall increase when the Ethernet Link value indicates no link.

### 2991 — Ethernet Error Message Counter data record
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- To support test and verification during development A data record with identifier 0xD240 shall be implemented exactly as defined in [UDSonIP_12] Global Master Reference Database.
- The 4 byte counter shall stop counting when it has reached its maximum value, i.
- it shall not act as a rolling counter.

### 2992 — Ethernet Error Message Counter History data record
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- A data record with identifier 0xD230 shall be implemented exactly as defined in [UDSonIP_12] Global Master Reference Database.
- The data record shall consist of the ten latest driving cycles where error messages on the Ethernet link occurred.
- Each error message event shall consist of a 4 byte counter value and a timestamp.

### 2993 — Ethernet Link Status data record
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- A data record with identifier 0xD250 shall be implemented exactly as defined in [UDSonIP_12] Global Master Reference Database.
- Read access: It shall be possible to read the data record 0xD250 by using services specified in [UDSonIP_1] UDS Services in all diagnostic sessions in which the service used for read the data record is supported, except programming session.

### 2994 — Extended Ethernet Link Status data record
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- A data record with identifier 0xD251 shall be implemented exactly as defined in [UDSonIP_12] Global Master Reference Database.
- Read access: It shall be possible to read the data record 0xD251 by using services specified in [UDSonIP_1] UDS Services in all diagnostic sessions in which the service used for read the data record is supported, except programming session.

### 2995 — Single Quality Index data record
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- A data record with identifier 0xD260 shall be implemented exactly as defined in [UDSonIP_12] Global Master Reference Database.
- Read access: It shall be possible to read the data record 0xD260 by using services specified in [UDSonIP_1] UDS Services in all diagnostic sessions in which the service used for read the data record is supported, except programming session.

### 2996 — VLAN Membership data record
- 版本：v2 ｜ 验证方式：- ｜ 适用：通用
- Verification Method: A data record containing information of the members that are part of the VLAN shall be implemented.
- If the ECU is member in more than one VLAN, the ECU shall implement a data record for each VLAN.
- The data record shall contain information regarding each VLAN member.

### 2997 — VLAN Priority record identifier
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- A data record with identifier 0xD02E shall be implemented exactly as defined in [UDSonIP_12] Global Master Reference Database.
- Read access: It shall be possible to read the data record 0xD02E by using services specified in [UDSonIP_1] UDS Services in all diagnostic sessions in which the service used for read the data record is supported, except programming session.
- Control access: It shall be possible to control the value of the data record 0xD02E, by using services specified in [UDSonIP_1] UDS Services in all diagnostic sessions in which the service used for read the data record is supported, except programming session.4.5.7.1.2.2.3 RoutinesRoutines shall be supported by the ECU according to the table below.

### 2998 — Ethernet Test Mode 1 routine
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The Ethernet Test Mode 1 routine with routine identifier 0xA001 shall be implemented as defined in [UDSonIP_12] Global Master Reference Database.
- Routine type: The routine shall be implemented as a type 2 routine according to definition in [UDSonIP_1] UDS Services.
- Routine access: It shall be possible to execute the routine by diagnostic service request specified in [UDSonIP_1] UDS Services in all diagnostic sessions in which the service is supported, except programming session.

### 2999 — Ethernet Test Mode 2 routine
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The Ethernet Test Mode 2 routine with routine identifier 0xA002 shall be implemented as defined in [UDSonIP_12] Global Master Reference Database.
- Routine type: The routine shall be implemented as a type 2 routine according to definition in [UDSonIP_1] UDS Services.
- Routine access: It shall be possible to execute the routine by diagnostic service request specified in [UDSonIP_1] UDS Services in all diagnostic sessions in which the service is supported, except programming session.

### 3000 — Ethernet Test Mode 3 routine
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The Ethernet Test Mode 2 routine with routine identifier 0xA003 shall be implemented as defined in [UDSonIP_12] Global Master Reference Database.
- Routine type: The routine shall be implemented as a type 2 routine according to definition in [UDSonIP_1] UDS Services.
- Routine access: It shall be possible to execute the routine by diagnostic service request specified in [UDSonIP_1] UDS Services in all diagnostic sessions in which the service is supported, except programming session.

### 3001 — Ethernet Test Mode 4 routine
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The Ethernet Test Mode 4 routine with routine identifier 0xA004 shall be implemented as defined in [UDSonIP_12] Global Master Reference Database.
- Routine type: The routine shall be implemented as a type 2 routine according to definition in [UDSonIP_1] UDS Services.
- Routine access: It shall be possible to execute the routine by diagnostic service request specified in [UDSonIP_1] UDS Services in all diagnostic sessions in which the service is supported, except programming session.

### 3002 — Ethernet Test Mode 5 routine
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The Ethernet Test Mode 5 routine with routine identifier 0xA005 shall be implemented as defined in [UDSonIP_12] Global Master Reference Database.
- Routine type: The routine shall be implemented as a type 2 routine according to definition in [UDSonIP_1] UDS Services.
- Routine access: It shall be possible to execute the routine by diagnostic service request specified in [UDSonIP_1] UDS Services in all diagnostic sessions in which the service is supported, except programming session.

### 3003 — Substitute Value In Ethernet Register routine
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The Substitute Value In Ethernet Register routine with routine identifier 0xA000 shall be implemented as defined in [UDSonIP_12] Global Master Reference Database.
- The value of the register shall only temporarily be substituted by the routine.
- After a restart of the ECU, register values shall return to the previous value stored in long term memory.

### 3004 — IP Router Switch ECU - Ethernet link_Base DTC value
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- Section "Detection of no Ethernet link to ECU" The IP Router/switch ECU shall implement one unique base DTC value for each ECU connected to it via Ethernet.

### 3005 — IP Router Switch ECU - Ethernet link_Decrease FDC steps
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- 3005 v1IP Router Switch ECU - Ethernet link_Decrease FDC steps Each time the Ethernet link is detected, the ECU shall consider the DTC as not set.
- Section "Diagnostic trouble code information", table "Calibrations of Ethernet DTCs", item 1 The Ethernet link FDC shall be decreased by 20 at every test sample passed.

### 3006 — IP Router Switch ECU - Ethernet link_Detection of no link for point-to-point connection on Ethernet
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Section "Detection of no Ethernet link to ECU" To detect if link exists for point-to-point connection on Ethernet, a link status bit on the Ethernet transceiver shall be used.

### 3007 — IP Router Switch ECU - Ethernet link_DTCAgedLimit
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Section "Diagnostic trouble code information", table "Calibrations of Ethernet DTCs", item 1 DTCs for no Ethernet link detection shall use DTCAgedLimit = 255.
- It may be the vehicle manufacturer or the ECU supplier diagnostic software designer.
- Tester A system that controls functions such as test, inspection, monitoring, or diagnosis of an on-vehicle electronic control unit and may be dedicated to a specific type of operators (e.

### 3008 — IP Router Switch ECU - Ethernet link_DTCConfirmedLimit
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- 3008 v1IP Router Switch ECU - Ethernet link_DTCConfirmedLimit Due to the nature of the DTC, the DTC shall be considered confirmed as soon as a test failed has been run.
- Section "Diagnostic trouble code information", table "Calibrations of Ethernet DTCs", Item 1 DTCs for no Ethernet link detection shall use DTCCConfirmedLimit = 3.

### 3009 — IP Router Switch ECU - Ethernet link_Failure type
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Section "Diagnostic trouble code information" DTCs for no Ethernet link detection shall use Failure Type 0x00.

### 3010 — IP Router Switch ECU - Ethernet link_FDC10 max value
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- 3010 v1IP Router Switch ECU - Ethernet link_FDC10 max value If Ethernet link error is detected it is assumed it has such a big impact on the functionality of the system that it shall cause setting the confirm bit of the DTC.
- Section "Diagnostic trouble code information", table "Calibrations of Ethernet DTCs", item 1 The DTC test for Ethernet link shall have FDC10 max value = 127.

### 3011 — IP Router Switch ECU - Ethernet link_Increase FDC steps
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- 3011 v1IP Router Switch ECU - Ethernet link_Increase FDC steps Each time the Ethernet link is not detected, the ECU shall consider the DTC as set.
- Section "Diagnostic trouble code information", table "Calibrations of Ethernet DTCs", item 1 The Ethernet link FDC shall be increased by 10 at every test sample fails.

### 3012 — IP Router Switch ECU - Ethernet link_No Ethernet link for point-to-point connections
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- The IP Routing/switch ECU shall monitor the ECUs connected to it via Ethernet to see if the Ethernet link is up.
- Section "Detection of no Ethernet link to ECU" The IP Router/switch ECU shall support DTC setting for detection of no Ethernet link between it self and the ECUs connected to it self via a point-to-point connection.

### 3013 — IP Router Switch ECU - Ethernet link_Test period
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- Section "Diagnostic trouble code information" The TRC to perform Ethernet link check shall be according to TRC1 in section Diagnostic trouble code information.

### 3014 — IP Router Switch ECU - Ethernet link_TRC 1
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- Besides the Generic Test Run Criteria, also voltage for communication on controller shall be fulfilled to be able to set DTC for no link for point-to-point connections on Ethernet.
- The operating voltage range for Ethernet network shall also be according to [UDSonIP_6] Ethernet Physical Layer.

### 3015 — IP Router Switch ECU - Ethernet link_UnconfirmedDTCLimit
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- 3015 v1IP Router Switch ECU - Ethernet link_UnconfirmedDTCLimit Due to the nature of the DTC, the DTC shall be considered unconfirmed as soon as a test passed has been run.
- Section "Diagnostic trouble code information", table "Calibrations of Ethernet DTCs", item 1 The Ethernet Link DTC test shall use UnconfirmedDTCLimit = 20.

### 3016 — Base DTC value for LIN slave node failure
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Summary of LIN related circuit faults" LIN network failure detection shall have one base DTC for each LIN slave and one base DTC for the LIN master.

### 3017 — Detection of faulty LIN physical bus
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Page No1301(1572) Table "Summary of LIN related circuit faults", Item 4 The LIN master shall be able to detect and set a Faulty LIN physical bus DTC.

### 3018 — Detection of faulty LIN response
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Table "Summary of LIN related circuit faults", Item 2 The LIN master shall be able to detect and set a Faulty LIN response DTCs.

### 3019 — Detection of faulty transmitted data
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Table "Summary of LIN related circuit faults", Item 1 The LIN master shall monitor the sent data on LIN and set a DTC when transmitted data does not match the data being read back.

### 3020 — Detection of missing LIN response
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- LIN slave diagnose response messages shall not be monitored since the LIN slaves may skip some frame requests.
- Table "Summary of LIN related circuit faults", Item 3 The LIN master shall be able to detect and set a missing LIN response DTCs when the master expects to receive but does not receive any LIN data at all.
- Diagnose response frames (LIN frame identifier 0x3D) shall not be monitored.

### 3021 — Detection of other LIN network faults
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- Support extended DTC coverage. Table "Summary of LIN related circuit faults", Item 5 It is mandatory that the LIN master set other LIN DTCs where the faults is detected by a fault monitor as part of the ECU functional requirements.

### 3022 — Failure type value for Faulty LIN physical bus
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Table "Summary of LIN related circuit faults", Item 4 Failure type byte for the Faulty LIN physical bus DTC shall be 0x01.

### 3023 — Failure type value for Faulty LIN response
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Table "Summary of LIN related circuit faults", Item 2 Failure type byte for Faulty LIN response DTC shall be 0x83.

### 3024 — Failure type value for Faulty transmitted data
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Table "Summary of LIN related circuit faults", Item 1 Failure type byte for Faulty transmitted data DTC shall be 0x86.

### 3025 — Failure type value for Missing LIN response
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Table "Summary of LIN related circuit faults", Item 3 Failure type byte for Missing LIN response DTC shall be 0x87.

### 3026 — Test period time for other LIN network faults
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- Table "Summary of LIN related circuit faults", Item 5 Test period for other LIN network faults shall be as defined by the implementer, but DTC test frequency below once every 100ms shall be avoided.

### 3027 — Test Run Criteria for detection of Faulty LIN physical bus
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Table "Summary of LIN related circuit faults", Item 4 The LIN master shall perform Faulty LIN physical bus DTC test on every transmitted LIN frame.

### 3028 — Test Run Criteria for detection of Faulty LIN response
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Table "Summary of LIN related circuit faults", Item 2 The LIN master shall perform a Faulty LIN response DTC test on every received LIN frame.

### 3029 — Test Run Criteria for detection of Faulty transmitted data
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Table "Summary of LIN related circuit faults", Item 1 The LIN master shall perform a Faulty transmitted DTC test on every transmitted LIN frame.

### 3030 — Test Run Criteria for detection of Missing LIN response
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Table "Summary of LIN related circuit faults", Item 3 The LIN master shall perform a Missing LIN response DTC test whenever a LIN frame response is expected, except for frame identifier 0x3D triggered responses.

### 3040 — Application layer
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- ECUs on LIN being involved with either diagnose or SWDL shall support the application layer services as specified in [UDSonLVDS_7] ISO 14229-7, with the restrictions/additions defined in the role specific chapter (i.

### 3041 — P2Server timing clarification
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- The LIN specification shall be followed in regards of how timing shall be measured but the actual values shall be as defined by [UDSonLVDS_3] UDS Session.4.5.9.2 UDSonLVDS - Generic LIN master4.5.9.2.1 Unified diagnostic services implementation4.5.9.2.1.1 Diagnostic Data4.5.9.2.1.1.1 Diagnostic trouble code informationThe diagnostic trouble codes each LIN master shall support are described in table Summary of LIN related circuit faults.

### 3042 — Data link and network layer
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- 3042 v1Data link and network layer Define data link to use on LIN LIN Data Link Layer Both the LIN master and LIN slave on LVDS shall support the data link and network layer as specified in [UDSonLVDS_5] LVDS Control Channel Datalink Layer, with the restrictions/additions defined in the role specific chapter (i.
- LIN master and LIN slave).4.5.9.1.4 Physical layerBoth the LIN master and LIN slave on LVDS shall support the physical layer as specified in [UDSonLVDS_6] LVDS Physical Layer, with the restrictions/additions defined in the role specific chapter (i.

### 3043 — Physical layer
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Define physical layer LIN Physical Layer Both the LIN master and LIN slave on LVDS shall support the physical layer as specified in [LVDS Physical Layer], with the restrictions/additions defined in the role specific chapter (i.
- In the case of any requirement conflict between this document and any of the referenced documents, the proposed solution to the conflict shall be approved by CEVT Electrical Architecture before the conflict is recognized as resolved.4.5.9.1.5.2 Definitions and Abbreviations Definition Description ECU ID Part of the ECU Address, unique identifier for each ECU on a network.
- It may be the vehicle manufacturer or the ECU supplier diagnostic software designer.

### 3044 — Session layer
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- ECUs on LIN being involved with either diagnose or SWDL shall support the session layer as specified in [UDSonLVDS_3]UDS Session, with the restrictions/additions defined in the role specific chapter (i.
- 4.5.9.1.1.1 Functional RequestA LIN master and LIN slaves on the LVDS network shall support SPRMIB on functional requests.
- The procedure when a LIN master on the LVDS network receives a functionally addressed request supporting diagnostic communication is the following:• The LIN master routes the request.• The LIN slave receives the request, sends an acknowledge response and performs the request.• The LIN master shall consider the diagnostic request as completed when a diagnostic response has been received from the LIN slave if the SPRMIB = FALSE.4.5.9.1.2 Transport layer

### 3045 — Transport layer
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- ECUs on LVDS being involved with either diagnose or SWDL shall support the transport/network layer as specified in [UDSonLVDS_4] LVDS Control Transport Layer, with the restrictions/additions defined in the role specific chapter (i.

### 3046 — Diagnostic data
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- Define data format of supported services on LIN Both the LIN master and diagnosable and/or reprogrammable LIN slaves shall support the diagnostic data as specified in [UDSonLVDS_2] UDS Data, with the restrictions/additions defined in the role specific chapter (i.

### 3047 — Diagnostic services
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- Both the LIN master (via routing messages) and LIN slave shall support the diagnostic services as specified in [UDSonLVDS_1] UDS Services, with the restrictions/additions defined in the role specific chapter (i.
- LIN master and LIN slave).4.5.9.1.7.2.1 LIN slave start of operation cycle time[UDSonLVDS_1] UDS Services specifies time an ECU may take performing start of operation cycle.
- In regards of LIN, this time is when the LIN master shall be able to respond on diagnostic requests from a tester.

### 3048 — Active Mode Received Input Failure
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- A DTC shall be set if there is an absence of LVDS link input while the receiver is in active mode.
- SWRS - LVDS Datalink Layer & Generic Requirements A transceiver ECU connected to a LVDS network shall be able to detect an absence of LVDS link input while the receiver is in active mode.
- When detected, the ECU shall set the DTC – Active Mode Received Input Failure.

### 3049 — Lock PLL Failure
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- A DTC shall be set when the LVDS channel fails to lock PLL.
- SWRS - LVDS Datalink Layer & Generic Requirements A receiver ECU connected to a LVDS network shall be able to detect a failure in locking PLL.
- When detected, the ECU shall set the DTC Lock PLL Failure.

### 3050 — LVDS Chipset Internal Error
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- An internal error in the LVDS chipset causes the stream not to be sent correctly, hence a DTC shall be set when this occurs.
- SWRS - LVDS Datalink Layer - Generic Requirements An ECU connected to a LVDS network shall be able to detect an internal error in the LVDS chipset.
- When detected, the ECU shall set the DTC - LVDS Chipset Internal Error.

### 3051 — LVDS Video Frame Alignment Loss
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- A DTC shall be set when the Video frame alignment of LVDS is missing.
- Generic Requirements A receiver ECU connected to a LVDS network shall be able to detect a loss of Video frame alignment on the LVDS link.
- When detected, the ECU shall set the DTC LVDS Video Frame Alignment Loss.

### 3052 — Stream Clock Sync Failure
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- A DTC shall be set if there is a failure in the synchronization to the clock in the received stream of the LVDS link.
- Generic Requirements A receiver ECU connected to a LVDS network shall be able to detect a failure in the synchronization of the LVDS link to the received stream clock.
- When detected, the ECU shall set the DTC - Stream Clock Sync Failure.

### 3053 — Video Display Internal Error
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- A receiver ECU connected to a LVDS network shall be able to detect an internal error causing the video not to be displayed correctly.
- When detected, the ECU shall set the DTC - Video Display Internal Error.
- The base DTC value shall be in the range of DTCs that are needed only during the development or quality tracking (refer to [UDSonLVDS_2] UDS Data for definition of this range and requirements on DTC in this range) and as defined in Global Master Reference Database.

### 3054 — Access to VerifyLinkCommunication - SetEqualizationParameters routine
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- It shall be possible to run the control routine from default session, extended session and programming session.
- It shall be possible to execute the VerifyLinkCommunication – SetEqualizationParameters routine, by diagnostic services specified in [UDSonLVDS_2] UDS Data, when the ECU is executing the default session, extended session and the primary and secondary bootloader in programming session.4.6 Software Download4.6.1 General Software Download4.6.1.1 Generic SWDL4.6.1.1.1 Definitions and Abbreviations Definition Description Broken software The software present in the ECU is only partly downloaded.
- Tester A system that controls functions such as test, inspection, monitoring, or diagnosis of an on-vehicle electronic control unit and may be dedicated to a specific type of operators (e.

### 3055 — VerifyLinkCommunication - SetEqualizationParameters routine
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The VerifyLinkCommunication – SetEqualizationParameters routine with routine identifier 0x800F shall be implemented as defined in Global Master Reference and in [UDSonLVDS_5] LVDS Control Channel Datalink Layer document.

### 3056 — VerifyLinkCommunication - SetEqualizationParameters routine type
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The control routine shall be implemented as a type 1 routine.
- The VerifyLinkCommunication – SetEqualizationParameters routine shall be implemented as a type 1 routine.

### 3061 — LVDS UART Frame Alignment Loss
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- A DTC shall be set when the UART frame alignment of LVDS is missing.
- SWRS - LVDS Datalink Layer & Generic Requirements An ECU connected to a LVDS network shall be able to detect a loss of UART frame alignment on the LVDS link.
- When detected, the ECU shall set the DTC - UART LVDS Frame Alignment Loss.

### 3062 — Access to VerifyLinkCommunication - RunPRBSTestReceiver routine
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- It shall be possible to run the control routine from extended session and programming session.
- Item 2 of Table i Control routines for ECUs on the LVDS network It shall be possible to execute the VerifyLinkCommunication – RunPRBSTestReceiver routine, by diagnostic services specified in [UDSonLVDS_2] UDS Data, when the ECU is executing the extended session and the primary and secondary bootloader in programming session.

### 3063 — Access to VerifyLinkCommunication - RunPRBSTestTransceiver routine
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- It shall be possible to run the control routine from extended session and programming session.
- Item 1 of Table i Control routines for ECUs on the LVDS network It shall be possible to execute the VerifyLinkCommunication – RunPRBSTestTransceiver routine, by diagnostic services specified in [UDSonLVDS_2] UDS Data.

### 3064 — Access to VerifyLinkCommunication - SetPreemphasisParameters routine
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- It shall be possible to run the control routine from default session, extended session and programming session.
- It shall be possible to execute the VerifyLinkCommunication – SetPreemphasisParameters routine, by diagnostic services specified in [UDSonLVDS_2] UDS Data.

### 3065 — VerifyLinkCommunication - RunPRBSTestReceiver routine
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The VerifyLinkCommunication – RunPRBSTestReceiver routine with routine identifier 0x800D shall be implemented as defined in Global Master Reference Database and in [UDSonLVDS_5] LVDS Control Channel Datalink Layer document.

### 3066 — VerifyLinkCommunication - RunPRBSTestReceiver routine type
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The control routine shall be implemented as a type 3 routine.
- The VerifyLinkCommunication – RunPRBSTestReceiver routine shall be implemented as a type 3 routine.

### 3067 — VerifyLinkCommunication - RunPRBSTestTransceiver routine type
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The control routine shall be implemented as a type 3 routine.
- The VerifyLinkCommunication – RunPRBSTestTransceiver routine shall be implemented as a type 3 routine.

### 3068 — VerifyLinkCommunication - SetPreemphasisParameters routine
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The VerifyLinkCommunication – SetPreemphasisParameters routine with routine identifier 0x800E shall be implemented as defined in Global Master Reference and in [UDSonLVDS_5] LVDS Control Channel Datalink Layer document.

### 3069 — VerifyLinkCommunication - SetPreemphasisParameters routine type
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The control routine shall be implemented as a type 1 routine.
- The VerifyLinkCommunication – SetPreemphasisParameters routine shall be implemented as a type 1 routine.

### 3070 — VerifyLinkCommunication - RunPRBSTestTransceiver routine
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The VerifyLinkCommunication RunPRBSTestTransceiver routine with routine identifier 0x800C shall be implemented as defined in Global Master Reference Database and in [UDSonLVDS_5] LVDS Control Channel Datalink Layer document.

### 3071 — Time routing incoming DiagnosticSessionControl
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The LIN slaves must be given a chance to start the operation cycle within the start of operation cycle timing.
- The DiagnosticSessionControl request shall be routed to the LIN network maximum 50ms after the LIN master have received the request.4.5.9.3.2 Unified diagnostic services implementation4.5.9.3.2.1 Diagnostic Services4.5.9.3.2.1.1 Mandatory LIN services and data recordsApart from LIN master DiagnosticSessionControl diagnosticSessionType programmingSession, the implementer is free to define when to actually send the diagnostic requests as long as the timing parameters defined in [UDSonLVDS_1] UDS Services are kept.

### 3072 — Master filters requests not addressed to present slave
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The LIN master shall know which LIN slave is supposed to be connected to the LVDS network and route physical addressed requests only if the requests are addressed to that LIN slave.

### 3073 — Master responsible for routing messages to correct network
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Since many networks could be connected to one LIN master ECU, the LIN master is responsible for routing the incoming messages to the correct network. The LIN master is responsible for routing messages to the correct sub-network connected in parallel to the mas

### 3074 — LIN master wait for LIN slave start of operation cycle time
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- To ensure a stable system there must be a time in between when the LIN slaves have completed the start of operation schedule and when the LIN master may start to read data from the LIN slave.
- As long as the implementer does not specify otherwise 100ms shall be added to the LIN slave start of operation cycle time (500 ms) before the LIN master starts to retrieve ECU info from LIN slaves.4.5.9.3.3 Transport Layer

### 3075 — LIN master DiagnosticSessionControl diagnosticSessionType programmingSession
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The LIN master shall route DiagnosticSessionControl diagnosticSessionType programmingSession requests on the LIN.
- The DiagnosticSessionControl request shall be routed to the LIN network.

### 3076 — LIN master ReadDataByIdentifier Application Diagnostic Database Part Number
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- A standard method shall be used by the LIN master to retrieve information from the LIN slaves.
- The data record Application Diagnostic Database Part Number shall be read on LIN via diagnostic requests.
- The LIN master shall present the Application Diagnostic Database Part Number as one of the data records in Private ECU(s) Application Diagnostic Database Part Number(s).

### 3077 — LIN master ReadDataByIdentifier Complete set of ECU private numbers
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- The diagnostic interface shall be used even when not directly used by the tester to primarily standardize the method used for retrieving information from the LIN slaves.
- The LIN master shall either read Complete ECU Part/Serial Number or corresponding info from the LIN slaves via reading each data identifiers separately.
- The LIN master shall present the Complete ECU Part/Serial Number as one of the data records in Complete Private ECU Part/Serial Number.

### 3078 — LIN master ReadDataByIdentifier ECU Core Assembly Part Number
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- A standard method shall be used by the LIN master to retrieve information from the LIN slaves.
- The data record ECU Core Assembly Part Number shall be read on LIN via diagnostic requests.
- The LIN master shall present the ECU Core Assembly Part Number as one of the data records in Private ECU(s) Core Assembly Part Number(s).

### 3079 — LIN master ReadDataByIdentifier ECU Delivery Assembly Part Number
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- A standard method shall be used by the LIN master to retrieve information from the LIN slaves.
- The data record ECU Delivery Assembly Part Number shall be read on LIN via diagnostic requests.
- The LIN master shall present the ECU Delivery Assembly Part Number as one of the data records in Private ECU(s) Delivery Assembly Part Number(s).

### 3080 — LIN master ReadDataByIdentifier ECU serial number
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- A standard method shall be used by the LIN master to retrieve information from the LIN slaves.
- The data record ECU serial number (0xF18C) shall be read on LIN via diagnostic requests.
- The LIN master shall present the ECU serial number (0xF18C) as one of the data records in Private ECU(s) Serial Number(s) (0xF13C).

### 3081 — LIN master ReadDataByIdentifier ECU Software Part Number(s)
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- A standard method shall be used by the LIN master to retrieve information from the LIN slaves.
- The data record ECU Software Part Number(s) shall be read on LIN via diagnostic requests.
- The LIN master shall present the ECU Software Part Number(s) as one of the data records in Private ECU(s) Software Part Number(s).

### 3104 — ECUs with multiple networks
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The bootloader shall only support software download from the network which is defined to be the incoming network for diagnostic communication.

### 3105 — Gateway requirement
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- To define the requirements with shall apply for an ECU which acts as a diagnostic gateway in the bootloader.
- An ECU which has more than one network connected that acts as a diagnostic gateway shall implement the requirements defined in [SWDL_8] Diagnostic and Bootloader Gateway.4.6.1.2.20 Additional bootloader requirements for secondary processorsSome ECU hardware architectures may include additional microcontrollers (secondary processors).
- This specification does not include any detail for this communication method and any such additional bootloader resource shall be defined by the implementer.

### 3106 — Interrupted communication to private ECU
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Interrupted communication to the private network ECU shall not prevent subsequent reprogramming The communication method implemented between the public ECU and the private ECU shall be protected such that erasing any or all of the programmable memory areas of the private ECU and removing the ECU power at any time shall not prevent the subsequent reprogramming of any normally programmable memory area in the private ECU.
- In addition, the complete or partial downloading of any non operational or partly operational software into the programmable memory areas of the private ECU shall not prevent the subsequent reprogramming of any normally programmable memory area.

### 3107 — Programming sequence for private ECU
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The programming and erasure of any memory area on a private ECU shall be implemented such that the tester programming sequence have the same format as for a memory area supported on the public connected ECU (i.
- e., the memory of the private ECU shall appear to be mapped into the memory space of the processor on the public ECU for the purposes of software download).
- Note: To keep the same programming sequence shall the private ECU share the same SBL as for the public ECU since only one SBL per ECU address is allowed.

### 3108 — Read information from a private ECU
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The public ECU is responsible to respond on the behalf of the private ECU regarding software and hardware part numbers as well as if the software stored on the private ECU is complete and compatible.4.6.1.2.19 Additional bootloader requirements for multiple networksSome ECU hardware architectures may include additional networks which are connected to an ECU.
- When developing the bootloader shall each requirement for respectively network be considered.
- This specification does not include any detail for how to merge the different bootloader implementation requirements and any such additional bootloader functionality shall be defined by the implementer.

### 3109 — Interrupted communication to the secondary processor
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Interrupted communication to the secondary processor shall not prevent subsequent reprogramming.
- The download communication method implemented on the secondary processor shall be protected such that aborting download or removing ECU power at any time during the download shall not prevent subsequent reprogramming.
- In addition the complete or partial downloading of any non operational or partly operational software into the secondary processor shall not prevent the subsequent reprogramming of any normally programmable memory area.

### 3110 — Programming sequence for secondary processors
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The programming and erasure of the additional memory areas shall be implemented such that the tester programming sequence have the same format as for a memory area supported on the main processor (in other words the memory of the secondary processors shall appear to be mapped into the memory space of the main processor for the purposes of software download).
- Note: To keep the same programming sequence shall the secondary processors share the same SBL since only one SBL per ECU is allowed.

### 3111 — Calibration and Customer data
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- To avoid re-calibration or re-installation of customer data after ECU programming, the calibration- or customer data shall be preserved.

### 3112 — Support for (un)compressed data
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- To decrease the time to download data the ECU shall support decompression of the received compressed data.
- To decrease the software download time of an ECU, compression of data stream to an ECU shall be used, while the ECU shall still support non-compressed data files.
- The ECU shall implement the decompression algorithm specified in the reference [Data Compression and Encryption].

### 3113 — Delta encoding
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- To reduce the time spent on the programming phase and the time spent in transfer over data communication networks. Delta encoding and decoding method is required when a data file that is contained within a software delivery exceeds 10MB in size.4.6.1.2.12 Cali

### 3114 — Disable monitoring and logging of DTCs
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The ECU shall ensure that the monitoring and logging of all diagnostic trouble codes (DTCs) is disabled when executing the bootloader (programmingSession).

### 3115 — Suspend non diagnostic communication
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Whenever an ECU is executing the bootloader, it shall ensure that non diagnostic communication e.
- From power on or reset initiated by the application the PBL shall start executing the initialization state where the PBL decide whether the application shall be started or not.
- The primary bootloader (PBL) shall have a time window (Timeout_Prog) for detection of the DiagnosticSessionControl service.

### 3116 — ProgSignature - CLEAR
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- To prevent unwanted bootloader activation The ProgSignature shall be cleared with a recommended value of 0x000000000000000000 by the bootloader before starting the application.

### 3117 — ProgSignature - SET
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The ProgSignature shall be written to a fixed address in the volatile memory, with a length of 8 bytes and a recommended value of 0x50726f675369676e (equal to text string "ProgSign" in ASCII-format) by the application after receiving the DiagnosticSessionControl(programmingSession) request.
- Note: The fixed address must be synchronized between the application and bootloader.4.6.1.2.5 ECU program modeProgram mode means that the ECU executing the primary or secondary bootloader.

### 3118 — File download order
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- No restrictions on the download order/sequence of the downloadable data files are allowed, with the exception of the SBL which shall be downloaded first.
- It shall be possible to download each data file separately without any requirements of downloading other data files before, exception is the SBL.
- Note: If an ECU Software Structure (ESS) is to be downloaded, it shall always be downloaded next to the SBL.

### 3119 — Handling of distribution relays
- 版本：v5 ｜ 验证方式：Test ｜ 适用：通用
- An ECU controlling the supply to other ECUs must ensure a stable supply during the transition from the application to the bootloader and vice versa.
- While the bootloader executes, all supplies that feed other ECUs shall be enabled.4.6.1.2.14 Internal data transfer speed

### 3120 — Internal data transfer speed
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- To improve the total programming time To improve the total programming time the internal transfer time between the bus communication controller and the memory (where the data is stored) shall not exceed the memory writing time.
- Note: The non-volatile memory itself shall set the dimensioning factor for a SWDL operation.4.6.1.2.15 Power consumption

### 3121 — Power Consumption
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- To minimize the power consumption in programming mode When an ECU executing either the primary or secondary bootloader, all of the ECU's I/O shall be set into a safe and minimize power consumption where components cannot be damaged and the area is safe for people working on the vehicle.
- Minimize power consumption means that the ECU only shall supply the necessary components to perform software download.4.6.1.2.16 TargetAllow any microprocessor based ECU to be configured and fully programmed at any assembly plant or dealership, via approved data links.
- The following requirement principles shall be met for software download to an ECU.

### 3123 — Separate memory sectors
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- To decrease the total programming time it shall be possible to replace only the specific data file that shall be replaced and not being forced to replace all software(s) that already is present in the ECU.
- Two or more data files shall not share a memory sector.
- 4.6.1.2.10 File download order The data files which are downloadable to the ECU shall be capable of being downloaded to the ECU individually or in any grouping combination independent of order.

### 3124 — Multiple processors - verification principle
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- + Analysis The logical block shall be verified by the target processor respectively, i.
- Hence, the main processor must forward a copy of the verification block, its signature and all data blocks belonging to the secondary processor.
- The actual number of downloaded data blocks, verification block excluded, shall be 1.

### 3125 — Multiple processors - Main processor SBL verification
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- + Analysis The main processor shall (at least) verify the data blocks dedicated to memory space of the main processor itself.
- The main processor shall forward the data blocks belonging to the secondary processor together with a copy of the verification block table.

### 3126 — Multiple processors - Secondary processor SBL verification
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- + Analysis The secondary processor shall first verify the verification block table and then the downloaded data blocks within its memory space.
- that a complete logical block must always be erased but delta requirement to only erase sectors that are altered (no eraseMemory requests are required by the client).
- (2) - The bootloader must always set the logical block to invalid, prior to the memory is altered,i.

### 3127 — Delta encoding - Verification
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The verification of a delta installation shall fulfill the same level of authenticityverification as for any other processing method.
- When a delta encoding processing method is used, following must (still apply): The final target shall be verified, i.
- The verification block table and CheckMemory parameters shall be generated from thetarget software and copied to the delta file when it is generated.

### 3128 — Erase Status Information
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- The ECU shall reserve some dedicated memory to the Erase Status Information.
- This information must be exclusively handled by the bootloader.
- If the logical block is "already erased" and an valid erase request is detected, the ECU shall not perform any erase operations.

### 3130 — Check Memory - verification of programmed data
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- This will inform the ECU that a software part is downloaded and that the authenticity verification of the stored data shall be started.
- for development and production units) The ECU shall start the authenticity verification of programmed data when the routineldentifier CheckMemory is received.
- It shall be possible to make two consecutive CheckMemory attempts (i.

### 3131 — Secondary Bootloader - Condition for activation
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- The authenticity of the secondary bootloader must be verified.
- The primary bootloader must ensure that the authenticity verification of the secondary bootloader is passed prior to it is activated.
- If the verification fails, the ECU shall remain in the primary bootloader and the volatile memory buffer shall be cleared.

### 3132 — Secondary Bootloader Verification of unused data
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The authenticity verification shall check that there is no data programmed to memory not part of the authenticated verification block table.
- The bootloader shall ensure that there is no SBL data programmed to memory that is not defined in the verification block table.4.6.1.2.2.6.7 Request Upload

### 3134 — Erase Identifier - restrictions
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- The erase identifier range(s) of the software part header must match a valid logical block.
- The ECU shall at an eraseMemory request verify that the erase startAddress and Length matches a logical block range, otherwise the ECU shall abort the request.
- If the eraseMemory request is valid, the ECU must ensure that the complete memory for the addressed logical block is erased.4.6.1.2.2.6.2 Request Download

### 3135 — Request Download - restrictions on number of addressed logical blocks
- 版本：v5 ｜ 验证方式：Test ｜ 适用：通用
- The ECU shall check that only one logical block is being updated for a single downloaded software part, i.
- a second logical block or some location not defined by the ESS at all, the ECU shall abort the RequestDownload and inform the client via a NRC.
- Anyhow, the download shall be aborted when it is detected.

### 3136 — RequestUpload - Restricted use
- 版本：v2 ｜ 验证方式：- ｜ 适用：通用
- Verification Method: If the RequestUpload service is supported by the ECU, the following areas shall be blocked and not possible to upload data from: (i) Boot area and where the verification function is stored(ii) Area where the public key is stored(iii) Area where validity status information is stored(iv) Area where any confidential key is storedNote: For intellectual properties rights (e.
- when the software part is encrypted at download), the service shall be used with care.4.6.1.2.2.7 Additional requirements for ECUs having multiple processorsThe term main processor is in this context used to define the microcontroller having the interface to the network used for software download.
- Figure - Additional processors - OverviewThe bootloader of the main processor must be able to identify the software parts belonging to a memory device at the secondary processor, typically by using an address offset, and transfer it accordingly.

### 3137 — Software authentication signing method and algorithms
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The ECU shall implement the default signing method as defined in [General Software Authentication].4.6.1.2.2.10 Software Authentication - Generic security requirementsThis section contains the generic Software Authentication security requirements.

### 3138 — Allocation of the Authenticity Verification function
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- The authenticity verification function shall be stored in a protected area.

### 3139 — Authenticity verification at every start-up
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- Define when the ECU authenticity verification shall be started (mandatory on condition) + Analysis If the ECU is able to fulfill the application start-up conditions, the authenticity verification shall be started every time the (main) application is to be started (via bootloader), typically at every ECU Reset or Power-Up.
- Hence, the validity status information shall not be permanently stored in the ECU.
- ECU internal secret keys shall be applied in that case, both the keys and MAC shall bestored in protected memory.

### 3140 — Authenticity verification at run time (main application running)
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- This requirement is optional. Authenticity checks could be performed at some time(s) when the main application is up and running. This run time check is to be performed by an additional trustworthy entity, a hardware secure module, and not the main application

### 3141 — Authenticity verification at software download (Program mode)
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- + Analysis The authenticity verification function shall always be performed at software download (installation).

### 3142 — Debug tools and ports
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- + Analysis The ECU must be protected from all kind of memory manipulations (e.
- via diagnostic services or debuggers) except the diagnostic services supported and specified by in Global Master Reference Database.4.6.1.2.3 Time window for PROG detectionIf not explicitly stated in respectively bootloader implementation specification shall the primary bootloader (PBL) have a time window (Timeout_Prog) for detection of the DiagnosticSessionControl service.
- This backdoor solution shall be used if the ECU believes it has valid software(s) present, but the application software is not correctly jumping to the PBL.

### 3143 — Logical Block - Properties
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- Define the constraints of a logical block The non-volatile memory for software download shall be divided into logical blocks that must start and end at the boundary of a flash sector.
- The logical blocks must not share a common flash sector, i.
- logical blocks must not overlap or contain another logical block.

### 3144 — Logical Block Declaration
- 版本：v5 ｜ 验证方式：Test ｜ 适用：通用
- To define the properties for each logical block + Analysis For each individual logical block, following properties must be defined:1.
- The verification block contains information (location and hash value) of the data blocks that shall have been programmed to the logical block.
- how to get the corresponding signature (mandatory) and where is shall be stored (optional).

### 3145 — Number of logical blocks
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- + Analysis The ECU shall contain at least one logical block.
- The maximum number of blocks shall be statically configured in the bootloader.

### 3146 — Programming of Logical Blocks
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- + Analysis Each logical block shall be possible to sign separately, i.
- each logical block must be possible to erase, program and verify independently in the ECU.

### 3147 — Software parts per logical block
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- The content (data blocks) of a software part must be within a single logical block range, i.
- two different logical blocks must not be addressed by a single software part.

### 3148 — ECU Software Structure Declaration
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- + Analysis The ECU Software Structure shall at least contain: A pattern known to the bootloader, defining the existence of the structure, i.
- But, the bootloader must know the properties of that logical block.

### 3149 — Erase memory when ECU Software Structure (ESS) is updated
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- + Analysis The complete programmable flash memory shall be erased when the logical block dedicated to the ESS is (internally) addressed for erasure, i.
- Note that a logical block shall be set to 'invalid' prior to it is erased.

### 3150 — Immediately apply ESS update
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The ESS updates must be applied immediately after being verified correctly, i.
- an initiation of the bootloader must not be required.
- EXE) shall be possible to program next to the ESS without requiring an ECU reset.

### 3151 — Reprogrammable ECU Software Structure (ESS)
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- The ESS shall be reprogrammable according to the Programming Sequence described in this document, i.

### 3152 — Restricted software download when no valid ESS stored
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- If there is no valid ESS stored, the software download must be restricted to the SBL and the logical block dedicated to the ESS only.
- That means that attempts to address other logical blocks shall be rejected.
- The ECU shall inform the tester of the aborted erase memory attempt or aborted request download.

### 3153 — Storage of the ECU Software Structure (ESS)
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- To reduce the complexity of the bootloader implementation with respect to ESS update use case and for the bootloader to know where to find the logical block definitions The ECU Software Structure (ESS) shall be stored at a reserved logical block (flash sector), i.

### 3154 — Validation of the ECU Software Structure
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- The ESS must be validated before the bootloader applies the ESS definitions.
- The minimum requirements are that it shall be verified as any other logical blocks and ensure that the complete memory is covered by the defined logical blocks.

### 3155 — Root ECU Software Structure Declaration
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- Define ESS properties that must be stored in a protected area known to, or part of, the bootloader.
- + Analysis The ECU shall in a protected (not possible to alter nor read) area statically store the definitions required to verify the logical block dedicated to the ECU Software Structure, i.
- 4.6.1.2.2.3 Erase Status InformationPer logical block, the bootloader shall able to identify if the logical block is erased or not.

### 3156 — Public Key storage
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- The trust anchor shall not be possible to manipulate, that could be used to bypass the protection.
- the public key, shall be stored in a protected (read-only) area, typically in a hardware secure module or a protected boot area.
- It shall be one-time-programmable.

### 3157 — Re-programmable initial development key
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- AND Test The ECU shall use an initial public key for development purposes.
- When the initial development key is stored in the ECU, the public key for production shall always be possible to program.
- When a valid public key has been programmed, the initial development key must no longer be used by the ECU.

### 3158 — Condition for a logical block to be valid
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- A logical block must be verified successfully with respect to its authenticity every time it has been altered, in order to be considered as valid.
- The verification shall be done on data in the non-volatile memory (i.
- the length must for some use cases be calculated (delta encoding).

### 3160 — Validity Status Information - Properties
- 版本：v6 ｜ 验证方式：Test ｜ 适用：通用
- Only a trusted entity must be able to store (alter) the validity information.
- if the block has passed- or failed the authenticity verification at software download, shall have a minimum length of 8 octets.
- One single value shall represent 'Valid' and all other values shall be interpreted as 'Invalid'.

### 3161 — Allocation of the Verification Block Table
- 版本：v4 ｜ 验证方式：Analysis ｜ 适用：通用
- The position of the verification block table must be known by the bootloader in order to perform the verification.
- The verification block must not be part of any other data block, as the verification block table contains hash values of all other data blocks, i.
- AND Test A verification block table as defined Req ID1600: Format of the Verification Block Table shall be stored in a separate data block.

### 3162 — Verification Block Table - Reserve space at application build process
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- + Analysis The application software build process must reserve memory space for the verification block table within a logical block.
- Any condition that triggers a change of memory (erase/write) of a logical block shall result in that the logical block is set to (or kept) invalid.
- triggered by a physical/functional EraseMemory, RequestDownload etc., request, the ECU must ensure that the validity status of the addressed logical block is set to invalidpriorto the actual memory erasure (or data write) operation is started.

### 3163 — Non-volatile memory for software storage
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- To be able to modify/upgrade stored software(s) All software(s) shall be stored in a non-volatile memory, SBL excluded.4.6.1.2.17 Data compression and encryptionTo decrease the time to download software to an ECU, compression of the data stream to an ECU shall be used.
- The ECU shall still support non compressed data files.

### 3164 — Time window (Timeout_Prog)
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The primary bootloader (PBL) shall have a time window (Timeout_Prog) of 5 ms (-0% / +10%) for detection of the DiagnosticSessionControl service.
- If a DiagnosticSessionControl service with diagnosticSessionType equal to programmingSession is received during the time window the ECU shall enter programmingSession state.
- 4.6.1.2.4 Enter the bootloader (PBL) from the applicationIf not explicitly stated in respectively bootloader implementation specification the application shall write a signature to the volatile memory after receiving the DiagnosticSessionControl(programmingSession) request.

### 3165 — Two level bootloader
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- For security and data integrity purpose the ECU shall support two levels ofbootloaders, PBL and SBL.
- An ECU shall support the software download concept by the use of two bootloaders;
- primary-and secondary bootloader.4.6.1.2.21.1 Primary Bootloader (PBL)The memory area containing the PBL shall be protected from erasure to eliminate thepossibility of accidentally erasing it, but if the processor architecture permits this protection tobe configured such that it is removable then the protection shall be set up such that it could beremoved if needed.

### 3166 — PBL can only write data to volatile memory
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Due to security and integrity purpose shall the PBL not be able to write orerase data in the non-volatile memory.
- The primary bootloader shall only be capable of writing data to the volatile memory.

### 3167 — PBL in non-volatile memory
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The PBL shall always be present in an ECU.
- The primary bootloader shall be pre-programmed in the non-volatile memory by the ECU manufacturer.

### 3168 — Pre-condition state of the ECUs IO
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- When an ECU executes the bootloader all I/O shall be set into state where components cannot be damaged and the area is safe for people working on the vehicle.
- The PBL must also enable any I/O that is required to power other ECUs that support software download.

### 3169 — Protected boot sector
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The memory area containing the PBL shall be protected from erasure to eliminate the possibility of unintentional erasure .
- Note: The protection shall be set up such that it could be removed if a special SBL were to be written for this purpose, however the standard SBL or the application shall not be able to overwrite or erase the PBL.4.6.1.2.21.1.1 Primary bootloader diagnostic data

### 3170 — Primary bootloader diagnostic data
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The PBL shall support the diagnostic data required in the programmingSession which are specified in [SWDL_6] UDS Data.

### 3171 — Primary bootloader diagnostic services
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The PBL shall support the diagnostic services required in the programmingSession which are specified in [SWDL_5] UDS Services.4.6.1.2.21.2 Secondary Bootloader (SBL)The SBL includes all routines for erase and program of data to the non-volatile memory.
- This means that all PBL diagnostic services shall be capable of being executed in the SBL, exception is reprogramming and activation of the SBL itself.
- After download activation of the SBL in the volatile memory it shall not be possible to make a new download to volatile memory, the ECU shall reject to execute the request with an NRC.

### 3172 — Prevent the possibility to download the SBL when already activated
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- After download and activation of the SBL in the volatile memory it shall not be possible to make a new SBL download to volatile memory, the ECU shall reject to execute the request with an NRC.
- Before the SBL activation request is received a new download of the SBL shall be possible to perform.

### 3173 — SBL in volatile memory
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The Secondary bootloader shall be stored in the volatile memory.

### 3174 — Support of erase and write data to non-volatile memory
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Only the Secondary Bootloader (SBL) shall be able to erase and write data to the non-volatile memory.
- The Secondary Bootloader shall upon request erase and write data to the ECU non-volatile memory, except for the non-volatile memory area containing the primary bootloader.

### 3175 — The SBL shall include all PBL functionality
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- The SBL shall include the complete PBL functionality.

### 3176 — Secondary bootloader diagnostic data
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The SBL shall support the diagnostic data required in programmingSession which are specified in [SWDL_6] UDS Data.

### 3177 — Secondary bootloader diagnostic services
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The SBL shall support the diagnostic services required in programmingSession which are specified in [SWDL_5] UDS Services.
- The program(s) may be copied and * used only with the written permission from Volvo Cars.
- i++ ){ /* Get matching byte from window */outByte = LZSS_window[ LZSS_MOD_WINDOW( matchPos + i ) ];/* Output byte */OutputByte(outByte, outBuf);/* Add matched byte to current window position */LZSS_window[ winPos ] = outByte;/* Increase window position */winPos = LZSS_MOD_WINDOW( winPos + 1 );}}}} /*End of file*/ 4.6.2.1.1.1.3 Implementation Advice Regarding DecompressionThe decompression algorithm shall be implemented by each ECU specified (elsewhere) to have this capability.

### 3178 — Complete and Compatible sequence diagram
- 版本：v5 ｜ 验证方式：Test ｜ 适用：通用
- Definition in which order the ECU shall validate the stored software(s).
- The ECU shall first check that all software parts are complete prior to the compatibility check is performed.
- If the ECU contains incomplete software(s) it shall not check whether the software(s) is compatible.

### 3180 — Complete and Compatible - Compatible function
- 版本：v3 ｜ 验证方式：Inspection ｜ 适用：通用
- The bootloader must always verify that the compatible function applied is available and is complete, i.

### 3181 — Complete&Compatible - Definition of being Compatible
- 版本：v4 ｜ 验证方式：- ｜ 适用：通用
- An ECU that is compatible shall always be able to enter Programming Session and be re-programmed.
- Note: The application must react accordingly, i.

### 3182 — Complete and Compatible - Complete function
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- This verification must be performed by a trusted entity, i.

### 3183 — Complete and Compatible - Definition of being Complete
- 版本：v3 ｜ 验证方式：- ｜ 适用：通用
- Verification Method: Demonstration To be considered complete, all expected software parts must have passed the authenticity verification (using signatures).
- Hence, the CompleteCompatibleFunction() shall return that a software part is complete or incomplete according to that verification result.
- Every exception must be agreed with CEVT.

### 3184 — CompleteCompatibleFunction - error handling
- 版本：v2 ｜ 验证方式：Inspection ｜ 适用：通用
- Define a error handling strategy, where a restricted approach is applied meaning that the application must not be started unless it is proven to be valid.
- In case of an unexpected fault during the CompleteCompatibleFunction() that prevents the function to be completed and the root cause cannot be derived to a specific software part, the ECU shall be considered as not complete (or not compatible respectively, dependent of the check that was not completed).
- This shall be indicated in the response to the routineldentifier(Check Complete & Compatible) request.

### 3185 — CompleteCompatibleFunction()
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- The CompleteCompatibleFunction() shall be implemented in a way that allows new or modified software part without an updated application(EXE).
- The CompleteCompatibleFunction() shall detect if any of the software parts are not as expected, missing, broken (partly downloaded), altered etc.

### 3186 — CompleteCompatibleFunction() return value
- 版本：v7 ｜ 验证方式：Test ｜ 适用：通用
- The return value from the CompleteCompatibleFunction() shall be 4 bytes long and bit coded and contain the type of failure and which software part(s) that has failed.
- The diagnostic database shall contain the actual return values for an ECU.
- Bit (4) shall be set to "0" if the ECU doesn't supports a software part (e.

### 3187 — Maximum time to perform the Complete&Compatible validation
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- The maximum time to perform the total Complete & Compatible sequence described in Figure - CompleteCompatibleFunction() shall not exceed 20ms.

### 3188 — Writing of received data
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- To decrease the total programming time the ECU shall start writing data to the non-volatile memory before the complete message is received.
- The ECU shall start writing data to the non-volatile memory before the complete message is received, decompression included if supported.
- The positive response shall be sent after all data included in the TransferData request is written to the non-volatile memory.

### 3240 — Data compression Method 1 parameters
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- State the compression method #1 parameters Data Compression The size of the sliding window in the LZSS compression method shall be 1024 bytes.

### 3241 — Data compression Method 1 parameters
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- State the compression method #1 parameters Data Compression The size of the look-ahead buffer in the LZSS compression method shall be 16 bytes.

### 3242 — Data compression Method 1 parameters
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- State the compression parameters Data Compression First bit in a compressed data segment shall indicate if the following data in the segment is an uncompressed byte or a position/length-pair.
- '1' indicates an uncompressed byte and '0' a position/length-pair.4.6.2.1.2.3 Compression Method #2 Requirements4.6.2.1.2.3.1 Data Compression 132947 v1 Data Compression Method 2 State the compression method #2 The data compression/decompression method #2 shall be LZMA.
- However, certain advanced users may need freely combine the values of different parameters.

### 3243 — Data compression method 1
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- State the compression method Data Compression The data compression method #1 shall be LZSS.

### 3352 — Application layer
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- ISO 14229-5 Road vehicles - Unified diagnostic services (UDS) - Part 5: Unified diagnostic services on Internet Protocol implementation (UDSonIP) The IP bootloader application layer shall be compliant with ISO 14229-5 Road vehicles — Unified diagnostic services (UDS) — Part 5: Unified diagnostic services on Internet Protocol implementation (UDSonIP).

### 3353 — Bootloader General SWDL requirements
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- Chapter ECU PROGRAM MODE The Edge Node bootloader, PseudoProgrammingSession state and the IP ECU bootloader shall implement the non network dependent requirement defined in General Software Download Specification.

### 3354 — Check ProgSignature in RAM
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- Chapter The Edge Node's flow chart - Init The ECU shall after a warm start check if the ProgSignature at fixed RAM address is SET.
- Note: The ProgSignature in RAM shall be written by the application when a DiagnosticSessionControl(programmingSession) received, the format and length of the ProgSignature is described in General Software Download Specification.

### 3355 — Clear ProgSignature
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- Chapter The Edge Node's flow chart - Init The bootloader shall CLEAR the ProgSignature variable according to Figure Edge Node flow chart - Init or Figure IP ECU flow chart - Init.

### 3356 — Cold or warm start detected
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- Chapter IP ECU flow chart - Init The ECU shall detect the type of start (cold or warm) and use that information to decide the next transition.

### 3357 — Cold start detected
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- There is a difference in actions between warm and cold start-up. This requirement defines the next transition when cold start is detected Chapter IP ECU flow chart - Init; Chapter The Edge Node's flow chart - Init When cold start is detected next step is to cl

### 3358 — Complete & compatible function
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- The ECU shall be able to detect if the current downloaded software is compatible or not.
- Chapter The Edge Node's flow chart - Init The ECU shall detect if the software is compatible or not, by using Complete & Compatible function specified in GeneralSoftware Download Specification.

### 3359 — Complete and compatible software(s)
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- To define the action when software is complete and compatible General Software Download Specification; Chapter IP ECU flow chart - Init; Chapter The Edge Node's flow chart - Init If the return value from the Complete & Compatible function is equal to PASSED, i

### 3360 — Complete hardware initiation when starting the ECU
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- e., write once registers, PLL- setup, memory re-map, interrupt vector table re-map, etc.) Chapter Edge Node's bootloader flow chart - Overview The ECU shall always start from reset, regardless if the reset was initiated by a diagnostic request or by power up.

### 3361 — Enter the bootloader from ECU application mode
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- Chapter: IP ECU flow chart - Application It must be possible to enter the bootloader from the application when the vehicle and the diagnostic client are connected over an Ethernet point-to-point link, by receiving the DiagnosticSessionControl(programmingSession) service only once and all the criteria, defined by application, have been met.

### 3362 — ProgSignature is not set
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- Chapter The Edge Node's flow chart - Init When the ProgSignature is not SET the ECU shall enter the “Clear ProgSignature in RAM” state.

### 3363 — ProgSignature is set
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- The purpose of setting the ProgSignature to a predefined value is to enter the "programmingSession" state Chapter IP ECU flow chart - Init; Chapter The Edge Node's flow chart - Init When the ProgSignature is SET the next step is to enter the “Clear ProgSignatu

### 3364 — Receive and process diagnostic programming session request
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- To define when the ECU shall be able to receive and process a diagnostic programming session request Chapter The Edge Node's flow chart - ProgrammingSession and Undefined state;
- Chapter IP ECU flow chart - ProgrammingSession When the ECU is in programmingSession state or Undefined state, the ECU shall be able to receive and process diagnostic programming session requests.

### 3365 — The reception of DiagnosticSessionControl(defaultSession)
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Chapter The Edge Node's flow chart - ProgrammingSession and Undefined state When the ECU received a diagnostic service DiagnosticSessionControl(defaultSession) request, the ECU shall make a reset, thus restarting the ECU from Init state.

### 3366 — The reception of DiagnosticSessionControl(programmingSession)
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Chapter: The Edge Node's PseudoProgrammingSession flow chart When the bootloader is in the programmingSession state and receives a DiagnosticSessionControl(programmingSession) request, the request shall not make the ECU to reset.
- The bootloader shall stay in the programmingSession state.

### 3367 — The reception of ECU Reset service
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Chapter The Edge Node's - Application When the ECU receives an ECUReset request, the ECU shall make a reset, thus restarting the ECU from Init state.

### 3368 — Trig a reset in ECU application mode
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- Chapter: IP ECU flow chart- Application The ECU application shall trig a reset on reception of aDiagnosticSessionControl(programmingSession) on a wired connection.

### 3369 — Warm start detected
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- There is a difference in actions between warm and cold start-up. Thisrequirement defines the next transition when warm start is detected. Chapter IP ECU flow chart - Init; Chapter The Edge Node's flow chart - Init When warm start is detected next step is to ch

### 3370 — Write ProgSignature
- 版本：v4 ｜ 验证方式：Analysis ｜ 适用：通用
- Chapter: IP ECU flow chart- Application When the ECU application receives a DiagnosticSessionControl(programmingSession) requeston a wired connection the ProgSignature shall be written to a fixed address in RAM.
- Additional shall thisbootloader also implement the non network dependent bootloader requirements described inGeneral Software Download Specification.
- The IP ECUs shall implement a TCP/IP for in-vehicle communication.

### 3371 — TCP for internal communication
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- To get a robust solution and future safe communication, diagnostic messages shall be sent on TCP.
- Chapter Edge Node's Network/transport layer TCP shall be used for interna diagnostic communication on IP based network, in accordance to Internetworks General Specification

### 3372 — TCP-IP layer
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- This requirement defines the aspects of a TCP/IP stack that shall be fulfilled from the OEMs point of view.
- Chapter IP ECUs Network/transport layer The IP Bootloader shall implement the Internetworks General Specification.

### 3373 — Diagnostic gateway
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- Diagnostic And Bootloader Gateway Specification ECUs which shall gateway diagnostic messages shall implement the applicable bootloader requirements specified in Diagnostic And Bootloader Gateway Specification.

### 3374 — Diagnostic router
- 版本：v4 ｜ 验证方式：Analysis ｜ 适用：通用
- IP routing and firewalling The IP bootloader which shall route diagnostic messages shall support the routing requirements applicable for a bootloader defined IP Routing and Firewalling Specification.

### 3375 — Session layer
- 版本：v4 ｜ 验证方式：Analysis ｜ 适用：通用
- Chapter The Edge Node's PseudoProgrammingSession flow chart The IP bootloader shall implement the session layer defined in UDS Session.

### 3376 — RequestDownload Service
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- To decrease the total software download time UDS Services The maxNumberOfBlockLenght shall be 16386 bytes.

### 3377 — TransferData Service
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The TransferData message length of 3842 bytes (0F02 hex) shall be supported independent if the parameter maxNumberOfBlockLenght returned in the RequestDownload service is larger,Note 1: The Diagnostic tester is normally using an interface towards the vehicle supporting message length larger than 4 kB, therefore it is required to support as large block lengths as possible to reduce the software download time.

### 3378 — IP ECU - Non complete or compatible software(s)
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- Chapter IP ECU flow chart - Init If the return value from the Complete & Compatible function is not equal to PASSED it means the ECU is either not complete or compatible, and therefore the ECU shall go to Programming Session state.

### 3379 — IP ECU - Bootloader startup sequence
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- Chapter: IP ECU bootloader flow chart - Overview The IP ECU shall implement a bootloader sequence in accordance to Figure: IPECUbootloader flow chart - Overview .
- The figure shows the order in which events shall take place.

### 3380 — IP ECU - Define T_EstablishedTCPconnection timeout
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- - If ProgSignature is set then T_EstablishedTCPConnection shall be set to 30 000 ms.- If ProgSignature is not set then T_EstablishedTCPConnection shall be set to 1000 ms.

### 3381 — IP ECU - Establish TCP connection
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- The ECU shall not end up in an infint loop if no TCP communication is established with the Edge node.
- Therefore the ECU shall evaluate if a connection is established to Edge node within a specific time,T_EstablishedTCPConnection.
- The IP ECU shall evaluate if TCP connection is established withinT_EstablishedTCPConnection timeout.

### 3382 — IP ECU - Incomplete or incompatible software
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- If there is no completely downloaded data or if software parts are not compatible to each other, it shall be possible to check for TCP connection again.

### 3383 — IP ECU - No PROG received within Timeout_Prog
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- To define next transition when noDiagnosticSessionControl(ProgrammingSession) request is received withinTimeout_Prog Chapter: IP ECU flow chart - Init If no DiagnosticSessionControl(ProgrammingSession) request on Ethernet is received withinTimeout_Prog the IP ECU shall enter the Complete & Compatible function

### 3384 — IP ECU - PROG received within Timeout_Prog
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Chapter IP ECU flow chart - Init When the IP ECU receives the diagnostic requestDiagnosticSessionControl(ProgrammingSession) on Ethernet within Timeout_Prog the IP ECU shall enter the "programmingSession" state.

### 3385 — IP ECU - Restart T_EstablishedTCPconnection
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- To define when T_EstablishedTCPconnection shall be started and restarted.
- The T_EstablishedTCPConnection shall be restarted when ProgSignature is cleared or application is not complete or compatible.

### 3386 — IP ECU - S3Server timer times out in the PBL
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- Chapter IP ECU flow chart - ProgrammingSession If S3server times out when running PBL, the ECU shall make a test on Complete and Compatible function and if Complete and Compatible function returns PASSED the ECU shall make a reset.

### 3387 — IP ECU - S3Server timer times out in the SBL
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- To define the behaviour when the S3server times out in SBL Chapter IP ECU flow chart - ProgrammingSession When the S3server times out when running SBL, the ECU shall make a reset.

### 3388 — IP ECU - TCPconnection is established after cold start.
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- When TCP connection is established after cold start, the IP ECU shall start listen to DiagnosticSessionControl, see Flow chart IP ECU bootloader flow chart - Init.

### 3389 — IP ECU - TCPconnection is established after warm start.
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- To define next step when TCP connection is established after warm start The IP ECU shall enter programmingSession, when TCP connection is established after warm start, see Flow charts IPECU bootloader flow chart – Init and IPECU bootloader flow chart - ProgrammingSession.

### 3390 — IP ECU - TCPconnection is not established after cold start.
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- The ECU shall be able to handle the scenario where no TCP connection is established in bootloader.
- When TCP connection is not established after cold start the IP ECU shall enter the Complete & Compatible function.

### 3391 — IP ECU - TCPconnection is not established after warm start.
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- The ECU shall be able to handle the scenario where no TCP connection is established in bootloader.
- When TCP connection is not established after warm start the IP ECU shall do a reset, see flow charts IPECU bootloader flow chart - Init and IPECU bootloader flow chart - ProgrammingSession.

### 3392 — IP ECU - DoIP Layer
- 版本：v4 ｜ 验证方式：Analysis ｜ 适用：通用
- DoIP Communication IP ECU shall support those parts of DoIP that are defined for in-vehicle DoIP Communication in DoIP Communication.

### 3456 — Application layer
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- LIN master and LIN slaves shall be compliant to the application layer services specified in [UDSonLIN_8] ISO 14229-7, with the restrictions/additions defined in the role specific chapter (i.

### 3457 — LIN master time out not receiving consecutive 0x78 NRCs
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- 3457 v1LIN master time out not receiving consecutive 0x78 NRCs Define max time a LIN master shall wait before the LIN master shall consider a diagnostic request to LIN to be completed, if no subsequent NRC 0x78 (requestCorrectlyReceivedResponsePending) are received.
- The LIN master shall consider a diagnostic request as timed out if the LIN master does not receive a new NRC 0x78 (requestCorrectlyReceivedResponsePending) 5000ms after sending the previous NRC 0x78 (requestCorrectlyReceivedResponsePending).

### 3458 — LIN master time out not receiving first NRC 0x78
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- 3458 v1LIN master time out not receiving first NRC 0x78 Define max time a LIN master shall wait before the LIN master shall consider a diagnostic request to LIN to be completed, if no NRC 0x78 (requestCorrectlyReceivedResponsePending) is received.
- The LIN master shall consider a physically addressed diagnostic request as timed out if the LIN master does not receive a 0x78 NRC (requestCorrectlyReceivedResponsePending) 100ms after the diagnostic request was sent.
- For diagnostic requests with SPRMIB = TRUE the time shall be 0 (i.

### 3459 — LIN slave being responsible of P2*Server timer
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Directly after the diagnostic request has been sent on LIN the LIN master shall repeatedly request the response until the reception of the response can be considered completed.

### 3460 — P2Server timing clarification
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- The LIN specification shall be followed in regards of how timing shall be measured but the actual values shall be as defined by [BL_LVDS_4] UDS Session.

### 3461 — Data link and network layer
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Define data link to use on LVDS LVDS Control Channel Datalink Layer LIN master and LIN slaves shall be compliant to the data link and network layer specified in [BL_LVDS_6] LVDS Control Channel Datalink Layer, with the restrictions/additions defined in the role specific chapter (i.

### 3462 — Physical layer
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Define physical layer LVDS Physical Layer LIN master and LIN slaves shall be compliant to the physical layer specified in [BL_LVDS_7]LVDS Physical Layer, with the restrictions/additions defined in the role specific chapter (i.
- It may be the vehicle manufacturer or the ECU supplier diagnostic software designer.
- Tester A system that controls functions such as test, inspection, monitoring, or diagnosis of an on-vehicle electronic control unit and may be dedicated to a specific type of operators (e.

### 3463 — Session layer
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- Define session layer for LIN LIN master (via routing messages) and LIN slaves shall be compliant to the session layer services required for the bootloader specified in [BL_LVDS_4] UDS Session, with the restrictions/additions defined in the role specific chapter (i.

### 3464 — LVDS master routing functional requests
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The LVDS master shall route functional diagnostic requests and since the SPRMIB is placed in the diagnostic request, the LVDS slave shall perform the interpretation of the SPRMIB.
- The LVDS master shall always route functional requests regardless value of SPRMIB.

### 3465 — LVDS master time to poll time for functional addressed responses
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The LVDS master shall poll for responses on functionally addressed diagnostic requests if SPRMIB = FALSE.
- If SPRMIB = FALSE the LVDS master shall consider a functional addressed diagnostic request completed when the LVDS master has sent the request on LVDS and has received a response from the slave i.
- the LVDS master shall poll for a diagnostic response (send frame identifier 0x3D) for functional addressed requests in the same way as for physical addressed requests.

### 3466 — LVDS slaves responding on functional requests
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Hence the slave ECU shall respond to functional addressed requests if SPRMIB = FALSE.
- LVDS slaves shall process functional addressed diagnostic requests, and after the request has been processed the LVDS slave shall respond in the same way as physical addressed diagnostic requests.4.6.5.1.2 Transport Layer

### 3467 — Transport layer
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- Define transport layer to use for LVDS LIN master and LIN slaves shall be compliant to the transport/network layer specified in [BL_LVDS_5] LVDS Control Transport Layer, with the restrictions/additions defined in the role specific chapter (i.

### 3468 — LIN scheduling interval
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Maximum utilization of the LIN network The LIN master shall run the LIN schedule table at least once every 10th ms and the allowed jitter is defined in either the corresponding platform specification or the LIN Data Link Specification.4.6.5.2.3 Unified diagnostic services implementation requirements4.6.5.2.3.1 Diagnostic Services

### 3469 — Buffer requirements on LIN master
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The buffering shall be enough for handling both parallel and queued requests simultaneously.
- Request message buffer - Rx (Physical addressed request): The LIN master shall have one diagnostic request buffer for each LVDS network connected to the LIN master, the size for the diagnostic request buffer shall be big enough to fit two complete diagnostic request messages (queued request).
- The LIN master shall have a FIFO queue to send the next message when the previous message completely has been transferred.

### 3470 — Concurrent LIN master and LIN slave diagnostic requests
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- The LIN master shall concurrent be able to receive and process diagnostic requests addressed to the LIN master itself during gateway to/from LIN slaves.
- This means the LIN master shall be able to be re-programmed during the same time as the LIN slave.

### 3471 — Requests to parallel networks
- 版本：v1 ｜ 验证方式：- ｜ 适用：通用
- The tester shall not need to consider limitations on LVDS.
- Verification Method: The LIN master shall be able to handle physical addressed diagnostic requests to more than one LVDS network connected in parallel.4.6.5.2.1.4 Buffer requirements on LIN Master

### 3472 — Queued requests
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The tester shall not need to consider limitations on LIN.
- The LIN master shall be able to queue physical addressed diagnostic requests to a LIN slave.
- The method the LIN master shall handle queued request shall be via FIFO buffering the second request.4.6.5.2.1.3 Parallel requests

### 3473 — Routing timing for frames to and from LVDS
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- When the LIN master receives a diagnostic request addressed to a LIN slave the LIN master shall route the request within the timing defined by the following parameters:·10ms scheduling incoming network requests.·10ms LIN schedule table.·n ms periodic schedule jitter as defined in either the corresponding platform specification or the LVDS Control Channel Datalink Specification.
- The same gateway timing requirement applies when the LIN master shall route the diagnostic response.

### 3474 — Master filters requests not addressed to present slave
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The LIN master shall know which LIN slave is supposed to be connected to the LVDS network and route physical addressed requests only if the requests are addressed to that LIN slave.

### 3475 — Master responsible for routing messages to correct network
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Since many networks could be connected to one LIN master ECU, the LIN master is responsible for routing the incoming messages to the correct network. The LIN master is responsible for routing messages to the correct sub-network connected in parallel to the mas

### 3476 — Comments
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- N/A Comments are allowed in the header section only and may appear within an expression as described in section Identifiers, reserved words, and expressions.
- Valid comments shall always be ignored by a VBF parser.

### 3477 — Header expression termination
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Data shall be contained in braces only if there is more than one set of data with the exception of description [see section Header section - description] and erase [see section Header section - erase] identifiers.
- In these cases, a single set of data shall also be contained in braces.

### 3478 — Header Identifiers
- 版本：v5 ｜ 验证方式：Test ｜ 适用：通用
- To define allowed header identifiers N/A Identifier is the name of a variable and IdentifierValue is the data assigned to the variable. Allowed identifiers are vbf_version, header, description, sw_part_number, sw_current_part_number, sw_version, sw_current_ver

### 3479 — IdentifierValue format
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- N/A Each element within an IdentifierValue shall either be an integer, real, string embedded within quotes, or a reserved IdentifierValue (reserved word).
- Unless otherwise specified, a valid expression shall always consist of the following format (where WS/CM is defined as any combination of white space characters and complete comments ).[WS/CM]identifier[WS/CM]=[WS/CM]IdentifierValue[WS/CM];[WS/CM ]When the IdentifierValue is enclosed within matching brace characters "{" and "}" as allowed by this specification, the format of the IdentifierValue (including braces) shall be as follows :{[WS/CM]IdentifierValue[WS/CM][,[WS/CM]IdentifierValue[WS/CM ]} ;
- where the optional field of [,[WS/CM]IdentifierValue[WS/CM]] may occur multiple times .

### 3480 — Integers
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- It shall be represented in hexadecimal format, start with the prefix "0x" and the following characters must be chosen from the string "0123456789abcdefABCDEF".

### 3481 — Non-printing characters
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Communication needs may be defined elsewhere and determined on logical level (in application SW-Cs) by Virtual Function Cluster (VFC) activation and deactivation criteras.
- Partial networking may improve energy efficiency by only activating currently needed networks and nodes.
- Text written outside the requirement tags in this section shall be regarded as complementing information and not as a requirement.

### 3482 — White space characters
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- A VBF parser shall always ignore valid white space characters unless otherwise specified in this document.

### 3483 — Data section - start
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- To define the start of the data section. N/A After the header section ends, the data section immediately follows. The header section ends with a } character (ASCII 0x7D). The binary data section begins with the next byte immediately following this ASCII } char

### 3484 — Data section - structure
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- N/A The data section may contain more than one block of data, and every block includes four parts.
- The Start address, Length, and Checksum fields shall always be stored with the most significant byte (msb) first.

### 3485 — Software part version in the data section
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- N/A The software part version containing sw_part_number and sw_version shall reside somewhere in the data section in the VBF file that is being programmed into the ECU and this downloaded part number shall be readable using service 0x22 (ReadDataByIdentifier).

### 3486 — Data block checksum
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- N/A The VBF file shall include a 2-byte checksum for every data block.
- The 2-byte checksum shall be calculated including all data bytes (excluding Start address, Length, and Checksum) in the data block.
- If a data compression method is used, the data block checksum shall be calculated using unprocessed data (i.

### 3487 — Header section
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The information between the braces in the header section shall consist entirely of expressions as defined in section 4.3.

### 3488 — Header section - Format
- 版本：v6 ｜ 验证方式：Test ｜ 适用：通用
- To define the format of the header section N/A ```ini GEELY Note-SWRS Revision 005 Document Release Status RELEASED Revision Volume No 01 Page No 1466(1572) The format of the header section is defined as follows (the grouping symbols [ ] indicates optional ide

### 3489 — call
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- To define the format and use of the call identifier. N/A The call entry is mandatory in VBF files with sw_part_type identifier values equal to SBL or SSBL and optional in VBF files with sw_part_type equal to TEST. For all other identifier values of sw_part_typ

### 3490 — data_format_identifier
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- // Invalid format (must be from 0x00 – 0xFF)2.
- // Invalid format (integers shall be hexadecimal)4.6.6.1.1.2.8 ecu_address

### 3491 — description
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The description IdentifierValue may contain a maximum of 16 rows, with each row containing a maximum of 80 characters (bytes).
- All of the description rows shall be contained within braces whether there is one row or multiple rows.

### 3492 — ecu_address
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- To define the format and use of the ecu_address identifier. N/A The ecu_address identifier indicates the physical target address of the ECU. The ecu_address is divided into three parts where the combination of Domain ID, Network ID and ECU ID is utilized. The 

### 3493 — erase
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- The erase identifier values shall always be contained in two sets of braces whether there is one or more ranges present.
- Note: If sw_part_type = SBL or SSBL, the VBF file shall not contain the erase identifier Note: If delta encoding is used (data_format_identifier = 0x80 or 0x90), the VBF file shall not contain the erase identifier Examples: Valid Format: 1.

### 3494 — file_checksum
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- N/A A four-byte file checksum shall be provided in the header section with a range of 0x00000000 to 0xFFFFFFFF.
- The checksum shall be a CRC32 of all the data contained in the data section of the file, including start address, length and checksum for all data blocks.
- The tester shall check this checksum against the file checksum it has calculated before the software download operation is performed with the VBF file.

### 3495 — sw_current_part_number
- 版本：v3 ｜ 验证方式：Inspection ｜ 适用：通用
- The sw_current_part_number IdentifierValue shall be contained in quotes and shall consist of a maximum of 20 characters.

### 3496 — sw_current_version
- 版本：v2 ｜ 验证方式：Inspection ｜ 适用：通用
- The sw_current_version IdentifierValue shall be contained in quotes and shall consist of a maximum of 4 characters (bytes).
- The sw_current_version IdentifierValue is case sensitive and shall only contain the uppercase characters A-Z.

### 3497 — sw_part_number
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- The sw_part_number IdentifierValue shall be contained in quotes and shall consist of a maximum of 20 characters.

### 3498 — sw_part_type
- 版本：v5 ｜ 验证方式：Test ｜ 适用：通用
- Only the reserved word IdentifierValues defined in the table below shall be considered valid for the sw_part_type identifier.
- These software types are downloaded to RAM and no erase operation shall be performed in this case.

### 3499 — sw_signature
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- The sw_signature shall be represented as an integer and the length is dependent of the signing method used.

### 3500 — sw_signature_dev
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The sw_signature_dev shall be represented as an integer and the length is dependent of the signing method used.

### 3501 — sw_version
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The sw_version IdentifierValue shall be contained in quotes and shall consist of a maximum of 4 characters (bytes).
- sw_version IdentifierValue is case sensitive and shall only contain the uppercase characters A-Z.

### 3502 — verification_block_length
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- To define the format and use of the verification_block_length identifier. The purpose of the identifier is to identify the length of the unprocessed data that is signed. The verification_block_length represents the unprocessed length (prior to compression/encr

### 3503 — verification_block_root_hash
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- The verification_block_root_hash shall be represented as an integer and the length is dependent of the hashing method used.

### 3504 — verification_block_start
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- To define the format and use of the verification_block_start identifier. The purpose of the identifier is to identify the start address of the data (unprocessed) that is signed. The verification_block_start represents the start address of the unprocessed data 

### 3505 — Version section
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- N/A The first line of the VBF file shall indicate the version of the VBF file.
- Note that this means the first byte of the VBF file shall always be 0x76 (i.
- This specification is for version 2.6 of the VBF file, and so the first line shall always read: vbf_version = 2.6;

### 3506 — File Naming
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- N/A All delivered or released VBF files shall be named the same as the corresponding released software part number which consist of (sw_part_number and sw_version) with an extension of ".
- shall utilize the file name of 31808832AB.
- shall utilize the file name of 31808832A.

### 3507 — VBF file generation
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- N/A The VBF Convert tool shall generate VBF files from Motorola S-record or Intel Hex formatted files.4.6.6.1.6 Notation and lexical elementsThe VBF file header section uses some basic lexical elements, which are described, in this section.
- The grouping symbols ( ), parentheses, contain a set of items separated by |, then one of the items must appear.4.6.6.1.6.2 General structure

### 3518 — Definition of TCANPowerWakeUpToApp
- 版本：v5 ｜ 验证方式：Test ｜ 适用：通用
- TCANPowerWakeUpToApp shall be equal to 150 ms.
- If another requirement define this time to be shorter that requirement shall override this requirement.

### 3519 — Definition of TCANResumeCom
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- TCANResumeCom shall be equal to 25 ms.
- If another requirement define this time to be shorter that requirement shall override this requirement.

### 3520 — Timing at power up or reset initialization CAN
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- For definition of node types see Node Types, Autosar Network Management(additional requirements) - Overview A node shall be ready to receive and transmit CAN frames maximumTCANPowerWakeUpToApp after power is applied, a hardware reset and a diagnosticECUReset(hardReset).

### 3521 — Timing at resumed communication CAN - relay powered/ignition sensing node
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- For definition of node types see Node Types, Autosar Network Management(additional requirements) - Overview If more than TCANPowerWakeUpToApp has passed since power on, a hardware reset or a diagnostic ECUReset(hardReset), a node shall be ready to receive and transmit application signals maximum TCANResumeCom after communication is requested by another node.
- Communication shall not be enabled until all conditions are fulfilled.

### 3522 — CAN network management history algorithm
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- pdf, Autosar Network Management (additional requirements) - External publications The state of the Autosar CAN network management state machine and additional conditions shall continuously be evaluated and prioritized according to the tables below.
- A new value shall be added to the history buffer if it differs from the last value that was added to the buffer.

### 3523 — Diagnostic trouble code for CAN bus-off
- 版本：v5 ｜ 验证方式：Test ｜ 适用：4.0.x
- For Autosar 4.0.3 and later see also CANSM522 For all Autosar versions: There shall be 32 detections of CAN bus off in CANSM until a DTC for CAN bus off is set to testFailed.
- A diagnostic trouble code (DTC) for CAN bus off shall be set within 100 ms according to [AR_NM_17] UDS Data.
- The number of CAN bus off events required until a DTC is set to testFailed shall be same regardless of Autosar version.

### 3525 — Timing at network and hardware wake up CAN - microcontroller powered in sleep
- 版本：v7 ｜ 验证方式：Test ｜ 适用：通用
- Network wakeup and hardware wakeup: A node shall be ready to receive and transmit CAN frames maximumTCANEventWakeUpToApp after network activity or a hardware sensor signal change (e.
- Note: Some nodes may be equipped with "selective wake up transceivers".

### 3526 — Timing at network and hardware wake up CAN - microcontroller unpowered in sleep
- 版本：v6 ｜ 验证方式：Test ｜ 适用：通用
- A node shall be ready to receive and transmit CAN frames maximum TCANPowerWakeUpToApp after network activity or a hardware sensor signal change (e.
- Note: Some nodes may be equipped with "selective wake up transceivers".
- Therefore attention must be paid on the hardware design as well even if this specification is called Autosar Network Management - additional requirements, and Autosar actually is a software architecture.

### 3529 — Definition of TFRResumeComSynchronized
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- TFRResumeComSynchronized shall be equal to 50 ms.
- If another requirement define this time to be shorter that requirement shall override this requirement.

### 3530 — Timing at resumed communication FlexRay - relay powered/ignition sensing node
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- If more than TFRPowerWakeUpToAppSynchronized has passed since power on, a hardware reset or a diagnostic ECUReset(hardReset, a node shall be ready to receive and transmit application signals maximum TFRResumeComSynchronized after communication is requested by another node.
- Communication shall not be enabled until all conditions are fulfilled.

### 3531 — FlexRay network management history algorithm
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- pdf, Autosar Network Management (additional requirements) - External publications The state of the Autosar FlexRay network management state machine and additional conditions shall continuously be evaluated and prioritized according to the following conditions.
- A new value shall be added to the history buffer if it differs from the last value that was added to the buffer.

### 3532 — Diagnostic trouble code for cluster startup error FlexRay
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- Unified diagnostic services (UDS) - Part 1: Specification and requirements - Data If the node is unable to synchronize to a schedule and FrSM reportsFE_DEM_STATUS_FAILED (transition T30) a diagnostic trouble code (DTC) shall be set according to [AR_NM_17] UDS Data .
- If Autosar FlexRay State Manager reports FE_DEM_STATUS_PASSED (transition T08, T108) the diagnostic trouble code shall be reported as tested and passed OK.

### 3533 — Definition of TFREventToNetworkWakeUp
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- TFREventToNetworkWakeUp shall be equal to 25 ms.
- If another requirement define this time to be shorter that requirement shall override this requirement.

### 3534 — Definition of TFREventWakeToAppSynchronized
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- TFREventWakeToAppSynchronized shall be equal to 75 ms.
- If another requirement define this time to be shorter that requirement shall override this requirement.4.7.1.7.1.1 Microcontroller is powered in sleep

### 3535 — Timing at network and hardware wakeup FlexRay - microcontroller is powered in sleep
- 版本：v5 ｜ 验证方式：Test ｜ 适用：通用
- FlexRay Communications System Protocol Specification Version 2.1, Revision A, 22-December-2005, Autosar Network Management (additional requirements) - External publications Network wakeup: A node shall synchronize to the FlexRay application schedule and receive and transmit Flexray frames in that schedule maximum TFREventWakeToAppSynchronized after network activity is detected by FlexRay transceiver.
- Hardware wakeup: When a hardware sensor signal change is detected that shall initiate network communication the waking node shall start transmission of a wake up pattern maximumTFREventToNetworkWakeUp after the hardware sensor signal change is detected.
- The node shall synchronize to the FlexRay application schedule and receive and transmit FlexRay frames in that schedule maximum TFREventWakeToAppSynchronized after the wake up pattern transmission is started.

### 3536 — Timing at network and hardware wake up FlexRay - microcontroller unpowered in sleep
- 版本：v6 ｜ 验证方式：Test ｜ 适用：4.0.x
- FlexRay Communications System Protocol Specification Version 2.1, Revision A, 22-December-2005, Autosar Network Management (additional requirements) - External publications Network wakeup: A node shall synchronize to the FlexRay application schedule and receive and transmit Flexray frames in that schedule maximum TFRPowerWakeToAppSynchronized after network activity is detected by FlexRay transceiver.
- Hardware wakeup: When a hardware sensor signal change is detected that shall initiate network communication the waking node shall start transmission of a wake up pattern maximumTFREventToNetworkWakeUp after the hardware sensor signal change is detected.
- A node shall synchronize to the FlexRay application schedule and receive and transmit Flexray frames in that schedule maximum TFRPowerWakeToAppSynchronized after a hardware sensor signal change is detected.

### 3537 — Network management state history buffers
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- Unified diagnostic services (UDS) - Part 1: Specification and requirements - Data specifies DID, Autosar Network Management (additional requirements) For each network connected to the node there shall be a separate network management state history buffer.
- Each buffer shall be updated with the last value derived from the respective network management history algorithm.
- There shall be a time stamp that relates to each value in all history buffers.

### 3538 — Storage and clearing of network management state history buffers
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- Page No1512(1572) Nodes Type D may not be noticed in advance of release of the control signal IGN, Clamp-15 which often is used to trigger write of data to persistent memory.
- Therefore this node type shall not be required to persistently store network management history buffer.
- Nodes Type A, Type B and Type C shall have persistent storage, i.

### 3539 — Minimum number of write events of history buffer
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：4.0.x
- FEE102, FEE103 in Autosar Specification of Flash EEPROM Emulation Node types that are required to have persistent storage of NM history buffers shall have hardware and software that allows persistent storage of history buffer data with minimum 100000 number of event where new state data is shifted into and written in the history buffer.
- Wear leveling algorithms in software shall be used to fulfill requirement if hardware memory does not on its own support the number of write events.
- The network from which a triggering condition to activate additional networks arise is called the source network, and the network that shall be woken up or change to be requested active by the node is called the destination network.

### 3540 — Definition of TCANGwNetworkRequest
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- To define the maximum time for gatewaying the network request TCANGwNetworkRequest shall be equal to 15ms.
- If another requirement define this time to be shorter that requirement shall override this requirement.

### 3541 — Definition of TCANWakeAndGwNetworkRequest
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- TCANWakeAndGwNetworkRequest shall be equal to 15 ms.
- If another requirement define this time to be shorter that requirement shall override this requirement.

### 3542 — Definition of TFRGwNetworkRequest
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- TFRGwNetworkRequest shall be equal to the transmit period of the FlexRay NM-PDU + 10 ms.
- If another requirement define this time to be shorter that requirement shall override this requirement.

### 3543 — Definition of TFRGwNetworkWakeUp
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- TFRGwNetworkWakeUp shall be equal to 10 ms.
- If another requirement define this time to be shorter that requirement shall override this requirement.

### 3544 — Timing at destination network wake up and gatewaying network request to CAN
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The network that shall become active is not active.
- If an application signal changes status, an NM-PDU or the content of a NM-PDU becomes active on a source network which shall lead to the activation of a CAN destination network which is not active, the node shall transmit the first NM-PDU on the CAN destination network and be ready to receive and transmit CAN frames maximumTCANWakeAndGwNetworkRequest after the activation condition became fulfilled on the source network.

### 3545 — Timing at destination network wake up and gatewaying network request to FlexRay
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- 3545 v1Timing at destination network wake up and gatewaying network request to FlexRay The network to which the network request shall be gatewayed is not active.
- If an application signal changes status, an NM-PDU or the content of a NM-PDU becomes active on a source network which shall lead to the activation of a FlexRay destination network which is not active, then transmission of a wake up pattern shall start maximum TFRGwNetworkWakeUp on the Flexray destination network after the triggering condition became fulfilled on the source network.
- The node shall transmit NM-PDU with NM-Vote that reflect the network request and be ready to receive and transmit FlexRay frames maximum TFREventWakeToAppSynchronized after the wakeup pattern was transmitted.

### 3546 — Timing at gatewaying network request to CAN
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- If an application signal changes status, an NM-PDU or the content of a NM-PDU becomes active on a source network which shall lead to the network request of a CAN destination network which is already activated by other nodes, the node shall transmit the first NM-PDU on the CAN destination network maximum TCANGwNetworkRequest after the activation condition became fulfilled on the source network.
- Note: Source network may be CAN or FlexRay and destination network is a CAN network.
- The logical condition for activation of the destination network shall be specified in another requirement.3547 v1 Timing at gatewaying network request to FlexRay To ensure sufficiently short response time when waking up a network and start gatewaying.

### 3548 — Definition of TCANGwPncRequest
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- To define the maximum time for gatewaying the PNC request TCANGwPncRequest shall be equal to 15ms.
- If another requirement define this time to be shorter that requirement shall override this requirement.3549 v2 Definition of TCANWakeAndGwPncRequest To define the maximum time to start communication and gatewaying the PNC request TCANWakeAndGwPncRequest shall be equal to 15 ms.

### 3550 — Definition of TFRGwPncRequest
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- To define the maximum time for gatewaying the PNC request TFRGwPncRequest shall be equal to the transmit period of the FlexRay NM-PDU + 10 ms.
- If another requirement define this time to be shorter that requirement shall override this requirement.

### 3551 — Definition of TFRPncEventToNetworkWakeUp
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- TFRPncEventToNetworkWakeUp shall be equal to 10 ms.
- If another requirement define this time to be shorter that requirement shall override this requirement.

### 3552 — Timing at destination network wake up and gatewaying PNC request to CAN
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- The network to which the PNC request shall be gatewayed is not active.
- If a PNC request becomes active on a source network and is to be gatewayed to a CAN destination network which is not active the node shall transmit the source PNC request in a NM-PDU on the CAN destination network and be ready to receive and transmit CAN frames maximum TCANWakeAndGwPncRequest after the source PNC request became active.
- The first NM-PDU transmitted on CAN destination network shall include the source PNC request that causes the destination network to become active.

### 3553 — Timing at destination network wake up and gatewaying PNC request to FlexRay
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- The network to which the PNC request shall be gatewayed is not active.
- If a PNC request becomes active on a source network and is to be gatewayed to a FlexRay network which is not active then transmission of a wake up pattern shall start maximum TFRPncEventWakeToNetworkWakeUp after the source PNC request became active.
- The node shall transmit the source PNC request in a NM-PDU on the FlexRay network and be ready to receive and transmit FlexRay frames maximum TFREventWakeToAppSynchronized after the wakeup pattern was transmitted.

### 3554 — Timing at gatewaying PNC request to CAN
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- The network to which the PNC request shall be gatewayed is already active, due to at least one other PNC request.
- If a PNC request becomes active on a source network and is to be gatewayed to a CAN destination network on which the gateway is already active the node shall transmit the source PNC request on the CAN destination network in a NM-PDU maximum TCANGwPncRequest after the source PNC request became active.
- Note: Source network may be CAN or FlexRay and destination network is a CAN network.

### 3558 — Needed Tier1 requirements on Tier2 for AUTOSAR Diagnostic BSW
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：4.0.x
- To be able to fulfill Tier1 (ECU supplier) Diagnostic requirements when using AUTOSAR 4.0.3, the Tier1 (ECU supplier) shall require a Tier2 (AUTOSAR BSW supplier) to at least fix the already known AUTOSAR BSW issues as specified in: SWRS_31835918-VCC AUTOSAR DemSWRS_31835919-VCC AUTOSAR DcmSWRS_31836996-VCC AUTOSAR FiMNote: The VCC AUTOSAR Diagnostic BSW specifications are available from CEVT upon request.
- Note: Which issues a Tier1 must require a Tier2 to fix in the AUTOSAR BSW is dependent on the Tier1 REQPROD requirements.
- Note: The used version of VCC AUTOSAR BSW Diagnostic specifications shall be documented in DID F126.

### 5000 — Detection of missing LIN response in a LVDS network
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The LIN master shall be able to detect and set a missing LIN response DTC when the master expects to receive but does not receive any LIN response on the LVDS network.
- Diagnose response frames (LIN frame identifier 0x3D) shall not be monitored.

### 5265 — PDU Structure
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Define thee structure of the PDUs on the network Verification Method: The structure of the PDUs used on the LVDS network shall be structured as in Figure Structure of PDUs on the LVDS network.
- The LIN master shall not time out N_Cr transport protocol timer on first frames (FF).

### 6252 — Hardware security module Security Functional Requirements
- 版本：v1 ｜ 验证方式：Inspection ｜ 适用：通用
- Req: The use of the hardware security module security functional mechanism shall be in accordance with the analysis of all the applications using the hardware security module.

### 6253 — Access control
- 版本：v0 ｜ 验证方式：Analysis ｜ 适用：通用
- Access rules shall be specified based on engineering analysis of the implementation context and cover the privileges of all interacting entities.

### 6254 — Secure boot process
- 版本：v1 ｜ 验证方式：- ｜ 适用：通用
- Verification Method: The software shall be authenticated by the hardware security module (useing the trust anchor).

### 6256 — Diagnostic interface
- 版本：v0 ｜ 验证方式：Test ｜ 适用：通用
- Maintainability The following diagnostic information shall be available as diagnostic services (DID).

### 6257 — Separation of trust communities
- 版本：v0 ｜ 验证方式：Test ｜ 适用：通用
- Access control shall maintain separation between different trust communities (PKI: s).

### 6261 — Interface requirements
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- The interface to the hardware security module shall be autosar compliant when used in application mode..

### 6267 — Time routing incoming Diagnostic request
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The LIN slaves must be given a chance to start the operation cycle within the start of operation cycle timing.
- A diagnostic request shall be routed to the LIN network maximum 50ms after the LIN master have received the request.4.5.1.12.2 Gateway allocation of buffers for DIAG

### 6268 — X-LIN DIAG Minimum RAM for request buffers
- 版本：v0 ｜ 验证方式：Test ｜ 适用：通用
- For each LIN network behind the LIN master: In application mode, the LIN master shall be able to reserve at least a 264 bytes RAM buffer pool only for requests.
- The buffers for each LIN network shall be structured as: Buffers size Number of Buffers Memory need Total Memory need 200 1 200 32 2 64 Page No854(1572) # of buffers 3 264

### 6269 — X-LIN DIAG Minimum RAM for response buffers
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- For each LIN network behind the LIN master: In application mode, the LIN master shall be able to reserve at least a 900 bytes RAM buffer pool only for responses.
- The buffers for each LIN network shall be structured as: Buffers size Number of Buffers Memory need Total Memory need 500 1 500 200 2 400 # of buffers 3 900 4.5.1.13 Gateway X-LIN SWDL4.5.1.13.1 Diagnostic schedule execution

### 6270 — LIN scheduling method
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Minimize SWDL time The LIN master shall run LIN scheduling in Diagnostics Only Mode.

### 6271 — LIN scheduling interval
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Maximum utilization of the LIN network The LIN master shall run the LIN schedule table at least once every 10th ms and the allowed jitter is defined in either the corresponding platform specification or the LIN Data Link Specification.4.5.1.13.2 Gateway allocation of buffers for SWDL

### 6272 — X-LIN SWDL Minimum RAM for request buffers
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- For each LIN network behind the LIN master: In bootloader mode, the LIN master shall be able to reserve at least a 12300 bytes RAM buffer pool only for requests.
- The buffers for each LIN network shall be structured as: Buffers size Number of Buffers Memory need Total Memory need 2050 6 12300 # of buffers 6 12300

### 6273 — X-LIN SWDL Minimum RAM for response buffers
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- For each LIN network behind the LIN master: In bootloader mode, the LIN master shall be able to reserve at least a 324 bytes RAM buffer pool only for responses.
- The buffers for each LIN network shall be structured as: Buffers size Number of Buffers Memory need Total Memory need 100 3 300 8 3 24 # of buffers 6 324 4.5.2 UDS Data4.5.2.1 UDS Data4.5.2.1.1 APPENDIX4.5.2.1.1.1 Appendix AData records requested and reported via diagnostic services shall fit into one of the data classifications as described below.
- Where multi-byte data records are specified and the byte order is not already specified in [Data_4] Global Master Reference Database then the order shall be that the most significant byte of the multi-byte record shall be placed in the data byte with the lowest number according to the data byte numbering convention used in [Data_50] Road vehicles – Diagnostics systems – Diagnostic services.

### 6274 — X-LIN SWDL Support for queued request
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- For each LIN network behind the LIN master: In bootloader mode and the LIN master shall be able to receive two(2) queued request on three(3) communication channels without sending flow control Wait (FC.

### 6275 — Conversion from TA to NAD to SA
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Standard method shall be used for routing IDs in between LIN (i.
- The LIN master shall convert all diagnostic requests from TA logical ECU address to LIN NAD and convert LIN slave NAD to SA logical ECU address, as specified in Table - Network and ECU ID mapping to and from NAD.
- In terms of diagnostic addressing the LIN master shall be transparent in regards of not knowing which LIN slaves there are on a LIN network.

### 6276 — Physical request NAD validation
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The LIN master shall not block physically addressed diagnostic requests.
- The LIN master shall be transparent in regards of physically addressed diagnostic requests.4.5.1.12 Gateway X-LIN DIAG4.5.1.12.1 Gateway latency requirements

### 6277 — LIN master routing functional requests
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The LIN master shall route functional diagnostic requests and since the SPRMIB is placed in the diagnostic request, the LIN slave might as well perform the interpretation of the SPRMIB.
- The LIN master shall always route functional requests .

### 6278 — LIN master time to poll time for functional addressed responses
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- To save bus bandwidth the LIN master shall not poll for responses on diagnostic requests.
- The LIN master shall consider a functionally addressed diagnostic request completed as soon as the LIN master have sent the request on LIN i.
- the LIN master shall not poll for a diagnostic response (send frame identifier 0x3D) for functionally addressed requests.

### 6279 — LIN master to prioritize routing functionally addressed requests
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- The diagnostic request TesterPresent must be prioritized to prevent LIN slaves from timing out.
- LIN master shall prioritize sending functional requests.
- Even if a message is being transferred on LIN, the LIN master shall pause the message transmission (in between two LIN frames), send the functionally addressed request and then continue sending the message.4.5.1.11.4 Conversion from TA to NAD to SA

### 6281 — LIN master time out not receiving first NRC 0x78
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- 6281 v1LIN master time out not receiving first NRC 0x78 Define max time a LIN master shall wait before the LIN master shall consider a diagnostic request to LIN to be completed, if no NRC 0x78 (requestCorrectlyReceivedResponsePending) is received.
- The LIN master shall consider a physically addressed diagnostic request as timed out if the LIN master does not receive a 0x78 NRC (requestCorrectlyReceivedResponsePending) 100ms after the diagnostic request was sent.
- For functionally addressed diagnostic request the time shall be 0 (i.

### 6282 — LIN master time out not receiving consecutive 0x78 NRCs
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- Define max time a LIN master shall wait before the LIN master shall consider a diagnostic request to LIN to be completed, if no subsequent NRC 0x78 (requestCorrectlyReceivedResponsePending) are received.
- The LIN master shall consider a diagnostic request as timed out if the LIN master does not receive a new NRC 0x78 (requestCorrectlyReceivedResponsePending) 5000ms after sending the previous NRC 0x78 (requestCorrectlyReceivedResponsePending).

### 6283 — Concurrent LIN master and LIN slave diagnostic requests
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- The LIN master shall concurrent be able to receive and process diagnostic requests addressed to the LIN master itself during gateway to/from LIN slaves.
- This means the LIN master shall be able to be re-programmed during the same time as the LIN slave.4.5.1.11.2 LIN master time out

### 6284 — Parallel requests on LIN
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- 6284 v3Parallel requests on LIN The tester shall not need to consider limitations on LIN.
- The LIN master shall be able to handle parallel physical addressed diagnostic requests to a LIN network.
- On one LIN network there shall only be one ongoing physical address diagnostic request, the LIN master needs to wait until response is received or time out before next request is sent on the LIN network.

### 6286 — Compatibility between versions
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- To guarantee compatibility between versions Together with the latest software version for every new software release there shall be delta files generated for three previous versions of the of the software.

### 6287 — Compression
- 版本：v2 ｜ 验证方式：Inspection ｜ 适用：通用
- To decrease the size of the delta encoded data The delta encoded data shall be compressed.

### 6288 — Data file type
- 版本：v2 ｜ 验证方式：Inspection ｜ 适用：通用
- To ensure support for data file format The delta files shall be provided within the data file format.

### 6289 — Delta file distribution
- 版本：v1 ｜ 验证方式：Inspection ｜ 适用：通用
- To ensure consistent software deliveries The delta files shall be provided to the Software Configuration System in the same software archive as the target version that they are intended to create.

### 6290 — Delta file name
- 版本：v4 ｜ 验证方式：Inspection ｜ 适用：通用
- To guarantee delta version traceability The generated delta files shall have the source and target software part number and version included in the filename.
- A VBF file that contains a delta and uses the header data above shall utilize the file name of: E.

### 6291 — Delta file release information
- 版本：v2 ｜ 验证方式：Inspection ｜ 适用：通用
- To guarantee installation efficiency Together with the delta file delivery there shall be formal information about the software supplier's test results.
- The figures shall be results from system tests conducted in a system testing environment.
- The delta file installation time and delta file size shall be stated together with the install time and file size of a full target version.

### 6292 — Delta file size
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- To guarantee installation efficiency The generated compressed delta file shall be at least 50% smaller, compared to a complete compressed full version See [Data Compression and Encryption].
- Note: If the full version file is not compressed due to decreased install time as a result of the decompression routine, then the file shall be compressed using the compression method described in [Data Compression and Encryption] in order to perform the comparison.
- The file size shall be verified by selecting the file in Windows Explorer and select properties (Or equivalent for e.

### 6293 — Delta file structure
- 版本：v2 ｜ 验证方式：Inspection ｜ 适用：通用
- To ensure a consistent delta file structure Delta files are Data files with one single data block that shall consist of delta installation parameters and the actual delta/difference data.

### 6294 — Delta file version info
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- The delta installation data shall include the Software product number as well as the Softwareversion number for the source version (see below example), so that the ECU can read this dataand decide to reject the installation before start if the installed ECU software version is notcompatible.

### 6295 — Delta installation RAM buffer size
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- To ensure that the ECU provides enough memory for the delta installation Page No1423(1572) The delta installation data shall include the size of the RAM needed for the delta installation, so that the ECU can read this data and decide to reject the installation before start if the memory amount can not be allocated.

### 6296 — Delta installation time
- 版本：v2 ｜ 验证方式：Inspection ｜ 适用：通用
- To guarantee installation efficiency The Installation time of the generated delta shall be at least 50% shorter in average compared to a complete installation of the compressed full version.

### 6297 — New and obsolete data info
- 版本：v1 ｜ 验证方式：Inspection ｜ 适用：通用
- The delta installation data shall contain instructions for the bootloader to locate where in memory the delta data shall be written.
- The installation data shall also contain instructions in order to locate and erase any obsolete data from the old version that otherwise would remain unused in memory after the delta update.4.6.3.3 Delta installation4.6.3.3.1 RequirementsDelta encoded data is applied to the ECU software by the bootloader's delta installation routine.

### 6298 — Data decoding
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- To decode the delta file The ECU shall support decoding of a delta-encoded file Note: The dataFormatIdentifier in the RequestDownload request indicates if the data is delta encoded

### 6299 — Data decompression
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- To decompress the delta file The ECU shall support decompression of a compressed delta fileNote: The dataFormatIdentifier in the RequestDownload request indicates if the data is compressed

### 6300 — Delta installation data
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- To ensure that the ECU installation process receives all installation data provided in the delta file When the bootloader receives a delta file, it shall read and validate the delta installation data provided prior start of the installation phase.
- Software version information shall be provided and used to decide if installation can start.)The delta installation data shall be provided within the beginning of the streamed delta data, the complete delta file shall not be downloaded before this information is checked.

### 6301 — Delta installation memory segment
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- To enable delta data manipulation The ECU memory map must have memory segment (e.
- It shall not be considered a solution Delta installation - Extra sector usage example

### 6302 — Delta installation RAM usage
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- To ensure fast delta installation The bootloader shall use volatile memory (RAM) when processing the delta data.

### 6303 — Delta memory segment size
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- To enable delta data manipulation The available non-volatile memory segment size shall be at least the same size compared to the largest possible segment size within the ECU.

### 6304 — Delta SWDL in normal operational mode
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- Reduce installation time If the ECU supports software installation in normal operational mode then delta download and installation shall also be supported.

### 6305 — Delta SWDL in program mode
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- Reduce programming time The ECU shall support delta download and installation of software in program mode.

### 6306 — Obsolete data removal
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- The bootloader shall use instruction provided in the delta installation data to locate and erase data that is no longer a part of the installed software product.

### 6307 — Software consistency check
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- To ensure that the target image is correct after installation The bootloader shall verify that the applied delta resulted in the correct software image by using the method specified in [Software Authentication Specification].

### 6308 — Streamed installation
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- 6308 v2Streamed installation To reduce programming time The ECU shall support streamed installation using UDS, meaning that the bootloader shall start to decode and install data before the complete data file is received.

### 6309 — Target sector erase check
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- 6309 v1Target sector erase check To ensure that a fallback is possible on each sector during installation Before a target sector is erased and replaced with the delta update, a backup of the sector shall be stored and verified to be exactly the same as the target sector.4.6.3.3.1.1 Error Handling

### 6310 — Consistency check failure
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- 6310 v1Consistency check failure To guarantee that the correct image is installed The ECU shall reject the installation and respond with a negative response code if the ECU software is not verified as consistent using the method defined in [Software Authentication Specification]

### 6311 — Delta file corruption
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- 6311 v2Delta file corruption To guarantee that corrupted data is not used as installation data The ECU shall reject the installation and respond with a negative response code if the bootloader detects that the delta update package is corrupted.

### 6312 — Error code mapping
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- To ensure negative diagnostic response code feedback for error codes during the delta installation Error codes used during the delta installation shall have corresponding negative diagnostic response codes.

### 6313 — Full version install check
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- To ensure that a full version installation can be installed after a failed delta installation After a failed delta installation the bootloader shall not prevent or resume installation when a full version is to be installed.

### 6314 — Not enough memory
- 版本：v1 ｜ 验证方式：Test ｜ 适用：通用
- To guarantee that there is enough memory to perform a delta installation The ECU shall reject the installation and respond with a negative response code if the bootloader detects that either non-volatile memory or the RAM buffer provided in the init-routine is less than needed to apply the update

### 6315 — Recover from interrupted Installation
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- To ensure recovery after interrupted Installation If the ECU has memory enough to store a copy of the source version before the delta installation starts, then it shall be possible to fall back to the source version.
- If the ECU does not have enough memory available to fall back to the source version then it shall be possible to resume the update installation from the beginning or from the last successfully written code.

### 6316 — Subsequent reprogramming during recover
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- To avoid loss of data or broken ECUs The ECU software shall be designed in such way that an aborted download or install, or removing ECU power at any time during the download and install operation, shall not prevent subsequent reprogramming of the same delta file.

### 6317 — Version mismatch
- 版本：v2 ｜ 验证方式：Test ｜ 适用：通用
- To guarantee compatibility between versions The ECU shall reject the installation and respond with a negative response code if the currently installed ECU software version does not match sw_current_version provided in the delta installation data.
- Figure Document structure overviewThis document defines implementation specific requirements that shall apply to an IP ECU and the Edge Node.
- All diagnostic messages on IP shall be sent and received according to this and referenced documents.

### 6411 — In-Place Reconstruction of Delta Files
- 版本：v1 ｜ 验证方式：Analysis ｜ 适用：通用
- General Bootloader requirements - Delta encoding Legacy ID: The ECU shall support in-place reconstruction of software delta files according to the [Delta Encoding] specification.

### 6429 — Security Access Algorithm Description
- 版本：v2 ｜ 验证方式：Analysis ｜ 适用：通用
- 6429 v2Security Access Algorithm Description Define the algorithm used for Security Access The Security Access algorithm description is provided by CEVT Base Technology Team upon request.4.4.3.1.6 Security Constant

### 6436 — Privacy Regulations
- 版本：v1 ｜ 验证方式：- ｜ 适用：通用
- Privacy Regulations shall be followed Verification Method: DocumentationLegacy ID: All systems storing any personal data shall adhere to privacy regulations or policies applicable (e.

### 6437 — Privacy as Default
- 版本：v2 ｜ 验证方式：Inspection ｜ 适用：通用
- Whenever it is possible, personal data shall be anonymized or de-identified and encrypted.
- It shall not be possible to access other person’s personal data and it shall be possible to erase all personal data on request to eliminate any footprints e.
- Any administrator access to personal data shall be restricted to a minimum and actions logged.

### 6438 — Purpose and Consent
- 版本：v2 ｜ 验证方式：- ｜ 适用：通用
- Only necessary data collected, consent given and right to be forgotten Verification Method: DocumentationLegacy ID: A basic principle is that only necessary personal data shall be stored and the purpose for collecting the data must be clearly expressed.
- The contractor shall be able to present a list of what data is collected and the purpose must be clearly expressed.
- Consent for data collection as well as the possibility to erase personal data from the system is mandatory and shall be considered in the system design.4.4.7 Cyber Security4.4.7.1 Cyber Security Requirements for Security Level 1 ECUs4.4.7.1.1 Cyber Security Related Information SharingEffective defense against cyberattacks requires a high level of collaboration among multiple suppliers, information sharing is essential for many reasons.

### 6443 — Industry Standards
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- Ensure a good security process for development Legacy ID: Cyber Security must be part of the design and development processSystems and applications shall be developed in accordance with an appointed industry security standard or guidelines (e.
- The way of work shall correspond to "SAE J3061 - CyberSecurity Guidebook for Cyber-Physical Vehicle systems" and must be presented by the supplier covering: Guiding Principles in the Cyber Security WorkOverall management of Cyber SecurityCyber Security Life Cycle ProcessesSecurity StandardsApplications and programming interfaces shall be developed, deployed and tested in accordance with leading industry security standards, such as POSIX.
- The contractor shall be able to present the way of working to ensure application and code security, such as program language coding guidelines.

### 6446 — Remove Debug Functionality
- 版本：v4 ｜ 验证方式：Test ｜ 适用：通用
- Debug functionality shall be removed on all systems produced or intended for end customer use.
- Any software debug services must be removed and it is not sufficient to block access using a filter and firewall rule.
- HW debug interfaces shall be removed or permanently disabled by e.

### 6448 — System Hardening
- 版本：v4 ｜ 验证方式：Inspection ｜ 适用：通用
- Ensure a secure configuration Legacy ID: Operating systems, application functionality, user accounts and communication protocols used shall be hardened to only allow the features or access rights needed for the demanded functionality.
- Hardening shall also consider an attacker that may already has gained access to a system and make it more difficult to get any further access to the compromised system and thereby provide a second line of defense.
- Hardening process shall include: Configuration of access rights and configuration files of operation systems and applications shall be reviewed and if necessary modified to ensure they support a secure system and application setup.

### 6453 — Handling Anomalies
- 版本：v4 ｜ 验证方式：- ｜ 适用：通用
- Handling of anomalies Verification Method: DocumentationLegacy ID: System anomalies, such as misuse, unexpected system events or buffer overflow, that can endanger system security shall be logged, detected and acted upon to prevent any information loss or system breach.
- The system shall be designed with a proper error handling to be able to withstand unexpected events or inputs.
- Input validation shall be performed to reject any malformed or out of band input to avoid unexpected behavior or execution that can endanger system security.

### 6455 — Encryption keys and Algorithms
- 版本：v4 ｜ 验证方式：- ｜ 适用：通用
- Secure storage of sensitive encryption information and do not use propriety encryption algorithms Verification Method: DocumentationLegacy ID: Any encryption keys, trust files or otherwise sensitive data shall be stored in a secure way.
- Highly sensitive data like encryption keys, trust chains or critical secret information that can endanger system integrity or be a direct or indirect threat to personal privacy shall be stored in a HTA, e.

### 6456 — Least Necessary Privilege
- 版本：v3 ｜ 验证方式：- ｜ 适用：通用
- Do not use higher permissions than needed Verification Method: DocumentationLegacy ID: Every function and every user of the system shall operate using the least set of privileges necessary (the most restrictive) for the minimum amount of time to complete the job.
- Each user, process or program shall only have the least amount of privilege required to perform their tasks.
- This concept shall apply to both systems and operations/users.

### 6459 — Contact Persons
- 版本：v2 ｜ 验证方式：- ｜ 适用：通用
- Supplier to provide a point of contact for security related tasks Verification Method: Legacy ID: The contractor shall identify contact persons with a relevant security experience to interface with Geely/CEVT security personnel throughout the execution and implementation of the requirements.

### 6461 — Cyber Security Risk Assessment
- 版本：v4 ｜ 验证方式：Analysis ｜ 适用：通用
- Legacy ID: A Cyber security risks assessment shall be done on the delivered system and presented to CEVT/GRI.
- HEAVENS shall be used as the risk assessment method and all underlying judgments and ratings shall be shared with CEVT/GRI.
- Other risk assessment methods may be used after approval of CEVT/GRI Cyber Security team.

### 6464 — Incident and Patch Management
- 版本：v3 ｜ 验证方式：- ｜ 适用：通用
- Manage life cycle of product Verification Method: DocumentationLegacy ID: During the entire ECU life cycle, any discovered security risks or incidents shall be promptly reported to Geely/CEVT.
- Any highly critical patch shall be in place within one week after being discovered or published.
- A security patch process and strategy shall be presented by the supplier.

### 6465 — Security Review Involvement
- 版本：v2 ｜ 验证方式：- ｜ 适用：通用
- Contractor shall support security reviews at the contractor's or CEVT's premises with contractor security engineering personnel when requested.

### 6466 — Security Compliance Status review
- 版本：v3 ｜ 验证方式：- ｜ 适用：通用
- Continuous status updates on requirements Verification Method: DocumentationLegacy ID: The status of each Cyber security requirement shall continuously be kept up to date and presented to CEVT/Geely as part of any security review activity or follow up meetings

### 6512 — Event logging
- 版本：v4 ｜ 验证方式：Inspection ｜ 适用：通用
- Log security events using a common log format Legacy ID: If the ECU supports logging, security event logs shall be included in the log file according to the specification in this requirement.
- Any major events like software updates, high privilege system access, changes to encryption keys or important system events shall be logged.
- Passwords shall not be written to the log and any sensitive data or personal information shall be anonymized or encrypted.

### 6522 — Password Protection
- 版本：v4 ｜ 验证方式：Inspection ｜ 适用：通用
- Protect any passwords stored Legacy ID: Any passwords stored in the ECU must be safeguarded in accordance with security best-practices so they cannot be retrieved or guessed.
- If HTA is not available then any saved password data must be one way encrypted according to SHA-2 (SHA 512).
- The password hash must also be protected by salt.

### 6523 — Enforce Secure Coding
- 版本：v3 ｜ 验证方式：Analysis ｜ 适用：通用
- The supplier must ensure and continuously motivate the developers to seek higher knowledge within the security domain.
- All data input and output shall be validated (e.
- There shall be a defined and predictable error handling to handle any exceptions and error states.

### 6538 — IDS and IPS
- 版本：v3 ｜ 验证方式：- ｜ 适用：通用
- Prevent and detect intrusion attempts Verification Method: DemonstrationLegacy ID: A connected ECU shall have the capability to detect and prevent intrusions from networks such as Internet or a neighboring ECU.
- If any anomalies/attacks are detected these events must be logged and if possible mitigated.
- Examples of behaviors that shall be detected and acted upon:1.

### 6724 — Detailed Security Logging
- 版本：v3 ｜ 验证方式：Test ｜ 适用：通用
- It shall be possible to upload all on-board logs to a remote central cloud based solution for further diagnosis as well as: Remotely reset the on-board logsRemotely configure log parameters and settingsReceive IDSP/IPS logsDebug levelLimit local logging to configured security levels (Emergency, Alert, Critical, Error, Warning, Notice, Informational, Debug)Limit remote logging to configured security levels (Emergency, Alert, Critical, Error, Warning, Notice, Informational, Debug)Log protectionAll logs shall be encrypted when transported outside the ECUAll log files shall be encrypted when in restLog files may not contain passwordsPrivacy req followedSecurity Levels are defined according to RFC5424o Emergency: system is unusableAlert: action must be taken immediatelyCritical: critical conditions 3 Error: error conditions4 Warning: warning conditions5 Notice: normal but significant condition6 Informational: informational messages7 Debug: debug-level messagesInformation to be logged includes: a) User/car/ECU IDs;
- l) Activation and de-activation of system services or deamonsAll logs shall be in RFC5424 syslog format and the structured data pair shall include at least the following information in the set order: VIN: VIN numberEcuID: Unique Identification ID (S/N) of ECU Details about the origin of the attack, can be a adress, service, a user, a process and / or a nodeTarget: Details on the target of the attack can be a adress, service, a user, a process and / or a node and a file Action: Action taken (Drop, Log, Reject)Classification: Name of the attack and references, as CVEsSeverityLevel: Evaluation (also used in priority calculation) of the severity.)AdditionalData: Additional information on the attackAny additional information shall be added as separate fields after the AdditionalData fieldThe log buffer shall be sized to allow storage of at least 10000 messages and a FIFO strategy shall be applied.
- The following is a sample syslog message:<34>1 2017-02-23T23:20:50Z IHU su - ID47 [IDS_SDID@o vin="ABCDEFGH"ecuid="12345678" source="1.2.3.4" target="" action="block" classification="CVE-2017-0001" severity_level="warning" additional_data=""] BOM'su root exploitIf the same message is logged multiple times in a short period of time it shall be possible to rate limit the individual message to prevent filling up the log.

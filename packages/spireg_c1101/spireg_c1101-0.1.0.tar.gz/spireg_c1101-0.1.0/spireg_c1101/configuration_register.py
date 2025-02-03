from typing import cast
from spireg import Register, Entry


class IOCFG2Types(Register):
    """ GDO2 Output Pin Configuration """
    R0: int
    """ Bit 7: Not used """
    GDO2_INV: int
    """ Bit 6: Invert output, i.e. select active low (1) / high (0) """
    GDO2_CFG: int
    """ Bits 5-0: Default is CHP_RDYn (See Table 41 on page 62). """


IOCFG2 = cast(IOCFG2Types, Register("IOCFG2", 0x00, "GDO2 output pin configuration.", [
        Entry("R0", 1),
        Entry("GDO2_INV", 1),
        Entry("GDO2_CFG", 6, 0x29),
    ]))


class IOCFG1Types(Register):
    """ GDO1 Output Pin Configuration """
    GDO_DS: int
    """ Bit 7: Set high (1) or low (0) output drive strength on the GDO pins. """
    GDO1_INV: int
    """ Bit 6: Invert output, i.e. select active low (1) / high (0) """
    GDO1_CFG: int
    """ Bits 5-0: Default is 3-state (See Table 41 on page 62). """


IOCFG1 = cast(IOCFG1Types, Register("IOCFG1", 0x01, "GDO1 output pin configuration.", [
        Entry("GDO_DS", 1),
        Entry("GDO1_INV", 1),
        Entry("GDO1_CFG", 6, 0x2E),
    ]))


class IOCFG0Types(Register):
    """ GDO0 Output Pin Configuration """
    TEMP_SENSOR_ENABLE: int
    """ Bit 7: Enable analog temperature sensor. Write 0 in all other register bits
    when using temperature sensor. """
    GDO0_INV: int
    """ Bit 6: Invert output, i.e. select active low (1) / high (0) """
    GDO0_CFG: int
    """ Bits 5-0: Default is CLK_XOSC/192 (See Table 41 on page 62).
    It is recommended to disable the clock output in initialization, in
    order to optimize RF performance. """


IOCFG0 = cast(IOCFG0Types, Register("IOCFG0", 0x02, "GDO0 output pin configuration.", [
        Entry("TEMP_SENSOR_ENABLE", 1),
        Entry("GDO0_INV", 1),
        Entry("GDO0_CFG", 6, 0x3F),
    ]))


class FIFOTHRTypes(Register):
    ''' RX FIFO and TX FIFO Thresholds '''
    RESERVED: int
    ''' Bit 7: Reserved , write 0 for compatibility with possible future extension '''
    ADC_RETENTION: int
    ''' Bit 6:
0: TEST1 = 0x31 and TEST2= 0x88 when waking up from SLEEP
1: TEST1 = 0x35 and TEST2 = 0x81 when waking up from SLEEP

Note that the changes in the TEST registers due to the
ADC_RETENTION bit setting are only seen INTERNALLY in the analog
part. The values read from the TEST registers when waking up from
SLEEP mode will always be the reset value.

The ADC_RETENTION bit should be set to 1before going into SLEEP
mode if settings with an RX filter bandwidth below 325 kHz are wanted at
time of wake-up.
    '''
    CLOSE_IN_RX: int
    ''' Bit 5-4:
For more details, please see DN010 [8]

| Setting | RX Attenuation, Typical Values |
|---------|-------------------------------|
| 0 (00)  | 0 dB                          |
| 1 (01)  | 6 dB                          |
| 2 (10)  | 12 dB                         |
| 3 (11)  | 18 dB                         |
    '''
    FIFO_THR: int
    ''' Bit 3-0: Set the threshold for the TX FIFO and RX FIFO. The threshold is
    exceeded when the number of bytes in the FIFO is equal to or higher than
    the threshold value.
Setting | Bytes in TX FIFO | Bytes in RX FIFO
--------|------------------|-----------------
0 (0000)| 61               | 4
1 (0001)| 57               | 8
2 (0010)| 53               | 12
3 (0011)| 49               | 16
4 (0100)| 45               | 20
5 (0101)| 41               | 24
6 (0110)| 37               | 28
7 (0111)| 33               | 32
8 (1000)| 29               | 36
9 (1001)| 25               | 40
10 (1010)| 21              | 44
11 (1011)| 17              | 48
12 (1100)| 13              | 52
13 (1101)| 9               | 56
14 (1110)| 5               | 60
15 (1111)| 1               | 64
'''


FIFOTHR = cast(
    FIFOTHRTypes,
    Register("FIFOTHR", 0x03, "RX FIFO and TX FIFO thresholds.", [
        Entry("RESERVED", 1),
        Entry("ADC_RETENTION", 1),
        Entry("CLOSE_IN_RX", 2),
        Entry("FIFO_THR", 4, 7),
    ]))


class SYNC1Types(Register):
    ''' Sync Word, High Byte '''
    SYNC: int
    ''' Bits 7-0: 8 MSB of 16-bit sync word '''


SYNC1 = cast(SYNC1Types, Register("SYNC1", 0x04, "Sync word, high byte.", [
        Entry("SYNC", 8, 0xD3),
    ]))


class SYNC0Types(Register):
    ''' Sync Word, Low Byte '''
    SYNC: int
    ''' Bits 7-0: 8 LSB of 16-bit sync word '''


SYNC0 = cast(SYNC0Types, Register("SYNC0", 0x05, "Sync word, low byte.", [
        Entry("SYNC", 8, 0x91),
    ]))


class PKTLENTypes(Register):
    ''' Packet Length '''
    PACKET_LENGTH: int
    ''' Bits 7-0: Indicates the packet length when fixed packet length mode is enabled.
    If variable packet length mode is used, this value indicates the
    maximum packet length allowed. This value must be different from 0.'''


PKTLEN = cast(PKTLENTypes, Register("PKTLEN", 0x06, "Packet length.", [
        Entry("PACKET_LENGTH", 8, 0xFF),
    ]))


class PKTCTRL1Types(Register):
    ''' Packet Automation Control '''
    PQT: int
    ''' Bit 7-5: Preamble quality estimator threshold. The preamble quality estimator
increases an internal counter by one each time a bit is received that is different
from the previous bit, and decreases the counter by 8 each time a bit is received
that is the same as the last bit.

A threshold of 4∙PQT for this counter is used to gate sync word detection. When PQT=0 a
sync word is always accepted. '''
    RESERVED: int
    ''' Bit 4: Not used '''
    CRC_AUTOFLUSH: int
    ''' Bit 3: Enable automatic flush of RX FIFO when CRC is not OK. This requires that
only one packet is in the RXIFIFO and that packet length
is limited to the RX FIFO size. '''
    APPEND_STATUS: int
    ''' Bit 2: When enabled, two status bytes will be appended to the payload of the
    packet. The status bytes contain RSSI and LQI values, as well as CRC OK. '''
    ADR_CHK: int
    ''' Bit 1-0: Controls address check configuration of received packages.
Setting | Address check configuration
--------|----------------------------
0 (00)  | No address check
1 (01)  | Address check, no broadcast
2 (10)  | Address check and 0 (0x00) broadcast
3 (11)  | Address check and 0 (0x00) and 255 (0xFF) broadcast '''


PKTCTRL1 = cast(
    PKTCTRL1Types,
    Register("PKTCTRL1", 0x07, "Packet automation control.", [
        Entry("PQT", 3),
        Entry("RESERVED", 1),
        Entry("CRC_AUTOFLUSH", 1),
        Entry("APPEND_STATUS", 1, 1),
        Entry("ADR_CHK", 2),
    ]))


class PKTCTRL0Types(Register):
    ''' Packet Automation Control '''
    RESERVED: int
    WHITE_DATA: int
    ''' Bit 6: Turn data whitening on / off
0: Whitening off
1: Whitening on '''
    PKT_FORMAT: int
    ''' Bit 5-4: Format of RX and TX data
Setting | Packet format
--------|----------------
0 (00)  | Normal mode, use FIFOs for RX and TX
1 (01)  | Synchronous serial mode, Data in on GDO0 and data out on either of the GDOx
        | pins
2 (10)  | Random TX mode; sends random data using PN9 generator. Used for test. Works
        | as normal mode, setting 0 (00), in RX
3 (11)  | Asynchronous serial mode, Data in on GDO0 and data out on either of the GDOx
        | pins
'''
    RESERVED2: int
    CRC_EN: int
    ''' Bit 2: 1: CRC calculation in TX and CRC check in RX enabled
0: CRC disabled for TX and RX
'''
    LENGTH_CONFIG: int
    ''' Bit 1-0: Configure the packet length
Setting | Packet length configuration
--------|----------------------------
0 (00)  | Fixed packet length mode. Length configured in PKTLEN register
1 (01)  | Variable packet length mode. Packet length configured by the first byte after
        | sync word
2 (10)  | Infinite packet length mode
3 (11)  | Reserved
'''


PKTCTRL0 = cast(
    PKTCTRL0Types,
    Register("PKTCTRL0", 0x08, "Packet automation control.", [
        Entry("RESERVED", 1),
        Entry("WHITE_DATA", 1, 1),
        Entry("PKT_FORMAT", 2),
        Entry("RESERVED2", 1),
        Entry("CRC_EN", 1, 1),
        Entry("LENGTH_CONFIG", 2, 1),
    ]))


class ADDRTypes(Register):
    ''' Device Address '''
    DEVICE_ADDRESS: int
    ''' Bits 7-0: Address used for packet filtration. Optional broadcast addresses are
    0 (0x00) and 255 (0xFF). '''


ADDR = cast(ADDRTypes, Register("ADDR", 0x09, "Device address.", [
        Entry("DEVICE_ADDRESS", 8, 0x00),
    ]))


class CHANNRTypes(Register):
    ''' Channel Number '''
    CHANNEL_NUMBER: int
    ''' Bits 7-0: The 8-bit unsigned channel number, which is multiplied by the channel
    spacing setting and added to the base frequency. '''


CHANNR = cast(CHANNRTypes, Register("CHANNR", 0x0A, "Channel number.", [
        Entry("CHANNEL_NUMBER", 8, 0x00),
    ]))


class FSCTRL1Types(Register):
    ''' Frequency Synthesizer Control '''
    NOT_USED: int
    ''' Bit 7-6: Not used '''
    RESERVED: int
    ''' Bit 5: Reserved '''
    FREQ_IF: int
    ''' Bit 4-0: The desired IF frequency to employ in RX. Subtracted from FS base
    frequency in RX and controls the digital complex mixer in the demodulator.

F_IF = (F_XOSC/2^10) * FREQ_IF

The default value gives an IF frequency of 381kHz, assuming a 26.0 MHz crystal. '''


FSCTRL1 = cast(
    FSCTRL1Types,
    Register("FSCTRL1", 0x0B, "Frequency synthesizer control.", [
        Entry("NOT_USED", 2),
        Entry("RESERVED", 1),
        Entry("FREQ_IF", 5, 0x0F),
    ]))


class FSCTRL0Types(Register):
    ''' Frequency Synthesizer Control '''
    FREQOFF: int
    ''' Bits 7-0: Frequency offset added to the base frequency before being used by the
    frequency synthesizer. (2s-complement).

Resolution is FXTAL/2^14 (1.59kHz-1.65kHz); range is ±202 kHz to ±210 kHz, dependent of
XTAL frequency. '''


FSCTRL0 = cast(
    FSCTRL0Types,
    Register("FSCTRL0", 0x0C, "Frequency synthesizer control.", [
        Entry("FREQOFF", 8, 0x00),
    ]))


class FREQ2Types(Register):
    ''' Frequency Control Word, High Byte '''
    RESERVED: int
    ''' Bits 7-6: FREQ[23:22] is always 0 (the FREQ2 register is less than 36 with
    26-27 MHz crystal) '''
    FREQ: int
    ''' Bits 5-0: FREQ[21:16] FREQ[23:0] is the base frequency for the frequency
    synthesiser in increments of fXOSC/2^16.
F_carrier = F_XOSC/2^16 * FREQ
'''


FREQ2 = cast(FREQ2Types, Register("FREQ2", 0x0D, "Frequency control word, high byte.", [
        Entry("RESERVED", 2),  # Bits 7-6: FREQ[23:22] is always 0
        Entry("FREQ", 6, 0x1E),  # Bits 5-0: FREQ[21:16]
    ]))


class FREQ1Types(Register):
    ''' Frequency Control Word, Middle Byte '''
    FREQ: int
    ''' Bits 7-0: FREQ[15:8] '''


FREQ1 = cast(
    FREQ1Types,
    Register("FREQ1", 0x0E, "Frequency control word, middle byte.", [
        Entry("FREQ", 8, 0xC4),  # Bits 7-0: FREQ[15:8]
    ]))


class FREQ0Types(Register):
    ''' Frequency Control Word, Low Byte '''
    FREQ: int
    ''' Bits 7-0: FREQ[7:0] '''


FREQ0 = cast(FREQ0Types, Register("FREQ0", 0x0F, "Frequency control word, low byte.", [
        Entry("FREQ", 8, 0xEC),  # Bits 7-0: FREQ[7:0]
    ]))


class MDMCFG4Types(Register):
    ''' Modem Configuration '''
    CHANBW_E: int
    ''' Bits 7-6: '''
    CHANBW_M: int
    ''' Bits 5-4: Sets the decimation ratio for the delta-sigma ADC input stream and
    thus the channel bandwidth.

BW_channel = F_XOSC / (8 * (4 + CHANBW_M) * 2^CHANBW_E)

The default values give 203 kHz channel filter bandwidth,
assuming a 26.0 MHz crystal.'''
    DRATE_E: int
    ''' Bits 3-0: The exponent of the user specified symbol rate '''


MDMCFG4 = cast(MDMCFG4Types, Register("MDMCFG4", 0x10, "Modem configuration.", [
        Entry("CHANBW_E", 2, 2),
        Entry("CHANBW_M", 2, 0),
        Entry("DRATE_E", 4, 0x0C),
    ]))


class MDMCFG3Types(Register):
    ''' Modem Configuration '''
    DRATE_M: int
    ''' Bits 7-0: The mantissa of the user specified symbol rate. The symbol rate is
    configured using an unsigned, floating-point number with 9-bit mantissa and 4-bit
exponent. The 9th bit is a hidden '1'. The resulting data rate is:

R_DATA = (256 + DRATE_M) * 2^DRATE_E * F_XOSC / 2^28

The default values give a data rate of 115.051 kBaud (closest setting to 115.2 kBaud),
assuming a 26.0 MHz crystal.
 '''


MDMCFG3 = cast(MDMCFG3Types, Register("MDMCFG3", 0x11, "Modem configuration.", [
        Entry("DRATE_M", 8, 0x22),
    ]))


class MDMCFG2Types(Register):
    ''' Modem Configuration '''
    DEM_DCFILT_OFF: int
    ''' Bit 7: Disable digital DC blocking filter before demodulator.

0 = Enable (better sensitivity)

1 = Disable (current optimized). Only for data rates≤ 250 kBaud

The recommended IF frequency changes when the DC blocking is disabled.
Please use SmartRF Studio [5] to calculate correct register setting. '''
    MOD_FORMAT: int
    ''' Bits 6-4: The modulation format of the radio signal
Setting | Modulation format
--------|------------------
0 (000) | 2-FSK
1 (001) | GFSK
2 (010) | -
3 (011) | ASK/OOK
4 (100) | 4-FSK
5 (101) | -
6 (110) | -
7 (111) | MSK
MSK is only supported for data rates above 26 kBaud
'''
    MANCHESTER_EN: int
    ''' Bit 3: Enable Manchester encoding/decoding

0 = Disable

1 = Enable '''
    SYNC_MODE: int
    ''' Bits 2-0: Combined sync-word qualifier mode
    Setting | Sync-word qualifier mode
    --------|--------------------------
    0 (000) | No preamble/sync
    1 (001) | 15/16 sync word bits detected
    2 (010) | 16/16 sync word bits detected
    3 (011) | 30/32 sync word bits detected
    4 (100) | No preamble/sync, carrier-sense above threshold
    5 (101) | 15/16 + carrier-sense above threshold
    6 (110) | 16/16 + carrier-sense above threshold
    7 (111) | 30/32 + carrier-sense above threshold
    '''


MDMCFG2 = cast(MDMCFG2Types, Register("MDMCFG2", 0x12, "Modem configuration.", [
        Entry("DEM_DCFILT_OFF", 1, 0),
        Entry("MOD_FORMAT", 3, 0x00),
        Entry("MANCHESTER_EN", 1, 0),
        Entry("SYNC_MODE", 3, 0b010),
    ]))


class MDMCFG1Types(Register):
    ''' Modem Configuration '''
    FEC_EN: int
    ''' Bit 7: Enable Forward Error Correction (FEC) with interleaving for packet
    payload

    0 = Disable

    1 = Enable (Only supported for fixed packet length mode, i.e.
    PKTCTRL0.LENGTH_CONFIG=0) '''
    NUM_PREAMBLE: int
    ''' Bits 6-4: Number of preamble bytes to send before the sync word
    Sets the minimum number of preamble bytes to be transmitted
    Setting | Number of preamble bytes
    --------|-------------------------
    0 (000) | 2
    1 (001) | 3
    2 (010) | 4
    3 (011) | 6
    4 (100) | 8
    5 (101) | 12
    6 (110) | 16
    7 (111) | 24
    '''
    NOT_USED: int
    ''' Bit 3-2: Not used '''
    CHANSPC_E: int
    ''' Bits 1-0: 2 bit exponent of channel spacing '''


MDMCFG1 = cast(MDMCFG1Types, Register("MDMCFG1", 0x13, "Modem configuration.", [
        Entry("FEC_EN", 1, 0),
        Entry("NUM_PREAMBLE", 3, 0b110),
        Entry("NOT_USED", 2),
        Entry("CHANSPC_E", 2, 0),
    ]))


class MDMCFG0Types(Register):
    ''' Modem Configuration '''
    CHANSPC_M: int
    ''' Bits 7-0: 8 bit mantissa of channel spacing '''
    CHANSPC_M: int
    ''' Bits 7-0: 8-bit mantissa of channel spacing. The channel spacing is
multiplied by the channel number CHAN and added to the base
frequency. It is unsigned and has the format:

Δf_CHANNEL = f_XOSC / 2^18 * (256 + CHANSPC_M) * 2^CHANSPC_E

The default values give 199.951 kHz channel spacing (the closest
setting to 200 kHz), assuming 26.0 MHz crystal frequency. '''


MDMCFG0 = cast(MDMCFG0Types, Register("MDMCFG0", 0x14, "Modem configuration.", [
    Entry("CHANSPC_M", 8, 0xF8),  # Bits 7-0: 8-bit mantissa of channel spacing
]))


class DEVIATNTypes(Register):
    ''' Modem Deviation Setting '''
    NOT_USED: int
    ''' Bit 7: Not used '''
    DEVIATION_E: int
    ''' Bits 6-4: Deviation exponent.'''
    NOT_USED2: int
    ''' Bit 3: Not used '''
    DEVIATION_M: int
    ''' Bits 2-0:
TX

2-FSK/GFSK/4-FSK: Specifies the nominal frequency deviation from the carrier for a '0'
(-DEVIATN) and '1' (+DEVIATN) in a mantissa-exponent format,
interpreted as a 4-bit value with MSB implicit 1. The resulting frequency deviation is
given by: F_dev = F_XOSC / 2^17 * (8 + DEVIATN_M) * 2^DEVIATN_E The default values give
a frequency deviation of ±47.607 kHz, assuming a 26.0 MHz crystal frequency.

MSK: Specifies the fraction of symbol period (1/8-8/8) during which a phase change
occurs ('0': +90deg, '1':-90deg). Refer to the SmartRF Studio software [5]
for correct DEVIATN setting when using MSK.

ASK/OOK: This setting has no effect

RX

2-FSK/GFSK/4-FSK: Specifies the expected frequency deviation of incoming signal, must
be approximately right for demodulation to be performed reliably and robustly

MSK/ASK/OOK: This setting has no effect
    '''


DEVIATN = cast(DEVIATNTypes, Register("DEVIATN", 0x15, "Modem deviation setting.", [
    Entry("NOT_USED", 1),       # Bit 7: Not used
    Entry("DEVIATION_E", 3, 4),  # Bits 6-4: Deviation exponent.
    Entry("NOT_USED2", 1),      # Bit 3: Not used
    Entry("DEVIATION_M", 4, 0x07),  # Bits 2-0: Deviation mantissa.
]))


class MCSM2Types(Register):
    ''' Main Radio Control State Machine Configuration

    The RX timeout in µs is given by EVENT0·C(RX_TIME, WOR_RES)·26/X, where C is given
    by the table below and X is the crystal oscillator frequency in MHz:

    Setting | WOR_RES = 0 | WOR_RES = 1 | WOR_RES = 2 | WOR_RES = 3
    --------|-------------|-------------|-------------|-------------
    0 (000) | 3.6058      | 18.0288     | 32.4519     | 46.8750
    1 (001) | 1.8029      | 9.0144      | 16.2260     | 23.4375
    2 (010) | 0.9014      | 4.5072      | 8.1130      | 11.7188
    3 (011) | 0.4507      | 2.2536      | 4.0565      | 5.8594
    4 (100) | 0.2254      | 1.1268      | 2.0282      | 2.9297
    5 (101) | 0.1127      | 0.5634      | 1.0141      | 1.4648
    6 (110) | 0.0563      | 0.2817      | 0.5071      | 0.7324
    7 (111) | Until end of packet

    As an example, EVENT0=34666, WOR_RES=0 and RX_TIME=6 corresponds to 1.96 ms RX
    timeout, 1 s polling interval and 0.195% duty cycle. Note that WOR_RES should
    be 0 or 1 when using WOR because using WOR_RES > 1 will give a very low duty cycle.
    In applications where WOR is not used all settings of WOR_RES can be used.

    The duty cycle using WOR is approximated by:

    Setting | WOR_RES=0 | WOR_RES=1
    --------|-----------|-----------
    0 (000) | 12.50%    | 1.95%
    1 (001) | 6.250%    | 9765ppm
    2 (010) | 3.125%    | 4883ppm
    3 (011) | 1.563%    | 2441ppm
    4 (100) | 0.781%    | NA
    5 (101) | 0.391%    | NA
    6 (110) | 0.195%    | NA
    7 (111) | NA        | NA

    Note that the RC oscillator must be enabled in order to use setting 0-6, because
    the timeout counts RC oscillator periods. WOR mode does not need to be enabled.

    The timeout counter resolution is limited: With RX_TIME=0, the timeout count is
    given by the 13 MSBs of EVENT0, decreasing to the 7 MSBs of EVENT0 with RX_TIME=6.
    '''
    NOT_USED: int
    ''' Bit 7-5: Not used '''
    RX_TIME_RSSI: int
    ''' Bit 4: Direct RX termination based on RSSI measurement (carrier sense).
    For ASK/OOK modulation, RX times out if there is no carrier sense in the first
    8 symbol periods.'''
    RX_TIME_QUAL: int
    ''' Bit 3: When the RX_TIME timer expires, the chip checks if sync word is found
    when RX_TIME_QUAL=0, or either sync word is found or PQI is set when
    RX_TIME_QUAL=1. '''
    RX_TIME: int
    ''' Bits 2-0: Timeout for sync word search in RX for both WOR mode and normal RX
    operation. The timeout is relative to the programmed EVENT0 timeout.
 '''


MCSM2 = cast(
    MCSM2Types,
    Register("MCSM2", 0x16, "Main Radio Control State Machine configuration.", [
        Entry("NOT_USED", 3),
        Entry("RX_TIME_RSSI", 1),
        Entry("RX_TIME_QUAL", 1),
        Entry("RX_TIME", 3, 0x07),
    ]))


class MCSM1Types(Register):
    ''' Main Radio Control State Machine Configuration '''
    NOT_USED: int
    ''' Bit 7-6: Not used '''
    CCA_MODE: int
    ''' Bit 5-4: Selects CCA_MODE; Reflected in CCA signal
    Setting | Clear channel indication
    --------|--------------------------
    0 (00)  | Always
    1 (01)  | If RSSI below threshold
    2 (10)  | Unless currently receiving a packet
    3 (11)  | If RSSI below threshold unless currently receiving a packet
    '''
    RXOFF_MODE: int
    ''' Bit 3-2: Select what should happen when a packet has been received
    Setting | Next state after finishing packet reception
    --------|-------------------------------------
    0 (00)  | IDLE
    1 (01)  | FSTXON
    2 (10)  | TX
    3 (11)  | Stay in RX
    '''
    TXOFF_MODE: int
    ''' Bit 1-0: Select what should happen when a packet has been sent (TX)
    Setting | Next state after finishing packet transmission
    --------|-------------------------------------
    0 (00)  | IDLE
    1 (01)  | FSTXON
    2 (10)  | Stay in TX (start sending preamble)
    3 (11)  | RX
    '''


MCSM1 = cast(
    MCSM1Types,
    Register("MCSM1", 0x17, "Main Radio Control State Machine configuration.", [
        Entry("R0", 2),
        Entry("CCA_MODE", 2, 0b11),
        Entry("RXOFF_MODE", 2, 0b00),
        Entry("TXOFF_MODE", 2, 0b00),
    ]))


class MCSM0Types(Register):
    """ Main Radio Control State Machine Configuration """
    NOT_USED: int
    """ Bits 7-6: Not used """
    FS_AUTOCAL: int
    """ Bits 5-4: Automatically calibrate when going to RX or TX, or back to IDLE

    Setting | When to perform automatic calibration
    --------|--------------------------------------
    0 (00)  | Never (manually calibrate using SCAL strobe)
    1 (01)  | When going from IDLE to RX or TX (or FSTXON)
    2 (10)  | When going from RX or TX back to IDLE automatically
    3 (11)  | Every 4th time when going from RX or TX to IDLE automatically

    In some automatic wake-on-radio (WOR) applications, using setting 3 (11) can
    significantly reduce current consumption.
    """
    PO_TIMEOUT: int
    """ Bits 3-2: Programs the number of times the six-bit ripple counter must expire
    after XOSC has stabilized before CHP_RDYn goes low [1].

If XOSC is on (stable) during power-down, PO_TIMEOUT should be set so that the
regulated digital supply voltage has time to stabilize before CHP_RDYn goes low
(PO_TIMEOUT=2 recommended). Typical start-up time for the voltage regulator is 50 μs.

For robust operation it is recommended to use PO_TIMEOUT = 2 or 3 when XOSC is off
during power-down.

[1] Note that the XOSC_STABLE signal will be asserted at the same time as the CHP_RDYn
signal; i.e. the PO_TIMEOUT delays both signals and does not insert a delay between the
signals
Setting | Expire count | Timeout after XOSC start
--------|--------------|-------------------------
0 (00)  | 1            | Approx. 2.3 - 2.4 μs
1 (01)  | 16           | Approx. 37 - 39 μs
2 (10)  | 64           | Approx. 149 - 155 μs
3 (11)  | 256          | Approx. 597 - 620 μs

Exact timeout depends on crystal frequency
    """
    PIN_CTRL_EN: int
    """ Bit 1: Enables the pin radio control option """
    XOSC_FORCE_ON: int
    """ Bit 0: Force the XOSC to stay on in the SLEEP state """


MCSM0 = cast(
    MCSM0Types,
    Register("MCSM0", 0x18, "Main Radio Control State Machine configuration.", [
        Entry("R0", 2),
        Entry("FS_AUTOCAL", 2, 0),
        Entry("PO_TIMEOUT", 2, 1),
        Entry("PIN_CTRL_EN", 1, 0),
        Entry("XOSC_FORCE_ON", 1, 0),
    ]))


class FOCCFGTypes(Register):
    NOT_USED: int
    """ Bits 7-6: Not used """
    FOC_BS_CS_GATE: int
    """ Bit 5: If set, the demodulator freezes the frequency offset compensation and
    clock recovery feedback loops until the CS signal goes high. """
    FOC_PRE_K: int
    """ Bits 4-3: Frequency compensation loop gain before a sync word is detected.
    Setting | Freq. compensation loop gain before sync word
    --------|---------------------------------------------
    0 (00)  | K
    1 (01)  | 2K
    2 (10)  | 3K
    3 (11)  | 4K
    """
    FOC_POST_K: int
    """ Bit 2: The frequency compensation loop gain to be used after a sync word is
    detected.
    Setting | Freq. compensation loop gain after sync word
    --------|--------------------------------------------
    0 (0)   | Same as FOC_PRE_K
    1 (1)   | K/2
    """
    FOC_LIMIT: int
    """ Bits 1-0: The saturation point for the frequency offset compensation algorithm.
    Setting | Saturation point (max compensated offset)
    --------|---------------------------------------
    0 (00) ±0 (no frequency offset compensation)
    1 (01) ±BWCHAN/8
    2 (10) ±BWCHAN/4
    3 (11) ±BWCHAN/2
    Frequency offset compensation is not supported for ASK/OOK. Always use FOC_LIMIT=0
    with these modulation formats.
    """


FOCCFG = cast(
    FOCCFGTypes,
    Register("FOCCFG", 0x19, "Frequency Offset Compensation configuration.", [
        Entry("R0", 2),
        Entry("FOC_BS_CS_GATE", 1, 1),
        Entry("FOC_PRE_K", 2, 2),
        Entry("FOC_POST_K", 1, 1),
        Entry("FOC_LIMIT", 2, 2),
    ]))


class BSCFGTypes(Register):
    BS_PRE_KI: int
    """ Bits 7-6: The clock recovery feedback loop integral gain to be used before a
    sync word is detected (used to correct offsets in data rate):
    Setting | Clock recovery loop integral gain before sync word
    --------|----------------------------------------------
    0 (00)  | KI
    1 (01)  | 2KI
    2 (10)  | 3KI
    3 (11)  | 4KI
    """
    BS_PRE_KP: int
    """ Bits 5-4: The clock recovery feedback loop proportional gain to be used before
    a sync word is detected.
    Setting | Clock recovery loop proportional gain before sync word
    --------|--------------------------------------------------
    0 (00)  | KP
    1 (01)  | 2KP
    2 (10)  | 3KP
    3 (11)  | 4KP
    """
    BS_POST_KI: int
    """ Bit 3: The clock recovery feedback loop integral gain to be used after a
    sync word is detected.
    Setting | Clock recovery loop integral gain after sync word
    --------|----------------------------------------------
    0       | Same as BS_PRE_KI
    1       | KI / 2
    """
    BS_POST_KP: int
    """ Bit 2: The clock recovery feedback loop proportional gain to be used after a
    sync word is detected.
    Setting | Clock recovery loop proportional gain after sync word
    --------|--------------------------------------------
    0       | Same as BS_PRE_KP
    1       | KP
    """
    BS_LIMIT: int
    """ Bits 1-0: The saturation point for the data rate offset compensation algorithm.
    Setting | Data rate offset saturation (max data rate difference)
    --------|-----------------------------------------------
    0 (00)  | ±0 (No data rate offset compensation performed)
    1 (01)  | ±3.125 % data rate offset
    2 (10)  | ±6.25 % data rate offset
    3 (11)  | ±12.5 % data rate offset
    """


BSCFG = cast(BSCFGTypes, Register("BSCFG", 0x1A, "Bit Synchronization configuration.", [
            Entry("BS_PRE_KI", 2, 1),
            Entry("BS_PRE_KP", 2, 2),
            Entry("BS_POST_KI", 1, 1),
            Entry("BS_POST_KP", 1, 1),
            Entry("BS_LIMIT", 2, 0),
]))


class AGCTRL2Types(Register):
    MAX_DVGA_GAIN: int
    """ Bits 7-6: Reduces the maximum allowable DVGA gain.
    Setting | Allowable DVGA settings
    --------|-----------------------------------------
    0 (00)  | All gain settings can be used
    1 (01)  | The highest gain setting cannot be used
    2 (10)  | The 2 highest gain settings cannot be used
    3 (11)  | The 3 highest gain settings cannot be used
    """
    MAX_LNA_GAIN: int
    """ Bits 5-3: Sets the maximum allowable LNA + LNA 2 gain relative to the maximum
    possible gain.
    Setting | Maximum allowable LNA + LNA 2 gain
    --------|-----------------------------------------------
    0 (000) | Maximum possible LNA + LNA 2 gain
    1 (001) | Approx. 2.6 dB below maximum possible gain
    2 (010) | Approx. 6.1 dB below maximum possible gain
    3 (011) | Approx. 7.4 dB below maximum possible gain
    4 (100) | Approx. 9.2 dB below maximum possible gain
    5 (101) | Approx. 11.5 dB below maximum possible gain
    6 (110) | Approx. 14.6 dB below maximum possible gain
    7 (111) | Approx. 17.1 dB below maximum possible gain
    """
    MAGN_TARGET: int
    """ Bits 2-0: These bits set the target value for the averaged amplitude from the
    digital channel filter (1 LSB = 0 dB).
    Setting | Target amplitude from channel filter
    --------|--------------------------------
    0 (000) | 24 dB
    1 (001) | 27 dB
    2 (010) | 30 dB
    3 (011) | 33 dB
    4 (100) | 36 dB
    5 (101) | 38 dB
    6 (110) | 40 dB
    7 (111) | 42 dB
    """


AGCTRL2 = cast(AGCTRL2Types, Register("AGCTRL2", 0x1B, "AGC control.", [
            Entry("MAX_DVGA_GAIN", 2, 0),
            Entry("MAX_LNA_GAIN", 3, 0),
            Entry("MAGN_TARGET", 3, 3),
        ]))


class AGCTRL1Types(Register):
    R0: int
    """ Bit 7: Not used. """

    AGC_LNA_PRIORITY: int
    """ Bit 6: Selects between two strategies for LNA and LNA 2 gain adjustment.
    Setting | Description
    --------|-------------
    0       | LNA 2 gain is decreased to minimum before decreasing LNA gain.
    1       | LNA gain is decreased first.
    """

    CARRIER_SENSE_REL_THR: int
    """ Bits 5-4: Sets the relative change threshold for asserting carrier sense.
    Setting | Description
    --------|-------------
    0 (00)  | Relative carrier sense threshold disabled.
    1 (01)  | 6 dB increase in RSSI value.
    2 (10)  | 10 dB increase in RSSI value.
    3 (11)  | 14 dB increase in RSSI value.
    """

    CARRIER_SENSE_ABS_THR: int
    """ Bits 3-0: Sets the absolute RSSI threshold for asserting carrier sense.
    The 2-complement signed threshold is programmed in steps of 1 dB
    and is relative to the MAGN_TARGET setting.
    Setting | Description
    --------|-------------
    -8 (1000) | Absolute carrier sense threshold disabled.
    -7 (1001) | 7 dB below MAGN_TARGET setting.
    ...       | ...
    -1 (1111) | 1 dB below MAGN_TARGET setting.
     0 (0000) | At MAGN_TARGET setting.
     1 (0001) | 1 dB above MAGN_TARGET setting.
    ...       | ...
     7 (0111) | 7 dB above MAGN_TARGET setting.
    """


AGCTRL1 = cast(AGCTRL1Types, Register("AGCTRL1", 0x1C, "AGC control.", [
        Entry("R0", 1, 0),
        Entry("AGC_LNA_PRIORITY", 1, 1),
        Entry("CARRIER_SENSE_REL_THR", 2, 0),
        Entry("CARRIER_SENSE_ABS_THR", 4, 0),
    ]))


class AGCTRL0Types(Register):
    HYST_LEVEL: int
    """ Bits 7-6: Sets the level of hysteresis on the magnitude deviation
    (internal AGC signal that determines gain changes).
    Setting | Description
    --------|-------------
    0 (00)  | No hysteresis, small symmetric dead zone, high gain.
    1 (01)  | Low hysteresis, small asymmetric dead zone, medium gain.
    2 (10)  | Medium hysteresis, medium asymmetric dead zone, medium gain.
    3 (11)  | Large hysteresis, large asymmetric dead zone, low gain.
    """

    WAIT_TIME: int
    """ Bits 5-4: Sets the number of channel filter samples from a gain adjustment has
    been made until the AGC algorithm starts accumulating new samples.
    Setting | Channel filter samples
    --------|-----------------------
    0 (00)  | 8
    1 (01)  | 16
    2 (10)  | 24
    3 (11)  | 32
    """

    AGC_FREEZE: int
    """ Bits 3-2: Controls when the AGC gain should be frozen.
    Setting | Function
    --------|---------
    0 (00)  | Normal operation. Always adjust gain when required.
    1 (01)  | The gain setting is frozen when a sync word has been found.
    2 (10)  | Manually freeze the analogue gain setting and continue to adjust the
    digital gain.
    3 (11)  | Manually freezes both the analogue and the digital gain setting. Used for
    manually overriding the gain.
    """

    FILTER_LENGTH: int
    """ Bits 1-0: Sets the averaging length for the amplitude from the channel filter
    for 2-FSK, 4-FSK, MSK.
    For ASK, OOK, it sets the OOK/ASK decision boundary for OOK/ASK reception.
    Setting | Channel filter samples | OOK/ASK decision boundary
    --------|------------------------|---------------------------
    0 (00)  | 8                      | 4 dB
    1 (01)  | 16                     | 8 dB
    2 (10)  | 32                     | 12 dB
    3 (11)  | 64                     | 16 dB
    """


AGCTRL0 = cast(AGCTRL0Types, Register("AGCTRL0", 0x1D, "AGC control.", [
        Entry("HYST_LEVEL", 2, 2),
        Entry("WAIT_TIME", 2, 1),
        Entry("AGC_FREEZE", 2, 0),
        Entry("FILTER_LENGTH", 2, 1),
    ]))


class WOREVT1Types(Register):
    EVENT0_HIGH: int
    """ Bits 7-0: High byte of EVENT0 timeout register.
    t_Event0 = 750 / f_XOSC * Event0 * 2^5WOR_RES
    """


WOREVT1 = cast(WOREVT1Types, Register(
    "WOREVT1", 0x1E, "High Byte Event0 Timeout", [
        Entry("EVENT0_HIGH", 8, 0x87),  # Bits 7-0
    ]))


class WOREVT0Types(Register):
    EVENT0_LOW: int
    """ Bits 7-0: Low byte of EVENT0 timeout register.

    The default EVENT0 value gives a 1.0s timeout, assuming a 26.0 MHz crystal.
    """


WOREVT0 = cast(WOREVT0Types, Register(
    "WOREVT0", 0x1F, "Low Byte Event0 Timeout", [
        Entry("EVENT0_LOW", 8, 0x6B),  # Bits 7-0
    ]))


class WORCTRLTypes(Register):
    RC_PD: int
    """ Bit 7: Power down signal to RC oscillator.
    When written to 0, automatic initial calibration will be performed.
    Default value: 1.
    """

    EVENT1: int
    """ Bits 6-4: Timeout setting from register block. Decoded to Event 1 timeout.
    RC oscillator clock frequency equals FXOSC/750, which is 34.7 - 36 kHz,
    depending on crystal frequency. The table below lists the number of clock periods
    after Event 0 before Event 1 times out.
    Setting | tEvent1 (ms)
    --------|---------------------------
    0 (000) | 4 (0.111 - 0.115 ms)
    1 (001) | 6 (0.167 - 0.173 ms)
    2 (010) | 8 (0.222 - 0.230 ms)
    3 (011) | 12 (0.333 - 0.346 ms)
    4 (100) | 16 (0.444 - 0.462 ms)
    5 (101) | 24 (0.667 - 0.692 ms)
    6 (110) | 32 (0.889 - 0.923 ms)
    7 (111) | 48 (1.333 - 1.385 ms)
    Default value: 7 (111).
    """

    RC_CAL: int
    """ Bit 3: Enables (1) or disables (0) the RC oscillator calibration.
    Default value: 1.
    """

    R0: int
    """ Bit 2: Not used. """

    WOR_RES: int
    """ Bits 1-0: Controls the Event 0 resolution as well as maximum timeout of the WOR
    module and maximum timeout under normal RX operation:
    Setting | Resolution (1 LSB)  | Max timeout
    --------|----------------------|-----------------------------
    0 (00)  | 1 period (28-29 µs) | 1.8 - 1.9 seconds
    1 (01)  | 2^5 periods (0.89-0.92 ms) | 58 - 61 seconds
    2 (10)  | 2^10 periods (28-30 ms) | 31 - 32 minutes
    3 (11)  | 2^15 periods (0.91-0.94 s) | 16.5 - 17.2 hours
    Note that WOR_RES should be 0 or 1 when using WOR because WOR_RES > 1 will give a
    very low duty cycle.
    In normal RX operation all settings of WOR_RES can be used.
    Default value: 0 (00).
    """


WORCTRL = cast(WORCTRLTypes, Register(
    "WORCTRL", 0x20, "Wake On Radio Control", [
        Entry("RC_PD", 1, 1),           # Bit 7
        Entry("EVENT1", 3, 7),          # Bits 6-4
        Entry("RC_CAL", 1, 1),          # Bit 3
        Entry("R0", 1, 0),              # Bit 2
        Entry("WOR_RES", 2, 0),         # Bits 1-0
    ]))


class FREND1Types(Register):
    LNA_CURRENT: int
    """ Bits 7-6: Adjusts front-end LNA PTAT current output.
    Default value: 1 (01).
    """

    LNA2MIX_CURRENT: int
    """ Bits 5-4: Adjusts front-end PTAT outputs.
    Default value: 1 (01).
    """

    LODIV_BUF_CURRENT_RX: int
    """ Bits 3-2: Adjusts current in RX LO buffer (LO input to mixer).
    Default value: 1 (01).
    """

    MIX_CURRENT: int
    """ Bits 1-0: Adjusts current in mixer.
    Default value: 2 (10).
    """


FREND1 = cast(FREND1Types, Register(
    "FREND1", 0x21, "Front End RX Configuration", [
        Entry("LNA_CURRENT", 2, 1),           # Bits 7-6
        Entry("LNA2MIX_CURRENT", 2, 1),       # Bits 5-4
        Entry("LODIV_BUF_CURRENT_RX", 2, 1),  # Bits 3-2
        Entry("MIX_CURRENT", 2, 2),           # Bits 1-0
    ]))


class FREND0Types(Register):
    R0_1: int
    """ Bits 7-6: Not used.
    Default value: Reserved.
    """

    LODIV_BUF_CURRENT_TX: int
    """ Bits 5-4: Adjusts current TX LO buffer (input to PA).
    The value to use in this field is given by the SmartRF Studio software [5].
    Default value: 1 (01).
    """

    R0_2: int
    """ Bit 3: Not used.
    Default value: Reserved.
    """

    PA_POWER: int
    """ Bits 2-0: Selects PA power setting. This value is an index to the PATABLE,
    which can be programmed with up to 8 different PA settings.
    In OOK/ASK mode, this selects the PATABLE index to use when transmitting a '1'.
    PATABLE index zero is used in OOK/ASK when transmitting a '0'. The PATABLE settings
    from index '0' to the PA_POWER value are used for ASK TX shaping,
    and for power ramp-up/ramp-down at the start/end of transmission in all TX
    modulation formats.
    Default value: 0 (00).
    """


FREND0 = cast(FREND0Types, Register(
    "FREND0", 0x22, "Front End TX Configuration", [
        Entry("R0_1", 2),                   # Bits 7-6
        Entry("LODIV_BUF_CURRENT_TX", 2, 1),  # Bits 5-4
        Entry("R0_2", 1),                   # Bit 3
        Entry("PA_POWER", 3, 0),              # Bits 2-0
    ]))


class FSCAL3Types(Register):
    FSCAL3_HIGH: int
    """ Bits 7-6: Frequency synthesizer calibration configuration.
    Default value: 2 (0x02).
    The value to write in this field before calibration is given by the
    SmartRF Studio software.
    """

    CHP_CURR_CAL_EN: int
    """ Bits 5-4: Disable charge pump calibration stage when 0.
    Default value: 2 (0x02).
    """

    FSCAL3_LOW: int
    """ Bits 3-0: Frequency synthesizer calibration result register.
    Default value: 9 (1001).
    Digital bit vector defining the charge pump output current, on an exponential scale:
    I_OUT = I_0·2^(FSCAL3[3:0]/4)

    Fast frequency hopping without calibration for each hop can be done by calibrating
    upfront for each frequency and saving the resulting FSCAL3,
    FSCAL2 and FSCAL1 register values. Between each frequency hop, calibration can be
    replaced by writing the FSCAL3, FSCAL2 and FSCAL1 register
    values corresponding to the next RF frequency.
    """


FSCAL3 = cast(FSCAL3Types, Register(
    "FSCAL3", 0x23, "Frequency Synthesizer Calibration", [
        Entry("FSCAL3_HIGH", 2, 2),           # Bits 7-6
        Entry("CHP_CURR_CAL_EN", 2, 2),      # Bits 5-4
        Entry("FSCAL3_LOW", 4, 9),           # Bits 3-0
    ]))


class FSCAL2Types(Register):
    R0: int
    """ Bits 7-6: Not used.
    Default value: Reserved.
    """

    VCO_CORE_H_EN: int
    """ Bit 5: Choose high (1) / low (0) VCO.
    Default value: 0.
    """

    FSCAL2_RESULT: int
    """ Bits 4-0: Frequency synthesizer calibration result register.
    Default value: 10 (0x0A).
    VCO current calibration result and override value.

    Fast frequency hopping without calibration for each hop can be done by calibrating
    upfront for each frequency and saving the resulting FSCAL3,
    FSCAL2 and FSCAL1 register values. Between each frequency hop, calibration can be
    replaced by writing the FSCAL3, FSCAL2 and FSCAL1 register
    values corresponding to the next RF frequency.
    """


FSCAL2 = cast(FSCAL2Types, Register(
    "FSCAL2", 0x24, "Frequency Synthesizer Calibration", [
        Entry("R0", 2, 0),                     # Bits 7-6
        Entry("VCO_CORE_H_EN", 1, 0),        # Bit 5
        Entry("FSCAL2_RESULT", 5, 10),       # Bits 4-0
    ]))


class FSCAL1Types(Register):
    R0: int
    """ Bits 7-6: Not used.
    Default value: Reserved.
    """

    FSCAL1_RESULT: int
    """ Bits 5-0: Frequency synthesizer calibration result register.
    Default value: 32 (0x20).
    Capacitor array setting for VCO coarse tuning.

    Fast frequency hopping without calibration for each hop can be done by calibrating
    upfront for each frequency and saving the resulting FSCAL3,
    FSCAL2 and FSCAL1 register values. Between each frequency hop, calibration can be
    replaced by writing the FSCAL3, FSCAL2 and FSCAL1 register
    values corresponding to the next RF frequency.
    """


FSCAL1 = cast(FSCAL1Types, Register(
    "FSCAL1", 0x25, "Frequency Synthesizer Calibration", [
        Entry("R0", 2, 0),                     # Bits 7-6
        Entry("FSCAL1_RESULT", 6, 32),       # Bits 5-0
    ]))


class FSCAL0Types(Register):
    R0: int
    """ Bit 7: Not used.
    Default value: Reserved.
    """

    FSCAL0_CONTROL: int
    """ Bits 6-0: Frequency synthesizer calibration control.
    Default value: 13 (0x0D).
    The value to use in this register is given by the SmartRF Studio software [5].
    """


FSCAL0 = cast(FSCAL0Types, Register(
    "FSCAL0", 0x26, "Frequency Synthesizer Calibration", [
        Entry("R0", 1, 0),                     # Bit 7
        Entry("FSCAL0_CONTROL", 7, 13),      # Bits 6-0
    ]))


class RCCTRL1Types(Register):
    NOT_USED: int
    """ Bit 7: Not used. """
    RCCTRL0: int
    """ Bits 6-0: RC oscillator configuration. """


RCCTRL1 = cast(RCCTRL1Types, Register("RCCTRL1", 0x27, "RC oscillator configuration.", [
    Entry("NOT_USED", 1, 0),  # Bit 7
    Entry("RCCTRL0", 7, 65),   # Bits 6-0
]))


class RCCTRL0Types(Register):
    R0: int
    """ Bit 7: Not used. """
    RCCTRL0: int
    """ Bits 6-0: RC oscillator configuration. """


RCCTRL0 = cast(RCCTRL0Types, Register("RCCTRL0", 0x28, "RC oscillator configuration.", [
    Entry("R0", 1, 0),  # Bit 7
    Entry("RCCTRL0", 7, 0),   # Bits 6-0
]))


class FSTESTTypes(Register):
    """ Frequency synthesizer calibration control """
    FSTEST: int
    """ Bits 7-0: For test only. Do not write to this register. """


FSTEST = cast(
    FSTESTTypes,
    Register("FSTEST", 0x59, "Frequency synthesizer calibration control", [
        Entry("FSTEST", 8, 0),
    ]))


class PTESTTypes(Register):
    """ Production test """
    PTEST: int
    """ Bits 7-0: Writing 0xBF to this register makes the on-chip temperature sensor
available in the IDLE state. The default 0x7F value should then be written
back before leaving the IDLE state. Other use of this register is for test only """


PTEST = cast(PTESTTypes, Register("PTEST", 0x2A, "Production test", [
    Entry("PTEST", 8, 0x7F),
]))


class AGCTESTTypes(Register):
    """ AGC test """
    AGCTEST: int
    """ Bits 7-0: For test only. Do not write to this register. """


AGCTEST = cast(AGCTESTTypes, Register("AGCTEST", 0x2B, "AGC Test", [
    Entry("AGCTEST", 8, 0),
]))


class TEST2Types(Register):
    """ Various test settings """
    TEST2: int
    """ Bits 7-0: The value to use in this register is given by the
    SmartRF Studio software[5]. This register will be forced to 0x88 or 0x81 when
    it wakes up from SLEEP mode, depending on the configuration of FIFOTHR.
ADC_RETENTION.
Note that the value read from this register when waking up from SLEEP
always is the reset value (0x88) regardless of the ADC_RETENTION
setting. The inverting of some of the bits due to the ADC_RETENTION
setting is only seen INTERNALLY in the analog part.
 """


TEST2 = cast(TEST2Types, Register("TEST2", 0x2C, "Various test settings", [
    Entry("TEST2", 8, 0x88),
]))


class TEST1Types(Register):
    """ Various test settings """
    TEST1: int
    """ Bits 7-0: The value to use in this register is given by the
SmartRF Studio software
[5]. This register will be forced to 0x31 or 0x35 when it wakes up from
SLEEP mode, depending on the configuration of FIFOTHR.
ADC_RETENTION.
Note that the value read from this register when waking up from SLEEP
always is the reset value (0x31) regardless of the ADC_RETENTION
setting. The inverting of some of the bits due to the ADC_RETENTION
setting is only seen INTERNALLY in the analog part. """


TEST1 = cast(TEST1Types, Register("TEST1", 0x2D, "Various test settings", [
    Entry("TEST1", 8, 0x31),
]))


class TEST0Types(Register):
    """ Various test settings """
    TEST0: int
    """ Bits 7-2: The value to use in this register is given by the
    SmartRF Studio software """
    VCO_SEL_CAL_EN: int
    """ Bit 1: Enable VCO selection calibration stage when 1 """
    TEST0_0: int
    """ Bit 0: The value to use in this register is given by the SmartRF Studio
    software """


TEST0 = cast(TEST0Types, Register("TEST0", 0x2E, "Various test settings", [
    Entry("TEST0", 6, 0),
    Entry("VCO_SEL_CAL_EN", 1, 0),
    Entry("TEST0_0", 1, 0),
]))

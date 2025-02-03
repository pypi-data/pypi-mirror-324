from typing import cast
from spireg import Register, Entry
from enum import Enum


class PARTNUMTypes(Register):
    """ Chip ID """
    PARTNUM: int
    """ Chip part number """


PARTNUM = cast(PARTNUMTypes, Register("PARTNUM", 0x30, "Part number for CC1101.", [
        Entry("PARTNUM", 8),
    ]))


class VERSIONTypes(Register):
    """ Chip ID """
    VERSION: int
    """ Chip version number. Subject to change without notice. """


VERSION = cast(VERSIONTypes, Register("VERSION", 0x31, "Current version number.", [
        Entry("VERSION", 8),
    ]))


class FREQESTTypes(Register):
    """ Frequency Offset Estimate from Demodulator """
    FREQOFF_EST: int
    """ The estimated frequency offset (2's complement) of the carrier. Resolution is
    F_XTAL/2^14 (1.59 - 1.65 kHz); range is ±202 kHz to ±210 kHz,
    depending on XTAL frequency.
    Frequency offset compensation is only supported for 2-FSK, GFSK, 4-FSK, and MSK
    modulation. This register will read 0 when using ASK or OOK modulation. """


FREQEST = cast(FREQESTTypes, Register("FREQEST", 0x32, "Frequency Offset Estimate.", [
        Entry("FREQOFF_EST", 8),
    ]))


class LQITypes(Register):
    """ Demodulator Estimate for Link Quality """
    CRC_OK: int
    """ The last CRC comparison matched. Cleared when entering/restarting RX mode. """
    LQI_EST: int
    """ The Link Quality Indicator estimates how easily a received signal can be
    demodulated. Calculated over the 64 symbols following the sync word. """


LQI = cast(LQITypes, Register("LQI", 0x33, "Demodulator estimate for Link Quality.", [
        Entry("CRC_OK", 1),
        Entry("LQI_EST", 7),
    ]))


class RSSITypes(Register):
    """ Received Signal Strength Indication """
    RSSI: int
    """ Received signal strength indicator """


RSSI = cast(RSSITypes, Register("RSSI", 0x34, "Received signal strength indication.", [
        Entry("RSSI", 8),
    ]))


class MARCSTATES(Enum):
    SLEEP = 0x00
    IDLE = 0x01
    XOFF = 0x02
    VCOON_MC = 0x03
    REGON_MC = 0x04
    MANCAL = 0x05
    VCOON = 0x06
    REGON = 0x07
    STARTCAL = 0x08
    BWBOOST = 0x09
    FS_LOCK = 0x0A
    IFADCON = 0x0B
    ENDCAL = 0x0C
    RX = 0x0D
    RX_END = 0x0E
    RX_RST = 0x0F
    TXRX_SWITCH = 0x10
    RXFIFO_OVERFLOW = 0x11
    FSTXON = 0x12
    TX = 0x13
    TX_END = 0x14
    RXTX_SWITCH = 0x15
    TXFIFO_UNDERFLOW = 0x16


class MARCSTATETypes(Register):
    """ Main Radio Control State Machine State """
    R0: int
    """ Bit 7-5: Not used. """
    MARC_STATE: MARCSTATES
    """ Bit 4-0: Main Radio Control FSM State

    Note: it is not possible to read back the SLEEP or XOFF state numbers because
    setting CSn low will make the chip enter the IDLE mode from the
    SLEEP or XOFF states. """


MARCSTATE = cast(
    MARCSTATETypes,
    Register("MARCSTATE", 0x35, "Control state machine state.", [
        Entry("R0", 3),
        Entry("MARC_STATE", 5),
    ]))


class WORTIME1Types(Register):
    """ High Byte of WOR Time """
    TIME: int
    """ High byte of timer value in WOR module """


WORTIME1 = cast(WORTIME1Types, Register("WORTIME1", 0x36, "High byte of WOR timer.", [
        Entry("TIME", 8),
    ]))


class WORTIME0Types(Register):
    """ Low Byte of WOR Time """
    TIME: int
    """ Low byte of timer value in WOR module """


WORTIME0 = cast(WORTIME0Types, Register("WORTIME0", 0x37, "Low byte of WOR timer.", [
        Entry("TIME", 8),
    ]))


class PKTSTATUSRegister(Register):
    """ Current GDOx status and packet status """
    CRC_OK: int
    """ The last CRC comparison matched. Cleared when entering/restarting RX mode. """
    CS: int
    """ Carrier sense. Cleared when entering IDLE mode. """
    PQT_REACHED: int
    """ Preamble Quality reached. If leaving RX state when this bit is set it will
    remain asserted until the chip re-enters RX state (MARCSTATE=0x0D). The bit will
    also be cleared if PQI goes below the programmed PQT value. """
    CCA: int
    """ Channel is clear """
    SFD: int
    """ Start of Frame Delimiter. In RX, this bit is asserted when sync word has been
    received and de-asserted at the end of the packet. It will also deassert when a
    packet is discarded due to address or maximum length filtering or the radio
    enters RXFIFO_OVERFLOW state. In TX this bit will always read as 0. """
    GDO2: int
    """ Current GDO2 value. Note: the reading gives the non-inverted value irrespective
    of what IOCFG2.GDO2_INV is programmed to.

    It is not recommended to check for PLL lock by reading PKTSTATUS[2]
    with GDO2_CFG=0x0A. """
    UNUSED: int
    """ Unused """
    GDO0: int
    """ Current GDO0 value. Note: the reading gives the non-inverted value irrespective
    of what IOCFG0.GDO0_INV is programmed to.

    It is not recommended to check for PLL lock by reading PKTSTATUS[0]
    with GDO0_CFG=0x0A. """


PKTSTATUS = cast(
    PKTSTATUSRegister,
    Register("PKTSTATUS", 0x38, "Current GDOx status and packet status.", [
        Entry("CRC_OK", 1),
        Entry("CS", 1),
        Entry("PQT_REACHED", 1),
        Entry("CCA", 1),
        Entry("SFD", 1),
        Entry("GDO2", 1),
        Entry("UNUSED", 1),
        Entry("GDO0", 1),
    ]))


class VCO_VC_DACTypes(Register):
    """ Current setting from PLL calibration module """
    VCO_VC_DAC: int
    """ Status register for test only. """


VCO_VC_DAC = cast(
    PKTSTATUSRegister,
    Register("VCO_VC_DAC", 0x39, "Current setting from PLL calibration module.", [
        Entry("VCO_VC_DAC", 8),
    ]))


class TXBYTESTypes(Register):
    """ Underflow and Number of Bytes """
    TXFIFO_UNDERFLOW: int
    """ """
    NUM_TXBYTES: int
    """ Number of bytes in TX FIFO """


TXBYTES = cast(
    TXBYTESTypes,
    Register("TXBYTES", 0x3A, "Underflow and number of bytes in the TX FIFO.", [
        Entry("TXFIFO_UNDERFLOW", 1),
        Entry("NUM_TXBYTES", 7),
    ]))


class RXBYTESTypes(Register):
    """ Overflow and Number of Bytes """
    RXFIFO_OVERFLOW: int
    """ """
    NUM_RXBYTES: int
    """ Number of bytes in RX FIFO """


RXBYTES = cast(
    RXBYTESTypes,
    Register("RXBYTES", 0x3B, "Overflow and number of bytes in the RX FIFO.", [
        Entry("RXFIFO_OVERFLOW", 1),
        Entry("NUM_RXBYTES", 7),
    ]))


class RCCTRL1_STATUS(Register):
    """ Last RC oscillator calibration result """
    R0: int
    """ Not used """
    RCCTRL1_STATUS: int
    """ Contains the value from the last run of the RC oscillator calibration routine.
    For usage description refer to Application Note AN047 [4] """


RCCTRL1_STATUS = cast(
    RCCTRL1_STATUS,
    Register("RCCTRL1_STATUS", 0x3C, "Last RC oscillator calibration result.", [
        Entry("R0", 6),
        Entry("RCCTRL1_STATUS", 2),
    ]))


class RCCTRL0_STATUS(Register):
    """ Last RC oscillator calibration result """
    R0: int
    """ Not used """
    RCCTRL0_STATUS: int
    """ Contains the value from the last run of the RC oscillator calibration routine.
    For usage description refer to Application Note AN047 [4] """


RCCTRL0_STATUS = cast(
    RCCTRL0_STATUS,
    Register("RCCTRL0_STATUS", 0x3D, "Last RC oscillator calibration result.", [
        Entry("R0", 6),
        Entry("RCCTRL0_STATUS", 2),
    ]))

from enum import Enum


class EnableStateEnum(Enum):
    ON = 2
    OFF = 3

class EnumMode(Enum):
    AUTO = 0
    MANUAL = 1

class KneeEnum(Enum):
    AUTO = 0
    MANUAL = 4

class ExposureModeEnum(Enum):
    FULL_AUTO = 0
    MANUAL = 3
    SHUTTER_PRIORITY = 10
    IRIS_PRIORITY = 11

class ShutterSpeedEnum_60(Enum):
    s1_1 = 0
    s2_3 = 1
    s1_2 = 2
    s1_3 = 3
    s1_4 = 4
    s1_6 = 5
    s1_8 = 6
    s1_10 = 7
    s1_15 = 8
    s1_20 = 9
    s1_30 = 10
    s1_50 = 11
    s1_60 = 12
    s1_90 = 13
    s1_100 = 14
    s1_125 = 15
    s1_180 = 16
    s1_250 = 17
    s1_350 = 18
    s1_500 = 19
    s1_725 = 20
    s1_1000 = 21
    s1_1500 = 22
    s1_2000 = 23
    s1_3000 = 24
    s1_4000 = 25
    s1_6000 = 26
    s1_10000 = 27

class IrisSettingsEnum(Enum):
    F1_8 = 20
    F2_0 = 19
    F2_2 = 18
    F2_4 = 17
    F2_6 = 16
    F2_8 = 15
    F3_1 = 14
    F3_4 = 13
    F3_7 = 12
    F4_0 = 11
    F4_4 = 10
    F4_8 = 9
    F5_2 = 8
    F5_6 = 7
    F6_2 = 6
    F6_8 = 5
    F7_3 = 4
    F8_0 = 3
    F8_7 = 2
    F9_6 = 1
    FCLOSE = 0

class GainValueEnum(Enum):
    GAIN_48DB = 11
    GAIN_45DB = 10
    GAIN_42DB = 15
    GAIN_39DB = 14
    GAIN_36DB = 13
    GAIN_33DB = 12
    GAIN_30DB = 11
    GAIN_27DB = 10
    GAIN_24DB = 9
    GAIN_21DB = 8
    GAIN_18DB = 7
    GAIN_15DB = 6
    GAIN_12DB = 5
    GAIN_9DB = 4
    GAIN_6DB = 3
    GAIN_3DB = 2
    GAIN_0DB = 1
    GAIN_n3DB = 0

class VisibilityEnhancerEffectLevel(Enum):
    DARK = 0
    NORMAL = 1
    BRIGHT = 2

class VisibilityEnhancerBrightnessCompensation(Enum):
    VERY_DARK = 0
    DARK = 1
    STANDARD = 2
    BRIGHT = 3

class VisibilityEnhancerCompensationLevel(Enum):
    LOW = 0
    MID = 1
    HIGH = 2

class LowLightBiasLevel(Enum):
    LLB_04 = 4
    LLB_05 = 5
    LLB_06 = 6
    LLB_07 = 7
    LLB_08 = 8
    LLB_09 = 9
    LLB_0A = 10

class WhiteBalanceModeEnum(Enum):
    AUTO_1 = 0
    AUTO_2 = 1
    PRESET_A = 2
    PRESET_B = 3
    ONE_PUSH = 4
    MANUAL = 5

class MatrixSelectEnum(Enum):
    STD = 2
    OFF = 3
    HIGH_SAT = 4
    FL_LIGHT = 5
    MOVIE = 6
    STILL = 7
    CINEMA = 8
    PRO = 9
    ITU709 = 10
    B_W = 11

class ChromaSuppressionEnum(Enum):
    OFF = 0
    WEAK = 1
    MID = 2
    STRONG = 3

class DetailBandWidthEnum(Enum):
    DEFAULT = 0
    LOW = 1
    MID = 2
    HIGH = 3
    WIDE = 4

class DetailBWBalanceEnum(Enum):
    TYPE_0 = 0
    TYPE_1 = 1
    TYPE_2 = 2
    TYPE_3 = 3
    TYPE_4 = 4

class GammaLevelEnum(Enum):
    STD = 0
    STRAIGHT = 1
    PATTERN = 2
    MOVIE = 8
    STILL = 9
    CINE1 = 10
    CINE2 = 11
    CINE3 = 12
    CINE4 = 13
    ITU709 = 14

class BlackGammaRangeEnum(Enum):
    WIDE = 0
    MIDDLE = 1
    NARROW = 2

class GammaPolarityEnum(Enum):
    POSITIVE = 0
    NEGATIVE = 1

class PictureProfileEnum(Enum):
    PP1 = 0
    PP2 = 1
    PP3 = 2
    PP4 = 3
    PP5 = 4
    PP6 = 5

class NoiseReductionLevel(Enum):
    OFF = 0  # Nessuna riduzione del rumore
    WEAK = 1  # Riduzione debole
    NR_2 = 2  # Livello di riduzione 2
    NR_3 = 3  # Livello di riduzione 3
    NR_4 = 4  # Livello di riduzione 4
    STRONG = 5  # Riduzione forte
    ENABLE_2D_3D_NR = 127  # Abilita 2D NR e 3D NR

class NoiseReduction2DEnum(Enum):
    OFF = 0  # Nessuna riduzione
    WEAK = 1  # Riduzione debole
    NR_2 = 2  # Livello 2
    NR_3 = 3  # Livello 3
    NR_4 = 4  # Livello 4
    STRONG = 5  # Riduzione forte

class NoiseReduction3DEnum(Enum):
    OFF = 0  # Nessuna riduzione
    WEAK = 1  # Riduzione debole
    NR_2 = 2  # Livello 2
    NR_3 = 3  # Livello 3
    NR_4 = 4  # Livello 4
    STRONG = 5  # Riduzione forte

class FocusModeEnum(Enum):
    AUTO = 2
    MANUAL = 3
    TOGGLE = 10

class AutoFocusModeEnum(Enum):
    NORMAL = 0
    INTERVAL = 1
    ZOOM_TRIGGER = 2

class AutoFocusSensitivityEnum(Enum):
    NORMAL = 2
    LOW = 3

class AutoFocusOperationTime(Enum):
    NORMAL = 0
    INTERVAL = 1
    ZOOM_TRIGGER = 2



class IRCorrectionEnum(Enum):
    STANDARD = 0
    IRLIGHT = 1

class TallyLevel(Enum):
    OFF = 0
    LOW = 4
    HIGH = 5

class HdmiColorFormatEnum(Enum):
    YCbCr = 0
    RGB = 1

class PictureEffectEnum(Enum):
    OFF = 0
    BandW = 4

class ZoomModeEnum(Enum):
    DIGITAL = 2
    OPTICAL = 3
    CLEAR_IMAGE = 4

class ZoomRatioEnum(Enum):
    ZOOM_1X = 0      # 0x0000
    ZOOM_2X = 3521   # 0x0DC1
    ZOOM_3X = 6252   # 0x186C
    ZOOM_4X = 8213   # 0x2015
    ZOOM_5X = 9620   # 0x2594
    ZOOM_6X = 10679  # 0x29B7
    ZOOM_7X = 11515  # 0x2CFB
    ZOOM_8X = 12208  # 0x2FB0
    ZOOM_9X = 12812  # 0x320C
    ZOOM_10X = 13357 # 0x342D
    ZOOM_11X = 13832 # 0x3608
    ZOOM_12X = 14250 # 0x37AA
    ZOOM_13X = 14620 # 0x391C
    ZOOM_14X = 14950 # 0x3A66
    ZOOM_15X = 15248 # 0x3B90
    ZOOM_16X = 15516 # 0x3C9C
    ZOOM_17X = 15761 # 0x3D91
    ZOOM_18X = 15986 # 0x3E72
    ZOOM_20X = 16384 # 0x4000
    ZOOM_30X_CLEAR_IMAGE = 21846 # 0x5556
    ZOOM_40X_CLEAR_IMAGE = 24576 # 0x6000
    ZOOM_60X_DIGITAL = 27307     # 0x6AAB
    ZOOM_80X_DIGITAL = 28672     # 0x7000
    ZOOM_100X_DIGITAL = 29492    # 0x7334
    ZOOM_120X_DIGITAL = 30038    # 0x7556
    ZOOM_140X_DIGITAL = 30428    # 0x76DC
    ZOOM_160X_DIGITAL = 30720    # 0x7800
    ZOOM_180X_DIGITAL = 30948    # 0x78E4
    ZOOM_200X_DIGITAL = 31130    # 0x799A
    ZOOM_220X_DIGITAL = 31279    # 0x7A2F
    ZOOM_240X_DIGITAL = 31424    # 0x7AC0
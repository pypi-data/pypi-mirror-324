from visca.dictionary.enumerations import *

class DetailMemories:
    # Stato interno
    _detail_level: int
    _detail_mode: EnumMode
    _detail_bandwidth: DetailBandWidthEnum
    _detail_crispening: int
    _detail_hv_balance: int
    _detail_bw_balance: DetailBWBalanceEnum
    _detail_limit: int
    _detail_highlight: int
    _detail_super_low: int

    def __init__(self):
        # Valori di default
        self._detail_level = 0
        self._detail_mode = EnumMode.MANUAL
        self._detail_bandwidth = DetailBandWidthEnum.DEFAULT
        self._detail_crispening = 0
        self._detail_hv_balance = 0
        self._detail_bw_balance = DetailBWBalanceEnum.TYPE_2
        self._detail_limit = 0
        self._detail_highlight = 0
        self._detail_super_low = 0

    @property
    def detailLevel(self):
        return self._detail_level

    @detailLevel.setter
    def detailLevel(self, value):
        self._detail_level = value

    @property
    def detailMode(self):
        return self._detail_mode

    @detailMode.setter
    def detailMode(self, value: EnumMode):
        self._detail_mode = value

    @property
    def detailBandwidth(self):
        return self._detail_bandwidth

    @detailBandwidth.setter
    def detailBandwidth(self, value: DetailBandWidthEnum):
        self._detail_bandwidth = value

    @property
    def detailCrispening(self):
        return self._detail_crispening

    @detailCrispening.setter
    def detailCrispening(self, value):
        self._detail_crispening = value

    @property
    def detailHvBalance(self):
        return self._detail_hv_balance

    @detailHvBalance.setter
    def detailHvBalance(self, value):
        self._detail_hv_balance = value

    @property
    def detailBwBalance(self):
        return self._detail_bw_balance

    @detailBwBalance.setter
    def detailBwBalance(self, value: DetailBWBalanceEnum):
        self._detail_bw_balance = value

    @property
    def detailLimit(self):
        return self._detail_limit

    @detailLimit.setter
    def detailLimit(self, value):
        self._detail_limit = value

    @property
    def detailHighlight(self):
        return self._detail_highlight

    @detailHighlight.setter
    def detailHighlight(self, value):
        self._detail_highlight = value

    @property
    def detailSuperLow(self):
        return self._detail_super_low

    @detailSuperLow.setter
    def detailSuperLow(self, value):
        self._detail_super_low = value

    def serialize(self):
        return {
            "detail_level": self._detail_level,
            "detail_mode": self._detail_mode,
            "detail_bandwidth": self._detail_bandwidth,
            "detail_crispening": self._detail_crispening,
            "detail_hv_balance": self._detail_hv_balance,
            "detail_bw_balance": self._detail_bw_balance,
            "detail_limit": self._detail_limit,
            "detail_highlight": self._detail_highlight,
            "detail_super_low": self._detail_super_low
        }

    def deserialize(self, data):
        try:
            if not isinstance(data, dict):
                raise ValueError("I dati devono essere un dizionario.")

            self._detail_level = data.get("detail_level", self._detail_level)
            self._detail_mode = data.get("detail_mode", self._detail_mode)
            self._detail_bandwidth = data.get("detail_bandwidth", self._detail_bandwidth)
            self._detail_crispening = data.get("detail_crispening", self._detail_crispening)
            self._detail_hv_balance = data.get("detail_hv_balance", self._detail_hv_balance)
            self._detail_bw_balance = data.get("detail_bw_balance", self._detail_bw_balance)
            self._detail_limit = data.get("detail_limit", self._detail_limit)
            self._detail_highlight = data.get("detail_highlight", self._detail_highlight)
            self._detail_super_low = data.get("detail_super_low", self._detail_super_low)

        except Exception as e:
            print(f"Errore durante la deserializzazione: {e}")
            return False

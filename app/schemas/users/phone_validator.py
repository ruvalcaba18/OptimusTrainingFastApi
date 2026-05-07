class PhoneValidator:
    _COUNTRY_DIGITS = {
        "1": 10, "34": 9, "51": 9, "52": 10,
        "54": 10, "55": 11, "56": 9, "57": 10,
    }

    @classmethod
    def validate(cls, phone: str) -> str:
        cls._check_format(phone)
        raw = phone[1:]
        cls._check_digits(raw)
        cls._check_country_length(raw)

        return phone

    @staticmethod
    def _check_format(phone: str):
        if not phone.startswith("+") or len(phone) < 8:
            raise ValueError("Formato inválido")

    @staticmethod
    def _check_digits(raw: str):
        if not raw.isdigit():
            raise ValueError("Solo dígitos después del +")

    @classmethod
    def _check_country_length(cls, raw: str):
        code = raw[:2] if raw[:2] in cls._COUNTRY_DIGITS else raw[:1]
        
        expected = cls._COUNTRY_DIGITS.get(code)
        if expected and len(raw) - len(code) != expected:
            raise ValueError(f"Se esperan {expected} dígitos para +{code}")

from typing import Any

from app.utils import normalized2upper


class Base:
    _normalize: list[str]

    def __init__(self, data: dict):
        for key, value in data.items():
            key: str
            value: Any
            if not hasattr(self, key) or not value:
                continue
            if key.endswith('_id'):
                try:
                    value = value[0]
                except TypeError:
                    pass
            if key in self._normalize:
                value = normalized2upper(value)
            setattr(self, key, value)

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.__dict__}'

    @classmethod
    def get_fields(cls) -> list[str]:
        return [k for k, v in cls.__dict__.items() if not k.startswith('_') and not isinstance(v, classmethod)]


class CrmLead(Base):
    id: int = None
    user_id: int = None
    team_id: int = None
    partner_id: int = None
    contact_name: str = None
    partner_name: str = None
    display_name: str = None
    email_from: str = None
    email_domain_criterion: str = None
    phone: str = None
    mobile: str = None
    website: str = None

    _normalize: list[str] = ['contact_name', 'partner_name', 'display_name']

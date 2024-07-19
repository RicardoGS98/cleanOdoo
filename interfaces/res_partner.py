from interfaces import CrmLead
from interfaces.crm_lead import Base


class ResPartner(Base):
    id: int = None
    name: str = None
    user_id: int = None
    parent_id: int = None
    is_company: bool = None
    team_id: int = None
    phone: str = None
    mobile: str = None
    website: str = None
    email: str = None

    _normalize: list[str] = ['name']

    @classmethod
    def create_from_lead(cls, lead: CrmLead, is_company: bool = False) -> dict:

        # Se inicializa como company
        name = lead.partner_name
        email = lead.email_domain_criterion
        if not is_company:
            try:
                name = max(lead.contact_name, lead.display_name)
            except TypeError:
                name = lead.contact_name or lead.display_name
            email = lead.email_from
        final_dict = dict(email=email, name=name, is_company=is_company)

        lead_fields = lead.get_fields()
        for field in cls.get_fields():
            if field not in lead_fields or field == 'id':
                continue
            final_dict[field] = getattr(lead, field)
        return final_dict

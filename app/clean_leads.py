import Levenshtein

from app.odoo import Odoo
from interfaces import CrmLead, ResPartner


class CleanLeads:
    odoo = Odoo()
    contacts = 0
    companies = 0
    partners_by_parent_id: dict[int, list[ResPartner]] = {}

    def __init__(self):
        self.odoo = Odoo()

    def create_partner_from_lead(self, _lead: CrmLead, _partner_id: int) -> None:
        partner_dict = ResPartner.create_from_lead(_lead)
        partner_dict['parent_id'] = _partner_id
        _id = self.odoo.create('res.partner', partner_dict)
        self.contacts += 1

        # Se actualiza el dict por parent_id
        partner = ResPartner({**partner_dict, 'id': _id})
        self.partners_by_parent_id.setdefault(_partner_id, []).append(partner)

    def clean_leads(self) -> None:
        # Se extraen los leads de odoo:
        data = self.odoo.list_all(
            'crm.lead', domain=[["|", ("contact_name", "!=", False), ("partner_name", "!=", False)]],
            fields=CrmLead.get_fields()
        )
        leads = list(map(CrmLead, data))

        # Se extraen los partners de odoo:
        data = self.odoo.list_all('res.partner', fields=ResPartner.get_fields())
        _partners = list(map(ResPartner, data))

        incorrectos = []
        for lead in leads:
            # Por alguna razon decidieron que el nombre a mostrar podría ser lo mismo más grande que el partner_name o
            # viceversa por lo que comprobamos ambas
            p, d, c = lead.partner_name, lead.display_name, lead.contact_name
            p_sim = Levenshtein.ratio(p, d)
            if (p or not c) and (p in d or d in p or p_sim > 0.8) or c and not p and (c not in d or d not in c):
                continue
            incorrectos.append(lead)

        # Se crean dict para búsqueda mas rapida
        partners: dict[str, ResPartner] = {p.name: p for p in sorted(_partners, key=lambda _p: _p.id) if p.name}
        for p in _partners:
            if p.is_company or not p.name or not p.parent_id:
                continue
            self.partners_by_parent_id.setdefault(p.parent_id, []).append(p)

        for lead in incorrectos:
            # ¿Existe ya una compañía para ese `partner_name`?
            company: ResPartner = partners.get(lead.partner_name)
            if company:
                # El partner_id final con el que actualizar el lead
                partner_id = company.id

                # Buscamos a la persona en la compannia
                for p in self.partners_by_parent_id.get(partner_id, []):
                    if p.name in (lead.display_name, lead.contact_name):
                        break
                else:
                    self.create_partner_from_lead(lead, partner_id)
            else:
                # Aqui ya creamos la compannia para obtener el id que será el `parent_id`
                # en caso de que no exista la persona
                company_dict = ResPartner.create_from_lead(lead, True)
                partner_id = self.odoo.create('res.partner', company_dict)
                self.companies += 1

                # Se actualiza el dict de companies:
                company = ResPartner({**company_dict, 'id': partner_id})
                partners[company.name] = company

                # No buscamos la persona para evitar actualizar personas con el mismo nombre pero de distinta company.
                #  Simplemente se crea
                self.create_partner_from_lead(lead, partner_id)

            # Por último se actualiza el lead:
            data = dict(partner_id=partner_id, name=company.name)
            self.odoo.update('crm.lead', lead.id, data)

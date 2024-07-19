import unittest
from unittest.mock import patch

from interfaces import CrmLead  # Asegúrate de importar correctamente tu módulo


class TestCrmLead(unittest.TestCase):

    @patch('interfaces.crm_lead.normalized2upper')
    def test_initialization_with_normalization(self, mock_normalized):
        mock_normalized.side_effect = lambda x: x.upper()  # Simulando el comportamiento de la función

        data = {
            'contact_name': 'test name',
            'partner_name': 'partner',
            'display_name': 'display',
            'email_from': 'test@example.com'
        }
        lead = CrmLead(data)
        self.assertEqual(lead.contact_name, 'TEST NAME')
        self.assertEqual(lead.partner_name, 'PARTNER')
        self.assertEqual(lead.display_name, 'DISPLAY')
        self.assertEqual(lead.email_from, 'test@example.com')

        # Verificar que las llamadas se hicieron correctamente
        mock_normalized.assert_any_call('test name')
        mock_normalized.assert_any_call('partner')
        mock_normalized.assert_any_call('display')

    def test_initialization_without_normalization(self):
        data = {
            'email_from': 'test@example.com',
            'phone': '123456789'
        }
        lead = CrmLead(data)
        self.assertEqual(lead.email_from, 'test@example.com')
        self.assertEqual(lead.phone, '123456789')

    def test_initialization_with_id_list(self):
        data = {
            'user_id': [1, 4]
        }
        lead = CrmLead(data)
        self.assertEqual(lead.user_id, 1)

    def test_initialization_with_id_single_value(self):
        data = {
            'user_id': 2
        }
        lead = CrmLead(data)
        self.assertEqual(lead.user_id, 2)

    def test_repr(self):
        data = {
            'contact_name': 'test name'
        }
        lead = CrmLead(data)
        expected_repr = "CrmLead: {'contact_name': 'TEST NAME'}"
        self.assertEqual(repr(lead), expected_repr)

    def test_get_fields(self):
        fields = CrmLead.get_fields()
        expected_fields = [
            'id', 'user_id', 'team_id', 'partner_id',
            'contact_name', 'partner_name', 'display_name', 'email_from',
            'email_domain_criterion', 'phone', 'mobile', 'website'
        ]
        self.assertListEqual(fields, expected_fields)


if __name__ == '__main__':
    unittest.main()

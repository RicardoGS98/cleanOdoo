import unittest
from random import randint
from unittest.mock import patch

from app.clean_leads import CleanLeads  # Asegúrate de importar correctamente tu módulo


class TestCleanLeads(unittest.TestCase):

    @patch('app.clean_leads.Odoo', autospec=True)
    @patch('app.clean_leads.Levenshtein.ratio', autospec=True)
    def test_clean_leads(self, mock_levenshtein, mock_odoo):
        # Configuración del mock de Odoo
        mock_odoo_instance = mock_odoo.return_value

        # Simulación de datos de leads y partners
        leads_data = [
            {'id': 1, 'partner_name': 'Company A', 'display_name': 'Company A', 'contact_name': 'Alice'},
            {'id': 2, 'partner_name': 'Company B', 'display_name': 'Company B', 'contact_name': 'Bob'}
        ]
        partners_data = [
            {'id': 1, 'name': 'Company A', 'parent_id': None},
            {'id': 2, 'name': 'Company B', 'parent_id': None}
        ]

        mock_odoo_instance.list_all.side_effect = [leads_data, partners_data]

        # Simulación de la función de ratio de Levenshtein
        mock_levenshtein.side_effect = lambda x, y: 1.0 if x == y else 0.0

        # Instancia de CleanLeads y llamada al método clean_leads
        cleaner = CleanLeads()
        cleaner.clean_leads()

        # Verificación de llamadas a métodos de Odoo
        self.assertEqual(mock_odoo_instance.create.call_count, 0)  # No debería crear nada si es correcto
        self.assertEqual(mock_odoo_instance.update.call_count, 0)  # No debería actualizar nada si es correcto

    @patch('app.clean_leads.Odoo', autospec=True)
    def test_clean_leads_with_incorrect_leads(self, mock_odoo):
        # Configuración del mock de Odoo
        mock_odoo_instance = mock_odoo.return_value

        # Simulación de datos de leads y partners
        leads_data = [
            {'id': 1, 'partner_name': 'Company A', 'display_name': 'Alice', 'contact_name': 'Alice'},
            {'id': 2, 'partner_name': 'Company B', 'display_name': 'Company B', 'contact_name': 'Bob'},
            {'id': 3, 'partner_name': 'Company C', 'display_name': 'Alberto', 'contact_name': 'Alberto Perez'},
            {'id': 4, 'partner_name': 'Company C', 'display_name': 'Jose', 'contact_name': 'Jose Luis'},
            {'id': 4, 'partner_name': 'Company C', 'display_name': 'Manolo', 'contact_name': 'Manolo Luis'},
            {'id': 5, 'partner_name': 'Company D', 'display_name': 'Company D', 'contact_name': 'Jose Lopez'},
        ]
        partners_data = [
            {'id': 1, 'name': 'Company A', 'parent_id': None},
            {'id': 2, 'name': 'Company B', 'parent_id': None}
        ]

        mock_odoo_instance.list_all.side_effect = [leads_data, partners_data]

        # Simulación de creación de partners y leads
        mock_odoo_instance.create.side_effect = lambda *_, **__: randint(1, 1000)  # IDs para nuevos partners

        # Instancia de CleanLeads y llamada al método clean_leads
        cleaner = CleanLeads()
        cleaner.clean_leads()

        # Verificación de la cantidad de companies creadas
        self.assertEqual(cleaner.contacts, 4)
        self.assertEqual(cleaner.companies, 1)

        # Verificación de llamadas a métodos de Odoo
        self.assertEqual(mock_odoo_instance.create.call_count, 5)  # Debería crear un nuevo company y un nuevo contact
        self.assertEqual(mock_odoo_instance.update.call_count, 4)  # Debería actualizar un lead


if __name__ == '__main__':
    unittest.main()

import os
from xmlrpc.client import ServerProxy

from app.utils import cache_decorator


class Odoo:
    url = os.environ['ODOO_HOST']
    uid = os.environ['ODOO_ID']
    pw = os.environ['ODOO_PW']
    db = os.environ['ODOO_DB']

    def _execute(self, table: str, func: str, domain=(), **others):
        with ServerProxy('{}/xmlrpc/2/object'.format(self.url), allow_none=True, use_builtin_types=True) as models:
            return models.execute_kw(self.db, self.uid, self.pw, table, func, domain, others)

    def create(self, table: str, data: dict, **others):
        return self._execute(table, func='create', domain=[data], **others)

    def update(self, table: str, _id: int, data: dict, **others):
        return self._execute(table, func='write', domain=[[_id], data], **others)

    @cache_decorator
    def list_all(self, table: str, limit: int = None, **others):
        return self._execute(table, 'search_read', limit=limit, **others)

    @cache_decorator
    def search_by(self, table: str, field: str, value: str, comp: str):
        if not all([field, value, comp, table]):
            raise Exception('All params must be set')
        return self._execute(table, 'search', [[(field, comp, value)]])

    def delete(self, table: str, ids: list[int]):
        self._execute(table, func='unlink', domain=[ids])

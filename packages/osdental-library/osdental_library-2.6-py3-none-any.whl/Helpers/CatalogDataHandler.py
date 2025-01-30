from sqlalchemy import text, Row
from Database.Connection import DBConnection

class CatalogDataHandler:

    def __init__(self):
        self.db = DBConnection()
    
    def get_catalog_data(self, catalog_name:str) -> Row:
        session = self.db.get_session()
        query = text('EXEC CATALOG.sps_GetCatalogByName @i_nameCatalog = :catalog_name')
        result = session.execute(query, {'catalog_name': catalog_name})
        rows = result.fetchall()
        data = {}
        for row in rows:
            if row.Value != '':
                data[row.Code] = row.Value
        
        session.close()
        return data
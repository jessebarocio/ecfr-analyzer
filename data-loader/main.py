from ecfr_api import ECFRAPI
from ecfr_database import ECFRDatabase

class DataLoader:
    def __init__(self, api_base_url: str, db_path: str):
        self.api_base_url = api_base_url
        self.ecfr_api = ECFRAPI(api_base_url)
        self.db = ECFRDatabase(db_path)

    def run(self):
        # Load agencies
        agencies = self.ecfr_api.get_agencies()
        for agency in agencies: 
            self.db.insert_agency(agency, None)

            for child in agency.get('children', []):
                self.db.insert_agency(child, parent_id=agency['slug'])
        
        # Load titles
        titles = self.ecfr_api.get_titles()
        # Filter out reserved
        for title in filter(lambda t: t['reserved'] == False, titles):
            self.db.insert_title(title)


if __name__ == "__main__":
    loader = DataLoader(api_base_url="https://www.ecfr.gov/", db_path="ecfr.db")
    loader.run()

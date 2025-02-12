import logging
import time
from ecfr_api import ECFRAPI
from ecfr_database import ECFRDatabase
from code_info import CodeInfo

logger = logging.getLogger(__name__)


class DataLoader:
    def __init__(self, api_base_url: str, db_path: str, cache_dir: str):
        self.api = ECFRAPI(api_base_url, cache_dir)
        self.db = ECFRDatabase(db_path)

    def refresh_agencies(self):
        logger.info("Refreshing agencies and code references")
        agencies = self.api.get_agencies()

        def insert_agency(agency, parent_id):
            self.db.insert_agency(agency, parent_id)
            self.db.clear_code_references(agency["slug"])
            for code_reference in agency.get("cfr_references", []):
                self.db.insert_code_reference(
                    agency["slug"],
                    code_reference.get("title"),
                    code_reference.get("subtitle"),
                    code_reference.get("chapter"),
                    code_reference.get("subchapter"),
                    code_reference.get("part"),
                    code_reference.get("subpart"),
                    code_reference.get("section"),
                )
            for child in agency.get("children", []):
                insert_agency(child, agency["slug"])

        for agency in agencies:
            insert_agency(agency, None)
            self.db.commit()

    def refresh_titles(self):
        logger.info("Loading titles")
        titles = self.api.get_titles()
        # Filter out reserved titles
        for title in filter(lambda t: t["reserved"] == False, titles):
            self.db.insert_title(title)
        self.db.commit()

    def process_code_references(self):
        # Loop through all code references that have not been processed yet and calculate their metrics
        code_references = self.db.get_code_references_for_processing()
        for code_reference in code_references:
            try:
                xml = self.api.get_xml(
                    code_reference["latest_issue_date"],
                    code_reference["title_id"],
                    code_reference["subtitle"],
                    code_reference["chapter"],
                    code_reference["subchapter"],
                    code_reference["part"],
                    code_reference["subpart"],
                    code_reference["section"],
                )

                if xml is not None:
                    code_info = CodeInfo(code_reference, xml)
                    reference_text = code_info.get_reference_text()
                    name = code_info.get_name()
                    link = code_info.get_link()
                    metrics = code_info.calculate_burden_score()
                    self.db.set_code_reference_metrics(
                        code_reference["id"],
                        reference_text,
                        name,
                        link,
                        metrics["burden_score"],
                        metrics["word_count"],
                    )
                    self.db.commit()
            except Exception as e:
                logger.error(
                    f"Error processing code reference {code_reference['id']}: {e}"
                )
                self.db.set_code_reference_processing_failed(code_reference["id"])
                self.db.commit()
        # Update the burden category (HIGH, MEDIUM, LOW) for all code references
        self.db.calculate_burden_categories()
        self.db.commit()

    def run(self):
        try:
            logger.info("Starting data load")
            if not self.db.data_load_in_progress():
                logger.info("Refreshing all data.")
                self.refresh_agencies()
                self.refresh_titles()
            else:
                logger.info(f"An existing data load process was interrupted. Resuming.")
            self.process_code_references()
        except Exception as e:
            logger.error(f"Error: {e}")
        finally:
            self.db.close()

    def temp_run(self):
        code_references = self.db.get_code_references_for_burden_score()
        for code_reference in code_references:
            xml = self.api.get_xml(
                code_reference["latest_issue_date"],
                code_reference["title_id"],
                code_reference["subtitle"],
                code_reference["chapter"],
                code_reference["subchapter"],
                code_reference["part"],
                code_reference["subpart"],
                code_reference["section"],
            )
            code_info = CodeInfo(code_reference, xml)
            print(code_info.calculate_burden_score())


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    start = time.time()
    loader = DataLoader(
        api_base_url="https://www.ecfr.gov", db_path="ecfr.db", cache_dir="xmlcache"
    )
    loader.run()
    end = time.time()
    logger.debug(f"Execution time: {end - start} seconds")

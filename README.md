# eCFR Analyzer

## Notes

MVP: word count and complexity by agency

eCFR API docs: https://www.ecfr.gov/developers/documentation/api/v1#/

Useful endpoints:

- `api/versioner/v1/titles.json` - retrieves titles and `latest_issue_date`
- `api/admin/v1/agencies.json` - ties subtitles and chapters to agencies
- `api/versioner/v1/versions/title-{title}.json` - retrieves full title structure

There are bulk exports available on govinfo.gov. They are delayed and the XML schema doesn't match what comes out of the eCFR API.

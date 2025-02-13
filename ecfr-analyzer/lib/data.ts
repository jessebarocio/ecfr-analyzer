import sqlite3 from "sqlite3";
import { open } from "sqlite";

async function initializeDatabase() {
  return await open({
    filename: "./ecfr.db",
    driver: sqlite3.Database,
  });
}

export async function getAgencies(): Promise<Agency[]> {
  const db = await initializeDatabase();
  const agencies = await db.all<Agency[]>("SELECT * FROM agencies");

  return agencies;
}

export async function getAgency(id: string): Promise<Agency | undefined> {
  const db = await initializeDatabase();
  const agency = await db.get<Agency>("SELECT * FROM agencies WHERE id = ?", id);
  return agency;
}

export async function getAgencyCodeReferences(id: string): Promise<AgencyCodeReference[]> {
  const db = await initializeDatabase();
  const references = await db.all<AgencyCodeReference[]>("SELECT * FROM code_references WHERE agency_id = ?", id);
  return references;
}

export async function getRelatedAgencies(id: string): Promise<Agency[]> {
  const db = await initializeDatabase();
  const agencies = await db.all<Agency[]>(
    "SELECT * FROM agencies WHERE id IN (SELECT parent_id FROM agencies WHERE id = ? UNION ALL SELECT id FROM agencies WHERE parent_id = ?)", id, id);
  return agencies;
}

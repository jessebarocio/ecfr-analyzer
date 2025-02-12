import { getAgencies } from "@/lib/data";
import Link from "next/link";

export default async function HomePage() {
  const agencies = await getAgencies();

  return <div>
    <ol>
      {agencies.map((agency, idx) => {
        return (<li key={agency.id}>
          <Link href={`/agency/${agency.id}`}>{agency.name}</Link>
          {agency.children.length > 0 && (
            <ol>
              {agency.children.map((child) => (
                <li key={child.id}><Link href={`/agency/${child.id}`}>{child.name}</Link></li>
              ))}
            </ol>
          )}
        </li>);
      })}
    </ol>
  </div>;
}

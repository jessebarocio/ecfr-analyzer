import { getAgencies } from "@/lib/data";
import SearchContainer from "./SearchContainer";

export default async function HomePage() {
  const agencies = await getAgencies();

  return (<SearchContainer initAgencies={agencies} />);
}

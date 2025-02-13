import AgencyCard from "./AgencyCard";
import { SimpleGrid } from "@mantine/core";

export default function AgencyList({ agencies }: { agencies: Agency[] }) {
  return (
    <SimpleGrid mt="md" cols={{ base: 1, md: 2, lg: 3 }}>
      {agencies.map((agency) => <AgencyCard key={agency.id} agency={agency} />)}
    </SimpleGrid>
  );
}

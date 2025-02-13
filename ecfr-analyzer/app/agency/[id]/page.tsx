import AgencyList from "@/app/AgencyList";
import CodeReferenceCard from "@/app/CodeReferenceCard";
import ComplianceBurden from "@/app/ComplianceBurden";
import WordCount from "@/app/WordCount";
import { getAgency, getAgencyCodeReferences, getRelatedAgencies } from "@/lib/data";
import { Badge, Button, Card, Divider, SimpleGrid, Text, Title } from "@mantine/core";
import Link from "next/link";

export default async function AgencyPage({ params }: { params: { id: string } }) {
  const agency = await getAgency((await params).id);
  const references = await getAgencyCodeReferences((await params).id);
  const relatedAgencies = await getRelatedAgencies((await params).id);

  return (<>
    <Link href="/">Back to Agency List</Link>
    {agency ?
      <AgencyDetails agency={agency} references={references} relatedAgencies={relatedAgencies} />
      : <Title order={2} my="md">Agency Not Found</Title>}
  </>);
}

function AgencyDetails({ agency, references, relatedAgencies }: { agency: Agency, references: AgencyCodeReference[], relatedAgencies: Agency[] }) {
  return (<>
    <Title order={2} my="md">{agency.name}</Title>
    <SimpleGrid cols={2} my="md">
      <Card withBorder shadow="sm" p="sm" radius="md">
        <WordCount wordCount={agency.total_word_count} />
      </Card>
      <Card withBorder shadow="sm" p="sm" radius="md">
        <ComplianceBurden burdenCategory={agency.burden_category} />
      </Card>
    </SimpleGrid>
    <Divider my="md" />
    <Title order={3} my="md">eCFR References</Title>
    <Text size="sm" my="md">This agency owns the following chapters/parts of the eCFR:</Text>

    <SimpleGrid cols={3} my="md">
      {references.map((reference) => <CodeReferenceCard key={reference.id} reference={reference} />)}
    </SimpleGrid>

    <Divider my="md" />
    <Title order={3} my="md">Related Agencies</Title>
    <Text size="sm" my="md">{(relatedAgencies.length > 0 && "This agency is related to the following agencies:") || "None."}</Text>
    <AgencyList agencies={relatedAgencies} />
  </>);
}

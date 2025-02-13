import { Badge, Card, Divider, Flex, Group, Text, Title } from "@mantine/core";
import Link from "next/link";
import WordCount from "./WordCount";
import ComplianceBurden from "./ComplianceBurden";

export default function AgencyCard({ agency }: { agency: Agency }) {
  return (
    <Card
      withBorder
      shadow="sm"
      p="sm"
      radius="md"
      component={Link}
      href={`/agency/${agency.id}`}>

      <Title order={3}>{agency.short_name || agency.name}</Title>
      {agency.short_name && <Text size="sm" mt="md">{agency.name}</Text>}
      <Divider mt="md" />
      <Group justify="space-between" mt="md">
        <Flex direction="column" align="center">
          <WordCount wordCount={agency.total_word_count} />
        </Flex>
        <Flex direction="column" align="center">
          <ComplianceBurden burdenCategory={agency.burden_category} />
        </Flex>
      </Group>
    </Card>
  );
}

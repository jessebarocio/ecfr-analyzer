import { Button, Card, Divider, Flex, Group, Text, Title } from "@mantine/core";
import Link from "next/link";
import WordCount from "./WordCount";
import ComplianceBurden from "./ComplianceBurden";

export default function CodeReferenceCard({ reference }: { reference: AgencyCodeReference }) {
  return (
    <Card 
      withBorder 
      shadow="sm" 
      p="sm" 
      radius="md">
      
      <Title order={3}>{reference.reference_text}</Title>
      <Text size="sm" mt="md">{reference.name}</Text>
      <Divider my="md" />
      <Group justify="space-between" mt="md">
        <Flex direction="column" align="center">
          <WordCount wordCount={reference.word_count} />
        </Flex>
        <Flex direction="column" align="center">
          <ComplianceBurden burdenCategory={reference.burden_category} />
        </Flex>
      </Group>
      <Button variant="light" color="blue" size="sm" mt="md" component={Link} href={reference.link} target="_blank">View in eCFR ⤴</Button>
    </Card>
  );
}

'use client';

import { Badge, Card, Divider, Flex, Group, Input, SegmentedControl, SimpleGrid, Text, Title } from "@mantine/core";
import Link from "next/link";
import { useState } from "react";

export default function SearchContainer({ initAgencies }: { initAgencies: Agency[] }) {
  const [agencies, setAgencies] = useState(initAgencies);
  const [filter, setFilter] = useState("");
  const sortValues = [
    {
      label: "Name ↑",
      value: "asc",
      sortFn: (a: Agency, b: Agency) => a.name.localeCompare(b.name),
    },
    {
      label: "Name ↓",
      value: "desc",
      sortFn: (a: Agency, b: Agency) => b.name.localeCompare(a.name),
    },
    {
      label: "Word Count ↓",
      value: "wcdesc",
      sortFn: (a: Agency, b: Agency) => b.total_word_count - a.total_word_count,
    },
    {
      label: "Word Count ↑",
      value: "wcasc",
      sortFn: (a: Agency, b: Agency) => a.total_word_count - b.total_word_count ,
    }
  ];
  const [sort, setSort] = useState(sortValues[0].value);

  const sortedAndFilteredAgencies = agencies
    .filter((agency) =>
      agency.name.toLowerCase().includes(filter.toLowerCase()) ||
      agency.short_name?.toLowerCase().includes(filter.toLowerCase()))
    .sort((a, b) => sortValues.find((s) => s.value === sort)?.sortFn(a, b) || 0);


  return (
    <>
      <Text mt="md" size="lg">Search for an agency and click on it to see more details.</Text>
      <Input size="lg" mt="md" radius="md" placeholder="Search agencies, e.g. FDA or Department of State"
        value={filter} onChange={(e) => setFilter(e.target.value)} />


      Sort: <SegmentedControl
        mt="md"
        radius="md"
        value={sort}
        onChange={(value) => setSort(value)}
        data={sortValues}
      />
      <AgencyList agencies={sortedAndFilteredAgencies} />
    </>
  );
}

function AgencyList({ agencies }: { agencies: Agency[] }) {
  return (
    <SimpleGrid mt="md" cols={{ base: 1, md: 2, lg: 3 }}>
      {agencies.map((agency) => <AgencyCard key={agency.id} agency={agency} />)}
    </SimpleGrid>
  );
}

function AgencyCard({ agency }: { agency: Agency }) {
  return (
    <Card
      withBorder
      shadow="sm"
      p="xl"
      radius="md"
      component={Link}
      href={`/agency/${agency.id}`}>

      <Title order={3}>{agency.short_name || agency.name}</Title>
      {agency.short_name && <Text size="sm" mt="md">{agency.name}</Text>}
      <Divider mt="md" />
      <Group justify="space-between" mt="md">
        <Flex direction="column" align="center">
          <Text size="lg" fw={500}><MetricValue value={agency.total_word_count} /></Text>
          <Text size="sm">Words</Text>
        </Flex>
        <Flex direction="column" align="center">
          <Badge color={agency.burden_category === "LOW" ? "green" : agency.burden_category === "MEDIUM" ? "yellow" : "red"} size="lg">{agency.burden_category || "N/A"}</Badge>
          <Text size="sm">Compliance Burden</Text>
        </Flex>
      </Group>
    </Card>
  );
}

function MetricValue({ value }: { value: number }) {
  const formatNumber = (num: number) => {
    if (num > 1000000) {
      return `${(num / 1000000).toFixed(1)}M`;
    } else if (num > 1000) {
      return `${(num / 1000).toFixed(1)}k`;
    } else {
      return num && num.toString() || "Unk";
    }
  }
  return (
    <span>{formatNumber(value)}</span>
  );
}

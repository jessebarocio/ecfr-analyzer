'use client';

import { Input, SegmentedControl, SimpleGrid, Text } from "@mantine/core";
import { useState } from "react";
import AgencyCard from "./AgencyCard";
import AgencyList from "./AgencyList";

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
      label: "Word Count ↑",
      value: "wcasc",
      sortFn: (a: Agency, b: Agency) => a.total_word_count - b.total_word_count ,
    },
    {
      label: "Word Count ↓",
      value: "wcdesc",
      sortFn: (a: Agency, b: Agency) => b.total_word_count - a.total_word_count,
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

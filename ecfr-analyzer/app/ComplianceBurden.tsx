'use client';
import { Badge, Flex, Popover, Text } from "@mantine/core";
import { useDisclosure } from "@mantine/hooks";

export default function ComplianceBurden({ burdenCategory }: { burdenCategory: string }) {
  const [opened, { close, open }] = useDisclosure(false);
  const color = burdenCategory === "LOW" ? "green" : burdenCategory === "MEDIUM" ? "yellow" : burdenCategory === "HIGH" ? "red" : "gray";

  return (
    <>
      <Popover opened={opened} position="bottom" withArrow width="target">
        <Popover.Target>
          <Flex direction="column" onMouseEnter={open} onMouseLeave={close}>
            <Badge color={color} size="lg" mb={2.8}>{burdenCategory || "N/A"}</Badge>
            <Text size="sm">Compliance Burden</Text>
          </Flex>
        </Popover.Target>
        <Popover.Dropdown>
          <Text size="sm">Compliance Burden is based on the analyzed complexity of the regulatory language.</Text>
        </Popover.Dropdown>
      </Popover>
    </>);
}

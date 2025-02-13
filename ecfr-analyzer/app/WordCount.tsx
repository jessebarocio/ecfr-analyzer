import { Text } from "@mantine/core";

export default function WordCount({ wordCount }: { wordCount: number }) {
  return (
    <>
      <Text size="lg" fw={500}><MetricValue value={wordCount} /></Text>
      <Text size="sm">Word Count</Text>
    </>);
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

import "@mantine/core/styles.css";
import React from "react";
import {
  MantineProvider,
  ColorSchemeScript,
  mantineHtmlProps,
  Container,
  Title,
} from "@mantine/core";
import { theme } from "../theme";

export const metadata = {
  title: "eCFR Statistics",
  description: "eCFR Statistics shows the word count and compliance burden of each agency that publishes regulations in the eCFR.",
};

export default function RootLayout({ children }: { children: any }) {
  return (
    <html lang="en" {...mantineHtmlProps}>
      <head>
        <ColorSchemeScript />
        <link rel="shortcut icon" href="/favicon.svg" />
        <meta
          name="viewport"
          content="minimum-scale=1, initial-scale=1, width=device-width, user-scalable=no"
        />
      </head>
      <body>
        <MantineProvider theme={theme}>
          <Container>
            <Title order={1} my="xl">eCFR Statistics</Title>
            {children}
          </Container>
        </MantineProvider>
      </body>
    </html>
  );
}

import React from "react";
import useBaseUrl from "@docusaurus/useBaseUrl";
import { useColorMode } from "@docusaurus/theme-common";

/**
 * <Figure>
 *
 *   <Figure src="/img/x.png" caption="..." />           // simple
 *   <Figure src="/img/x.png" darkSrc="/img/x-dark.png" alt="..." caption="..." />
 *   <Figure src="/img/screenshots/foo.png" alt="..." caption="..." todo="Capture from /studio/foo" />
 *
 * When `todo` is set we render a labelled placeholder instead of trying to
 * load the missing image — so a page can ship with the intended layout and
 * the team can grep `todo=` to find the asset capture queue.
 */
export default function Figure({ src, darkSrc, alt, caption, width, height, todo }) {
  const isDark = useColorMode().colorMode === "dark";
  const resolvedSrc = isDark && darkSrc ? darkSrc : src;
  const altText = alt || caption || "";

  if (todo) {
    // In production builds the placeholder is omitted entirely so the deployed
    // site never shows an unfinished asset. In development (`npm start`) the
    // placeholder renders so builders can see what still needs to be captured.
    if (process.env.NODE_ENV === "production") {
      return null;
    }
    return (
      <figure
        style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          width: "100%",
          margin: "1.5rem 0",
        }}
      >
        <div
          role="img"
          aria-label={altText}
          style={{
            width: "100%",
            minHeight: "180px",
            border: "2px dashed var(--ifm-color-emphasis-400, #cbd5e1)",
            borderRadius: "8px",
            background: "var(--ifm-color-emphasis-100, #f5f7fa)",
            padding: "1.5rem",
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
            gap: "0.5rem",
            color: "var(--ifm-color-emphasis-700, #475569)",
            fontFamily: "var(--ifm-font-family-base)",
          }}
        >
          <div style={{ fontSize: "0.75rem", letterSpacing: "0.08em", textTransform: "uppercase", fontWeight: 600 }}>
            Screenshot placeholder
          </div>
          <div style={{ textAlign: "center", maxWidth: "540px", fontSize: "0.95rem" }}>{altText}</div>
          <code
            style={{
              fontSize: "0.75rem",
              padding: "0.15rem 0.5rem",
              borderRadius: "4px",
              background: "var(--ifm-color-emphasis-200, #e2e8f0)",
            }}
          >
            todo: {todo}
          </code>
          <code
            style={{
              fontSize: "0.7rem",
              color: "var(--ifm-color-emphasis-600, #64748b)",
            }}
          >
            {resolvedSrc}
          </code>
        </div>
        {caption && (
          <figcaption
            style={{
              textAlign: "center",
              fontWeight: 300,
              marginTop: "0.5rem",
              fontSize: "0.9rem",
            }}
          >
            {caption}
          </figcaption>
        )}
      </figure>
    );
  }

  return (
    <figure style={{ display: "flex", flexDirection: "column", alignItems: "center", margin: "1.5rem 0" }}>
      <img
        src={useBaseUrl(resolvedSrc)}
        alt={altText}
        width={width || "auto"}
        height={height || "auto"}
        style={{ maxWidth: "100%", borderRadius: "6px" }}
      />
      {caption && (
        <figcaption
          style={{
            textAlign: "center",
            fontWeight: 300,
            marginTop: "0.5rem",
            fontSize: "0.9rem",
          }}
        >
          {caption}
        </figcaption>
      )}
    </figure>
  );
}

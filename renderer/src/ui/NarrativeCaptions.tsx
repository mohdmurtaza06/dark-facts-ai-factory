import React from "react";
import {interpolate} from "remotion";

const captions = [
  {start: 60, end: 210, text: "At 2:13 AM, the elevator opened by itself."},
  {start: 225, end: 390, text: "Nobody had pressed the button. Nobody was inside."},
  {start: 405, end: 570, text: "Then the display lit up: FLOOR ZERO."},
  {start: 585, end: 765, text: "The building only had twelve floors."},
  {start: 780, end: 990, text: "I stepped closer. The doors began to close."},
  {start: 1005, end: 1200, text: "A voice behind me whispered, “You forgot your badge.”"},
  {start: 1215, end: 1440, text: "I turned around. My reflection was still in the elevator."},
  {start: 1455, end: 1710, text: "It smiled first. I don't work there anymore."}
];

export const NarrativeCaptions: React.FC<{frame: number}> = ({frame}) => {
  const active = captions.find((c) => frame >= c.start && frame < c.end);
  if (!active) return null;
  const opacity = interpolate(frame, [active.start, active.start + 12, active.end - 12, active.end], [0, 1, 1, 0], {extrapolateLeft: "clamp", extrapolateRight: "clamp"});
  return (
    <div style={{position: "absolute", left: 70, right: 70, bottom: 115, display: "flex", justifyContent: "center", opacity, pointerEvents: "none"}}>
      <div style={{maxWidth: 920, padding: "18px 26px", borderRadius: 18, background: "rgba(4,7,13,0.78)", border: "1px solid rgba(220,230,245,0.16)", color: "#f5f2eb", fontSize: 39, fontWeight: 750, lineHeight: 1.18, textAlign: "center", textShadow: "0 3px 16px #000", fontFamily: "Arial, sans-serif"}}>
        {active.text}
      </div>
    </div>
  );
};

import React from "react";
import {interpolate} from "remotion";

const captions = [
  {start: 45, end: 255, text: "At 2:13 AM, the elevator opened by itself. I was the only person on night shift."},
  {start: 255, end: 465, text: "No button had been pressed. No footsteps. Just the soft little chime nobody wanted to hear."},
  {start: 465, end: 675, text: "The display blinked, went dark, then lit up again: FLOOR ZERO. Our building had twelve floors."},
  {start: 675, end: 885, text: "I checked the panel twice. Twelve buttons. Basement. Lobby. Floors one through ten. Absolutely no zero."},
  {start: 885, end: 1095, text: "The doors started closing. Then a voice behind me said, “You forgot your badge.”"},
  {start: 1095, end: 1305, text: "I turned around. Nobody there. When I looked back, the elevator was still waiting."},
  {start: 1305, end: 1530, text: "My reflection stood inside. Same uniform. Same tired face. Except it was smiling."},
  {start: 1530, end: 1760, text: "I quit that morning. HR asked why. I told them the elevator had hired my replacement."}
];

export const NarrativeCaptions: React.FC<{frame: number}> = ({frame}) => {
  const active = captions.find((c) => frame >= c.start && frame < c.end);
  if (!active) return null;
  const opacity = interpolate(frame, [active.start, active.start + 12, active.end - 12, active.end], [0, 1, 1, 0], {extrapolateLeft: "clamp", extrapolateRight: "clamp"});
  return (
    <div style={{position: "absolute", left: 58, right: 58, bottom: 105, display: "flex", justifyContent: "center", opacity, pointerEvents: "none"}}>
      <div style={{maxWidth: 950, padding: "20px 25px", borderRadius: 18, background: "rgba(4,7,13,0.82)", border: "1px solid rgba(220,230,245,0.16)", color: "#f5f2eb", fontSize: 34, fontWeight: 750, lineHeight: 1.2, textAlign: "center", textShadow: "0 3px 16px #000", fontFamily: "Arial, sans-serif"}}>
        {active.text}
      </div>
    </div>
  );
};

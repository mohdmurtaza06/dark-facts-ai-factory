import React from "react";
import {interpolate, useCurrentFrame} from "remotion";

export const TitleCard: React.FC<{frame: number}> = ({frame}) => {
  const show = interpolate(frame, [35, 75, 270, 315], [0, 1, 1, 0], {extrapolateLeft: "clamp", extrapolateRight: "clamp"});
  const reveal = interpolate(frame, [0, 50], [24, 0], {extrapolateRight: "clamp"});
  return (
    <div style={{position: "absolute", inset: 0, display: "flex", flexDirection: "column", justifyContent: "flex-end", padding: 88, paddingBottom: 230, opacity: show, transform: `translateY(${reveal}px)`, color: "#f4f0e8", fontFamily: "Arial, sans-serif", pointerEvents: "none"}}>
      <div style={{fontSize: 25, letterSpacing: 9, color: "#ff526e", fontWeight: 800}}>DARK FACTS</div>
      <div style={{fontSize: 78, lineHeight: 0.98, fontWeight: 900, textShadow: "0 8px 30px #000"}}>THE LAST<br/>ELEVATOR</div>
      <div style={{fontSize: 27, marginTop: 24, color: "#c4cad5", letterSpacing: 2}}>A NIGHT SHIFT THAT NEVER ENDED</div>
    </div>
  );
};

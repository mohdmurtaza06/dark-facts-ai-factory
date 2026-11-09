import React from "react";
import {interpolate} from "remotion";

export const TitleCard: React.FC<{frame: number}> = ({frame}) => {
  const show = interpolate(frame, [12, 42, 225, 270], [0, 1, 1, 0], {extrapolateLeft: "clamp", extrapolateRight: "clamp"});
  const reveal = interpolate(frame, [0, 45], [28, 0], {extrapolateRight: "clamp"});
  return (
    <div style={{position: "absolute", inset: 0, display: "flex", flexDirection: "column", justifyContent: "flex-end", padding: 88, paddingBottom: 330, opacity: show, transform: `translateY(${reveal}px)`, color: "#f4f0e8", fontFamily: "Arial, sans-serif", pointerEvents: "none"}}>
      <div style={{fontSize: 25, letterSpacing: 9, color: "#ff526e", fontWeight: 800}}>DARK FACTS ORIGINAL</div>
      <div style={{fontSize: 86, lineHeight: 0.94, fontWeight: 900, textShadow: "0 8px 30px #000"}}>THE LAST<br/>ELEVATOR</div>
      <div style={{fontSize: 26, marginTop: 24, color: "#c4cad5", letterSpacing: 2}}>SOME FLOORS SHOULD STAY LOST</div>
    </div>
  );
};

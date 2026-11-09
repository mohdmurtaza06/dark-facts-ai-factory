import React from "react";
import {AbsoluteFill, interpolate, useCurrentFrame} from "remotion";
import {ThreeCanvas} from "@remotion/three";
import {Environment} from "../world/Environment";
import {Detective} from "../characters/Detective";
import {TitleCard} from "../ui/TitleCard";

export const DarkMysteryPilot: React.FC = () => {
  const frame = useCurrentFrame();
  const fade = interpolate(frame, [0, 30, 1740, 1800], [0, 1, 1, 0], {extrapolateLeft: "clamp", extrapolateRight: "clamp"});
  const cameraZ = interpolate(frame, [0, 600, 1200, 1800], [13, 10, 8, 6]);
  return (
    <AbsoluteFill style={{backgroundColor: "#07090f", opacity: fade}}>
      <ThreeCanvas width={1080} height={1920} camera={{position: [0, 4, cameraZ], fov: 38}}>
        <Environment frame={frame}/>
        <Detective frame={frame}/>
      </ThreeCanvas>
      <TitleCard frame={frame}/>
    </AbsoluteFill>
  );
};

import React from "react";
import {AbsoluteFill, interpolate, useCurrentFrame} from "remotion";
import {ThreeCanvas} from "@remotion/three";
import {Environment} from "../world/Environment";
import {Detective} from "../characters/Detective";
import {Reflection} from "../characters/Reflection";
import {TitleCard} from "../ui/TitleCard";
import {NarrativeCaptions} from "../ui/NarrativeCaptions";
import {PilotAudio} from "../audio/PilotAudio";

export const DarkMysteryPilot: React.FC = () => {
  const frame = useCurrentFrame();
  const fade = interpolate(frame, [0, 24, 1770, 1800], [0, 1, 1, 0], {extrapolateLeft: "clamp", extrapolateRight: "clamp"});
  const cameraZ = interpolate(frame, [0, 360, 900, 1350, 1800], [13, 11, 8.5, 7.5, 6.5]);
  const cameraX = interpolate(frame, [0, 720, 1200, 1800], [0, 0, 0.7, 0]);
  return (
    <AbsoluteFill style={{backgroundColor: "#07090f", opacity: fade}}>
      <ThreeCanvas width={1080} height={1920} camera={{position: [cameraX, 3.4, cameraZ], fov: 38}}>
        <Environment frame={frame}/>
        <Detective frame={frame}/>
        <Reflection frame={frame}/>
      </ThreeCanvas>
      <TitleCard frame={frame}/>
      <NarrativeCaptions frame={frame}/>
      <PilotAudio/>
    </AbsoluteFill>
  );
};

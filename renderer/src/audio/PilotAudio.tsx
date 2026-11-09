import React from "react";
import {Audio, staticFile, useCurrentFrame, interpolate} from "remotion";

export const PilotAudio: React.FC = () => {
  const frame = useCurrentFrame();
  const voiceVolume = interpolate(frame, [0, 20, 1760, 1800], [0, 1, 1, 0], {extrapolateLeft: "clamp", extrapolateRight: "clamp"});
  const bedVolume = interpolate(frame, [0, 90, 1740, 1800], [0, 0.22, 0.22, 0], {extrapolateLeft: "clamp", extrapolateRight: "clamp"});
  return (
    <>
      <Audio src={staticFile("audio/pilot-voice.mp3")} volume={voiceVolume}/>
      <Audio src={staticFile("audio/pilot-ambience.mp3")} volume={bedVolume}/>
    </>
  );
};

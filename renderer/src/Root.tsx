import React from "react";
import {Composition} from "remotion";
import {DarkMysteryPilot} from "./scenes/DarkMysteryPilot";

export const Root: React.FC = () => (
  <Composition
    id="DarkMysteryPilot"
    component={DarkMysteryPilot}
    durationInFrames={1800}
    fps={30}
    width={1080}
    height={1920}
  />
);

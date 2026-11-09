import React from "react";
import {interpolate} from "remotion";

export const Reflection: React.FC<{frame: number}> = ({frame}) => {
  const reveal = interpolate(frame, [1320, 1440, 1560, 1680], [0, 1, 1, 0], {extrapolateLeft: "clamp", extrapolateRight: "clamp"});
  const smile = interpolate(frame, [1450, 1510, 1580], [0.025, 0.13, 0.13], {extrapolateLeft: "clamp", extrapolateRight: "clamp"});
  const headTilt = interpolate(frame, [1450, 1580], [0, -0.16], {extrapolateLeft: "clamp", extrapolateRight: "clamp"});
  return (
    <group position={[0, -0.25, -4.55]} rotation={[0, Math.PI, headTilt]} scale={[1, 1, 0.65]}>
      <mesh position={[0, 1.62, 0]} scale={[1, 1, 0.12]}>
        <sphereGeometry args={[0.36, 24, 18]}/>
        <meshBasicMaterial color="#05070c" transparent opacity={0.94 * reveal}/>
      </mesh>
      <mesh position={[0, 0.72, 0]} scale={[1, 1, 0.12]}>
        <capsuleGeometry args={[0.38, 0.9, 6, 12]}/>
        <meshBasicMaterial color="#05070c" transparent opacity={0.92 * reveal}/>
      </mesh>
      <mesh position={[0, 1.52, 0.045]} rotation={[0, 0, Math.PI]}>
        <torusGeometry args={[0.13, 0.018, 8, 24, Math.PI]}/>
        <meshBasicMaterial color="#d8d1c4" transparent opacity={reveal}/>
      </mesh>
      <mesh position={[0, 1.46, 0.05]} scale={[1, smile / 0.13, 1]}>
        <boxGeometry args={[0.23, 0.018, 0.015]}/>
        <meshBasicMaterial color="#d8d1c4" transparent opacity={reveal}/>
      </mesh>
      <mesh position={[-0.13, 1.68, 0.055]}>
        <sphereGeometry args={[0.035, 10, 10]}/>
        <meshBasicMaterial color="#ff405d" transparent opacity={reveal}/>
      </mesh>
      <mesh position={[0.13, 1.68, 0.055]}>
        <sphereGeometry args={[0.035, 10, 10]}/>
        <meshBasicMaterial color="#ff405d" transparent opacity={reveal}/>
      </mesh>
    </group>
  );
};

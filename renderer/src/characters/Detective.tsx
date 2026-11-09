import React from "react";
import {interpolate} from "remotion";

export const Detective: React.FC<{frame: number}> = ({frame}) => {
  const walk = Math.sin(frame / 7) * 0.12;
  const turn = interpolate(frame, [450, 510, 600, 660], [0, 0.75, 0.75, 0], {extrapolateLeft: "clamp", extrapolateRight: "clamp"});
  return (
    <group position={[0, -0.45, 2.1]} rotation={[0, turn, 0]}>
      <mesh position={[0, 0.72 + Math.abs(walk) * 0.2, 0]} castShadow>
        <capsuleGeometry args={[0.38, 0.9, 6, 12]}/>
        <meshStandardMaterial color="#202a3c" roughness={0.8}/>
      </mesh>
      <mesh position={[0, 1.55 + Math.abs(walk) * 0.2, 0]} castShadow>
        <sphereGeometry args={[0.38, 24, 18]}/>
        <meshStandardMaterial color="#d7a77f" roughness={0.68}/>
      </mesh>
      <mesh position={[0, 1.83 + Math.abs(walk) * 0.2, -0.03]} castShadow>
        <sphereGeometry args={[0.4, 24, 12, 0, Math.PI * 2, 0, Math.PI * 0.48]}/>
        <meshStandardMaterial color="#11151f" roughness={0.9}/>
      </mesh>
      <mesh position={[0, 1.43, 0.34]}>
        <boxGeometry args={[0.42, 0.09, 0.05]}/>
        <meshBasicMaterial color="#15131a"/>
      </mesh>
      <mesh position={[-0.18, 0.12 + walk, 0]} rotation={[walk, 0, 0]} castShadow>
        <capsuleGeometry args={[0.13, 0.62, 4, 8]}/>
        <meshStandardMaterial color="#111722"/>
      </mesh>
      <mesh position={[0.18, 0.12 - walk, 0]} rotation={[-walk, 0, 0]} castShadow>
        <capsuleGeometry args={[0.13, 0.62, 4, 8]}/>
        <meshStandardMaterial color="#111722"/>
      </mesh>
      <mesh position={[0.52, 0.78, 0.08]} rotation={[0, 0, -0.2 + walk]} castShadow>
        <capsuleGeometry args={[0.11, 0.62, 4, 8]}/>
        <meshStandardMaterial color="#202a3c"/>
      </mesh>
    </group>
  );
};

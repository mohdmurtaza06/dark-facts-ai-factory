import React from "react";
import {interpolate} from "remotion";

export const Detective: React.FC<{frame: number}> = ({frame}) => {
  const walk = Math.sin(frame / 7) * 0.13;
  const approach = interpolate(frame, [180, 420, 600, 780], [0, -0.85, -0.85, 0], {extrapolateLeft: "clamp", extrapolateRight: "clamp"});
  const recoil = interpolate(frame, [1110, 1140, 1200, 1260], [0, 0.32, 0.32, 0], {extrapolateLeft: "clamp", extrapolateRight: "clamp"});
  const turn = interpolate(frame, [900, 990, 1110, 1170], [0, 1.2, 1.2, 0], {extrapolateLeft: "clamp", extrapolateRight: "clamp"});
  const bob = Math.abs(walk) * 0.24;
  return (
    <group position={[0.25, -0.45, 2.2 + approach]} rotation={[0, turn, recoil]}>
      <mesh position={[0, 0.76 + bob, 0]} castShadow>
        <capsuleGeometry args={[0.39, 0.96, 7, 14]}/>
        <meshStandardMaterial color="#202b3d" roughness={0.82}/>
      </mesh>
      <mesh position={[0, 1.68 + bob, 0]} castShadow>
        <sphereGeometry args={[0.39, 28, 22]}/>
        <meshStandardMaterial color="#d5a47c" roughness={0.68}/>
      </mesh>
      <mesh position={[0, 1.96 + bob, -0.035]} castShadow>
        <sphereGeometry args={[0.41, 28, 14, 0, Math.PI * 2, 0, Math.PI * 0.49]}/>
        <meshStandardMaterial color="#11151f" roughness={0.9}/>
      </mesh>
      <mesh position={[0, 1.54 + bob, 0.35]}>
        <boxGeometry args={[0.45, frame > 1110 && frame < 1260 ? 0.13 : 0.07, 0.05]}/>
        <meshBasicMaterial color="#17131a"/>
      </mesh>
      <mesh position={[-0.2, 0.16 + walk, 0]} rotation={[walk, 0, 0]} castShadow>
        <capsuleGeometry args={[0.13, 0.66, 5, 9]}/>
        <meshStandardMaterial color="#101722"/>
      </mesh>
      <mesh position={[0.2, 0.16 - walk, 0]} rotation={[-walk, 0, 0]} castShadow>
        <capsuleGeometry args={[0.13, 0.66, 5, 9]}/>
        <meshStandardMaterial color="#101722"/>
      </mesh>
      <mesh position={[0.53, 0.85 + bob, 0.08]} rotation={[0, 0, -0.24 + walk]}>
        <capsuleGeometry args={[0.11, 0.68, 5, 9]}/>
        <meshStandardMaterial color="#202b3d"/>
      </mesh>
      <mesh position={[-0.5, 0.88 + bob, 0.08]} rotation={[0, 0, 0.22 - walk]}>
        <capsuleGeometry args={[0.11, 0.65, 5, 9]}/>
        <meshStandardMaterial color="#202b3d"/>
      </mesh>
      <mesh position={[0.53, 0.42, 0.2]} rotation={[0, 0, 0.3]}>
        <boxGeometry args={[0.22, 0.34, 0.18]}/>
        <meshStandardMaterial color="#d6b16e" metalness={0.5} roughness={0.3} emissive="#5b3b16" emissiveIntensity={0.4}/>
      </mesh>
    </group>
  );
};

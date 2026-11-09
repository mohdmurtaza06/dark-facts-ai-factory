import React from "react";
import * as THREE from "three";

export const Environment: React.FC<{frame: number}> = ({frame}) => {
  const pulse = 1 + Math.sin(frame / 17) * 0.08;
  return (
    <>
      <color attach="background" args={["#080b14"]}/>
      <fog attach="fog" args={["#080b14", 9, 30]}/>
      <ambientLight intensity={0.45}/>
      <spotLight position={[4, 9, 5]} intensity={150} angle={0.42} penumbra={0.8} color="#8ab6ff" castShadow/>
      <pointLight position={[-4, 3, -4]} intensity={38 * pulse} color="#ff365d" distance={16}/>
      <mesh rotation={[-Math.PI/2, 0, 0]} position={[0, -1.3, 0]} receiveShadow>
        <planeGeometry args={[30, 40]}/>
        <meshStandardMaterial color="#111827" roughness={0.92}/>
      </mesh>
      {Array.from({length: 9}, (_, i) => (
        <group key={i} position={[(i % 3 - 1) * 5.2, 0, -5 - Math.floor(i / 3) * 5]}>
          <mesh position={[0, 1.8, 0]} castShadow>
            <boxGeometry args={[3.2, 5.8 + (i % 2), 2.6]}/>
            <meshStandardMaterial color={i % 2 ? "#182235" : "#20283a"} roughness={0.86}/>
          </mesh>
          {Array.from({length: 6}, (_, w) => (
            <mesh key={w} position={[(w % 2 ? 0.65 : -0.65), 1.2 + Math.floor(w / 2) * 1.35, 1.32]}>
              <planeGeometry args={[0.34, 0.55]}/>
              <meshBasicMaterial color={(w + i) % 4 === 0 ? "#e5b86b" : "#26344c"}/>
            </mesh>
          ))}
        </group>
      ))}
      <mesh position={[0, 0.08, -3]} rotation={[-Math.PI/2, 0, 0]}>
        <circleGeometry args={[2.4, 48]}/>
        <meshBasicMaterial color="#24334b" transparent opacity={0.28}/>
      </mesh>
    </>
  );
};

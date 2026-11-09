import React from "react";
import {interpolate} from "remotion";

export const Environment: React.FC<{frame: number}> = ({frame}) => {
  const flicker = frame % 173 < 5 ? 0.18 : 1;
  const doorOpen = interpolate(frame, [390, 510, 720, 810, 1530, 1650], [0, 1, 1, 0, 0, 1], {extrapolateLeft: "clamp", extrapolateRight: "clamp"});
  const leftDoor = -0.78 - doorOpen * 0.72;
  const rightDoor = 0.78 + doorOpen * 0.72;
  return (
    <>
      <color attach="background" args={["#080b14"]}/>
      <fog attach="fog" args={["#080b14", 10, 34]}/>
      <ambientLight intensity={0.32}/>
      <spotLight position={[3, 8, 5]} intensity={125 * flicker} angle={0.38} penumbra={0.82} color="#9abfff" castShadow/>
      <pointLight position={[-3, 2.8, -1]} intensity={34 * flicker} color="#ff365d" distance={14}/>
      <pointLight position={[0, 2.6, -5]} intensity={28} color="#e4b56a" distance={9}/>
      <mesh rotation={[-Math.PI/2, 0, 0]} position={[0, -1.25, 0]} receiveShadow>
        <planeGeometry args={[22, 30]}/>
        <meshStandardMaterial color="#111722" roughness={0.94}/>
      </mesh>
      <mesh position={[0, 2.1, -5.1]}>
        <boxGeometry args={[4.3, 6.7, 0.34]}/>
        <meshStandardMaterial color="#202735" metalness={0.42} roughness={0.54}/>
      </mesh>
      <group position={[0, 0, -4.88]}>
        <mesh position={[leftDoor, 2.05, 0]} castShadow>
          <boxGeometry args={[1.48, 4.45, 0.16]}/>
          <meshStandardMaterial color="#394454" metalness={0.72} roughness={0.3}/>
        </mesh>
        <mesh position={[rightDoor, 2.05, 0]} castShadow>
          <boxGeometry args={[1.48, 4.45, 0.16]}/>
          <meshStandardMaterial color="#303b4b" metalness={0.72} roughness={0.3}/>
        </mesh>
        <mesh position={[0, 4.55, 0.1]}>
          <boxGeometry args={[1.25, 0.44, 0.08]}/>
          <meshBasicMaterial color="#120d14"/>
        </mesh>
        <mesh position={[0, 4.55, 0.16]}>
          <planeGeometry args={[0.82, 0.18]}/>
          <meshBasicMaterial color="#ff526e"/>
        </mesh>
        <mesh position={[0, 4.9, 0.08]}>
          <boxGeometry args={[0.72, 0.08, 0.08]}/>
          <meshBasicMaterial color="#d7b16d"/>
        </mesh>
      </group>
      {Array.from({length: 8}, (_, i) => (
        <group key={i} position={[(i % 2 ? 1 : -1) * 3.2, 0, -1.5 - i * 2.8]}>
          <mesh position={[0, 1.7, 0]} castShadow>
            <boxGeometry args={[1.2, 4.8, 1.1]}/>
            <meshStandardMaterial color="#151e2d" roughness={0.88}/>
          </mesh>
          <mesh position={[0, 1.9, 0.57]}>
            <planeGeometry args={[0.12, 0.5]}/>
            <meshBasicMaterial color={i % 3 === 0 ? "#c89d61" : "#25344b"}/>
          </mesh>
        </group>
      ))}
      <mesh position={[0, -1.17, -1.9]} rotation={[-Math.PI/2, 0, 0]}>
        <planeGeometry args={[3.6, 7.2]}/>
        <meshStandardMaterial color="#263044" roughness={0.7} metalness={0.2}/>
      </mesh>
    </>
  );
};

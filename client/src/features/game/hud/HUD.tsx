import { useEffect, useState } from 'react'

export function HUD({ timeLeft, hp, kills }: { timeLeft: number; hp: number; kills: number }) {
  const [mm, ss] = [Math.floor(timeLeft / 60), timeLeft % 60]
  return (
    <div style={{ position: 'absolute', top: 8, left: 8, color: '#fff' }}>
      <div>⏱ {mm}:{ss.toString().padStart(2, '0')}</div>
      <div>❤️ {hp}</div>
      <div>💀 {kills}</div>
    </div>
  )
}
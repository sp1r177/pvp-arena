import { useEffect, useRef, useState } from 'react'
import { Group, Header, Button } from '@vkontakte/vkui'
import { HUD } from './hud/HUD'
import { GameSocket } from '../../app/socket'
import { WS_URL } from '../../shared/config'

export function Arena({ mode, onExit }: { mode: 'ffa' | 'duo'; onExit: () => void }) {
  const canvasRef = useRef<HTMLCanvasElement | null>(null)
  const [state, setState] = useState<any>({ players: [], bullets: [], timeLeft: 0 })
  const socketRef = useRef<GameSocket | null>(null)
  const seqRef = useRef(0)

  useEffect(() => {
    const socket = new GameSocket(WS_URL)
    socket.connect()
    socket.onMessage((msg) => {
      if (msg.type === 'state') setState(msg)
    })
    socket.join(mode)
    socketRef.current = socket
    return () => socket.leave()
  }, [mode])

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return
    const ctx = canvas.getContext('2d')!
    let raf = 0

    const render = () => {
      ctx.fillStyle = '#0b1020'
      ctx.fillRect(0, 0, canvas.width, canvas.height)

      // players
      for (const p of state.players) {
        ctx.fillStyle = p.alive ? '#58a6ff' : '#444'
        ctx.beginPath()
        ctx.arc(p.x * 20, p.y * 20, 8, 0, Math.PI * 2)
        ctx.fill()
      }

      // bullets
      ctx.fillStyle = '#ff6b6b'
      for (const b of state.bullets) {
        ctx.beginPath()
        ctx.arc(b.x * 20, b.y * 20, 3, 0, Math.PI * 2)
        ctx.fill()
      }

      raf = requestAnimationFrame(render)
    }

    raf = requestAnimationFrame(render)
    return () => cancelAnimationFrame(raf)
  }, [state])

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      const move = { x: 0, y: 0 }
      if (e.type === 'keydown') {
        if (e.key === 'w') move.y = -1
        if (e.key === 's') move.y = 1
        if (e.key === 'a') move.x = -1
        if (e.key === 'd') move.x = 1
      }
      seqRef.current += 1
      socketRef.current?.sendInput(seqRef.current, 0.016, move, e.key === ' ')
    }
    window.addEventListener('keydown', onKey)
    window.addEventListener('keyup', onKey)
    return () => {
      window.removeEventListener('keydown', onKey)
      window.removeEventListener('keyup', onKey)
    }
  }, [])

  return (
    <Group header={<Header mode="primary">Арена</Header>}>
      <div style={{ position: 'relative' }}>
        <canvas ref={canvasRef} width={640} height={360} />
        <HUD timeLeft={state.timeLeft ?? 0} hp={100} kills={0} />
      </div>
      <Button style={{ marginTop: 12 }} onClick={onExit}>Ещё бой</Button>
    </Group>
  )
}
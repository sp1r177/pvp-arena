import { useState } from 'react'
import { Button, Group, Header, Spacing } from '@vkontakte/vkui'
import { MatchSearch } from '../features/lobby/MatchSearch'
import { Arena } from '../features/game/Arena'

export function AppRouter() {
  const [screen, setScreen] = useState<'lobby' | 'search' | 'arena'>('lobby')
  const [mode, setMode] = useState<'ffa' | 'duo'>('ffa')

  if (screen === 'search') return <MatchSearch mode={mode} onCancel={() => setScreen('lobby')} onFound={() => setScreen('arena')} />
  if (screen === 'arena') return <Arena mode={mode} onExit={() => setScreen('lobby')} />

  return (
    <Group header={<Header mode="secondary">Выбор режима</Header>}>
      <Button size="l" stretched onClick={() => { setMode('ffa'); setScreen('search') }}>FFA (8-12 игроков)</Button>
      <Spacing size={16} />
      <Button size="l" stretched mode="secondary" onClick={() => { setMode('duo'); setScreen('search') }}>1v1 / 2v2</Button>
    </Group>
  )
}
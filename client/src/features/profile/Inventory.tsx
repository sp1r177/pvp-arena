import { useEffect, useState } from 'react'
import { Group, Header, SimpleCell } from '@vkontakte/vkui'

export function Inventory() {
  const [items, setItems] = useState<Array<{ id: string; name: string; rarity: string }>>([])
  useEffect(() => {
    // TODO: fetch from API
    setItems([
      { id: 'skin_basic', name: 'Basic Suit', rarity: 'common' },
      { id: 'trail_red', name: 'Red Trail', rarity: 'rare' },
    ])
  }, [])

  return (
    <Group header={<Header mode="primary">Инвентарь</Header>}>
      {items.map((it) => (
        <SimpleCell key={it.id} subtitle={it.rarity}>{it.name}</SimpleCell>
      ))}
    </Group>
  )
}
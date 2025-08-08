import { useEffect } from 'react'
import { Group, Header, Spinner, Text, Button, Spacing } from '@vkontakte/vkui'

export function MatchSearch({ mode, onCancel, onFound }: { mode: 'ffa' | 'duo'; onCancel: () => void; onFound: () => void }) {
  useEffect(() => {
    const id = setTimeout(() => onFound(), 1500)
    return () => clearTimeout(id)
  }, [onFound])

  return (
    <Group header={<Header mode="primary">Поиск матча ({mode})</Header>}>
      <Spinner size="large" style={{ margin: 32 }} />
      <Text>Подбираем оппонентов... Если игроков мало, добавим ботов.</Text>
      <Spacing size={16} />
      <Button mode="secondary" onClick={onCancel}>Отмена</Button>
    </Group>
  )
}
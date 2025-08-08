import { useEffect } from 'react'
import { AppRoot, View, Panel, PanelHeader, SplitLayout, SplitCol } from '@vkontakte/vkui'
import '@vkontakte/vkui/dist/vkui.css'
import { initVK, getUserInfo } from './bridge'
import { AppRouter } from './router'

export function App() {
  useEffect(() => {
    initVK()
    getUserInfo()
  }, [])

  return (
    <AppRoot>
      <SplitLayout>
        <SplitCol>
          <View activePanel="main">
            <Panel id="main">
              <PanelHeader>VK PvP Arena</PanelHeader>
              <AppRouter />
            </Panel>
          </View>
        </SplitCol>
      </SplitLayout>
    </AppRoot>
  )
}
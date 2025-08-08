import bridge from 'vk-bridge'

export async function initVK() {
  try {
    await bridge.send('VKWebAppInit')
  } catch (e) {
    // ignore
  }
}

export async function getUserInfo() {
  try {
    const data = await bridge.send('VKWebAppGetUserInfo')
    return data
  } catch (e) {
    return null
  }
}
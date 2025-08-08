type Listener = (msg: any) => void

export class GameSocket {
  private ws?: WebSocket
  private listeners: Set<Listener> = new Set()

  constructor(private url: string) {}

  connect() {
    this.ws = new WebSocket(this.url)
    this.ws.onmessage = (ev) => {
      try {
        const msg = JSON.parse(ev.data)
        this.listeners.forEach((l) => l(msg))
      } catch {}
    }
  }

  onMessage(cb: Listener) {
    this.listeners.add(cb)
    return () => this.listeners.delete(cb)
  }

  join(mode: 'ffa' | 'duo', token?: string) {
    this.send({ type: 'join', mode, token })
  }

  sendInput(seq: number, dt: number, move: { x: number; y: number }, fire: boolean) {
    this.send({ type: 'input', seq, dt, move, fire })
  }

  leave() {
    this.send({ type: 'leave' })
  }

  private send(obj: any) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(obj))
    }
  }
}
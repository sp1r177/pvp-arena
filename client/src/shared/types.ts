export type ClientToServer =
  | { type: 'join'; mode: 'ffa' | 'duo'; token?: string }
  | { type: 'input'; seq: number; dt: number; move: { x: number; y: number }; fire: boolean }
  | { type: 'leave' }

export type ServerToClient =
  | { type: 'state'; t: number; youId?: string; players: any[]; bullets: any[]; powerups?: any[]; mapHash: string; timeLeft: number }
  | { type: 'event'; event: { type: 'hit' | 'kill' | 'powerup' | 'countdown' | 'finish'; payload: any } }
  | { type: 'ack'; seq: number }
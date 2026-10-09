import {SCENES, SceneManifestItem} from "./scene-manifest"

const scenesBySequence = new Map(SCENES.map(scene => [scene.sequence, scene]))

export function getScene(sequence: number): SceneManifestItem {
  const scene = scenesBySequence.get(sequence)
  if (!scene) throw new Error(`缺少 Q${String(sequence).padStart(2, "0")} 的场景配置`)
  return scene
}

export function validateScenes(): boolean {
  return SCENES.length === 24
    && SCENES.every((scene, index) => scene.sequence === index + 1)
}

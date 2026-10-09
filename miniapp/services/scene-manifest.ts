// Runtime copy of assets/questions/manifest.json.
// Keep this as a TypeScript module because the WeChat runtime does not bundle
// arbitrary JSON required from page code.
export interface SceneManifestItem {
  sequence: number
  sceneKey: string
  sceneAsset: string
  chapter: string
  motionPreset: string
  layout: string
}

export const SCENES: SceneManifestItem[] = [
  {sequence: 1, sceneKey: "unexpected_afternoon", sceneAsset: "/assets/questions/q01/scene.jpg", chapter: "靠近的方式", motionPreset: "lake-breeze", layout: "left-right-staggered"},
  {sequence: 2, sceneKey: "tree_hollow_reply", sceneAsset: "/assets/questions/q02/scene.jpg", chapter: "靠近的方式", motionPreset: "letter-and-light", layout: "right-left-staggered"},
  {sequence: 3, sceneKey: "glowing_shell", sceneAsset: "/assets/questions/q03/scene.jpg", chapter: "靠近的方式", motionPreset: "gentle-ripples", layout: "left-right-staggered"},
  {sequence: 4, sceneKey: "forest_festival", sceneAsset: "/assets/questions/q04/scene.jpg", chapter: "靠近的方式", motionPreset: "lantern-breath", layout: "right-left-staggered"},
  {sequence: 5, sceneKey: "valley_lights", sceneAsset: "/assets/questions/q05/scene.jpg", chapter: "靠近的方式", motionPreset: "mist-and-lights", layout: "left-right-staggered"},
  {sequence: 6, sceneKey: "treehouse_day", sceneAsset: "/assets/questions/q06/scene.jpg", chapter: "靠近的方式", motionPreset: "window-and-leaves", layout: "right-left-staggered"},
  {sequence: 7, sceneKey: "rain_broken_path", sceneAsset: "/assets/questions/q07/scene.jpg", chapter: "情绪被看见", motionPreset: "path-pawprints", layout: "left-right-staggered"},
  {sequence: 8, sceneKey: "home_in_rain", sceneAsset: "/assets/questions/q08/scene.jpg", chapter: "情绪被看见", motionPreset: "rain-and-steam", layout: "right-left-staggered"},
  {sequence: 9, sceneKey: "reeds_nothing", sceneAsset: "/assets/questions/q09/scene.jpg", chapter: "情绪被看见", motionPreset: "mist-and-water", layout: "left-right-staggered"},
  {sequence: 10, sceneKey: "under_the_leaf", sceneAsset: "/assets/questions/q10/scene.jpg", chapter: "情绪被看见", motionPreset: "soft-wind", layout: "right-left-staggered"},
  {sequence: 11, sceneKey: "sinking_feather", sceneAsset: "/assets/questions/q11/scene.jpg", chapter: "情绪被看见", motionPreset: "feather-ripple", layout: "left-right-staggered"},
  {sequence: 12, sceneKey: "one_night_light", sceneAsset: "/assets/questions/q12/scene.jpg", chapter: "情绪被看见", motionPreset: "camp-light", layout: "right-left-staggered"},
  {sequence: 13, sceneKey: "swaying_bridge", sceneAsset: "/assets/questions/q13/scene.jpg", chapter: "分歧与修复", motionPreset: "bridge-settle", layout: "left-right-staggered"},
  {sequence: 14, sceneKey: "upside_down_map", sceneAsset: "/assets/questions/q14/scene.jpg", chapter: "分歧与修复", motionPreset: "map-turn", layout: "right-left-staggered"},
  {sequence: 15, sceneKey: "stepping_stones", sceneAsset: "/assets/questions/q15/scene.jpg", chapter: "分歧与修复", motionPreset: "water-settle", layout: "left-right-staggered"},
  {sequence: 16, sceneKey: "leaking_dam", sceneAsset: "/assets/questions/q16/scene.jpg", chapter: "分歧与修复", motionPreset: "stream-settle", layout: "right-left-staggered"},
  {sequence: 17, sceneKey: "fire_between_us", sceneAsset: "/assets/questions/q17/scene.jpg", chapter: "分歧与修复", motionPreset: "fire-breath", layout: "left-right-staggered"},
  {sequence: 18, sceneKey: "boat_returns", sceneAsset: "/assets/questions/q18/scene.jpg", chapter: "分歧与修复", motionPreset: "rope-and-ripples", layout: "right-left-staggered"},
  {sequence: 19, sceneKey: "two_weekend_paths", sceneAsset: "/assets/questions/q19/scene.jpg", chapter: "一起生活", motionPreset: "cloud-and-water", layout: "left-right-staggered"},
  {sequence: 20, sceneKey: "snow_station_map", sceneAsset: "/assets/questions/q20/scene.jpg", chapter: "一起生活", motionPreset: "map-and-snow", layout: "right-left-staggered"},
  {sequence: 21, sceneKey: "moon_lake_stones", sceneAsset: "/assets/questions/q21/scene.jpg", chapter: "一起生活", motionPreset: "stone-glow", layout: "left-right-staggered"},
  {sequence: 22, sceneKey: "treehouse_and_stream", sceneAsset: "/assets/questions/q22/scene.jpg", chapter: "一起生活", motionPreset: "page-and-water", layout: "right-left-staggered"},
  {sequence: 23, sceneKey: "four_things_table", sceneAsset: "/assets/questions/q23/scene.jpg", chapter: "一起生活", motionPreset: "map-and-stones", layout: "left-right-staggered"},
  {sequence: 24, sceneKey: "last_moonlit_path", sceneAsset: "/assets/questions/q24/scene.jpg", chapter: "一起生活", motionPreset: "final-pawprints", layout: "right-left-staggered"},
]

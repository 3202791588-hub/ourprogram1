import {getFull} from "../../services/results"
import {rewardedAd} from "../../services/ad"
import {track} from "../../services/analytics"

Page({
  data: {
    id: 0,
    loading: true,
    locked: false,
    error: "",
    result: null as any,
    scores: [] as any[],
    navTop: 50,
  },

  onLoad(options: Record<string, string>) {
    const windowInfo = wx.getWindowInfo()
    this.setData({
      id: Number(options.id),
      navTop: (windowInfo.statusBarHeight || 44) + 8,
    })
    this.load()
  },

  back() {
    wx.navigateBack({delta: 1})
  },

  async load() {
    this.setData({loading: true, error: ""})
    try {
      const result = await getFull(this.data.id)
      const labels: Record<string, string> = {
        social_energy: "靠近的主动度",
        sensitivity: "情绪感知力",
        exploration: "共同探索欲",
      }
      const scores = Object.entries(result.dimension_scores || {}).map(([key, value]) => ({
        key,
        label: labels[key] || key,
        value: Number(value),
      }))
      this.setData({result, scores, loading: false, locked: false, error: ""})
      track("full_result_view", {result_id: this.data.id})
    } catch (error: any) {
      if (error.status === 403) this.setData({locked: true, loading: false, error: ""})
      else this.setData({error: error.message, loading: false})
    }
  },

  async unlock() {
    this.setData({loading: true})
    try {
      track("unlock_click", {result_id: this.data.id})
      await rewardedAd.unlockResult(this.data.id)
      await this.load()
    } catch (error: any) {
      this.setData({error: error.message, loading: false})
    }
  },
})

import {getPreview} from "../../services/results"
import {createInvite} from "../../services/relations"
import {track} from "../../services/analytics"

const RESULT_DECOR: Record<string, {animal: string; glyph: string; tone: string; caption: string}> = {
  night_cat: {animal: "夜行猫", glyph: "☾", tone: "night-cat", caption: "先听见风，再决定向哪里靠近"},
  golden_retriever: {animal: "金毛", glyph: "☀", tone: "golden-retriever", caption: "愿意把温暖变成看得见的行动"},
  fox: {animal: "狐狸", glyph: "✦", tone: "fox", caption: "总能从熟悉的路旁发现新入口"},
}

const SCORE_LABELS: Record<string, {label: string; hint: string}> = {
  social_energy: {label: "靠近的主动度", hint: "你如何发出连接信号"},
  sensitivity: {label: "情绪感知力", hint: "你如何看见细小变化"},
  exploration: {label: "共同探索欲", hint: "你如何面对关系中的未知"},
}

Page({
  data: {
    id: 0,
    loading: true,
    error: "",
    result: null as any,
    invite: "",
    scores: [] as any[],
    decor: RESULT_DECOR.fox,
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

  async load() {
    this.setData({loading: true, error: ""})
    try {
      const result = await getPreview(this.data.id)
      const scores = Object.entries(result.dimension_scores || {}).map(([key, value]) => ({
        key,
        label: SCORE_LABELS[key]?.label || key,
        hint: SCORE_LABELS[key]?.hint || "",
        value: Number(value),
      }))
      this.setData({
        result,
        scores,
        decor: RESULT_DECOR[result.result_type] || RESULT_DECOR.fox,
        loading: false,
        error: "",
      })
      track("result_preview", {result_id: this.data.id})
    } catch (error: any) {
      this.setData({error: error.message, loading: false})
    }
  },

  home() {
    wx.reLaunch({url: "/pages/home/index"})
  },

  full() {
    wx.navigateTo({url: `/pages/full-result/index?id=${this.data.id}`})
  },

  async inviteFriend() {
    try {
      const response = await createInvite(this.data.id)
      this.setData({invite: response.invite_code})
      track("invite_create", {result_id: this.data.id})
      wx.setClipboardData({
        data: response.invite_code,
        success: () => wx.showToast({title: "邀请口令已复制", icon: "success"}),
      })
    } catch (error: any) {
      this.setData({error: error.message})
    }
  },

  onShareAppMessage() {
    track("result_share", {result_id: this.data.id})
    return {
      title: `我在月森遇见了${this.data.decor.animal}，你呢？`,
      // Result previews are private. Sharing leads friends to the journey
      // entrance; the dedicated invitation flow carries relationship state.
      path: `/pages/home/index?from=result&type=${this.data.result?.result_type || ""}`,
    }
  },
})

import {mockLogin} from "../../services/auth"
import {restoreAuth, getMockUser} from "../../store/auth"
import {track} from "../../services/analytics"

Page({
  data: {
    loading: true,
    error: "",
    user: "user_a" as "user_a" | "user_b",
    navTop: 50,
  },

  async onLoad() {
    restoreAuth()
    const windowInfo = wx.getWindowInfo()
    this.setData({navTop: (windowInfo.statusBarHeight || 44) + 8})
    await this.login(getMockUser() as "user_a" | "user_b")
    track("home_view")
  },

  async login(user: "user_a" | "user_b") {
    this.setData({loading: true, error: "", user})
    try {
      await mockLogin(user)
      this.setData({loading: false})
    } catch (error: any) {
      this.setData({loading: false, error: error.message})
    }
  },

  retry() {
    this.login(this.data.user)
  },

  switchUser(event: WechatMiniprogram.TouchEvent) {
    this.login(event.currentTarget.dataset.user)
  },

  start() {
    wx.navigateTo({url: "/pages/test-detail/index"})
  },

  history() {
    wx.navigateTo({url: "/pages/history/index"})
  },
})

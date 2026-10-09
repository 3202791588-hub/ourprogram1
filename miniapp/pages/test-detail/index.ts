import {getTest, createSession} from "../../services/tests"
import {track} from "../../services/analytics"

Page({
  data: {
    loading: true,
    error: "",
    test: null as any,
    navTop: 50,
  },

  onLoad() {
    const windowInfo = wx.getWindowInfo()
    this.setData({navTop: (windowInfo.statusBarHeight || 44) + 8})
    this.load()
  },

  async load() {
    try {
      const test = await getTest()
      this.setData({test, loading: false, error: ""})
      track("test_view", {test_slug: test.slug})
    } catch (error: any) {
      this.setData({error: error.message, loading: false})
    }
  },

  back() {
    wx.navigateBack()
  },

  async start() {
    this.setData({loading: true})
    try {
      const session = await createSession()
      track("test_start", {}, session.id)
      wx.redirectTo({url: `/pages/test-run/index?id=${session.id}`})
    } catch (error: any) {
      this.setData({error: error.message, loading: false})
    }
  },
})

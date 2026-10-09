import {getSession, getTest, saveAnswer, submitSession} from "../../services/tests"
import {track} from "../../services/analytics"
import {getScene, validateScenes} from "../../services/scenes"
import {Question} from "../../types/index"

const SELECTION_ANIMATION_MS = 320
const ENTER_ANIMATION_MS = 260

let tapLocked = false
let pendingSave: Promise<unknown> | null = null

function wait(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms))
}

function decorateQuestion(question: Question) {
  const fallback = getScene(question.sequence)
  return {
    ...question,
    displayTitle: question.metadata?.title || `月森的第 ${question.sequence} 段路`,
    // The API still carries the former WebP path. Runtime assets are client-owned
    // so a frontend-only compatibility release can use JPEG without redeploying it.
    sceneAsset: fallback.sceneAsset,
    chapter: question.metadata?.chapter || fallback.chapter,
    motionPreset: question.metadata?.motion_preset || fallback.motionPreset,
    layout: question.metadata?.layout || fallback.layout,
  }
}

Page({
  data: {
    loading: true,
    saving: false,
    submitting: false,
    completing: false,
    entering: false,
    sceneFailed: false,
    error: "",
    sessionId: 0,
    questions: [] as any[],
    currentQuestion: null as any,
    sceneAsset: "",
    nextSceneAsset: "",
    index: 0,
    answers: {} as Record<number, number>,
    answeredCount: 0,
    navTop: 52,
    assetPackProbe: false,
  },

  onLoad(options: Record<string, string>) {
    tapLocked = false
    pendingSave = null
    const windowInfo = wx.getWindowInfo()
    this.setData({
      sessionId: Number(options.id),
      navTop: (windowInfo.statusBarHeight || 44) + 6,
    })
    this.load()
  },

  back() {
    wx.navigateBack({delta: 1})
  },

  setCurrentQuestion(index: number, extra: Record<string, unknown> = {}) {
    const currentQuestion = this.data.questions[index]
    const nextQuestion = this.data.questions[index + 1]
    this.setData({
      index,
      currentQuestion,
      sceneAsset: currentQuestion?.sceneAsset || "",
      nextSceneAsset: nextQuestion?.sceneAsset || "",
      sceneFailed: false,
      entering: true,
      ...extra,
    })
    setTimeout(() => this.setData({entering: false}), ENTER_ANIMATION_MS)
  },

  sceneLoaded() {
    if (this.data.sceneFailed) this.setData({sceneFailed: false})
  },

  sceneError() {
    this.setData({sceneFailed: true})
  },

  async load() {
    tapLocked = false
    pendingSave = null
    this.setData({loading: true, saving: false, submitting: false, completing: false})
    try {
      if (!validateScenes()) throw new Error("题目场景配置不完整")
      const [test, session] = await Promise.all([
        getTest(),
        getSession(this.data.sessionId),
      ])
      const questions = (session.questions?.length
        ? session.questions
        : test.current_version.questions).map(decorateQuestion)
      const answers = Object.fromEntries(
        session.answers.map(answer => [answer.question_id, answer.option_id]),
      ) as Record<number, number>
      const answeredCount = questions.filter(question => answers[question.id] !== undefined).length
      const index = Math.min(Math.max(0, session.current_question - 1), Math.max(0, questions.length - 1))
      this.setData({
        questions,
        answers,
        answeredCount,
        loading: false,
        error: "",
      }, () => this.setCurrentQuestion(index))
    } catch (error: any) {
      this.setData({error: error.message, loading: false})
    }
  },

  async choose(event: WechatMiniprogram.TouchEvent) {
    if (tapLocked || this.data.saving || this.data.submitting) return

    const questionId = Number(event.currentTarget.dataset.questionId)
    const optionId = Number(event.currentTarget.dataset.optionId)
    const currentQuestion = this.data.currentQuestion

    // A fast tap can arrive from the previous question while the native view is
    // still rendering the next one. Ignore that stale event instead of pairing
    // an old option with the new question.
    if (!currentQuestion || currentQuestion.id !== questionId) return
    if (!currentQuestion.options.some((option: any) => option.id === optionId)) return

    tapLocked = true
    const questionIndex = this.data.index
    const previousOptionId = this.data.answers[questionId]
    const optimisticAnswers = {...this.data.answers, [questionId]: optionId}

    this.setData({
      answers: optimisticAnswers,
      saving: true,
      completing: true,
      error: "",
    })

    const saveRequest = saveAnswer(this.data.sessionId, questionId, optionId)
    pendingSave = saveRequest

    try {
      await Promise.all([saveRequest, wait(SELECTION_ANIMATION_MS)])
      const answeredCount = this.data.questions.filter(
        (question: any) => optimisticAnswers[question.id] !== undefined,
      ).length

      await new Promise<void>(resolve => this.setData({answeredCount, saving: false}, resolve))
      track("question_answer", {question_id: questionId}, this.data.sessionId)

      if (answeredCount === this.data.questions.length) {
        // Completing the final missing answer anywhere in the journey is enough
        // to generate the result. This also repairs older sessions with a gap.
        await wait(360)
        await new Promise<void>(resolve => this.setData({completing: false}, resolve))
        await this.submit()
      } else if (questionIndex < this.data.questions.length - 1) {
        this.setCurrentQuestion(questionIndex + 1, {completing: false})
      } else {
        // An older interrupted session can reach Q24 while an earlier answer is
        // missing. Bring the user to the first gap instead of leaving a disabled
        // result button with no explanation.
        const missingIndex = this.data.questions.findIndex(
          (question: any) => optimisticAnswers[question.id] === undefined,
        )
        this.setCurrentQuestion(Math.max(0, missingIndex), {completing: false})
        wx.showToast({
          title: `还差 ${this.data.questions.length - answeredCount} 段路，已带你回到漏题`,
          icon: "none",
          duration: 2600,
        })
      }
    } catch (error: any) {
      const revertedAnswers = {...this.data.answers}
      if (previousOptionId === undefined) delete revertedAnswers[questionId]
      else revertedAnswers[questionId] = previousOptionId
      this.setData({
        answers: revertedAnswers,
        saving: false,
        completing: false,
        error: error.message,
      })
    } finally {
      if (pendingSave === saveRequest) pendingSave = null
      tapLocked = false
    }
  },

  prev() {
    if (tapLocked || this.data.saving || this.data.submitting) return
    if (this.data.index > 0) this.setCurrentQuestion(this.data.index - 1, {completing: false})
  },

  async submit() {
    if (this.data.submitting) return
    if (pendingSave) {
      try {
        await pendingSave
      } catch (_) {
        return
      }
    }

    this.setData({submitting: true, error: ""})
    try {
      // The server is the source of truth. This also closes the last-answer
      // race when the user taps submit immediately after selecting an option.
      const session = await getSession(this.data.sessionId)
      const serverAnswers = Object.fromEntries(
        session.answers.map(answer => [answer.question_id, answer.option_id]),
      ) as Record<number, number>
      const answeredCount = this.data.questions.filter(
        (question: any) => serverAnswers[question.id] !== undefined,
      ).length

      this.setData({answers: serverAnswers, answeredCount})
      if (answeredCount !== this.data.questions.length) {
        this.setData({submitting: false})
        wx.showToast({title: `还有 ${this.data.questions.length - answeredCount} 题未完成`, icon: "none"})
        return
      }

      const result = await submitSession(this.data.sessionId)
      track("test_submit", {}, this.data.sessionId)
      wx.redirectTo({
        url: result.relationship_id
          ? `/pages/relation/index?id=${result.relationship_id}`
          : `/pages/result/index?id=${result.result_id}`,
      })
    } catch (error: any) {
      this.setData({submitting: false, error: error.message})
    }
  },
})

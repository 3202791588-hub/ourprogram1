const API = "/api/v1";
const app = document.querySelector("#app");
const state = {
  token: localStorage.getItem("web_token") || "",
  user: localStorage.getItem("web_user") || "user_a",
  test: null,
  session: null,
  questions: [],
  answers: {},
  questionIndex: 0,
  result: null,
  invite: null,
};

const labels = {
  social_energy: "社交能量",
  sensitivity: "感受敏锐度",
  exploration: "探索倾向",
  emotion: "情绪默契",
  communication: "沟通节奏",
  pace: "行动节奏",
  exploration_relation: "新鲜感匹配",
};

async function api(path, method = "GET", data) {
  const response = await fetch(API + path, {
    method,
    headers: { "Content-Type": "application/json", ...(state.token ? { Authorization: `Bearer ${state.token}` } : {}) },
    body: data === undefined ? undefined : JSON.stringify(data),
  });
  let body;
  try { body = await response.json(); } catch { throw new Error("服务返回了无法识别的内容"); }
  if (!response.ok) throw Object.assign(new Error(typeof body.message === "string" ? body.message : "请求失败"), { status: response.status });
  return body.data;
}

function toast(message) {
  const element = document.querySelector("#toast");
  element.textContent = message;
  element.classList.add("show");
  setTimeout(() => element.classList.remove("show"), 2200);
}

function setLoading(text = "正在连接 Demo 服务…") {
  app.innerHTML = `<div class="loading"><div class="spinner"></div>${text}</div>`;
}

function setError(error, retry = "home") {
  app.innerHTML = `<div class="panel error"><h2>没有顺利加载</h2><p>${escapeHtml(error.message || String(error))}</p><button class="primary" data-action="${retry}">重试</button></div>`;
}

function escapeHtml(value = "") {
  return String(value).replace(/[&<>'"]/g, char => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#39;", '"': "&quot;" }[char]));
}

async function login(user = state.user, render = true) {
  if (render) setLoading(`正在切换到${user === "user_a" ? "用户 A" : "用户 B"}…`);
  const data = await api("/auth/wechat", "POST", { mock_user: user });
  state.token = data.access_token;
  state.user = user;
  localStorage.setItem("web_token", state.token);
  localStorage.setItem("web_user", user);
  updateUserSwitch();
  if (render) home();
}

function updateUserSwitch() {
  document.querySelectorAll("[data-user]").forEach(button => button.classList.toggle("active", button.dataset.user === state.user));
}

async function ensureLogin() {
  try {
    if (state.token) { await api("/me"); updateUserSwitch(); return; }
  } catch { state.token = ""; }
  await login(state.user, false);
}

function home() {
  app.innerHTML = `
    <section class="hero">
      <div>
        <span class="eyebrow">Hidden Personality Test</span>
        <h1>遇见那个<br>藏在日常里的<em>你</em></h1>
        <p class="lead">24 个轻松的生活选择，生成一份可分享的人格侧写。邀请好友完成同一套测试，还能解锁你们独有的关系互动报告。</p>
        <div class="cta-row">
          <button class="primary" data-action="detail">开始探索 <span aria-hidden="true">→</span></button>
          <button class="ghost" data-action="history">查看历史记录</button>
        </div>
        <div class="feature-row"><span><i></i>约 3 分钟</span><span><i></i>自动保存进度</span><span><i></i>娱乐探索，非诊断</span></div>
      </div>
      <div class="hero-art" aria-hidden="true">
        <div class="orbit"></div>
        <div class="persona-card"><span class="card-number">PERSONA / 01</span><div class="animal-glyph">☾</div><h3>夜行猫型观察者</h3><p>先读懂环境，再决定如何靠近。</p></div>
      </div>
    </section>`;
  updateUserSwitch();
  track("home_view");
}

async function detail() {
  setLoading("正在准备测试…");
  try {
    state.test = await api("/tests/hidden-personality");
    const version = state.test.current_version;
    app.innerHTML = `<section class="panel">
      <span class="eyebrow">Test No. 01</span>
      <h2>${escapeHtml(state.test.name)}</h2>
      <p class="muted">${escapeHtml(state.test.description)}</p>
      <div class="score-grid">
        <div class="score-item"><strong>${version.question_count}</strong><small>道生活情境题</small></div>
        <div class="score-item"><strong>3</strong><small>分钟左右完成</small></div>
        <div class="score-item"><strong>3</strong><small>种 Demo 人格</small></div>
      </div>
      <p class="muted">当前结果由稳定的 Mock Engine 生成，用于验证产品体验，不代表科学人格测量。</p>
      <div class="cta-row"><button class="primary" data-action="start-test">开始答题</button><button class="ghost" data-action="home">返回</button></div>
    </section>`;
    track("test_view", { test_slug: state.test.slug });
  } catch (error) { setError(error, "detail"); }
}

async function startTest(inviteId) {
  setLoading("正在创建答题进度…");
  try {
    if (!state.test) state.test = await api("/tests/hidden-personality");
    const payload = { test_slug: "hidden-personality", ...(inviteId ? { relation_invite_id: Number(inviteId) } : {}) };
    state.session = await api("/test-sessions", "POST", payload);
    state.questions = state.test.current_version.questions;
    state.answers = Object.fromEntries(state.session.answers.map(answer => [answer.question_id, answer.option_id]));
    state.questionIndex = Math.max(0, Math.min(state.questions.length - 1, state.session.current_question - 1));
    renderQuestion();
    track("test_start", {}, state.session.id);
  } catch (error) { setError(error, "detail"); }
}

function renderQuestion() {
  const question = state.questions[state.questionIndex];
  const selected = state.answers[question.id];
  const done = Object.keys(state.answers).length;
  app.innerHTML = `<section class="panel wide">
    <div class="quiz-meta"><span>隐藏人格测试</span><span>已保存 ${done} / ${state.questions.length}</span></div>
    <div class="progress"><span style="width:${((state.questionIndex + 1) / state.questions.length) * 100}%"></span></div>
    <span class="eyebrow">Question ${String(state.questionIndex + 1).padStart(2, "0")}</span>
    <h2 class="question">${escapeHtml(question.content)}</h2>
    <div class="options">${question.options.map(option => `<button class="option ${selected === option.id ? "selected" : ""}" data-option="${option.id}"><b>${option.label}</b><span>${escapeHtml(option.content)}</span></button>`).join("")}</div>
    <div class="quiz-nav"><button class="ghost" data-action="prev-question" ${state.questionIndex === 0 ? "disabled" : ""}>上一题</button>${state.questionIndex === state.questions.length - 1 ? `<button class="primary" data-action="submit-test" ${done !== state.questions.length ? "disabled" : ""}>生成我的结果</button>` : `<button class="secondary" data-action="next-question" ${!selected ? "disabled" : ""}>下一题</button>`}</div>
  </section>`;
}

async function chooseOption(optionId) {
  const question = state.questions[state.questionIndex];
  state.answers[question.id] = Number(optionId);
  renderQuestion();
  try {
    await api(`/test-sessions/${state.session.id}/answers`, "PUT", { question_id: question.id, option_id: Number(optionId) });
    track("question_answer", { question_id: question.id }, state.session.id);
    if (state.questionIndex < state.questions.length - 1) { state.questionIndex += 1; renderQuestion(); }
  } catch (error) { toast("保存失败，请重试"); }
}

async function submitTest() {
  if (Object.keys(state.answers).length !== state.questions.length) return toast("请先完成全部题目");
  setLoading("正在生成稳定的 Demo 结果…");
  try {
    const submitted = await api(`/test-sessions/${state.session.id}/submit`, "POST", {});
    track("test_submit", {}, state.session.id);
    if (submitted.relationship_id) return relation(submitted.relationship_id);
    return result(submitted.result_id);
  } catch (error) { setError(error, "history"); }
}

async function result(id) {
  setLoading("正在读取人格结果…");
  try {
    state.result = await api(`/results/${id}/preview`);
    const scoreItems = Object.entries(state.result.dimension_scores).map(([key, value]) => `<div class="score-item"><strong>${value}</strong><small>${labels[key] || key}</small></div>`).join("");
    app.innerHTML = `<section class="panel">
      <div class="result-top"><span class="eyebrow">Your Hidden Persona</span><div class="result-glyph">☾</div><h2>${escapeHtml(state.result.name)}</h2><div class="tags">${state.result.tags.map(tag => `<span class="tag">${escapeHtml(tag)}</span>`).join("")}</div><p class="muted">${escapeHtml(state.result.summary)}</p></div>
      <div class="score-grid">${scoreItems}</div>
      <div class="cta-row"><button class="primary" data-action="full-result" data-id="${id}">${state.result.is_unlocked ? "查看完整报告" : "解锁完整报告"}</button><button class="secondary" data-action="create-invite" data-id="${id}">邀请好友测关系</button><button class="ghost" data-action="history">历史记录</button></div>
      <div id="invite-slot"></div>
    </section>`;
    track("result_preview", { result_id: id });
  } catch (error) { setError(error, "history"); }
}

async function fullResult(id) {
  setLoading("正在打开完整报告…");
  try {
    let full;
    try { full = await api(`/results/${id}/full`); }
    catch (error) {
      if (error.status !== 403) throw error;
      await api(`/results/${id}/unlock`, "POST", { unlock_type: "MOCK" });
      full = await api(`/results/${id}/full`);
      toast("Demo 报告已直接解锁");
    }
    app.innerHTML = `<section class="panel">
      <span class="eyebrow">Full Report</span><h2>${escapeHtml(full.name)}</h2><p class="muted">${escapeHtml(full.summary)}</p>
      ${full.sections.map(section => `<article class="section-card"><h3>${escapeHtml(section.title)}</h3><p class="muted">${escapeHtml(section.content)}</p></article>`).join("")}
      <div class="cta-row"><button class="primary" data-action="result" data-id="${id}">返回基础结果</button><button class="ghost" data-action="home">回到首页</button></div>
    </section>`;
    track("full_result_view", { result_id: id });
  } catch (error) { setError(error, "history"); }
}

async function createInvite(resultId) {
  try {
    state.invite = await api("/relation-invites", "POST", { result_id: Number(resultId) });
    const slot = document.querySelector("#invite-slot");
    slot.innerHTML = `<div class="invite-box"><h3>好友邀请已创建</h3><p>邀请码已准备好。为了方便本机人工验收，可直接切换到 B 并接受。</p><div class="invite-code">${escapeHtml(state.invite.invite_code)}</div><div class="cta-row"><button class="secondary" data-action="copy-invite">复制邀请码</button><button class="primary" data-action="switch-b-accept">切换到 B 并接受邀请</button></div></div>`;
    track("invite_create", { result_id: Number(resultId) });
  } catch (error) { toast(error.message); }
}

async function switchBAndAccept() {
  setLoading("正在切换到用户 B 并接受邀请…");
  try {
    await login("user_b", false);
    const accepted = await api(`/relation-invites/${state.invite.invite_code}/accept`, "POST", {});
    state.test = await api(`/tests/${accepted.test_slug}`);
    toast("用户 B 已接受邀请");
    await startTest(accepted.invite_id);
    track("invite_accept", { invite_id: accepted.invite_id });
  } catch (error) { setError(error, "home"); }
}

async function relation(id) {
  setLoading("正在生成双人关系报告…");
  try {
    const report = await api(`/relationships/${id}`);
    const dimensionLabels = { emotion: "情绪默契", communication: "沟通节奏", pace: "行动节奏", exploration: "新鲜感匹配" };
    app.innerHTML = `<section class="panel">
      <div class="result-top"><span class="eyebrow">Relationship Report</span><p class="muted">你们是</p><h2>「${escapeHtml(report.report_payload.name)}」</h2><p class="muted">${escapeHtml(report.report_payload.summary)}</p><div class="relation-score"><div><strong>${report.compatibility_score}</strong><span>相处适配度</span></div></div></div>
      <div class="relation-dimensions">${Object.entries(report.dimension_scores).map(([key, value]) => `<div class="relation-dimension"><span>${dimensionLabels[key] || key}</span><strong>${value}</strong></div>`).join("")}</div>
      <div class="cta-row"><button class="primary" data-action="history">查看双方历史</button><button class="ghost" data-action="home">回到首页</button></div>
    </section>`;
    track("relationship_view", { relationship_id: id });
  } catch (error) { setError(error, "history"); }
}

async function history() {
  setLoading("正在读取历史记录…");
  try {
    const [results, relationships] = await Promise.all([api("/me/results"), api("/me/relationships")]);
    app.innerHTML = `<section class="panel wide">
      <div class="panel-header"><div><span class="eyebrow">Archive</span><h2>我的探索记录</h2><p class="muted">当前查看：${state.user === "user_a" ? "用户 A" : "用户 B"}</p></div><button class="ghost" data-action="home">返回首页</button></div>
      <h3>人格测试</h3>${results.length ? results.map(item => `<button class="history-item text-button" data-action="result" data-id="${item.id}"><strong>${escapeHtml(item.name)}</strong><span class="muted">${escapeHtml(item.summary)}</span></button>`).join("") : `<div class="empty">还没有人格测试记录</div>`}
      <h3>好友关系</h3>${relationships.length ? relationships.map(item => `<button class="history-item text-button" data-action="relation" data-id="${item.id}"><strong>${escapeHtml(item.report_payload.name)}</strong><span class="muted">相处适配度 ${item.compatibility_score}</span></button>`).join("") : `<div class="empty">还没有双人关系报告</div>`}
    </section>`;
  } catch (error) { setError(error, "history"); }
}

function privacy() {
  app.innerHTML = `<section class="panel"><span class="eyebrow">Privacy</span><h2>隐私与数据</h2><p class="muted">本 Demo 不收集手机号、身份证、定位、通讯录或敏感健康信息。测试答案、结果快照和关系报告只保存在本地 Demo 数据库。</p><p class="muted">删除会移除当前模拟用户的测试、结果、邀请、关系与分析事件，且不可恢复。</p><div class="cta-row"><button class="ghost" data-action="home">返回首页</button><button class="secondary" data-action="delete-data">删除当前用户数据</button></div></section>`;
}

async function deleteData() {
  if (!window.confirm("确定删除当前模拟用户的全部测试数据吗？此操作不可恢复。")) return;
  try { await api("/me/data", "DELETE"); state.token = ""; localStorage.removeItem("web_token"); await login(state.user); toast("当前用户数据已删除"); }
  catch (error) { toast(error.message); }
}

function track(event_name, properties = {}, session_id) {
  api("/events", "POST", { event_name, properties, ...(session_id ? { session_id } : {}) }).catch(() => undefined);
}

document.addEventListener("click", async event => {
  const button = event.target.closest("button");
  if (!button) return;
  if (button.dataset.user) { await login(button.dataset.user); return; }
  if (button.dataset.option) { await chooseOption(button.dataset.option); return; }
  const action = button.dataset.action;
  const actions = {
    home, detail, history, privacy,
    "start-test": () => startTest(),
    "prev-question": () => { state.questionIndex = Math.max(0, state.questionIndex - 1); renderQuestion(); },
    "next-question": () => { state.questionIndex = Math.min(state.questions.length - 1, state.questionIndex + 1); renderQuestion(); },
    "submit-test": submitTest,
    result: () => result(button.dataset.id),
    "full-result": () => fullResult(button.dataset.id),
    "create-invite": () => createInvite(button.dataset.id),
    "copy-invite": async () => { await navigator.clipboard.writeText(state.invite.invite_code); toast("邀请码已复制"); },
    "switch-b-accept": switchBAndAccept,
    relation: () => relation(button.dataset.id),
    "delete-data": deleteData,
  };
  if (actions[action]) await actions[action]();
});

(async function boot() {
  setLoading();
  try { await ensureLogin(); home(); }
  catch (error) { setError(error, "home"); }
})();

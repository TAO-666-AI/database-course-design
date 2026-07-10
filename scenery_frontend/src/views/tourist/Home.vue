<template>
  <section>
    <h1 class="hero-title">你好，欢迎来到南京中山陵</h1>
    <p class="hero-sub">中山陵导览 · 历史文化 · 文本问答服务</p>

    <div class="guide-card" @click="$router.push('/tourist/chat')">
      <div class="avatar">问</div>
      <div class="guide-content">
        <div class="guide-kicker">智能导览</div>
        <h2>中山陵导览助手</h2>
        <p>围绕景点、路线、门票和开放时间提供即时问答。</p>
        <div class="guide-tags">
          <span>FAQ 优先</span>
          <span>历史记录</span>
          <span>游客服务</span>
        </div>
      </div>
      <div class="arrow-wrap"><ArrowRight class="arrow" /></div>
    </div>

    <h3 class="section-title">快捷服务</h3>
    <div class="quick-grid">
      <div class="quick-card" @click="$router.push('/tourist/spots')">
        <Location class="teal" />
        <strong>景点介绍</strong>
        <span>了解景区景点详情与讲解信息</span>
      </div>
      <div class="quick-card" @click="$router.push('/tourist/routes')">
        <Guide class="blue" />
        <strong>推荐路线</strong>
        <span>浏览轻松游、普通游与深度游路线</span>
      </div>
      <div class="quick-card" @click="$router.push('/tourist/faqs')">
        <Document class="gold" />
        <strong>常见问题</strong>
        <span>门票、开放时间、路线快速查询</span>
      </div>
      <div class="quick-card" @click="$router.push('/tourist/feedback')">
        <ChatLineRound class="red" />
        <strong>游客反馈</strong>
        <span>提交建议并查看处理状态</span>
      </div>
    </div>
  </section>
</template>

<style scoped>
.hero-title {
  margin: 0;
  font-size: 29px;
  font-weight: 900;
}
.hero-sub {
  color: var(--muted);
  margin: 12px 0 22px;
}
.guide-card {
  position: relative;
  overflow: hidden;
  border-radius: 22px;
  border: 1px solid #cde9ea;
  background:
    linear-gradient(135deg, rgba(232, 251, 248, 0.95), rgba(239, 245, 255, 0.96));
  padding: 18px;
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 22px;
  min-height: 158px;
  cursor: pointer;
  box-shadow: 0 16px 34px rgba(25, 68, 91, 0.08);
}
.guide-card::after {
  content: '';
  position: absolute;
  width: 128px;
  height: 128px;
  right: -42px;
  top: -42px;
  border-radius: 50%;
  background: rgba(18, 164, 147, 0.09);
}
.avatar {
  width: 64px;
  height: 64px;
  flex: 0 0 64px;
  border-radius: 20px;
  background: linear-gradient(135deg, #13b1a0, #087d73);
  color: #fff;
  display: grid;
  place-items: center;
  font-size: 30px;
  font-weight: 900;
  box-shadow: 0 10px 22px rgba(18, 164, 147, 0.22);
  position: relative;
  z-index: 1;
}
.guide-content {
  min-width: 0;
  position: relative;
  z-index: 1;
}
.guide-kicker {
  display: inline-block;
  color: var(--primary-dark);
  background: rgba(255, 255, 255, 0.75);
  border: 1px solid #cde9ea;
  border-radius: 999px;
  padding: 3px 9px;
  font-size: 12px;
  font-weight: 800;
  margin-bottom: 8px;
}
.guide-card h2 {
  margin: 0 0 8px;
  font-size: 21px;
  line-height: 1.25;
}
.guide-card p {
  margin: 0;
  color: var(--muted);
  line-height: 1.55;
  font-size: 14px;
}
.guide-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 7px;
  margin-top: 12px;
}
.guide-tags span {
  border-radius: 999px;
  padding: 5px 9px;
  background: #fff;
  color: var(--primary-dark);
  font-size: 12px;
  border: 1px solid #d9efec;
}
.arrow-wrap {
  width: 38px;
  height: 38px;
  flex: 0 0 38px;
  margin-left: auto;
  border-radius: 50%;
  display: grid;
  place-items: center;
  color: #fff;
  background: var(--primary);
  position: relative;
  z-index: 1;
  box-shadow: 0 8px 18px rgba(18, 164, 147, 0.2);
}
.arrow {
  width: 22px;
  height: 22px;
}
@media (max-width: 430px) {
  .guide-card {
    align-items: flex-start;
  }
  .avatar {
    width: 56px;
    height: 56px;
    flex-basis: 56px;
    font-size: 26px;
  }
  .arrow-wrap {
    width: 34px;
    height: 34px;
    flex-basis: 34px;
  }
}
.section-title {
  margin: 30px 0 16px;
}
.quick-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}
.quick-card {
  background: #fff;
  border-radius: 18px;
  padding: 22px 18px;
  min-height: 148px;
  box-shadow: 0 12px 28px rgba(25, 68, 91, 0.06);
  cursor: pointer;
}
.quick-card svg {
  width: 34px;
  height: 34px;
  padding: 8px;
  border-radius: 13px;
  background: #eff8f7;
  box-sizing: content-box;
}
.quick-card strong {
  display: block;
  margin: 18px 0 8px;
  font-size: 18px;
}
.quick-card span {
  color: var(--muted);
  font-size: 14px;
}
.teal {
  color: var(--primary);
}
.blue {
  color: #4d76ff;
}
.gold {
  color: #d59d31;
}
.red {
  color: #ef5b66;
}
</style>

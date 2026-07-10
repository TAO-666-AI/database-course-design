<template>
  <div class="tourist-shell">
    <main class="tourist-main">
      <router-view />
    </main>
    <nav class="bottom-nav">
      <router-link to="/tourist/home"><House />首页</router-link>
      <router-link to="/tourist/spots"><Location />景点</router-link>
      <router-link class="chat-entry" to="/tourist/chat"><ChatDotRound />问答</router-link>
      <router-link to="/tourist/routes"><Guide />路线</router-link>
      <router-link to="/tourist/mine"><User />我的</router-link>
    </nav>
  </div>
</template>

<style scoped>
.tourist-shell {
  min-height: 100vh;
  max-width: 620px;
  margin: 0 auto;
  background: linear-gradient(180deg, #effbf8 0%, #f7f9ff 55%, #f4f9fb 100%);
  box-shadow: 0 0 0 1px rgba(190, 220, 225, 0.4);
}
.tourist-main {
  min-height: 100vh;
  padding: 24px 24px 110px;
}
.bottom-nav {
  position: fixed;
  left: 50%;
  bottom: 0;
  transform: translateX(-50%);
  width: min(620px, 100%);
  height: 82px;
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  align-items: center;
  background: rgba(255, 255, 255, 0.95);
  border-top: 1px solid #e1edf1;
  backdrop-filter: blur(12px);
}
.bottom-nav a {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  color: #8190a6;
  font-size: 13px;
}
.bottom-nav svg {
  width: 23px;
  height: 23px;
}
.bottom-nav a.router-link-active {
  color: var(--primary);
  font-weight: 700;
}
.chat-entry {
  width: 66px;
  height: 66px;
  margin: -28px auto 0;
  border-radius: 50%;
  background: var(--primary);
  color: #fff !important;
  justify-content: center;
  box-shadow: 0 14px 30px rgba(18, 164, 147, 0.32);
}
</style>

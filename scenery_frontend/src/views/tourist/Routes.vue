<template>
  <section>
    <h1 class="page-title">路线推荐</h1>
    <p class="page-subtitle">根据游览时间选择中山陵轻松版、普通版和深度版路线。</p>
    <div class="toolbar">
      <el-input v-model="query.keyword" placeholder="搜索路线" clearable />
      <el-select v-model="query.difficulty" placeholder="程度" clearable style="width: 140px">
        <el-option label="轻松" value="easy" />
        <el-option label="普通" value="medium" />
        <el-option label="深度" value="hard" />
      </el-select>
      <el-button type="primary" @click="load">查询</el-button>
    </div>
    <div v-loading="loading" class="route-list">
      <article v-for="item in items" :key="item.id" class="route-card">
        <div class="route-head">
          <h3>{{ item.name }}</h3>
          <el-tag>{{ difficultyText(item.difficulty) }}</el-tag>
        </div>
        <p>{{ item.description }}</p>
        <div class="route-meta">预计 {{ item.duration_hours }} 小时</div>
        <div v-if="item.spots?.length" class="route-map">
          <div class="map-title">路线图</div>
          <div class="route-steps">
            <div v-for="(spot, index) in item.spots" :key="spot.id" class="route-step">
              <div class="step-dot">{{ index + 1 }}</div>
              <div class="step-card">
                <strong>{{ spot.name }}</strong>
                <span>{{ spot.category || '景点' }}</span>
                <em>{{ spot.location || '中山陵景区游线' }}</em>
                <small>{{ spot.recommended_duration || '建议短暂停留' }}</small>
              </div>
            </div>
          </div>
        </div>
      </article>
      <div v-if="!items.length" class="empty-hint">暂无路线数据</div>
    </div>
  </section>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue'
import { getRoutes } from '../../api/tourist'

const loading = ref(false)
const items = ref([])
const query = reactive({ keyword: '', difficulty: '' })
const difficultyText = (v) => ({ easy: '轻松', medium: '普通', hard: '深度' }[v] || v)
const load = async () => {
  loading.value = true
  try {
    const res = await getRoutes(query)
    if (res.code === 200) items.value = res.data.items
  } finally {
    loading.value = false
  }
}
onMounted(load)
</script>

<style scoped>
.route-list {
  display: grid;
  gap: 18px;
  width: 100%;
  min-width: 0;
}
.route-card {
  width: 100%;
  max-width: 100%;
  min-width: 0;
  overflow: hidden;
  background: #fff;
  border-left: 5px solid var(--primary);
  border-radius: 20px;
  padding: 22px;
  box-shadow: 0 12px 28px rgba(25, 68, 91, 0.06);
}
.route-head {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}
h3 {
  margin: 0;
  font-size: 21px;
  min-width: 0;
  overflow-wrap: anywhere;
}
p {
  color: var(--muted);
  line-height: 1.7;
}
.route-meta {
  color: var(--primary-dark);
  font-weight: 800;
  margin-bottom: 12px;
}
.route-map {
  margin-top: 14px;
  min-width: 0;
}
.map-title {
  color: var(--primary-dark);
  font-weight: 800;
  margin-bottom: 12px;
}
.route-steps {
  display: grid;
  gap: 10px;
  min-width: 0;
  padding: 4px 0;
}
.route-step {
  min-width: 0;
  position: relative;
  display: grid;
  grid-template-columns: 32px minmax(0, 1fr);
  column-gap: 10px;
  align-items: start;
}
.route-step::before {
  content: '';
  position: absolute;
  top: 32px;
  left: 15px;
  bottom: -10px;
  width: 3px;
  background: #bfe6e2;
}
.route-step:last-child::before {
  display: none;
}
.step-dot {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: var(--primary);
  color: #fff;
  display: grid;
  place-items: center;
  font-weight: 800;
  position: relative;
  z-index: 1;
  box-shadow: 0 6px 14px rgba(16, 166, 150, 0.24);
}
.step-card {
  width: 100%;
  min-width: 0;
  border: 1px solid #d9efec;
  background: #f7fdfc;
  border-radius: 12px;
  padding: 10px 12px;
}
.step-card strong,
.step-card span,
.step-card em,
.step-card small {
  display: block;
}
.step-card strong {
  color: var(--text);
  margin-bottom: 5px;
}
.step-card span {
  color: var(--primary-dark);
  font-size: 13px;
  margin-bottom: 5px;
}
.step-card em {
  color: #60718a;
  font-style: normal;
  font-size: 12px;
  line-height: 1.5;
  margin-bottom: 5px;
}
.step-card small {
  color: #8ca0b4;
  font-size: 12px;
}
</style>

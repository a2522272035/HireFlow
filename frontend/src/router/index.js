import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Layout',
    component: () => import('@/components/layout/MainLayout.vue'),
    children: [
      {
        path: '',
        redirect: '/resumes',
      },
      {
        path: 'resumes',
        name: 'ResumeAnalysis',
        component: () => import('@/views/ResumeAnalysis.vue'),
        meta: { title: '简历分析' },
      },
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('@/views/Dashboard.vue'),
        meta: { title: '仪表盘' },
      },
      {
        path: 'interviews',
        name: 'CandidateList',
        component: () => import('@/views/CandidateList.vue'),
        meta: { title: '候选人管理' },
      },
      {
        path: 'interview/:id',
        name: 'InterviewRoom',
        component: () => import('@/views/InterviewRoom.vue'),
        meta: { title: '面试间' },
      },
      {
        path: 'questions',
        name: 'QuestionList',
        component: () => import('@/views/QuestionList.vue'),
        meta: { title: '提问清单' },
      },
      {
        path: 'reports/:id',
        name: 'ReportDetail',
        component: () => import('@/views/ReportDetail.vue'),
        meta: { title: '评估报告' },
      },
      {
        path: 'policies',
        name: 'PolicyQA',
        component: () => import('@/views/PolicyQA.vue'),
        meta: { title: '规章制度问答' },
      },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  document.title = to.meta.title
    ? `${to.meta.title} - HireFlow`
    : 'HireFlow'
  next()
})

export default router

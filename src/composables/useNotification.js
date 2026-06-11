// 第五阶段考点：自定义 Composables 实现逻辑复用
export function useNotification() {
  const showSuccess = (msg) => {
    // 这里简单封装一个弹窗，实际企业项目中会替换成更高级的 UI 组件弹窗
    alert(`✅ [操作成功] ${msg}`)
  }

  const showError = (msg) => {
    alert(`❌ [操作失败] ${msg}`)
  }

  return {
    showSuccess,
    showError
  }
}
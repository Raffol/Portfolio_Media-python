import { ref, onMounted } from 'vue'
import { getWorks } from '@/api/works'

export function useWorks(params = {}) {
  const works = ref([])
  const loading = ref(true)
  const error = ref(null)

  const load = async () => {
    loading.value = true
    try {
      works.value = await getWorks(params)
    } catch (e) {
      error.value = e
    } finally {
      loading.value = false
    }
  }

  onMounted(load)
  return { works, loading, error, reload: load }
}

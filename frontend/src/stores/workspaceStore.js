import { defineStore } from 'pinia'

const LS_KEY = 'bde.workspace'

export const useWorkspaceStore = defineStore('workspace', {
  state: () => ({
    datasetId: 'blood-domain-dataset',
    filters: {
      dateRange: null,
      dimension: 'time'
    },
    dashboards: {
      // id -> { id, name, layout, widgets }
    },
    activeDashboardId: ''
  }),
  actions: {
    load() {
      try {
        const raw = localStorage.getItem(LS_KEY)
        if (!raw) return
        const parsed = JSON.parse(raw)
        this.$patch(parsed)
      } catch {
        // ignore
      }
    },
    save() {
      const payload = {
        datasetId: this.datasetId,
        filters: this.filters,
        dashboards: this.dashboards,
        activeDashboardId: this.activeDashboardId
      }
      localStorage.setItem(LS_KEY, JSON.stringify(payload))
    },
    setDataset(id) {
      this.datasetId = id
      this.save()
    },
    setFilters(patch) {
      this.filters = { ...this.filters, ...patch }
      this.save()
    },
    upsertDashboard(d) {
      this.dashboards[d.id] = d
      if (!this.activeDashboardId) this.activeDashboardId = d.id
      this.save()
    },
    setActiveDashboard(id) {
      this.activeDashboardId = id
      this.save()
    },
    ensureDefaultDashboard() {
      if (Object.keys(this.dashboards).length) return
      const id = 'default'
      this.upsertDashboard({
        id,
        name: 'Default Dashboard',
        layout: [
          { i: 'trend', x: 0, y: 0, w: 6, h: 8 },
          { i: 'forecast', x: 6, y: 0, w: 6, h: 8 },
          { i: 'associations', x: 0, y: 8, w: 12, h: 8 }
        ],
        widgets: {
          trend: { type: 'trend' },
          forecast: { type: 'forecast' },
          associations: { type: 'associations' }
        }
      })
    }
  }
})

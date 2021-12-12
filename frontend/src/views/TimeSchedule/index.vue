<template>
    <div class="h-100 content-box">
        <bk-tab :active.sync="activePanel" type="unborder-card">
            <bk-tab-panel
                v-for="panel in panels"
                :label="panel.name"
                :name="panel.index"
                :key="panel.index">
            </bk-tab-panel>
        </bk-tab>
        <component :is="activeComponent" />
    </div>
</template>

<script>
    import UserTime from './UserTime'
    import GroupTime from './GroupTime'
    export default {
        name: 'index',
        components: { UserTime, GroupTime },
        data () {
            return {
                activePanel: 'group',
                panels: [
                    { index: 'user', name: '个人时间管理' },
                    { index: 'group', name: '组时间管理' }
                ]
            }
        },
        computed: {
            activeComponent () {
                if (this.activePanel === 'user') {
                    return UserTime
                }
                return GroupTime
            }
        }
    }
</script>

<style scoped>
    @import "./index.css";
</style>

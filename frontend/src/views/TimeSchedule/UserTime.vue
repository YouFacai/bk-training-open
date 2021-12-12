<template>
    <div class="user-time-content-box" v-bkloading="{ isLoading: loading, zIndex: 10 }">
        <div class="header-box">
            <bk-form form-type="inline">
                <bk-form-item label="起始日期">
                    <bk-date-picker class="mr15" v-model="startTime" placeholder="起始日期" />
                </bk-form-item>
                <bk-form-item label="结束日期">
                    <bk-date-picker class="mr15" v-model="endTime" placeholder="结束日期" />
                </bk-form-item>
            </bk-form>
            <bk-button theme="primary" @click="showAddTime">增加</bk-button>
        </div>
        <bk-table class="data-table" :data="timeData" border>
            <bk-table-column prop="date" label="日期"></bk-table-column>
            <bk-table-column prop="start_time" label="起始时间"></bk-table-column>
            <bk-table-column prop="end_time" label="结束时间"></bk-table-column>
            <bk-table-column label="操作" width="100">
                <template slot-scope="props">
                    <bk-button theme="danger" text @click="removeTime(props.row)">移除</bk-button>
                </template>
            </bk-table-column>
        </bk-table>
        <bk-dialog v-model="addTimeDialog.visible" render-directive="if" theme="primary" title="添加空闲时间" class="add-time-dialog" @confirm="doAddTime">
            <bk-form label-width="80">
                <bk-form-item label="日期">
                    <bk-date-picker class="mr15" :options="options" v-model="addTimeDialog.data.date" placeholder="起始日期" />
                </bk-form-item>
                <bk-form-item label="起始时间">
                    <bk-time-picker class="mr15" format="HH:mm" :editable="false" :enter-mode="false" v-model="addTimeDialog.data.startTime" placeholder="结束日期" />
                </bk-form-item>
                <bk-form-item label="结束时间">
                    <bk-time-picker class="mr15" format="HH:mm" :editable="false" :enter-mode="false" v-model="addTimeDialog.data.endTime" placeholder="结束日期" />
                </bk-form-item>
            </bk-form>
        </bk-dialog>
    </div>
</template>

<script>
    import moment from 'moment'

    export default {
        name: 'UserTime',
        data () {
            return {
                loading: true,
                startTime: new Date(),
                endTime: new Date(),
                timeData: [],
                addTimeDialog: {
                    visible: false,
                    data: {
                        date: new Date(),
                        startTime: '08:00:00',
                        endTime: '22:00:00'
                    }
                },
                options: {
                    disabledDate: (date) => {
                        return date < new Date()
                    }
                }
            }
        },
        created () {
            this.loadUserTime()
        },
        methods: {
            loadUserTime () {
                this.loading = true
                const startDate = moment(this.startTime).format(moment.HTML5_FMT.DATE)
                const endDate = moment(this.endTime).format(moment.HTML5_FMT.DATE)
                this.$http.get(
                    '/free_time/?start_date=' + startDate + '&end_date=' + endDate
                ).then(res => {
                    if (res.result) {
                        this.timeData = res.data
                    } else {
                        this.$bkMessage({
                            theme: 'warning',
                            message: res.message
                        })
                    }
                }).finally(() => {
                    setTimeout(() => {
                        this.loading = false
                    }, 600)
                })
            },
            removeTime (row) {
                this.loading = true
                this.$http.delete(
                    '/free_time/' + row.id + '/'
                ).finally(() => {
                    this.loadUserTime()
                })
            },
            showAddTime () {
                this.addTimeDialog.data = {
                    date: new Date(),
                    startTime: '08:00',
                    endTime: '22:00'
                }
                this.addTimeDialog.visible = true
            },
            doAddTime () {
                this.addTimeDialog.visible = false
                this.loading = true
                const date = moment(this.addTimeDialog.data.date).format('YYYY-MM-DD')
                const data = {
                    free_times: [
                        {
                            start_time: date + ' ' + this.addTimeDialog.data.startTime,
                            end_time: date + ' ' + this.addTimeDialog.data.endTime
                        }
                    ]
                }
                this.$http.post(
                    '/free_time/',
                    data
                ).then(res => {
                    if (res.result) {
                        this.loadUserTime()
                    } else {
                        this.$bkMessage({
                            theme: 'warning',
                            message: res.message
                        })
                        this.loading = false
                    }
                })
            }
        }
    }
</script>

<style scoped>
    .user-time-content-box {
        padding: 0 10px;
        box-sizing: border-box;
    }

    .data-table {
        margin-top: 20px;
    }
</style>

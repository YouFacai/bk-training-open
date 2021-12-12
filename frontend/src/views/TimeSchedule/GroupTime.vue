<template>
    <div class="user-time-content-box" v-bkloading="{ isLoading: loading, zIndex: 10 }">
        <div class="header-box">
            <bk-form form-type="inline">
                <bk-form-item label="组">
                    <bk-select class="mr15" :disabled="false" v-model="curGroupId" style="width: 200px;">
                        <bk-option v-for="option in groups"
                            :key="option.id"
                            :id="option.id"
                            :name="option.name">
                        </bk-option>
                    </bk-select>
                </bk-form-item>
                <bk-form-item label="日期">
                    <bk-date-picker class="mr15" v-model="startDate" placeholder="起始日期" style="width: 200px;" />
                </bk-form-item>
            </bk-form>
            <bk-button theme="primary" @click="loadTime(); splitTime();">搜索</bk-button>
        </div>
        <div class="group-time-box">
            <div v-for="user in timeData" :key="user.username">
                <div class="username-box">
                    {{ user.username }}
                </div>
                <div class="time-box">
                    <bk-popover :content="formatTimeDelta(item)" v-for="item in timeSplits" :key="item">
                        <div class="time-single-box" :class="checkFreeTime(user.free_time, item)"></div>
                    </bk-popover>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import moment from 'moment'
    export default {
        name: 'GroupTime',
        data () {
            return {
                loading: true,
                startDate: new Date(new Date(new Date().toLocaleDateString()).getTime()),
                endDate: new Date(new Date(new Date().toLocaleDateString()).getTime()),
                timeDelta: 'h',
                timeSplits: [],
                timeData: [],
                groups: [],
                curGroupId: null
            }
        },
        watch: {
            timeDelta () {
                this.splitTime()
            },
            startDate () {
                this.endDate = this.startDate
            }
        },
        created () {
            this.loadGroup()
            this.splitTime()
        },
        methods: {
            loadGroup () {
                this.$http.get(
                    '/list_admin_group/'
                ).then(res => {
                    if (res.result) {
                        this.groups = res.data
                        if (this.groups.length > 0) {
                            this.curGroupId = this.groups[0].id
                        }
                    }
                }).finally(() => {
                    this.loadTime()
                })
            },
            loadTime () {
                if (!this.curGroupId) {
                    return
                }
                this.loading = true
                const startDate = moment(this.startDate).format(moment.HTML5_FMT.DATE)
                const endDate = moment(this.endDate).format(moment.HTML5_FMT.DATE)
                this.$http.get(
                    '/group_free_time/' + this.curGroupId + '/?start_date=' + startDate + '&end_date=' + endDate
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
            splitTime () {
                this.timeSplits = []
                let delta = 3600000
                if (this.timeDelta === 'd') {
                    delta = delta * 24
                }
                let i = 0
                while (this.startDate - (-(i + 1) * delta) <= this.endDate - (-24 * 3600 * 1000)) {
                    this.timeSplits.push({
                        startTime: new Date(this.startDate - (-i * delta)),
                        endTime: new Date(this.startDate - (-(i + 1) * delta))
                    })
                    i++
                }
            },
            checkFreeTime (freeTime, timeDelta) {
                for (const i in freeTime) {
                    const startTime = new Date(freeTime[i].start_time)
                    const endTime = new Date(freeTime[i].end_time)
                    if (timeDelta.startTime >= startTime && timeDelta.endTime <= endTime) {
                        return 'blue-background'
                    }
                }
                return 'gray-background'
            },
            formatTimeDelta (item) {
                return moment(item.startTime).format(moment.HTML5_FMT.DATETIME_LOCAL) + '~' + moment(item.endTime).format(moment.HTML5_FMT.DATETIME_LOCAL)
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

    .group-time-box {
        margin-top: 20px;
        padding: 10px;
        box-sizing: border-box;
    }

    .group-time-box > div {
        display: flex;
        border: 1px solid #EAEBF0;
    }

    .group-time-box .username-box {
        line-height: 36px;
        width: 200px;
        word-break: break-all;
        padding: 0 10px;
    }

    .group-time-box .time-box {
        display: flex;
        align-items: center;
        justify-content: space-around;
        width: 100%;
    }

    .group-time-box .time-box .time-single-box {
        width: 20px;
        height: 20px;
        margin-right: 10px;
    }

    .blue-background {
        background: #3A84FF;
    }

    .gray-background {
        background: #DCDEE5;
    }
</style>

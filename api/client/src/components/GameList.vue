<template>
    <v-container>
        <v-autocomplete
                :search-input.sync="inputGameName"
                v-model="selectGameName" clearable
                label="使用游戏名/简拼/全拼搜索">
        </v-autocomplete>

        <v-data-table :headers="tableHeader"
                      hide-actions :items="games" item-key="id">
            <template slot="items" slot-scope="props">
                <td>{{ props.item.game_name }}</td>
                <td>{{ props.item.game_number }}</td>
                <td>{{ props.item.game_price === 0? "免费":props.item.game_price }}</td>
                <td>
                    <v-icon @click="openStore(props.item)" small>call_made</v-icon>
                </td>
                <td>
                    <router-link :to="{name:'product',params:{number:props.item.game_number}}">历史价格</router-link>
                </td>
            </template>
        </v-data-table>
        <div class="text-xs-center">
            <v-pagination @input="changePage"
                          v-model="pagination.page"
                          :total-visible="8"
                          :length="pagination.pasge"></v-pagination>
        </div>
    </v-container>
</template>

<script>

    import {debounceTime, map, switchMap, distinctUntilChanged, filter} from 'rxjs/operators'
    import {from} from 'rxjs'
    import {FetchDataStore} from "../helper/helper";


    export default {
        name: "GameList",
        data() {
            return {
                loading: false,
                games: [],
                tableHeader: [
                    {text: '游戏名称', value: 'game_name'},
                    {text: '游戏编号', value: 'game_number'},
                    {text: '当前价格', value: 'game_price'},
                    {text: '链接', value: 'game_link'},
                    {text: '', value: ''},
                ],
                pagination: {
                    page: 1,
                    rowsPerPage: 20,
                    pasge: 10,
                    totalItems: 10,
                    descending: false
                },
                inputGameName: null,
                selectGameName: null
            }
        },
        mounted() {
            this.getData()
        },
        watch: {
            inputGameName(keyword) {
                keyword = keyword.replace(/[\ |\~|\`|\!|\@|\#|\$|\%|\^|\&|\*|\(|\)|\-|\_|\+|\=|\||\\|\[|\]|\{|\}|\;|\:|\"|\'|\,|\<|\.|\>|\/|\?]/g, "");
                const url = new URL(baseUrl + 'filter')
                const params = {keyword: keyword}
                url.search = new URLSearchParams(params)
                new FetchDataStore(() => fetch(url))
                    .data$
                    .subscribe(res => {
                        if (typeof(res.items) === 'undefined') {
                            this.games = res
                        } else {
                            this.games = res.items
                        }
                    })
            }
        },
        methods: {
            getData() {

                const url = new URL(baseUrl + 'games')
                const params = {
                    page: this.pagination.page,
                    per_page: this.pagination.rowsPerPage
                }
                url.search = new URLSearchParams(params)
                from(fetch(url))
                    .pipe(switchMap(res => from(res.json())))
                    .subscribe((res) => {
                        this.pagination = {
                            rowsPerPage: res.per_page,
                            page: res.page,
                            pasge: res.pasge,
                            totalItems: res.total
                        }
                        this.games = res.items
                    })
            },
            openStore(row) {
                const playstation = 'https://store.playstation.com'
                window.open(playstation + row.game_link)
            },
            changePage(page) {
                this.pagination.page = page
                this.getData()
            },
        },
    }
</script>

<style scoped>

</style>
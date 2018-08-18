<template>
    <v-container>
        <v-data-table :headers="gamesHeader"
                      hide-actions :items="games" item-key="id">
            <template slot="items" slot-scope="props">
                <td>{{ props.item.game_name }}</td>
                <td>{{ props.item.game_number }}</td>
                <td>{{ props.item.game_price === 0? "免费":props.item.game_price }}</td>
                <td>
                    <v-icon @click="openStore(props.item)" small>call_made</v-icon>
                </td>
                <td>
                    <router-link :to="{name:'product',params:{number:props.item.game_number}}">查看打折信息</router-link>
                </td>
            </template>
        </v-data-table>
        <div class="text-xs-center">
            <v-pagination @input="change_page"
                          v-model="pagination.page"
                          :total-visible="8"
                          :length="pagination.pasge"></v-pagination>
        </div>
    </v-container>
</template>

<script>
    import {getGames} from "../helper/getData";

    export default {
        name: "GameList",
        data() {
            return {
                temp: {},
                loading: false,
                playstation: 'https://store.playstation.com',
                games: [],
                debuggerText: '',
                gamesHeader: [
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

            }
        },
        mounted() {
            this.getData()
        },
        methods: {
            getData() {
                getGames(this.pagination.page, this.pagination.rowsPerPage).then(({data}) => {
                    this.pagination = {
                        rowsPerPage: data.per_page,
                        page: data.page,
                        pasge: data.pasge,
                        totalItems: data.total
                    }
                    this.games = data.items
                })
            },
            openStore(row) {
                this.debuggerText = row
                window.open(this.playstation + row.game_link)
            },
            change_page(page) {
                this.pagination.page = page
                this.getData()
            }
        },

    }
</script>

<style scoped>

</style>
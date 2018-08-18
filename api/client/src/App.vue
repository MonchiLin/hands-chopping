<template>
    <div id="app">
        <v-app>
            <v-toolbar>
                <v-toolbar-title>Rua!</v-toolbar-title>
                <v-spacer></v-spacer>
                <v-toolbar-items>
                    <v-btn flat @click="$router.push({name:'games'})">所有游戏</v-btn>
                    <v-btn flat @click="$router.push({name:'chopping'})">正在打折</v-btn>
                </v-toolbar-items>
            </v-toolbar>
            <router-view></router-view>
        </v-app>
    </div>
</template>

<script>
    export default {
        name: 'app',
        components: {}
    }
</script>

<style>
    div.v-menu__content {
        display: none;
    }
</style>

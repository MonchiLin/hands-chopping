<template>
    <v-container>

    </v-container>
</template>

<script>
    import {getGames} from "../helper/getData";

    export default {
        name: "GameList",
        data() {
            return {}
        },
        mounted() {
            getGames().then(console.log)
        }
    }
</script>

<style scoped>

</style>
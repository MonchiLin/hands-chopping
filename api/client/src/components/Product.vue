<template>
    <v-layout>
        <v-flex xs12 sm6 offset-sm3>
            <v-card>
                <v-card-media
                        :src="game.game_picture"
                        height="480px">
                </v-card-media>

                <v-card-title primary-title>
                    <div>
                        <h3 class="headline mb-0">{{game.game_name}}</h3>
                        <div v-html="game.game_detail"></div>
                    </div>
                </v-card-title>
                <v-list two-line v-for="price of prices">
                    <v-list-tile @click="">
                        <v-list-tile-action>
                            <v-icon>attach_money</v-icon>
                        </v-list-tile-action>

                        <v-list-tile-content>
                            <v-list-tile-title>{{price.game_price}} RMB</v-list-tile-title>
                            <v-list-tile-sub-title>{{price.time | date}}</v-list-tile-sub-title>
                        </v-list-tile-content>
                    </v-list-tile>
                </v-list>
                <v-card-actions>
                    <v-btn flat color="orange">Link
                        <v-icon right dark>cloud_upload</v-icon>
                    </v-btn>
                    <v-btn flat color="orange">Star
                        <v-icon right dark>cloud_upload</v-icon>
                    </v-btn>
                </v-card-actions>
            </v-card>
        </v-flex>
    </v-layout>
</template>
<script>
	import { switchMap } from 'rxjs/operators'
	import { from } from 'rxjs'

	export default {
		name   : 'Chopping',
		data () {
			return {
				game  : {},
				prices: [],
			}
		},
		mounted () {
			this.getData()
		},
		methods: {
			getData () {
				const self   = this,
					  url    = new URL(baseUrl + 'game'),
					  params = {
						  game_number: this.$route.params.number,
					  }

				url.search = new URLSearchParams(params)
				from(fetch(url)).pipe(switchMap(res => from(res.json()))).subscribe((res) => {
					self.game = res.game
					self.prices = res.prices
				})

			},
			openStore (game_link) {
				window.open(playstation + game_link)
			},
		},
    }
</script>

<style scoped>

</style>
<script>
	import Card from './Card.svelte'
	export let WIDTH
	export let selected
	export let cards
	export let round
	export let fileWrapper
	export let prettyFilename
</script>

{#each cards as card,index}
	<Card {WIDTH} {card} bind:selected {index} {round} {fileWrapper} {prettyFilename} />
{/each}

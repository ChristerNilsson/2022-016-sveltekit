<script>
	import _ from "lodash"
	export let WIDTH
	export let card
	export let selected
	export let index
	export let round
	export let fileWrapper
	export let prettyFilename

	$: filename = card[2] + "\\" + card[12]

	$: FS = getNumbers(filename,'F')
	$: LS = getNumbers(filename,'L')
	$: IS = getNumbers(filename,'I')
	$: RS = getNumbers(filename,'R')
	$: MS = getNumbers(filename,'M')
	$: TS = getNumbers(filename,'T')
	$: VS = getNumbers(filename,'V')

	function getNumbers(path,letter) { // Används för filnummer = MTV FLIR member tournament video file (deprecated) link invite result
		let matches
		if (letter=='F') matches = path.matchAll(/[F]\d+/g) // deprecated
		if (letter=='L') matches = path.matchAll(/[L]\d+/g)
		if (letter=='I') matches = path.matchAll(/[I]\d+/g)
		if (letter=='R') matches = path.matchAll(/[R]\d+/g)
		if (letter=='M') matches = path.matchAll(/[M]\d+/g)
		if (letter=='T') matches = path.matchAll(/[T]\d+/g)
		if (letter=='V') matches = path.matchAll(/[V]\d+/g)
		if (! matches) return []
		matches = [...matches]
		return _.map(matches, (match) => match[0].slice(1)) // skippa bokstaven
	}

	function prettyPath(path) { // Tag bort eventuellt T-nummer
		path = path.split('\\')
		path = path.slice(2,path.length-1)
		path = path.join(" • ")
		path = path.replaceAll(/_F\d+/g,'') // deprecated
		path = path.replaceAll(/_L\d+/g,'')
		path = path.replaceAll(/_I\d+/g,'')
		path = path.replaceAll(/_R\d+/g,'')
		path = path.replaceAll(/_M\d+/g,'')
		path = path.replaceAll(/_T\d+/g,'')
		path = path.replaceAll(/_V\d+/g,'')
		return path.replaceAll('_', ' ')
	}

	// function getPath(path,dir) { return path.replace("Home",dir) }

</script>

<div class="card" id="images" style="position:absolute; width:{WIDTH}px; left:{card[5]}px; top:{card[6]}px">
	<img
		margin:0px
		padding:0px
		src = {"/small/" + card[13] + ".jpg"}
		width = {WIDTH}px
		alt = ""
		on:click = {() => {
			const host = location.origin + location.pathname
			window.open(host + `?bs=${card[9]}&bw=${card[10]}&bh=${card[11]}&md5=${card[13]}&path=${card[2]}&filename=${card[12]}`)
		}}
		on:keydown = {() =>{}}
	/>
	<div class="group">
		<div class="info" style="width:{WIDTH}px">
			&nbsp;{prettyFilename(filename)}
		</div>
		<div class="info" style="width:{WIDTH}px">
			&nbsp;{prettyPath(filename)}
		</div>
		<div class="info" style="display:flex; height:13px; width:{WIDTH}px">
			&nbsp;{card[7]}

			{#if card[1]}
				&nbsp;&nbsp;{card[1]}
			{/if}

			&nbsp;&nbsp;<input class="largerCheckbox" type="checkbox" value="" bind:checked={selected[index]}/> 

			{#each FS as F}
				&nbsp;&nbsp;<a target="_blank" rel = "noreferrer" href="{fileWrapper[0][F]}">Result</a> <!-- deprecated -->
			{/each}
			{#each LS as L}
				&nbsp;&nbsp;<a target="_blank" rel = "noreferrer" href="{fileWrapper[0][L]}">Link</a>
			{/each}
			{#each IS as I}
				&nbsp;&nbsp;<a target="_blank" rel = "noreferrer" href="{fileWrapper[0][I]}">Invite</a>
			{/each}
			{#each RS as R}
				&nbsp;&nbsp;<a target="_blank" rel = "noreferrer" href="{fileWrapper[0][R]}">Result</a>
			{/each}
			{#each MS as M}
				&nbsp;&nbsp;<a target="_blank" rel = "noreferrer" href="https://member.schack.se/ViewPlayerRatingDiagram?memberid={M}">Member</a>
			{/each}
			{#each TS as T}
				&nbsp;&nbsp;<a target="_blank" rel = "noreferrer" href="https://member.schack.se/ShowTournamentServlet?id={T}&listingtype=2">Result</a>
			{/each}
			{#each VS as V}
				&nbsp;&nbsp;<a target="_blank" rel = "noreferrer" href="https://player.vimeo.com/video/{V}">Video</a>
			{/each}

			<span style="flex:2; text-align:center; white-space:nowrap;"> © Lars OA Hedlund </span>
			<span style="flex:1; text-align:right; white-space:nowrap;"> {round(card[10]*card[11]/1024/1024,1)} MP • {card[10]} x {card[11]} • {round(card[9]/1024,0)} kB &nbsp;</span>
		</div>	
	</div>
</div>

<style>
	input.largerCheckbox {
		width: 12px;
		height: 12px;
	}	
	.group {
		margin-top:-3px;
	}
	.info {
		margin:0px;
		text-align:left;
		padding-top:1px;
		white-space:nowrap;
		overflow:hidden;
		background-color:lightgray;
	}
	.card {
		margin:0px;
		font-size: 0.9em;
		max-height: 800px;
	}
	div {
		margin:0px;
		padding:0px;
		font-size: 0.9em;
	}
</style>

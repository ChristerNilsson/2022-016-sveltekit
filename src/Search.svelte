<script>
	export let sokruta
	export let text0
	export let text1
	export let stack
	export let WIDTH
	export let GAP
	export let spreadWidth
	export let path
	export let _
	export let is_jpg

	import { saveAs } from 'file-saver'

	function clear() {
		sokruta = ""
		document.getElementById("search").focus()
	}

	function share () {
		const q1 = stack.length <= 1 ? "" : "folder=" + stack.join("/") 
		const q2 = sokruta == "" ? "" : "query=" + sokruta		
		const q = q1=="" && q2=="" ? "" : "?"
		const a = q1!="" && q2!="" ? "&" : ""
		navigator.clipboard.writeText(location.origin + location.pathname + q + q1 + a + q2)
	}

	let hash = {}
	const letters = "+!§()0123456789_,.-¤"
	const stoppord = 'aasen adepterr adersson jpg lowres och på adrian allan alsamarrai amalie amen analyse anmästearen anzambi autografskrvning ble blixte calm campo cat ceremonie coh dah dax deltagran do during ea edvin eisler ellen enricsson entre exteriöre frisys fö föräldrarl fötäldrar galleriet ggr gm hampus hanna hasselbacken his hurry huvudnonader idar ingertz interiiör interiö interiöri intervjuvar intrvjuas istället jadoube joakim jonathan jouni jubileuml junioer juniotturneringen jöberg kafeet kafffet kankse khalili klari koentatorsrummet kollar kollekt kommentatorr kommentatorrummet kommentatorsrummeti kommentatro kommenttorsrummet kommpisar kompisarpg lagdledare lagledate larsson lennart lexander linnea linus livesändningl livesåndning lokander lottnig lågstadet lögdahl mallanstadiet malmö mediaansvari miniior morellr mourad muntean mästartklassen näringsllivet oc ocb ocg ochh ocj oh olk ollefsén ostafiev ove pannka pch pettersson prisutdelnineng prisutdelningl prisutdelningr prize producenr profiiler publiparti qi radd raden resultatapportering resultatrapporteing reultatrapportering reultatredovisning rmorgondagens rondpausl rånby santiago sara schackinstruktio schackyouga seo severingen sgnerer simultanspell sk slutforsering snabbschacksdm solemn solomia some spealre spelaregistrering speling spellokaleni spleare sponsorerrond steinitz stromästarna stsningsgruppen ter the thordur tran trino triumvirat truskavetska träder tuomainen utanföt vallatorpsskolan vatn vede ver veteranallmän vilolaäge waeli wedberg wernberg with wweb xunming xxxxx åskådarei åskådarer åsådare af amassadör emanuel exteriörr klaas klas kolobok line livesädningen lottnib ooch prisutdelnigen pågåender shah sllutspel stasik to träbingsparti årfest års årsjubileum rondl tränongsparti vt it problemlösnings ron xuanming la mter and bokförsälning rrond highres cafeét veterner avlutningen of ans gr an'.split(' ')

	function flatWords(node) {
		for (const key of _.keys(node)) {
			let words = key
			for (const letter of letters) {
				words = words.replaceAll(letter," ")
			}
			for (const word of words.split(' ')) {
				const wordLower = word.toLowerCase()
				if (word.length > 1 && wordLower == word) {
					hash[word] = word in hash ? hash[word]+1 : 1
				}
			}
			if (! is_jpg(key)) flatWords(node[key])
		}
	}

	function convert(hash) {
		let arr = []
		for (const key of _.keys(hash)) {
			if (! stoppord.includes(key)) {
				arr.push([key,hash[key]])
			}
		}
		arr.sort()
		return arr
	}

	function keywords() {
		hash = {}
		flatWords(_.last(path))
		const keys = convert(hash)
		const res = []
		for (const [key,antal] of keys) res.push(key + ': ' + antal)
		const blob = new Blob([res.join("\n")], {type: "text/plain;charset=utf-8;"})
		saveAs(blob, `${_.last(stack)}_${res.length}_keywords.txt`)
	}

	function help() {
		window.open("https://github.com/ChristerNilsson/2022-011-Bildbanken-svelte#readme")
	}

	// window.onload = () => document.getElementById("search").focus()

</script>

<input autocomplete="off" id="search" bind:value={sokruta} placeholder='Search' style="width:{WIDTH-2*GAP}px">
<div class="center" style="width:{WIDTH}px">
	{text1}
</div>

<div style="width:{WIDTH}px; height:34px">
	<button on:click={clear}       style="left:{0}px;         width:{spreadWidth(1/4,WIDTH)}px">Clear</button>
	<button on:click={share}       style="left:{WIDTH/4}px;   width:{spreadWidth(1/4,WIDTH)}px">Share</button>
	<button on:click={keywords}    style="left:{2*WIDTH/4}px; width:{spreadWidth(1/4,WIDTH)}px">Keywords</button>
	<button on:click={help}        style="left:{3*WIDTH/4}px; width:{spreadWidth(1/4,WIDTH)}px">Help</button>
</div>

{#if (sokruta.split(" ").length <= 3) && (sokruta.length > 0)}
	<div class="center" style="width:{WIDTH}px">
		{text0}
	</div>
{/if}

<style>
	.center {
		margin-top:7px;
		text-align:center;
		height:27px
	}
	div {
		margin:0px;
	}
	button {
		position:absolute;
		margin:2px;
		height:30px;
	}
	input {
		margin:2px;
		height:30px;
	}
	::placeholder {
		color: lightgray;
		opacity: 1;
	} 
</style>

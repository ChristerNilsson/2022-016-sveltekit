<script>
	import _ from "lodash"
	import JSZip from "jszip"
	import axios from "axios"
	import { saveAs } from "file-saver"

	export let selected
	export let images
	export let WIDTH
	export let spreadWidth
	export let MAX_DOWNLOAD
	export let stack
	export let pop

	$: n = _.sumBy(selected, (value) => value ? 1 : 0)

	function make(value) { selected = _.map(images, () => value) }
	function download(item) { return axios.get(item.url, { responseType: "blob" }).then((resp) => {zip.file(item.name, resp.data)}) }

	let zip = null

	function all() {make(true)}
	function none() {make(false)}
	function downloadAll() { // download all files as ZIP archive
		zip = new JSZip()
		const fileArr = []
		for (const i in _.range(Math.min(MAX_DOWNLOAD,selected.length))) {
			if (selected[i]==true) {
				const path = images[i][2] + "\\" + images[i][12]
				// console.log("Home\\" + images[i][13] + ".jpg")
				fileArr.push({name:path, url:"Home\\" + images[i][13] + ".jpg"})
			}
		}
		n = fileArr.length
		if (fileArr.length == 0) return

		const arrOfFiles = fileArr.map((item) => download(item)) //create array of promises
		Promise.all(arrOfFiles)
			.then(() => {zip.generateAsync({ type: "blob" }).then(function (blob) { saveAs(blob, `Bildbanken ${fileArr.length} .zip`) })})
			.catch((err) => {console.log(err)})
	}

</script>

<div style="width:{WIDTH}px; height:34px">

	{#if _.last(stack) == "Home"}
		<button style="left:0px;          width:{spreadWidth(0.17,WIDTH)}px" on:click = {pop} disabled >Up</button>
	{:else}
		<button style="left:0px;          width:{spreadWidth(0.17,WIDTH)}px" on:click = {pop} >Up</button>
	{/if}

	<button style="left:{0.17*WIDTH}px; width:{spreadWidth(0.16,WIDTH)}px" on:click = {none}>None</button>
	<button style="left:{0.33*WIDTH}px; width:{spreadWidth(0.52,WIDTH)}px" on:click = {downloadAll}>Download {n} image(s)</button>
	<button style="left:{0.85*WIDTH}px; width:{spreadWidth(0.15,WIDTH)}px" on:click = {all}>All</button>
</div>

<style>
	button {
		position:absolute;
		height:30px;
		margin:2px;
	}
	div {
		margin:0px
	}
</style>

<script>
	import _ from "lodash"
	export let big
	export let prettyFilename

	const INCR = 0.08

	let exif = null

	let path = big.path.replaceAll("_"," ").replace('.jpg','').replaceAll("\\",' • ')
	let filename = big.filename //_.last(big.filename)
//	let path = names.slice(1,names.length-1).join(' • ')
	// let path = names.join(' • ')
	
	const round = (x,n=0) => Math.round(x*Math.pow(10,n))/Math.pow(10,n)

	function getExif() {
		const img = document.getElementById("picture")
		big.bw = img.naturalWidth
		big.bh = img.naturalHeight
		big.exifState = 1
		big = big
		EXIF.getData(img, function() {
			exif = EXIF.getAllTags(this)
			if (exif.ExifVersion) {
				big.exifState = 2
				big = big
				exif.DateTimeOriginal = exif.DateTimeOriginal.replace(":","-").replace(":","-")
			}
		})
	}

	window.onscroll = (e)=> {
		e.preventDefault()
		e.stopPropagation()
		return false 
	}

	function wheel(e) {
		e.preventDefault()
		e.stopPropagation()
		if (exif == null) getExif()

		big.mouseState = 0

		const x = e.x // musens position
		const y = e.y

		const f = (skala,left,x) => (1-skala) * (x-left)
	
		let faktor = 1 + INCR
		if (e.deltaY > 0) faktor = 1/faktor

		big.left += f(faktor,big.left,x)
		big.top  += f(faktor,big.top,y)

		big.skala *= faktor

		big.width  = big.skala * big.bw
		big.height = big.skala * big.bh

		big = big
		return false 
	}

	function mousedown(e) {
		e.preventDefault()
		e.stopPropagation()
		if (exif == null) getExif()
		big.mouseState = 1
		big.startX = e.x
		big.startY = e.y
		big = big
	}

	function mousemove(e) {
		if (e.button==0 && big.mouseState==1) {
			big.left += e.x - big.startX
			big.top += e.y - big.startY
			big.startX = e.x
			big.startY = e.y
		} else {
			big.mousestate=0
		}
		big = big
	}

	function mouseup(e) {
		big.mouseState = 0
		big = big
	}

	function share () {
		const extra = `bs=${big.bs}&bw=${big.bw}&bh=${big.bh}&md5=${big.md5}&path=${big.path}&filename=${big.filename}`
		navigator.clipboard.writeText(location.origin + location.pathname + "?" + extra)
	}

	document.onmousemove = mousemove

	document.title = prettyFilename(big.filename,false)

</script>

<button on:click={share}> Share </button>

<span style="top:8%">{big.filename}</span>
<span style="top:12%">{path}</span>
{#if big.exifState >= 1}
	<span style="top:20%"> {round(big.bw * big.bh/1024/1024,1)} MP • {big.bw} x {big.bh} • {round(big.bs/1024)} kB </span>
{/if}
{#if big.exifState == 2}
	<span style="top:16%;"> {exif.DateTimeOriginal.replace(" "," • ")} </span>
	<span style="top:24%;"> {exif.Model} • f/{exif.FNumber} • 1/{1/exif.ExposureTime} • {exif.FocalLength} mm • ISO {exif.ISOSpeedRatings} </span>
	<span style="top:28%;"> © {exif.Copyright} </span>
{/if}

<img 
	id='picture'
	src={"Home/" + big.md5 + ".jpg"}
	alt=""
	on:wheel={wheel}
	on:mousedown={mousedown}
	on:mouseup={mouseup}
	on:blur={blur}
	width = {big.width}
	style = "position:absolute; left:{big.left}px; top:{big.top}px;"
>

<style>
	button {
		margin:1%
	}
	span {
		position:absolute;
		left:1%;
	}
</style>


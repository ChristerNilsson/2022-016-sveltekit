<script>
	import _ from "lodash"
	import { bilder, path } from '$lib/stores.js'
	import { log } from '$lib/utils.js'

  export let data

	function search(curr) { // returnerar lista av [sw,sh,bs,bw,bh,md5]
		const res = []
		function recurse(c,ancestors=[]) {
			log('recurse',ancestors)
			for (const key of _.keys(c)) {
				if (key.endsWith('.jpg')) {
					// const list1 = c[key].concat(ancestors)
					res.push(c[key].concat(ancestors.concat([key])))
				} else {
					recurse(c[key],ancestors.concat([key]))
				}
			}
		}
		recurse(curr)
		return res
	}

	console.log('bilder')
	$: path.set(data.slug.split('/'))

	// sök upp alla bilder via $bilder
	$: log('path',$path)

	$: curr = $bilder
	
	$: {for (const p of $path) {
		curr = curr[p]
		// log(_.keys(curr))
	}
}

	$: images  = search(curr)
	$: log(images)

</script>

{$path.join('/')}
{images.length}
<!-- <img src={'/Home/81e71fb5822ee9b2e1c2b19a6d5f7733.jpg'} alt=''/> -->

<!-- <div style='width:{innerwidth}px'>

	<h1>{filename}</h1>
	<i>{published}</i>

	<svelte:component this={data.content} />

	<h6>
	{#each words as word}
		<a href={`/query/${word}`}>{word}</a> â€¢&nbsp;
	{/each}
	</h6>

</div> -->
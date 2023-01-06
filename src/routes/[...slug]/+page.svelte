<script>
	import _ from "lodash"
	import { bilder, path } from '$lib/stores.js'
	import { log } from '$lib/utils.js'

  export let data

	function search(curr) { // returnerar lista av [sw,sh,bs,bw,bh,md5,ancestors]
		const res = []
		function recurse(c,ancestors=$path) {
			// log('recurse',ancestors)
			for (const key of _.keys(c)) {
				if (key.endsWith('.jpg')) {
					res.push(c[key].concat([ancestors.concat([key])]))
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
	// $: log('path',$path)

	$: curr = $bilder
	
	$: {for (const p of $path) {
		curr = curr[p]
		// log(_.keys(curr))
	}
}

	$: images  = search(curr)
	// $: log(images)

</script>

Antal {images.length} <br>
{$path.join('/')} <br>
{#each images as image}
	{image[6].join(' * ')}<br>
{/each}

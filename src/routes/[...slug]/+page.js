import _ from "lodash"

export const prerender = true

export async function load({ params }){
	let post = null

	console.log({params})

	// if (_.endsWith(params.slug,'.md')) {

	// 	const name = params.slug.replace('.md','')
	// 	const splitName = name.split('/')
	// 	console.log('Fetching Markdown', splitName)

	// 	// https://github.com/vitejs/vite/issues/4945#issuecomment-951770052 Troligen orsakad av kodanalys
	// 	if (splitName.length === 1) post = await import(`../../../../src/${splitName[0]}.md`)
	// 	if (splitName.length === 2) post = await import(`../../../../src/${splitName[0]}/${splitName[1]}.md`)
	// 	if (splitName.length === 3) post = await import(`../../../../src/${splitName[0]}/${splitName[1]}/${splitName[2]}.md`)
	// 	if (splitName.length === 4) post = await import(`../../../../src/${splitName[0]}/${splitName[1]}/${splitName[2]}/${splitName[3]}.md`)

	// } else {
	// 	console.log('unexpected',params.slug)
	// }

	// const content = post.default
	const slug = params.slug
	return {
		// content,
		slug
	}
}
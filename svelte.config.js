import adapter from '@sveltejs/adapter-static';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	kit: {
		adapter: adapter({strict : false}),
		alias: { 'lib/': './src/lib/' }		
	}
};

export default config;

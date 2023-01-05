import { readable } from 'svelte/store'
import { writable } from 'svelte/store'

import data from '$lib/data/bilder.json'

$: console.log('store loaded')

function stop () {}
function start (set) {return stop}

export const bilder = readable(data, start)
export const path = writable([], start)
